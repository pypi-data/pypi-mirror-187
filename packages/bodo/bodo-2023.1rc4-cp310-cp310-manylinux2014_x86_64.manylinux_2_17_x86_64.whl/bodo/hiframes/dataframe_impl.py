"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_castable_arr_dtype, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        izob__vrj = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({izob__vrj})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    ygby__ohho = 'def impl(df):\n'
    if df.has_runtime_cols:
        ygby__ohho += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        ayggx__kitfo = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        ygby__ohho += f'  return {ayggx__kitfo}'
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    jusf__rad = len(df.columns)
    ajj__uvey = set(i for i in range(jusf__rad) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in ajj__uvey else '') for i in
        range(jusf__rad))
    ygby__ohho = 'def f(df):\n'.format()
    ygby__ohho += '    return np.stack(({},), 1)\n'.format(data_args)
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'np': np}, cghh__zimi)
    damnq__obocq = cghh__zimi['f']
    return damnq__obocq


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    vpllq__drewi = {'dtype': dtype, 'na_value': na_value}
    jqhn__sncv = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            kjwj__kpyls = bodo.hiframes.table.compute_num_runtime_columns(t)
            return kjwj__kpyls * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            kjwj__kpyls = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), kjwj__kpyls
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), ncols)


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    ygby__ohho = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    sne__zngg = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    ygby__ohho += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{sne__zngg}), {index}, None)
"""
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if type(dtype) in bodo.libs.int_arr_ext.pd_int_dtype_classes:
        return dtype.name
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    vpllq__drewi = {'errors': errors}
    jqhn__sncv = {'errors': 'raise'}
    check_unsupported_args('df.astype', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    if not is_overload_bool(copy):
        raise BodoError("DataFrame.astype(): 'copy' must be a boolean value")
    extra_globals = None
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    if df.is_table_format:
        extra_globals = {}
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        hcl__hpjx = []
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        wgcgy__scvt = _bodo_object_typeref.instance_type
        assert isinstance(wgcgy__scvt, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        if df.is_table_format:
            for i, name in enumerate(df.columns):
                if name in wgcgy__scvt.column_index:
                    idx = wgcgy__scvt.column_index[name]
                    arr_typ = wgcgy__scvt.data[idx]
                else:
                    arr_typ = df.data[i]
                hcl__hpjx.append(arr_typ)
        else:
            extra_globals = {}
            fwbun__fua = {}
            for i, name in enumerate(wgcgy__scvt.columns):
                arr_typ = wgcgy__scvt.data[i]
                extra_globals[f'_bodo_schema{i}'] = get_castable_arr_dtype(
                    arr_typ)
                fwbun__fua[name] = f'_bodo_schema{i}'
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {fwbun__fua[nsg__dhub]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if nsg__dhub in fwbun__fua else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, nsg__dhub in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        dlbvm__rsh = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        if df.is_table_format:
            dlbvm__rsh = {name: dtype_to_array_type(parse_dtype(dtype)) for
                name, dtype in dlbvm__rsh.items()}
            for i, name in enumerate(df.columns):
                if name in dlbvm__rsh:
                    arr_typ = dlbvm__rsh[name]
                else:
                    arr_typ = df.data[i]
                hcl__hpjx.append(arr_typ)
        else:
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(dlbvm__rsh[nsg__dhub])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if nsg__dhub in dlbvm__rsh else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, nsg__dhub in enumerate(df.columns))
    elif df.is_table_format:
        arr_typ = dtype_to_array_type(parse_dtype(dtype))
        hcl__hpjx = [arr_typ] * len(df.columns)
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    if df.is_table_format:
        fygy__mygk = bodo.TableType(tuple(hcl__hpjx))
        extra_globals['out_table_typ'] = fygy__mygk
        data_args = (
            'bodo.utils.table_utils.table_astype(table, out_table_typ, copy, _bodo_nan_to_str)'
            )
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    header = 'def impl(df, deep=True):\n'
    extra_globals = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        ixap__vxjxt = types.none
        extra_globals = {'output_arr_typ': ixap__vxjxt}
        if is_overload_false(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if deep else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        xkdrs__owof = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                xkdrs__owof.append(arr + '.copy()')
            elif is_overload_false(deep):
                xkdrs__owof.append(arr)
            else:
                xkdrs__owof.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(xkdrs__owof)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    vpllq__drewi = {'index': index, 'level': level, 'errors': errors}
    jqhn__sncv = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        uslfx__ozjst = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        uslfx__ozjst = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    coycl__lcco = tuple([uslfx__ozjst.get(df.columns[i], df.columns[i]) for
        i in range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    bppm__ygyr = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        bppm__ygyr = df.copy(columns=coycl__lcco)
        ixap__vxjxt = types.none
        extra_globals = {'output_arr_typ': ixap__vxjxt}
        if is_overload_false(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if copy else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        xkdrs__owof = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                xkdrs__owof.append(arr + '.copy()')
            elif is_overload_false(copy):
                xkdrs__owof.append(arr)
            else:
                xkdrs__owof.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(xkdrs__owof)
    return _gen_init_df(header, coycl__lcco, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    oxogg__piu = not is_overload_none(items)
    zkeq__djpdw = not is_overload_none(like)
    awl__nzn = not is_overload_none(regex)
    lpwe__wek = oxogg__piu ^ zkeq__djpdw ^ awl__nzn
    dfvp__zkyb = not (oxogg__piu or zkeq__djpdw or awl__nzn)
    if dfvp__zkyb:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not lpwe__wek:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        lylr__qol = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        lylr__qol = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert lylr__qol in {0, 1}
    ygby__ohho = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if lylr__qol == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if lylr__qol == 1:
        fav__eol = []
        ckb__fuyq = []
        rzeg__eay = []
        if oxogg__piu:
            if is_overload_constant_list(items):
                hgd__czvz = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if zkeq__djpdw:
            if is_overload_constant_str(like):
                kli__nrarx = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if awl__nzn:
            if is_overload_constant_str(regex):
                gbxlq__pez = get_overload_const_str(regex)
                fsfv__jdoq = re.compile(gbxlq__pez)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, nsg__dhub in enumerate(df.columns):
            if not is_overload_none(items
                ) and nsg__dhub in hgd__czvz or not is_overload_none(like
                ) and kli__nrarx in str(nsg__dhub) or not is_overload_none(
                regex) and fsfv__jdoq.search(str(nsg__dhub)):
                ckb__fuyq.append(nsg__dhub)
                rzeg__eay.append(i)
        for i in rzeg__eay:
            var_name = f'data_{i}'
            fav__eol.append(var_name)
            ygby__ohho += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(fav__eol)
        return _gen_init_df(ygby__ohho, ckb__fuyq, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    bppm__ygyr = None
    if df.is_table_format:
        ixap__vxjxt = types.Array(types.bool_, 1, 'C')
        bppm__ygyr = DataFrameType(tuple([ixap__vxjxt] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ixap__vxjxt}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    ziqg__eqh = is_overload_none(include)
    wzb__iph = is_overload_none(exclude)
    ntyr__qbzl = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if ziqg__eqh and wzb__iph:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not ziqg__eqh:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            kpmc__bwm = [dtype_to_array_type(parse_dtype(elem, ntyr__qbzl)) for
                elem in include]
        elif is_legal_input(include):
            kpmc__bwm = [dtype_to_array_type(parse_dtype(include, ntyr__qbzl))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        kpmc__bwm = get_nullable_and_non_nullable_types(kpmc__bwm)
        vah__fzg = tuple(nsg__dhub for i, nsg__dhub in enumerate(df.columns
            ) if df.data[i] in kpmc__bwm)
    else:
        vah__fzg = df.columns
    if not wzb__iph:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            wsh__jey = [dtype_to_array_type(parse_dtype(elem, ntyr__qbzl)) for
                elem in exclude]
        elif is_legal_input(exclude):
            wsh__jey = [dtype_to_array_type(parse_dtype(exclude, ntyr__qbzl))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        wsh__jey = get_nullable_and_non_nullable_types(wsh__jey)
        vah__fzg = tuple(nsg__dhub for nsg__dhub in vah__fzg if df.data[df.
            column_index[nsg__dhub]] not in wsh__jey)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[nsg__dhub]})'
         for nsg__dhub in vah__fzg)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, vah__fzg, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    bppm__ygyr = None
    if df.is_table_format:
        ixap__vxjxt = types.Array(types.bool_, 1, 'C')
        bppm__ygyr = DataFrameType(tuple([ixap__vxjxt] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ixap__vxjxt}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


def overload_dataframe_head(df, n=5):
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[:n]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[m:]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    drcl__tld = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in drcl__tld:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    drcl__tld = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in drcl__tld:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    ygby__ohho = 'def impl(df, values):\n'
    xtk__ameip = {}
    uxhd__tlcp = False
    if isinstance(values, DataFrameType):
        uxhd__tlcp = True
        for i, nsg__dhub in enumerate(df.columns):
            if nsg__dhub in values.column_index:
                xcn__vio = 'val{}'.format(i)
                ygby__ohho += f"""  {xcn__vio} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[nsg__dhub]})
