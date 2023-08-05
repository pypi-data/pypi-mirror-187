"""IR node for the groupby"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, decref_table_array, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, py_data_to_cpp_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import gen_getitem, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        juzs__bhsrl = func.signature
        if juzs__bhsrl == types.none(types.voidptr):
            noylb__jqio = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            cjhly__bhrh = cgutils.get_or_insert_function(builder.module,
                noylb__jqio, sym._literal_value)
            builder.call(cjhly__bhrh, [context.get_constant_null(
                juzs__bhsrl.args[0])])
        elif juzs__bhsrl == types.none(types.int64, types.voidptr, types.
            voidptr):
            noylb__jqio = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            cjhly__bhrh = cgutils.get_or_insert_function(builder.module,
                noylb__jqio, sym._literal_value)
            builder.call(cjhly__bhrh, [context.get_constant(types.int64, 0),
                context.get_constant_null(juzs__bhsrl.args[1]), context.
                get_constant_null(juzs__bhsrl.args[2])])
        else:
            noylb__jqio = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            cjhly__bhrh = cgutils.get_or_insert_function(builder.module,
                noylb__jqio, sym._literal_value)
            builder.call(cjhly__bhrh, [context.get_constant_null(
                juzs__bhsrl.args[0]), context.get_constant_null(juzs__bhsrl
                .args[1]), context.get_constant_null(juzs__bhsrl.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'ngroup', 'head', 'transform', 'size',
    'shift', 'sum', 'count', 'nunique', 'median', 'cumsum', 'cumprod',
    'cummin', 'cummax', 'mean', 'min', 'max', 'prod', 'first', 'last',
    'idxmin', 'idxmax', 'var', 'std', 'boolor_agg', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last', 'boolor_agg'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        lokbv__mppsx = True
        xebl__poylw = 1
        fkck__wwouu = -1
        if isinstance(rhs, ir.Expr):
            for sxdh__sow in rhs.kws:
                if func_name in list_cumulative:
                    if sxdh__sow[0] == 'skipna':
                        lokbv__mppsx = guard(find_const, func_ir, sxdh__sow[1])
                        if not isinstance(lokbv__mppsx, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if sxdh__sow[0] == 'dropna':
                        lokbv__mppsx = guard(find_const, func_ir, sxdh__sow[1])
                        if not isinstance(lokbv__mppsx, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            xebl__poylw = get_call_expr_arg('shift', rhs.args, dict(rhs.kws
                ), 0, 'periods', xebl__poylw)
            xebl__poylw = guard(find_const, func_ir, xebl__poylw)
        if func_name == 'head':
            fkck__wwouu = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(fkck__wwouu, int):
                fkck__wwouu = guard(find_const, func_ir, fkck__wwouu)
            if fkck__wwouu < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = lokbv__mppsx
        func.periods = xebl__poylw
        func.head_n = fkck__wwouu
        if func_name == 'transform':
            kws = dict(rhs.kws)
            auhw__nytnz = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            tdrn__skuai = typemap[auhw__nytnz.name]
            yzfg__qminy = None
            if isinstance(tdrn__skuai, str):
                yzfg__qminy = tdrn__skuai
            elif is_overload_constant_str(tdrn__skuai):
                yzfg__qminy = get_overload_const_str(tdrn__skuai)
            elif bodo.utils.typing.is_builtin_function(tdrn__skuai):
                yzfg__qminy = bodo.utils.typing.get_builtin_function_name(
                    tdrn__skuai)
            if yzfg__qminy not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {yzfg__qminy}'
                    )
            func.transform_func = supported_agg_funcs.index(yzfg__qminy)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    auhw__nytnz = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if auhw__nytnz == '':
        tdrn__skuai = types.none
    else:
        tdrn__skuai = typemap[auhw__nytnz.name]
    if is_overload_constant_dict(tdrn__skuai):
        pqj__gjlg = get_overload_constant_dict(tdrn__skuai)
        xdvrh__kta = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in pqj__gjlg.values()]
        return xdvrh__kta
    if tdrn__skuai == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(tdrn__skuai, types.BaseTuple) or is_overload_constant_list(
        tdrn__skuai):
        xdvrh__kta = []
        qbn__oks = 0
        if is_overload_constant_list(tdrn__skuai):
            czk__eeqh = get_overload_const_list(tdrn__skuai)
        else:
            czk__eeqh = tdrn__skuai.types
        for t in czk__eeqh:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                xdvrh__kta.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(czk__eeqh) > 1:
                    func.fname = '<lambda_' + str(qbn__oks) + '>'
                    qbn__oks += 1
                xdvrh__kta.append(func)
        return [xdvrh__kta]
    if is_overload_constant_str(tdrn__skuai):
        func_name = get_overload_const_str(tdrn__skuai)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(tdrn__skuai):
        func_name = bodo.utils.typing.get_builtin_function_name(tdrn__skuai)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        qbn__oks = 0
        hkvh__ioh = []
        for drc__hwjw in f_val:
            func = get_agg_func_udf(func_ir, drc__hwjw, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{qbn__oks}>'
                qbn__oks += 1
            hkvh__ioh.append(func)
        return hkvh__ioh
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    yzfg__qminy = code.co_name
    return yzfg__qminy


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            mdb__cdgza = types.DType(args[0])
            return signature(mdb__cdgza, *args)


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_vars, in_vars, in_key_inds, df_in_type, out_type,
        input_has_index, same_index, return_key, loc, func_name, dropna,
        _num_shuffle_keys):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_vars = out_vars
        self.in_vars = in_vars
        self.in_key_inds = in_key_inds
        self.df_in_type = df_in_type
        self.out_type = out_type
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self._num_shuffle_keys = _num_shuffle_keys
        self.dead_in_inds = set()
        self.dead_out_inds = set()

    def get_live_in_vars(self):
        return [qkwzf__kcu for qkwzf__kcu in self.in_vars if qkwzf__kcu is not
            None]

    def get_live_out_vars(self):
        return [qkwzf__kcu for qkwzf__kcu in self.out_vars if qkwzf__kcu is not
            None]

    @property
    def is_in_table_format(self):
        return self.df_in_type.is_table_format

    @property
    def n_in_table_arrays(self):
        return len(self.df_in_type.columns
            ) if self.df_in_type.is_table_format else 1

    @property
    def n_in_cols(self):
        return self.n_in_table_arrays + len(self.in_vars) - 1

    @property
    def in_col_types(self):
        return list(self.df_in_type.data) + list(get_index_data_arr_types(
            self.df_in_type.index))

    @property
    def is_output_table(self):
        return not isinstance(self.out_type, SeriesType)

    @property
    def n_out_table_arrays(self):
        return len(self.out_type.table_type.arr_types) if not isinstance(self
            .out_type, SeriesType) else 1

    @property
    def n_out_cols(self):
        return self.n_out_table_arrays + len(self.out_vars) - 1

    @property
    def out_col_types(self):
        zefrp__fkyxr = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        dtkxk__wyty = list(get_index_data_arr_types(self.out_type.index))
        return zefrp__fkyxr + dtkxk__wyty

    def update_dead_col_info(self):
        for myul__kduh in self.dead_out_inds:
            self.gb_info_out.pop(myul__kduh, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for hvnr__urf, gpisu__bjg in self.gb_info_in.copy().items():
            kiouz__tkrm = []
            for drc__hwjw, vnnru__akwv in gpisu__bjg:
                if vnnru__akwv not in self.dead_out_inds:
                    kiouz__tkrm.append((drc__hwjw, vnnru__akwv))
            if not kiouz__tkrm:
                if hvnr__urf is not None and hvnr__urf not in self.in_key_inds:
                    self.dead_in_inds.add(hvnr__urf)
                self.gb_info_in.pop(hvnr__urf)
            else:
                self.gb_info_in[hvnr__urf] = kiouz__tkrm
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for dywcr__rouz in range(1, len(self.in_vars)):
                myul__kduh = self.n_in_table_arrays + dywcr__rouz - 1
                if myul__kduh in self.dead_in_inds:
                    self.in_vars[dywcr__rouz] = None
        else:
            for dywcr__rouz in range(len(self.in_vars)):
                if dywcr__rouz in self.dead_in_inds:
                    self.in_vars[dywcr__rouz] = None

    def __repr__(self):
        tiutt__vhad = ', '.join(qkwzf__kcu.name for qkwzf__kcu in self.
            get_live_in_vars())
        htxa__gszhd = f'{self.df_in}{{{tiutt__vhad}}}'
        tvhw__ewvwx = ', '.join(qkwzf__kcu.name for qkwzf__kcu in self.
            get_live_out_vars())
        txld__bopy = f'{self.df_out}{{{tvhw__ewvwx}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {htxa__gszhd} {txld__bopy}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({qkwzf__kcu.name for qkwzf__kcu in aggregate_node.
        get_live_in_vars()})
    def_set.update({qkwzf__kcu.name for qkwzf__kcu in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    plyit__grhp = agg_node.out_vars[0]
    if plyit__grhp is not None and plyit__grhp.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            uqssa__wmthx = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(uqssa__wmthx)
        else:
            agg_node.dead_out_inds.add(0)
    for dywcr__rouz in range(1, len(agg_node.out_vars)):
        qkwzf__kcu = agg_node.out_vars[dywcr__rouz]
        if qkwzf__kcu is not None and qkwzf__kcu.name not in lives:
            agg_node.out_vars[dywcr__rouz] = None
            myul__kduh = agg_node.n_out_table_arrays + dywcr__rouz - 1
            agg_node.dead_out_inds.add(myul__kduh)
    if all(qkwzf__kcu is None for qkwzf__kcu in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    ekhgc__aagp = {qkwzf__kcu.name for qkwzf__kcu in aggregate_node.
        get_live_out_vars()}
    return set(), ekhgc__aagp


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for dywcr__rouz in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[dywcr__rouz] is not None:
            aggregate_node.in_vars[dywcr__rouz] = replace_vars_inner(
                aggregate_node.in_vars[dywcr__rouz], var_dict)
    for dywcr__rouz in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[dywcr__rouz] is not None:
            aggregate_node.out_vars[dywcr__rouz] = replace_vars_inner(
                aggregate_node.out_vars[dywcr__rouz], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for dywcr__rouz in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[dywcr__rouz] is not None:
            aggregate_node.in_vars[dywcr__rouz] = visit_vars_inner(
                aggregate_node.in_vars[dywcr__rouz], callback, cbdata)
    for dywcr__rouz in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[dywcr__rouz] is not None:
            aggregate_node.out_vars[dywcr__rouz] = visit_vars_inner(
                aggregate_node.out_vars[dywcr__rouz], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    kfrpe__qutmp = []
    for ylg__hve in aggregate_node.get_live_in_vars():
        nwtem__ivsl = equiv_set.get_shape(ylg__hve)
        if nwtem__ivsl is not None:
            kfrpe__qutmp.append(nwtem__ivsl[0])
    if len(kfrpe__qutmp) > 1:
        equiv_set.insert_equiv(*kfrpe__qutmp)
    bjkjq__evd = []
    kfrpe__qutmp = []
    for ylg__hve in aggregate_node.get_live_out_vars():
        pnfts__zqrf = typemap[ylg__hve.name]
        nup__axiai = array_analysis._gen_shape_call(equiv_set, ylg__hve,
            pnfts__zqrf.ndim, None, bjkjq__evd)
        equiv_set.insert_equiv(ylg__hve, nup__axiai)
        kfrpe__qutmp.append(nup__axiai[0])
        equiv_set.define(ylg__hve, set())
    if len(kfrpe__qutmp) > 1:
        equiv_set.insert_equiv(*kfrpe__qutmp)
    return [], bjkjq__evd


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    rzcn__ovn = aggregate_node.get_live_in_vars()
    ceyh__xxjx = aggregate_node.get_live_out_vars()
    eirep__jwuy = Distribution.OneD
    for ylg__hve in rzcn__ovn:
        eirep__jwuy = Distribution(min(eirep__jwuy.value, array_dists[
            ylg__hve.name].value))
    scls__fqq = Distribution(min(eirep__jwuy.value, Distribution.OneD_Var.
        value))
    for ylg__hve in ceyh__xxjx:
        if ylg__hve.name in array_dists:
            scls__fqq = Distribution(min(scls__fqq.value, array_dists[
                ylg__hve.name].value))
    if scls__fqq != Distribution.OneD_Var:
        eirep__jwuy = scls__fqq
    for ylg__hve in rzcn__ovn:
        array_dists[ylg__hve.name] = eirep__jwuy
    for ylg__hve in ceyh__xxjx:
        array_dists[ylg__hve.name] = scls__fqq


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ylg__hve in agg_node.get_live_out_vars():
        definitions[ylg__hve.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    mgh__roh = agg_node.get_live_in_vars()
    shin__rdo = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for qkwzf__kcu in (mgh__roh + shin__rdo):
            if array_dists[qkwzf__kcu.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                qkwzf__kcu.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    xdvrh__kta = []
    func_out_types = []
    for vnnru__akwv, (hvnr__urf, func) in agg_node.gb_info_out.items():
        if hvnr__urf is not None:
            t = agg_node.in_col_types[hvnr__urf]
            in_col_typs.append(t)
        xdvrh__kta.append(func)
        func_out_types.append(out_col_typs[vnnru__akwv])
    dpml__beo = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for dywcr__rouz, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            dpml__beo.update({f'in_cat_dtype_{dywcr__rouz}': in_col_typ})
    for dywcr__rouz, wrq__uwbsw in enumerate(out_col_typs):
        if isinstance(wrq__uwbsw, bodo.CategoricalArrayType):
            dpml__beo.update({f'out_cat_dtype_{dywcr__rouz}': wrq__uwbsw})
    udf_func_struct = get_udf_func_struct(xdvrh__kta, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[qkwzf__kcu.name] if qkwzf__kcu is not None else
        types.none) for qkwzf__kcu in agg_node.out_vars]
    ejpuq__nnfpe, jbmn__gywat = gen_top_level_agg_func(agg_node,
        in_col_typs, out_col_typs, func_out_types, parallel,
        udf_func_struct, out_var_types, typemap)
    dpml__beo.update(jbmn__gywat)
    dpml__beo.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decref_table_array': decref_table_array, 'decode_if_dict_array':
        decode_if_dict_array, 'set_table_data': bodo.hiframes.table.
        set_table_data, 'get_table_data': bodo.hiframes.table.
        get_table_data, 'out_typs': out_col_typs})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            dpml__beo.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            dpml__beo.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {}, bqx__hvw)
    xzze__kbgf = bqx__hvw['agg_top']
    nozqn__lwwp = compile_to_numba_ir(xzze__kbgf, dpml__beo, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[qkwzf__kcu.
        name] for qkwzf__kcu in mgh__roh), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(nozqn__lwwp, mgh__roh)
    niuyo__pgch = nozqn__lwwp.body[-2].value.value
    dbrr__axwp = nozqn__lwwp.body[:-2]
    for dywcr__rouz, qkwzf__kcu in enumerate(shin__rdo):
        gen_getitem(qkwzf__kcu, niuyo__pgch, dywcr__rouz, calltypes, dbrr__axwp
            )
    return dbrr__axwp


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        fycg__azfi = IntDtype(t.dtype).name
        assert fycg__azfi.endswith('Dtype()')
        fycg__azfi = fycg__azfi[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{fycg__azfi}'))"
            )
    elif isinstance(t, FloatingArrayType):
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1.0], dtype='{t.dtype}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif t == bodo.dict_str_arr_type:
        return (
            'bodo.libs.dict_arr_ext.init_dict_arr(pre_alloc_string_array(1, 1), bodo.libs.int_arr_ext.alloc_int_array(1, np.int32), False, False)'
            )
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        zjak__lvf = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {zjak__lvf}_cat_dtype_{colnum})')
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    do_combine, func_idx_to_in_col, label_suffix):
    fdph__ksnj = udf_func_struct.var_typs
    ijb__stptw = len(fdph__ksnj)
    ejpuq__nnfpe = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    ejpuq__nnfpe += '    if is_null_pointer(in_table):\n'
    ejpuq__nnfpe += '        return\n'
    ejpuq__nnfpe += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in fdph__ksnj]), 
        ',' if len(fdph__ksnj) == 1 else '')
    teeew__jux = n_keys
    fdrz__dufmo = []
    redvar_offsets = []
    crpv__jxi = []
    if do_combine:
        for dywcr__rouz, drc__hwjw in enumerate(allfuncs):
            if drc__hwjw.ftype != 'udf':
                teeew__jux += drc__hwjw.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(teeew__jux, teeew__jux +
                    drc__hwjw.n_redvars))
                teeew__jux += drc__hwjw.n_redvars
                crpv__jxi.append(data_in_typs_[func_idx_to_in_col[dywcr__rouz]]
                    )
                fdrz__dufmo.append(func_idx_to_in_col[dywcr__rouz] + n_keys)
    else:
        for dywcr__rouz, drc__hwjw in enumerate(allfuncs):
            if drc__hwjw.ftype != 'udf':
                teeew__jux += drc__hwjw.ncols_post_shuffle
            else:
                redvar_offsets += list(range(teeew__jux + 1, teeew__jux + 1 +
                    drc__hwjw.n_redvars))
                teeew__jux += drc__hwjw.n_redvars + 1
                crpv__jxi.append(data_in_typs_[func_idx_to_in_col[dywcr__rouz]]
                    )
                fdrz__dufmo.append(func_idx_to_in_col[dywcr__rouz] + n_keys)
    assert len(redvar_offsets) == ijb__stptw
    mpb__dvo = len(crpv__jxi)
    jqsl__aaf = []
    for dywcr__rouz, t in enumerate(crpv__jxi):
        jqsl__aaf.append(_gen_dummy_alloc(t, dywcr__rouz, True))
    ejpuq__nnfpe += '    data_in_dummy = ({}{})\n'.format(','.join(
        jqsl__aaf), ',' if len(crpv__jxi) == 1 else '')
    ejpuq__nnfpe += """
    # initialize redvar cols
