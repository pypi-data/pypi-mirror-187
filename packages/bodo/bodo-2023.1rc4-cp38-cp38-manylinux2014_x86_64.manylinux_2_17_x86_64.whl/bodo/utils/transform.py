"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'FloatingArrayType', 'IntervalArrayType',
    'IntervalIndexType', 'List', 'MapArrayType', 'NumericIndexType',
    'PDCategoricalDtype', 'PeriodIndexType', 'RangeIndexType', 'SeriesType',
    'StringIndexType', 'BinaryIndexType', 'StructArrayType',
    'TimedeltaIndexType', 'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('Int32Dtype',
    pd), ('Int64Dtype', pd), ('Timestamp', pd), ('Week', 'offsets',
    'tseries', pd), ('init_series', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_data', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_index', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'init_float_array', 'float_arr_ext', 'libs', bodo), (
    'alloc_float_array', 'float_arr_ext', 'libs', bodo), ('inplace_eq',
    'str_arr_ext', 'libs', bodo), ('get_bool_arr_data', 'bool_arr_ext',
    'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext', 'libs', bodo), (
    'init_bool_array', 'bool_arr_ext', 'libs', bodo), ('alloc_bool_array',
    'bool_arr_ext', 'libs', bodo), ('datetime_date_arr_to_dt64_arr',
    'pd_timestamp_ext', 'hiframes', bodo), ('alloc_pd_datetime_array',
    'pd_datetime_arr_ext', 'libs', bodo), (bodo.libs.bool_arr_ext.
    compute_or_body,), (bodo.libs.bool_arr_ext.compute_and_body,), (
    'alloc_datetime_date_array', 'datetime_date_ext', 'hiframes', bodo), (
    'alloc_datetime_timedelta_array', 'datetime_timedelta_ext', 'hiframes',
    bodo), ('cat_replace', 'pd_categorical_ext', 'hiframes', bodo), (
    'init_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'alloc_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'get_categorical_arr_codes', 'pd_categorical_ext', 'hiframes', bodo), (
    '_sum_handle_nan', 'series_kernels', 'hiframes', bodo), ('_box_cat_val',
    'series_kernels', 'hiframes', bodo), ('_mean_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_var_handle_mincount',
    'series_kernels', 'hiframes', bodo), ('_compute_var_nan_count_ddof',
    'series_kernels', 'hiframes', bodo), ('_sem_handle_nan',
    'series_kernels', 'hiframes', bodo), ('dist_return', 'distributed_api',
    'libs', bodo), ('rep_return', 'distributed_api', 'libs', bodo), (
    'init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_all_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), (bodo.libs.str_arr_ext.
    num_total_chars,), ('num_total_chars', 'str_arr_ext', 'libs', bodo), (
    'copy',), ('from_iterable_impl', 'typing', 'utils', bodo), ('chain',
    itertools), ('groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.
    hiframes.pd_categorical_ext.get_code_for_value,), ('asarray', np), (
    'int32', np), ('int64', np), ('float64', np), ('float32', np), ('bool_',
    np), ('full', np), ('round', np), ('isnan', np), ('isnat', np), (
    'arange', np), ('internal_prange', 'parfor', numba), ('internal_prange',
    'parfor', 'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe',
    numba), ('_slice_span', 'unicode', numba), ('_normalize_slice',
    'unicode', numba), ('init_session_builder', 'pyspark_ext', 'libs', bodo
    ), ('init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_to_numeric', 'dict_arr_ext',
    'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs', bodo), (
    'dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_capitalize', 'dict_arr_ext', 'libs', bodo), ('str_lower',
    'dict_arr_ext', 'libs', bodo), ('str_swapcase', 'dict_arr_ext', 'libs',
    bodo), ('str_title', 'dict_arr_ext', 'libs', bodo), ('str_upper',
    'dict_arr_ext', 'libs', bodo), ('str_center', 'dict_arr_ext', 'libs',
    bodo), ('str_get', 'dict_arr_ext', 'libs', bodo), ('str_repeat_int',
    'dict_arr_ext', 'libs', bodo), ('str_lstrip', 'dict_arr_ext', 'libs',
    bodo), ('str_rstrip', 'dict_arr_ext', 'libs', bodo), ('str_strip',
    'dict_arr_ext', 'libs', bodo), ('str_zfill', 'dict_arr_ext', 'libs',
    bodo), ('str_ljust', 'dict_arr_ext', 'libs', bodo), ('str_rjust',
    'dict_arr_ext', 'libs', bodo), ('str_find', 'dict_arr_ext', 'libs',
    bodo), ('str_rfind', 'dict_arr_ext', 'libs', bodo), ('str_index',
    'dict_arr_ext', 'libs', bodo), ('str_rindex', 'dict_arr_ext', 'libs',
    bodo), ('str_slice', 'dict_arr_ext', 'libs', bodo), ('str_extract',
    'dict_arr_ext', 'libs', bodo), ('str_extractall', 'dict_arr_ext',
    'libs', bodo), ('str_extractall_multi', 'dict_arr_ext', 'libs', bodo),
    ('str_len', 'dict_arr_ext', 'libs', bodo), ('str_count', 'dict_arr_ext',
    'libs', bodo), ('str_isalnum', 'dict_arr_ext', 'libs', bodo), (
    'str_isalpha', 'dict_arr_ext', 'libs', bodo), ('str_isdigit',
    'dict_arr_ext', 'libs', bodo), ('str_isspace', 'dict_arr_ext', 'libs',
    bodo), ('str_islower', 'dict_arr_ext', 'libs', bodo), ('str_isupper',
    'dict_arr_ext', 'libs', bodo), ('str_istitle', 'dict_arr_ext', 'libs',
    bodo), ('str_isnumeric', 'dict_arr_ext', 'libs', bodo), (
    'str_isdecimal', 'dict_arr_ext', 'libs', bodo), ('str_match',
    'dict_arr_ext', 'libs', bodo), ('prange', bodo), (bodo.prange,), (
    'objmode', bodo), (bodo.objmode,), ('get_label_dict_from_categories',
    'pd_categorial_ext', 'hiframes', bodo), (
    'get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo), ('table_astype', 'table_utils', 'utils', bodo), ('table_concat',
    'table_utils', 'utils', bodo), ('table_filter', 'table', 'hiframes',
    bodo), ('table_subset', 'table', 'hiframes', bodo), (
    'logical_table_to_table', 'table', 'hiframes', bodo), ('set_table_data',
    'table', 'hiframes', bodo), ('set_table_null', 'table', 'hiframes',
    bodo), ('startswith',), ('endswith',), ('upper',), ('lower',), (
    '__bodosql_replace_columns_dummy', 'dataframe_impl', 'hiframes', bodo)}