"""
                xtk__ameip[nsg__dhub] = xcn__vio
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        xtk__ameip = {nsg__dhub: 'values' for nsg__dhub in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        xcn__vio = 'data{}'.format(i)
        ygby__ohho += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(xcn__vio, i))
        data.append(xcn__vio)
    dqelx__vhn = ['out{}'.format(i) for i in range(len(df.columns))]
    qpg__xgrg = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    uyl__svda = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    iqc__eeos = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, stu__qca) in enumerate(zip(df.columns, data)):
        if cname in xtk__ameip:
            tcgm__cye = xtk__ameip[cname]
            if uxhd__tlcp:
                ygby__ohho += qpg__xgrg.format(stu__qca, tcgm__cye,
                    dqelx__vhn[i])
            else:
                ygby__ohho += uyl__svda.format(stu__qca, tcgm__cye,
                    dqelx__vhn[i])
        else:
            ygby__ohho += iqc__eeos.format(dqelx__vhn[i])
    return _gen_init_df(ygby__ohho, df.columns, ','.join(dqelx__vhn))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    jusf__rad = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(jusf__rad))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    wwuox__auv = [nsg__dhub for nsg__dhub, vckqe__wyx in zip(df.columns, df
        .data) if bodo.utils.typing._is_pandas_numeric_dtype(vckqe__wyx.dtype)]
    assert len(wwuox__auv) != 0
    qtv__tfia = ''
    if not any(vckqe__wyx == types.float64 for vckqe__wyx in df.data):
        qtv__tfia = '.astype(np.float64)'
    gchfa__vno = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nsg__dhub], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[nsg__dhub]], IntegerArrayType) or
        df.data[df.column_index[nsg__dhub]] == boolean_array else '') for
        nsg__dhub in wwuox__auv)
    ypu__scu = 'np.stack(({},), 1){}'.format(gchfa__vno, qtv__tfia)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(wwuox__auv))
        )
    index = f'{generate_col_to_index_func_text(wwuox__auv)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(ypu__scu)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, wwuox__auv, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    hufbv__twj = dict(ddof=ddof)
    odmlh__pek = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    jyru__jisxa = '1' if is_overload_none(min_periods) else 'min_periods'
    wwuox__auv = [nsg__dhub for nsg__dhub, vckqe__wyx in zip(df.columns, df
        .data) if bodo.utils.typing._is_pandas_numeric_dtype(vckqe__wyx.dtype)]
    if len(wwuox__auv) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    qtv__tfia = ''
    if not any(vckqe__wyx == types.float64 for vckqe__wyx in df.data):
        qtv__tfia = '.astype(np.float64)'
    gchfa__vno = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nsg__dhub], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[nsg__dhub]], IntegerArrayType) or
        df.data[df.column_index[nsg__dhub]] == boolean_array else '') for
        nsg__dhub in wwuox__auv)
    ypu__scu = 'np.stack(({},), 1){}'.format(gchfa__vno, qtv__tfia)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(wwuox__auv))
        )
    index = f'pd.Index({wwuox__auv})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(ypu__scu)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        jyru__jisxa)
    return _gen_init_df(header, wwuox__auv, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    hufbv__twj = dict(axis=axis, level=level, numeric_only=numeric_only)
    odmlh__pek = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    ygby__ohho = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    ygby__ohho += '  data = np.array([{}])\n'.format(data_args)
    ayggx__kitfo = (bodo.hiframes.dataframe_impl.
        generate_col_to_index_func_text(df.columns))
    ygby__ohho += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ayggx__kitfo})\n'
        )
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'np': np}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    hufbv__twj = dict(axis=axis)
    odmlh__pek = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    ygby__ohho = 'def impl(df, axis=0, dropna=True):\n'
    ygby__ohho += '  data = np.asarray(({},))\n'.format(data_args)
    ayggx__kitfo = (bodo.hiframes.dataframe_impl.
        generate_col_to_index_func_text(df.columns))
    ygby__ohho += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ayggx__kitfo})\n'
        )
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'np': np}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    hufbv__twj = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    odmlh__pek = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    hufbv__twj = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    odmlh__pek = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    hufbv__twj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    odmlh__pek = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    hufbv__twj = dict(numeric_only=numeric_only, interpolation=interpolation)
    odmlh__pek = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    hufbv__twj = dict(axis=axis, skipna=skipna)
    odmlh__pek = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for gvym__koyu in df.data:
        if not (bodo.utils.utils.is_np_array_typ(gvym__koyu) and (
            gvym__koyu.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(gvym__koyu.dtype, (types.Number, types.Boolean))) or
            isinstance(gvym__koyu, (bodo.IntegerArrayType, bodo.
            FloatingArrayType, bodo.CategoricalArrayType)) or gvym__koyu in
            [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {gvym__koyu} not supported.'
                )
        if isinstance(gvym__koyu, bodo.CategoricalArrayType
            ) and not gvym__koyu.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    hufbv__twj = dict(axis=axis, skipna=skipna)
    odmlh__pek = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for gvym__koyu in df.data:
        if not (bodo.utils.utils.is_np_array_typ(gvym__koyu) and (
            gvym__koyu.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(gvym__koyu.dtype, (types.Number, types.Boolean))) or
            isinstance(gvym__koyu, (bodo.IntegerArrayType, bodo.
            FloatingArrayType, bodo.CategoricalArrayType)) or gvym__koyu in
            [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {gvym__koyu} not supported.'
                )
        if isinstance(gvym__koyu, bodo.CategoricalArrayType
            ) and not gvym__koyu.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        wwuox__auv = tuple(nsg__dhub for nsg__dhub, vckqe__wyx in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (vckqe__wyx.dtype))
        out_colnames = wwuox__auv
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            vlv__daq = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[nsg__dhub]].dtype) for nsg__dhub in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(vlv__daq, []))
    except NotImplementedError as eytd__qjim:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    myuyw__fkgha = ''
    if func_name in ('sum', 'prod'):
        myuyw__fkgha = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    ygby__ohho = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, myuyw__fkgha))
    if func_name == 'quantile':
        ygby__ohho = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        ygby__ohho = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        ygby__ohho += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        ygby__ohho += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    xgtj__wpuqs = ''
    if func_name in ('min', 'max'):
        xgtj__wpuqs = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        xgtj__wpuqs = ', dtype=np.float32'
    pfdn__fvy = f'bodo.libs.array_ops.array_op_{func_name}'
    abd__kqc = ''
    if func_name in ['sum', 'prod']:
        abd__kqc = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        abd__kqc = 'index'
    elif func_name == 'quantile':
        abd__kqc = 'q'
    elif func_name in ['std', 'var']:
        abd__kqc = 'True, ddof'
    elif func_name == 'median':
        abd__kqc = 'True'
    data_args = ', '.join(
        f'{pfdn__fvy}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[nsg__dhub]}), {abd__kqc})'
         for nsg__dhub in out_colnames)
    ygby__ohho = ''
    if func_name in ('idxmax', 'idxmin'):
        ygby__ohho += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        ygby__ohho += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        ygby__ohho += '  data = np.asarray(({},){})\n'.format(data_args,
            xgtj__wpuqs)
    ygby__ohho += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return ygby__ohho


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    phws__pgr = [df_type.column_index[nsg__dhub] for nsg__dhub in out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in phws__pgr)
    izwk__yyko = '\n        '.join(f'row[{i}] = arr_{phws__pgr[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    sfojw__ddw = f'len(arr_{phws__pgr[0]})'
    fumij__iprjz = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in fumij__iprjz:
        ivab__hfe = fumij__iprjz[func_name]
        dveh__geozw = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        ygby__ohho = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {sfojw__ddw}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{dveh__geozw})
    for i in numba.parfors.parfor.internal_prange(n):
        {izwk__yyko}
        A[i] = {ivab__hfe}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return ygby__ohho
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    hufbv__twj = dict(fill_method=fill_method, limit=limit, freq=freq)
    odmlh__pek = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    hufbv__twj = dict(axis=axis, skipna=skipna)
    odmlh__pek = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    hufbv__twj = dict(skipna=skipna)
    odmlh__pek = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, (IntegerArrayType, FloatingArrayType)
        ) or isinstance(data, types.Array) and isinstance(data.dtype, types
        .Number) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    hufbv__twj = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    odmlh__pek = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    wwuox__auv = [nsg__dhub for nsg__dhub, vckqe__wyx in zip(df.columns, df
        .data) if _is_describe_type(vckqe__wyx)]
    if len(wwuox__auv) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    elc__avhv = sum(df.data[df.column_index[nsg__dhub]].dtype == bodo.
        datetime64ns for nsg__dhub in wwuox__auv)

    def _get_describe(col_ind):
        luwb__xch = df.data[col_ind].dtype == bodo.datetime64ns
        if elc__avhv and elc__avhv != len(wwuox__auv):
            if luwb__xch:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for nsg__dhub in wwuox__auv:
        col_ind = df.column_index[nsg__dhub]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[nsg__dhub]) for
        nsg__dhub in wwuox__auv)
    opg__orb = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if elc__avhv == len(wwuox__auv):
        opg__orb = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif elc__avhv:
        opg__orb = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({opg__orb})'
    return _gen_init_df(header, wwuox__auv, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    hufbv__twj = dict(axis=axis, convert=convert, is_copy=is_copy)
    odmlh__pek = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    hufbv__twj = dict(freq=freq, axis=axis)
    odmlh__pek = dict(freq=None, axis=0)
    check_unsupported_args('DataFrame.shift', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for sdrni__can in df.data:
        if not is_supported_shift_array_type(sdrni__can):
            raise BodoError(
                f'Dataframe.shift() column input type {sdrni__can.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False, fill_value)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    hufbv__twj = dict(axis=axis)
    odmlh__pek = dict(axis=0)
    check_unsupported_args('DataFrame.diff', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for sdrni__can in df.data:
        if not (isinstance(sdrni__can, types.Array) and (isinstance(
            sdrni__can.dtype, types.Number) or sdrni__can.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {sdrni__can.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    oyu__rzzn = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(oyu__rzzn)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        sfu__eyk = get_overload_const_list(column)
    else:
        sfu__eyk = [get_literal_value(column)]
    zrqmd__lpe = [df.column_index[nsg__dhub] for nsg__dhub in sfu__eyk]
    for i in zrqmd__lpe:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{zrqmd__lpe[0]})\n'
        )
    for i in range(n):
        if i in zrqmd__lpe:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    vpllq__drewi = {'inplace': inplace, 'append': append,
        'verify_integrity': verify_integrity}
    jqhn__sncv = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(nsg__dhub for nsg__dhub in df.columns if nsg__dhub !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    vpllq__drewi = {'inplace': inplace}
    jqhn__sncv = {'inplace': False}
    check_unsupported_args('query', vpllq__drewi, jqhn__sncv, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        blc__ivpas = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[blc__ivpas]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    vpllq__drewi = {'subset': subset, 'keep': keep}
    jqhn__sncv = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    jusf__rad = len(df.columns)
    ygby__ohho = "def impl(df, subset=None, keep='first'):\n"
    for i in range(jusf__rad):
        ygby__ohho += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    tpb__cjj = ', '.join(f'data_{i}' for i in range(jusf__rad))
    tpb__cjj += ',' if jusf__rad == 1 else ''
    ygby__ohho += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({tpb__cjj}))\n')
    ygby__ohho += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    ygby__ohho += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    vpllq__drewi = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    jqhn__sncv = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    crok__tuwl = []
    if is_overload_constant_list(subset):
        crok__tuwl = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        crok__tuwl = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        crok__tuwl = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    olb__fbxg = []
    for col_name in crok__tuwl:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        olb__fbxg.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', vpllq__drewi,
        jqhn__sncv, package_name='pandas', module_name='DataFrame')
    ukc__tho = []
    if olb__fbxg:
        for nvi__jltz in olb__fbxg:
            if isinstance(df.data[nvi__jltz], bodo.MapArrayType):
                ukc__tho.append(df.columns[nvi__jltz])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                ukc__tho.append(col_name)
    if ukc__tho:
        raise BodoError(f'DataFrame.drop_duplicates(): Columns {ukc__tho} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    jusf__rad = len(df.columns)
    eib__giin = ['data_{}'.format(i) for i in olb__fbxg]
    gvpr__puu = ['data_{}'.format(i) for i in range(jusf__rad) if i not in
        olb__fbxg]
    if eib__giin:
        pwobb__moyql = len(eib__giin)
    else:
        pwobb__moyql = jusf__rad
    zmy__pctsn = ', '.join(eib__giin + gvpr__puu)
    data_args = ', '.join('data_{}'.format(i) for i in range(jusf__rad))
    ygby__ohho = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(jusf__rad):
        ygby__ohho += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    ygby__ohho += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(zmy__pctsn, index, pwobb__moyql))
    ygby__ohho += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(ygby__ohho, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):

                def cond_str(i, gen_all_false):
                    if df.columns[i] in cond.column_index:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {cond.column_index[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            ftfg__oef = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                ftfg__oef = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                ftfg__oef = lambda i: f'other[:,{i}]'
        jusf__rad = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {ftfg__oef(i)})'
             for i in range(jusf__rad))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        tglv__mfc = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(tglv__mfc)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    hufbv__twj = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    odmlh__pek = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    jusf__rad = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        for i in range(jusf__rad):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], other.data[other.
                    column_index[df.columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(jusf__rad):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other.data)
    else:
        for i in range(jusf__rad):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    wabvr__iphq = ColNamesMetaType(tuple(columns))
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    ygby__ohho = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, __col_name_meta_value_gen_init_df)
"""
    cghh__zimi = {}
    tdsb__ovjf = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba,
        '__col_name_meta_value_gen_init_df': wabvr__iphq}
    tdsb__ovjf.update(extra_globals)
    exec(ygby__ohho, tdsb__ovjf, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        soyr__nzv = pd.Index(lhs.columns)
        ujxe__rwzu = pd.Index(rhs.columns)
        gzxy__natug, ozl__psxk, shwq__ljfwj = soyr__nzv.join(ujxe__rwzu,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(gzxy__natug), ozl__psxk, shwq__ljfwj
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        kyp__kpxs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        iij__sbsv = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, kyp__kpxs)
        check_runtime_cols_unsupported(rhs, kyp__kpxs)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                gzxy__natug, ozl__psxk, shwq__ljfwj = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {ftvbl__ctwdn}) {kyp__kpxs}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {srjr__fpdh})'
                     if ftvbl__ctwdn != -1 and srjr__fpdh != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for ftvbl__ctwdn, srjr__fpdh in zip(ozl__psxk,
                    shwq__ljfwj))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, gzxy__natug, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            brwn__xkp = []
            pgno__has = []
            if op in iij__sbsv:
                for i, jgo__dsb in enumerate(lhs.data):
                    if is_common_scalar_dtype([jgo__dsb.dtype, rhs]):
                        brwn__xkp.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {kyp__kpxs} rhs'
                            )
                    else:
                        ugx__iirqo = f'arr{i}'
                        pgno__has.append(ugx__iirqo)
                        brwn__xkp.append(ugx__iirqo)
                data_args = ', '.join(brwn__xkp)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {kyp__kpxs} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(pgno__has) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {ugx__iirqo} = np.empty(n, dtype=np.bool_)\n' for
                    ugx__iirqo in pgno__has)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(ugx__iirqo, 
                    op == operator.ne) for ugx__iirqo in pgno__has)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            brwn__xkp = []
            pgno__has = []
            if op in iij__sbsv:
                for i, jgo__dsb in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, jgo__dsb.dtype]):
                        brwn__xkp.append(
                            f'lhs {kyp__kpxs} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        ugx__iirqo = f'arr{i}'
                        pgno__has.append(ugx__iirqo)
                        brwn__xkp.append(ugx__iirqo)
                data_args = ', '.join(brwn__xkp)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, kyp__kpxs) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(pgno__has) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(ugx__iirqo) for ugx__iirqo in pgno__has)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(ugx__iirqo, 
                    op == operator.ne) for ugx__iirqo in pgno__has)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        tglv__mfc = create_binary_op_overload(op)
        overload(op)(tglv__mfc)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        kyp__kpxs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, kyp__kpxs)
        check_runtime_cols_unsupported(right, kyp__kpxs)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                gzxy__natug, _, shwq__ljfwj = _get_binop_columns(left,
                    right, True)
                ygby__ohho = 'def impl(left, right):\n'
                for i, srjr__fpdh in enumerate(shwq__ljfwj):
                    if srjr__fpdh == -1:
                        ygby__ohho += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    ygby__ohho += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    ygby__ohho += f"""  df_arr{i} {kyp__kpxs} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {srjr__fpdh})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    gzxy__natug)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(ygby__ohho, gzxy__natug, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            ygby__ohho = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                ygby__ohho += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                ygby__ohho += '  df_arr{0} {1} right\n'.format(i, kyp__kpxs)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(ygby__ohho, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        tglv__mfc = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(tglv__mfc)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            kyp__kpxs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, kyp__kpxs)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, kyp__kpxs) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        tglv__mfc = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(tglv__mfc)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            scal__qmrfx = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                scal__qmrfx[i] = bodo.libs.array_kernels.isna(obj, i)
            return scal__qmrfx
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            scal__qmrfx = np.empty(n, np.bool_)
            for i in range(n):
                scal__qmrfx[i] = pd.isna(obj[i])
            return scal__qmrfx
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    vpllq__drewi = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    jqhn__sncv = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    yum__rxlp = str(expr_node)
    return yum__rxlp.startswith('(left.') or yum__rxlp.startswith('(right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    fotj__kgq = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (fotj__kgq,))
    nbyld__gedcl = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        nnte__fyqp = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        ieffr__uvxzb = {('NOT_NA', nbyld__gedcl(jgo__dsb)): jgo__dsb for
            jgo__dsb in null_set}
        zptiq__ygt, _, _ = _parse_query_expr(nnte__fyqp, env, [], [], None,
            join_cleaned_cols=ieffr__uvxzb)
        frvbo__pnuw = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            pdmjo__gsvkt = pd.core.computation.ops.BinOp('&', zptiq__ygt,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = frvbo__pnuw
        return pdmjo__gsvkt

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                egfty__ckvd = set()
                hiac__gfcw = set()
                izr__vly = _insert_NA_cond_body(expr_node.lhs, egfty__ckvd)
                xciy__qms = _insert_NA_cond_body(expr_node.rhs, hiac__gfcw)
                hrzdx__eoly = egfty__ckvd.intersection(hiac__gfcw)
                egfty__ckvd.difference_update(hrzdx__eoly)
                hiac__gfcw.difference_update(hrzdx__eoly)
                null_set.update(hrzdx__eoly)
                expr_node.lhs = append_null_checks(izr__vly, egfty__ckvd)
                expr_node.rhs = append_null_checks(xciy__qms, hiac__gfcw)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            pbh__lbn = expr_node.name
            bvrzx__pun, col_name = pbh__lbn.split('.')
            if bvrzx__pun == 'left':
                zzw__jrj = left_columns
                data = left_data
            else:
                zzw__jrj = right_columns
                data = right_data
            vaw__zrr = data[zzw__jrj.index(col_name)]
            if bodo.utils.typing.is_nullable(vaw__zrr):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    pbmfy__vvwaq = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        niq__duhg = str(expr_node.lhs)
        okwrf__koc = str(expr_node.rhs)
        if niq__duhg.startswith('(left.') and okwrf__koc.startswith('(left.'
            ) or niq__duhg.startswith('(right.') and okwrf__koc.startswith(
            '(right.'):
            return [], [], expr_node
        left_on = [niq__duhg.split('.')[1][:-1]]
        right_on = [okwrf__koc.split('.')[1][:-1]]
        if niq__duhg.startswith('(right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        zfcus__wle, kqs__eclb, hpo__gjza = _extract_equal_conds(expr_node.lhs)
        izghi__slhb, man__azsc, kynl__taep = _extract_equal_conds(expr_node.rhs
            )
        left_on = zfcus__wle + izghi__slhb
        right_on = kqs__eclb + man__azsc
        if hpo__gjza is None:
            return left_on, right_on, kynl__taep
        if kynl__taep is None:
            return left_on, right_on, hpo__gjza
        expr_node.lhs = hpo__gjza
        expr_node.rhs = kynl__taep
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    fotj__kgq = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (fotj__kgq,))
    uslfx__ozjst = dict()
    nbyld__gedcl = pd.core.computation.parsing.clean_column_name
    for name, oxjq__vrh in (('left', left_columns), ('right', right_columns)):
        for jgo__dsb in oxjq__vrh:
            poyxs__xdc = nbyld__gedcl(jgo__dsb)
            cebsg__dgugj = name, poyxs__xdc
            if cebsg__dgugj in uslfx__ozjst:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{jgo__dsb}' and '{uslfx__ozjst[poyxs__xdc]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            uslfx__ozjst[cebsg__dgugj] = jgo__dsb
    yxxd__mwq, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=uslfx__ozjst)
    left_on, right_on, ucr__hcu = _extract_equal_conds(yxxd__mwq.terms)
    return left_on, right_on, _insert_NA_cond(ucr__hcu, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    hufbv__twj = dict(sort=sort, copy=copy, validate=validate)
    odmlh__pek = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    fmqli__euszl = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    swej__tzux = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in fmqli__euszl and ('left.' in on_str or 
                'right.' in on_str):
                left_on, right_on, uqz__rer = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if uqz__rer is None:
                    swej__tzux = ''
                else:
                    swej__tzux = str(uqz__rer)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = fmqli__euszl
        right_keys = fmqli__euszl
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    pqh__hyz = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        lon__xvo = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lon__xvo = list(get_overload_const_list(suffixes))
    suffix_x = lon__xvo[0]
    suffix_y = lon__xvo[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    ygby__ohho = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    ygby__ohho += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    ygby__ohho += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    ygby__ohho += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, pqh__hyz, swej__tzux))
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    _impl = cghh__zimi['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, FloatingArrayType, DecimalArrayType,
        IntervalArrayType, bodo.DatetimeArrayType, TimeArrayType)
    bkqua__qvt = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    wmzqm__cuqk = {get_overload_const_str(xyjro__opp) for xyjro__opp in (
        left_on, right_on, on) if is_overload_constant_str(xyjro__opp)}
    for df in (left, right):
        for i, jgo__dsb in enumerate(df.data):
            if not isinstance(jgo__dsb, valid_dataframe_column_types
                ) and jgo__dsb not in bkqua__qvt:
                raise BodoError(
                    f'{name_func}(): use of column with {type(jgo__dsb)} in merge unsupported'
                    )
            if df.columns[i] in wmzqm__cuqk and isinstance(jgo__dsb,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        lon__xvo = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        lon__xvo = list(get_overload_const_list(suffixes))
    if len(lon__xvo) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    fmqli__euszl = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        tpygx__zgciq = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            tpygx__zgciq = on_str not in fmqli__euszl and ('left.' in
                on_str or 'right.' in on_str)
        if len(fmqli__euszl) == 0 and not tpygx__zgciq:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner', 'cross'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    eaqt__ddhpc = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            hfdp__jzx = left.index
            vnpxs__znjm = isinstance(hfdp__jzx, StringIndexType)
            xpkn__xeoh = right.index
            wxlu__rzrz = isinstance(xpkn__xeoh, StringIndexType)
        elif is_overload_true(left_index):
            hfdp__jzx = left.index
            vnpxs__znjm = isinstance(hfdp__jzx, StringIndexType)
            xpkn__xeoh = right.data[right.columns.index(right_keys[0])]
            wxlu__rzrz = xpkn__xeoh.dtype == string_type
        elif is_overload_true(right_index):
            hfdp__jzx = left.data[left.columns.index(left_keys[0])]
            vnpxs__znjm = hfdp__jzx.dtype == string_type
            xpkn__xeoh = right.index
            wxlu__rzrz = isinstance(xpkn__xeoh, StringIndexType)
        if vnpxs__znjm and wxlu__rzrz:
            return
        hfdp__jzx = hfdp__jzx.dtype
        xpkn__xeoh = xpkn__xeoh.dtype
        try:
            agy__abic = eaqt__ddhpc.resolve_function_type(operator.eq, (
                hfdp__jzx, xpkn__xeoh), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=hfdp__jzx, rk_dtype=xpkn__xeoh))
    else:
        for xqam__lquxf, iyidy__zgnhl in zip(left_keys, right_keys):
            hfdp__jzx = left.data[left.columns.index(xqam__lquxf)].dtype
            phrjx__stgxf = left.data[left.columns.index(xqam__lquxf)]
            xpkn__xeoh = right.data[right.columns.index(iyidy__zgnhl)].dtype
            fezsv__tchg = right.data[right.columns.index(iyidy__zgnhl)]
            if phrjx__stgxf == fezsv__tchg:
                continue
            qsa__xckad = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=xqam__lquxf, lk_dtype=hfdp__jzx, rk=iyidy__zgnhl,
                rk_dtype=xpkn__xeoh))
            ddse__txe = hfdp__jzx == string_type
            yajyp__umheg = xpkn__xeoh == string_type
            if ddse__txe ^ yajyp__umheg:
                raise_bodo_error(qsa__xckad)
            try:
                agy__abic = eaqt__ddhpc.resolve_function_type(operator.eq,
                    (hfdp__jzx, xpkn__xeoh), {})
            except:
                raise_bodo_error(qsa__xckad)


def validate_keys(keys, df):
    ybxi__qfzdt = set(keys).difference(set(df.columns))
    if len(ybxi__qfzdt) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in ybxi__qfzdt:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {ybxi__qfzdt} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    hufbv__twj = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    odmlh__pek = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    ygby__ohho = "def _impl(left, other, on=None, how='left',\n"
    ygby__ohho += "    lsuffix='', rsuffix='', sort=False):\n"
    ygby__ohho += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    _impl = cghh__zimi['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        zlex__qkg = get_overload_const_list(on)
        validate_keys(zlex__qkg, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    fmqli__euszl = tuple(set(left.columns) & set(other.columns))
    if len(fmqli__euszl) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=fmqli__euszl))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    bqwdb__wos = set(left_keys) & set(right_keys)
    whlh__ehuju = set(left_columns) & set(right_columns)
    mhtq__ylbd = whlh__ehuju - bqwdb__wos
    acx__rgb = set(left_columns) - whlh__ehuju
    eegcl__nha = set(right_columns) - whlh__ehuju
    lvtdj__mxk = {}

    def insertOutColumn(col_name):
        if col_name in lvtdj__mxk:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        lvtdj__mxk[col_name] = 0
    for vpi__yng in bqwdb__wos:
        insertOutColumn(vpi__yng)
    for vpi__yng in mhtq__ylbd:
        hadr__lmpz = str(vpi__yng) + suffix_x
        typw__bsl = str(vpi__yng) + suffix_y
        insertOutColumn(hadr__lmpz)
        insertOutColumn(typw__bsl)
    for vpi__yng in acx__rgb:
        insertOutColumn(vpi__yng)
    for vpi__yng in eegcl__nha:
        insertOutColumn(vpi__yng)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    raise BodoError('pandas.merge_asof() not support yet')
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    fmqli__euszl = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = fmqli__euszl
        right_keys = fmqli__euszl
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        lon__xvo = suffixes
    if is_overload_constant_list(suffixes):
        lon__xvo = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        lon__xvo = suffixes.value
    suffix_x = lon__xvo[0]
    suffix_y = lon__xvo[1]
    ygby__ohho = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    ygby__ohho += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    ygby__ohho += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    ygby__ohho += "    allow_exact_matches=True, direction='backward'):\n"
    ygby__ohho += '  suffix_x = suffixes[0]\n'
    ygby__ohho += '  suffix_y = suffixes[1]\n'
    ygby__ohho += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo}, cghh__zimi)
    _impl = cghh__zimi['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True, _bodo_num_shuffle_keys=-1):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna, _bodo_num_shuffle_keys)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True,
        _bodo_num_shuffle_keys=-1):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna, _bodo_num_shuffle_keys)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna, _num_shuffle_keys):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    if not is_overload_constant_int(_num_shuffle_keys):
        raise_bodo_error(
            f"groupby(): '_num_shuffle_keys' parameter must be a constant integer, not {_num_shuffle_keys}."
            )
    hufbv__twj = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    rrm__zrdm = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', hufbv__twj, rrm__zrdm,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    cyc__ailcf = func_name == 'DataFrame.pivot_table'
    if cyc__ailcf:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    ysgq__imhu = get_literal_value(columns)
    if isinstance(ysgq__imhu, (list, tuple)):
        if len(ysgq__imhu) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {ysgq__imhu}"
                )
        ysgq__imhu = ysgq__imhu[0]
    if ysgq__imhu not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {ysgq__imhu} not found in DataFrame {df}."
            )
    qbf__aoaky = df.column_index[ysgq__imhu]
    if is_overload_none(index):
        ateu__hql = []
        xviu__ampkb = []
    else:
        xviu__ampkb = get_literal_value(index)
        if not isinstance(xviu__ampkb, (list, tuple)):
            xviu__ampkb = [xviu__ampkb]
        ateu__hql = []
        for index in xviu__ampkb:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            ateu__hql.append(df.column_index[index])
    if not (all(isinstance(nsg__dhub, int) for nsg__dhub in xviu__ampkb) or
        all(isinstance(nsg__dhub, str) for nsg__dhub in xviu__ampkb)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        pup__fvba = []
        frhog__lazpv = []
        yjc__dmmct = ateu__hql + [qbf__aoaky]
        for i, nsg__dhub in enumerate(df.columns):
            if i not in yjc__dmmct:
                pup__fvba.append(i)
                frhog__lazpv.append(nsg__dhub)
    else:
        frhog__lazpv = get_literal_value(values)
        if not isinstance(frhog__lazpv, (list, tuple)):
            frhog__lazpv = [frhog__lazpv]
        pup__fvba = []
        for val in frhog__lazpv:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            pup__fvba.append(df.column_index[val])
    qpgyt__ddmew = set(pup__fvba) | set(ateu__hql) | {qbf__aoaky}
    if len(qpgyt__ddmew) != len(pup__fvba) + len(ateu__hql) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(ateu__hql) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for mypc__dagek in ateu__hql:
            index_column = df.data[mypc__dagek]
            check_valid_index_typ(index_column)
    bix__jtw = df.data[qbf__aoaky]
    if isinstance(bix__jtw, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(bix__jtw, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for tgj__ojqit in pup__fvba:
        dpr__aio = df.data[tgj__ojqit]
        if isinstance(dpr__aio, (bodo.ArrayItemArrayType, bodo.MapArrayType,
            bodo.StructArrayType, bodo.TupleArrayType)
            ) or dpr__aio == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (xviu__ampkb, ysgq__imhu, frhog__lazpv, ateu__hql, qbf__aoaky,
        pup__fvba)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (xviu__ampkb, ysgq__imhu, frhog__lazpv, mypc__dagek, qbf__aoaky, nwbr__qby
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(xviu__ampkb) == 0:
        if is_overload_none(data.index.name_typ):
            nkqi__pidc = None,
        else:
            nkqi__pidc = get_literal_value(data.index.name_typ),
    else:
        nkqi__pidc = tuple(xviu__ampkb)
    xviu__ampkb = ColNamesMetaType(nkqi__pidc)
    frhog__lazpv = ColNamesMetaType(tuple(frhog__lazpv))
    ysgq__imhu = ColNamesMetaType((ysgq__imhu,))
    ygby__ohho = 'def impl(data, index=None, columns=None, values=None):\n'
    ygby__ohho += "    ev = tracing.Event('df.pivot')\n"
    ygby__ohho += f'    pivot_values = data.iloc[:, {qbf__aoaky}].unique()\n'
    ygby__ohho += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(mypc__dagek) == 0:
        ygby__ohho += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        ygby__ohho += '        (\n'
        for wopck__eis in mypc__dagek:
            ygby__ohho += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {wopck__eis}),
"""
        ygby__ohho += '        ),\n'
    ygby__ohho += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {qbf__aoaky}),),
