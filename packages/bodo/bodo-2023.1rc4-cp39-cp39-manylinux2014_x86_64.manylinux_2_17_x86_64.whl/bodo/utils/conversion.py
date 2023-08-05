"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.time_ext import TimeArrayType, cast_time_to_int
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_dtype
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.nullable_tuple_ext import NullableTupleType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_np_arr_typ, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, to_nullable_type, unwrap_typeref
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if isinstance(data, bodo.libs.float_arr_ext.FloatingArrayType
        ) and is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.float_arr_ext.
            get_float_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and (isinstance(data.
            dtype, (types.Boolean, types.Integer)) or isinstance(data.dtype,
            types.Float) and bodo.libs.float_arr_ext._use_nullable_float):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif isinstance(data.dtype, types.Float
                ) and bodo.libs.float_arr_ext._use_nullable_float:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.float_arr_ext.init_float_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.float_arr_ext.init_float_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        udh__iqwtp = data.dtype
        if isinstance(udh__iqwtp, types.Optional):
            udh__iqwtp = udh__iqwtp.type
            if bodo.utils.typing.is_scalar_type(udh__iqwtp):
                use_nullable_array = True
        faj__hmbi = dtype_to_array_type(udh__iqwtp)
        if not is_overload_none(use_nullable_array):
            faj__hmbi = to_nullable_type(faj__hmbi)

        def impl(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            nwd__hrlco = len(data)
            A = bodo.utils.utils.alloc_type(nwd__hrlco, faj__hmbi, (-1,))
            bodo.utils.utils.tuple_list_to_array(A, data, udh__iqwtp)
            return A
        return impl
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            gjfa__zzse = data.precision
            sfk__ljuq = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(nwd__hrlco,
                    gjfa__zzse, sfk__ljuq)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            pynx__kjc = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = np.empty(nwd__hrlco, pynx__kjc)
                txoio__kjylx = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                whhp__dxu = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    txoio__kjylx)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = whhp__dxu
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            zbk__sfsbs = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = np.empty(nwd__hrlco, zbk__sfsbs)
                tbbl__int = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = tbbl__int
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    nwd__hrlco)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = data
                return A
            return impl_ts
        if isinstance(data, bodo.hiframes.time_ext.TimeType):
            gjfa__zzse = data.precision

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = bodo.hiframes.time_ext.alloc_time_array(nwd__hrlco,
                    gjfa__zzse)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            pynx__kjc = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                nwd__hrlco = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, pynx__kjc)
                txoio__kjylx = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    A[zhglk__sqkl] = txoio__kjylx
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = scalar_to_arr_len
                juln__gaki = bodo.libs.int_arr_ext.alloc_int_array(nwd__hrlco,
                    dtype)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    juln__gaki[zhglk__sqkl] = data
                return juln__gaki
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Float) and bodo.libs.float_arr_ext._use_nullable_float:

            def impl_null_float(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = scalar_to_arr_len
                juln__gaki = bodo.libs.float_arr_ext.alloc_float_array(
                    nwd__hrlco, dtype)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    juln__gaki[zhglk__sqkl] = data
                return juln__gaki
            return impl_null_float
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = scalar_to_arr_len
                juln__gaki = bodo.libs.bool_arr_ext.alloc_bool_array(nwd__hrlco
                    )
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    juln__gaki[zhglk__sqkl] = data
                return juln__gaki
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            nwd__hrlco = scalar_to_arr_len
            juln__gaki = np.empty(nwd__hrlco, dtype)
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                juln__gaki[zhglk__sqkl] = data
            return juln__gaki
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(lqpq__zdfl, (
        types.Float, types.Integer)) for lqpq__zdfl in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_scalar_to_array(scalar, length, arr_type):
    pass


@overload(coerce_scalar_to_array)
def overload_coerce_scalar_to_array(scalar, length, arr_type):
    clzf__nfg = to_nullable_type(unwrap_typeref(arr_type))
    if scalar == types.none:

        def impl(scalar, length, arr_type):
            return bodo.libs.array_kernels.gen_na_array(length, clzf__nfg, True
                )
    elif isinstance(scalar, types.Optional):

        def impl(scalar, length, arr_type):
            if scalar is None:
                return bodo.libs.array_kernels.gen_na_array(length,
                    clzf__nfg, True)
            else:
                return bodo.utils.conversion.coerce_to_array(bodo.utils.
                    indexing.unoptional(scalar), True, True, length)
    else:

        def impl(scalar, length, arr_type):
            return bodo.utils.conversion.coerce_to_array(scalar, True, None,
                length)
    return impl


def ndarray_if_nullable_arr(data):
    pass


@overload(ndarray_if_nullable_arr)
def overload_ndarray_if_nullable_arr(data):
    if isinstance(data, (bodo.libs.int_arr_ext.IntegerArrayType, bodo.libs.
        float_arr_ext.FloatingArrayType)
        ) or data == bodo.libs.bool_arr_ext.boolean_array:
        return lambda data: bodo.utils.conversion.coerce_to_ndarray(data)
    return lambda data: data


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.BaseTuple) and data.count == 0:
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            empty_str_arr(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(lqpq__zdfl, types.StringLiteral) for
        lqpq__zdfl in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        binary_array_type, bodo.libs.bool_arr_ext.boolean_array, bodo.
        hiframes.datetime_date_ext.datetime_date_array_type, bodo.hiframes.
        datetime_timedelta_ext.datetime_timedelta_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type) or isinstance(data, (bodo
        .libs.int_arr_ext.IntegerArrayType, bodo.libs.float_arr_ext.
        FloatingArrayType, DecimalArrayType, bodo.libs.interval_arr_ext.
        IntervalArrayType, bodo.libs.tuple_arr_ext.TupleArrayType, bodo.
        libs.struct_arr_ext.StructArrayType, bodo.hiframes.
        pd_categorical_ext.CategoricalArrayType, bodo.libs.csr_matrix_ext.
        CSRMatrixType, bodo.DatetimeArrayType, TimeArrayType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        ssphl__cns = tuple(dtype_to_array_type(lqpq__zdfl) for lqpq__zdfl in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            nwd__hrlco = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(nwd__hrlco,
                (-1,), ssphl__cns)
            for zhglk__sqkl in range(nwd__hrlco):
                arr[zhglk__sqkl] = data[zhglk__sqkl]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        xjy__hmdze = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            nwd__hrlco = len(data)
            yive__cysg = init_nested_counts(xjy__hmdze)
            for zhglk__sqkl in range(nwd__hrlco):
                wcxtx__yxubm = bodo.utils.conversion.coerce_to_array(data[
                    zhglk__sqkl], use_nullable_array=True)
                yive__cysg = add_nested_counts(yive__cysg, wcxtx__yxubm)
            juln__gaki = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(nwd__hrlco, yive__cysg, xjy__hmdze))
            tfyoa__xdx = bodo.libs.array_item_arr_ext.get_null_bitmap(
                juln__gaki)
            for ovyq__sde in range(nwd__hrlco):
                wcxtx__yxubm = bodo.utils.conversion.coerce_to_array(data[
                    ovyq__sde], use_nullable_array=True)
                juln__gaki[ovyq__sde] = wcxtx__yxubm
                bodo.libs.int_arr_ext.set_bit_to_arr(tfyoa__xdx, ovyq__sde, 1)
            return juln__gaki
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            nwd__hrlco = scalar_to_arr_len
            xuwj__nsu = bodo.libs.str_arr_ext.str_arr_from_sequence([data])
            xke__qwgv = bodo.libs.int_arr_ext.alloc_int_array(nwd__hrlco,
                np.int32)
            numba.parfors.parfor.init_prange()
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                xke__qwgv[zhglk__sqkl] = 0
            A = bodo.libs.dict_arr_ext.init_dict_arr(xuwj__nsu, xke__qwgv, 
                True, True)
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            nwd__hrlco = len(data)
            A = np.empty(nwd__hrlco, np.dtype('datetime64[ns]'))
            for zhglk__sqkl in range(nwd__hrlco):
                A[zhglk__sqkl
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(data
                    [zhglk__sqkl].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            nwd__hrlco = len(data)
            A = np.empty(nwd__hrlco, np.dtype('timedelta64[ns]'))
            for zhglk__sqkl in range(nwd__hrlco):
                A[zhglk__sqkl
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[zhglk__sqkl].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType
        ) and data.tz is not None:
        hrw__jir = data.tz

        def impl_timestamp_tz_aware(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            A = np.empty(scalar_to_arr_len, 'datetime64[ns]')
            vsv__zav = data.to_datetime64()
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                scalar_to_arr_len):
                A[zhglk__sqkl] = vsv__zav
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(A,
                hrw__jir)
        return impl_timestamp_tz_aware
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_tz_naive_type, bodo.pd_timedelta_type]:
        epgka__lah = ('datetime64[ns]' if data == bodo.
            pd_timestamp_tz_naive_type else 'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            nwd__hrlco = scalar_to_arr_len
            A = np.empty(nwd__hrlco, epgka__lah)
            data = bodo.utils.conversion.unbox_if_tz_naive_timestamp(data)
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                A[zhglk__sqkl] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str' or isinstance(dtype, types.TypeRef
        ) and dtype.instance_type == types.unicode_type


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    pass


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    boaub__djf = False
    if is_overload_none(new_dtype):
        boaub__djf = True
    elif isinstance(new_dtype, types.TypeRef):
        boaub__djf = new_dtype.instance_type == data
    if not boaub__djf:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'fix_arr_dtype()')
    tsv__siq = is_overload_true(copy)
    tdh__ggjb = is_overload_constant_str(new_dtype) and get_overload_const_str(
        new_dtype) == 'object'
    if is_overload_none(new_dtype) or tdh__ggjb:
        if tsv__siq:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        unmo__gyi = {types.unicode_type: '', boolean_dtype: False, types.
            bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        wghoi__txu = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        opzy__zdlsi = unmo__gyi.keys()
        jhlls__fitv = list(data._tuple_typ.types)
        if nb_dtype not in opzy__zdlsi:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for mdgn__ful in jhlls__fitv:
            if mdgn__ful == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {mdgn__ful} to {nb_dtype}.'
                        )
            elif mdgn__ful == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {mdgn__ful} to {nb_dtype}.'
                        )
        cpga__bya = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        cpga__bya += '  data_tup = data._data\n'
        cpga__bya += '  null_tup = data._null_values\n'
        for zhglk__sqkl in range(len(jhlls__fitv)):
            cpga__bya += f'  val_{zhglk__sqkl} = convert_func(default_value)\n'
            cpga__bya += f'  if not null_tup[{zhglk__sqkl}]:\n'
            cpga__bya += (
                f'    val_{zhglk__sqkl} = convert_func(data_tup[{zhglk__sqkl}])\n'
                )
        kwovt__clotk = ', '.join(f'val_{zhglk__sqkl}' for zhglk__sqkl in
            range(len(jhlls__fitv)))
        cpga__bya += f'  vals_tup = ({kwovt__clotk},)\n'
        cpga__bya += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        cpga__bya += '  return res_tup\n'
        mia__odtph = {}
        myt__ufh = wghoi__txu[nb_dtype]
        abns__ptfrn = unmo__gyi[nb_dtype]
        exec(cpga__bya, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            abns__ptfrn, 'convert_func': myt__ufh}, mia__odtph)
        impl = mia__odtph['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(nwd__hrlco, -1
                    )
                for xzuj__xlx in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, xzuj__xlx):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                xzuj__xlx)
                        else:
                            bodo.libs.array_kernels.setna(A, xzuj__xlx)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            xzuj__xlx, data[xzuj__xlx])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(nwd__hrlco, -1
                    )
                for xzuj__xlx in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, xzuj__xlx):
                        bodo.libs.array_kernels.setna(A, xzuj__xlx)
                    else:
                        A[xzuj__xlx] = ''.join([chr(jpi__pev) for jpi__pev in
                            data[xzuj__xlx]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(nwd__hrlco, -1
                    )
                for xzuj__xlx in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, xzuj__xlx):
                        if nan_to_str:
                            A[xzuj__xlx] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, xzuj__xlx)
                        continue
                    A[xzuj__xlx] = str(box_if_dt64(data[xzuj__xlx]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                nwd__hrlco = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(nwd__hrlco, -1
                    )
                for xzuj__xlx in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, xzuj__xlx):
                        if nan_to_str:
                            A[xzuj__xlx] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, xzuj__xlx)
                        continue
                    A[xzuj__xlx] = str(data[xzuj__xlx])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            nwd__hrlco = len(data)
            numba.parfors.parfor.init_prange()
            wzpy__wdv = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                nwd__hrlco, new_dtype)
            gnbwv__jeaxf = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                    bodo.libs.array_kernels.setna(A, zhglk__sqkl)
                    continue
                val = data[zhglk__sqkl]
                if val not in wzpy__wdv:
                    bodo.libs.array_kernels.setna(A, zhglk__sqkl)
                    continue
                gnbwv__jeaxf[zhglk__sqkl] = wzpy__wdv[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            gcen__olji = bodo.libs.array_kernels.unique(data, dropna=True)
            gcen__olji = pd.Series(gcen__olji).sort_values().values
            gcen__olji = bodo.allgatherv(gcen__olji, False)
            fyd__pok = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(gcen__olji, None), False,
                None, None)
            nwd__hrlco = len(data)
            numba.parfors.parfor.init_prange()
            wzpy__wdv = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(gcen__olji))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                nwd__hrlco, fyd__pok)
            gnbwv__jeaxf = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                    bodo.libs.array_kernels.setna(A, zhglk__sqkl)
                    continue
                val = data[zhglk__sqkl]
                gnbwv__jeaxf[zhglk__sqkl] = wzpy__wdv[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        rzsqn__een = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    elif isinstance(data, bodo.libs.float_arr_ext.FloatingArrayType):
        rzsqn__een = isinstance(nb_dtype, bodo.libs.float_arr_ext.FloatDtype
            ) and data.dtype == nb_dtype.dtype
    elif bodo.utils.utils.is_array_typ(nb_dtype, False):
        rzsqn__een = data == nb_dtype
    else:
        rzsqn__een = data.dtype == nb_dtype
    if tsv__siq and rzsqn__een:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if rzsqn__een:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        epgka__lah = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                nwd__hrlco = len(data)
                numba.parfors.parfor.init_prange()
                ybv__fjs = bodo.libs.int_arr_ext.alloc_int_array(nwd__hrlco,
                    epgka__lah)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                        bodo.libs.array_kernels.setna(ybv__fjs, zhglk__sqkl)
                    else:
                        ybv__fjs[zhglk__sqkl] = int(data[zhglk__sqkl])
                return ybv__fjs
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        epgka__lah)
                return impl_dict
            if isinstance(data, bodo.hiframes.time_ext.TimeArrayType):

                def impl(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    nwd__hrlco = len(data)
                    numba.parfors.parfor.init_prange()
                    ybv__fjs = bodo.libs.int_arr_ext.alloc_int_array(nwd__hrlco
                        , epgka__lah)
                    for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                        nwd__hrlco):
                        if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                            bodo.libs.array_kernels.setna(ybv__fjs, zhglk__sqkl
                                )
                        else:
                            ybv__fjs[zhglk__sqkl] = cast_time_to_int(data[
                                zhglk__sqkl])
                    return ybv__fjs
                return impl

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                nwd__hrlco = len(data)
                numba.parfors.parfor.init_prange()
                ybv__fjs = bodo.libs.int_arr_ext.alloc_int_array(nwd__hrlco,
                    epgka__lah)
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                        bodo.libs.array_kernels.setna(ybv__fjs, zhglk__sqkl)
                    else:
                        ybv__fjs[zhglk__sqkl] = np.int64(data[zhglk__sqkl])
                return ybv__fjs
            return impl
    if isinstance(nb_dtype, bodo.libs.float_arr_ext.FloatDtype):
        epgka__lah = nb_dtype.dtype

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            nwd__hrlco = len(data)
            numba.parfors.parfor.init_prange()
            ybv__fjs = bodo.libs.float_arr_ext.alloc_float_array(nwd__hrlco,
                epgka__lah)
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                    bodo.libs.array_kernels.setna(ybv__fjs, zhglk__sqkl)
                else:
                    ybv__fjs[zhglk__sqkl] = float(data[zhglk__sqkl])
            return ybv__fjs
        return impl
    if isinstance(nb_dtype, types.Integer) and isinstance(data.dtype, types
        .Integer):

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if isinstance(nb_dtype, types.Float) and isinstance(data.dtype, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            nwd__hrlco = len(data)
            numba.parfors.parfor.init_prange()
            ybv__fjs = bodo.libs.bool_arr_ext.alloc_bool_array(nwd__hrlco)
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                    bodo.libs.array_kernels.setna(ybv__fjs, zhglk__sqkl)
                else:
                    ybv__fjs[zhglk__sqkl] = bool(data[zhglk__sqkl])
            return ybv__fjs
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                nwd__hrlco = len(data)
                juln__gaki = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(nwd__hrlco))
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                        bodo.libs.array_kernels.setna(juln__gaki, zhglk__sqkl)
                    else:
                        juln__gaki[zhglk__sqkl
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            zhglk__sqkl]).date()
                return juln__gaki
            return impl_date
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                nwd__hrlco = len(data)
                numba.parfors.parfor.init_prange()
                juln__gaki = np.empty(nwd__hrlco, dtype=np.dtype(
                    'datetime64[ns]'))
                for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                    nwd__hrlco):
                    if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                        bodo.libs.array_kernels.setna(juln__gaki, zhglk__sqkl)
                    else:
                        juln__gaki[zhglk__sqkl
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[zhglk__sqkl]))
                return juln__gaki
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if tsv__siq:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    nwd__hrlco = len(data)
                    numba.parfors.parfor.init_prange()
                    juln__gaki = np.empty(nwd__hrlco, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for zhglk__sqkl in numba.parfors.parfor.internal_prange(
                        nwd__hrlco):
                        if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                            bodo.libs.array_kernels.setna(juln__gaki,
                                zhglk__sqkl)
                        else:
                            juln__gaki[zhglk__sqkl] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[zhglk__sqkl])))
                    return juln__gaki
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            nwd__hrlco = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(nwd__hrlco, types.int64)
            for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco
                ):
                if bodo.libs.array_kernels.isna(data, zhglk__sqkl):
                    bodo.libs.array_kernels.setna(A, zhglk__sqkl)
                else:
                    A[zhglk__sqkl] = np.int64(data[zhglk__sqkl])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    xqinl__sykw = []
    nwd__hrlco = len(A)
    for zhglk__sqkl in range(nwd__hrlco):
        bdh__slrml = A[zhglk__sqkl]
        for kajy__ntg in bdh__slrml:
            xqinl__sykw.append(kajy__ntg)
    return bodo.utils.conversion.coerce_to_array(xqinl__sykw)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        nwd__hrlco = len(data)
        pqy__rip = np.empty(nwd__hrlco, bodo.utils.conversion.NS_DTYPE)
        for zhglk__sqkl in numba.parfors.parfor.internal_prange(nwd__hrlco):
            pqy__rip[zhglk__sqkl
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                zhglk__sqkl])
        return pqy__rip
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if is_np_arr_typ(data, types.NPDatetime('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if is_np_arr_typ(data, types.NPTimedelta('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for timedelta64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, PeriodIndexType, types.NoneType)
        ):
        return lambda data, name=None: data

    def impl(data, name=None):
        ldoq__nen = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(ldoq__nen, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type, bodo.
        dict_str_arr_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    if isinstance(data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_datetime_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_tz_naive_timestamp(val):
    return val


@overload(unbox_if_tz_naive_timestamp, no_unliteral=True)
def overload_unbox_if_tz_naive_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type):

        def impl_optional(val):
            if val is None:
                qnxoi__vlm = None
            else:
                qnxoi__vlm = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    bodo.utils.indexing.unoptional(val).value)
            return qnxoi__vlm
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                qnxoi__vlm = None
            else:
                qnxoi__vlm = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return qnxoi__vlm
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        qmfr__hqvw = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        cpga__bya = 'def f(val):\n'
        poz__ojmr = ','.join(f'val[{zhglk__sqkl}]' for zhglk__sqkl in range
            (qmfr__hqvw))
        cpga__bya += f'  return ({poz__ojmr},)\n'
        mia__odtph = {}
        exec(cpga__bya, {}, mia__odtph)
        impl = mia__odtph['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                zticn__ycec = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(zticn__ycec)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            jamax__qcv = bodo.utils.conversion.coerce_to_array(index)
            return jamax__qcv
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {veelv__krccj: txoio__kjylx for veelv__krccj, txoio__kjylx in
        zip(names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    zlk__jdhcc = len(values.types)
    cpga__bya = 'def f(values, names):\n'
    poz__ojmr = ','.join("'{}': values[{}]".format(get_overload_const_str(
        names.types[zhglk__sqkl]), zhglk__sqkl) for zhglk__sqkl in range(
        zlk__jdhcc))
    cpga__bya += '  return {{{}}}\n'.format(poz__ojmr)
    mia__odtph = {}
    exec(cpga__bya, {}, mia__odtph)
    impl = mia__odtph['f']
    return impl


def nullable_bool_to_bool_na_false(arr):
    pass


@overload(nullable_bool_to_bool_na_false)
def overload_nullable_bool_to_bool_na_false(arr):
    if arr == bodo.boolean_array:

        def impl(arr):
            baaxb__ban = bodo.libs.bool_arr_ext.get_bool_arr_data(arr)
            for zhglk__sqkl in range(len(arr)):
                baaxb__ban[zhglk__sqkl] = baaxb__ban[zhglk__sqkl
                    ] and not bodo.libs.array_kernels.isna(arr, zhglk__sqkl)
            return baaxb__ban
        return impl
    else:
        return lambda arr: arr
