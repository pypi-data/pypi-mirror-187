"""
File that contains the main functionality for the Iceberg
integration within the Bodo repo. This does not contain the
main IR transformation.
"""
import os
import re
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.extending import intrinsic
import bodo
from bodo.io.fs_io import get_s3_bucket_region_njit
from bodo.io.helpers import _get_numba_typ_from_pa_typ, pyarrow_table_schema_type
from bodo.libs.array import arr_info_list_to_table, array_to_info, py_table_to_cpp_table
from bodo.libs.str_ext import unicode_to_utf8
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError


def format_iceberg_conn(conn_str: str) ->str:
    jwq__kjf = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and jwq__kjf.scheme not in (
        'iceberg', 'iceberg+file', 'iceberg+s3', 'iceberg+thrift',
        'iceberg+http', 'iceberg+https'):
        raise BodoError(
            "'con' must start with one of the following: 'iceberg://', 'iceberg+file://', 'iceberg+s3://', 'iceberg+thrift://', 'iceberg+http://', 'iceberg+https://', 'iceberg+glue'"
            )
    if sys.version_info.minor < 9:
        if conn_str.startswith('iceberg+'):
            conn_str = conn_str[len('iceberg+'):]
        if conn_str.startswith('iceberg://'):
            conn_str = conn_str[len('iceberg://'):]
    else:
        conn_str = conn_str.removeprefix('iceberg+').removeprefix('iceberg://')
    return conn_str


@numba.njit
def format_iceberg_conn_njit(conn_str):
    with numba.objmode(conn_str='unicode_type'):
        conn_str = format_iceberg_conn(conn_str)
    return conn_str