_np_type_names = {'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16',
    'uint32', 'uint64', 'float32', 'float64', 'bool_'}


def remove_hiframes(rhs, lives, call_list):
    zvzic__yxcpq = tuple(call_list)
    if zvzic__yxcpq in no_side_effect_call_tuples:
        return True
    if zvzic__yxcpq == (bodo.hiframes.pd_index_ext.init_range_index,):
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if call_list[1:] == ['bodosql_array_kernels', 'libs', bodo]:
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list in (['setna', 'array_kernels', 'libs', bodo], [
        'copy_array_element', 'array_kernels', 'libs', bodo], [
        'get_str_arr_item_copy', 'str_arr_ext', 'libs', bodo]) and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(zvzic__yxcpq) == 1 and tuple in getattr(zvzic__yxcpq[0],
        '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        ezhx__iwawf = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        ezhx__iwawf = func.__globals__
    if extra_globals is not None:
        ezhx__iwawf.update(extra_globals)
    if add_default_globals:
        ezhx__iwawf.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd':
            pd, 'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, ezhx__iwawf, typingctx=typing_info
            .typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[rdz__jgnq.name] for rdz__jgnq in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, ezhx__iwawf)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        emal__qsy = tuple(typing_info.typemap[rdz__jgnq.name] for rdz__jgnq in
            args)
        ctj__cvchs = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, emal__qsy, {}, {}, flags)
        ctj__cvchs.run()
    csadt__ljxua = f_ir.blocks.popitem()[1]
    replace_arg_nodes(csadt__ljxua, args)
    zhbi__zpnpu = csadt__ljxua.body[:-2]
    update_locs(zhbi__zpnpu[len(args):], loc)
    for stmt in zhbi__zpnpu[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        pawo__mxlfv = csadt__ljxua.body[-2]
        assert is_assign(pawo__mxlfv) and is_expr(pawo__mxlfv.value, 'cast')
        hgxg__fmrr = pawo__mxlfv.value.value
        zhbi__zpnpu.append(ir.Assign(hgxg__fmrr, ret_var, loc))
    return zhbi__zpnpu


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for lmf__owvpl in stmt.list_vars():
            lmf__owvpl.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        fgfaf__orb = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        igllw__lzs, qkmcr__pccn = fgfaf__orb(stmt)
        return qkmcr__pccn
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        yvlxl__xvldd = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(yvlxl__xvldd, ir.UndefinedType):
            ziszb__uulx = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{ziszb__uulx}' is not defined", loc=loc)
    except GuardException as aiifb__ilrwa:
        raise BodoError(err_msg, loc=loc)
    return yvlxl__xvldd


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    zrgj__fwsdy = get_definition(func_ir, var)
    mxdly__mwwue = None
    if typemap is not None:
        mxdly__mwwue = typemap.get(var.name, None)
    if isinstance(zrgj__fwsdy, ir.Arg) and arg_types is not None:
        mxdly__mwwue = arg_types[zrgj__fwsdy.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(mxdly__mwwue):
        return get_literal_value(mxdly__mwwue)
    if isinstance(zrgj__fwsdy, (ir.Const, ir.Global, ir.FreeVar)):
        yvlxl__xvldd = zrgj__fwsdy.value
        return yvlxl__xvldd
    if literalize_args and isinstance(zrgj__fwsdy, ir.Arg
        ) and can_literalize_type(mxdly__mwwue, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({zrgj__fwsdy.index}, loc=
            var.loc, file_infos={zrgj__fwsdy.index: file_info} if file_info
             is not None else None)
    if is_expr(zrgj__fwsdy, 'binop'):
        if file_info and zrgj__fwsdy.fn == operator.add:
            try:
                ojq__rqtkd = get_const_value_inner(func_ir, zrgj__fwsdy.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ojq__rqtkd, True)
                cqj__wvq = get_const_value_inner(func_ir, zrgj__fwsdy.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return zrgj__fwsdy.fn(ojq__rqtkd, cqj__wvq)
            except (GuardException, BodoConstUpdatedError) as aiifb__ilrwa:
                pass
            try:
                cqj__wvq = get_const_value_inner(func_ir, zrgj__fwsdy.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(cqj__wvq, False)
                ojq__rqtkd = get_const_value_inner(func_ir, zrgj__fwsdy.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return zrgj__fwsdy.fn(ojq__rqtkd, cqj__wvq)
            except (GuardException, BodoConstUpdatedError) as aiifb__ilrwa:
                pass
        ojq__rqtkd = get_const_value_inner(func_ir, zrgj__fwsdy.lhs,
            arg_types, typemap, updated_containers)
        cqj__wvq = get_const_value_inner(func_ir, zrgj__fwsdy.rhs,
            arg_types, typemap, updated_containers)
        return zrgj__fwsdy.fn(ojq__rqtkd, cqj__wvq)
    if is_expr(zrgj__fwsdy, 'unary'):
        yvlxl__xvldd = get_const_value_inner(func_ir, zrgj__fwsdy.value,
            arg_types, typemap, updated_containers)
        return zrgj__fwsdy.fn(yvlxl__xvldd)
    if is_expr(zrgj__fwsdy, 'getattr') and typemap:
        tob__pgvp = typemap.get(zrgj__fwsdy.value.name, None)
        if isinstance(tob__pgvp, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and zrgj__fwsdy.attr == 'columns':
            return pd.Index(tob__pgvp.columns)
        if isinstance(tob__pgvp, types.SliceType):
            uaugc__qflqe = get_definition(func_ir, zrgj__fwsdy.value)
            require(is_call(uaugc__qflqe))
            etrdd__lzmnx = find_callname(func_ir, uaugc__qflqe)
            desq__dfukm = False
            if etrdd__lzmnx == ('_normalize_slice', 'numba.cpython.unicode'):
                require(zrgj__fwsdy.attr in ('start', 'step'))
                uaugc__qflqe = get_definition(func_ir, uaugc__qflqe.args[0])
                desq__dfukm = True
            require(find_callname(func_ir, uaugc__qflqe) == ('slice',
                'builtins'))
            if len(uaugc__qflqe.args) == 1:
                if zrgj__fwsdy.attr == 'start':
                    return 0
                if zrgj__fwsdy.attr == 'step':
                    return 1
                require(zrgj__fwsdy.attr == 'stop')
                return get_const_value_inner(func_ir, uaugc__qflqe.args[0],
                    arg_types, typemap, updated_containers)
            if zrgj__fwsdy.attr == 'start':
                yvlxl__xvldd = get_const_value_inner(func_ir, uaugc__qflqe.
                    args[0], arg_types, typemap, updated_containers)
                if yvlxl__xvldd is None:
                    yvlxl__xvldd = 0
                if desq__dfukm:
                    require(yvlxl__xvldd == 0)
                return yvlxl__xvldd
            if zrgj__fwsdy.attr == 'stop':
                assert not desq__dfukm
                return get_const_value_inner(func_ir, uaugc__qflqe.args[1],
                    arg_types, typemap, updated_containers)
            require(zrgj__fwsdy.attr == 'step')
            if len(uaugc__qflqe.args) == 2:
                return 1
            else:
                yvlxl__xvldd = get_const_value_inner(func_ir, uaugc__qflqe.
                    args[2], arg_types, typemap, updated_containers)
                if yvlxl__xvldd is None:
                    yvlxl__xvldd = 1
                if desq__dfukm:
                    require(yvlxl__xvldd == 1)
                return yvlxl__xvldd
    if is_expr(zrgj__fwsdy, 'getattr'):
        return getattr(get_const_value_inner(func_ir, zrgj__fwsdy.value,
            arg_types, typemap, updated_containers), zrgj__fwsdy.attr)
    if is_expr(zrgj__fwsdy, 'getitem'):
        value = get_const_value_inner(func_ir, zrgj__fwsdy.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, zrgj__fwsdy.index, arg_types,
            typemap, updated_containers)
        return value[index]
    oatll__libiv = guard(find_callname, func_ir, zrgj__fwsdy, typemap)
    if oatll__libiv is not None and len(oatll__libiv) == 2 and oatll__libiv[0
        ] == 'keys' and isinstance(oatll__libiv[1], ir.Var):
        kbpu__mlmwy = zrgj__fwsdy.func
        zrgj__fwsdy = get_definition(func_ir, oatll__libiv[1])
        diyyp__sri = oatll__libiv[1].name
        if updated_containers and diyyp__sri in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                diyyp__sri, updated_containers[diyyp__sri]))
        require(is_expr(zrgj__fwsdy, 'build_map'))
        vals = [lmf__owvpl[0] for lmf__owvpl in zrgj__fwsdy.items]
        dxvwj__pakaw = guard(get_definition, func_ir, kbpu__mlmwy)
        assert isinstance(dxvwj__pakaw, ir.Expr
            ) and dxvwj__pakaw.attr == 'keys'
        dxvwj__pakaw.attr = 'copy'
        return [get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in vals]
    if is_expr(zrgj__fwsdy, 'build_map'):
        return {get_const_value_inner(func_ir, lmf__owvpl[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            lmf__owvpl[1], arg_types, typemap, updated_containers) for
            lmf__owvpl in zrgj__fwsdy.items}
    if is_expr(zrgj__fwsdy, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.items)
    if is_expr(zrgj__fwsdy, 'build_list'):
        return [get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.items]
    if is_expr(zrgj__fwsdy, 'build_set'):
        return {get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.items}
    if oatll__libiv == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if oatll__libiv == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('range', 'builtins') and len(zrgj__fwsdy.args) == 1:
        return range(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, lmf__owvpl,
            arg_types, typemap, updated_containers) for lmf__owvpl in
            zrgj__fwsdy.args))
    if oatll__libiv == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('format', 'builtins'):
        rdz__jgnq = get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers)
        idhh__ckp = get_const_value_inner(func_ir, zrgj__fwsdy.args[1],
            arg_types, typemap, updated_containers) if len(zrgj__fwsdy.args
            ) > 1 else ''
        return format(rdz__jgnq, idhh__ckp)
    if oatll__libiv in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, zrgj__fwsdy.
            args[0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, zrgj__fwsdy.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            zrgj__fwsdy.args[2], arg_types, typemap, updated_containers))
    if oatll__libiv == ('len', 'builtins') and typemap and isinstance(typemap
        .get(zrgj__fwsdy.args[0].name, None), types.BaseTuple):
        return len(typemap[zrgj__fwsdy.args[0].name])
    if oatll__libiv == ('len', 'builtins'):
        mekkk__bgegs = guard(get_definition, func_ir, zrgj__fwsdy.args[0])
        if isinstance(mekkk__bgegs, ir.Expr) and mekkk__bgegs.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(mekkk__bgegs.items)
        return len(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv == ('CategoricalDtype', 'pandas'):
        kws = dict(zrgj__fwsdy.kws)
        lqm__lvf = get_call_expr_arg('CategoricalDtype', zrgj__fwsdy.args,
            kws, 0, 'categories', '')
        pqqo__pvv = get_call_expr_arg('CategoricalDtype', zrgj__fwsdy.args,
            kws, 1, 'ordered', False)
        if pqqo__pvv is not False:
            pqqo__pvv = get_const_value_inner(func_ir, pqqo__pvv, arg_types,
                typemap, updated_containers)
        if lqm__lvf == '':
            lqm__lvf = None
        else:
            lqm__lvf = get_const_value_inner(func_ir, lqm__lvf, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(lqm__lvf, pqqo__pvv)
    if oatll__libiv == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, zrgj__fwsdy.args[0],
            arg_types, typemap, updated_containers))
    if oatll__libiv is not None and oatll__libiv[1
        ] == 'numpy' and oatll__libiv[0] in _np_type_names:
        return getattr(np, oatll__libiv[0])(get_const_value_inner(func_ir,
            zrgj__fwsdy.args[0], arg_types, typemap, updated_containers))
    if oatll__libiv is not None and len(oatll__libiv) == 2 and oatll__libiv[1
        ] == 'pandas' and oatll__libiv[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, oatll__libiv[0])()
    if oatll__libiv is not None and len(oatll__libiv) == 2 and isinstance(
        oatll__libiv[1], ir.Var):
        yvlxl__xvldd = get_const_value_inner(func_ir, oatll__libiv[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.args]
        kws = {qmhsh__urjcj[0]: get_const_value_inner(func_ir, qmhsh__urjcj
            [1], arg_types, typemap, updated_containers) for qmhsh__urjcj in
            zrgj__fwsdy.kws}
        return getattr(yvlxl__xvldd, oatll__libiv[0])(*args, **kws)
    if oatll__libiv is not None and len(oatll__libiv) == 2 and oatll__libiv[1
        ] == 'bodo' and oatll__libiv[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.args)
        kwargs = {ziszb__uulx: get_const_value_inner(func_ir, lmf__owvpl,
            arg_types, typemap, updated_containers) for ziszb__uulx,
            lmf__owvpl in dict(zrgj__fwsdy.kws).items()}
        return getattr(bodo, oatll__libiv[0])(*args, **kwargs)
    if is_call(zrgj__fwsdy) and typemap and isinstance(typemap.get(
        zrgj__fwsdy.func.name, None), types.Dispatcher):
        py_func = typemap[zrgj__fwsdy.func.name].dispatcher.py_func
        require(zrgj__fwsdy.vararg is None)
        args = tuple(get_const_value_inner(func_ir, lmf__owvpl, arg_types,
            typemap, updated_containers) for lmf__owvpl in zrgj__fwsdy.args)
        kwargs = {ziszb__uulx: get_const_value_inner(func_ir, lmf__owvpl,
            arg_types, typemap, updated_containers) for ziszb__uulx,
            lmf__owvpl in dict(zrgj__fwsdy.kws).items()}
        arg_types = tuple(bodo.typeof(lmf__owvpl) for lmf__owvpl in args)
        kw_types = {zatpl__fdmiz: bodo.typeof(lmf__owvpl) for zatpl__fdmiz,
            lmf__owvpl in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, ood__mdeeu, ood__mdeeu = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    opax__opppt = guard(get_definition, f_ir, rhs.func)
                    if isinstance(opax__opppt, ir.Const) and isinstance(
                        opax__opppt.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    tgsrc__fleud = guard(find_callname, f_ir, rhs)
                    if tgsrc__fleud is None:
                        return False
                    func_name, cvxix__jcucw = tgsrc__fleud
                    if cvxix__jcucw == 'pandas' and func_name.startswith(
                        'read_'):
                        return False
                    if tgsrc__fleud in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if tgsrc__fleud == ('File', 'h5py'):
                        return False
                    if isinstance(cvxix__jcucw, ir.Var):
                        mxdly__mwwue = typemap[cvxix__jcucw.name]
                        if isinstance(mxdly__mwwue, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(mxdly__mwwue, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(mxdly__mwwue, bodo.LoggingLoggerType):
                            return False
                        if str(mxdly__mwwue).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            cvxix__jcucw), ir.Arg)):
                            return False
                    if cvxix__jcucw in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        nzkgi__hfbx = func.literal_value.code
        ccn__feftk = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            ccn__feftk = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(ccn__feftk, nzkgi__hfbx)
        fix_struct_return(f_ir)
        typemap, rtf__nfhso, eice__ubj, ood__mdeeu = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, eice__ubj, rtf__nfhso = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, eice__ubj, rtf__nfhso = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, eice__ubj, rtf__nfhso = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(rtf__nfhso, types.DictType):
        lbxg__vhiu = guard(get_struct_keynames, f_ir, typemap)
        if lbxg__vhiu is not None:
            rtf__nfhso = StructType((rtf__nfhso.value_type,) * len(
                lbxg__vhiu), lbxg__vhiu)
    if is_udf and isinstance(rtf__nfhso, (SeriesType, HeterogeneousSeriesType)
        ):
        icspq__qmwuq = numba.core.registry.cpu_target.typing_context
        qeor__exo = numba.core.registry.cpu_target.target_context
        zgc__vvzqu = bodo.transforms.series_pass.SeriesPass(f_ir,
            icspq__qmwuq, qeor__exo, typemap, eice__ubj, {})
        elr__wdk = zgc__vvzqu.run()
        if elr__wdk:
            elr__wdk = zgc__vvzqu.run()
            if elr__wdk:
                zgc__vvzqu.run()
        vpbs__wlgi = compute_cfg_from_blocks(f_ir.blocks)
        frw__rdpmr = [guard(_get_const_series_info, f_ir.blocks[wmvtd__baja
            ], f_ir, typemap) for wmvtd__baja in vpbs__wlgi.exit_points() if
            isinstance(f_ir.blocks[wmvtd__baja].body[-1], ir.Return)]
        if None in frw__rdpmr or len(pd.Series(frw__rdpmr).unique()) != 1:
            rtf__nfhso.const_info = None
        else:
            rtf__nfhso.const_info = frw__rdpmr[0]
    return rtf__nfhso


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    enzt__vcdrf = block.body[-1].value
    mzdz__jplu = get_definition(f_ir, enzt__vcdrf)
    require(is_expr(mzdz__jplu, 'cast'))
    mzdz__jplu = get_definition(f_ir, mzdz__jplu.value)
    require(is_call(mzdz__jplu) and find_callname(f_ir, mzdz__jplu) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    kcaiy__yqe = mzdz__jplu.args[1]
    fnwo__xek = tuple(get_const_value_inner(f_ir, kcaiy__yqe, typemap=typemap))
    if isinstance(typemap[enzt__vcdrf.name], HeterogeneousSeriesType):
        return len(typemap[enzt__vcdrf.name].data), fnwo__xek
    wvsi__cjq = mzdz__jplu.args[0]
    car__vkf = get_definition(f_ir, wvsi__cjq)
    func_name, wiaa__mgiy = find_callname(f_ir, car__vkf)
    if is_call(car__vkf) and bodo.utils.utils.is_alloc_callname(func_name,
        wiaa__mgiy):
        duds__asw = car__vkf.args[0]
        hqse__qzleu = get_const_value_inner(f_ir, duds__asw, typemap=typemap)
        return hqse__qzleu, fnwo__xek
    if is_call(car__vkf) and find_callname(f_ir, car__vkf) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        wvsi__cjq = car__vkf.args[0]
        car__vkf = get_definition(f_ir, wvsi__cjq)
    require(is_expr(car__vkf, 'build_tuple') or is_expr(car__vkf, 'build_list')
        )
    return len(car__vkf.items), fnwo__xek


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    gkn__fyn = []
    ksoo__lxv = []
    values = []
    for zatpl__fdmiz, lmf__owvpl in build_map.items:
        hho__jvg = find_const(f_ir, zatpl__fdmiz)
        require(isinstance(hho__jvg, str))
        ksoo__lxv.append(hho__jvg)
        gkn__fyn.append(zatpl__fdmiz)
        values.append(lmf__owvpl)
    mkz__vzz = ir.Var(scope, mk_unique_var('val_tup'), loc)
    kclkj__xtf = ir.Assign(ir.Expr.build_tuple(values, loc), mkz__vzz, loc)
    f_ir._definitions[mkz__vzz.name] = [kclkj__xtf.value]
    bvwk__jsj = ir.Var(scope, mk_unique_var('key_tup'), loc)
    ruh__xvxlb = ir.Assign(ir.Expr.build_tuple(gkn__fyn, loc), bvwk__jsj, loc)
    f_ir._definitions[bvwk__jsj.name] = [ruh__xvxlb.value]
    if typemap is not None:
        typemap[mkz__vzz.name] = types.Tuple([typemap[lmf__owvpl.name] for
            lmf__owvpl in values])
        typemap[bvwk__jsj.name] = types.Tuple([typemap[lmf__owvpl.name] for
            lmf__owvpl in gkn__fyn])
    return ksoo__lxv, mkz__vzz, kclkj__xtf, bvwk__jsj, ruh__xvxlb


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    ynvx__fvav = block.body[-1].value
    nxh__ixwp = guard(get_definition, f_ir, ynvx__fvav)
    require(is_expr(nxh__ixwp, 'cast'))
    mzdz__jplu = guard(get_definition, f_ir, nxh__ixwp.value)
    require(is_expr(mzdz__jplu, 'build_map'))
    require(len(mzdz__jplu.items) > 0)
    loc = block.loc
    scope = block.scope
    ksoo__lxv, mkz__vzz, kclkj__xtf, bvwk__jsj, ruh__xvxlb = (
        extract_keyvals_from_struct_map(f_ir, mzdz__jplu, loc, scope))
    dyu__tfi = ir.Var(scope, mk_unique_var('conv_call'), loc)
    vhl__nkaly = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), dyu__tfi, loc)
    f_ir._definitions[dyu__tfi.name] = [vhl__nkaly.value]
    qso__fzhh = ir.Var(scope, mk_unique_var('struct_val'), loc)
    zutzi__xgip = ir.Assign(ir.Expr.call(dyu__tfi, [mkz__vzz, bvwk__jsj], {
        }, loc), qso__fzhh, loc)
    f_ir._definitions[qso__fzhh.name] = [zutzi__xgip.value]
    nxh__ixwp.value = qso__fzhh
    mzdz__jplu.items = [(zatpl__fdmiz, zatpl__fdmiz) for zatpl__fdmiz,
        ood__mdeeu in mzdz__jplu.items]
    block.body = block.body[:-2] + [kclkj__xtf, ruh__xvxlb, vhl__nkaly,
        zutzi__xgip] + block.body[-2:]
    return tuple(ksoo__lxv)


def get_struct_keynames(f_ir, typemap):
    vpbs__wlgi = compute_cfg_from_blocks(f_ir.blocks)
    soze__jldqt = list(vpbs__wlgi.exit_points())[0]
    block = f_ir.blocks[soze__jldqt]
    require(isinstance(block.body[-1], ir.Return))
    ynvx__fvav = block.body[-1].value
    nxh__ixwp = guard(get_definition, f_ir, ynvx__fvav)
    require(is_expr(nxh__ixwp, 'cast'))
    mzdz__jplu = guard(get_definition, f_ir, nxh__ixwp.value)
    require(is_call(mzdz__jplu) and find_callname(f_ir, mzdz__jplu) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[mzdz__jplu.args[1].name])


def fix_struct_return(f_ir):
    bsmv__etif = None
    vpbs__wlgi = compute_cfg_from_blocks(f_ir.blocks)
    for soze__jldqt in vpbs__wlgi.exit_points():
        bsmv__etif = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            soze__jldqt], soze__jldqt)
    return bsmv__etif


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    xqzw__gdk = ir.Block(ir.Scope(None, loc), loc)
    xqzw__gdk.body = node_list
    build_definitions({(0): xqzw__gdk}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(lmf__owvpl) for lmf__owvpl in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    qop__vqga = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(qop__vqga, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for divdc__zth in range(len(vals) - 1, -1, -1):
        lmf__owvpl = vals[divdc__zth]
        if isinstance(lmf__owvpl, str) and lmf__owvpl.startswith(
            NESTED_TUP_SENTINEL):
            rfskt__nvm = int(lmf__owvpl[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:divdc__zth]) + (
                tuple(vals[divdc__zth + 1:divdc__zth + rfskt__nvm + 1]),) +
                tuple(vals[divdc__zth + rfskt__nvm + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    rdz__jgnq = None
    if len(args) > arg_no and arg_no >= 0:
        rdz__jgnq = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        rdz__jgnq = kws[arg_name]
    if rdz__jgnq is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return rdz__jgnq


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    ezhx__iwawf = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        ezhx__iwawf.update(extra_globals)
    func.__globals__.update(ezhx__iwawf)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            xki__idof = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[xki__idof.name] = types.literal(default)
            except:
                pass_info.typemap[xki__idof.name] = numba.typeof(default)
            dimes__nqx = ir.Assign(ir.Const(default, loc), xki__idof, loc)
            pre_nodes.append(dimes__nqx)
            return xki__idof
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    emal__qsy = tuple(pass_info.typemap[lmf__owvpl.name] for lmf__owvpl in args
        )
    if const:
        flpl__vwmva = []
        for divdc__zth, rdz__jgnq in enumerate(args):
            yvlxl__xvldd = guard(find_const, pass_info.func_ir, rdz__jgnq)
            if yvlxl__xvldd:
                flpl__vwmva.append(types.literal(yvlxl__xvldd))
            else:
                flpl__vwmva.append(emal__qsy[divdc__zth])
        emal__qsy = tuple(flpl__vwmva)
    return ReplaceFunc(func, emal__qsy, args, ezhx__iwawf,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(ybewd__peoa) for ybewd__peoa in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        tzn__zgh = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {tzn__zgh} = 0\n', (tzn__zgh,)
    if isinstance(t, ArrayItemArrayType):
        dyu__hxyh, hlc__gntbr = gen_init_varsize_alloc_sizes(t.dtype)
        tzn__zgh = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {tzn__zgh} = 0\n' + dyu__hxyh, (tzn__zgh,) + hlc__gntbr
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(ybewd__peoa.dtype) for
            ybewd__peoa in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(ybewd__peoa) for ybewd__peoa in t.data
            )
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(ybewd__peoa) for ybewd__peoa in t.
            types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    axo__kvp = typing_context.resolve_getattr(obj_dtype, func_name)
    if axo__kvp is None:
        qxb__rxlg = types.misc.Module(np)
        try:
            axo__kvp = typing_context.resolve_getattr(qxb__rxlg, func_name)
        except AttributeError as aiifb__ilrwa:
            axo__kvp = None
        if axo__kvp is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return axo__kvp


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    axo__kvp = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(axo__kvp, types.BoundFunction):
        if axis is not None:
            ifuet__ugznz = axo__kvp.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            ifuet__ugznz = axo__kvp.get_call_type(typing_context, (), {})
        return ifuet__ugznz.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(axo__kvp):
            ifuet__ugznz = axo__kvp.get_call_type(typing_context, (
                obj_dtype,), {})
            return ifuet__ugznz.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    axo__kvp = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(axo__kvp, types.BoundFunction):
        szk__lzab = axo__kvp.template
        if axis is not None:
            return szk__lzab._overload_func(obj_dtype, axis=axis)
        else:
            return szk__lzab._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    opskr__ssbsa = get_definition(func_ir, dict_var)
    require(isinstance(opskr__ssbsa, ir.Expr))
    require(opskr__ssbsa.op == 'build_map')
    lkcs__xhqk = opskr__ssbsa.items
    gkn__fyn = []
    values = []
    hhx__tlzl = False
    for divdc__zth in range(len(lkcs__xhqk)):
        fwswg__coafp, value = lkcs__xhqk[divdc__zth]
        try:
            mcf__nipu = get_const_value_inner(func_ir, fwswg__coafp,
                arg_types, typemap, updated_containers)
            gkn__fyn.append(mcf__nipu)
            values.append(value)
        except GuardException as aiifb__ilrwa:
            require_const_map[fwswg__coafp] = label
            hhx__tlzl = True
    if hhx__tlzl:
        raise GuardException
    return gkn__fyn, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        gkn__fyn = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as aiifb__ilrwa:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in gkn__fyn):
        raise BodoError(err_msg, loc)
    return gkn__fyn


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    gkn__fyn = _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc
        )
    evj__yzb = []
    qtmzv__qss = [bodo.transforms.typing_pass._create_const_var(
        zatpl__fdmiz, 'dict_key', scope, loc, evj__yzb) for zatpl__fdmiz in
        gkn__fyn]
    wtyj__aknuj = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        xakz__ydjy = ir.Var(scope, mk_unique_var('sentinel'), loc)
        xckl__msbcg = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        evj__yzb.append(ir.Assign(ir.Const('__bodo_tup', loc), xakz__ydjy, loc)
            )
        sxbzi__klc = [xakz__ydjy] + qtmzv__qss + wtyj__aknuj
        evj__yzb.append(ir.Assign(ir.Expr.build_tuple(sxbzi__klc, loc),
            xckl__msbcg, loc))
        return (xckl__msbcg,), evj__yzb
    else:
        wzl__wprug = ir.Var(scope, mk_unique_var('values_tup'), loc)
        hguxr__ccfr = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        evj__yzb.append(ir.Assign(ir.Expr.build_tuple(wtyj__aknuj, loc),
            wzl__wprug, loc))
        evj__yzb.append(ir.Assign(ir.Expr.build_tuple(qtmzv__qss, loc),
            hguxr__ccfr, loc))
        return (wzl__wprug, hguxr__ccfr), evj__yzb
