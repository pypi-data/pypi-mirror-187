"""IR node for the parquet data access"""
from typing import List
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, models, register_model, unbox
import bodo
import bodo.ir.connector
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.io.helpers import is_nullable, numba_to_pyarrow_schema, pyarrow_table_schema_type
from bodo.io.parquet_pio import ParquetFileInfo, get_filters_pyobject, parquet_file_schema, parquet_predicate_type
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_ext import unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, FilenameType
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None, use_hive=True):
        yuq__dveux = lhs.scope
        loc = lhs.loc
        yjmyh__uxchh = None
        if lhs.name in self.locals:
            yjmyh__uxchh = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        qof__jvnc = {}
        if lhs.name + ':convert' in self.locals:
            qof__jvnc = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if yjmyh__uxchh is None:
            mfffd__zxdpf = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            kro__hpifg = get_const_value(file_name, self.func_ir,
                mfffd__zxdpf, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols, use_hive=use_hive))
            kakty__cvsx = guard(get_definition, self.func_ir, file_name)
            if isinstance(kakty__cvsx, ir.Arg) and isinstance(self.args[
                kakty__cvsx.index], FilenameType):
                typ: FilenameType = self.args[kakty__cvsx.index]
                (col_names, cwc__beneu, jypb__uxcw, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, cwc__beneu, jypb__uxcw, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(kro__hpifg, columns,
                    storage_options, input_file_name_col, read_as_dict_cols,
                    use_hive))
        else:
            klla__lvnph: List[str] = list(yjmyh__uxchh.keys())
            yczjv__zeoy = {c: oinna__djwrj for oinna__djwrj, c in enumerate
                (klla__lvnph)}
            gdxm__fng = [omhfe__soxrf for omhfe__soxrf in yjmyh__uxchh.values()
                ]
            col_names: List[str] = klla__lvnph if columns is None else columns
            col_indices = [yczjv__zeoy[c] for c in col_names]
            cwc__beneu = [gdxm__fng[yczjv__zeoy[c]] for c in col_names]
            jypb__uxcw = next((fun__ujkpk for fun__ujkpk in col_names if
                fun__ujkpk.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (cwc__beneu), columns=tuple(col_names)))
        ylhhl__rmeom = None if isinstance(jypb__uxcw, dict
            ) or jypb__uxcw is None else jypb__uxcw
        index_column_index = None
        index_column_type = types.none
        if ylhhl__rmeom:
            qes__wnnms = col_names.index(ylhhl__rmeom)
            index_column_index = col_indices.pop(qes__wnnms)
            index_column_type = cwc__beneu.pop(qes__wnnms)
            col_names.pop(qes__wnnms)
        for oinna__djwrj, c in enumerate(col_names):
            if c in qof__jvnc:
                cwc__beneu[oinna__djwrj] = qof__jvnc[c]
        evzrv__uhs = [ir.Var(yuq__dveux, mk_unique_var('pq_table'), loc),
            ir.Var(yuq__dveux, mk_unique_var('pq_index'), loc)]
        ctttg__gktsg = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, cwc__beneu, evzrv__uhs, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, evzrv__uhs, jypb__uxcw, ctttg__gktsg, cwc__beneu,
            index_column_type)


class ParquetReader(ir.Stmt):

    def __init__(self, file_name, df_out, col_names, col_indices, out_types,
        out_vars, loc, partition_names, storage_options, index_column_index,
        index_column_type, input_file_name_col, unsupported_columns,
        unsupported_arrow_types, arrow_schema, use_hive):
        self.connector_typ = 'parquet'
        self.file_name = file_name
        self.df_out = df_out
        self.df_colnames = col_names
        self.col_indices = col_indices
        self.out_types = out_types
        self.original_out_types = out_types
        self.original_df_colnames = col_names
        self.out_vars = out_vars
        self.loc = loc
        self.partition_names = partition_names
        self.filters = None
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(col_indices)))
        self.input_file_name_col = input_file_name_col
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.arrow_schema = arrow_schema
        self.is_live_table = True
        self.use_hive = use_hive

    def __repr__(self):
        return (
            '({}) = ReadParquet({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
            .format(self.df_out, self.file_name.name, self.df_colnames,
            self.col_indices, self.out_types, self.original_out_types, self
            .original_df_colnames, self.out_vars, self.partition_names,
            self.filters, self.storage_options, self.index_column_index,
            self.index_column_type, self.out_used_cols, self.
            input_file_name_col, self.unsupported_columns, self.
            unsupported_arrow_types, self.arrow_schema))