"""
    ygby__ohho += '        (\n'
    for tgj__ojqit in nwbr__qby:
        ygby__ohho += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {tgj__ojqit}),
"""
    ygby__ohho += '        ),\n'
    ygby__ohho += '        pivot_values,\n'
    ygby__ohho += '        index_lit,\n'
    ygby__ohho += '        columns_lit,\n'
    ygby__ohho += '        values_lit,\n'
    ygby__ohho += '    )\n'
    ygby__ohho += '    ev.finalize()\n'
    ygby__ohho += '    return result\n'
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'index_lit': xviu__ampkb, 'columns_lit':
        ysgq__imhu, 'values_lit': frhog__lazpv, 'tracing': tracing}, cghh__zimi
        )
    impl = cghh__zimi['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    hufbv__twj = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    odmlh__pek = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    (xviu__ampkb, ysgq__imhu, frhog__lazpv, mypc__dagek, qbf__aoaky, nwbr__qby
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot_table'))
    jdens__scayo = xviu__ampkb
    xviu__ampkb = ColNamesMetaType(tuple(xviu__ampkb))
    frhog__lazpv = ColNamesMetaType(tuple(frhog__lazpv))
    osqqm__gxoyj = ysgq__imhu
    ysgq__imhu = ColNamesMetaType((ysgq__imhu,))
    ygby__ohho = 'def impl(\n'
    ygby__ohho += '    data,\n'
    ygby__ohho += '    values=None,\n'
    ygby__ohho += '    index=None,\n'
    ygby__ohho += '    columns=None,\n'
    ygby__ohho += '    aggfunc="mean",\n'
    ygby__ohho += '    fill_value=None,\n'
    ygby__ohho += '    margins=False,\n'
    ygby__ohho += '    dropna=True,\n'
    ygby__ohho += '    margins_name="All",\n'
    ygby__ohho += '    observed=False,\n'
    ygby__ohho += '    sort=True,\n'
    ygby__ohho += '    _pivot_values=None,\n'
    ygby__ohho += '):\n'
    ygby__ohho += "    ev = tracing.Event('df.pivot_table')\n"
    lmon__zied = mypc__dagek + [qbf__aoaky] + nwbr__qby
    ygby__ohho += f'    data = data.iloc[:, {lmon__zied}]\n'
    uiioi__tnxn = jdens__scayo + [osqqm__gxoyj]
    if not is_overload_none(_pivot_values):
        kghpy__tnenl = tuple(sorted(_pivot_values.meta))
        _pivot_values = ColNamesMetaType(kghpy__tnenl)
        ygby__ohho += '    pivot_values = _pivot_values_arr\n'
        ygby__ohho += (
            f'    data = data[data.iloc[:, {len(mypc__dagek)}].isin(pivot_values)]\n'
            )
        if all(isinstance(nsg__dhub, str) for nsg__dhub in kghpy__tnenl):
            qoksq__oanp = pd.array(kghpy__tnenl, 'string')
        elif all(isinstance(nsg__dhub, int) for nsg__dhub in kghpy__tnenl):
            qoksq__oanp = np.array(kghpy__tnenl, 'int64')
        else:
            raise BodoError(
                f'pivot(): pivot values selcected via pivot JIT argument must all share a common int or string type.'
                )
    else:
        qoksq__oanp = None
    clsig__jyx = is_overload_constant_str(aggfunc) and get_overload_const_str(
        aggfunc) == 'nunique'
    ptf__qhcfc = len(uiioi__tnxn) if clsig__jyx else len(jdens__scayo)
    ygby__ohho += f"""    data = data.groupby({uiioi__tnxn!r}, as_index=False, _bodo_num_shuffle_keys={ptf__qhcfc}).agg(aggfunc)
"""
    if is_overload_none(_pivot_values):
        ygby__ohho += (
            f'    pivot_values = data.iloc[:, {len(mypc__dagek)}].unique()\n')
    ygby__ohho += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    ygby__ohho += '        (\n'
    for i in range(0, len(mypc__dagek)):
        ygby__ohho += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    ygby__ohho += '        ),\n'
    ygby__ohho += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(mypc__dagek)}),),