"""
    ejpuq__nnfpe += '    init_vals = __init_func()\n'
    for dywcr__rouz in range(ijb__stptw):
        ejpuq__nnfpe += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(dywcr__rouz, redvar_offsets[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(redvar_arr_{})\n'.format(dywcr__rouz)
        ejpuq__nnfpe += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            dywcr__rouz, dywcr__rouz)
    ejpuq__nnfpe += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(dywcr__rouz) for dywcr__rouz in range(
        ijb__stptw)]), ',' if ijb__stptw == 1 else '')
    ejpuq__nnfpe += '\n'
    for dywcr__rouz in range(mpb__dvo):
        ejpuq__nnfpe += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(dywcr__rouz, fdrz__dufmo[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(data_in_{})\n'.format(dywcr__rouz)
    ejpuq__nnfpe += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(dywcr__rouz) for dywcr__rouz in range(mpb__dvo)]), ',' if 
        mpb__dvo == 1 else '')
    ejpuq__nnfpe += '\n'
    ejpuq__nnfpe += '    for i in range(len(data_in_0)):\n'
    ejpuq__nnfpe += '        w_ind = row_to_group[i]\n'
    ejpuq__nnfpe += '        if w_ind != -1:\n'
    ejpuq__nnfpe += (
        '            __update_redvars(redvars, data_in, w_ind, i)\n')
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bqx__hvw)
    return bqx__hvw['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    fdph__ksnj = udf_func_struct.var_typs
    ijb__stptw = len(fdph__ksnj)
    ejpuq__nnfpe = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    ejpuq__nnfpe += '    if is_null_pointer(in_table):\n'
    ejpuq__nnfpe += '        return\n'
    ejpuq__nnfpe += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in fdph__ksnj]), 
        ',' if len(fdph__ksnj) == 1 else '')
    owa__ppvh = n_keys
    bunm__pnwrk = n_keys
    vix__grrp = []
    qpsdg__rel = []
    for drc__hwjw in allfuncs:
        if drc__hwjw.ftype != 'udf':
            owa__ppvh += drc__hwjw.ncols_pre_shuffle
            bunm__pnwrk += drc__hwjw.ncols_post_shuffle
        else:
            vix__grrp += list(range(owa__ppvh, owa__ppvh + drc__hwjw.n_redvars)
                )
            qpsdg__rel += list(range(bunm__pnwrk + 1, bunm__pnwrk + 1 +
                drc__hwjw.n_redvars))
            owa__ppvh += drc__hwjw.n_redvars
            bunm__pnwrk += 1 + drc__hwjw.n_redvars
    assert len(vix__grrp) == ijb__stptw
    ejpuq__nnfpe += """
    # initialize redvar cols
