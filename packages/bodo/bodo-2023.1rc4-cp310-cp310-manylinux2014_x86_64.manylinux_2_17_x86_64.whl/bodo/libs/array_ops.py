"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils import tracing
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


def array_op_any(arr, skipna=True):
    pass


@overload(array_op_any)
def overload_array_op_any(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        oeaxa__jiz = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        oeaxa__jiz = False
    elif A == bodo.string_array_type:
        oeaxa__jiz = ''
    elif A == bodo.binary_array_type:
        oeaxa__jiz = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, bdstd__pkgxa):
                if A[bdstd__pkgxa] != oeaxa__jiz:
                    tuh__bqyhv += 1
        return tuh__bqyhv != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        oeaxa__jiz = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        oeaxa__jiz = False
    elif A == bodo.string_array_type:
        oeaxa__jiz = ''
    elif A == bodo.binary_array_type:
        oeaxa__jiz = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, bdstd__pkgxa):
                if A[bdstd__pkgxa] == oeaxa__jiz:
                    tuh__bqyhv += 1
        return tuh__bqyhv == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    eppm__now = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(eppm__now.ctypes, arr,
        parallel, skipna)
    return eppm__now[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        llzae__yms = len(arr)
        eukvt__piynr = np.empty(llzae__yms, np.bool_)
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(llzae__yms):
            eukvt__piynr[bdstd__pkgxa] = bodo.libs.array_kernels.isna(arr,
                bdstd__pkgxa)
        return eukvt__piynr
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
            flrqg__xnlj = 0
            if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                flrqg__xnlj = 1
            tuh__bqyhv += flrqg__xnlj
        eppm__now = tuh__bqyhv
        return eppm__now
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    ygc__xerjk = array_op_count(arr)
    lyaor__ivdv = array_op_min(arr)
    jixiv__zxblm = array_op_max(arr)
    bdznt__bdxtp = array_op_mean(arr)
    oyml__fws = array_op_std(arr)
    kwn__zhi = array_op_quantile(arr, 0.25)
    ijb__mlk = array_op_quantile(arr, 0.5)
    beuqs__alahf = array_op_quantile(arr, 0.75)
    return (ygc__xerjk, bdznt__bdxtp, oyml__fws, lyaor__ivdv, kwn__zhi,
        ijb__mlk, beuqs__alahf, jixiv__zxblm)


def array_op_describe_dt_impl(arr):
    ygc__xerjk = array_op_count(arr)
    lyaor__ivdv = array_op_min(arr)
    jixiv__zxblm = array_op_max(arr)
    bdznt__bdxtp = array_op_mean(arr)
    kwn__zhi = array_op_quantile(arr, 0.25)
    ijb__mlk = array_op_quantile(arr, 0.5)
    beuqs__alahf = array_op_quantile(arr, 0.75)
    return (ygc__xerjk, bdznt__bdxtp, lyaor__ivdv, kwn__zhi, ijb__mlk,
        beuqs__alahf, jixiv__zxblm)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = numba.cpython.builtins.get_type_max_value(np.int64)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[bdstd__pkgxa]))
                    flrqg__xnlj = 1
                dqwyr__zefp = min(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dqwyr__zefp,
                tuh__bqyhv)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = numba.cpython.builtins.get_type_max_value(np.int64)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[bdstd__pkgxa]))
                    flrqg__xnlj = 1
                dqwyr__zefp = min(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dqwyr__zefp,
                tuh__bqyhv)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            vfju__tkin = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = numba.cpython.builtins.get_type_max_value(np.int64)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(
                vfju__tkin)):
                haz__slkgy = vfju__tkin[bdstd__pkgxa]
                if haz__slkgy == -1:
                    continue
                dqwyr__zefp = min(dqwyr__zefp, haz__slkgy)
                tuh__bqyhv += 1
            eppm__now = bodo.hiframes.series_kernels._box_cat_val(dqwyr__zefp,
                arr.dtype, tuh__bqyhv)
            return eppm__now
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = bodo.hiframes.series_kernels._get_date_max_value()
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = arr[bdstd__pkgxa]
                    flrqg__xnlj = 1
                dqwyr__zefp = min(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            eppm__now = bodo.hiframes.series_kernels._sum_handle_nan(
                dqwyr__zefp, tuh__bqyhv)
            return eppm__now
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqwyr__zefp = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
            nbvb__kabkr = dqwyr__zefp
            flrqg__xnlj = 0
            if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                nbvb__kabkr = arr[bdstd__pkgxa]
                flrqg__xnlj = 1
            dqwyr__zefp = min(dqwyr__zefp, nbvb__kabkr)
            tuh__bqyhv += flrqg__xnlj
        eppm__now = bodo.hiframes.series_kernels._sum_handle_nan(dqwyr__zefp,
            tuh__bqyhv)
        return eppm__now
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = numba.cpython.builtins.get_type_min_value(np.int64)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[bdstd__pkgxa]))
                    flrqg__xnlj = 1
                dqwyr__zefp = max(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(dqwyr__zefp,
                tuh__bqyhv)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = numba.cpython.builtins.get_type_min_value(np.int64)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[bdstd__pkgxa]))
                    flrqg__xnlj = 1
                dqwyr__zefp = max(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            return bodo.hiframes.pd_index_ext._dti_val_finalize(dqwyr__zefp,
                tuh__bqyhv)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            vfju__tkin = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = -1
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(
                vfju__tkin)):
                dqwyr__zefp = max(dqwyr__zefp, vfju__tkin[bdstd__pkgxa])
            eppm__now = bodo.hiframes.series_kernels._box_cat_val(dqwyr__zefp,
                arr.dtype, 1)
            return eppm__now
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = bodo.hiframes.series_kernels._get_date_min_value()
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = dqwyr__zefp
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = arr[bdstd__pkgxa]
                    flrqg__xnlj = 1
                dqwyr__zefp = max(dqwyr__zefp, nbvb__kabkr)
                tuh__bqyhv += flrqg__xnlj
            eppm__now = bodo.hiframes.series_kernels._sum_handle_nan(
                dqwyr__zefp, tuh__bqyhv)
            return eppm__now
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqwyr__zefp = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
            nbvb__kabkr = dqwyr__zefp
            flrqg__xnlj = 0
            if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                nbvb__kabkr = arr[bdstd__pkgxa]
                flrqg__xnlj = 1
            dqwyr__zefp = max(dqwyr__zefp, nbvb__kabkr)
            tuh__bqyhv += flrqg__xnlj
        eppm__now = bodo.hiframes.series_kernels._sum_handle_nan(dqwyr__zefp,
            tuh__bqyhv)
        return eppm__now
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    xhhni__fzms = types.float64
    edl__ngq = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        xhhni__fzms = types.float32
        edl__ngq = types.float32
    dhoz__nqbj = xhhni__fzms(0)
    dsosw__winn = edl__ngq(0)
    tyq__zqo = edl__ngq(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        dqwyr__zefp = dhoz__nqbj
        tuh__bqyhv = dsosw__winn
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
            nbvb__kabkr = dhoz__nqbj
            flrqg__xnlj = dsosw__winn
            if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                nbvb__kabkr = arr[bdstd__pkgxa]
                flrqg__xnlj = tyq__zqo
            dqwyr__zefp += nbvb__kabkr
            tuh__bqyhv += flrqg__xnlj
        eppm__now = bodo.hiframes.series_kernels._mean_handle_nan(dqwyr__zefp,
            tuh__bqyhv)
        return eppm__now
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        girsq__kwoe = 0.0
        jhlit__kije = 0.0
        tuh__bqyhv = 0
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
            nbvb__kabkr = 0.0
            flrqg__xnlj = 0
            if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa
                ) or not skipna:
                nbvb__kabkr = arr[bdstd__pkgxa]
                flrqg__xnlj = 1
            girsq__kwoe += nbvb__kabkr
            jhlit__kije += nbvb__kabkr * nbvb__kabkr
            tuh__bqyhv += flrqg__xnlj
        eppm__now = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            girsq__kwoe, jhlit__kije, tuh__bqyhv, ddof)
        return eppm__now
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                eukvt__piynr = np.empty(len(q), np.int64)
                for bdstd__pkgxa in range(len(q)):
                    umftf__wbr = np.float64(q[bdstd__pkgxa])
                    eukvt__piynr[bdstd__pkgxa
                        ] = bodo.libs.array_kernels.quantile(arr.view(np.
                        int64), umftf__wbr)
                return eukvt__piynr.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            eukvt__piynr = np.empty(len(q), np.float64)
            for bdstd__pkgxa in range(len(q)):
                umftf__wbr = np.float64(q[bdstd__pkgxa])
                eukvt__piynr[bdstd__pkgxa] = bodo.libs.array_kernels.quantile(
                    arr, umftf__wbr)
            return eukvt__piynr
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        eub__kax = types.intp
    elif arr.dtype == types.bool_:
        eub__kax = np.int64
    else:
        eub__kax = arr.dtype
    trpw__rgefu = eub__kax(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = trpw__rgefu
            llzae__yms = len(arr)
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(llzae__yms
                ):
                nbvb__kabkr = trpw__rgefu
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa
                    ) or not skipna:
                    nbvb__kabkr = arr[bdstd__pkgxa]
                    flrqg__xnlj = 1
                dqwyr__zefp += nbvb__kabkr
                tuh__bqyhv += flrqg__xnlj
            eppm__now = bodo.hiframes.series_kernels._var_handle_mincount(
                dqwyr__zefp, tuh__bqyhv, min_count)
            return eppm__now
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = trpw__rgefu
            llzae__yms = len(arr)
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(llzae__yms
                ):
                nbvb__kabkr = trpw__rgefu
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = arr[bdstd__pkgxa]
                dqwyr__zefp += nbvb__kabkr
            return dqwyr__zefp
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    ozdt__nxnga = arr.dtype(1)
    if arr.dtype == types.bool_:
        ozdt__nxnga = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = ozdt__nxnga
            tuh__bqyhv = 0
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = ozdt__nxnga
                flrqg__xnlj = 0
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa
                    ) or not skipna:
                    nbvb__kabkr = arr[bdstd__pkgxa]
                    flrqg__xnlj = 1
                tuh__bqyhv += flrqg__xnlj
                dqwyr__zefp *= nbvb__kabkr
            eppm__now = bodo.hiframes.series_kernels._var_handle_mincount(
                dqwyr__zefp, tuh__bqyhv, min_count)
            return eppm__now
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            dqwyr__zefp = ozdt__nxnga
            for bdstd__pkgxa in numba.parfors.parfor.internal_prange(len(arr)):
                nbvb__kabkr = ozdt__nxnga
                if not bodo.libs.array_kernels.isna(arr, bdstd__pkgxa):
                    nbvb__kabkr = arr[bdstd__pkgxa]
                dqwyr__zefp *= nbvb__kabkr
            return dqwyr__zefp
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        bdstd__pkgxa = bodo.libs.array_kernels._nan_argmax(arr)
        return index[bdstd__pkgxa]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        bdstd__pkgxa = bodo.libs.array_kernels._nan_argmin(arr)
        return index[bdstd__pkgxa]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            hxnc__gokcb = {}
            for iplt__mwto in values:
                hxnc__gokcb[bodo.utils.conversion.box_if_dt64(iplt__mwto)] = 0
            return hxnc__gokcb
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        llzae__yms = len(arr)
        eukvt__piynr = np.empty(llzae__yms, np.bool_)
        for bdstd__pkgxa in numba.parfors.parfor.internal_prange(llzae__yms):
            eukvt__piynr[bdstd__pkgxa] = bodo.utils.conversion.box_if_dt64(arr
                [bdstd__pkgxa]) in values
        return eukvt__piynr
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    ezqph__yzbrg = len(in_arr_tup) != 1
    pyh__stdnx = list(in_arr_tup.types)
    ozty__lgtiq = 'def impl(in_arr_tup):\n'
    ozty__lgtiq += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    ozty__lgtiq += '  n = len(in_arr_tup[0])\n'
    if ezqph__yzbrg:
        awz__qlxq = ', '.join([f'in_arr_tup[{bdstd__pkgxa}][unused]' for
            bdstd__pkgxa in range(len(in_arr_tup))])
        afvh__dsvh = ', '.join(['False' for sjosu__vfid in range(len(
            in_arr_tup))])
        ozty__lgtiq += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({awz__qlxq},), ({afvh__dsvh},)): 0 for unused in range(0)}}
