"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, convert_val_to_timestamp, pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import unwrap_tz_array
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import is_var_size_item_array_type
from bodo.utils.typing import BodoError, ColNamesMetaType, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_index_names, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            tekjn__eem = bodo.hiframes.pd_series_ext.get_series_data(s)
            zxi__eans = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                tekjn__eem)
            return zxi__eans
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            fadp__ivqj = list()
            for jmtr__xctzs in range(len(S)):
                fadp__ivqj.append(S.iat[jmtr__xctzs])
            return fadp__ivqj
        return impl_float

    def impl(S):
        fadp__ivqj = list()
        for jmtr__xctzs in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, jmtr__xctzs):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            fadp__ivqj.append(S.iat[jmtr__xctzs])
        return fadp__ivqj
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    jmq__afoq = dict(dtype=dtype, copy=copy, na_value=na_value)
    kqonb__mfoba = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    jmq__afoq = dict(name=name, inplace=inplace)
    kqonb__mfoba = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        wikw__gre = ', '.join(['index_arrs[{}]'.format(jmtr__xctzs) for
            jmtr__xctzs in range(S.index.nlevels)])
    else:
        wikw__gre = '    bodo.utils.conversion.index_to_array(index)\n'
    iax__dka = 'index' if 'index' != series_name else 'level_0'
    aaxg__tbavd = get_index_names(S.index, 'Series.reset_index()', iax__dka)
    columns = [name for name in aaxg__tbavd]
    columns.append(series_name)
    qkop__hhv = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    qkop__hhv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qkop__hhv += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        qkop__hhv += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    qkop__hhv += (
        '    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)\n'
        )
    qkop__hhv += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({wikw__gre}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    onob__eiui = {}
    exec(qkop__hhv, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, onob__eiui)
    wevs__kqzwe = onob__eiui['_impl']
    return wevs__kqzwe


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        twhyr__yeg = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[jmtr__xctzs]):
                bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
            else:
                twhyr__yeg[jmtr__xctzs] = np.round(arr[jmtr__xctzs], decimals)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    jmq__afoq = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    kqonb__mfoba = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        jolxr__odz = bodo.hiframes.pd_series_ext.get_series_data(S)
        wqjaf__nymuh = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        gisp__cxbws = 0
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(jolxr__odz)
            ):
            czbn__chuy = 0
            cia__ytgw = bodo.libs.array_kernels.isna(jolxr__odz, jmtr__xctzs)
            uzq__bydj = bodo.libs.array_kernels.isna(wqjaf__nymuh, jmtr__xctzs)
            if cia__ytgw and not uzq__bydj or not cia__ytgw and uzq__bydj:
                czbn__chuy = 1
            elif not cia__ytgw:
                if jolxr__odz[jmtr__xctzs] != wqjaf__nymuh[jmtr__xctzs]:
                    czbn__chuy = 1
            gisp__cxbws += czbn__chuy
        return gisp__cxbws == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    jmq__afoq = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    kqonb__mfoba = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    jmq__afoq = dict(level=level)
    kqonb__mfoba = dict(level=None)
    check_unsupported_args('Series.mad', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    ykm__bgi = types.float64
    vjj__jaaa = types.float64
    if S.dtype == types.float32:
        ykm__bgi = types.float32
        vjj__jaaa = types.float32
    tcp__tzqt = ykm__bgi(0)
    ost__wjj = vjj__jaaa(0)
    ogcp__pslh = vjj__jaaa(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        hmiki__csfbt = tcp__tzqt
        gisp__cxbws = ost__wjj
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(A)):
            czbn__chuy = tcp__tzqt
            sxfh__jmkh = ost__wjj
            if not bodo.libs.array_kernels.isna(A, jmtr__xctzs) or not skipna:
                czbn__chuy = A[jmtr__xctzs]
                sxfh__jmkh = ogcp__pslh
            hmiki__csfbt += czbn__chuy
            gisp__cxbws += sxfh__jmkh
        sxksm__nlnp = bodo.hiframes.series_kernels._mean_handle_nan(
            hmiki__csfbt, gisp__cxbws)
        feqi__gnov = tcp__tzqt
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(A)):
            czbn__chuy = tcp__tzqt
            if not bodo.libs.array_kernels.isna(A, jmtr__xctzs) or not skipna:
                czbn__chuy = abs(A[jmtr__xctzs] - sxksm__nlnp)
            feqi__gnov += czbn__chuy
        hgyig__onu = bodo.hiframes.series_kernels._mean_handle_nan(feqi__gnov,
            gisp__cxbws)
        return hgyig__onu
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    jmq__afoq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        qdf__zyf = 0
        emtqu__chmzo = 0
        gisp__cxbws = 0
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(A)):
            czbn__chuy = 0
            sxfh__jmkh = 0
            if not bodo.libs.array_kernels.isna(A, jmtr__xctzs) or not skipna:
                czbn__chuy = A[jmtr__xctzs]
                sxfh__jmkh = 1
            qdf__zyf += czbn__chuy
            emtqu__chmzo += czbn__chuy * czbn__chuy
            gisp__cxbws += sxfh__jmkh
        ghod__tjmd = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            qdf__zyf, emtqu__chmzo, gisp__cxbws, ddof)
        jgekb__wazi = bodo.hiframes.series_kernels._sem_handle_nan(ghod__tjmd,
            gisp__cxbws)
        return jgekb__wazi
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        qdf__zyf = 0.0
        emtqu__chmzo = 0.0
        myiyy__uqh = 0.0
        rzaa__qrd = 0.0
        gisp__cxbws = 0
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(A)):
            czbn__chuy = 0.0
            sxfh__jmkh = 0
            if not bodo.libs.array_kernels.isna(A, jmtr__xctzs) or not skipna:
                czbn__chuy = np.float64(A[jmtr__xctzs])
                sxfh__jmkh = 1
            qdf__zyf += czbn__chuy
            emtqu__chmzo += czbn__chuy ** 2
            myiyy__uqh += czbn__chuy ** 3
            rzaa__qrd += czbn__chuy ** 4
            gisp__cxbws += sxfh__jmkh
        ghod__tjmd = bodo.hiframes.series_kernels.compute_kurt(qdf__zyf,
            emtqu__chmzo, myiyy__uqh, rzaa__qrd, gisp__cxbws)
        return ghod__tjmd
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        qdf__zyf = 0.0
        emtqu__chmzo = 0.0
        myiyy__uqh = 0.0
        gisp__cxbws = 0
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(A)):
            czbn__chuy = 0.0
            sxfh__jmkh = 0
            if not bodo.libs.array_kernels.isna(A, jmtr__xctzs) or not skipna:
                czbn__chuy = np.float64(A[jmtr__xctzs])
                sxfh__jmkh = 1
            qdf__zyf += czbn__chuy
            emtqu__chmzo += czbn__chuy ** 2
            myiyy__uqh += czbn__chuy ** 3
            gisp__cxbws += sxfh__jmkh
        ghod__tjmd = bodo.hiframes.series_kernels.compute_skew(qdf__zyf,
            emtqu__chmzo, myiyy__uqh, gisp__cxbws)
        return ghod__tjmd
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        jolxr__odz = bodo.hiframes.pd_series_ext.get_series_data(S)
        wqjaf__nymuh = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        dxslo__peggi = 0
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(jolxr__odz)
            ):
            typ__ghqlg = jolxr__odz[jmtr__xctzs]
            duq__ozci = wqjaf__nymuh[jmtr__xctzs]
            dxslo__peggi += typ__ghqlg * duq__ozci
        return dxslo__peggi
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    jmq__afoq = dict(skipna=skipna)
    kqonb__mfoba = dict(skipna=True)
    check_unsupported_args('Series.cumsum', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumsum'), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    jmq__afoq = dict(skipna=skipna)
    kqonb__mfoba = dict(skipna=True)
    check_unsupported_args('Series.cumprod', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumprod'), index, name)
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    jmq__afoq = dict(skipna=skipna)
    kqonb__mfoba = dict(skipna=True)
    check_unsupported_args('Series.cummin', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummin'), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    jmq__afoq = dict(skipna=skipna)
    kqonb__mfoba = dict(skipna=True)
    check_unsupported_args('Series.cummax', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummax'), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    jmq__afoq = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    kqonb__mfoba = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        cyx__qbua = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, cyx__qbua, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    jmq__afoq = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    kqonb__mfoba = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )
    dhq__bnd = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        twhyr__yeg = bodo.utils.utils.alloc_type(n, dhq__bnd, (-1,))
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, jmtr__xctzs):
                bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                continue
            twhyr__yeg[jmtr__xctzs] = np.abs(A[jmtr__xctzs])
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    jmq__afoq = dict(level=level)
    kqonb__mfoba = dict(level=None)
    check_unsupported_args('Series.count', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    jmq__afoq = dict(method=method, min_periods=min_periods)
    kqonb__mfoba = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        vzj__beb = S.sum()
        okbyl__kjw = other.sum()
        a = n * (S * other).sum() - vzj__beb * okbyl__kjw
        pbqzf__hozh = n * (S ** 2).sum() - vzj__beb ** 2
        kslbk__ohlb = n * (other ** 2).sum() - okbyl__kjw ** 2
        return a / np.sqrt(pbqzf__hozh * kslbk__ohlb)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    jmq__afoq = dict(min_periods=min_periods)
    kqonb__mfoba = dict(min_periods=None)
    check_unsupported_args('Series.cov', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        vzj__beb = S.mean()
        okbyl__kjw = other.mean()
        bbx__hspr = ((S - vzj__beb) * (other - okbyl__kjw)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(bbx__hspr, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            scul__xfnio = np.sign(sum_val)
            return np.inf * scul__xfnio
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jmq__afoq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        ynp__fpg = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=ynp__fpg)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jmq__afoq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        ynp__fpg = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=ynp__fpg)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    jmq__afoq = dict(axis=axis, skipna=skipna)
    kqonb__mfoba = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    jmq__afoq = dict(axis=axis, skipna=skipna)
    kqonb__mfoba = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jmq__afoq = dict(level=level, numeric_only=numeric_only)
    kqonb__mfoba = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kbkr__whf = arr[:n]
        lln__aeh = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(kbkr__whf, lln__aeh,
            name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        zul__awfd = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kbkr__whf = arr[zul__awfd:]
        lln__aeh = index[zul__awfd:]
        return bodo.hiframes.pd_series_ext.init_series(kbkr__whf, lln__aeh,
            name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    ycyx__lqr = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ycyx__lqr:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            hfv__mmqxw = index[0]
            cseq__shvec = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                hfv__mmqxw, False))
        else:
            cseq__shvec = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kbkr__whf = arr[:cseq__shvec]
        lln__aeh = index[:cseq__shvec]
        return bodo.hiframes.pd_series_ext.init_series(kbkr__whf, lln__aeh,
            name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    ycyx__lqr = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ycyx__lqr:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            xho__zdk = index[-1]
            cseq__shvec = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, xho__zdk,
                True))
        else:
            cseq__shvec = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kbkr__whf = arr[len(arr) - cseq__shvec:]
        lln__aeh = index[len(arr) - cseq__shvec:]
        return bodo.hiframes.pd_series_ext.init_series(kbkr__whf, lln__aeh,
            name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        vfsk__xsl = bodo.utils.conversion.index_to_array(index)
        wlw__scznk, hcua__kieyp = (bodo.libs.array_kernels.
            first_last_valid_index(arr, vfsk__xsl))
        return hcua__kieyp if wlw__scznk else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        vfsk__xsl = bodo.utils.conversion.index_to_array(index)
        wlw__scznk, hcua__kieyp = (bodo.libs.array_kernels.
            first_last_valid_index(arr, vfsk__xsl, False))
        return hcua__kieyp if wlw__scznk else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    jmq__afoq = dict(keep=keep)
    kqonb__mfoba = dict(keep='first')
    check_unsupported_args('Series.nlargest', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        vfsk__xsl = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg, tskas__gny = bodo.libs.array_kernels.nlargest(arr,
            vfsk__xsl, n, True, bodo.hiframes.series_kernels.gt_f)
        dzy__jscs = bodo.utils.conversion.convert_to_index(tskas__gny)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    jmq__afoq = dict(keep=keep)
    kqonb__mfoba = dict(keep='first')
    check_unsupported_args('Series.nsmallest', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        vfsk__xsl = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg, tskas__gny = bodo.libs.array_kernels.nlargest(arr,
            vfsk__xsl, n, False, bodo.hiframes.series_kernels.lt_f)
        dzy__jscs = bodo.utils.conversion.convert_to_index(tskas__gny)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    jmq__afoq = dict(errors=errors)
    kqonb__mfoba = dict(errors='raise')
    check_unsupported_args('Series.astype', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    jmq__afoq = dict(axis=axis, is_copy=is_copy)
    kqonb__mfoba = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        nyh__edzd = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[nyh__edzd],
            index[nyh__edzd], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    jmq__afoq = dict(axis=axis, kind=kind, order=order)
    kqonb__mfoba = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        cynx__llb = S.notna().values
        if not cynx__llb.all():
            twhyr__yeg = np.full(n, -1, np.int64)
            twhyr__yeg[cynx__llb] = argsort(arr[cynx__llb])
        else:
            twhyr__yeg = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    jmq__afoq = dict(axis=axis, numeric_only=numeric_only)
    kqonb__mfoba = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_str(method):
        raise BodoError(
            "Series.rank(): 'method' argument must be a constant string")
    if not is_overload_constant_str(na_option):
        raise BodoError(
            "Series.rank(): 'na_option' argument must be a constant string")

    def impl(S, axis=0, method='average', numeric_only=None, na_option=
        'keep', ascending=True, pct=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    jmq__afoq = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    kqonb__mfoba = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    oory__wti = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        csepc__ztidm = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, oory__wti)
        ejj__hnh = csepc__ztidm.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        twhyr__yeg = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(ejj__hnh
            , 0)
        dzy__jscs = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(ejj__hnh
            )
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    jmq__afoq = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    kqonb__mfoba = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    xvq__isyj = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        csepc__ztidm = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, xvq__isyj)
        ejj__hnh = csepc__ztidm.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        twhyr__yeg = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(ejj__hnh
            , 0)
        dzy__jscs = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(ejj__hnh
            )
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    yhd__npsn = is_overload_true(is_nullable)
    qkop__hhv = 'def impl(bins, arr, is_nullable=True, include_lowest=True):\n'
    qkop__hhv += '  numba.parfors.parfor.init_prange()\n'
    qkop__hhv += '  n = len(arr)\n'
    if yhd__npsn:
        qkop__hhv += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        qkop__hhv += '  out_arr = np.empty(n, np.int64)\n'
    qkop__hhv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    qkop__hhv += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if yhd__npsn:
        qkop__hhv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        qkop__hhv += '      out_arr[i] = -1\n'
    qkop__hhv += '      continue\n'
    qkop__hhv += '    val = arr[i]\n'
    qkop__hhv += '    if include_lowest and val == bins[0]:\n'
    qkop__hhv += '      ind = 1\n'
    qkop__hhv += '    else:\n'
    qkop__hhv += '      ind = np.searchsorted(bins, val)\n'
    qkop__hhv += '    if ind == 0 or ind == len(bins):\n'
    if yhd__npsn:
        qkop__hhv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        qkop__hhv += '      out_arr[i] = -1\n'
    qkop__hhv += '    else:\n'
    qkop__hhv += '      out_arr[i] = ind - 1\n'
    qkop__hhv += '  return out_arr\n'
    onob__eiui = {}
    exec(qkop__hhv, {'bodo': bodo, 'np': np, 'numba': numba}, onob__eiui)
    impl = onob__eiui['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        vdlp__yxwfg, gmxa__vqddg = np.divmod(x, 1)
        if vdlp__yxwfg == 0:
            cajz__qvz = -int(np.floor(np.log10(abs(gmxa__vqddg)))
                ) - 1 + precision
        else:
            cajz__qvz = precision
        return np.around(x, cajz__qvz)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        guwfr__vpxm = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(guwfr__vpxm)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        ulyr__qlbby = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            loown__ywpov = bins.copy()
            if right and include_lowest:
                loown__ywpov[0] = loown__ywpov[0] - ulyr__qlbby
            xvml__glj = bodo.libs.interval_arr_ext.init_interval_array(
                loown__ywpov[:-1], loown__ywpov[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(xvml__glj,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        loown__ywpov = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            loown__ywpov[0] = loown__ywpov[0] - 10.0 ** -precision
        xvml__glj = bodo.libs.interval_arr_ext.init_interval_array(loown__ywpov
            [:-1], loown__ywpov[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(xvml__glj, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        xhrk__pxoxs = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        awx__ujy = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        twhyr__yeg = np.zeros(nbins, np.int64)
        for jmtr__xctzs in range(len(xhrk__pxoxs)):
            twhyr__yeg[awx__ujy[jmtr__xctzs]] = xhrk__pxoxs[jmtr__xctzs]
        return twhyr__yeg
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            torg__ecsv = (max_val - min_val) * 0.001
            if right:
                bins[0] -= torg__ecsv
            else:
                bins[-1] += torg__ecsv
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    jmq__afoq = dict(dropna=dropna)
    kqonb__mfoba = dict(dropna=True)
    check_unsupported_args('Series.value_counts', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    djafw__skq = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    qkop__hhv = 'def impl(\n'
    qkop__hhv += '    S,\n'
    qkop__hhv += '    normalize=False,\n'
    qkop__hhv += '    sort=True,\n'
    qkop__hhv += '    ascending=False,\n'
    qkop__hhv += '    bins=None,\n'
    qkop__hhv += '    dropna=True,\n'
    qkop__hhv += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    qkop__hhv += '):\n'
    qkop__hhv += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    qkop__hhv += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    qkop__hhv += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if djafw__skq:
        qkop__hhv += '    right = True\n'
        qkop__hhv += _gen_bins_handling(bins, S.dtype)
        qkop__hhv += '    arr = get_bin_inds(bins, arr)\n'
    qkop__hhv += '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n'
    qkop__hhv += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    qkop__hhv += '    )\n'
    qkop__hhv += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if djafw__skq:
        qkop__hhv += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        qkop__hhv += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        qkop__hhv += '    index = get_bin_labels(bins)\n'
    else:
        qkop__hhv += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        qkop__hhv += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        qkop__hhv += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        qkop__hhv += '    )\n'
        qkop__hhv += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    qkop__hhv += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        qkop__hhv += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        hsuhu__ydq = 'len(S)' if djafw__skq else 'count_arr.sum()'
        qkop__hhv += f'    res = res / float({hsuhu__ydq})\n'
    qkop__hhv += '    return res\n'
    onob__eiui = {}
    exec(qkop__hhv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, onob__eiui)
    impl = onob__eiui['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    qkop__hhv = ''
    if isinstance(bins, types.Integer):
        qkop__hhv += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        qkop__hhv += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            qkop__hhv += '    min_val = min_val.value\n'
            qkop__hhv += '    max_val = max_val.value\n'
        qkop__hhv += '    bins = compute_bins(bins, min_val, max_val, right)\n'
        if dtype == bodo.datetime64ns:
            qkop__hhv += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        qkop__hhv += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return qkop__hhv


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    jmq__afoq = dict(right=right, labels=labels, retbins=retbins, precision
        =precision, duplicates=duplicates, ordered=ordered)
    kqonb__mfoba = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    qkop__hhv = 'def impl(\n'
    qkop__hhv += '    x,\n'
    qkop__hhv += '    bins,\n'
    qkop__hhv += '    right=True,\n'
    qkop__hhv += '    labels=None,\n'
    qkop__hhv += '    retbins=False,\n'
    qkop__hhv += '    precision=3,\n'
    qkop__hhv += '    include_lowest=False,\n'
    qkop__hhv += "    duplicates='raise',\n"
    qkop__hhv += '    ordered=True\n'
    qkop__hhv += '):\n'
    if isinstance(x, SeriesType):
        qkop__hhv += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        qkop__hhv += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        qkop__hhv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        qkop__hhv += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    qkop__hhv += _gen_bins_handling(bins, x.dtype)
    qkop__hhv += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    qkop__hhv += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    qkop__hhv += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    qkop__hhv += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        qkop__hhv += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        qkop__hhv += '    return res\n'
    else:
        qkop__hhv += '    return out_arr\n'
    onob__eiui = {}
    exec(qkop__hhv, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, onob__eiui)
    impl = onob__eiui['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    jmq__afoq = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    kqonb__mfoba = dict(labels=None, retbins=False, precision=3, duplicates
        ='raise')
    check_unsupported_args('pandas.qcut', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        umyd__gwenv = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, umyd__gwenv)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    jmq__afoq = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    kqonb__mfoba = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )
        qtswy__esxpj = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            urwbn__rxitq = bodo.utils.conversion.coerce_to_array(index)
            csepc__ztidm = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                urwbn__rxitq, arr), index, qtswy__esxpj)
            return csepc__ztidm.groupby(' ')['']
        return impl_index
    kcx__zxehq = by
    if isinstance(by, SeriesType):
        kcx__zxehq = by.data
    if isinstance(kcx__zxehq, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    qbke__jhkw = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        urwbn__rxitq = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        csepc__ztidm = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            urwbn__rxitq, arr), index, qbke__jhkw)
        return csepc__ztidm.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    jmq__afoq = dict(verify_integrity=verify_integrity)
    kqonb__mfoba = dict(verify_integrity=False)
    check_unsupported_args('Series.append', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            qmuyk__bxnvb = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            twhyr__yeg = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(twhyr__yeg, A, qmuyk__bxnvb, False)
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    jmq__afoq = dict(interpolation=interpolation)
    kqonb__mfoba = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            twhyr__yeg = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        jhkmg__qgwzv = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(jhkmg__qgwzv, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    jmq__afoq = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    kqonb__mfoba = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, (IntegerArrayType, FloatingArrayType)):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        nzgke__frlkc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        nzgke__frlkc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    qkop__hhv = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {nzgke__frlkc}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    qhrem__ycv = dict()
    exec(qkop__hhv, {'bodo': bodo, 'numba': numba}, qhrem__ycv)
    qxlvy__ccsg = qhrem__ycv['impl']
    return qxlvy__ccsg


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        nzgke__frlkc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        nzgke__frlkc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    qkop__hhv = 'def impl(S,\n'
    qkop__hhv += '     value=None,\n'
    qkop__hhv += '    method=None,\n'
    qkop__hhv += '    axis=None,\n'
    qkop__hhv += '    inplace=False,\n'
    qkop__hhv += '    limit=None,\n'
    qkop__hhv += '   downcast=None,\n'
    qkop__hhv += '):\n'
    qkop__hhv += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    qkop__hhv += '    n = len(in_arr)\n'
    qkop__hhv += f'    out_arr = {nzgke__frlkc}(n, -1)\n'
    qkop__hhv += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    qkop__hhv += '        s = in_arr[j]\n'
    qkop__hhv += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    qkop__hhv += '            s = value\n'
    qkop__hhv += '        out_arr[j] = s\n'
    qkop__hhv += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    qhrem__ycv = dict()
    exec(qkop__hhv, {'bodo': bodo, 'numba': numba}, qhrem__ycv)
    qxlvy__ccsg = qhrem__ycv['impl']
    return qxlvy__ccsg


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
    zkvsr__tlsgu = bodo.hiframes.pd_series_ext.get_series_data(value)
    for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(bcygi__brot)):
        s = bcygi__brot[jmtr__xctzs]
        if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs
            ) and not bodo.libs.array_kernels.isna(zkvsr__tlsgu, jmtr__xctzs):
            s = zkvsr__tlsgu[jmtr__xctzs]
        bcygi__brot[jmtr__xctzs] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
    for jmtr__xctzs in numba.parfors.parfor.internal_prange(len(bcygi__brot)):
        s = bcygi__brot[jmtr__xctzs]
        if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs):
            s = value
        bcygi__brot[jmtr__xctzs] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    zkvsr__tlsgu = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(bcygi__brot)
    twhyr__yeg = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for aqd__vxn in numba.parfors.parfor.internal_prange(n):
        s = bcygi__brot[aqd__vxn]
        if bodo.libs.array_kernels.isna(bcygi__brot, aqd__vxn
            ) and not bodo.libs.array_kernels.isna(zkvsr__tlsgu, aqd__vxn):
            s = zkvsr__tlsgu[aqd__vxn]
        twhyr__yeg[aqd__vxn] = s
        if bodo.libs.array_kernels.isna(bcygi__brot, aqd__vxn
            ) and bodo.libs.array_kernels.isna(zkvsr__tlsgu, aqd__vxn):
            bodo.libs.array_kernels.setna(twhyr__yeg, aqd__vxn)
    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    zkvsr__tlsgu = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(bcygi__brot)
    twhyr__yeg = bodo.utils.utils.alloc_type(n, bcygi__brot.dtype, (-1,))
    for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
        s = bcygi__brot[jmtr__xctzs]
        if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs
            ) and not bodo.libs.array_kernels.isna(zkvsr__tlsgu, jmtr__xctzs):
            s = zkvsr__tlsgu[jmtr__xctzs]
        twhyr__yeg[jmtr__xctzs] = s
    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    jmq__afoq = dict(limit=limit, downcast=downcast)
    kqonb__mfoba = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    tux__iyma = not is_overload_none(value)
    lwp__hbys = not is_overload_none(method)
    if tux__iyma and lwp__hbys:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not tux__iyma and not lwp__hbys:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if lwp__hbys:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        ddi__fcw = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(ddi__fcw)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(ddi__fcw)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    ptuk__cobid = element_type(S.data)
    uzeuf__yalgn = None
    if tux__iyma:
        uzeuf__yalgn = element_type(types.unliteral(value))
    if uzeuf__yalgn and not can_replace(ptuk__cobid, uzeuf__yalgn):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {uzeuf__yalgn} with series type {ptuk__cobid}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        ryucq__ipnby = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                zkvsr__tlsgu = bodo.hiframes.pd_series_ext.get_series_data(
                    value)
                n = len(bcygi__brot)
                twhyr__yeg = bodo.utils.utils.alloc_type(n, ryucq__ipnby, (-1,)
                    )
                for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs
                        ) and bodo.libs.array_kernels.isna(zkvsr__tlsgu,
                        jmtr__xctzs):
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                        continue
                    if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs):
                        twhyr__yeg[jmtr__xctzs
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            zkvsr__tlsgu[jmtr__xctzs])
                        continue
                    twhyr__yeg[jmtr__xctzs
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        bcygi__brot[jmtr__xctzs])
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return fillna_series_impl
        if lwp__hbys:
            hdcnx__qpnps = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(ptuk__cobid, (types.Integer, types.Float)
                ) and ptuk__cobid not in hdcnx__qpnps:
                raise BodoError(
                    f"Series.fillna(): series of type {ptuk__cobid} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                twhyr__yeg = bodo.libs.array_kernels.ffill_bfill_arr(
                    bcygi__brot, method)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(bcygi__brot)
            twhyr__yeg = bodo.utils.utils.alloc_type(n, ryucq__ipnby, (-1,))
            for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    bcygi__brot[jmtr__xctzs])
                if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs):
                    s = value
                twhyr__yeg[jmtr__xctzs] = s
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        ltdsw__amp = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        jmq__afoq = dict(limit=limit, downcast=downcast)
        kqonb__mfoba = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', jmq__afoq,
            kqonb__mfoba, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        ptuk__cobid = element_type(S.data)
        hdcnx__qpnps = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(ptuk__cobid, (types.Integer, types.Float)
            ) and ptuk__cobid not in hdcnx__qpnps:
            raise BodoError(
                f'Series.{overload_name}(): series of type {ptuk__cobid} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            twhyr__yeg = bodo.libs.array_kernels.ffill_bfill_arr(bcygi__brot,
                ltdsw__amp)
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        sbf__nixxc = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            sbf__nixxc)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        lfbz__uascp = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(lfbz__uascp)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        lfbz__uascp = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(lfbz__uascp)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        lfbz__uascp = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(lfbz__uascp)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    jmq__afoq = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    yazrp__pxe = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', jmq__afoq, yazrp__pxe,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    ptuk__cobid = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        qxwnm__tslo = element_type(to_replace.key_type)
        uzeuf__yalgn = element_type(to_replace.value_type)
    else:
        qxwnm__tslo = element_type(to_replace)
        uzeuf__yalgn = element_type(value)
    oup__bxlob = None
    if ptuk__cobid != types.unliteral(qxwnm__tslo):
        if bodo.utils.typing.equality_always_false(ptuk__cobid, types.
            unliteral(qxwnm__tslo)
            ) or not bodo.utils.typing.types_equality_exists(ptuk__cobid,
            qxwnm__tslo):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(ptuk__cobid, (types.Float, types.Integer)
            ) or ptuk__cobid == np.bool_:
            oup__bxlob = ptuk__cobid
    if not can_replace(ptuk__cobid, types.unliteral(uzeuf__yalgn)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    pfpvt__oxquq = to_str_arr_if_dict_array(S.data)
    if isinstance(pfpvt__oxquq, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bcygi__brot.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(bcygi__brot)
        twhyr__yeg = bodo.utils.utils.alloc_type(n, pfpvt__oxquq, (-1,))
        cpw__gcyxd = build_replace_dict(to_replace, value, oup__bxlob)
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(bcygi__brot, jmtr__xctzs):
                bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                continue
            s = bcygi__brot[jmtr__xctzs]
            if s in cpw__gcyxd:
                s = cpw__gcyxd[s]
            twhyr__yeg[jmtr__xctzs] = s
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    iikbk__obj = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    oftk__nenff = is_iterable_type(to_replace)
    fiuf__nhn = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    hhep__zzyud = is_iterable_type(value)
    if iikbk__obj and fiuf__nhn:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                cpw__gcyxd = {}
                cpw__gcyxd[key_dtype_conv(to_replace)] = value
                return cpw__gcyxd
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            cpw__gcyxd = {}
            cpw__gcyxd[to_replace] = value
            return cpw__gcyxd
        return impl
    if oftk__nenff and fiuf__nhn:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                cpw__gcyxd = {}
                for ipcj__zdpd in to_replace:
                    cpw__gcyxd[key_dtype_conv(ipcj__zdpd)] = value
                return cpw__gcyxd
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            cpw__gcyxd = {}
            for ipcj__zdpd in to_replace:
                cpw__gcyxd[ipcj__zdpd] = value
            return cpw__gcyxd
        return impl
    if oftk__nenff and hhep__zzyud:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                cpw__gcyxd = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for jmtr__xctzs in range(len(to_replace)):
                    cpw__gcyxd[key_dtype_conv(to_replace[jmtr__xctzs])
                        ] = value[jmtr__xctzs]
                return cpw__gcyxd
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            cpw__gcyxd = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for jmtr__xctzs in range(len(to_replace)):
                cpw__gcyxd[to_replace[jmtr__xctzs]] = value[jmtr__xctzs]
            return cpw__gcyxd
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            twhyr__yeg = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    jmq__afoq = dict(ignore_index=ignore_index)
    wrrht__cwk = dict(ignore_index=False)
    check_unsupported_args('Series.explode', jmq__afoq, wrrht__cwk,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        vfsk__xsl = bodo.utils.conversion.index_to_array(index)
        twhyr__yeg, zvswb__tifa = bodo.libs.array_kernels.explode(arr,
            vfsk__xsl)
        dzy__jscs = bodo.utils.conversion.index_from_array(zvswb__tifa)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            ohug__cgka = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                ohug__cgka[jmtr__xctzs] = np.argmax(a[jmtr__xctzs])
            return ohug__cgka
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            vtmwu__nht = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                vtmwu__nht[jmtr__xctzs] = np.argmin(a[jmtr__xctzs])
            return vtmwu__nht
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            yqfwy__vhsr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo
                .hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, yqfwy__vhsr)
        return impl
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            b = bodo.utils.conversion.ndarray_if_nullable_arr(b)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            a = bodo.utils.conversion.ndarray_if_nullable_arr(a)
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    jmq__afoq = dict(axis=axis, inplace=inplace, how=how)
    awtmm__eec = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', jmq__afoq, awtmm__eec,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            cynx__llb = S.notna().values
            vfsk__xsl = bodo.utils.conversion.extract_index_array(S)
            dzy__jscs = bodo.utils.conversion.convert_to_index(vfsk__xsl[
                cynx__llb])
            twhyr__yeg = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(bcygi__brot))
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                dzy__jscs, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            vfsk__xsl = bodo.utils.conversion.extract_index_array(S)
            cynx__llb = S.notna().values
            dzy__jscs = bodo.utils.conversion.convert_to_index(vfsk__xsl[
                cynx__llb])
            twhyr__yeg = bcygi__brot[cynx__llb]
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                dzy__jscs, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    jmq__afoq = dict(freq=freq, axis=axis)
    kqonb__mfoba = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.hiframes.rolling.shift(arr, periods, False,
            fill_value)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    jmq__afoq = dict(fill_method=fill_method, limit=limit, freq=freq)
    kqonb__mfoba = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', 'Series', S,
            cond, other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            fwt__rre = 'None'
        else:
            fwt__rre = 'other'
        qkop__hhv = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            qkop__hhv += '  cond = ~cond\n'
        qkop__hhv += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        qkop__hhv += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        qkop__hhv += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        qkop__hhv += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {fwt__rre})\n'
            )
        qkop__hhv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        onob__eiui = {}
        exec(qkop__hhv, {'bodo': bodo, 'np': np}, onob__eiui)
        impl = onob__eiui['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        sbf__nixxc = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(sbf__nixxc)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    jmq__afoq = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    kqonb__mfoba = dict(inplace=False, level=None, errors='raise', try_cast
        =False)
    check_unsupported_args(f'{func_name}', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name=module_name)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(S, bodo.hiframes.pd_index_ext.RangeIndexType):
        arr = types.Array(types.int64, 1, 'C')
    else:
        arr = S.data
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, module_name, arr, other.data
            )
    else:
        _validate_self_other_mask_where(func_name, module_name, arr, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, module_name, arr, other,
    max_ndim=1, is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or
        isinstance(arr, FloatingArrayType) or bodo.utils.utils.is_array_typ
        (arr, False) and arr.dtype in [bodo.string_type, bodo.bytes_type] or
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type
         not in [bodo.datetime64ns, bodo.timedelta64ns, bodo.
        pd_timestamp_tz_naive_type, bodo.pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() {module_name} data with type {arr} not yet supported'
            )
    hyoj__jtykp = is_overload_constant_nan(other)
    if not (is_default or hyoj__jtykp or is_scalar_type(other) or 
        isinstance(other, types.Array) and other.ndim >= 1 and other.ndim <=
        max_ndim or isinstance(other, SeriesType) and (isinstance(arr,
        types.Array) or arr.dtype in [bodo.string_type, bodo.bytes_type]) or
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, (IntegerArrayType, FloatingArrayType)))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for {module_name}."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            gdd__bjg = arr.dtype.elem_type
        else:
            gdd__bjg = arr.dtype
        if is_iterable_type(other):
            sngw__fnfpw = other.dtype
        elif hyoj__jtykp:
            sngw__fnfpw = types.float64
        else:
            sngw__fnfpw = types.unliteral(other)
        if not hyoj__jtykp and not is_common_scalar_dtype([gdd__bjg,
            sngw__fnfpw]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        jmq__afoq = dict(level=level, axis=axis)
        kqonb__mfoba = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), jmq__afoq,
            kqonb__mfoba, package_name='pandas', module_name='Series')
        yrxdy__fucyv = other == string_type or is_overload_constant_str(other)
        kicg__lzg = is_iterable_type(other) and other.dtype == string_type
        xagd__nmvmo = S.dtype == string_type and (op == operator.add and (
            yrxdy__fucyv or kicg__lzg) or op == operator.mul and isinstance
            (other, types.Integer))
        zul__jvjui = S.dtype == bodo.timedelta64ns
        kgxj__mjq = S.dtype == bodo.datetime64ns
        qvov__btiak = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        ajnty__lwn = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        jzy__xah = zul__jvjui and (qvov__btiak or ajnty__lwn
            ) or kgxj__mjq and qvov__btiak
        jzy__xah = jzy__xah and op == operator.add
        if not (isinstance(S.dtype, types.Number) or xagd__nmvmo or jzy__xah):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        wivea__jgdyu = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            pfpvt__oxquq = wivea__jgdyu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and pfpvt__oxquq == types.Array(types.bool_, 1, 'C'):
                pfpvt__oxquq = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                twhyr__yeg = bodo.utils.utils.alloc_type(n, pfpvt__oxquq, (-1,)
                    )
                for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                    abm__voklj = bodo.libs.array_kernels.isna(arr, jmtr__xctzs)
                    if abm__voklj:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(twhyr__yeg,
                                jmtr__xctzs)
                        else:
                            twhyr__yeg[jmtr__xctzs] = op(fill_value, other)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(arr[jmtr__xctzs], other)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        pfpvt__oxquq = wivea__jgdyu.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and pfpvt__oxquq == types.Array(types.bool_, 1, 'C'):
            pfpvt__oxquq = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bhty__yea = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            twhyr__yeg = bodo.utils.utils.alloc_type(n, pfpvt__oxquq, (-1,))
            for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                abm__voklj = bodo.libs.array_kernels.isna(arr, jmtr__xctzs)
                krlb__kqpr = bodo.libs.array_kernels.isna(bhty__yea,
                    jmtr__xctzs)
                if abm__voklj and krlb__kqpr:
                    bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                elif abm__voklj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(fill_value, bhty__yea[
                            jmtr__xctzs])
                elif krlb__kqpr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(arr[jmtr__xctzs],
                            fill_value)
                else:
                    twhyr__yeg[jmtr__xctzs] = op(arr[jmtr__xctzs],
                        bhty__yea[jmtr__xctzs])
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        wivea__jgdyu = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            pfpvt__oxquq = wivea__jgdyu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and pfpvt__oxquq == types.Array(types.bool_, 1, 'C'):
                pfpvt__oxquq = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                twhyr__yeg = bodo.utils.utils.alloc_type(n, pfpvt__oxquq, None)
                for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                    abm__voklj = bodo.libs.array_kernels.isna(arr, jmtr__xctzs)
                    if abm__voklj:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(twhyr__yeg,
                                jmtr__xctzs)
                        else:
                            twhyr__yeg[jmtr__xctzs] = op(other, fill_value)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(other, arr[jmtr__xctzs])
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        pfpvt__oxquq = wivea__jgdyu.resolve_function_type(op, args, {}
            ).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and pfpvt__oxquq == types.Array(types.bool_, 1, 'C'):
            pfpvt__oxquq = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            bhty__yea = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            twhyr__yeg = bodo.utils.utils.alloc_type(n, pfpvt__oxquq, None)
            for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                abm__voklj = bodo.libs.array_kernels.isna(arr, jmtr__xctzs)
                krlb__kqpr = bodo.libs.array_kernels.isna(bhty__yea,
                    jmtr__xctzs)
                twhyr__yeg[jmtr__xctzs] = op(bhty__yea[jmtr__xctzs], arr[
                    jmtr__xctzs])
                if abm__voklj and krlb__kqpr:
                    bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                elif abm__voklj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(bhty__yea[jmtr__xctzs],
                            fill_value)
                elif krlb__kqpr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                    else:
                        twhyr__yeg[jmtr__xctzs] = op(fill_value, arr[
                            jmtr__xctzs])
                else:
                    twhyr__yeg[jmtr__xctzs] = op(bhty__yea[jmtr__xctzs],
                        arr[jmtr__xctzs])
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, nabs__qkfpv in explicit_binop_funcs_two_ways.items():
        for name in nabs__qkfpv:
            sbf__nixxc = create_explicit_binary_op_overload(op)
            grip__lnoia = create_explicit_binary_reverse_op_overload(op)
            isysg__mry = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(sbf__nixxc)
            overload_method(SeriesType, isysg__mry, no_unliteral=True)(
                grip__lnoia)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        sbf__nixxc = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(sbf__nixxc)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xjcj__ostn = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                twhyr__yeg = dt64_arr_sub(arr, xjcj__ostn)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                twhyr__yeg = np.empty(n, np.dtype('datetime64[ns]'))
                for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, jmtr__xctzs):
                        bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                        continue
                    sjkc__mzj = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[jmtr__xctzs]))
                    gbrg__uwt = op(sjkc__mzj, rhs)
                    twhyr__yeg[jmtr__xctzs
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gbrg__uwt.value)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    xjcj__ostn = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    twhyr__yeg = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(xjcj__ostn))
                    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xjcj__ostn = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                twhyr__yeg = op(arr, xjcj__ostn)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    uun__vuw = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    twhyr__yeg = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(uun__vuw), arr)
                    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                uun__vuw = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                twhyr__yeg = op(uun__vuw, arr)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        sbf__nixxc = create_binary_op_overload(op)
        overload(op)(sbf__nixxc)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    rhtal__vjc = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, rhtal__vjc)
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, jmtr__xctzs
                ) or bodo.libs.array_kernels.isna(arg2, jmtr__xctzs):
                bodo.libs.array_kernels.setna(S, jmtr__xctzs)
                continue
            S[jmtr__xctzs
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                jmtr__xctzs]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[jmtr__xctzs]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                bhty__yea = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, bhty__yea)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        sbf__nixxc = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(sbf__nixxc)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                twhyr__yeg = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        sbf__nixxc = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(sbf__nixxc)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    twhyr__yeg = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    bhty__yea = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    twhyr__yeg = ufunc(arr, bhty__yea)
                    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    bhty__yea = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    twhyr__yeg = ufunc(arr, bhty__yea)
                    return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        sbf__nixxc = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(sbf__nixxc)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        dzua__muga = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),)
            )
        tekjn__eem = np.arange(n),
        bodo.libs.timsort.sort(dzua__muga, 0, n, tekjn__eem)
        return tekjn__eem[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        iwhs__ofdar = get_overload_const_str(downcast)
        if iwhs__ofdar in ('integer', 'signed'):
            out_dtype = types.int64
        elif iwhs__ofdar == 'unsigned':
            out_dtype = types.uint64
        else:
            assert iwhs__ofdar == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            bcygi__brot = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            twhyr__yeg = pd.to_numeric(bcygi__brot, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    nwjf__hqlgz = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        jdmz__vak = bodo.utils.utils.alloc_type(n, nwjf__hqlgz, (-1,))
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, jmtr__xctzs):
                bodo.libs.array_kernels.setna(jdmz__vak, jmtr__xctzs)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(jdmz__vak,
                    jmtr__xctzs, arg_a, jmtr__xctzs)
        return jdmz__vak
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        eudpu__okue = if_series_to_array_type(args[0])
        if isinstance(eudpu__okue, types.Array) and isinstance(eudpu__okue.
            dtype, types.Integer):
            eudpu__okue = types.Array(types.float64, 1, 'C')
        return eudpu__okue(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    cgop__tln = bodo.utils.utils.is_array_typ(x, True)
    galre__milxm = bodo.utils.utils.is_array_typ(y, True)
    qkop__hhv = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        qkop__hhv += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if cgop__tln and not bodo.utils.utils.is_array_typ(x, False):
        qkop__hhv += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if galre__milxm and not bodo.utils.utils.is_array_typ(y, False):
        qkop__hhv += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    qkop__hhv += '  n = len(condition)\n'
    lkkg__tnl = x.dtype if cgop__tln else types.unliteral(x)
    wfbn__ccfq = y.dtype if galre__milxm else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        lkkg__tnl = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        wfbn__ccfq = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    axhe__rodkp = get_data(x)
    hohn__amf = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(tekjn__eem) for
        tekjn__eem in [axhe__rodkp, hohn__amf])
    if hohn__amf == types.none:
        if isinstance(lkkg__tnl, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif axhe__rodkp == hohn__amf and not is_nullable:
        out_dtype = dtype_to_array_type(lkkg__tnl)
    elif lkkg__tnl == string_type or wfbn__ccfq == string_type:
        out_dtype = bodo.string_array_type
    elif axhe__rodkp == bytes_type or (cgop__tln and lkkg__tnl == bytes_type
        ) and (hohn__amf == bytes_type or galre__milxm and wfbn__ccfq ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(lkkg__tnl, bodo.PDCategoricalDtype):
        out_dtype = None
    elif lkkg__tnl in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(lkkg__tnl, 1, 'C')
    elif wfbn__ccfq in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(wfbn__ccfq, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(lkkg__tnl), numba.np.numpy_support.
            as_dtype(wfbn__ccfq)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(lkkg__tnl, bodo.PDCategoricalDtype):
        hexnh__sbfnj = 'x'
    else:
        hexnh__sbfnj = 'out_dtype'
    qkop__hhv += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {hexnh__sbfnj}, (-1,))\n')
    if isinstance(lkkg__tnl, bodo.PDCategoricalDtype):
        qkop__hhv += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        qkop__hhv += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    qkop__hhv += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    qkop__hhv += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if cgop__tln:
        qkop__hhv += '      if bodo.libs.array_kernels.isna(x, j):\n'
        qkop__hhv += '        setna(out_arr, j)\n'
        qkop__hhv += '        continue\n'
    if isinstance(lkkg__tnl, bodo.PDCategoricalDtype):
        qkop__hhv += '      out_codes[j] = x_codes[j]\n'
    else:
        qkop__hhv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if cgop__tln else 'x'))
    qkop__hhv += '    else:\n'
    if galre__milxm:
        qkop__hhv += '      if bodo.libs.array_kernels.isna(y, j):\n'
        qkop__hhv += '        setna(out_arr, j)\n'
        qkop__hhv += '        continue\n'
    if hohn__amf == types.none:
        if isinstance(lkkg__tnl, bodo.PDCategoricalDtype):
            qkop__hhv += '      out_codes[j] = -1\n'
        else:
            qkop__hhv += '      setna(out_arr, j)\n'
    else:
        qkop__hhv += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if galre__milxm else 'y'))
    qkop__hhv += '  return out_arr\n'
    onob__eiui = {}
    exec(qkop__hhv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, onob__eiui)
    wevs__kqzwe = onob__eiui['_impl']
    return wevs__kqzwe


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        briv__ohtzm = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(briv__ohtzm, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(briv__ohtzm):
            rytje__qen = briv__ohtzm.data.dtype
        else:
            rytje__qen = briv__ohtzm.dtype
        if isinstance(rytje__qen, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        xqxi__ljmue = briv__ohtzm
    else:
        xqy__lzr = []
        for briv__ohtzm in choicelist:
            if not bodo.utils.utils.is_array_typ(briv__ohtzm, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(briv__ohtzm):
                rytje__qen = briv__ohtzm.data.dtype
            else:
                rytje__qen = briv__ohtzm.dtype
            if isinstance(rytje__qen, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            xqy__lzr.append(rytje__qen)
        if not is_common_scalar_dtype(xqy__lzr):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        xqxi__ljmue = choicelist[0]
    if is_series_type(xqxi__ljmue):
        xqxi__ljmue = xqxi__ljmue.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, xqxi__ljmue.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(xqxi__ljmue, types.Array) or isinstance(xqxi__ljmue,
        BooleanArrayType) or isinstance(xqxi__ljmue, IntegerArrayType) or
        isinstance(xqxi__ljmue, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(xqxi__ljmue, False) and xqxi__ljmue.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {xqxi__ljmue} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    ieenz__dufve = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        isiwg__wfo = choicelist.dtype
    else:
        ylk__fgzwv = False
        xqy__lzr = []
        for briv__ohtzm in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                briv__ohtzm, 'numpy.select()')
            if is_nullable_type(briv__ohtzm):
                ylk__fgzwv = True
            if is_series_type(briv__ohtzm):
                rytje__qen = briv__ohtzm.data.dtype
            else:
                rytje__qen = briv__ohtzm.dtype
            if isinstance(rytje__qen, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            xqy__lzr.append(rytje__qen)
        uikrg__mhi, rpqk__hrj = get_common_scalar_dtype(xqy__lzr)
        if not rpqk__hrj:
            raise BodoError('Internal error in overload_np_select')
        uts__jlvy = dtype_to_array_type(uikrg__mhi)
        if ylk__fgzwv:
            uts__jlvy = to_nullable_type(uts__jlvy)
        isiwg__wfo = uts__jlvy
    if isinstance(isiwg__wfo, SeriesType):
        isiwg__wfo = isiwg__wfo.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        wjmg__nkyf = True
    else:
        wjmg__nkyf = False
    dvfw__coag = False
    jjxp__xzkox = False
    if wjmg__nkyf:
        if isinstance(isiwg__wfo.dtype, types.Number):
            pass
        elif isiwg__wfo.dtype == types.bool_:
            jjxp__xzkox = True
        else:
            dvfw__coag = True
            isiwg__wfo = to_nullable_type(isiwg__wfo)
    elif default == types.none or is_overload_constant_nan(default):
        dvfw__coag = True
        isiwg__wfo = to_nullable_type(isiwg__wfo)
    qkop__hhv = 'def np_select_impl(condlist, choicelist, default=0):\n'
    qkop__hhv += '  if len(condlist) != len(choicelist):\n'
    qkop__hhv += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    qkop__hhv += '  output_len = len(choicelist[0])\n'
    qkop__hhv += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    qkop__hhv += '  for i in range(output_len):\n'
    if dvfw__coag:
        qkop__hhv += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif jjxp__xzkox:
        qkop__hhv += '    out[i] = False\n'
    else:
        qkop__hhv += '    out[i] = default\n'
    if ieenz__dufve:
        qkop__hhv += '  for i in range(len(condlist) - 1, -1, -1):\n'
        qkop__hhv += '    cond = condlist[i]\n'
        qkop__hhv += '    choice = choicelist[i]\n'
        qkop__hhv += '    out = np.where(cond, choice, out)\n'
    else:
        for jmtr__xctzs in range(len(choicelist) - 1, -1, -1):
            qkop__hhv += f'  cond = condlist[{jmtr__xctzs}]\n'
            qkop__hhv += f'  choice = choicelist[{jmtr__xctzs}]\n'
            qkop__hhv += f'  out = np.where(cond, choice, out)\n'
    qkop__hhv += '  return out'
    onob__eiui = dict()
    exec(qkop__hhv, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': isiwg__wfo}, onob__eiui)
    impl = onob__eiui['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        twhyr__yeg = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    jmq__afoq = dict(subset=subset, keep=keep, inplace=inplace)
    kqonb__mfoba = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', jmq__afoq,
        kqonb__mfoba, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        oful__rlzhb = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (oful__rlzhb,), vfsk__xsl = bodo.libs.array_kernels.drop_duplicates((
            oful__rlzhb,), index, 1)
        index = bodo.utils.conversion.index_from_array(vfsk__xsl)
        return bodo.hiframes.pd_series_ext.init_series(oful__rlzhb, index, name
            )
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    puje__gmc = element_type(S.data)
    if not is_common_scalar_dtype([puje__gmc, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([puje__gmc, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        twhyr__yeg = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for jmtr__xctzs in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, jmtr__xctzs):
                bodo.libs.array_kernels.setna(twhyr__yeg, jmtr__xctzs)
                continue
            czbn__chuy = bodo.utils.conversion.box_if_dt64(arr[jmtr__xctzs])
            if inclusive == 'both':
                twhyr__yeg[jmtr__xctzs
                    ] = czbn__chuy <= right and czbn__chuy >= left
            else:
                twhyr__yeg[jmtr__xctzs
                    ] = czbn__chuy < right and czbn__chuy > left
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    jmq__afoq = dict(axis=axis)
    kqonb__mfoba = dict(axis=None)
    check_unsupported_args('Series.repeat', jmq__afoq, kqonb__mfoba,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            vfsk__xsl = bodo.utils.conversion.index_to_array(index)
            twhyr__yeg = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            zvswb__tifa = bodo.libs.array_kernels.repeat_kernel(vfsk__xsl,
                repeats)
            dzy__jscs = bodo.utils.conversion.index_from_array(zvswb__tifa)
            return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
                dzy__jscs, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        vfsk__xsl = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        twhyr__yeg = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        zvswb__tifa = bodo.libs.array_kernels.repeat_kernel(vfsk__xsl, repeats)
        dzy__jscs = bodo.utils.conversion.index_from_array(zvswb__tifa)
        return bodo.hiframes.pd_series_ext.init_series(twhyr__yeg,
            dzy__jscs, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        tekjn__eem = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(tekjn__eem)
        axlo__etwl = {}
        for jmtr__xctzs in range(n):
            czbn__chuy = bodo.utils.conversion.box_if_dt64(tekjn__eem[
                jmtr__xctzs])
            axlo__etwl[index[jmtr__xctzs]] = czbn__chuy
        return axlo__etwl
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    ddi__fcw = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            voq__ghc = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(ddi__fcw)
    elif is_literal_type(name):
        voq__ghc = get_literal_value(name)
    else:
        raise_bodo_error(ddi__fcw)
    voq__ghc = 0 if voq__ghc is None else voq__ghc
    qicsh__ummqt = ColNamesMetaType((voq__ghc,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            qicsh__ummqt)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
