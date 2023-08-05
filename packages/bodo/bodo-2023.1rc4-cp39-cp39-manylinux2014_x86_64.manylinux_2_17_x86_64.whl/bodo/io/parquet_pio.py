import os
import warnings
from collections import defaultdict
from glob import has_magic
from typing import Optional
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
import pyarrow
import pyarrow as pa
import pyarrow.dataset as ds
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, models, overload, register_model, unbox
from pyarrow._fs import PyFileSystem
from pyarrow.fs import FSSpecHandler
import bodo
import bodo.utils.tracing as tracing
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path
from bodo.io.helpers import _get_numba_typ_from_pa_typ
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, FileSchema, get_overload_const_str
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ParquetPredicateType)
def box_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return val


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None, use_hive=True):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        self.use_hive = use_hive
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols, use_hive=self.use_hive)
        except OSError as tgzwh__ykgrp:
            if 'non-file path' in str(tgzwh__ykgrp):
                raise FileNotFoundError(str(tgzwh__ykgrp))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    hsac__ifibw = get_overload_const_str(dnf_filter_str)
    ehjeq__urevx = get_overload_const_str(expr_filter_str)
    fapb__ilvpu = ', '.join(f'f{byayo__tau}' for byayo__tau in range(len(
        var_tup)))
    zfysn__zkm = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        zfysn__zkm += f'  {fapb__ilvpu}, = var_tup\n'
    zfysn__zkm += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    zfysn__zkm += f'    dnf_filters_py = {hsac__ifibw}\n'
    zfysn__zkm += f'    expr_filters_py = {ehjeq__urevx}\n'
    zfysn__zkm += '  return (dnf_filters_py, expr_filters_py)\n'
    rcf__kcnb = {}
    ocruj__xlaaa = globals()
    ocruj__xlaaa['numba'] = numba
    exec(zfysn__zkm, ocruj__xlaaa, rcf__kcnb)
    return rcf__kcnb['impl']


def unify_schemas(schemas):
    uajw__gsndb = []
    for schema in schemas:
        for byayo__tau in range(len(schema)):
            ecj__yuuc = schema.field(byayo__tau)
            if ecj__yuuc.type == pa.large_string():
                schema = schema.set(byayo__tau, ecj__yuuc.with_type(pa.
                    string()))
            elif ecj__yuuc.type == pa.large_binary():
                schema = schema.set(byayo__tau, ecj__yuuc.with_type(pa.
                    binary()))
            elif isinstance(ecj__yuuc.type, (pa.ListType, pa.LargeListType)
                ) and ecj__yuuc.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(byayo__tau, ecj__yuuc.with_type(pa.
                    list_(pa.field(ecj__yuuc.type.value_field.name, pa.
                    string()))))
            elif isinstance(ecj__yuuc.type, pa.LargeListType):
                schema = schema.set(byayo__tau, ecj__yuuc.with_type(pa.
                    list_(pa.field(ecj__yuuc.type.value_field.name,
                    ecj__yuuc.type.value_type))))
        uajw__gsndb.append(schema)
    return pa.unify_schemas(uajw__gsndb)


