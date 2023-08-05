from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.out_used_cols = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, out_used_colss={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.out_used_cols))


def check_node_typing(node, typemap):
    puqkg__omy = typemap[node.file_name.name]
    if types.unliteral(puqkg__omy) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {puqkg__omy}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        zmzf__cch = typemap[node.skiprows.name]
        if isinstance(zmzf__cch, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(zmzf__cch, types.Integer) and not (isinstance(
            zmzf__cch, (types.List, types.Tuple)) and isinstance(zmzf__cch.
            dtype, types.Integer)) and not isinstance(zmzf__cch, (types.
            LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {zmzf__cch}."
                , loc=node.skiprows.loc)
        elif isinstance(zmzf__cch, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        ecdvh__tni = typemap[node.nrows.name]
        if not isinstance(ecdvh__tni, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {ecdvh__tni}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)


@intrinsic
def csv_file_chunk_reader(typingctx, fname_t, is_parallel_t, skiprows_t,
    nrows_t, header_t, compression_t, bucket_region_t, storage_options_t,
    chunksize_t, is_skiprows_list_t, skiprows_list_len_t, pd_low_memory_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        fdqn__xpi = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        exp__mlz = cgutils.get_or_insert_function(builder.module, fdqn__xpi,
            name='csv_file_chunk_reader')
        hfa__xnnk = builder.call(exp__mlz, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        gxs__sfma = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        nvwxi__lswl = context.get_python_api(builder)
        gxs__sfma.meminfo = nvwxi__lswl.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), hfa__xnnk)
        gxs__sfma.pyobj = hfa__xnnk
        nvwxi__lswl.decref(hfa__xnnk)
        return gxs__sfma._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        ahcj__yfk = csv_node.out_vars[0]
        if ahcj__yfk.name not in lives:
            return None
    else:
        vflm__notg = csv_node.out_vars[0]
        moqqw__ehnj = csv_node.out_vars[1]
        if vflm__notg.name not in lives and moqqw__ehnj.name not in lives:
            return None
        elif moqqw__ehnj.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif vflm__notg.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    zmzf__cch = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            nvhg__gpx = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            zlbs__okk = csv_node.loc.strformat()
            usbpo__osuvi = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', nvhg__gpx,
                zlbs__okk, usbpo__osuvi)
            limn__mijq = csv_node.out_types[0].yield_type.data
            jgy__kaxo = [lkaeq__gagrb for ink__lgwy, lkaeq__gagrb in
                enumerate(csv_node.df_colnames) if isinstance(limn__mijq[
                ink__lgwy], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if jgy__kaxo:
                ftch__avwzo = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    ftch__avwzo, zlbs__okk, jgy__kaxo)
        if array_dists is not None:
            smy__hjkyj = csv_node.out_vars[0].name
            parallel = array_dists[smy__hjkyj] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        bkam__xjsj = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        bkam__xjsj += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        bkam__xjsj += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        ctn__jxm = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(bkam__xjsj, {}, ctn__jxm)
        wkizj__yovdx = ctn__jxm['csv_iterator_impl']
        earv__meaaz = 'def csv_reader_init(fname, nrows, skiprows):\n'
        earv__meaaz += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        earv__meaaz += '  return f_reader\n'
        exec(earv__meaaz, globals(), ctn__jxm)
        kvc__ewl = ctn__jxm['csv_reader_init']
        kpnox__svcd = numba.njit(kvc__ewl)
        compiled_funcs.append(kpnox__svcd)
        tpna__gejzr = compile_to_numba_ir(wkizj__yovdx, {'_csv_reader_init':
            kpnox__svcd, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, zmzf__cch), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(tpna__gejzr, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        vls__izj = tpna__gejzr.body[:-3]
        vls__izj[-1].target = csv_node.out_vars[0]
        return vls__izj
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    bkam__xjsj = 'def csv_impl(fname, nrows, skiprows):\n'
    bkam__xjsj += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    ctn__jxm = {}
    exec(bkam__xjsj, {}, ctn__jxm)
    jaqpc__fvypn = ctn__jxm['csv_impl']
    ayt__blel = csv_node.usecols
    if ayt__blel:
        ayt__blel = [csv_node.usecols[ink__lgwy] for ink__lgwy in csv_node.
            out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        nvhg__gpx = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        zlbs__okk = csv_node.loc.strformat()
        usbpo__osuvi = []
        jgy__kaxo = []
        if ayt__blel:
            for ink__lgwy in csv_node.out_used_cols:
                bzpla__wwss = csv_node.df_colnames[ink__lgwy]
                usbpo__osuvi.append(bzpla__wwss)
                if isinstance(csv_node.out_types[ink__lgwy], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    jgy__kaxo.append(bzpla__wwss)
        bodo.user_logging.log_message('Column Pruning', nvhg__gpx,
            zlbs__okk, usbpo__osuvi)
        if jgy__kaxo:
            ftch__avwzo = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ftch__avwzo, zlbs__okk, jgy__kaxo)
    jpwyz__ydzfd = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, ayt__blel, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    tpna__gejzr = compile_to_numba_ir(jaqpc__fvypn, {'_csv_reader_py':
        jpwyz__ydzfd}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, zmzf__cch), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(tpna__gejzr, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    vls__izj = tpna__gejzr.body[:-3]
    vls__izj[-1].target = csv_node.out_vars[1]
    vls__izj[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not ayt__blel
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        vls__izj.pop(-1)
    elif not ayt__blel:
        vls__izj.pop(-2)
    return vls__izj


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    dxq__ewgx = t.dtype
    if isinstance(dxq__ewgx, PDCategoricalDtype):
        yjtl__hdtq = CategoricalArrayType(dxq__ewgx)
        xgvox__jwejp = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, xgvox__jwejp, yjtl__hdtq)
        return xgvox__jwejp
    if dxq__ewgx == types.NPDatetime('ns'):
        dxq__ewgx = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        noof__xlj = 'int_arr_{}'.format(dxq__ewgx)
        setattr(types, noof__xlj, t)
        return noof__xlj
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if dxq__ewgx == types.bool_:
        dxq__ewgx = 'bool_'
    if dxq__ewgx == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(dxq__ewgx, (
        StringArrayType, ArrayItemArrayType)):
        gob__rzkp = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, gob__rzkp, t)
        return gob__rzkp
    return '{}[::1]'.format(dxq__ewgx)


def _get_pd_dtype_str(t):
    dxq__ewgx = t.dtype
    if isinstance(dxq__ewgx, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(dxq__ewgx.categories)
    if dxq__ewgx == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if dxq__ewgx.signed else 'U',
            dxq__ewgx.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(dxq__ewgx, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(dxq__ewgx)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    bvcdi__qwnu = ''
    from collections import defaultdict
    trtko__rkf = defaultdict(list)
    for lrku__fdrlq, jgi__naxv in typemap.items():
        trtko__rkf[jgi__naxv].append(lrku__fdrlq)
    atkiu__svv = df.columns.to_list()
    iogo__uyh = []
    for jgi__naxv, smte__umer in trtko__rkf.items():
        try:
            iogo__uyh.append(df.loc[:, smte__umer].astype(jgi__naxv, copy=
                False))
            df = df.drop(smte__umer, axis=1)
        except (ValueError, TypeError) as uax__ulnyb:
            bvcdi__qwnu = (
                f"Caught the runtime error '{uax__ulnyb}' on columns {smte__umer}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    gbdo__fxy = bool(bvcdi__qwnu)
    if parallel:
        ecch__mky = MPI.COMM_WORLD
        gbdo__fxy = ecch__mky.allreduce(gbdo__fxy, op=MPI.LOR)
    if gbdo__fxy:
        cpfd__pglih = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if bvcdi__qwnu:
            raise TypeError(f'{cpfd__pglih}\n{bvcdi__qwnu}')
        else:
            raise TypeError(
                f'{cpfd__pglih}\nPlease refer to errors on other ranks.')
    df = pd.concat(iogo__uyh + [df], axis=1)
    ldks__qqhul = df.loc[:, atkiu__svv]
    return ldks__qqhul


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    ndvbi__ckpfp = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        bkam__xjsj = '  skiprows = sorted(set(skiprows))\n'
    else:
        bkam__xjsj = '  skiprows = [skiprows]\n'
    bkam__xjsj += '  skiprows_list_len = len(skiprows)\n'
    bkam__xjsj += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    bkam__xjsj += '  check_java_installation(fname)\n'
    bkam__xjsj += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    bkam__xjsj += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    bkam__xjsj += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    bkam__xjsj += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, ndvbi__ckpfp, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    bkam__xjsj += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    bkam__xjsj += "      raise FileNotFoundError('File does not exist')\n"
    return bkam__xjsj


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    vfuv__doyf = [str(ink__lgwy) for ink__lgwy, eadi__cqn in enumerate(
        usecols) if col_typs[out_used_cols[ink__lgwy]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        vfuv__doyf.append(str(idx_col_index))
    ioyi__biqo = ', '.join(vfuv__doyf)
    opxb__gsxs = _gen_parallel_flag_name(sanitized_cnames)
    mwt__enxlg = f"{opxb__gsxs}='bool_'" if check_parallel_runtime else ''
    hde__kofio = [_get_pd_dtype_str(col_typs[out_used_cols[ink__lgwy]]) for
        ink__lgwy in range(len(usecols))]
    gny__yux = None if idx_col_index is None else _get_pd_dtype_str(idx_col_typ
        )
    kfll__tcun = [eadi__cqn for ink__lgwy, eadi__cqn in enumerate(usecols) if
        hde__kofio[ink__lgwy] == 'str']
    if idx_col_index is not None and gny__yux == 'str':
        kfll__tcun.append(idx_col_index)
    uga__ddqw = np.array(kfll__tcun, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = uga__ddqw
    bkam__xjsj = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    bnvdx__sktth = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = bnvdx__sktth
    bkam__xjsj += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    mwmiy__qxbis = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = mwmiy__qxbis
        bkam__xjsj += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    exfek__zzpy = defaultdict(list)
    for ink__lgwy, eadi__cqn in enumerate(usecols):
        if hde__kofio[ink__lgwy] == 'str':
            continue
        exfek__zzpy[hde__kofio[ink__lgwy]].append(eadi__cqn)
    if idx_col_index is not None and gny__yux != 'str':
        exfek__zzpy[gny__yux].append(idx_col_index)
    for ink__lgwy, gnt__ajw in enumerate(exfek__zzpy.values()):
        glbs[f't_arr_{ink__lgwy}_{call_id}'] = np.asarray(gnt__ajw)
        bkam__xjsj += (
            f'  t_arr_{ink__lgwy}_{call_id}_2 = t_arr_{ink__lgwy}_{call_id}\n')
    if idx_col_index != None:
        bkam__xjsj += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {mwt__enxlg}):
"""
    else:
        bkam__xjsj += (
            f'  with objmode(T=table_type_{call_id}, {mwt__enxlg}):\n')
    bkam__xjsj += f'    typemap = {{}}\n'
    for ink__lgwy, acyrc__wqb in enumerate(exfek__zzpy.keys()):
        bkam__xjsj += f"""    typemap.update({{i:{acyrc__wqb} for i in t_arr_{ink__lgwy}_{call_id}_2}})
"""
    bkam__xjsj += '    if f_reader.get_chunk_size() == 0:\n'
    bkam__xjsj += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    bkam__xjsj += '    else:\n'
    bkam__xjsj += '      df = pd.read_csv(f_reader,\n'
    bkam__xjsj += '        header=None,\n'
    bkam__xjsj += '        parse_dates=[{}],\n'.format(ioyi__biqo)
    bkam__xjsj += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    bkam__xjsj += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        bkam__xjsj += f'    {opxb__gsxs} = f_reader.is_parallel()\n'
    else:
        bkam__xjsj += f'    {opxb__gsxs} = {parallel}\n'
    bkam__xjsj += f'    df = astype(df, typemap, {opxb__gsxs})\n'
    if idx_col_index != None:
        tam__rgvuy = sorted(bnvdx__sktth).index(idx_col_index)
        bkam__xjsj += f'    idx_arr = df.iloc[:, {tam__rgvuy}].values\n'
        bkam__xjsj += (
            f'    df.drop(columns=df.columns[{tam__rgvuy}], inplace=True)\n')
    if len(usecols) == 0:
        bkam__xjsj += f'    T = None\n'
    else:
        bkam__xjsj += f'    arrs = []\n'
        bkam__xjsj += f'    for i in range(df.shape[1]):\n'
        bkam__xjsj += f'      arrs.append(df.iloc[:, i].values)\n'
        bkam__xjsj += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return bkam__xjsj


def _gen_parallel_flag_name(sanitized_cnames):
    opxb__gsxs = '_parallel_value'
    while opxb__gsxs in sanitized_cnames:
        opxb__gsxs = '_' + opxb__gsxs
    return opxb__gsxs


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(lkaeq__gagrb) for lkaeq__gagrb in
        col_names]
    bkam__xjsj = 'def csv_reader_py(fname, nrows, skiprows):\n'
    bkam__xjsj += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    xvhb__agxsg = globals()
    if idx_col_typ != types.none:
        xvhb__agxsg[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        xvhb__agxsg[f'table_type_{call_id}'] = types.none
    else:
        xvhb__agxsg[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    bkam__xjsj += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, xvhb__agxsg, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        bkam__xjsj += '  return (T, idx_arr)\n'
    else:
        bkam__xjsj += '  return (T, None)\n'
    ctn__jxm = {}
    xvhb__agxsg['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(bkam__xjsj, xvhb__agxsg, ctn__jxm)
    jpwyz__ydzfd = ctn__jxm['csv_reader_py']
    kpnox__svcd = numba.njit(jpwyz__ydzfd)
    compiled_funcs.append(kpnox__svcd)
    return kpnox__svcd