def remove_dead_pq(pq_node, lives_no_aliases, lives, arg_aliases, alias_map,
    func_ir, typemap):
    arj__grgs = pq_node.out_vars[0].name
    ylnjr__ppxzd = pq_node.out_vars[1].name
    if arj__grgs not in lives and ylnjr__ppxzd not in lives:
        return None
    elif arj__grgs not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif ylnjr__ppxzd not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    mcnwn__uwii = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    qjt__wggt, xye__bup = bodo.ir.connector.generate_filter_map(pq_node.filters
        )
    extra_args = ', '.join(qjt__wggt.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, qjt__wggt, xye__bup, pq_node.original_df_colnames,
        pq_node.partition_names, pq_node.original_out_types, typemap,
        'parquet', output_dnf=False)
    sbiz__ipyr = ', '.join(f'out{oinna__djwrj}' for oinna__djwrj in range(
        mcnwn__uwii))
    xnkg__kdvk = f'def pq_impl(fname, {extra_args}):\n'
    xnkg__kdvk += (
        f'    (total_rows, {sbiz__ipyr},) = _pq_reader_py(fname, {extra_args})\n'
        )
    vmm__xal = {}
    exec(xnkg__kdvk, {}, vmm__xal)
    ivofz__ulxwp = vmm__xal['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        uvk__nlm = pq_node.loc.strformat()
        qju__wobtm = []
        gho__nove = []
        for oinna__djwrj in pq_node.out_used_cols:
            lsua__wzmpq = pq_node.df_colnames[oinna__djwrj]
            qju__wobtm.append(lsua__wzmpq)
            if isinstance(pq_node.out_types[oinna__djwrj], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                gho__nove.append(lsua__wzmpq)
        kkxn__uqbuy = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', kkxn__uqbuy,
            uvk__nlm, qju__wobtm)
        if gho__nove:
            cev__tbhzh = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', cev__tbhzh,
                uvk__nlm, gho__nove)
    byuqs__xpxh = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        mtqub__gwz = set(pq_node.out_used_cols)
        mkp__ere = set(pq_node.unsupported_columns)
        nsbw__zavs = mtqub__gwz & mkp__ere
        if nsbw__zavs:
            njveo__srgq = sorted(nsbw__zavs)
            okcv__kro = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            tdhk__ohfql = 0
            for wsqjj__uhy in njveo__srgq:
                while pq_node.unsupported_columns[tdhk__ohfql] != wsqjj__uhy:
                    tdhk__ohfql += 1
                okcv__kro.append(
                    f"Column '{pq_node.df_colnames[wsqjj__uhy]}' with unsupported arrow type {pq_node.unsupported_arrow_types[tdhk__ohfql]}"
                    )
                tdhk__ohfql += 1
            gfa__dswa = '\n'.join(okcv__kro)
            raise BodoError(gfa__dswa, loc=pq_node.loc)
    fswj__bdtmb = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.out_used_cols, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, byuqs__xpxh, meta_head_only_info,
        pq_node.index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    daawt__lsd = typemap[pq_node.file_name.name]
    nnn__kvk = (daawt__lsd,) + tuple(typemap[dob__yuw.name] for dob__yuw in
        xye__bup)
    cnalp__ahhu = compile_to_numba_ir(ivofz__ulxwp, {'_pq_reader_py':
        fswj__bdtmb}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        nnn__kvk, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(cnalp__ahhu, [pq_node.file_name] + xye__bup)
    ctttg__gktsg = cnalp__ahhu.body[:-3]
    if meta_head_only_info:
        ctttg__gktsg[-3].target = meta_head_only_info[1]
    ctttg__gktsg[-2].target = pq_node.out_vars[0]
    ctttg__gktsg[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        ctttg__gktsg.pop(-1)
    elif not pq_node.is_live_table:
        ctttg__gktsg.pop(-2)
    return ctttg__gktsg


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    chml__qcoe = next_label()
    lff__wog = ',' if extra_args else ''
    xnkg__kdvk = f'def pq_reader_py(fname,{extra_args}):\n'
    xnkg__kdvk += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    xnkg__kdvk += f"    ev.add_attribute('g_fname', fname)\n"
    xnkg__kdvk += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{lff__wog}))