"""
    ejpuq__nnfpe += '    init_vals = __init_func()\n'
    for dywcr__rouz in range(ijb__stptw):
        ejpuq__nnfpe += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(dywcr__rouz, qpsdg__rel[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(redvar_arr_{})\n'.format(dywcr__rouz)
        ejpuq__nnfpe += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            dywcr__rouz, dywcr__rouz)
    ejpuq__nnfpe += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(dywcr__rouz) for dywcr__rouz in range(
        ijb__stptw)]), ',' if ijb__stptw == 1 else '')
    ejpuq__nnfpe += '\n'
    for dywcr__rouz in range(ijb__stptw):
        ejpuq__nnfpe += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(dywcr__rouz, vix__grrp[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(recv_redvar_arr_{})\n'.format(dywcr__rouz)
    ejpuq__nnfpe += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(dywcr__rouz) for dywcr__rouz in range(
        ijb__stptw)]), ',' if ijb__stptw == 1 else '')
    ejpuq__nnfpe += '\n'
    if ijb__stptw:
        ejpuq__nnfpe += '    for i in range(len(recv_redvar_arr_0)):\n'
        ejpuq__nnfpe += '        w_ind = row_to_group[i]\n'
        ejpuq__nnfpe += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bqx__hvw)
    return bqx__hvw['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    fdph__ksnj = udf_func_struct.var_typs
    ijb__stptw = len(fdph__ksnj)
    teeew__jux = n_keys
    redvar_offsets = []
    nam__vvmey = []
    elc__kqkka = []
    for dywcr__rouz, drc__hwjw in enumerate(allfuncs):
        if drc__hwjw.ftype != 'udf':
            teeew__jux += drc__hwjw.ncols_post_shuffle
        else:
            nam__vvmey.append(teeew__jux)
            redvar_offsets += list(range(teeew__jux + 1, teeew__jux + 1 +
                drc__hwjw.n_redvars))
            teeew__jux += 1 + drc__hwjw.n_redvars
            elc__kqkka.append(out_data_typs_[dywcr__rouz])
    assert len(redvar_offsets) == ijb__stptw
    mpb__dvo = len(elc__kqkka)
    ejpuq__nnfpe = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    ejpuq__nnfpe += '    if is_null_pointer(table):\n'
    ejpuq__nnfpe += '        return\n'
    ejpuq__nnfpe += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in fdph__ksnj]), 
        ',' if len(fdph__ksnj) == 1 else '')
    ejpuq__nnfpe += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        elc__kqkka]), ',' if len(elc__kqkka) == 1 else '')
    for dywcr__rouz in range(ijb__stptw):
        ejpuq__nnfpe += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(dywcr__rouz, redvar_offsets[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(redvar_arr_{})\n'.format(dywcr__rouz)
    ejpuq__nnfpe += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(dywcr__rouz) for dywcr__rouz in range(
        ijb__stptw)]), ',' if ijb__stptw == 1 else '')
    ejpuq__nnfpe += '\n'
    for dywcr__rouz in range(mpb__dvo):
        ejpuq__nnfpe += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(dywcr__rouz, nam__vvmey[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(data_out_{})\n'.format(dywcr__rouz)
    ejpuq__nnfpe += '    data_out = ({}{})\n'.format(','.join([
        'data_out_{}'.format(dywcr__rouz) for dywcr__rouz in range(mpb__dvo
        )]), ',' if mpb__dvo == 1 else '')
    ejpuq__nnfpe += '\n'
    ejpuq__nnfpe += '    for i in range(len(data_out_0)):\n'
    ejpuq__nnfpe += '        __eval_res(redvars, data_out, i)\n'
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, bqx__hvw)
    return bqx__hvw['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    teeew__jux = n_keys
    anjr__boi = []
    for dywcr__rouz, drc__hwjw in enumerate(allfuncs):
        if drc__hwjw.ftype == 'gen_udf':
            anjr__boi.append(teeew__jux)
            teeew__jux += 1
        elif drc__hwjw.ftype != 'udf':
            teeew__jux += drc__hwjw.ncols_post_shuffle
        else:
            teeew__jux += drc__hwjw.n_redvars + 1
    ejpuq__nnfpe = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    ejpuq__nnfpe += '    if num_groups == 0:\n'
    ejpuq__nnfpe += '        return\n'
    for dywcr__rouz, func in enumerate(udf_func_struct.general_udf_funcs):
        ejpuq__nnfpe += '    # col {}\n'.format(dywcr__rouz)
        ejpuq__nnfpe += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(anjr__boi[dywcr__rouz], dywcr__rouz))
        ejpuq__nnfpe += '    incref(out_col)\n'
        ejpuq__nnfpe += '    for j in range(num_groups):\n'
        ejpuq__nnfpe += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(dywcr__rouz, dywcr__rouz))
        ejpuq__nnfpe += '        incref(in_col)\n'
        ejpuq__nnfpe += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(dywcr__rouz))
    dpml__beo = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    hpy__zun = 0
    for dywcr__rouz, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[hpy__zun]
        dpml__beo['func_{}'.format(hpy__zun)] = func
        dpml__beo['in_col_{}_typ'.format(hpy__zun)] = in_col_typs[
            func_idx_to_in_col[dywcr__rouz]]
        dpml__beo['out_col_{}_typ'.format(hpy__zun)] = out_col_typs[dywcr__rouz
            ]
        hpy__zun += 1
    bqx__hvw = {}
    exec(ejpuq__nnfpe, dpml__beo, bqx__hvw)
    drc__hwjw = bqx__hvw['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    sivi__bwlx = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(sivi__bwlx, nopython=True)(drc__hwjw)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    xrfy__emt = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        rtwr__dlz = []
        if agg_node.in_vars[0] is not None:
            rtwr__dlz.append('arg0')
        for dywcr__rouz in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if dywcr__rouz not in agg_node.dead_in_inds:
                rtwr__dlz.append(f'arg{dywcr__rouz}')
    else:
        rtwr__dlz = [f'arg{dywcr__rouz}' for dywcr__rouz, qkwzf__kcu in
            enumerate(agg_node.in_vars) if qkwzf__kcu is not None]
    ejpuq__nnfpe = f"def agg_top({', '.join(rtwr__dlz)}):\n"
    akggr__rdq = []
    if agg_node.is_in_table_format:
        akggr__rdq = agg_node.in_key_inds + [hvnr__urf for hvnr__urf,
            alb__twqe in agg_node.gb_info_out.values() if hvnr__urf is not None
            ]
        if agg_node.input_has_index:
            akggr__rdq.append(agg_node.n_in_cols - 1)
        yexxe__ivnn = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        dbvu__zth = []
        for dywcr__rouz in range(agg_node.n_in_table_arrays, agg_node.n_in_cols
            ):
            if dywcr__rouz in agg_node.dead_in_inds:
                dbvu__zth.append('None')
            else:
                dbvu__zth.append(f'arg{dywcr__rouz}')
        myka__tvq = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        ejpuq__nnfpe += f"""    table = py_data_to_cpp_table({myka__tvq}, ({', '.join(dbvu__zth)}{yexxe__ivnn}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        clfci__wack = [f'arg{dywcr__rouz}' for dywcr__rouz in agg_node.
            in_key_inds]
        qdtm__jvzxb = [f'arg{hvnr__urf}' for hvnr__urf, alb__twqe in
            agg_node.gb_info_out.values() if hvnr__urf is not None]
        imy__kev = clfci__wack + qdtm__jvzxb
        if agg_node.input_has_index:
            imy__kev.append(f'arg{len(agg_node.in_vars) - 1}')
        ejpuq__nnfpe += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({fcpz__pyv})' for fcpz__pyv in imy__kev))
        ejpuq__nnfpe += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    kvdbl__qjxv = []
    func_idx_to_in_col = []
    vjjbq__vrj = []
    lokbv__mppsx = False
    yuov__rxysn = 1
    fkck__wwouu = -1
    rtlon__oox = 0
    yvbni__phhwz = 0
    xdvrh__kta = [func for alb__twqe, func in agg_node.gb_info_out.values()]
    for ekh__xxqk, func in enumerate(xdvrh__kta):
        kvdbl__qjxv.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            rtlon__oox += 1
        if hasattr(func, 'skipdropna'):
            lokbv__mppsx = func.skipdropna
        if func.ftype == 'shift':
            yuov__rxysn = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            yvbni__phhwz = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            fkck__wwouu = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(ekh__xxqk)
        if func.ftype == 'udf':
            vjjbq__vrj.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            vjjbq__vrj.append(0)
            do_combine = False
    kvdbl__qjxv.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if rtlon__oox > 0:
        if rtlon__oox != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    qpukz__bfz = []
    if udf_func_struct is not None:
        mvuft__atx = next_label()
        if udf_func_struct.regular_udfs:
            sivi__bwlx = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            nusvu__dlwja = numba.cfunc(sivi__bwlx, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, mvuft__atx))
            owf__vcekl = numba.cfunc(sivi__bwlx, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, mvuft__atx))
            tqaxy__hmo = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, mvuft__atx))
            udf_func_struct.set_regular_cfuncs(nusvu__dlwja, owf__vcekl,
                tqaxy__hmo)
            for myoj__qyzxw in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[myoj__qyzxw.native_name] = myoj__qyzxw
                gb_agg_cfunc_addr[myoj__qyzxw.native_name
                    ] = myoj__qyzxw.address
        if udf_func_struct.general_udfs:
            wtput__vtvpn = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                mvuft__atx)
            udf_func_struct.set_general_cfunc(wtput__vtvpn)
        fdph__ksnj = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        evr__wpqxr = 0
        dywcr__rouz = 0
        for puhmw__xnqj, drc__hwjw in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if drc__hwjw.ftype in ('udf', 'gen_udf'):
                qpukz__bfz.append(out_col_typs[puhmw__xnqj])
                for yaeb__jxfhi in range(evr__wpqxr, evr__wpqxr +
                    vjjbq__vrj[dywcr__rouz]):
                    qpukz__bfz.append(dtype_to_array_type(fdph__ksnj[
                        yaeb__jxfhi]))
                evr__wpqxr += vjjbq__vrj[dywcr__rouz]
                dywcr__rouz += 1
        ejpuq__nnfpe += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{dywcr__rouz}' for dywcr__rouz in range(len(qpukz__bfz)))}{',' if len(qpukz__bfz) == 1 else ''}))