class ParquetDataset:

    def __init__(self, pa_pq_dataset, prefix=''):
        self.schema: pa.Schema = pa_pq_dataset.schema
        self.filesystem = None
        self._bodo_total_rows = 0
        self._prefix = prefix
        self.partitioning = None
        partitioning = pa_pq_dataset.partitioning
        self.partition_names = ([] if partitioning is None or partitioning.
            schema == pa_pq_dataset.schema else list(partitioning.schema.names)
            )
        if self.partition_names:
            self.partitioning_dictionaries = partitioning.dictionaries
            self.partitioning_cls = partitioning.__class__
            self.partitioning_schema = partitioning.schema
        else:
            self.partitioning_dictionaries = {}
        for byayo__tau in range(len(self.schema)):
            ecj__yuuc = self.schema.field(byayo__tau)
            if ecj__yuuc.type == pa.large_string():
                self.schema = self.schema.set(byayo__tau, ecj__yuuc.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for zgde__bro in self.pieces:
            zgde__bro.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            yixlw__mbzqd = {zgde__bro: self.partitioning_dictionaries[
                byayo__tau] for byayo__tau, zgde__bro in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, yixlw__mbzqd)


class ParquetPiece(object):

    def __init__(self, frag, partitioning, partition_names):
        self._frag = None
        self.format = frag.format
        self.path = frag.path
        self._bodo_num_rows = 0
        self.partition_keys = []
        if partitioning is not None:
            self.partition_keys = ds._get_partition_keys(frag.
                partition_expression)
            self.partition_keys = [(kach__morix, partitioning.dictionaries[
                byayo__tau].index(self.partition_keys[kach__morix]).as_py()
                ) for byayo__tau, kach__morix in enumerate(partition_names)]

    @property
    def frag(self):
        if self._frag is None:
            self._frag = self.format.make_fragment(self.path, self.filesystem)
            del self.format
        return self._frag

    @property
    def metadata(self):
        return self.frag.metadata

    @property
    def num_row_groups(self):
        return self.frag.num_row_groups


def get_parquet_dataset(fpath, get_row_counts: bool=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories: bool=False,
    is_parallel=False, tot_rows_to_read: Optional[int]=None,
    typing_pa_schema: Optional[pa.Schema]=None, use_hive: bool=True,
    partitioning='hive') ->ParquetDataset:
    if not use_hive:
        partitioning = None
    if get_row_counts:
        rnc__ommmp = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    rkdf__mni = MPI.COMM_WORLD
    if isinstance(fpath, list):
        jlu__pfbjh = urlparse(fpath[0])
        protocol = jlu__pfbjh.scheme
        wobo__laua = jlu__pfbjh.netloc
        for byayo__tau in range(len(fpath)):
            ecj__yuuc = fpath[byayo__tau]
            hdzck__dle = urlparse(ecj__yuuc)
            if hdzck__dle.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if hdzck__dle.netloc != wobo__laua:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[byayo__tau] = ecj__yuuc.rstrip('/')
    else:
        jlu__pfbjh = urlparse(fpath)
        protocol = jlu__pfbjh.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as kftsr__lyp:
            shbuq__vyk = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(shbuq__vyk)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as kftsr__lyp:
            shbuq__vyk = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            cbo__gav = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(cbo__gav)))
        elif protocol == 'http':
            fs.append(PyFileSystem(FSSpecHandler(fsspec.filesystem('http'))))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(pa.fs.LocalFileSystem())
        return fs[0]

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pa.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            xekrp__hfcr = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(xekrp__hfcr) == 0:
            raise BodoError('No files found matching glob pattern')
        return xekrp__hfcr
    ufaoy__tcu = False
    if get_row_counts:
        fwfo__sjgrr = getfs(parallel=True)
        ufaoy__tcu = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        dfb__kir = 1
        cuq__krot = os.cpu_count()
        if cuq__krot is not None and cuq__krot > 1:
            dfb__kir = cuq__krot // 2
        try:
            if get_row_counts:
                awhj__xluf = tracing.Event('pq.ParquetDataset', is_parallel
                    =False)
                if tracing.is_tracing():
                    awhj__xluf.add_attribute('g_dnf_filter', str(dnf_filters))
            vqtma__sqer = pa.io_thread_count()
            pa.set_io_thread_count(dfb__kir)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{jlu__pfbjh.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    godsx__folqy = [ecj__yuuc[len(prefix):] for ecj__yuuc in
                        fpath]
                else:
                    godsx__folqy = fpath[len(prefix):]
            else:
                godsx__folqy = fpath
            if isinstance(godsx__folqy, list):
                ikb__sfwu = []
                for zgde__bro in godsx__folqy:
                    if has_magic(zgde__bro):
                        ikb__sfwu += glob(protocol, getfs(), zgde__bro)
                    else:
                        ikb__sfwu.append(zgde__bro)
                godsx__folqy = ikb__sfwu
            elif has_magic(godsx__folqy):
                godsx__folqy = glob(protocol, getfs(), godsx__folqy)
            uzwk__stymw = pq.ParquetDataset(godsx__folqy, filesystem=getfs(
                ), filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                uzwk__stymw._filters = dnf_filters
                uzwk__stymw._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            cpi__crd = len(uzwk__stymw.files)
            uzwk__stymw = ParquetDataset(uzwk__stymw, prefix)
            pa.set_io_thread_count(vqtma__sqer)
            if typing_pa_schema:
                uzwk__stymw.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    awhj__xluf.add_attribute('num_pieces_before_filter',
                        cpi__crd)
                    awhj__xluf.add_attribute('num_pieces_after_filter', len
                        (uzwk__stymw.pieces))
                awhj__xluf.finalize()
        except Exception as tgzwh__ykgrp:
            if isinstance(tgzwh__ykgrp, IsADirectoryError):
                tgzwh__ykgrp = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(tgzwh__ykgrp, (
                OSError, FileNotFoundError)):
                tgzwh__ykgrp = BodoError(str(tgzwh__ykgrp) +
                    list_of_files_error_msg)
            else:
                tgzwh__ykgrp = BodoError(
                    f"""error from pyarrow: {type(tgzwh__ykgrp).__name__}: {str(tgzwh__ykgrp)}
"""
                    )
            rkdf__mni.bcast(tgzwh__ykgrp)
            raise tgzwh__ykgrp
        if get_row_counts:
            wslr__dfsqe = tracing.Event('bcast dataset')
        uzwk__stymw = rkdf__mni.bcast(uzwk__stymw)
    else:
        if get_row_counts:
            wslr__dfsqe = tracing.Event('bcast dataset')
        uzwk__stymw = rkdf__mni.bcast(None)
        if isinstance(uzwk__stymw, Exception):
            cxpvk__egy = uzwk__stymw
            raise cxpvk__egy
    uzwk__stymw.set_fs(getfs())
    if get_row_counts:
        wslr__dfsqe.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = ufaoy__tcu = False
    if get_row_counts or ufaoy__tcu:
        if get_row_counts and tracing.is_tracing():
            nhb__vago = tracing.Event('get_row_counts')
            nhb__vago.add_attribute('g_num_pieces', len(uzwk__stymw.pieces))
            nhb__vago.add_attribute('g_expr_filters', str(expr_filters))
        artb__pqqpi = 0.0
        num_pieces = len(uzwk__stymw.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        mapu__esqun = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        syahy__zzhfy = 0
        lxbt__ayv = 0
        xisaf__til = 0
        kiipu__nbp = True
        if expr_filters is not None:
            import random
            random.seed(37)
            unt__gcti = random.sample(uzwk__stymw.pieces, k=len(uzwk__stymw
                .pieces))
        else:
            unt__gcti = uzwk__stymw.pieces
        fpaths = [zgde__bro.path for zgde__bro in unt__gcti[start:mapu__esqun]]
        dfb__kir = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(dfb__kir)
        pa.set_cpu_count(dfb__kir)
        cxpvk__egy = None
        try:
            kra__rwb = ds.dataset(fpaths, filesystem=uzwk__stymw.filesystem,
                partitioning=uzwk__stymw.partitioning)
            for fuy__andy, frag in zip(unt__gcti[start:mapu__esqun],
                kra__rwb.get_fragments()):
                if ufaoy__tcu:
                    lxb__tthpn = frag.metadata.schema.to_arrow_schema()
                    juz__zlkrc = set(lxb__tthpn.names)
                    molmu__dyjab = set(uzwk__stymw.schema.names) - set(
                        uzwk__stymw.partition_names)
                    if molmu__dyjab != juz__zlkrc:
                        pki__cdufc = juz__zlkrc - molmu__dyjab
                        pausc__gnsxh = molmu__dyjab - juz__zlkrc
                        lge__yyl = f'Schema in {fuy__andy} was different.\n'
                        if typing_pa_schema is not None:
                            if pki__cdufc:
                                lge__yyl += f"""File contains column(s) {pki__cdufc} not found in other files in the dataset.
"""
                                raise BodoError(lge__yyl)
                        else:
                            if pki__cdufc:
                                lge__yyl += f"""File contains column(s) {pki__cdufc} not found in other files in the dataset.
"""
                            if pausc__gnsxh:
                                lge__yyl += f"""File missing column(s) {pausc__gnsxh} found in other files in the dataset.
"""
                            raise BodoError(lge__yyl)
                    try:
                        uzwk__stymw.schema = unify_schemas([uzwk__stymw.
                            schema, lxb__tthpn])
                    except Exception as tgzwh__ykgrp:
                        lge__yyl = (
                            f'Schema in {fuy__andy} was different.\n' + str
                            (tgzwh__ykgrp))
                        raise BodoError(lge__yyl)
                fbvy__hlxy = time.time()
                kra__cbd = frag.scanner(schema=kra__rwb.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                artb__pqqpi += time.time() - fbvy__hlxy
                fuy__andy._bodo_num_rows = kra__cbd
                syahy__zzhfy += kra__cbd
                lxbt__ayv += frag.num_row_groups
                xisaf__til += sum(wzl__pjwrq.total_byte_size for wzl__pjwrq in
                    frag.row_groups)
        except Exception as tgzwh__ykgrp:
            cxpvk__egy = tgzwh__ykgrp
        if rkdf__mni.allreduce(cxpvk__egy is not None, op=MPI.LOR):
            for cxpvk__egy in rkdf__mni.allgather(cxpvk__egy):
                if cxpvk__egy:
                    if isinstance(fpath, list) and isinstance(cxpvk__egy, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(cxpvk__egy) +
                            list_of_files_error_msg)
                    raise cxpvk__egy
        if ufaoy__tcu:
            kiipu__nbp = rkdf__mni.allreduce(kiipu__nbp, op=MPI.LAND)
            if not kiipu__nbp:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            uzwk__stymw._bodo_total_rows = rkdf__mni.allreduce(syahy__zzhfy,
                op=MPI.SUM)
            ldfzb__ebefu = rkdf__mni.allreduce(lxbt__ayv, op=MPI.SUM)
            csf__svu = rkdf__mni.allreduce(xisaf__til, op=MPI.SUM)
            dqyft__olc = np.array([zgde__bro._bodo_num_rows for zgde__bro in
                uzwk__stymw.pieces])
            dqyft__olc = rkdf__mni.allreduce(dqyft__olc, op=MPI.SUM)
            for zgde__bro, rpatz__qdws in zip(uzwk__stymw.pieces, dqyft__olc):
                zgde__bro._bodo_num_rows = rpatz__qdws
            if is_parallel and bodo.get_rank(
                ) == 0 and ldfzb__ebefu < bodo.get_size(
                ) and ldfzb__ebefu != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({ldfzb__ebefu}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if ldfzb__ebefu == 0:
                phnvl__ahjbk = 0
            else:
                phnvl__ahjbk = csf__svu // ldfzb__ebefu
            if (bodo.get_rank() == 0 and csf__svu >= 20 * 1048576 and 
                phnvl__ahjbk < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({phnvl__ahjbk} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                nhb__vago.add_attribute('g_total_num_row_groups', ldfzb__ebefu)
                nhb__vago.add_attribute('total_scan_time', artb__pqqpi)
                zcptm__ocuj = np.array([zgde__bro._bodo_num_rows for
                    zgde__bro in uzwk__stymw.pieces])
                jafn__rgaa = np.percentile(zcptm__ocuj, [25, 50, 75])
                nhb__vago.add_attribute('g_row_counts_min', zcptm__ocuj.min())
                nhb__vago.add_attribute('g_row_counts_Q1', jafn__rgaa[0])
                nhb__vago.add_attribute('g_row_counts_median', jafn__rgaa[1])
                nhb__vago.add_attribute('g_row_counts_Q3', jafn__rgaa[2])
                nhb__vago.add_attribute('g_row_counts_max', zcptm__ocuj.max())
                nhb__vago.add_attribute('g_row_counts_mean', zcptm__ocuj.mean()
                    )
                nhb__vago.add_attribute('g_row_counts_std', zcptm__ocuj.std())
                nhb__vago.add_attribute('g_row_counts_sum', zcptm__ocuj.sum())
                nhb__vago.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(uzwk__stymw)
    if get_row_counts:
        rnc__ommmp.finalize()
    if ufaoy__tcu:
        if tracing.is_tracing():
            kyfj__mms = tracing.Event('unify_schemas_across_ranks')
        cxpvk__egy = None
        try:
            uzwk__stymw.schema = rkdf__mni.allreduce(uzwk__stymw.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as tgzwh__ykgrp:
            cxpvk__egy = tgzwh__ykgrp
        if tracing.is_tracing():
            kyfj__mms.finalize()
        if rkdf__mni.allreduce(cxpvk__egy is not None, op=MPI.LOR):
            for cxpvk__egy in rkdf__mni.allgather(cxpvk__egy):
                if cxpvk__egy:
                    lge__yyl = f'Schema in some files were different.\n' + str(
                        cxpvk__egy)
                    raise BodoError(lge__yyl)
    return uzwk__stymw


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    cuq__krot = os.cpu_count()
    if cuq__krot is None or cuq__krot == 0:
        cuq__krot = 2
    jri__wiv = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), cuq__krot)
    viq__dpdn = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), cuq__krot)
    if is_parallel and len(fpaths) > viq__dpdn and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(viq__dpdn)
        pa.set_cpu_count(viq__dpdn)
    else:
        pa.set_io_thread_count(jri__wiv)
        pa.set_cpu_count(jri__wiv)
    ydge__spjkn = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    blehe__ufgh = set(str_as_dict_cols)
    for byayo__tau, name in enumerate(schema.names):
        if name in blehe__ufgh:
            bvf__rlej = schema.field(byayo__tau)
            omywb__qype = pa.field(name, pa.dictionary(pa.int32(),
                bvf__rlej.type), bvf__rlej.nullable)
            schema = schema.remove(byayo__tau).insert(byayo__tau, omywb__qype)
    uzwk__stymw = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=ydge__spjkn)
    dygnl__hkoh = uzwk__stymw.schema.names
    trwi__rgdcj = [dygnl__hkoh[lbq__czzzf] for lbq__czzzf in selected_fields]
    qexol__vbbri = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if qexol__vbbri and expr_filters is None:
        vsqjw__oatat = []
        vmz__hxq = 0
        zdddh__gjzjp = 0
        for frag in uzwk__stymw.get_fragments():
            gqwa__xdx = []
            for wzl__pjwrq in frag.row_groups:
                wsqh__hdir = wzl__pjwrq.num_rows
                if start_offset < vmz__hxq + wsqh__hdir:
                    if zdddh__gjzjp == 0:
                        mte__jyh = start_offset - vmz__hxq
                        secu__rzbe = min(wsqh__hdir - mte__jyh, rows_to_read)
                    else:
                        secu__rzbe = min(wsqh__hdir, rows_to_read -
                            zdddh__gjzjp)
                    zdddh__gjzjp += secu__rzbe
                    gqwa__xdx.append(wzl__pjwrq.id)
                vmz__hxq += wsqh__hdir
                if zdddh__gjzjp == rows_to_read:
                    break
            vsqjw__oatat.append(frag.subset(row_group_ids=gqwa__xdx))
            if zdddh__gjzjp == rows_to_read:
                break
        uzwk__stymw = ds.FileSystemDataset(vsqjw__oatat, uzwk__stymw.schema,
            ydge__spjkn, filesystem=uzwk__stymw.filesystem)
        start_offset = mte__jyh
    bzjp__qjyt = uzwk__stymw.scanner(columns=trwi__rgdcj, filter=
        expr_filters, use_threads=True).to_reader()
    return uzwk__stymw, bzjp__qjyt, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    izbtw__exqez = [c for c in pa_schema.names if isinstance(pa_schema.
        field(c).type, pa.DictionaryType) and c not in pq_dataset.
        partition_names]
    if len(izbtw__exqez) == 0:
        pq_dataset._category_info = {}
        return
    rkdf__mni = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            jjjjz__qvelu = pq_dataset.pieces[0].frag.head(100, columns=
                izbtw__exqez)
            heb__pielb = {c: tuple(jjjjz__qvelu.column(c).chunk(0).
                dictionary.to_pylist()) for c in izbtw__exqez}
            del jjjjz__qvelu
        except Exception as tgzwh__ykgrp:
            rkdf__mni.bcast(tgzwh__ykgrp)
            raise tgzwh__ykgrp
        rkdf__mni.bcast(heb__pielb)
    else:
        heb__pielb = rkdf__mni.bcast(None)
        if isinstance(heb__pielb, Exception):
            cxpvk__egy = heb__pielb
            raise cxpvk__egy
    pq_dataset._category_info = heb__pielb


def get_pandas_metadata(schema, num_pieces):
    rsk__svu = None
    iexc__gpeq = defaultdict(lambda : None)
    qgyvj__wqnbu = b'pandas'
    if schema.metadata is not None and qgyvj__wqnbu in schema.metadata:
        import json
        yvk__ihjg = json.loads(schema.metadata[qgyvj__wqnbu].decode('utf8'))
        qhlp__rnbb = len(yvk__ihjg['index_columns'])
        if qhlp__rnbb > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        rsk__svu = yvk__ihjg['index_columns'][0] if qhlp__rnbb else None
        if not isinstance(rsk__svu, str) and not isinstance(rsk__svu, dict):
            rsk__svu = None
        for uikp__xnp in yvk__ihjg['columns']:
            xikw__wdbvn = uikp__xnp['name']
            vsxzg__iqr = uikp__xnp['pandas_type']
            if (vsxzg__iqr.startswith('int') or vsxzg__iqr.startswith('float')
                ) and xikw__wdbvn is not None:
                qao__faha = uikp__xnp['numpy_type']
                if qao__faha.startswith('Int') or qao__faha.startswith('Float'
                    ):
                    iexc__gpeq[xikw__wdbvn] = True
                else:
                    iexc__gpeq[xikw__wdbvn] = False
    return rsk__svu, iexc__gpeq


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for xikw__wdbvn in pa_schema.names:
        kwalj__zsn = pa_schema.field(xikw__wdbvn)
        if kwalj__zsn.type in (pa.string(), pa.large_string()):
            str_columns.append(xikw__wdbvn)
    return str_columns


def _pa_schemas_match(pa_schema1, pa_schema2):
    if pa_schema1.names != pa_schema2.names:
        return False
    try:
        unify_schemas([pa_schema1, pa_schema2])
    except:
        return False
    return True


def _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg):
    unt__gcti = pq_dataset.pieces
    if len(unt__gcti) > bodo.get_size():
        import random
        random.seed(37)
        unt__gcti = random.sample(unt__gcti, bodo.get_size())
    else:
        unt__gcti = unt__gcti
    if is_iceberg:
        unt__gcti = [zgde__bro for zgde__bro in unt__gcti if
            _pa_schemas_match(zgde__bro.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return unt__gcti


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    rkdf__mni = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    unt__gcti = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    oirz__cmbe = np.zeros(len(str_columns), dtype=np.int64)
    hyaw__dhpz = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(unt__gcti):
        fuy__andy = unt__gcti[bodo.get_rank()]
        try:
            metadata = fuy__andy.metadata
            for byayo__tau in range(fuy__andy.num_row_groups):
                for uou__uwjaj, xikw__wdbvn in enumerate(str_columns):
                    eock__vsmwj = pa_schema.get_field_index(xikw__wdbvn)
                    oirz__cmbe[uou__uwjaj] += metadata.row_group(byayo__tau
                        ).column(eock__vsmwj).total_uncompressed_size
            omvn__uxx = metadata.num_rows
        except Exception as tgzwh__ykgrp:
            if isinstance(tgzwh__ykgrp, (OSError, FileNotFoundError)):
                omvn__uxx = 0
            else:
                raise
    else:
        omvn__uxx = 0
    xqmgo__wfzzi = rkdf__mni.allreduce(omvn__uxx, op=MPI.SUM)
    if xqmgo__wfzzi == 0:
        return set()
    rkdf__mni.Allreduce(oirz__cmbe, hyaw__dhpz, op=MPI.SUM)
    goyi__xqpdu = hyaw__dhpz / xqmgo__wfzzi
    mmwru__phtth = set()
    for byayo__tau, mwp__ctoi in enumerate(goyi__xqpdu):
        if mwp__ctoi < READ_STR_AS_DICT_THRESHOLD:
            xikw__wdbvn = str_columns[byayo__tau]
            mmwru__phtth.add(xikw__wdbvn)
    return mmwru__phtth


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    dygnl__hkoh = []
    vjivc__cmeg = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    vsxnm__lxpk = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    xtt__bvmw = read_as_dict_cols - vsxnm__lxpk
    if len(xtt__bvmw) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {xtt__bvmw}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(vsxnm__lxpk)
    vsxnm__lxpk = vsxnm__lxpk - read_as_dict_cols
    str_columns = [dyk__ctn for dyk__ctn in str_columns if dyk__ctn in
        vsxnm__lxpk]
    mmwru__phtth = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    mmwru__phtth.update(read_as_dict_cols)
    dygnl__hkoh = pa_schema.names
    rsk__svu, iexc__gpeq = get_pandas_metadata(pa_schema, num_pieces)
    wdqt__qgl = []
    cxep__clp = []
    cjy__iop = []
    for byayo__tau, c in enumerate(dygnl__hkoh):
        if c in partition_names:
            continue
        kwalj__zsn = pa_schema.field(c)
        mlp__awkio, ymks__axn = _get_numba_typ_from_pa_typ(kwalj__zsn, c ==
            rsk__svu, iexc__gpeq[c], pq_dataset._category_info, str_as_dict
            =c in mmwru__phtth)
        wdqt__qgl.append(mlp__awkio)
        cxep__clp.append(ymks__axn)
        cjy__iop.append(kwalj__zsn.type)
    if partition_names:
        wdqt__qgl += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[byayo__tau]) for byayo__tau in range(
            len(partition_names))]
        cxep__clp.extend([True] * len(partition_names))
        cjy__iop.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        dygnl__hkoh += [input_file_name_col]
        wdqt__qgl += [dict_str_arr_type]
        cxep__clp.append(True)
        cjy__iop.append(None)
    fzud__buv = {c: byayo__tau for byayo__tau, c in enumerate(dygnl__hkoh)}
    if selected_columns is None:
        selected_columns = dygnl__hkoh
    for c in selected_columns:
        if c not in fzud__buv:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if rsk__svu and not isinstance(rsk__svu, dict
        ) and rsk__svu not in selected_columns:
        selected_columns.append(rsk__svu)
    dygnl__hkoh = selected_columns
    wrvjy__rvx = []
    vjivc__cmeg = []
    fsuoh__tbk = []
    jeap__gglzt = []
    for byayo__tau, c in enumerate(dygnl__hkoh):
        nylgn__got = fzud__buv[c]
        wrvjy__rvx.append(nylgn__got)
        vjivc__cmeg.append(wdqt__qgl[nylgn__got])
        if not cxep__clp[nylgn__got]:
            fsuoh__tbk.append(byayo__tau)
            jeap__gglzt.append(cjy__iop[nylgn__got])
    return (dygnl__hkoh, vjivc__cmeg, rsk__svu, wrvjy__rvx, partition_names,
        fsuoh__tbk, jeap__gglzt, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    alfk__pscr = dictionary.to_pandas()
    nqds__yod = bodo.typeof(alfk__pscr).dtype
    if isinstance(nqds__yod, types.Integer):
        ivj__avtpn = PDCategoricalDtype(tuple(alfk__pscr), nqds__yod, False,
            int_type=nqds__yod)
    else:
        ivj__avtpn = PDCategoricalDtype(tuple(alfk__pscr), nqds__yod, False)
    return CategoricalArrayType(ivj__avtpn)


from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region,
    row_group_size, file_prefix, convert_timedelta_to_int64, timestamp_tz,
    downcast_time_ns_to_us):

    def codegen(context, builder, sig, args):
        hrugw__hvw = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        sgwq__szp = cgutils.get_or_insert_function(builder.module,
            hrugw__hvw, name='pq_write')
        qnzp__xwl = builder.call(sgwq__szp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return qnzp__xwl
    return types.int64(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.boolean, types.voidptr, types.boolean
        ), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region,
    row_group_size, file_prefix, timestamp_tz):

    def codegen(context, builder, sig, args):
        hrugw__hvw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        sgwq__szp = cgutils.get_or_insert_function(builder.module,
            hrugw__hvw, name='pq_write_partitioned')
        builder.call(sgwq__szp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