"""
    xnkg__kdvk += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    xnkg__kdvk += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    hfq__nzylf = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        hfq__nzylf = meta_head_only_info[0]
    egeu__nwzay = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    ikdii__psddy = {c: oinna__djwrj for oinna__djwrj, c in enumerate(
        col_indices)}
    igv__bor = {c: oinna__djwrj for oinna__djwrj, c in enumerate(egeu__nwzay)}
    kcmq__mui = []
    vnc__rhln = set()
    uvy__crres = partition_names + [input_file_name_col]
    for oinna__djwrj in out_used_cols:
        if egeu__nwzay[oinna__djwrj] not in uvy__crres:
            kcmq__mui.append(col_indices[oinna__djwrj])
        elif not input_file_name_col or egeu__nwzay[oinna__djwrj
            ] != input_file_name_col:
            vnc__rhln.add(col_indices[oinna__djwrj])
    if index_column_index is not None:
        kcmq__mui.append(index_column_index)
    kcmq__mui = sorted(kcmq__mui)
    fep__efk = {c: oinna__djwrj for oinna__djwrj, c in enumerate(kcmq__mui)}
    wfjhz__zwre = [(int(is_nullable(out_types[ikdii__psddy[isdhg__vkfkh]])) if
        isdhg__vkfkh != index_column_index else int(is_nullable(
        index_column_type))) for isdhg__vkfkh in kcmq__mui]
    ubin__tdnr = []
    for isdhg__vkfkh in kcmq__mui:
        if isdhg__vkfkh == index_column_index:
            omhfe__soxrf = index_column_type
        else:
            omhfe__soxrf = out_types[ikdii__psddy[isdhg__vkfkh]]
        if omhfe__soxrf == dict_str_arr_type:
            ubin__tdnr.append(isdhg__vkfkh)
    nvm__gxgfg = []
    rqnpj__jhag = {}
    paqa__umv = []
    waxfw__ezk = []
    for oinna__djwrj, rrl__wgoub in enumerate(partition_names):
        try:
            dehyv__alt = igv__bor[rrl__wgoub]
            if col_indices[dehyv__alt] not in vnc__rhln:
                continue
        except (KeyError, ValueError) as nuweg__dioi:
            continue
        rqnpj__jhag[rrl__wgoub] = len(nvm__gxgfg)
        nvm__gxgfg.append(rrl__wgoub)
        paqa__umv.append(oinna__djwrj)
        bhb__uzd = out_types[dehyv__alt].dtype
        bzv__tds = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            bhb__uzd)
        waxfw__ezk.append(numba_to_c_type(bzv__tds))
    xnkg__kdvk += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{chml__qcoe},
        {hfq__nzylf},
        selected_cols_arr_{chml__qcoe}.ctypes,
        {len(kcmq__mui)},
        nullable_cols_arr_{chml__qcoe}.ctypes,
"""
    if len(paqa__umv) > 0:
        xnkg__kdvk += f"""        np.array({paqa__umv}, dtype=np.int32).ctypes,
        np.array({waxfw__ezk}, dtype=np.int32).ctypes,
        {len(paqa__umv)},
"""
    else:
        xnkg__kdvk += f'        0, 0, 0,\n'
    if len(ubin__tdnr) > 0:
        xnkg__kdvk += (
            f'        np.array({ubin__tdnr}, dtype=np.int32).ctypes, {len(ubin__tdnr)},\n'
            )
    else:
        xnkg__kdvk += f'        0, 0,\n'
    xnkg__kdvk += f'        total_rows_np.ctypes,\n'
    xnkg__kdvk += f'        {input_file_name_col is not None},\n'
    xnkg__kdvk += f'        {use_hive},\n'
    xnkg__kdvk += f'    )\n'
    xnkg__kdvk += f'    check_and_propagate_cpp_exception()\n'
    xnkg__kdvk += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        xnkg__kdvk += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        xnkg__kdvk += f'    local_rows = total_rows\n'
    ijzk__xpqik = index_column_type
    egx__nxod = TableType(tuple(out_types))
    if is_dead_table:
        egx__nxod = types.none
    if is_dead_table:
        vxji__phpi = None
    else:
        vxji__phpi = []
        xoas__rzq = 0
        bdt__hie = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for oinna__djwrj, wsqjj__uhy in enumerate(col_indices):
            if xoas__rzq < len(out_used_cols
                ) and oinna__djwrj == out_used_cols[xoas__rzq]:
                kzkv__fajeg = col_indices[oinna__djwrj]
                if bdt__hie and kzkv__fajeg == bdt__hie:
                    vxji__phpi.append(len(kcmq__mui) + len(nvm__gxgfg))
                elif kzkv__fajeg in vnc__rhln:
                    thb__mtf = egeu__nwzay[oinna__djwrj]
                    vxji__phpi.append(len(kcmq__mui) + rqnpj__jhag[thb__mtf])
                else:
                    vxji__phpi.append(fep__efk[wsqjj__uhy])
                xoas__rzq += 1
            else:
                vxji__phpi.append(-1)
        vxji__phpi = np.array(vxji__phpi, dtype=np.int64)
    if is_dead_table:
        xnkg__kdvk += '    T = None\n'
    else:
        xnkg__kdvk += f"""    T = cpp_table_to_py_table(out_table, table_idx_{chml__qcoe}, py_table_type_{chml__qcoe})
"""
        if len(out_used_cols) == 0:
            xnkg__kdvk += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        xnkg__kdvk += '    index_arr = None\n'
    else:
        ypp__pywbx = fep__efk[index_column_index]
        xnkg__kdvk += f"""    index_arr = info_to_array(info_from_table(out_table, {ypp__pywbx}), index_arr_type)
"""
    xnkg__kdvk += f'    delete_table(out_table)\n'
    xnkg__kdvk += f'    ev.finalize()\n'
    xnkg__kdvk += f'    return (total_rows, T, index_arr)\n'
    vmm__xal = {}
    waktm__szhfl = {f'py_table_type_{chml__qcoe}': egx__nxod,
        f'table_idx_{chml__qcoe}': vxji__phpi,
        f'selected_cols_arr_{chml__qcoe}': np.array(kcmq__mui, np.int32),
        f'nullable_cols_arr_{chml__qcoe}': np.array(wfjhz__zwre, np.int32),
        f'pyarrow_schema_{chml__qcoe}': pyarrow_schema.remove_metadata(),
        'index_arr_type': ijzk__xpqik, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo,
        'get_node_portion': bodo.libs.distributed_api.get_node_portion,
        'set_table_len': bodo.hiframes.table.set_table_len}
    exec(xnkg__kdvk, waktm__szhfl, vmm__xal)
    fswj__bdtmb = vmm__xal['pq_reader_py']
    qbd__wha = numba.njit(fswj__bdtmb, no_cpython_wrapper=True)
    return qbd__wha


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


numba.parfors.array_analysis.array_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[ParquetReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[ParquetReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[ParquetReader] = remove_dead_pq
numba.core.analysis.ir_extension_usedefs[ParquetReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[ParquetReader
    ] = bodo.ir.connector.build_connector_definitions
remove_dead_column_extensions[ParquetReader] = pq_remove_dead_column
ir_extension_table_column_use[ParquetReader
    ] = bodo.ir.connector.connector_table_column_use
distributed_pass.distributed_run_extensions[ParquetReader] = pq_distributed_run
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, parquet_predicate_type,
    parquet_predicate_type, storage_options_dict_type,
    pyarrow_table_schema_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean, types.boolean))