"""
        ejpuq__nnfpe += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(qpukz__bfz)})
"""
        if udf_func_struct.regular_udfs:
            ejpuq__nnfpe += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{nusvu__dlwja.native_name}')\n"
                )
            ejpuq__nnfpe += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{owf__vcekl.native_name}')\n"
                )
            ejpuq__nnfpe += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{tqaxy__hmo.native_name}')\n"
                )
            ejpuq__nnfpe += f"""    cpp_cb_update_addr = get_agg_udf_addr('{nusvu__dlwja.native_name}')
"""
            ejpuq__nnfpe += f"""    cpp_cb_combine_addr = get_agg_udf_addr('{owf__vcekl.native_name}')
"""
            ejpuq__nnfpe += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{tqaxy__hmo.native_name}')\n"
                )
        else:
            ejpuq__nnfpe += '    cpp_cb_update_addr = 0\n'
            ejpuq__nnfpe += '    cpp_cb_combine_addr = 0\n'
            ejpuq__nnfpe += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            myoj__qyzxw = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[myoj__qyzxw.native_name] = myoj__qyzxw
            gb_agg_cfunc_addr[myoj__qyzxw.native_name] = myoj__qyzxw.address
            ejpuq__nnfpe += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{myoj__qyzxw.native_name}')\n"
                )
            ejpuq__nnfpe += f"""    cpp_cb_general_addr = get_agg_udf_addr('{myoj__qyzxw.native_name}')
"""
        else:
            ejpuq__nnfpe += '    cpp_cb_general_addr = 0\n'
    else:
        ejpuq__nnfpe += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        ejpuq__nnfpe += '    cpp_cb_update_addr = 0\n'
        ejpuq__nnfpe += '    cpp_cb_combine_addr = 0\n'
        ejpuq__nnfpe += '    cpp_cb_eval_addr = 0\n'
        ejpuq__nnfpe += '    cpp_cb_general_addr = 0\n'
    ejpuq__nnfpe += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(drc__hwjw.ftype)) for
        drc__hwjw in allfuncs] + ['0']))
    ejpuq__nnfpe += (
        f'    func_offsets = np.array({str(kvdbl__qjxv)}, dtype=np.int32)\n')
    if len(vjjbq__vrj) > 0:
        ejpuq__nnfpe += (
            f'    udf_ncols = np.array({str(vjjbq__vrj)}, dtype=np.int32)\n')
    else:
        ejpuq__nnfpe += '    udf_ncols = np.array([0], np.int32)\n'
    ejpuq__nnfpe += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    entq__pxr = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    ejpuq__nnfpe += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {lokbv__mppsx}, {yuov__rxysn}, {yvbni__phhwz}, {fkck__wwouu}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {entq__pxr})