def get_iceberg_type_info(table_name: str, con: str, database_schema: str,
    is_merge_into_cow: bool=False):
    import bodo_iceberg_connector
    import numba.core
    ojkgz__nkr = None
    yyfvy__watg = None
    gsjhh__cbqa = None
    if bodo.get_rank() == 0:
        try:
            ojkgz__nkr, yyfvy__watg, gsjhh__cbqa = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if gsjhh__cbqa is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as czbb__vule:
            if isinstance(czbb__vule, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                ojkgz__nkr = BodoError(
                    f'{czbb__vule.message}: {czbb__vule.java_error}')
            else:
                ojkgz__nkr = BodoError(czbb__vule.message)
    dkz__mzcum = MPI.COMM_WORLD
    ojkgz__nkr = dkz__mzcum.bcast(ojkgz__nkr)
    if isinstance(ojkgz__nkr, Exception):
        raise ojkgz__nkr
    col_names = ojkgz__nkr
    yyfvy__watg = dkz__mzcum.bcast(yyfvy__watg)
    gsjhh__cbqa = dkz__mzcum.bcast(gsjhh__cbqa)
    bxly__bjtg = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in yyfvy__watg]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        bxly__bjtg.append(types.Array(types.int64, 1, 'C'))
    return col_names, bxly__bjtg, gsjhh__cbqa


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        flpj__lwrf = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as czbb__vule:
        if isinstance(czbb__vule, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{czbb__vule.message}:\n{czbb__vule.java_error}')
        else:
            raise BodoError(czbb__vule.message)
    return flpj__lwrf


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as czbb__vule:
        if isinstance(czbb__vule, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{czbb__vule.message}:\n{czbb__vule.java_error}')
        else:
            raise BodoError(czbb__vule.message)
    return snapshot_id


class IcebergParquetDataset:

    def __init__(self, conn, database_schema, table_name, pa_table_schema,
        pq_file_list, snapshot_id, pq_dataset=None):
        self.pq_dataset = pq_dataset
        self.conn = conn
        self.database_schema = database_schema
        self.table_name = table_name
        self.schema = pa_table_schema
        self.file_list = pq_file_list
        self.snapshot_id = snapshot_id
        self.pieces = []
        self._bodo_total_rows = 0
        self._prefix = ''
        self.filesystem = None
        if pq_dataset is not None:
            self.pieces = pq_dataset.pieces
            self._bodo_total_rows = pq_dataset._bodo_total_rows
            self._prefix = pq_dataset._prefix
            self.filesystem = pq_dataset.filesystem


def get_iceberg_pq_dataset(conn: str, database_schema: str, table_name: str,
    typing_pa_table_schema: pa.Schema, dnf_filters=None, expr_filters=None,
    tot_rows_to_read=None, is_parallel=False, get_row_counts=True):
    veyh__ytola = get_row_counts and tracing.is_tracing()
    if veyh__ytola:
        hknwt__hpq = tracing.Event('get_iceberg_pq_dataset')
    dkz__mzcum = MPI.COMM_WORLD
    qnztt__idx = None
    dpkio__pylar = None
    ojs__vpztg = None
    if bodo.get_rank() == 0:
        if veyh__ytola:
            xesuw__ezw = tracing.Event('get_iceberg_file_list', is_parallel
                =False)
            xesuw__ezw.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            qnztt__idx, ojs__vpztg = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if veyh__ytola:
                kwhrb__uddgr = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                xesuw__ezw.add_attribute('num_files', len(qnztt__idx))
                xesuw__ezw.add_attribute(f'first_{kwhrb__uddgr}_files',
                    ', '.join(qnztt__idx[:kwhrb__uddgr]))
        except Exception as czbb__vule:
            qnztt__idx = czbb__vule
        if veyh__ytola:
            xesuw__ezw.finalize()
            zemr__zgxfe = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            dpkio__pylar = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as czbb__vule:
            dpkio__pylar = czbb__vule
        if veyh__ytola:
            zemr__zgxfe.finalize()
    qnztt__idx, dpkio__pylar, ojs__vpztg = dkz__mzcum.bcast((qnztt__idx,
        dpkio__pylar, ojs__vpztg))
    if isinstance(qnztt__idx, Exception):
        khc__rnw = qnztt__idx
        raise BodoError(
            f'Error reading Iceberg Table: {type(khc__rnw).__name__}: {str(khc__rnw)}\n'
            )
    if isinstance(dpkio__pylar, Exception):
        khc__rnw = dpkio__pylar
        raise BodoError(
            f'Error reading Iceberg Table: {type(khc__rnw).__name__}: {str(khc__rnw)}\n'
            )
    fvjy__fwip: List[str] = qnztt__idx
    snapshot_id: int = dpkio__pylar
    if len(fvjy__fwip) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(fvjy__fwip,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as czbb__vule:
            if re.search('Schema .* was different', str(czbb__vule), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{czbb__vule}"""
                    )
            else:
                raise
    qonpn__qwav = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, ojs__vpztg, snapshot_id, pq_dataset)
    if veyh__ytola:
        hknwt__hpq.finalize()
    return qonpn__qwav


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        qtpy__erk = []
        for zzg__fjz in pa_schema:
            eall__afwnv = df_schema.field_by_name(zzg__fjz.name)
            if not (eall__afwnv is None and zzg__fjz.nullable):
                qtpy__erk.append(zzg__fjz)
        pa_schema = pa.schema(qtpy__erk)
    if len(pa_schema) != len(df_schema):
        return False
    for bctzj__ojwsq in range(len(df_schema)):
        eall__afwnv = df_schema.field(bctzj__ojwsq)
        zzg__fjz = pa_schema.field(bctzj__ojwsq)
        if eall__afwnv.equals(zzg__fjz):
            continue
        jgts__qxvdr = eall__afwnv.type
        mvwei__rvehu = zzg__fjz.type
        if not jgts__qxvdr.equals(mvwei__rvehu) and allow_downcasting and (
            pa.types.is_signed_integer(jgts__qxvdr) and pa.types.
            is_signed_integer(mvwei__rvehu) or pa.types.is_floating(
            jgts__qxvdr) and pa.types.is_floating(mvwei__rvehu)
            ) and jgts__qxvdr.bit_width > mvwei__rvehu.bit_width:
            eall__afwnv = eall__afwnv.with_type(mvwei__rvehu)
        if not eall__afwnv.nullable and zzg__fjz.nullable:
            eall__afwnv = eall__afwnv.with_nullable(True)
        elif allow_downcasting and eall__afwnv.nullable and not zzg__fjz.nullable:
            eall__afwnv = eall__afwnv.with_nullable(False)
        df_schema = df_schema.set(bctzj__ojwsq, eall__afwnv)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    hknwt__hpq = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    dkz__mzcum = MPI.COMM_WORLD
    llw__oixs = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    kowiu__gouu = {onstl__gtshs: lpbg__kqxkn for lpbg__kqxkn, onstl__gtshs in
        enumerate(df_schema.names)}
    if dkz__mzcum.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for himde__hhu, *hcjq__lmylt in partition_spec:
                assert himde__hhu in kowiu__gouu, f'Iceberg Partition column {himde__hhu} not found in dataframe'
            for himde__hhu, *hcjq__lmylt in sort_order:
                assert himde__hhu in kowiu__gouu, f'Iceberg Sort column {himde__hhu} not found in dataframe'
            partition_spec = [(kowiu__gouu[himde__hhu], *iiq__mejv) for 
                himde__hhu, *iiq__mejv in partition_spec]
            sort_order = [(kowiu__gouu[himde__hhu], *iiq__mejv) for 
                himde__hhu, *iiq__mejv in sort_order]
            if if_exists == 'append' and pa_schema is not None:
                if not are_schemas_compatible(pa_schema, df_schema,
                    allow_downcasting):
                    if numba.core.config.DEVELOPER_MODE:
                        raise BodoError(
                            f"""DataFrame schema needs to be an ordered subset of Iceberg table for append

Iceberg:
{pa_schema}

DataFrame:
{df_schema}
"""
                            )
                    else:
                        raise BodoError(
                            'DataFrame schema needs to be an ordered subset of Iceberg table for append'
                            )
            if iceberg_schema_id is None:
                iceberg_schema_str = connector.pyarrow_to_iceberg_schema_str(
                    df_schema)
        except connector.IcebergError as czbb__vule:
            if isinstance(czbb__vule, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                llw__oixs = BodoError(
                    f'{czbb__vule.message}: {czbb__vule.java_error}')
            else:
                llw__oixs = BodoError(czbb__vule.message)
        except Exception as czbb__vule:
            llw__oixs = czbb__vule
    llw__oixs = dkz__mzcum.bcast(llw__oixs)
    if isinstance(llw__oixs, Exception):
        raise llw__oixs
    table_loc = dkz__mzcum.bcast(table_loc)
    iceberg_schema_id = dkz__mzcum.bcast(iceberg_schema_id)
    partition_spec = dkz__mzcum.bcast(partition_spec)
    sort_order = dkz__mzcum.bcast(sort_order)
    iceberg_schema_str = dkz__mzcum.bcast(iceberg_schema_str)
    pa_schema = dkz__mzcum.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    hknwt__hpq.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    dkz__mzcum = MPI.COMM_WORLD
    msv__zbv = [zby__xha[0] for zby__xha in iceberg_files_info]
    bijpv__fnx = dkz__mzcum.gather(msv__zbv)
    fnames = [gcp__kbru for xya__caay in bijpv__fnx for gcp__kbru in xya__caay
        ] if dkz__mzcum.Get_rank() == 0 else None
    niyr__qsnl = np.array([zby__xha[1] for zby__xha in iceberg_files_info],
        dtype=np.int64)
    kiaj__rqaee = np.array([zby__xha[2] for zby__xha in iceberg_files_info],
        dtype=np.int64)
    cvbe__vqlbs = bodo.gatherv(niyr__qsnl).tolist()
    cfke__ykl = bodo.gatherv(kiaj__rqaee).tolist()
    return fnames, cvbe__vqlbs, cfke__ykl


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    hknwt__hpq = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    dkz__mzcum = MPI.COMM_WORLD
    success = False
    if dkz__mzcum.Get_rank() == 0:
        crkkn__ejaa = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, crkkn__ejaa,
            pa_schema, partition_spec, sort_order, mode)
    success = dkz__mzcum.bcast(success)
    hknwt__hpq.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    hknwt__hpq = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    dkz__mzcum = MPI.COMM_WORLD
    success = False
    if dkz__mzcum.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = dkz__mzcum.bcast(success)
    hknwt__hpq.finalize()
    return success


from numba.extending import NativeValue, box, models, register_model, unbox


class PythonListOfHeterogeneousTuples(types.Opaque):

    def __init__(self):
        super(PythonListOfHeterogeneousTuples, self).__init__(name=
            'PythonListOfHeterogeneousTuples')


python_list_of_heterogeneous_tuples_type = PythonListOfHeterogeneousTuples()
types.python_list_of_heterogeneous_tuples_type = (
    python_list_of_heterogeneous_tuples_type)
register_model(PythonListOfHeterogeneousTuples)(models.OpaqueModel)


@unbox(PythonListOfHeterogeneousTuples)
def unbox_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PythonListOfHeterogeneousTuples)
def box_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return val


this_module = sys.modules[__name__]
PyObjectOfList = install_py_obj_class(types_name='pyobject_of_list_type',
    python_type=None, module=this_module, class_name='PyObjectOfListType',
    model_name='PyObjectOfListModel')


@numba.njit()
def iceberg_pq_write(table_loc, bodo_table, col_names, partition_spec,
    sort_order, iceberg_schema_str, is_parallel, expected_schema):
    bucket_region = get_s3_bucket_region_njit(table_loc, is_parallel)
    yamol__kpc = 'snappy'
    dqft__pbafe = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(yamol__kpc), is_parallel, unicode_to_utf8(
        bucket_region), dqft__pbafe, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    hknwt__hpq = tracing.Event('iceberg_write_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        iceberg_schema_id='i8', partition_spec=
        'python_list_of_heterogeneous_tuples_type', sort_order=
        'python_list_of_heterogeneous_tuples_type', iceberg_schema_str=
        'unicode_type', expected_schema='pyarrow_table_schema_type'):
        (already_exists, table_loc, iceberg_schema_id, partition_spec,
            sort_order, iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, if_exists, allow_downcasting))
    if already_exists and if_exists == 'fail':
        raise ValueError(f'Table already exists.')
    if already_exists:
        mode = if_exists
    else:
        mode = 'create'
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, cvbe__vqlbs, cfke__ykl = collect_file_info(iceberg_files_info)
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': cfke__ykl, 'record_count':
            cvbe__vqlbs}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    hknwt__hpq.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    lbbki__nwpj = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        nxlfm__kez = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), nxlfm__kez),
                snapshot_id, old_fnames, array_to_info(lbbki__nwpj),
                df_pyarrow_schema, is_parallel)
    else:
        xjl__meg = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(lpbg__kqxkn) for lpbg__kqxkn in range(len(bodo_df.columns))
            )
        luqv__gpl = 'def impl(\n'
        luqv__gpl += '    table_name,\n'
        luqv__gpl += '    conn,\n'
        luqv__gpl += '    database_schema,\n'
        luqv__gpl += '    bodo_df,\n'
        luqv__gpl += '    snapshot_id,\n'
        luqv__gpl += '    old_fnames,\n'
        luqv__gpl += '    is_parallel=False,\n'
        luqv__gpl += '):\n'
        luqv__gpl += '    info_list = [{}]\n'.format(xjl__meg)
        luqv__gpl += '    table = arr_info_list_to_table(info_list)\n'
        luqv__gpl += '    iceberg_merge_cow(\n'
        luqv__gpl += '        table_name,\n'
        luqv__gpl += '        format_iceberg_conn_njit(conn),\n'
        luqv__gpl += '        database_schema,\n'
        luqv__gpl += '        table,\n'
        luqv__gpl += '        snapshot_id,\n'
        luqv__gpl += '        old_fnames,\n'
        luqv__gpl += '        array_to_info(col_names_py),\n'
        luqv__gpl += '        df_pyarrow_schema,\n'
        luqv__gpl += '        is_parallel,\n'
        luqv__gpl += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': lbbki__nwpj, 'df_pyarrow_schema': df_pyarrow_schema
            }
        exec(luqv__gpl, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    hknwt__hpq = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, hcjq__lmylt, partition_spec, sort_order,
            iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, 'append', allow_downcasting
            =True))
    if not already_exists:
        raise ValueError(f'Iceberg MERGE INTO: Table does not exist at write')
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, cvbe__vqlbs, cfke__ykl = collect_file_info(iceberg_files_info)
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size': cfke__ykl,
            'record_count': cvbe__vqlbs}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    hknwt__hpq.finalize()


import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('iceberg_pq_write', arrow_cpp.iceberg_pq_write)


@intrinsic
def iceberg_pq_write_table_cpp(typingctx, table_data_loc_t, table_t,
    col_names_t, partition_spec_t, sort_order_t, compression_t,
    is_parallel_t, bucket_region, row_group_size, iceberg_metadata_t,
    iceberg_schema_t):

    def codegen(context, builder, sig, args):
        xtiu__qnqx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        lyscc__zmh = cgutils.get_or_insert_function(builder.module,
            xtiu__qnqx, name='iceberg_pq_write')
        gdj__ovl = builder.call(lyscc__zmh, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return gdj__ovl
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
