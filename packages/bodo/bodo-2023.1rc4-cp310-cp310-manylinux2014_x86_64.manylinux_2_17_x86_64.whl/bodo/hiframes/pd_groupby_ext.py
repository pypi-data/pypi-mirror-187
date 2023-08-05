"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_numeric_index_if_range_index, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False, _num_shuffle_keys=-1):
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        self._num_shuffle_keys = _num_shuffle_keys
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select}, {_num_shuffle_keys})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select, self._num_shuffle_keys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ammsx__bhthm = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, ammsx__bhthm)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type, dropna_type,
    _num_shuffle_keys):

    def codegen(context, builder, signature, args):
        kxr__nocx = args[0]
        lywqw__anuwz = signature.return_type
        zwfb__ova = cgutils.create_struct_proxy(lywqw__anuwz)(context, builder)
        zwfb__ova.obj = kxr__nocx
        context.nrt.incref(builder, signature.args[0], kxr__nocx)
        return zwfb__ova._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for zjj__rxgfa in keys:
        selection.remove(zjj__rxgfa)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        yqq__zbuw = get_overload_const_int(_num_shuffle_keys)
    else:
        yqq__zbuw = -1
    lywqw__anuwz = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=yqq__zbuw)
    return lywqw__anuwz(obj_type, by_type, as_index_type, dropna_type,
        _num_shuffle_keys), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, kxbx__hcrnj = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(kxbx__hcrnj, (tuple, list)):
                if len(set(kxbx__hcrnj).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(kxbx__hcrnj).difference(set(grpby.
                        df_type.columns))))
                selection = kxbx__hcrnj
            else:
                if kxbx__hcrnj not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(kxbx__hcrnj))
                selection = kxbx__hcrnj,
                series_select = True
            ryei__yby = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(ryei__yby, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, kxbx__hcrnj = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            kxbx__hcrnj):
            ryei__yby = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(kxbx__hcrnj)), {}).return_type
            return signature(ryei__yby, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    tqvlw__ifn = arr_type == ArrayItemArrayType(string_array_type)
    gcn__wifou = arr_type.dtype
    if isinstance(gcn__wifou, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {gcn__wifou} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(gcn__wifou, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {gcn__wifou} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(
        gcn__wifou, (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(gcn__wifou, (Decimal128Type, types.Integer, types.
            Float, types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(gcn__wifou, (types.Integer, types.Float, types.Boolean)):
        if tqvlw__ifn or gcn__wifou == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(gcn__wifou, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not gcn__wifou.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {gcn__wifou} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(gcn__wifou, types.Boolean) and func_name in {'cumsum',
        'mean', 'sum', 'std', 'var'}:
        if func_name in {'sum'}:
            return to_nullable_type(dtype_to_array_type(types.int64)), 'ok'
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    elif func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    elif func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    gcn__wifou = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(gcn__wifou, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(gcn__wifou, types.Integer):
            return IntDtype(gcn__wifou)
        return gcn__wifou
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        wqgqo__zpmjw = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{wqgqo__zpmjw}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for zjj__rxgfa in grp.keys:
        if multi_level_names:
            npvj__pxl = zjj__rxgfa, ''
        else:
            npvj__pxl = zjj__rxgfa
        kftwl__oae = grp.df_type.column_index[zjj__rxgfa]
        data = grp.df_type.data[kftwl__oae]
        out_columns.append(npvj__pxl)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None, raise_on_any_error=False):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name in ('head', 'ngroup'):
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name in ('head', 'ngroup'):
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        qvjsf__zpx = tuple(grp.df_type.column_index[grp.keys[behml__did]] for
            behml__did in range(len(grp.keys)))
        yclie__jgc = tuple(grp.df_type.data[kftwl__oae] for kftwl__oae in
            qvjsf__zpx)
        index = MultiIndexType(yclie__jgc, tuple(types.StringLiteral(
            zjj__rxgfa) for zjj__rxgfa in grp.keys))
    else:
        kftwl__oae = grp.df_type.column_index[grp.keys[0]]
        uwv__zcx = grp.df_type.data[kftwl__oae]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(uwv__zcx,
            types.StringLiteral(grp.keys[0]))
    otxth__ppjqu = {}
    ntdwb__xgai = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        otxth__ppjqu[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        otxth__ppjqu[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        lkbio__riib = dict(ascending=ascending)
        osmbd__dmqc = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', lkbio__riib,
            osmbd__dmqc, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for sqzy__ldbvv in columns:
            kftwl__oae = grp.df_type.column_index[sqzy__ldbvv]
            data = grp.df_type.data[kftwl__oae]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            ebgfy__kacee = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                ebgfy__kacee = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    eznbp__xymm = SeriesType(data.dtype, data, None,
                        string_type)
                    woa__fer = get_const_func_output_type(func, (
                        eznbp__xymm,), {}, typing_context, target_context)
                    if woa__fer != ArrayItemArrayType(string_array_type):
                        woa__fer = dtype_to_array_type(woa__fer)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=sqzy__ldbvv, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    jrs__ixnoa = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    jcb__yjrb = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    lkbio__riib = dict(numeric_only=jrs__ixnoa, min_count=
                        jcb__yjrb)
                    osmbd__dmqc = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lkbio__riib, osmbd__dmqc, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    jrs__ixnoa = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    jcb__yjrb = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    lkbio__riib = dict(numeric_only=jrs__ixnoa, min_count=
                        jcb__yjrb)
                    osmbd__dmqc = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lkbio__riib, osmbd__dmqc, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    jrs__ixnoa = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    lkbio__riib = dict(numeric_only=jrs__ixnoa)
                    osmbd__dmqc = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lkbio__riib, osmbd__dmqc, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    zmilc__fep = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    xgbvv__vxns = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    lkbio__riib = dict(axis=zmilc__fep, skipna=xgbvv__vxns)
                    osmbd__dmqc = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lkbio__riib, osmbd__dmqc, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    cnoiw__sanwo = args[0] if len(args) > 0 else kws.pop('ddof'
                        , 1)
                    lkbio__riib = dict(ddof=cnoiw__sanwo)
                    osmbd__dmqc = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lkbio__riib, osmbd__dmqc, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                woa__fer, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                woa__fer = to_str_arr_if_dict_array(woa__fer) if func_name in (
                    'sum', 'cumsum') else woa__fer
                out_data.append(woa__fer)
                out_columns.append(sqzy__ldbvv)
                if func_name == 'agg':
                    byb__jiojl = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    otxth__ppjqu[sqzy__ldbvv, byb__jiojl] = sqzy__ldbvv
                else:
                    otxth__ppjqu[sqzy__ldbvv, func_name] = sqzy__ldbvv
                out_column_type.append(ebgfy__kacee)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                ntdwb__xgai.append(err_msg)
    if func_name == 'sum':
        gxkd__temr = any([(xhd__lainv == ColumnType.NumericalColumn.value) for
            xhd__lainv in out_column_type])
        if gxkd__temr:
            out_data = [xhd__lainv for xhd__lainv, dfdf__uuv in zip(
                out_data, out_column_type) if dfdf__uuv != ColumnType.
                NonNumericalColumn.value]
            out_columns = [xhd__lainv for xhd__lainv, dfdf__uuv in zip(
                out_columns, out_column_type) if dfdf__uuv != ColumnType.
                NonNumericalColumn.value]
            otxth__ppjqu = {}
            for sqzy__ldbvv in out_columns:
                if grp.as_index is False and sqzy__ldbvv in grp.keys:
                    continue
                otxth__ppjqu[sqzy__ldbvv, func_name] = sqzy__ldbvv
    vtuy__gokd = len(ntdwb__xgai)
    if len(out_data) == 0:
        if vtuy__gokd == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(vtuy__gokd, ' was' if vtuy__gokd == 1 else 's were',
                ','.join(ntdwb__xgai)))
    zck__ohbbw = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            hkwi__qics = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            hkwi__qics = FloatDtype(out_data[0].dtype)
        else:
            hkwi__qics = out_data[0].dtype
        rbr__kjcix = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        zck__ohbbw = SeriesType(hkwi__qics, data=out_data[0], index=index,
            name_typ=rbr__kjcix)
    return signature(zck__ohbbw, *args), otxth__ppjqu


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    tfhio__kfw = True
    if isinstance(f_val, str):
        tfhio__kfw = False
        olrm__nfrqh = f_val
    elif is_overload_constant_str(f_val):
        tfhio__kfw = False
        olrm__nfrqh = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        tfhio__kfw = False
        olrm__nfrqh = bodo.utils.typing.get_builtin_function_name(f_val)
    if not tfhio__kfw:
        if olrm__nfrqh not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {olrm__nfrqh}')
        ryei__yby = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(ryei__yby, (), olrm__nfrqh, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            xrb__isg = types.functions.MakeFunctionLiteral(f_val)
        else:
            xrb__isg = f_val
        validate_udf('agg', xrb__isg)
        func = get_overload_const_func(xrb__isg, None)
        akz__lss = func.code if hasattr(func, 'code') else func.__code__
        olrm__nfrqh = akz__lss.co_name
        ryei__yby = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(ryei__yby, (), 'agg', typing_context,
            target_context, xrb__isg, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    return olrm__nfrqh, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    ayzg__uits = kws and all(isinstance(lkjms__jdz, types.Tuple) and len(
        lkjms__jdz) == 2 for lkjms__jdz in kws.values())
    raise_on_any_error = ayzg__uits
    if is_overload_none(func) and not ayzg__uits:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not ayzg__uits:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    vjn__iunqz = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if ayzg__uits or is_overload_constant_dict(func):
        if ayzg__uits:
            wjx__qag = [get_literal_value(pcrfq__ujxp) for pcrfq__ujxp,
                xgnnu__ddpg in kws.values()]
            clyfx__etle = [get_literal_value(jph__uwcsm) for xgnnu__ddpg,
                jph__uwcsm in kws.values()]
        else:
            qfxy__ertzw = get_overload_constant_dict(func)
            wjx__qag = tuple(qfxy__ertzw.keys())
            clyfx__etle = tuple(qfxy__ertzw.values())
        for xywjc__fba in ('head', 'ngroup'):
            if xywjc__fba in clyfx__etle:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {xywjc__fba} cannot be mixed with other groupby operations.'
                    )
        if any(sqzy__ldbvv not in grp.selection and sqzy__ldbvv not in grp.
            keys for sqzy__ldbvv in wjx__qag):
            raise_bodo_error(
                f'Selected column names {wjx__qag} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            clyfx__etle)
        if ayzg__uits and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        otxth__ppjqu = {}
        out_columns = []
        out_data = []
        out_column_type = []
        cnux__kjupx = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for exlsg__gim, f_val in zip(wjx__qag, clyfx__etle):
            if isinstance(f_val, (tuple, list)):
                uunql__dyzbh = 0
                for xrb__isg in f_val:
                    olrm__nfrqh, out_tp = get_agg_funcname_and_outtyp(grp,
                        exlsg__gim, xrb__isg, typing_context,
                        target_context, raise_on_any_error)
                    vjn__iunqz = olrm__nfrqh in list_cumulative
                    if olrm__nfrqh == '<lambda>' and len(f_val) > 1:
                        olrm__nfrqh = '<lambda_' + str(uunql__dyzbh) + '>'
                        uunql__dyzbh += 1
                    out_columns.append((exlsg__gim, olrm__nfrqh))
                    otxth__ppjqu[exlsg__gim, olrm__nfrqh
                        ] = exlsg__gim, olrm__nfrqh
                    _append_out_type(grp, out_data, out_tp)
            else:
                olrm__nfrqh, out_tp = get_agg_funcname_and_outtyp(grp,
                    exlsg__gim, f_val, typing_context, target_context,
                    raise_on_any_error)
                vjn__iunqz = olrm__nfrqh in list_cumulative
                if multi_level_names:
                    out_columns.append((exlsg__gim, olrm__nfrqh))
                    otxth__ppjqu[exlsg__gim, olrm__nfrqh
                        ] = exlsg__gim, olrm__nfrqh
                elif not ayzg__uits:
                    out_columns.append(exlsg__gim)
                    otxth__ppjqu[exlsg__gim, olrm__nfrqh] = exlsg__gim
                elif ayzg__uits:
                    cnux__kjupx.append(olrm__nfrqh)
                _append_out_type(grp, out_data, out_tp)
        if ayzg__uits:
            for behml__did, phzu__pahbw in enumerate(kws.keys()):
                out_columns.append(phzu__pahbw)
                otxth__ppjqu[wjx__qag[behml__did], cnux__kjupx[behml__did]
                    ] = phzu__pahbw
        if vjn__iunqz:
            index = grp.df_type.index
        else:
            index = out_tp.index
        zck__ohbbw = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(zck__ohbbw, *args), otxth__ppjqu
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            utrja__bfbwq = get_overload_const_list(func)
        else:
            utrja__bfbwq = func.types
        if len(utrja__bfbwq) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        uunql__dyzbh = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        otxth__ppjqu = {}
        qxejg__mnc = grp.selection[0]
        for f_val in utrja__bfbwq:
            olrm__nfrqh, out_tp = get_agg_funcname_and_outtyp(grp,
                qxejg__mnc, f_val, typing_context, target_context,
                raise_on_any_error)
            vjn__iunqz = olrm__nfrqh in list_cumulative
            if olrm__nfrqh == '<lambda>' and len(utrja__bfbwq) > 1:
                olrm__nfrqh = '<lambda_' + str(uunql__dyzbh) + '>'
                uunql__dyzbh += 1
            out_columns.append(olrm__nfrqh)
            otxth__ppjqu[qxejg__mnc, olrm__nfrqh] = olrm__nfrqh
            _append_out_type(grp, out_data, out_tp)
        if vjn__iunqz:
            index = grp.df_type.index
        else:
            index = out_tp.index
        zck__ohbbw = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(zck__ohbbw, *args), otxth__ppjqu
    olrm__nfrqh = ''
    if types.unliteral(func) == types.unicode_type:
        olrm__nfrqh = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        olrm__nfrqh = bodo.utils.typing.get_builtin_function_name(func)
    if olrm__nfrqh:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, olrm__nfrqh, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = to_numeric_index_if_range_index(grp.df_type.index)
    if isinstance(index, MultiIndexType):
        raise_bodo_error(
            f'Groupby.{name_operation}: MultiIndex input not supported for groupby operations that use input Index'
            )
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        zmilc__fep = args[0] if len(args) > 0 else kws.pop('axis', 0)
        jrs__ixnoa = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        xgbvv__vxns = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        lkbio__riib = dict(axis=zmilc__fep, numeric_only=jrs__ixnoa)
        osmbd__dmqc = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', lkbio__riib,
            osmbd__dmqc, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        eptv__yag = args[0] if len(args) > 0 else kws.pop('periods', 1)
        grdo__uiib = args[1] if len(args) > 1 else kws.pop('freq', None)
        zmilc__fep = args[2] if len(args) > 2 else kws.pop('axis', 0)
        wqnr__zrk = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        lkbio__riib = dict(freq=grdo__uiib, axis=zmilc__fep, fill_value=
            wqnr__zrk)
        osmbd__dmqc = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', lkbio__riib,
            osmbd__dmqc, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        rcd__erf = args[0] if len(args) > 0 else kws.pop('func', None)
        xklxj__przcq = kws.pop('engine', None)
        qnuia__cdfhz = kws.pop('engine_kwargs', None)
        lkbio__riib = dict(engine=xklxj__przcq, engine_kwargs=qnuia__cdfhz)
        osmbd__dmqc = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', lkbio__riib,
            osmbd__dmqc, package_name='pandas', module_name='GroupBy')
    otxth__ppjqu = {}
    for sqzy__ldbvv in grp.selection:
        out_columns.append(sqzy__ldbvv)
        otxth__ppjqu[sqzy__ldbvv, name_operation] = sqzy__ldbvv
        kftwl__oae = grp.df_type.column_index[sqzy__ldbvv]
        data = grp.df_type.data[kftwl__oae]
        dhmip__lcjm = (name_operation if name_operation != 'transform' else
            get_literal_value(rcd__erf))
        if dhmip__lcjm in ('sum', 'cumsum'):
            data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            woa__fer, err_msg = get_groupby_output_dtype(data,
                get_literal_value(rcd__erf), grp.df_type.index)
            if err_msg == 'ok':
                data = woa__fer
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    zck__ohbbw = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        zck__ohbbw = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(zck__ohbbw, *args), otxth__ppjqu


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.ngroup', no_unliteral=True)
    def resolve_ngroup(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'ngroup', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        dolc__knamw = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        bkgx__hdsx = isinstance(dolc__knamw, (SeriesType,
            HeterogeneousSeriesType)
            ) and dolc__knamw.const_info is not None or not isinstance(
            dolc__knamw, (SeriesType, DataFrameType))
        if bkgx__hdsx:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                suv__mko = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                qvjsf__zpx = tuple(grp.df_type.column_index[grp.keys[
                    behml__did]] for behml__did in range(len(grp.keys)))
                yclie__jgc = tuple(grp.df_type.data[kftwl__oae] for
                    kftwl__oae in qvjsf__zpx)
                suv__mko = MultiIndexType(yclie__jgc, tuple(types.literal(
                    zjj__rxgfa) for zjj__rxgfa in grp.keys))
            else:
                kftwl__oae = grp.df_type.column_index[grp.keys[0]]
                uwv__zcx = grp.df_type.data[kftwl__oae]
                suv__mko = bodo.hiframes.pd_index_ext.array_type_to_index(
                    uwv__zcx, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            sro__zsu = tuple(grp.df_type.data[grp.df_type.column_index[
                sqzy__ldbvv]] for sqzy__ldbvv in grp.keys)
            ewqp__rhi = tuple(types.literal(lkjms__jdz) for lkjms__jdz in
                grp.keys) + get_index_name_types(dolc__knamw.index)
            if not grp.as_index:
                sro__zsu = types.Array(types.int64, 1, 'C'),
                ewqp__rhi = (types.none,) + get_index_name_types(dolc__knamw
                    .index)
            suv__mko = MultiIndexType(sro__zsu + get_index_data_arr_types(
                dolc__knamw.index), ewqp__rhi)
        if bkgx__hdsx:
            if isinstance(dolc__knamw, HeterogeneousSeriesType):
                xgnnu__ddpg, ndw__gmowk = dolc__knamw.const_info
                if isinstance(dolc__knamw.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    jrhsp__vzd = dolc__knamw.data.tuple_typ.types
                elif isinstance(dolc__knamw.data, types.Tuple):
                    jrhsp__vzd = dolc__knamw.data.types
                tzt__sfzix = tuple(to_nullable_type(dtype_to_array_type(
                    qapc__iwca)) for qapc__iwca in jrhsp__vzd)
                ksxnn__cwfdy = DataFrameType(out_data + tzt__sfzix,
                    suv__mko, out_columns + ndw__gmowk)
            elif isinstance(dolc__knamw, SeriesType):
                vzyi__vwqi, ndw__gmowk = dolc__knamw.const_info
                tzt__sfzix = tuple(to_nullable_type(dtype_to_array_type(
                    dolc__knamw.dtype)) for xgnnu__ddpg in range(vzyi__vwqi))
                ksxnn__cwfdy = DataFrameType(out_data + tzt__sfzix,
                    suv__mko, out_columns + ndw__gmowk)
            else:
                zajkc__pyadb = get_udf_out_arr_type(dolc__knamw)
                if not grp.as_index:
                    ksxnn__cwfdy = DataFrameType(out_data + (zajkc__pyadb,),
                        suv__mko, out_columns + ('',))
                else:
                    ksxnn__cwfdy = SeriesType(zajkc__pyadb.dtype,
                        zajkc__pyadb, suv__mko, None)
        elif isinstance(dolc__knamw, SeriesType):
            ksxnn__cwfdy = SeriesType(dolc__knamw.dtype, dolc__knamw.data,
                suv__mko, dolc__knamw.name_typ)
        else:
            ksxnn__cwfdy = DataFrameType(dolc__knamw.data, suv__mko,
                dolc__knamw.columns)
        jgu__npny = gen_apply_pysig(len(f_args), kws.keys())
        rwrn__etva = (func, *f_args) + tuple(kws.values())
        return signature(ksxnn__cwfdy, *rwrn__etva).replace(pysig=jgu__npny)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True, _num_shuffle_keys=
            grpby._num_shuffle_keys)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    vptq__vmwy = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            exlsg__gim = grp.selection[0]
            zajkc__pyadb = vptq__vmwy.data[vptq__vmwy.column_index[exlsg__gim]]
            xmr__buziv = SeriesType(zajkc__pyadb.dtype, zajkc__pyadb,
                vptq__vmwy.index, types.literal(exlsg__gim))
        else:
            tgg__pvaik = tuple(vptq__vmwy.data[vptq__vmwy.column_index[
                sqzy__ldbvv]] for sqzy__ldbvv in grp.selection)
            xmr__buziv = DataFrameType(tgg__pvaik, vptq__vmwy.index, tuple(
                grp.selection))
    else:
        xmr__buziv = vptq__vmwy
    fbdi__tebm = xmr__buziv,
    fbdi__tebm += tuple(f_args)
    try:
        dolc__knamw = get_const_func_output_type(func, fbdi__tebm, kws,
            typing_context, target_context)
    except Exception as faj__qemq:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', faj__qemq),
            getattr(faj__qemq, 'loc', None))
    return dolc__knamw


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    fbdi__tebm = (grp,) + f_args
    try:
        dolc__knamw = get_const_func_output_type(func, fbdi__tebm, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as faj__qemq:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', faj__qemq),
            getattr(faj__qemq, 'loc', None))
    jgu__npny = gen_apply_pysig(len(f_args), kws.keys())
    rwrn__etva = (func, *f_args) + tuple(kws.values())
    return signature(dolc__knamw, *rwrn__etva).replace(pysig=jgu__npny)


def gen_apply_pysig(n_args, kws):
    khvcf__pzz = ', '.join(f'arg{behml__did}' for behml__did in range(n_args))
    khvcf__pzz = khvcf__pzz + ', ' if khvcf__pzz else ''
    xjl__bire = ', '.join(f"{yddot__xcez} = ''" for yddot__xcez in kws)
    xvnw__hga = f'def apply_stub(func, {khvcf__pzz}{xjl__bire}):\n'
    xvnw__hga += '    pass\n'
    krwr__aib = {}
    exec(xvnw__hga, {}, krwr__aib)
    wod__hobid = krwr__aib['apply_stub']
    return numba.core.utils.pysignature(wod__hobid)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        eadnm__wozg = types.Array(types.int64, 1, 'C')
        bbljp__gmvr = _pivot_values.meta
        crdjc__saiw = len(bbljp__gmvr)
        akrjn__ljyxy = bodo.hiframes.pd_index_ext.array_type_to_index(index
            .data, types.StringLiteral('index'))
        swdxd__hrov = DataFrameType((eadnm__wozg,) * crdjc__saiw,
            akrjn__ljyxy, tuple(bbljp__gmvr))
        return signature(swdxd__hrov, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    xvnw__hga = 'def impl(keys, dropna, _is_parallel):\n'
    xvnw__hga += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    xvnw__hga += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{behml__did}])' for behml__did in range(len(
        keys.types))))
    xvnw__hga += '    table = arr_info_list_to_table(info_list)\n'
    xvnw__hga += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    xvnw__hga += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    xvnw__hga += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    xvnw__hga += '    delete_table_decref_arrays(table)\n'
    xvnw__hga += '    ev.finalize()\n'
    xvnw__hga += '    return sort_idx, group_labels, ngroups\n'
    krwr__aib = {}
    exec(xvnw__hga, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, krwr__aib)
    ypvu__txvg = krwr__aib['impl']
    return ypvu__txvg


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    opso__iqf = len(labels)
    cah__ecq = np.zeros(ngroups, dtype=np.int64)
    bssij__kbo = np.zeros(ngroups, dtype=np.int64)
    hggrk__egdro = 0
    hhl__jzy = 0
    for behml__did in range(opso__iqf):
        reh__cmb = labels[behml__did]
        if reh__cmb < 0:
            hggrk__egdro += 1
        else:
            hhl__jzy += 1
            if behml__did == opso__iqf - 1 or reh__cmb != labels[behml__did + 1
                ]:
                cah__ecq[reh__cmb] = hggrk__egdro
                bssij__kbo[reh__cmb] = hggrk__egdro + hhl__jzy
                hggrk__egdro += hhl__jzy
                hhl__jzy = 0
    return cah__ecq, bssij__kbo


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ypvu__txvg, xgnnu__ddpg = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ypvu__txvg


def gen_shuffle_dataframe(df, keys, _is_parallel):
    vzyi__vwqi = len(df.columns)
    zta__riz = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    xvnw__hga = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        xvnw__hga += '  return df, keys, get_null_shuffle_info()\n'
        krwr__aib = {}
        exec(xvnw__hga, {'get_null_shuffle_info': get_null_shuffle_info},
            krwr__aib)
        ypvu__txvg = krwr__aib['impl']
        return ypvu__txvg
    for behml__did in range(vzyi__vwqi):
        xvnw__hga += f"""  in_arr{behml__did} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {behml__did})
"""
    xvnw__hga += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    xvnw__hga += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{behml__did}])' for behml__did in range(
        zta__riz)), ', '.join(f'array_to_info(in_arr{behml__did})' for
        behml__did in range(vzyi__vwqi)), 'array_to_info(in_index_arr)')
    xvnw__hga += '  table = arr_info_list_to_table(info_list)\n'
    xvnw__hga += (
        f'  out_table = shuffle_table(table, {zta__riz}, _is_parallel, 1)\n')
    for behml__did in range(zta__riz):
        xvnw__hga += f"""  out_key{behml__did} = info_to_array(info_from_table(out_table, {behml__did}), keys{behml__did}_typ)
"""
    for behml__did in range(vzyi__vwqi):
        xvnw__hga += f"""  out_arr{behml__did} = info_to_array(info_from_table(out_table, {behml__did + zta__riz}), in_arr{behml__did}_typ)
"""
    xvnw__hga += f"""  out_arr_index = info_to_array(info_from_table(out_table, {zta__riz + vzyi__vwqi}), ind_arr_typ)
"""
    xvnw__hga += '  shuffle_info = get_shuffle_info(out_table)\n'
    xvnw__hga += '  delete_table(out_table)\n'
    xvnw__hga += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{behml__did}' for behml__did in range(
        vzyi__vwqi))
    xvnw__hga += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    xvnw__hga += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    xvnw__hga += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{behml__did}' for behml__did in range(zta__riz)))
    zuzu__jpdn = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    zuzu__jpdn.update({f'keys{behml__did}_typ': keys.types[behml__did] for
        behml__did in range(zta__riz)})
    zuzu__jpdn.update({f'in_arr{behml__did}_typ': df.data[behml__did] for
        behml__did in range(vzyi__vwqi)})
    krwr__aib = {}
    exec(xvnw__hga, zuzu__jpdn, krwr__aib)
    ypvu__txvg = krwr__aib['impl']
    return ypvu__txvg, zuzu__jpdn


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        mrt__eloxl = len(data.array_types)
        xvnw__hga = 'def impl(data, shuffle_info):\n'
        xvnw__hga += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{behml__did}])' for behml__did in
            range(mrt__eloxl)))
        xvnw__hga += '  table = arr_info_list_to_table(info_list)\n'
        xvnw__hga += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for behml__did in range(mrt__eloxl):
            xvnw__hga += f"""  out_arr{behml__did} = info_to_array(info_from_table(out_table, {behml__did}), data._data[{behml__did}])
"""
        xvnw__hga += '  delete_table(out_table)\n'
        xvnw__hga += '  delete_table(table)\n'
        xvnw__hga += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{behml__did}' for behml__did in range
            (mrt__eloxl))))
        krwr__aib = {}
        exec(xvnw__hga, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, krwr__aib)
        ypvu__txvg = krwr__aib['impl']
        return ypvu__txvg
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            yxc__wpfcs = bodo.utils.conversion.index_to_array(data)
            gid__upr = reverse_shuffle(yxc__wpfcs, shuffle_info)
            return bodo.utils.conversion.index_from_array(gid__upr)
        return impl_index

    def impl_arr(data, shuffle_info):
        eiu__jzbx = [array_to_info(data)]
        ehlij__fvsx = arr_info_list_to_table(eiu__jzbx)
        qqd__bzl = reverse_shuffle_table(ehlij__fvsx, shuffle_info)
        gid__upr = info_to_array(info_from_table(qqd__bzl, 0), data)
        delete_table(qqd__bzl)
        delete_table(ehlij__fvsx)
        return gid__upr
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    lkbio__riib = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    osmbd__dmqc = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', lkbio__riib, osmbd__dmqc,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    awp__esbq = get_overload_const_bool(ascending)
    pied__edi = grp.selection[0]
    xvnw__hga = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    ssu__mlyq = (
        f"lambda S: S.value_counts(ascending={awp__esbq}, _index_name='{pied__edi}')"
        )
    xvnw__hga += f'    return grp.apply({ssu__mlyq})\n'
    krwr__aib = {}
    exec(xvnw__hga, {'bodo': bodo}, krwr__aib)
    ypvu__txvg = krwr__aib['impl']
    return ypvu__txvg


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill', 'nth',
    'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail', 'corr', 'cov',
    'describe', 'diff', 'fillna', 'filter', 'hist', 'mad', 'plot',
    'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for bca__yuooh in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, bca__yuooh, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{bca__yuooh}'))
    for bca__yuooh in groupby_unsupported:
        overload_method(DataFrameGroupByType, bca__yuooh, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{bca__yuooh}'))
    for bca__yuooh in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, bca__yuooh, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{bca__yuooh}'))
    for bca__yuooh in series_only_unsupported:
        overload_method(DataFrameGroupByType, bca__yuooh, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{bca__yuooh}'))
    for bca__yuooh in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, bca__yuooh, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{bca__yuooh}'))


_install_groupby_unsupported()