"""
    ygby__ohho += '        (\n'
    for i in range(len(mypc__dagek) + 1, len(nwbr__qby) + len(mypc__dagek) + 1
        ):
        ygby__ohho += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    ygby__ohho += '        ),\n'
    ygby__ohho += '        pivot_values,\n'
    ygby__ohho += '        index_lit,\n'
    ygby__ohho += '        columns_lit,\n'
    ygby__ohho += '        values_lit,\n'
    ygby__ohho += '        check_duplicates=False,\n'
    ygby__ohho += f'        is_already_shuffled={not clsig__jyx},\n'
    ygby__ohho += '        _constant_pivot_values=_constant_pivot_values,\n'
    ygby__ohho += '    )\n'
    ygby__ohho += '    ev.finalize()\n'
    ygby__ohho += '    return result\n'
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'numba': numba, 'index_lit':
        xviu__ampkb, 'columns_lit': ysgq__imhu, 'values_lit': frhog__lazpv,
        '_pivot_values_arr': qoksq__oanp, '_constant_pivot_values':
        _pivot_values, 'tracing': tracing}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    hufbv__twj = dict(col_level=col_level, ignore_index=ignore_index)
    odmlh__pek = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame.")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal.")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal.")
    if not is_overload_none(var_name) and not (is_literal_type(var_name) and
        (is_scalar_type(var_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'var_name', if specified, must be a literal.")
    if value_name != 'value' and not (is_literal_type(value_name) and (
        is_scalar_type(value_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'value_name', if specified, must be a literal.")
    var_name = get_literal_value(var_name) if not is_overload_none(var_name
        ) else 'variable'
    value_name = get_literal_value(value_name
        ) if value_name != 'value' else 'value'
    fequ__hmra = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(fequ__hmra, (list, tuple)):
        fequ__hmra = [fequ__hmra]
    for nsg__dhub in fequ__hmra:
        if nsg__dhub not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {nsg__dhub} not found in {frame}."
                )
    golv__cpbs = [frame.column_index[i] for i in fequ__hmra]
    if is_overload_none(value_vars):
        fblg__wpbow = []
        hbuco__uqg = []
        for i, nsg__dhub in enumerate(frame.columns):
            if i not in golv__cpbs:
                fblg__wpbow.append(i)
                hbuco__uqg.append(nsg__dhub)
    else:
        hbuco__uqg = get_literal_value(value_vars)
        if not isinstance(hbuco__uqg, (list, tuple)):
            hbuco__uqg = [hbuco__uqg]
        hbuco__uqg = [v for v in hbuco__uqg if v not in fequ__hmra]
        if not hbuco__uqg:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        fblg__wpbow = []
        for val in hbuco__uqg:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            fblg__wpbow.append(frame.column_index[val])
    for nsg__dhub in hbuco__uqg:
        if nsg__dhub not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {nsg__dhub} not found in {frame}."
                )
    if not (all(isinstance(nsg__dhub, int) for nsg__dhub in hbuco__uqg) or
        all(isinstance(nsg__dhub, str) for nsg__dhub in hbuco__uqg)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    qjp__mwter = frame.data[fblg__wpbow[0]]
    yel__isuyl = [frame.data[i].dtype for i in fblg__wpbow]
    fblg__wpbow = np.array(fblg__wpbow, dtype=np.int64)
    golv__cpbs = np.array(golv__cpbs, dtype=np.int64)
    _, uft__rav = bodo.utils.typing.get_common_scalar_dtype(yel__isuyl)
    if not uft__rav:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': hbuco__uqg, 'val_type': qjp__mwter}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == qjp__mwter.dtype for v in yel__isuyl
        ):
        extra_globals['value_idxs'] = bodo.utils.typing.MetaType(tuple(
            fblg__wpbow))
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(hbuco__uqg) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {fblg__wpbow[0]})
"""
    else:
        gvxsl__tgroa = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in fblg__wpbow)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({gvxsl__tgroa},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in golv__cpbs:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(hbuco__uqg)})\n'
            )
    vag__begcr = ', '.join(f'out_id{i}' for i in golv__cpbs) + (', ' if len
        (golv__cpbs) > 0 else '')
    data_args = vag__begcr + 'var_col, val_col'
    columns = tuple(fequ__hmra + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(hbuco__uqg)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    raise BodoError(f'pandas.crosstab() not supported yet')
    hufbv__twj = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    odmlh__pek = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_chunk_bounds=None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    hufbv__twj = dict(ignore_index=ignore_index, key=key)
    odmlh__pek = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position, _bodo_chunk_bounds)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_chunk_bounds=None, _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position, _bodo_chunk_bounds)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position, _bodo_chunk_bounds):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    yrum__eiuf = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        yrum__eiuf.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        ikj__nkyf = [get_overload_const_tuple(by)]
    else:
        ikj__nkyf = get_overload_const_list(by)
    ikj__nkyf = set((k, '') if (k, '') in yrum__eiuf else k for k in ikj__nkyf)
    if len(ikj__nkyf.difference(yrum__eiuf)) > 0:
        drlnv__poxm = list(set(get_overload_const_list(by)).difference(
            yrum__eiuf))
        raise_bodo_error(f'sort_values(): invalid keys {drlnv__poxm} for by.')
    if not is_overload_none(_bodo_chunk_bounds) and len(ikj__nkyf) != 1:
        raise_bodo_error(
            f'sort_values(): _bodo_chunk_bounds only supported when there is a single key.'
            )
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        llgs__judl = get_overload_const_list(na_position)
        for na_position in llgs__judl:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    hufbv__twj = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    odmlh__pek = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position, None)
    return _impl