"""
        ozty__lgtiq += '  map_vector = np.empty(n, np.int64)\n'
        for bdstd__pkgxa, ktv__hudo in enumerate(pyh__stdnx):
            ozty__lgtiq += f'  in_lst_{bdstd__pkgxa} = []\n'
            if is_str_arr_type(ktv__hudo):
                ozty__lgtiq += f'  total_len_{bdstd__pkgxa} = 0\n'
            ozty__lgtiq += f'  null_in_lst_{bdstd__pkgxa} = []\n'
        ozty__lgtiq += '  for i in range(n):\n'
        buam__xonhc = ', '.join([f'in_arr_tup[{bdstd__pkgxa}][i]' for
            bdstd__pkgxa in range(len(pyh__stdnx))])
        lkl__xzyox = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{bdstd__pkgxa}], i)' for
            bdstd__pkgxa in range(len(pyh__stdnx))])
        ozty__lgtiq += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({buam__xonhc},), ({lkl__xzyox},))
"""
        ozty__lgtiq += '    if data_val not in arr_map:\n'
        ozty__lgtiq += '      set_val = len(arr_map)\n'
        ozty__lgtiq += '      values_tup = data_val._data\n'
        ozty__lgtiq += '      nulls_tup = data_val._null_values\n'
        for bdstd__pkgxa, ktv__hudo in enumerate(pyh__stdnx):
            ozty__lgtiq += (
                f'      in_lst_{bdstd__pkgxa}.append(values_tup[{bdstd__pkgxa}])\n'
                )
            ozty__lgtiq += (
                f'      null_in_lst_{bdstd__pkgxa}.append(nulls_tup[{bdstd__pkgxa}])\n'
                )
            if is_str_arr_type(ktv__hudo):
                ozty__lgtiq += f"""      total_len_{bdstd__pkgxa}  += nulls_tup[{bdstd__pkgxa}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{bdstd__pkgxa}], i)
"""
        ozty__lgtiq += '      arr_map[data_val] = len(arr_map)\n'
        ozty__lgtiq += '    else:\n'
        ozty__lgtiq += '      set_val = arr_map[data_val]\n'
        ozty__lgtiq += '    map_vector[i] = set_val\n'
        ozty__lgtiq += '  n_rows = len(arr_map)\n'
        for bdstd__pkgxa, ktv__hudo in enumerate(pyh__stdnx):
            if is_str_arr_type(ktv__hudo):
                ozty__lgtiq += f"""  out_arr_{bdstd__pkgxa} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{bdstd__pkgxa})
"""
            else:
                ozty__lgtiq += f"""  out_arr_{bdstd__pkgxa} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{bdstd__pkgxa}], (-1,))
"""
        ozty__lgtiq += '  for j in range(len(arr_map)):\n'
        for bdstd__pkgxa in range(len(pyh__stdnx)):
            ozty__lgtiq += f'    if null_in_lst_{bdstd__pkgxa}[j]:\n'
            ozty__lgtiq += (
                f'      bodo.libs.array_kernels.setna(out_arr_{bdstd__pkgxa}, j)\n'
                )
            ozty__lgtiq += '    else:\n'
            ozty__lgtiq += (
                f'      out_arr_{bdstd__pkgxa}[j] = in_lst_{bdstd__pkgxa}[j]\n'
                )
        efozw__kudy = ', '.join([f'out_arr_{bdstd__pkgxa}' for bdstd__pkgxa in
            range(len(pyh__stdnx))])
        ozty__lgtiq += "  ev.add_attribute('n_map_entries', n_rows)\n"
        ozty__lgtiq += '  ev.finalize()\n'
        ozty__lgtiq += f'  return ({efozw__kudy},), map_vector\n'
    else:
        ozty__lgtiq += '  in_arr = in_arr_tup[0]\n'
        ozty__lgtiq += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        ozty__lgtiq += '  map_vector = np.empty(n, np.int64)\n'
        ozty__lgtiq += '  is_na = 0\n'
        ozty__lgtiq += '  in_lst = []\n'
        ozty__lgtiq += '  na_idxs = []\n'
        if is_str_arr_type(pyh__stdnx[0]):
            ozty__lgtiq += '  total_len = 0\n'
        ozty__lgtiq += '  for i in range(n):\n'
        ozty__lgtiq += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        ozty__lgtiq += '      is_na = 1\n'
        ozty__lgtiq += '      # Always put NA in the last location.\n'
        ozty__lgtiq += '      # We use -1 as a placeholder\n'
        ozty__lgtiq += '      set_val = -1\n'
        ozty__lgtiq += '      na_idxs.append(i)\n'
        ozty__lgtiq += '    else:\n'
        ozty__lgtiq += '      data_val = in_arr[i]\n'
        ozty__lgtiq += '      if data_val not in arr_map:\n'
        ozty__lgtiq += '        set_val = len(arr_map)\n'
        ozty__lgtiq += '        in_lst.append(data_val)\n'
        if is_str_arr_type(pyh__stdnx[0]):
            ozty__lgtiq += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        ozty__lgtiq += '        arr_map[data_val] = len(arr_map)\n'
        ozty__lgtiq += '      else:\n'
        ozty__lgtiq += '        set_val = arr_map[data_val]\n'
        ozty__lgtiq += '    map_vector[i] = set_val\n'
        ozty__lgtiq += '  map_vector[na_idxs] = len(arr_map)\n'
        ozty__lgtiq += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(pyh__stdnx[0]):
            ozty__lgtiq += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            ozty__lgtiq += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        ozty__lgtiq += '  for j in range(len(arr_map)):\n'
        ozty__lgtiq += '    out_arr[j] = in_lst[j]\n'
        ozty__lgtiq += '  if is_na:\n'
        ozty__lgtiq += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        ozty__lgtiq += "  ev.add_attribute('n_map_entries', n_rows)\n"
        ozty__lgtiq += '  ev.finalize()\n'
        ozty__lgtiq += f'  return (out_arr,), map_vector\n'
    xdu__dvbwc = {}
    exec(ozty__lgtiq, {'bodo': bodo, 'np': np, 'tracing': tracing}, xdu__dvbwc)
    impl = xdu__dvbwc['impl']
    return impl