"""
    qktwm__lro = []
    vcvi__jdxaj = 0
    if agg_node.return_key:
        aoxv__gwn = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for dywcr__rouz in range(n_keys):
            myul__kduh = aoxv__gwn + dywcr__rouz
            qktwm__lro.append(myul__kduh if myul__kduh not in agg_node.
                dead_out_inds else -1)
            vcvi__jdxaj += 1
    for puhmw__xnqj in agg_node.gb_info_out.keys():
        qktwm__lro.append(puhmw__xnqj)
        vcvi__jdxaj += 1
    oxs__mgoqo = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            qktwm__lro.append(agg_node.n_out_cols - 1)
        else:
            oxs__mgoqo = True
    yexxe__ivnn = ',' if xrfy__emt == 1 else ''
    fwh__qju = (
        f"({', '.join(f'out_type{dywcr__rouz}' for dywcr__rouz in range(xrfy__emt))}{yexxe__ivnn})"
        )
    ree__qnni = []
    shozo__iews = []
    for dywcr__rouz, t in enumerate(out_col_typs):
        if dywcr__rouz not in agg_node.dead_out_inds and type_has_unknown_cats(
            t):
            if dywcr__rouz in agg_node.gb_info_out:
                hvnr__urf = agg_node.gb_info_out[dywcr__rouz][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                rkfoa__fnbfk = dywcr__rouz - aoxv__gwn
                hvnr__urf = agg_node.in_key_inds[rkfoa__fnbfk]
            shozo__iews.append(dywcr__rouz)
            if (agg_node.is_in_table_format and hvnr__urf < agg_node.
                n_in_table_arrays):
                ree__qnni.append(f'get_table_data(arg0, {hvnr__urf})')
            else:
                ree__qnni.append(f'arg{hvnr__urf}')
    yexxe__ivnn = ',' if len(ree__qnni) == 1 else ''
    ejpuq__nnfpe += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {fwh__qju}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(ree__qnni)}{yexxe__ivnn}), unknown_cat_out_inds)
"""
    ejpuq__nnfpe += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    ejpuq__nnfpe += '    delete_table_decref_arrays(table)\n'
    ejpuq__nnfpe += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for dywcr__rouz in range(n_keys):
            if qktwm__lro[dywcr__rouz] == -1:
                ejpuq__nnfpe += (
                    f'    decref_table_array(out_table, {dywcr__rouz})\n')
    if oxs__mgoqo:
        rmt__btxs = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        ejpuq__nnfpe += f'    decref_table_array(out_table, {rmt__btxs})\n'
    ejpuq__nnfpe += '    delete_table(out_table)\n'
    ejpuq__nnfpe += '    ev_clean.finalize()\n'
    ejpuq__nnfpe += '    return out_data\n'
    fuujl__uif = {f'out_type{dywcr__rouz}': out_var_types[dywcr__rouz] for
        dywcr__rouz in range(xrfy__emt)}
    fuujl__uif['out_col_inds'] = MetaType(tuple(qktwm__lro))
    fuujl__uif['in_col_inds'] = MetaType(tuple(akggr__rdq))
    fuujl__uif['cpp_table_to_py_data'] = cpp_table_to_py_data
    fuujl__uif['py_data_to_cpp_table'] = py_data_to_cpp_table
    fuujl__uif.update({f'udf_type{dywcr__rouz}': t for dywcr__rouz, t in
        enumerate(qpukz__bfz)})
    fuujl__uif['udf_dummy_col_inds'] = MetaType(tuple(range(len(qpukz__bfz))))
    fuujl__uif['create_dummy_table'] = create_dummy_table
    fuujl__uif['unknown_cat_out_inds'] = MetaType(tuple(shozo__iews))
    fuujl__uif['get_table_data'] = bodo.hiframes.table.get_table_data
    return ejpuq__nnfpe, fuujl__uif


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    zghop__yfnk = tuple(unwrap_typeref(data_types.types[dywcr__rouz]) for
        dywcr__rouz in range(len(data_types.types)))
    inhyr__ohd = bodo.TableType(zghop__yfnk)
    fuujl__uif = {'table_type': inhyr__ohd}
    ejpuq__nnfpe = 'def impl(data_types):\n'
    ejpuq__nnfpe += '  py_table = init_table(table_type, False)\n'
    ejpuq__nnfpe += '  py_table = set_table_len(py_table, 1)\n'
    for pnfts__zqrf, vbafa__obrfp in inhyr__ohd.type_to_blk.items():
        fuujl__uif[f'typ_list_{vbafa__obrfp}'] = types.List(pnfts__zqrf)
        fuujl__uif[f'typ_{vbafa__obrfp}'] = pnfts__zqrf
        njrh__qjx = len(inhyr__ohd.block_to_arr_ind[vbafa__obrfp])
        ejpuq__nnfpe += f"""  arr_list_{vbafa__obrfp} = alloc_list_like(typ_list_{vbafa__obrfp}, {njrh__qjx}, False)
"""
        ejpuq__nnfpe += f'  for i in range(len(arr_list_{vbafa__obrfp})):\n'
        ejpuq__nnfpe += f"""    arr_list_{vbafa__obrfp}[i] = alloc_type(1, typ_{vbafa__obrfp}, (-1,))
"""
        ejpuq__nnfpe += f"""  py_table = set_table_block(py_table, arr_list_{vbafa__obrfp}, {vbafa__obrfp})
"""
    ejpuq__nnfpe += '  return py_table\n'
    fuujl__uif.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    bqx__hvw = {}
    exec(ejpuq__nnfpe, fuujl__uif, bqx__hvw)
    return bqx__hvw['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    qqp__kkw = agg_node.in_vars[0].name
    hwhx__sxoi, nmhl__zqffv, rqp__zysm = block_use_map[qqp__kkw]
    if nmhl__zqffv or rqp__zysm:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        syw__geth, nqj__zyci, ihq__rrejv = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if nqj__zyci or ihq__rrejv:
            syw__geth = set(range(agg_node.n_out_table_arrays))
    else:
        syw__geth = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            syw__geth = {0}
    qttkb__yvlqh = set(dywcr__rouz for dywcr__rouz in agg_node.in_key_inds if
        dywcr__rouz < agg_node.n_in_table_arrays)
    pejsp__fjkyo = set(agg_node.gb_info_out[dywcr__rouz][0] for dywcr__rouz in
        syw__geth if dywcr__rouz in agg_node.gb_info_out and agg_node.
        gb_info_out[dywcr__rouz][0] is not None)
    pejsp__fjkyo |= qttkb__yvlqh | hwhx__sxoi
    kea__ybaol = len(set(range(agg_node.n_in_table_arrays)) - pejsp__fjkyo
        ) == 0
    block_use_map[qqp__kkw] = pejsp__fjkyo, kea__ybaol, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    yipo__wqoi = agg_node.n_out_table_arrays
    ylata__bga = agg_node.out_vars[0].name
    gzvt__sce = _find_used_columns(ylata__bga, yipo__wqoi, column_live_map,
        equiv_vars)
    if gzvt__sce is None:
        return False
    skmbk__zgh = set(range(yipo__wqoi)) - gzvt__sce
    otlh__eed = len(skmbk__zgh - agg_node.dead_out_inds) != 0
    if otlh__eed:
        agg_node.dead_out_inds.update(skmbk__zgh)
        agg_node.update_dead_col_info()
    return otlh__eed


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for qtuy__uxv in block.body:
            if is_call_assign(qtuy__uxv) and find_callname(f_ir, qtuy__uxv.
                value) == ('len', 'builtins') and qtuy__uxv.value.args[0
                ].name == f_ir.arg_names[0]:
                smkj__hkxn = get_definition(f_ir, qtuy__uxv.value.func)
                smkj__hkxn.name = 'dummy_agg_count'
                smkj__hkxn.value = dummy_agg_count
    tfyho__hzog = get_name_var_table(f_ir.blocks)
    dkacb__hky = {}
    for name, alb__twqe in tfyho__hzog.items():
        dkacb__hky[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, dkacb__hky)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    aegsj__idv = numba.core.compiler.Flags()
    aegsj__idv.nrt = True
    jltyh__ntky = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, aegsj__idv)
    jltyh__ntky.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, dulro__dqu, calltypes, alb__twqe = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    adgr__tpx = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    whzg__mytd = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    ujbx__bqnhi = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    dbbrx__eohw = ujbx__bqnhi(typemap, calltypes)
    pm = whzg__mytd(typingctx, targetctx, None, f_ir, typemap, dulro__dqu,
        calltypes, dbbrx__eohw, {}, aegsj__idv, None)
    apo__gor = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = whzg__mytd(typingctx, targetctx, None, f_ir, typemap, dulro__dqu,
        calltypes, dbbrx__eohw, {}, aegsj__idv, apo__gor)
    rrqh__xlbmo = numba.core.typed_passes.InlineOverloads()
    rrqh__xlbmo.run_pass(pm)
    iqorh__yligc = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    iqorh__yligc.run()
    for block in f_ir.blocks.values():
        for qtuy__uxv in block.body:
            if is_assign(qtuy__uxv) and isinstance(qtuy__uxv.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[qtuy__uxv.target.name],
                SeriesType):
                pnfts__zqrf = typemap.pop(qtuy__uxv.target.name)
                typemap[qtuy__uxv.target.name] = pnfts__zqrf.data
            if is_call_assign(qtuy__uxv) and find_callname(f_ir, qtuy__uxv.
                value) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[qtuy__uxv.target.name].remove(qtuy__uxv.value
                    )
                qtuy__uxv.value = qtuy__uxv.value.args[0]
                f_ir._definitions[qtuy__uxv.target.name].append(qtuy__uxv.value
                    )
            if is_call_assign(qtuy__uxv) and find_callname(f_ir, qtuy__uxv.
                value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[qtuy__uxv.target.name].remove(qtuy__uxv.value
                    )
                qtuy__uxv.value = ir.Const(False, qtuy__uxv.loc)
                f_ir._definitions[qtuy__uxv.target.name].append(qtuy__uxv.value
                    )
            if is_call_assign(qtuy__uxv) and find_callname(f_ir, qtuy__uxv.
                value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[qtuy__uxv.target.name].remove(qtuy__uxv.value
                    )
                qtuy__uxv.value = ir.Const(False, qtuy__uxv.loc)
                f_ir._definitions[qtuy__uxv.target.name].append(qtuy__uxv.value
                    )
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    goj__swyw = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, adgr__tpx)
    goj__swyw.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    ianlj__jslw = numba.core.compiler.StateDict()
    ianlj__jslw.func_ir = f_ir
    ianlj__jslw.typemap = typemap
    ianlj__jslw.calltypes = calltypes
    ianlj__jslw.typingctx = typingctx
    ianlj__jslw.targetctx = targetctx
    ianlj__jslw.return_type = dulro__dqu
    numba.core.rewrites.rewrite_registry.apply('after-inference', ianlj__jslw)
    udnub__avul = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        dulro__dqu, typingctx, targetctx, adgr__tpx, aegsj__idv, {})
    udnub__avul.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            gfs__bida = ctypes.pythonapi.PyCell_Get
            gfs__bida.restype = ctypes.py_object
            gfs__bida.argtypes = ctypes.py_object,
            pqj__gjlg = tuple(gfs__bida(dfg__utw) for dfg__utw in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            pqj__gjlg = closure.items
        assert len(code.co_freevars) == len(pqj__gjlg)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, pqj__gjlg)