@overload_method(DataFrameType, 'rank', inline='always', no_unliteral=True)
def overload_dataframe_rank(df, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    ygby__ohho = """def impl(df, axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False):
"""
    jusf__rad = len(df.columns)
    data_args = ', '.join(
        'bodo.libs.array_kernels.rank(data_{}, method=method, na_option=na_option, ascending=ascending, pct=pct)'
        .format(i) for i in range(jusf__rad))
    for i in range(jusf__rad):
        ygby__ohho += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(ygby__ohho, df.columns, data_args, index)


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    hufbv__twj = dict(limit=limit, downcast=downcast)
    odmlh__pek = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    tcnhg__qdk = not is_overload_none(value)
    kvgmo__vzz = not is_overload_none(method)
    if tcnhg__qdk and kvgmo__vzz:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not tcnhg__qdk and not kvgmo__vzz:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if tcnhg__qdk:
        hcr__gdc = 'value=value'
    else:
        hcr__gdc = 'method=method'
    data_args = [(f"df['{nsg__dhub}'].fillna({hcr__gdc}, inplace=inplace)" if
        isinstance(nsg__dhub, str) else
        f'df[{nsg__dhub}].fillna({hcr__gdc}, inplace=inplace)') for
        nsg__dhub in df.columns]
    ygby__ohho = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        ygby__ohho += '  ' + '  \n'.join(data_args) + '\n'
        cghh__zimi = {}
        exec(ygby__ohho, {}, cghh__zimi)
        impl = cghh__zimi['impl']
        return impl
    else:
        return _gen_init_df(ygby__ohho, df.columns, ', '.join(vckqe__wyx +
            '.values' for vckqe__wyx in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    hufbv__twj = dict(col_level=col_level, col_fill=col_fill)
    odmlh__pek = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    ygby__ohho = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    ygby__ohho += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        yomk__famk = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            yomk__famk)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            ygby__ohho += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            mmxt__jna = ['m_index[{}]'.format(i) for i in range(df.index.
                nlevels)]
            data_args = mmxt__jna + data_args
        else:
            svnmm__zmtk = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [svnmm__zmtk] + data_args
    return _gen_init_df(ygby__ohho, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    xac__sqbxx = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and xac__sqbxx == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(xac__sqbxx))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        cnqqk__tbdl = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        ilig__dzyls = get_overload_const_list(subset)
        cnqqk__tbdl = []
        for xqpzl__rrhl in ilig__dzyls:
            if xqpzl__rrhl not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{xqpzl__rrhl}' not in data frame columns {df}"
                    )
            cnqqk__tbdl.append(df.column_index[xqpzl__rrhl])
    jusf__rad = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(jusf__rad))
    ygby__ohho = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(jusf__rad):
        ygby__ohho += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    ygby__ohho += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in cnqqk__tbdl)))
    ygby__ohho += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(ygby__ohho, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    hufbv__twj = dict(index=index, level=level, errors=errors)
    odmlh__pek = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', hufbv__twj, odmlh__pek,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            otrff__qrjkc = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            otrff__qrjkc = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            otrff__qrjkc = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            otrff__qrjkc = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for nsg__dhub in otrff__qrjkc:
        if nsg__dhub not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(nsg__dhub, df.columns))
    if len(set(otrff__qrjkc)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    coycl__lcco = tuple(nsg__dhub for nsg__dhub in df.columns if nsg__dhub
         not in otrff__qrjkc)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[nsg__dhub], '.copy()' if not inplace else ''
        ) for nsg__dhub in coycl__lcco)
    ygby__ohho = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    ygby__ohho += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(ygby__ohho, coycl__lcco, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    hufbv__twj = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    yhft__sait = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', hufbv__twj, yhft__sait,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    jusf__rad = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(jusf__rad))
    snhjk__ahmu = ', '.join('rhs_data_{}'.format(i) for i in range(jusf__rad))
    ygby__ohho = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    ygby__ohho += '  if (frac == 1 or n == len(df)) and not replace:\n'
    ygby__ohho += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(jusf__rad):
        ygby__ohho += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    ygby__ohho += '  if frac is None:\n'
    ygby__ohho += '    frac_d = -1.0\n'
    ygby__ohho += '  else:\n'
    ygby__ohho += '    frac_d = frac\n'
    ygby__ohho += '  if n is None:\n'
    ygby__ohho += '    n_i = 0\n'
    ygby__ohho += '  else:\n'
    ygby__ohho += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    ygby__ohho += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({snhjk__ahmu},), {index}, n_i, frac_d, replace)
