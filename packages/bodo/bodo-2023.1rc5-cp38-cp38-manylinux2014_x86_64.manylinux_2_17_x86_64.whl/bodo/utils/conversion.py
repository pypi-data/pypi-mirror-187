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
        zwah__yetfd = data.dtype
        if isinstance(zwah__yetfd, types.Optional):
            zwah__yetfd = zwah__yetfd.type
            if bodo.utils.typing.is_scalar_type(zwah__yetfd):
                use_nullable_array = True
        twko__dwfsf = dtype_to_array_type(zwah__yetfd)
        if not is_overload_none(use_nullable_array):
            twko__dwfsf = to_nullable_type(twko__dwfsf)

        def impl(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            deykk__tmey = len(data)
            A = bodo.utils.utils.alloc_type(deykk__tmey, twko__dwfsf, (-1,))
            bodo.utils.utils.tuple_list_to_array(A, data, zwah__yetfd)
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
            fnu__dbeah = data.precision
            ccblu__mum = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(deykk__tmey,
                    fnu__dbeah, ccblu__mum)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            owt__nor = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = np.empty(deykk__tmey, owt__nor)
                sbgfk__zklc = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                zoe__rxca = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    sbgfk__zklc)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = zoe__rxca
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            dyuhd__mntes = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = np.empty(deykk__tmey, dyuhd__mntes)
                krprf__pitl = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = krprf__pitl
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    deykk__tmey)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = data
                return A
            return impl_ts
        if isinstance(data, bodo.hiframes.time_ext.TimeType):
            fnu__dbeah = data.precision

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = bodo.hiframes.time_ext.alloc_time_array(deykk__tmey,
                    fnu__dbeah)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            owt__nor = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                deykk__tmey = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, owt__nor)
                sbgfk__zklc = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    A[ysvn__ndgi] = sbgfk__zklc
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                deykk__tmey = scalar_to_arr_len
                jnhg__ugrkj = bodo.libs.int_arr_ext.alloc_int_array(deykk__tmey
                    , dtype)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    jnhg__ugrkj[ysvn__ndgi] = data
                return jnhg__ugrkj
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Float) and bodo.libs.float_arr_ext._use_nullable_float:

            def impl_null_float(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                deykk__tmey = scalar_to_arr_len
                jnhg__ugrkj = bodo.libs.float_arr_ext.alloc_float_array(
                    deykk__tmey, dtype)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    jnhg__ugrkj[ysvn__ndgi] = data
                return jnhg__ugrkj
            return impl_null_float
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                deykk__tmey = scalar_to_arr_len
                jnhg__ugrkj = bodo.libs.bool_arr_ext.alloc_bool_array(
                    deykk__tmey)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    jnhg__ugrkj[ysvn__ndgi] = data
                return jnhg__ugrkj
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            deykk__tmey = scalar_to_arr_len
            jnhg__ugrkj = np.empty(deykk__tmey, dtype)
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                jnhg__ugrkj[ysvn__ndgi] = data
            return jnhg__ugrkj
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(jmg__pstzf, (
        types.Float, types.Integer)) for jmg__pstzf in data.types):
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
    qcyx__xbzen = to_nullable_type(unwrap_typeref(arr_type))
    if scalar == types.none:

        def impl(scalar, length, arr_type):
            return bodo.libs.array_kernels.gen_na_array(length, qcyx__xbzen,
                True)
    elif isinstance(scalar, types.Optional):

        def impl(scalar, length, arr_type):
            if scalar is None:
                return bodo.libs.array_kernels.gen_na_array(length,
                    qcyx__xbzen, True)
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
        ) and all(isinstance(jmg__pstzf, types.StringLiteral) for
        jmg__pstzf in data.types):
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
        zer__nxn = tuple(dtype_to_array_type(jmg__pstzf) for jmg__pstzf in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            deykk__tmey = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(deykk__tmey,
                (-1,), zer__nxn)
            for ysvn__ndgi in range(deykk__tmey):
                arr[ysvn__ndgi] = data[ysvn__ndgi]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        hgo__kvve = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            deykk__tmey = len(data)
            powq__lzje = init_nested_counts(hgo__kvve)
            for ysvn__ndgi in range(deykk__tmey):
                odl__ylaev = bodo.utils.conversion.coerce_to_array(data[
                    ysvn__ndgi], use_nullable_array=True)
                powq__lzje = add_nested_counts(powq__lzje, odl__ylaev)
            jnhg__ugrkj = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(deykk__tmey, powq__lzje, hgo__kvve))
            ony__akn = bodo.libs.array_item_arr_ext.get_null_bitmap(jnhg__ugrkj
                )
            for hvdke__cciag in range(deykk__tmey):
                odl__ylaev = bodo.utils.conversion.coerce_to_array(data[
                    hvdke__cciag], use_nullable_array=True)
                jnhg__ugrkj[hvdke__cciag] = odl__ylaev
                bodo.libs.int_arr_ext.set_bit_to_arr(ony__akn, hvdke__cciag, 1)
            return jnhg__ugrkj
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            deykk__tmey = scalar_to_arr_len
            woon__eog = bodo.libs.str_arr_ext.str_arr_from_sequence([data])
            fwe__ezse = bodo.libs.int_arr_ext.alloc_int_array(deykk__tmey,
                np.int32)
            numba.parfors.parfor.init_prange()
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                fwe__ezse[ysvn__ndgi] = 0
            A = bodo.libs.dict_arr_ext.init_dict_arr(woon__eog, fwe__ezse, 
                True, True)
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            deykk__tmey = len(data)
            A = np.empty(deykk__tmey, np.dtype('datetime64[ns]'))
            for ysvn__ndgi in range(deykk__tmey):
                A[ysvn__ndgi] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[ysvn__ndgi].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            deykk__tmey = len(data)
            A = np.empty(deykk__tmey, np.dtype('timedelta64[ns]'))
            for ysvn__ndgi in range(deykk__tmey):
                A[ysvn__ndgi
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[ysvn__ndgi].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType
        ) and data.tz is not None:
        iit__wxk = data.tz

        def impl_timestamp_tz_aware(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            A = np.empty(scalar_to_arr_len, 'datetime64[ns]')
            phy__oimus = data.to_datetime64()
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                scalar_to_arr_len):
                A[ysvn__ndgi] = phy__oimus
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(A,
                iit__wxk)
        return impl_timestamp_tz_aware
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_tz_naive_type, bodo.pd_timedelta_type]:
        okkzm__ntspr = ('datetime64[ns]' if data == bodo.
            pd_timestamp_tz_naive_type else 'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            deykk__tmey = scalar_to_arr_len
            A = np.empty(deykk__tmey, okkzm__ntspr)
            data = bodo.utils.conversion.unbox_if_tz_naive_timestamp(data)
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                A[ysvn__ndgi] = data
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
    jba__wqql = False
    if is_overload_none(new_dtype):
        jba__wqql = True
    elif isinstance(new_dtype, types.TypeRef):
        jba__wqql = new_dtype.instance_type == data
    if not jba__wqql:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'fix_arr_dtype()')
    ljv__azq = is_overload_true(copy)
    rhxi__dwxa = is_overload_constant_str(new_dtype
        ) and get_overload_const_str(new_dtype) == 'object'
    if is_overload_none(new_dtype) or rhxi__dwxa:
        if ljv__azq:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        jflvs__hdps = {types.unicode_type: '', boolean_dtype: False, types.
            bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        zjwyv__jyf = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        lcax__gwntg = jflvs__hdps.keys()
        xjkax__uap = list(data._tuple_typ.types)
        if nb_dtype not in lcax__gwntg:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for tbi__hrm in xjkax__uap:
            if tbi__hrm == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {tbi__hrm} to {nb_dtype}.'
                        )
            elif tbi__hrm == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {tbi__hrm} to {nb_dtype}.'
                        )
        sbzu__ffp = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        sbzu__ffp += '  data_tup = data._data\n'
        sbzu__ffp += '  null_tup = data._null_values\n'
        for ysvn__ndgi in range(len(xjkax__uap)):
            sbzu__ffp += f'  val_{ysvn__ndgi} = convert_func(default_value)\n'
            sbzu__ffp += f'  if not null_tup[{ysvn__ndgi}]:\n'
            sbzu__ffp += (
                f'    val_{ysvn__ndgi} = convert_func(data_tup[{ysvn__ndgi}])\n'
                )
        mwk__ttcol = ', '.join(f'val_{ysvn__ndgi}' for ysvn__ndgi in range(
            len(xjkax__uap)))
        sbzu__ffp += f'  vals_tup = ({mwk__ttcol},)\n'
        sbzu__ffp += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        sbzu__ffp += '  return res_tup\n'
        mxl__igm = {}
        zvgb__wvddo = zjwyv__jyf[nb_dtype]
        urgbt__fif = jflvs__hdps[nb_dtype]
        exec(sbzu__ffp, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            urgbt__fif, 'convert_func': zvgb__wvddo}, mxl__igm)
        impl = mxl__igm['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                deykk__tmey = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(deykk__tmey,
                    -1)
                for kpecu__dpnu in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, kpecu__dpnu):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                kpecu__dpnu)
                        else:
                            bodo.libs.array_kernels.setna(A, kpecu__dpnu)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            kpecu__dpnu, data[kpecu__dpnu])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                deykk__tmey = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(deykk__tmey,
                    -1)
                for kpecu__dpnu in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, kpecu__dpnu):
                        bodo.libs.array_kernels.setna(A, kpecu__dpnu)
                    else:
                        A[kpecu__dpnu] = ''.join([chr(scra__uit) for
                            scra__uit in data[kpecu__dpnu]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                deykk__tmey = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(deykk__tmey,
                    -1)
                for kpecu__dpnu in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, kpecu__dpnu):
                        if nan_to_str:
                            A[kpecu__dpnu] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, kpecu__dpnu)
                        continue
                    A[kpecu__dpnu] = str(box_if_dt64(data[kpecu__dpnu]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                deykk__tmey = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(deykk__tmey,
                    -1)
                for kpecu__dpnu in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, kpecu__dpnu):
                        if nan_to_str:
                            A[kpecu__dpnu] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, kpecu__dpnu)
                        continue
                    A[kpecu__dpnu] = str(data[kpecu__dpnu])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            deykk__tmey = len(data)
            numba.parfors.parfor.init_prange()
            ssvst__qoyxk = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                deykk__tmey, new_dtype)
            ykzsy__ymxib = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                    bodo.libs.array_kernels.setna(A, ysvn__ndgi)
                    continue
                val = data[ysvn__ndgi]
                if val not in ssvst__qoyxk:
                    bodo.libs.array_kernels.setna(A, ysvn__ndgi)
                    continue
                ykzsy__ymxib[ysvn__ndgi] = ssvst__qoyxk[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            rcgyw__ybq = bodo.libs.array_kernels.unique(data, dropna=True)
            rcgyw__ybq = pd.Series(rcgyw__ybq).sort_values().values
            rcgyw__ybq = bodo.allgatherv(rcgyw__ybq, False)
            lumw__yfccb = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(rcgyw__ybq, None), False,
                None, None)
            deykk__tmey = len(data)
            numba.parfors.parfor.init_prange()
            ssvst__qoyxk = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(rcgyw__ybq))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                deykk__tmey, lumw__yfccb)
            ykzsy__ymxib = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                    bodo.libs.array_kernels.setna(A, ysvn__ndgi)
                    continue
                val = data[ysvn__ndgi]
                ykzsy__ymxib[ysvn__ndgi] = ssvst__qoyxk[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        foyug__zlzw = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    elif isinstance(data, bodo.libs.float_arr_ext.FloatingArrayType):
        foyug__zlzw = isinstance(nb_dtype, bodo.libs.float_arr_ext.FloatDtype
            ) and data.dtype == nb_dtype.dtype
    elif bodo.utils.utils.is_array_typ(nb_dtype, False):
        foyug__zlzw = data == nb_dtype
    else:
        foyug__zlzw = data.dtype == nb_dtype
    if ljv__azq and foyug__zlzw:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if foyug__zlzw:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        okkzm__ntspr = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                deykk__tmey = len(data)
                numba.parfors.parfor.init_prange()
                hmhvi__twlst = bodo.libs.int_arr_ext.alloc_int_array(
                    deykk__tmey, okkzm__ntspr)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                        bodo.libs.array_kernels.setna(hmhvi__twlst, ysvn__ndgi)
                    else:
                        hmhvi__twlst[ysvn__ndgi] = int(data[ysvn__ndgi])
                return hmhvi__twlst
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        okkzm__ntspr)
                return impl_dict
            if isinstance(data, bodo.hiframes.time_ext.TimeArrayType):

                def impl(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    deykk__tmey = len(data)
                    numba.parfors.parfor.init_prange()
                    hmhvi__twlst = bodo.libs.int_arr_ext.alloc_int_array(
                        deykk__tmey, okkzm__ntspr)
                    for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                        deykk__tmey):
                        if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                            bodo.libs.array_kernels.setna(hmhvi__twlst,
                                ysvn__ndgi)
                        else:
                            hmhvi__twlst[ysvn__ndgi] = cast_time_to_int(data
                                [ysvn__ndgi])
                    return hmhvi__twlst
                return impl

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                deykk__tmey = len(data)
                numba.parfors.parfor.init_prange()
                hmhvi__twlst = bodo.libs.int_arr_ext.alloc_int_array(
                    deykk__tmey, okkzm__ntspr)
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                        bodo.libs.array_kernels.setna(hmhvi__twlst, ysvn__ndgi)
                    else:
                        hmhvi__twlst[ysvn__ndgi] = np.int64(data[ysvn__ndgi])
                return hmhvi__twlst
            return impl
    if isinstance(nb_dtype, bodo.libs.float_arr_ext.FloatDtype):
        okkzm__ntspr = nb_dtype.dtype

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            deykk__tmey = len(data)
            numba.parfors.parfor.init_prange()
            hmhvi__twlst = bodo.libs.float_arr_ext.alloc_float_array(
                deykk__tmey, okkzm__ntspr)
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                    bodo.libs.array_kernels.setna(hmhvi__twlst, ysvn__ndgi)
                else:
                    hmhvi__twlst[ysvn__ndgi] = float(data[ysvn__ndgi])
            return hmhvi__twlst
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
            deykk__tmey = len(data)
            numba.parfors.parfor.init_prange()
            hmhvi__twlst = bodo.libs.bool_arr_ext.alloc_bool_array(deykk__tmey)
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                    bodo.libs.array_kernels.setna(hmhvi__twlst, ysvn__ndgi)
                else:
                    hmhvi__twlst[ysvn__ndgi] = bool(data[ysvn__ndgi])
            return hmhvi__twlst
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                deykk__tmey = len(data)
                jnhg__ugrkj = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(deykk__tmey))
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                        bodo.libs.array_kernels.setna(jnhg__ugrkj, ysvn__ndgi)
                    else:
                        jnhg__ugrkj[ysvn__ndgi
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            ysvn__ndgi]).date()
                return jnhg__ugrkj
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
                deykk__tmey = len(data)
                numba.parfors.parfor.init_prange()
                jnhg__ugrkj = np.empty(deykk__tmey, dtype=np.dtype(
                    'datetime64[ns]'))
                for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                    deykk__tmey):
                    if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                        bodo.libs.array_kernels.setna(jnhg__ugrkj, ysvn__ndgi)
                    else:
                        jnhg__ugrkj[ysvn__ndgi
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[ysvn__ndgi]))
                return jnhg__ugrkj
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
            if ljv__azq:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    deykk__tmey = len(data)
                    numba.parfors.parfor.init_prange()
                    jnhg__ugrkj = np.empty(deykk__tmey, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for ysvn__ndgi in numba.parfors.parfor.internal_prange(
                        deykk__tmey):
                        if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                            bodo.libs.array_kernels.setna(jnhg__ugrkj,
                                ysvn__ndgi)
                        else:
                            jnhg__ugrkj[ysvn__ndgi] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[ysvn__ndgi])))
                    return jnhg__ugrkj
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            deykk__tmey = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(deykk__tmey, types.int64)
            for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey
                ):
                if bodo.libs.array_kernels.isna(data, ysvn__ndgi):
                    bodo.libs.array_kernels.setna(A, ysvn__ndgi)
                else:
                    A[ysvn__ndgi] = np.int64(data[ysvn__ndgi])
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
    npomo__fwsjc = []
    deykk__tmey = len(A)
    for ysvn__ndgi in range(deykk__tmey):
        uilp__aei = A[ysvn__ndgi]
        for oyj__oev in uilp__aei:
            npomo__fwsjc.append(oyj__oev)
    return bodo.utils.conversion.coerce_to_array(npomo__fwsjc)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        deykk__tmey = len(data)
        fcny__kdgvp = np.empty(deykk__tmey, bodo.utils.conversion.NS_DTYPE)
        for ysvn__ndgi in numba.parfors.parfor.internal_prange(deykk__tmey):
            fcny__kdgvp[ysvn__ndgi
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                ysvn__ndgi])
        return fcny__kdgvp
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
        hjr__hocfd = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(hjr__hocfd, name)
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
                tenfa__vuyuo = None
            else:
                tenfa__vuyuo = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    bodo.utils.indexing.unoptional(val).value)
            return tenfa__vuyuo
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                tenfa__vuyuo = None
            else:
                tenfa__vuyuo = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return tenfa__vuyuo
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        jhbtl__jhgwc = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        sbzu__ffp = 'def f(val):\n'
        wcsc__sqaj = ','.join(f'val[{ysvn__ndgi}]' for ysvn__ndgi in range(
            jhbtl__jhgwc))
        sbzu__ffp += f'  return ({wcsc__sqaj},)\n'
        mxl__igm = {}
        exec(sbzu__ffp, {}, mxl__igm)
        impl = mxl__igm['f']
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
                rivly__epfzz = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(rivly__epfzz)
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
            ngy__itt = bodo.utils.conversion.coerce_to_array(index)
            return ngy__itt
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
    return {tyb__yhrnu: sbgfk__zklc for tyb__yhrnu, sbgfk__zklc in zip(
        names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    rqtww__cyhak = len(values.types)
    sbzu__ffp = 'def f(values, names):\n'
    wcsc__sqaj = ','.join("'{}': values[{}]".format(get_overload_const_str(
        names.types[ysvn__ndgi]), ysvn__ndgi) for ysvn__ndgi in range(
        rqtww__cyhak))
    sbzu__ffp += '  return {{{}}}\n'.format(wcsc__sqaj)
    mxl__igm = {}
    exec(sbzu__ffp, {}, mxl__igm)
    impl = mxl__igm['f']
    return impl


def nullable_bool_to_bool_na_false(arr):
    pass


@overload(nullable_bool_to_bool_na_false)
def overload_nullable_bool_to_bool_na_false(arr):
    if arr == bodo.boolean_array:

        def impl(arr):
            smv__cak = bodo.libs.bool_arr_ext.get_bool_arr_data(arr)
            for ysvn__ndgi in range(len(arr)):
                smv__cak[ysvn__ndgi] = smv__cak[ysvn__ndgi
                    ] and not bodo.libs.array_kernels.isna(arr, ysvn__ndgi)
            return smv__cak
        return impl
    else:
        return lambda arr: arr