class RegularUDFGenerator:

    def __init__(self, in_col_types, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        owljo__vkntf = SeriesType(in_col_typ.dtype,
            to_str_arr_if_dict_array(in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (owljo__vkntf,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        lzs__xrf, arr_var = _rm_arg_agg_block(block, pm.typemap)
        sqkz__fylz = -1
        for dywcr__rouz, qtuy__uxv in enumerate(lzs__xrf):
            if isinstance(qtuy__uxv, numba.parfors.parfor.Parfor):
                assert sqkz__fylz == -1, 'only one parfor for aggregation function'
                sqkz__fylz = dywcr__rouz
        parfor = None
        if sqkz__fylz != -1:
            parfor = lzs__xrf[sqkz__fylz]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = lzs__xrf[:sqkz__fylz] + parfor.init_block.body
        eval_nodes = lzs__xrf[sqkz__fylz + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for qtuy__uxv in init_nodes:
            if is_assign(qtuy__uxv) and qtuy__uxv.target.name in redvars:
                ind = redvars.index(qtuy__uxv.target.name)
                reduce_vars[ind] = qtuy__uxv.target
        var_types = [pm.typemap[qkwzf__kcu] for qkwzf__kcu in redvars]
        agv__bwov = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        hrjg__jnnoz = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        xieke__aylnx = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(xieke__aylnx)
        self.all_update_funcs.append(hrjg__jnnoz)
        self.all_combine_funcs.append(agv__bwov)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        bkhia__yhbwt = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        wbrr__jsq = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        myuxb__mom = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        ulnhr__fuacm = gen_all_eval_func(self.all_eval_funcs, self.
            redvar_offsets)
        return (self.all_vartypes, bkhia__yhbwt, wbrr__jsq, myuxb__mom,
            ulnhr__fuacm)


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, in_col_types, typingctx, targetctx):
    gng__biplq = []
    for t, drc__hwjw in zip(in_col_types, agg_func):
        gng__biplq.append((t, drc__hwjw))
    tpyak__okbl = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    nlk__cdsa = GeneralUDFGenerator()
    for in_col_typ, func in gng__biplq:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            tpyak__okbl.add_udf(in_col_typ, func)
        except:
            nlk__cdsa.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = tpyak__okbl.gen_all_func()
    general_udf_funcs = nlk__cdsa.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    reiv__fejod = compute_use_defs(parfor.loop_body)
    uzvxa__nufh = set()
    for hfx__atcqy in reiv__fejod.usemap.values():
        uzvxa__nufh |= hfx__atcqy
    owca__pys = set()
    for hfx__atcqy in reiv__fejod.defmap.values():
        owca__pys |= hfx__atcqy
    vppqt__qut = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    vppqt__qut.body = eval_nodes
    frftk__zevja = compute_use_defs({(0): vppqt__qut})
    rkxk__xmdd = frftk__zevja.usemap[0]
    jboq__bnmv = set()
    gcqz__ihfi = []
    ogrog__wwf = []
    for qtuy__uxv in reversed(init_nodes):
        wpd__pyxn = {qkwzf__kcu.name for qkwzf__kcu in qtuy__uxv.list_vars()}
        if is_assign(qtuy__uxv):
            qkwzf__kcu = qtuy__uxv.target.name
            wpd__pyxn.remove(qkwzf__kcu)
            if (qkwzf__kcu in uzvxa__nufh and qkwzf__kcu not in jboq__bnmv and
                qkwzf__kcu not in rkxk__xmdd and qkwzf__kcu not in owca__pys):
                ogrog__wwf.append(qtuy__uxv)
                uzvxa__nufh |= wpd__pyxn
                owca__pys.add(qkwzf__kcu)
                continue
        jboq__bnmv |= wpd__pyxn
        gcqz__ihfi.append(qtuy__uxv)
    ogrog__wwf.reverse()
    gcqz__ihfi.reverse()
    fzas__srqc = min(parfor.loop_body.keys())
    xmy__ekih = parfor.loop_body[fzas__srqc]
    xmy__ekih.body = ogrog__wwf + xmy__ekih.body
    return gcqz__ihfi


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    bkym__dbmte = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    wwxtb__jqk = set()
    lpnj__ipc = []
    for qtuy__uxv in init_nodes:
        if is_assign(qtuy__uxv) and isinstance(qtuy__uxv.value, ir.Global
            ) and isinstance(qtuy__uxv.value.value, pytypes.FunctionType
            ) and qtuy__uxv.value.value in bkym__dbmte:
            wwxtb__jqk.add(qtuy__uxv.target.name)
        elif is_call_assign(qtuy__uxv
            ) and qtuy__uxv.value.func.name in wwxtb__jqk:
            pass
        else:
            lpnj__ipc.append(qtuy__uxv)
    init_nodes = lpnj__ipc
    xnc__vlm = types.Tuple(var_types)
    oxwjh__oic = lambda : None
    f_ir = compile_to_numba_ir(oxwjh__oic, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    aftyf__ues = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    hyr__zvrp = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), aftyf__ues,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [hyr__zvrp] + block.body
    block.body[-2].value.value = aftyf__ues
    pcp__cnuh = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        xnc__vlm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    noerg__lmhrv = numba.core.target_extension.dispatcher_registry[cpu_target](
        oxwjh__oic)
    noerg__lmhrv.add_overload(pcp__cnuh)
    return noerg__lmhrv


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    gdpsz__qefoa = len(update_funcs)
    kvse__dsvd = len(in_col_types)
    ejpuq__nnfpe = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for yaeb__jxfhi in range(gdpsz__qefoa):
        qse__kcco = ', '.join(['redvar_arrs[{}][w_ind]'.format(dywcr__rouz) for
            dywcr__rouz in range(redvar_offsets[yaeb__jxfhi],
            redvar_offsets[yaeb__jxfhi + 1])])
        if qse__kcco:
            ejpuq__nnfpe += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                .format(qse__kcco, yaeb__jxfhi, qse__kcco, 0 if kvse__dsvd ==
                1 else yaeb__jxfhi))
    ejpuq__nnfpe += '  return\n'
    dpml__beo = {}
    for dywcr__rouz, drc__hwjw in enumerate(update_funcs):
        dpml__beo['update_vars_{}'.format(dywcr__rouz)] = drc__hwjw
    bqx__hvw = {}
    exec(ejpuq__nnfpe, dpml__beo, bqx__hvw)
    bciia__mjc = bqx__hvw['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(bciia__mjc)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    jxhh__vto = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = jxhh__vto, jxhh__vto, types.intp, types.intp
    sfrnp__cyxm = len(redvar_offsets) - 1
    ejpuq__nnfpe = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for yaeb__jxfhi in range(sfrnp__cyxm):
        qse__kcco = ', '.join(['redvar_arrs[{}][w_ind]'.format(dywcr__rouz) for
            dywcr__rouz in range(redvar_offsets[yaeb__jxfhi],
            redvar_offsets[yaeb__jxfhi + 1])])
        sks__pmf = ', '.join(['recv_arrs[{}][i]'.format(dywcr__rouz) for
            dywcr__rouz in range(redvar_offsets[yaeb__jxfhi],
            redvar_offsets[yaeb__jxfhi + 1])])
        if sks__pmf:
            ejpuq__nnfpe += '  {} = combine_vars_{}({}, {})\n'.format(qse__kcco
                , yaeb__jxfhi, qse__kcco, sks__pmf)
    ejpuq__nnfpe += '  return\n'
    dpml__beo = {}
    for dywcr__rouz, drc__hwjw in enumerate(combine_funcs):
        dpml__beo['combine_vars_{}'.format(dywcr__rouz)] = drc__hwjw
    bqx__hvw = {}
    exec(ejpuq__nnfpe, dpml__beo, bqx__hvw)
    laby__ufur = bqx__hvw['combine_all_f']
    f_ir = compile_to_numba_ir(laby__ufur, dpml__beo)
    myuxb__mom = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    noerg__lmhrv = numba.core.target_extension.dispatcher_registry[cpu_target](
        laby__ufur)
    noerg__lmhrv.add_overload(myuxb__mom)
    return noerg__lmhrv


def gen_all_eval_func(eval_funcs, redvar_offsets):
    sfrnp__cyxm = len(redvar_offsets) - 1
    ejpuq__nnfpe = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for yaeb__jxfhi in range(sfrnp__cyxm):
        qse__kcco = ', '.join(['redvar_arrs[{}][j]'.format(dywcr__rouz) for
            dywcr__rouz in range(redvar_offsets[yaeb__jxfhi],
            redvar_offsets[yaeb__jxfhi + 1])])
        ejpuq__nnfpe += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
            yaeb__jxfhi, yaeb__jxfhi, qse__kcco)
    ejpuq__nnfpe += '  return\n'
    dpml__beo = {}
    for dywcr__rouz, drc__hwjw in enumerate(eval_funcs):
        dpml__beo['eval_vars_{}'.format(dywcr__rouz)] = drc__hwjw
    bqx__hvw = {}
    exec(ejpuq__nnfpe, dpml__beo, bqx__hvw)
    tfjfc__dpdfj = bqx__hvw['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(tfjfc__dpdfj)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    djwu__vmc = len(var_types)
    jnjvk__fegm = [f'in{dywcr__rouz}' for dywcr__rouz in range(djwu__vmc)]
    xnc__vlm = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    djsl__ddp = xnc__vlm(0)
    ejpuq__nnfpe = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        jnjvk__fegm))
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {'_zero': djsl__ddp}, bqx__hvw)
    nyl__ujecd = bqx__hvw['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(nyl__ujecd, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': djsl__ddp}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    zen__gfn = []
    for dywcr__rouz, qkwzf__kcu in enumerate(reduce_vars):
        zen__gfn.append(ir.Assign(block.body[dywcr__rouz].target,
            qkwzf__kcu, qkwzf__kcu.loc))
        for qlx__tsvsn in qkwzf__kcu.versioned_names:
            zen__gfn.append(ir.Assign(qkwzf__kcu, ir.Var(qkwzf__kcu.scope,
                qlx__tsvsn, qkwzf__kcu.loc), qkwzf__kcu.loc))
    block.body = block.body[:djwu__vmc] + zen__gfn + eval_nodes
    xieke__aylnx = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xnc__vlm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    noerg__lmhrv = numba.core.target_extension.dispatcher_registry[cpu_target](
        nyl__ujecd)
    noerg__lmhrv.add_overload(xieke__aylnx)
    return noerg__lmhrv


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    djwu__vmc = len(redvars)
    kezxo__lke = [f'v{dywcr__rouz}' for dywcr__rouz in range(djwu__vmc)]
    jnjvk__fegm = [f'in{dywcr__rouz}' for dywcr__rouz in range(djwu__vmc)]
    ejpuq__nnfpe = 'def agg_combine({}):\n'.format(', '.join(kezxo__lke +
        jnjvk__fegm))
    aln__gjedk = wrap_parfor_blocks(parfor)
    ltgl__dpnxo = find_topo_order(aln__gjedk)
    ltgl__dpnxo = ltgl__dpnxo[1:]
    unwrap_parfor_blocks(parfor)
    pqqc__vwqqe = {}
    kesy__cqtxz = []
    for kfsn__xrb in ltgl__dpnxo:
        inqf__kmhy = parfor.loop_body[kfsn__xrb]
        for qtuy__uxv in inqf__kmhy.body:
            if is_assign(qtuy__uxv) and qtuy__uxv.target.name in redvars:
                vknh__orfy = qtuy__uxv.target.name
                ind = redvars.index(vknh__orfy)
                if ind in kesy__cqtxz:
                    continue
                if len(f_ir._definitions[vknh__orfy]) == 2:
                    var_def = f_ir._definitions[vknh__orfy][0]
                    ejpuq__nnfpe += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[vknh__orfy][1]
                    ejpuq__nnfpe += _match_reduce_def(var_def, f_ir, ind)
    ejpuq__nnfpe += '    return {}'.format(', '.join(['v{}'.format(
        dywcr__rouz) for dywcr__rouz in range(djwu__vmc)]))
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {}, bqx__hvw)
    xug__ilcu = bqx__hvw['agg_combine']
    arg_typs = tuple(2 * var_types)
    dpml__beo = {'numba': numba, 'bodo': bodo, 'np': np}
    dpml__beo.update(pqqc__vwqqe)
    f_ir = compile_to_numba_ir(xug__ilcu, dpml__beo, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    xnc__vlm = pm.typemap[block.body[-1].value.name]
    agv__bwov = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xnc__vlm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    noerg__lmhrv = numba.core.target_extension.dispatcher_registry[cpu_target](
        xug__ilcu)
    noerg__lmhrv.add_overload(agv__bwov)
    return noerg__lmhrv


def _match_reduce_def(var_def, f_ir, ind):
    ejpuq__nnfpe = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        ejpuq__nnfpe = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        tqx__ytssa = guard(find_callname, f_ir, var_def)
        if tqx__ytssa == ('min', 'builtins'):
            ejpuq__nnfpe = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if tqx__ytssa == ('max', 'builtins'):
            ejpuq__nnfpe = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return ejpuq__nnfpe


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    djwu__vmc = len(redvars)
    wve__qnd = 1
    in_vars = []
    for dywcr__rouz in range(wve__qnd):
        swch__fvblg = ir.Var(arr_var.scope, f'$input{dywcr__rouz}', arr_var.loc
            )
        in_vars.append(swch__fvblg)
    rwvlk__rropf = parfor.loop_nests[0].index_variable
    mmiw__cubal = [0] * djwu__vmc
    for inqf__kmhy in parfor.loop_body.values():
        uqqpx__lunzz = []
        for qtuy__uxv in inqf__kmhy.body:
            if is_var_assign(qtuy__uxv
                ) and qtuy__uxv.value.name == rwvlk__rropf.name:
                continue
            if is_getitem(qtuy__uxv
                ) and qtuy__uxv.value.value.name == arr_var.name:
                qtuy__uxv.value = in_vars[0]
            if is_call_assign(qtuy__uxv) and guard(find_callname, pm.
                func_ir, qtuy__uxv.value) == ('isna', 'bodo.libs.array_kernels'
                ) and qtuy__uxv.value.args[0].name == arr_var.name:
                qtuy__uxv.value = ir.Const(False, qtuy__uxv.target.loc)
            if is_assign(qtuy__uxv) and qtuy__uxv.target.name in redvars:
                ind = redvars.index(qtuy__uxv.target.name)
                mmiw__cubal[ind] = qtuy__uxv.target
            uqqpx__lunzz.append(qtuy__uxv)
        inqf__kmhy.body = uqqpx__lunzz
    kezxo__lke = ['v{}'.format(dywcr__rouz) for dywcr__rouz in range(djwu__vmc)
        ]
    jnjvk__fegm = ['in{}'.format(dywcr__rouz) for dywcr__rouz in range(
        wve__qnd)]
    ejpuq__nnfpe = 'def agg_update({}):\n'.format(', '.join(kezxo__lke +
        jnjvk__fegm))
    ejpuq__nnfpe += '    __update_redvars()\n'
    ejpuq__nnfpe += '    return {}'.format(', '.join(['v{}'.format(
        dywcr__rouz) for dywcr__rouz in range(djwu__vmc)]))
    bqx__hvw = {}
    exec(ejpuq__nnfpe, {}, bqx__hvw)
    gbv__ffe = bqx__hvw['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * wve__qnd)
    f_ir = compile_to_numba_ir(gbv__ffe, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    qfms__xodww = f_ir.blocks.popitem()[1].body
    xnc__vlm = pm.typemap[qfms__xodww[-1].value.name]
    aln__gjedk = wrap_parfor_blocks(parfor)
    ltgl__dpnxo = find_topo_order(aln__gjedk)
    ltgl__dpnxo = ltgl__dpnxo[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    xmy__ekih = f_ir.blocks[ltgl__dpnxo[0]]
    ozx__dbh = f_ir.blocks[ltgl__dpnxo[-1]]
    mtl__ddgk = qfms__xodww[:djwu__vmc + wve__qnd]
    if djwu__vmc > 1:
        ispg__jlcyd = qfms__xodww[-3:]
        assert is_assign(ispg__jlcyd[0]) and isinstance(ispg__jlcyd[0].
            value, ir.Expr) and ispg__jlcyd[0].value.op == 'build_tuple'
    else:
        ispg__jlcyd = qfms__xodww[-2:]
    for dywcr__rouz in range(djwu__vmc):
        avjxc__ngmff = qfms__xodww[dywcr__rouz].target
        fluv__bgc = ir.Assign(avjxc__ngmff, mmiw__cubal[dywcr__rouz],
            avjxc__ngmff.loc)
        mtl__ddgk.append(fluv__bgc)
    for dywcr__rouz in range(djwu__vmc, djwu__vmc + wve__qnd):
        avjxc__ngmff = qfms__xodww[dywcr__rouz].target
        fluv__bgc = ir.Assign(avjxc__ngmff, in_vars[dywcr__rouz - djwu__vmc
            ], avjxc__ngmff.loc)
        mtl__ddgk.append(fluv__bgc)
    xmy__ekih.body = mtl__ddgk + xmy__ekih.body
    tac__yki = []
    for dywcr__rouz in range(djwu__vmc):
        avjxc__ngmff = qfms__xodww[dywcr__rouz].target
        fluv__bgc = ir.Assign(mmiw__cubal[dywcr__rouz], avjxc__ngmff,
            avjxc__ngmff.loc)
        tac__yki.append(fluv__bgc)
    ozx__dbh.body += tac__yki + ispg__jlcyd
    vjs__dvo = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xnc__vlm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    noerg__lmhrv = numba.core.target_extension.dispatcher_registry[cpu_target](
        gbv__ffe)
    noerg__lmhrv.add_overload(vjs__dvo)
    return noerg__lmhrv


def _rm_arg_agg_block(block, typemap):
    lzs__xrf = []
    arr_var = None
    for dywcr__rouz, qtuy__uxv in enumerate(block.body):
        if is_assign(qtuy__uxv) and isinstance(qtuy__uxv.value, ir.Arg):
            arr_var = qtuy__uxv.target
            rjjfd__ngxd = typemap[arr_var.name]
            if not isinstance(rjjfd__ngxd, types.ArrayCompatible):
                lzs__xrf += block.body[dywcr__rouz + 1:]
                break
            qeoq__mtfky = block.body[dywcr__rouz + 1]
            assert is_assign(qeoq__mtfky) and isinstance(qeoq__mtfky.value,
                ir.Expr
                ) and qeoq__mtfky.value.op == 'getattr' and qeoq__mtfky.value.attr == 'shape' and qeoq__mtfky.value.value.name == arr_var.name
            reqng__itmeh = qeoq__mtfky.target
            uacw__dif = block.body[dywcr__rouz + 2]
            assert is_assign(uacw__dif) and isinstance(uacw__dif.value, ir.Expr
                ) and uacw__dif.value.op == 'static_getitem' and uacw__dif.value.value.name == reqng__itmeh.name
            lzs__xrf += block.body[dywcr__rouz + 3:]
            break
        lzs__xrf.append(qtuy__uxv)
    return lzs__xrf, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    aln__gjedk = wrap_parfor_blocks(parfor)
    ltgl__dpnxo = find_topo_order(aln__gjedk)
    ltgl__dpnxo = ltgl__dpnxo[1:]
    unwrap_parfor_blocks(parfor)
    for kfsn__xrb in reversed(ltgl__dpnxo):
        for qtuy__uxv in reversed(parfor.loop_body[kfsn__xrb].body):
            if isinstance(qtuy__uxv, ir.Assign) and (qtuy__uxv.target.name in
                parfor_params or qtuy__uxv.target.name in var_to_param):
                wuu__andoe = qtuy__uxv.target.name
                rhs = qtuy__uxv.value
                tbkd__ave = (wuu__andoe if wuu__andoe in parfor_params else
                    var_to_param[wuu__andoe])
                gukp__chyr = []
                if isinstance(rhs, ir.Var):
                    gukp__chyr = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    gukp__chyr = [qkwzf__kcu.name for qkwzf__kcu in
                        qtuy__uxv.value.list_vars()]
                param_uses[tbkd__ave].extend(gukp__chyr)
                for qkwzf__kcu in gukp__chyr:
                    var_to_param[qkwzf__kcu] = tbkd__ave
            if isinstance(qtuy__uxv, Parfor):
                get_parfor_reductions(qtuy__uxv, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for tgj__zzhq, gukp__chyr in param_uses.items():
        if tgj__zzhq in gukp__chyr and tgj__zzhq not in reduce_varnames:
            reduce_varnames.append(tgj__zzhq)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