"""
    ygby__ohho += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(ygby__ohho, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    vpllq__drewi = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    jqhn__sncv = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', vpllq__drewi, jqhn__sncv,
        package_name='pandas', module_name='DataFrame')
    nqhsu__ztsc = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            eyk__opmx = nqhsu__ztsc + '\n'
            eyk__opmx += 'Index: 0 entries\n'
            eyk__opmx += 'Empty DataFrame'
            print(eyk__opmx)
        return _info_impl
    else:
        ygby__ohho = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        ygby__ohho += '    ncols = df.shape[1]\n'
        ygby__ohho += f'    lines = "{nqhsu__ztsc}\\n"\n'
        ygby__ohho += f'    lines += "{df.index}: "\n'
        ygby__ohho += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            ygby__ohho += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            ygby__ohho += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            ygby__ohho += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        ygby__ohho += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        ygby__ohho += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        ygby__ohho += '    column_width = max(space, 7)\n'
        ygby__ohho += '    column= "Column"\n'
        ygby__ohho += '    underl= "------"\n'
        ygby__ohho += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        ygby__ohho += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        ygby__ohho += '    mem_size = 0\n'
        ygby__ohho += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        ygby__ohho += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        ygby__ohho += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        xdff__crqfo = dict()
        for i in range(len(df.columns)):
            ygby__ohho += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            svb__ekan = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                svb__ekan = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                waqa__vie = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                svb__ekan = f'{waqa__vie[:-7]}'
            ygby__ohho += f'    col_dtype[{i}] = "{svb__ekan}"\n'
            if svb__ekan in xdff__crqfo:
                xdff__crqfo[svb__ekan] += 1
            else:
                xdff__crqfo[svb__ekan] = 1
            ygby__ohho += f'    col_name[{i}] = "{df.columns[i]}"\n'
            ygby__ohho += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        ygby__ohho += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        ygby__ohho += '    for i in column_info:\n'
        ygby__ohho += "        lines += f'{i}\\n'\n"
        oqfhy__mgt = ', '.join(f'{k}({xdff__crqfo[k]})' for k in sorted(
            xdff__crqfo))
        ygby__ohho += f"    lines += 'dtypes: {oqfhy__mgt}\\n'\n"
        ygby__ohho += '    mem_size += df.index.nbytes\n'
        ygby__ohho += '    total_size = _sizeof_fmt(mem_size)\n'
        ygby__ohho += "    lines += f'memory usage: {total_size}'\n"
        ygby__ohho += '    print(lines)\n'
        cghh__zimi = {}
        exec(ygby__ohho, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, cghh__zimi)
        _info_impl = cghh__zimi['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    ygby__ohho = 'def impl(df, index=True, deep=False):\n'
    omj__tlcd = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    grirn__vtx = is_overload_true(index)
    columns = df.columns
    if grirn__vtx:
        columns = ('Index',) + columns
    if len(columns) == 0:
        ihzhd__loxi = ()
    elif all(isinstance(nsg__dhub, int) for nsg__dhub in columns):
        ihzhd__loxi = np.array(columns, 'int64')
    elif all(isinstance(nsg__dhub, str) for nsg__dhub in columns):
        ihzhd__loxi = pd.array(columns, 'string')
    else:
        ihzhd__loxi = columns
    if df.is_table_format and len(df.columns) > 0:
        vyjvr__kdvmf = int(grirn__vtx)
        kjwj__kpyls = len(columns)
        ygby__ohho += f'  nbytes_arr = np.empty({kjwj__kpyls}, np.int64)\n'
        ygby__ohho += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        ygby__ohho += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {vyjvr__kdvmf})
"""
        if grirn__vtx:
            ygby__ohho += f'  nbytes_arr[0] = {omj__tlcd}\n'
        ygby__ohho += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if grirn__vtx:
            data = f'{omj__tlcd},{data}'
        else:
            sne__zngg = ',' if len(columns) == 1 else ''
            data = f'{data}{sne__zngg}'
        ygby__ohho += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        ihzhd__loxi}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    cjfxw__picpu = 'read_excel_df{}'.format(next_label())
    setattr(types, cjfxw__picpu, df_type)
    cwj__wnguf = False
    if is_overload_constant_list(parse_dates):
        cwj__wnguf = get_overload_const_list(parse_dates)
    llqcc__dfec = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    ygby__ohho = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{cjfxw__picpu}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{llqcc__dfec}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={cwj__wnguf},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    cghh__zimi = {}
    exec(ygby__ohho, globals(), cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as eytd__qjim:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    ygby__ohho = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    ygby__ohho += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    ygby__ohho += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        ygby__ohho += '   fig, ax = plt.subplots()\n'
    else:
        ygby__ohho += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        ygby__ohho += '   fig.set_figwidth(figsize[0])\n'
        ygby__ohho += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        ygby__ohho += '   xlabel = x\n'
    ygby__ohho += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        ygby__ohho += '   ylabel = y\n'
    else:
        ygby__ohho += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        ygby__ohho += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        ygby__ohho += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    ygby__ohho += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            ygby__ohho += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            kdxko__gjufb = get_overload_const_str(x)
            ryy__piqoy = df.columns.index(kdxko__gjufb)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if ryy__piqoy != i:
                        ygby__ohho += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            ygby__ohho += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        ygby__ohho += '   ax.scatter(df[x], df[y], s=20)\n'
        ygby__ohho += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        ygby__ohho += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        ygby__ohho += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        ygby__ohho += '   ax.legend()\n'
    ygby__ohho += '   return ax\n'
    cghh__zimi = {}
    exec(ygby__ohho, {'bodo': bodo, 'plt': plt}, cghh__zimi)
    impl = cghh__zimi['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for rjtm__hbw in df_typ.data:
        if not (isinstance(rjtm__hbw, (IntegerArrayType, FloatingArrayType)
            ) or isinstance(rjtm__hbw.dtype, types.Number) or rjtm__hbw.
            dtype in (bodo.datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        koom__gpshv = args[0]
        oltzk__mzxm = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        veg__pufad = koom__gpshv
        check_runtime_cols_unsupported(koom__gpshv, 'set_df_col()')
        if isinstance(koom__gpshv, DataFrameType):
            index = koom__gpshv.index
            if len(koom__gpshv.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(koom__gpshv.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if is_overload_constant_str(val) or val == types.unicode_type:
                val = bodo.dict_str_arr_type
            elif not is_array_typ(val):
                val = dtype_to_array_type(val)
            if oltzk__mzxm in koom__gpshv.columns:
                coycl__lcco = koom__gpshv.columns
                kcd__jenm = koom__gpshv.columns.index(oltzk__mzxm)
                acqi__kvlr = list(koom__gpshv.data)
                acqi__kvlr[kcd__jenm] = val
                acqi__kvlr = tuple(acqi__kvlr)
            else:
                coycl__lcco = koom__gpshv.columns + (oltzk__mzxm,)
                acqi__kvlr = koom__gpshv.data + (val,)
            veg__pufad = DataFrameType(acqi__kvlr, index, coycl__lcco,
                koom__gpshv.dist, koom__gpshv.is_table_format)
        return veg__pufad(*args)


SetDfColInfer.prefer_literal = True


def __bodosql_replace_columns_dummy(df, col_names_to_replace,
    cols_to_replace_with):
    for i in range(len(col_names_to_replace)):
        df[col_names_to_replace[i]] = cols_to_replace_with[i]


@infer_global(__bodosql_replace_columns_dummy)
class BodoSQLReplaceColsInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 3
        assert is_overload_constant_tuple(args[1])
        assert isinstance(args[2], types.BaseTuple)
        okk__die = args[0]
        assert isinstance(okk__die, DataFrameType) and len(okk__die.columns
            ) > 0, 'Error while typechecking __bodosql_replace_columns_dummy: we should only generate a call __bodosql_replace_columns_dummy if the input dataframe'
        col_names_to_replace = get_overload_const_tuple(args[1])
        iura__wpk = args[2]
        assert len(col_names_to_replace) == len(iura__wpk
            ), 'Error while typechecking __bodosql_replace_columns_dummy: the tuple of column indicies to replace should be equal to the number of columns to replace them with'
        assert len(col_names_to_replace) <= len(okk__die.columns
            ), 'Error while typechecking __bodosql_replace_columns_dummy: The number of indicies provided should be less than or equal to the number of columns in the input dataframe'
        for col_name in col_names_to_replace:
            assert col_name in okk__die.columns, 'Error while typechecking __bodosql_replace_columns_dummy: All columns specified to be replaced should already be present in input dataframe'
        check_runtime_cols_unsupported(okk__die,
            '__bodosql_replace_columns_dummy()')
        index = okk__die.index
        coycl__lcco = okk__die.columns
        acqi__kvlr = list(okk__die.data)
        for i in range(len(col_names_to_replace)):
            col_name = col_names_to_replace[i]
            khzzh__fop = iura__wpk[i]
            assert isinstance(khzzh__fop, SeriesType
                ), 'Error while typechecking __bodosql_replace_columns_dummy: the values to replace the columns with are expected to be series'
            if isinstance(khzzh__fop, SeriesType):
                khzzh__fop = khzzh__fop.data
            nvi__jltz = okk__die.column_index[col_name]
            acqi__kvlr[nvi__jltz] = khzzh__fop
        acqi__kvlr = tuple(acqi__kvlr)
        veg__pufad = DataFrameType(acqi__kvlr, index, coycl__lcco, okk__die
            .dist, okk__die.is_table_format)
        return veg__pufad(*args)


BodoSQLReplaceColsInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    tpg__aww = {}

    def _rewrite_membership_op(self, node, left, right):
        gwbh__qojnr = node.op
        op = self.visit(gwbh__qojnr)
        return op, gwbh__qojnr, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    ctbzu__evxp = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in ctbzu__evxp:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in ctbzu__evxp:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing('(' + self.name + ')')

    def visit_Attribute(self, node, **kwargs):
        pdjtm__vxgfu = node.attr
        value = node.value
        pgo__pdtuz = pd.core.computation.ops.LOCAL_TAG
        if pdjtm__vxgfu in ('str', 'dt'):
            try:
                iozo__dcv = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as whank__oci:
                col_name = whank__oci.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            iozo__dcv = str(self.visit(value))
        cebsg__dgugj = iozo__dcv, pdjtm__vxgfu
        if cebsg__dgugj in join_cleaned_cols:
            pdjtm__vxgfu = join_cleaned_cols[cebsg__dgugj]
        name = iozo__dcv + '.' + pdjtm__vxgfu
        if name.startswith(pgo__pdtuz):
            name = name[len(pgo__pdtuz):]
        if pdjtm__vxgfu in ('str', 'dt'):
            xunh__ubb = columns[cleaned_columns.index(iozo__dcv)]
            tpg__aww[xunh__ubb] = iozo__dcv
            self.env.scope[name] = 0
            return self.term_type(pgo__pdtuz + name, self.env)
        ctbzu__evxp.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in ctbzu__evxp:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        drd__fldk = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        oltzk__mzxm = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(drd__fldk), oltzk__mzxm))

    def op__str__(self):
        juwl__sqj = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            szkgx__kqsk)) for szkgx__kqsk in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(juwl__sqj)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(juwl__sqj)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(juwl__sqj))
    rsiw__fitzb = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    aghg__qtsz = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    qiwz__fyj = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    hyegp__mjfly = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    vxgfd__nifew = pd.core.computation.ops.Term.__str__
    qljzg__nohn = pd.core.computation.ops.MathCall.__str__
    dqhl__akdm = pd.core.computation.ops.Op.__str__
    frvbo__pnuw = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        yxxd__mwq = pd.core.computation.expr.Expr(expr, env=env)
        yulc__ystot = str(yxxd__mwq)
    except pd.core.computation.ops.UndefinedVariableError as whank__oci:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == whank__oci.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {whank__oci}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            rsiw__fitzb)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            aghg__qtsz)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = qiwz__fyj
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = hyegp__mjfly
        pd.core.computation.ops.Term.__str__ = vxgfd__nifew
        pd.core.computation.ops.MathCall.__str__ = qljzg__nohn
        pd.core.computation.ops.Op.__str__ = dqhl__akdm
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            frvbo__pnuw)
    bdpy__xsw = pd.core.computation.parsing.clean_column_name
    tpg__aww.update({nsg__dhub: bdpy__xsw(nsg__dhub) for nsg__dhub in
        columns if bdpy__xsw(nsg__dhub) in yxxd__mwq.names})
    return yxxd__mwq, yulc__ystot, tpg__aww


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        hncvw__hetaj = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(hncvw__hetaj))
        indqd__hajcu = namedtuple('Pandas', col_names)
        nyxoq__iclj = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], indqd__hajcu)
        super(DataFrameTupleIterator, self).__init__(name, nyxoq__iclj)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_tz_naive_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        olwzf__ccdw = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        olwzf__ccdw = [types.Array(types.int64, 1, 'C')] + olwzf__ccdw
        iaj__gfqf = DataFrameTupleIterator(col_names, olwzf__ccdw)
        return iaj__gfqf(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        phae__zgey = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            phae__zgey)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    bowoq__wyjjw = args[len(args) // 2:]
    gmic__lfnj = sig.args[len(sig.args) // 2:]
    srv__cckry = context.make_helper(builder, sig.return_type)
    fiw__mvwi = context.get_constant(types.intp, 0)
    vtk__bjo = cgutils.alloca_once_value(builder, fiw__mvwi)
    srv__cckry.index = vtk__bjo
    for i, arr in enumerate(bowoq__wyjjw):
        setattr(srv__cckry, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(bowoq__wyjjw, gmic__lfnj):
        context.nrt.incref(builder, arr_typ, arr)
    res = srv__cckry._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    ciplj__bnwax, = sig.args
    ufbz__mbbs, = args
    srv__cckry = context.make_helper(builder, ciplj__bnwax, value=ufbz__mbbs)
    enhyf__vme = signature(types.intp, ciplj__bnwax.array_types[1])
    jij__xresg = context.compile_internal(builder, lambda a: len(a),
        enhyf__vme, [srv__cckry.array0])
    index = builder.load(srv__cckry.index)
    ksie__awsi = builder.icmp_signed('<', index, jij__xresg)
    result.set_valid(ksie__awsi)
    with builder.if_then(ksie__awsi):
        values = [index]
        for i, arr_typ in enumerate(ciplj__bnwax.array_types[1:]):
            uouq__pgb = getattr(srv__cckry, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                wuxf__uryix = signature(pd_timestamp_tz_naive_type, arr_typ,
                    types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    wuxf__uryix, [uouq__pgb, index])
            else:
                wuxf__uryix = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    wuxf__uryix, [uouq__pgb, index])
            values.append(val)
        value = context.make_tuple(builder, ciplj__bnwax.yield_type, values)
        result.yield_(value)
        dnhy__ncyi = cgutils.increment_index(builder, index)
        builder.store(dnhy__ncyi, srv__cckry.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    nsrru__adq = ir.Assign(rhs, lhs, expr.loc)
    nfv__szl = lhs
    lbbgo__coj = []
    fxoxn__nbw = []
    pcg__gfj = typ.count
    for i in range(pcg__gfj):
        admur__nsis = ir.Var(nfv__szl.scope, mk_unique_var('{}_size{}'.
            format(nfv__szl.name, i)), nfv__szl.loc)
        gsxir__jph = ir.Expr.static_getitem(lhs, i, None, nfv__szl.loc)
        self.calltypes[gsxir__jph] = None
        lbbgo__coj.append(ir.Assign(gsxir__jph, admur__nsis, nfv__szl.loc))
        self._define(equiv_set, admur__nsis, types.intp, gsxir__jph)
        fxoxn__nbw.append(admur__nsis)
    wmw__jbdg = tuple(fxoxn__nbw)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        wmw__jbdg, pre=[nsrru__adq] + lbbgo__coj)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
