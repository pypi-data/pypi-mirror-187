import os
import shutil
from contextlib import contextmanager
import pandas as pd
import bodo


@bodo.jit
def get_rank():
    return bodo.libs.distributed_api.get_rank()


@bodo.jit
def barrier():
    return bodo.libs.distributed_api.barrier()


@contextmanager
def ensure_clean(filename):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(filename) and os.path.isfile(
                filename):
                os.remove(filename)
        except Exception as swxxx__kyejr:
            print('Exception on removing file: {error}'.format(error=
                swxxx__kyejr))


@contextmanager
def ensure_clean_dir(dirname):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(dirname) and os.path.isdir(
                dirname):
                shutil.rmtree(dirname)
        except Exception as swxxx__kyejr:
            print('Exception on removing directory: {error}'.format(error=
                swxxx__kyejr))


@contextmanager
def ensure_clean2(pathname):
    try:
        yield
    finally:
        barrier()
        if get_rank() == 0:
            try:
                if os.path.exists(pathname) and os.path.isfile(pathname):
                    os.remove(pathname)
            except Exception as swxxx__kyejr:
                print('Exception on removing file: {error}'.format(error=
                    swxxx__kyejr))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as swxxx__kyejr:
                print('Exception on removing directory: {error}'.format(
                    error=swxxx__kyejr))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    pwz__yhemk = MPI.COMM_WORLD
    try:
        ckvrr__dpfd = None
        if bodo.get_rank() == 0:
            ckvrr__dpfd = f'{table_name_prefix}_{uuid.uuid4().hex}'
        ckvrr__dpfd = pwz__yhemk.bcast(ckvrr__dpfd)
        yield ckvrr__dpfd
    finally:
        bodo.barrier()
        azy__yits = None
        if bodo.get_rank() == 0:
            try:
                njth__kmi = create_engine(conn)
                dzi__lpxn = njth__kmi.connect()
                dzi__lpxn.execute(f'drop table if exists {ckvrr__dpfd}')
            except Exception as swxxx__kyejr:
                azy__yits = swxxx__kyejr
        azy__yits = pwz__yhemk.bcast(azy__yits)
        if isinstance(azy__yits, Exception):
            raise azy__yits


@contextmanager
def ensure_clean_snowflake_table(conn, table_name_prefix='test_table',
    parallel=True):
    import uuid
    from mpi4py import MPI
    pwz__yhemk = MPI.COMM_WORLD
    try:
        ckvrr__dpfd = None
        if bodo.get_rank() == 0 or not parallel:
            ckvrr__dpfd = f'{table_name_prefix}_{uuid.uuid4().hex}'.upper()
        if parallel:
            ckvrr__dpfd = pwz__yhemk.bcast(ckvrr__dpfd)
        yield ckvrr__dpfd
    finally:
        if parallel:
            bodo.barrier()
        azy__yits = None
        if bodo.get_rank() == 0 or not parallel:
            try:
                pd.read_sql(f'drop table if exists {ckvrr__dpfd}', conn)
            except Exception as swxxx__kyejr:
                azy__yits = swxxx__kyejr
        if parallel:
            azy__yits = pwz__yhemk.bcast(azy__yits)
        if isinstance(azy__yits, Exception):
            raise azy__yits
