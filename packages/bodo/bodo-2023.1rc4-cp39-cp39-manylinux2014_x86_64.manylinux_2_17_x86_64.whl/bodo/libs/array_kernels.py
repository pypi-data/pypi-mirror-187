"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_local_dictionary, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType, init_dict_arr
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, alloc_int_array
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import pre_alloc_string_array, str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_bin_arr_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr in (boolean_array,
        datetime_date_array_type, datetime_timedelta_array_type,
        string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr, types.Array) and isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        nqpp__sij = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = nqpp__sij
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        nqpp__sij = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = nqpp__sij
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            kpwvn__mjm = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            kpwvn__mjm[ind + 1] = kpwvn__mjm[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            kpwvn__mjm = bodo.libs.array_item_arr_ext.get_offsets(arr)
            kpwvn__mjm[ind + 1] = kpwvn__mjm[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            kpwvn__mjm = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            kpwvn__mjm[ind + 1] = kpwvn__mjm[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if isinstance(arr, bodo.TimeArrayType):

        def setna_time(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_time
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def copy_array_element(out_arr, out_ind, in_arr, in_ind):
    pass


@overload(copy_array_element)
def overload_copy_array_element(out_arr, out_ind, in_arr, in_ind):
    if out_arr == bodo.string_array_type and is_str_arr_type(in_arr):

        def impl_str(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                bodo.libs.str_arr_ext.get_str_arr_item_copy(out_arr,
                    out_ind, in_arr, in_ind)
        return impl_str
    if isinstance(out_arr, DatetimeArrayType) and isinstance(in_arr,
        DatetimeArrayType) and out_arr.tz == in_arr.tz:

        def impl_dt(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                out_arr._data[out_ind] = in_arr._data[in_ind]
        return impl_dt

    def impl(out_arr, out_ind, in_arr, in_ind):
        if bodo.libs.array_kernels.isna(in_arr, in_ind):
            bodo.libs.array_kernels.setna(out_arr, out_ind)
        else:
            out_arr[out_ind] = in_arr[in_ind]
    return impl


def setna_tup(arr_tup, ind, int_nan_const=0):
    pass


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    dqb__klj = arr_tup.count
    zyz__ubryr = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(dqb__klj):
        zyz__ubryr += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    zyz__ubryr += '  return\n'
    xosu__soj = {}
    exec(zyz__ubryr, {'setna': setna}, xosu__soj)
    impl = xosu__soj['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        gyei__hlg = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(gyei__hlg.start, gyei__hlg.stop, gyei__hlg.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        aphmb__klr = 'n'
        yevpp__dccud = 'n_pes'
        fdk__trcz = 'min_op'
    else:
        aphmb__klr = 'n-1, -1, -1'
        yevpp__dccud = '-1'
        fdk__trcz = 'max_op'
    zyz__ubryr = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {yevpp__dccud}
    for i in range({aphmb__klr}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {fdk__trcz}))
        if possible_valid_rank != {yevpp__dccud}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    xosu__soj = {}
    exec(zyz__ubryr, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, xosu__soj)
    impl = xosu__soj['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    somzp__jufl = array_to_info(arr)
    _median_series_computation(res, somzp__jufl, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(somzp__jufl)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    somzp__jufl = array_to_info(arr)
    _autocorr_series_computation(res, somzp__jufl, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(somzp__jufl)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    somzp__jufl = array_to_info(arr)
    _compute_series_monotonicity(res, somzp__jufl, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(somzp__jufl)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    xnirq__pyb = res[0] > 0.5
    return xnirq__pyb


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        bhvs__hxn = '-'
        sxho__kpqmb = 'index_arr[0] > threshhold_date'
        aphmb__klr = '1, n+1'
        xpft__wldpe = 'index_arr[-i] <= threshhold_date'
        ifmx__bypjv = 'i - 1'
    else:
        bhvs__hxn = '+'
        sxho__kpqmb = 'index_arr[-1] < threshhold_date'
        aphmb__klr = 'n'
        xpft__wldpe = 'index_arr[i] >= threshhold_date'
        ifmx__bypjv = 'i'
    zyz__ubryr = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        zyz__ubryr += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        zyz__ubryr += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            zyz__ubryr += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            zyz__ubryr += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            zyz__ubryr += '    else:\n'
            zyz__ubryr += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            zyz__ubryr += (
                f'    threshhold_date = initial_date {bhvs__hxn} date_offset\n'
                )
    else:
        zyz__ubryr += f'  threshhold_date = initial_date {bhvs__hxn} offset\n'
    zyz__ubryr += '  local_valid = 0\n'
    zyz__ubryr += f'  n = len(index_arr)\n'
    zyz__ubryr += f'  if n:\n'
    zyz__ubryr += f'    if {sxho__kpqmb}:\n'
    zyz__ubryr += '      loc_valid = n\n'
    zyz__ubryr += '    else:\n'
    zyz__ubryr += f'      for i in range({aphmb__klr}):\n'
    zyz__ubryr += f'        if {xpft__wldpe}:\n'
    zyz__ubryr += f'          loc_valid = {ifmx__bypjv}\n'
    zyz__ubryr += '          break\n'
    zyz__ubryr += '  if is_parallel:\n'
    zyz__ubryr += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    zyz__ubryr += '    return total_valid\n'
    zyz__ubryr += '  else:\n'
    zyz__ubryr += '    return loc_valid\n'
    xosu__soj = {}
    exec(zyz__ubryr, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, xosu__soj)
    return xosu__soj['impl']


def quantile(A, q):
    pass


def quantile_parallel(A, q):
    pass


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, FloatingArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    kuntr__nts = numba_to_c_type(sig.args[0].dtype)
    zyc__jegn = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), kuntr__nts))
    kvwcm__dvyc = args[0]
    kyfd__wyzx = sig.args[0]
    if isinstance(kyfd__wyzx, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        kvwcm__dvyc = cgutils.create_struct_proxy(kyfd__wyzx)(context,
            builder, kvwcm__dvyc).data
        kyfd__wyzx = types.Array(kyfd__wyzx.dtype, 1, 'C')
    assert kyfd__wyzx.ndim == 1
    arr = make_array(kyfd__wyzx)(context, builder, kvwcm__dvyc)
    vdw__wyh = builder.extract_value(arr.shape, 0)
    rgij__kdgz = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        vdw__wyh, args[1], builder.load(zyc__jegn)]
    rexc__dwtqb = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    uyw__owae = lir.FunctionType(lir.DoubleType(), rexc__dwtqb)
    kth__tamci = cgutils.get_or_insert_function(builder.module, uyw__owae,
        name='quantile_sequential')
    izj__ayg = builder.call(kth__tamci, rgij__kdgz)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return izj__ayg


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    kuntr__nts = numba_to_c_type(sig.args[0].dtype)
    zyc__jegn = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), kuntr__nts))
    kvwcm__dvyc = args[0]
    kyfd__wyzx = sig.args[0]
    if isinstance(kyfd__wyzx, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        kvwcm__dvyc = cgutils.create_struct_proxy(kyfd__wyzx)(context,
            builder, kvwcm__dvyc).data
        kyfd__wyzx = types.Array(kyfd__wyzx.dtype, 1, 'C')
    assert kyfd__wyzx.ndim == 1
    arr = make_array(kyfd__wyzx)(context, builder, kvwcm__dvyc)
    vdw__wyh = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        hvnk__ycv = args[2]
    else:
        hvnk__ycv = vdw__wyh
    rgij__kdgz = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        vdw__wyh, hvnk__ycv, args[1], builder.load(zyc__jegn)]
    rexc__dwtqb = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    uyw__owae = lir.FunctionType(lir.DoubleType(), rexc__dwtqb)
    kth__tamci = cgutils.get_or_insert_function(builder.module, uyw__owae,
        name='quantile_parallel')
    izj__ayg = builder.call(kth__tamci, rgij__kdgz)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return izj__ayg


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        lms__lpwee = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        lms__lpwee[0] = True
        nmu__hctd = pd.isna(arr)
        for i in range(1, len(arr)):
            if nmu__hctd[i] and nmu__hctd[i - 1]:
                lms__lpwee[i] = False
            elif nmu__hctd[i] or nmu__hctd[i - 1]:
                lms__lpwee[i] = True
            else:
                lms__lpwee[i] = arr[i] != arr[i - 1]
        return lms__lpwee
    return impl


def rank(arr, method='average', na_option='keep', ascending=True, pct=False):
    pass


@overload(rank, no_unliteral=True, inline='always')
def overload_rank(arr, method='average', na_option='keep', ascending=True,
    pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_str(na_option):
        raise_bodo_error(
            "Series.rank(): 'na_option' argument must be a constant string")
    na_option = get_overload_const_str(na_option)
    if not is_overload_constant_bool(ascending):
        raise_bodo_error(
            "Series.rank(): 'ascending' argument must be a constant boolean")
    ascending = get_overload_const_bool(ascending)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    if method == 'first' and not ascending:
        raise BodoError(
            "Series.rank(): method='first' with ascending=False is currently unsupported."
            )
    zyz__ubryr = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    zyz__ubryr += '  na_idxs = pd.isna(arr)\n'
    zyz__ubryr += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    zyz__ubryr += '  nas = sum(na_idxs)\n'
    if not ascending:
        zyz__ubryr += '  if nas and nas < (sorter.size - 1):\n'
        zyz__ubryr += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        zyz__ubryr += '  else:\n'
        zyz__ubryr += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        zyz__ubryr += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    zyz__ubryr += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    zyz__ubryr += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        zyz__ubryr += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        zyz__ubryr += '    inv,\n'
        zyz__ubryr += '    new_dtype=np.float64,\n'
        zyz__ubryr += '    copy=True,\n'
        zyz__ubryr += '    nan_to_str=False,\n'
        zyz__ubryr += '    from_series=True,\n'
        zyz__ubryr += '    ) + 1\n'
    else:
        zyz__ubryr += '  arr = arr[sorter]\n'
        zyz__ubryr += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        zyz__ubryr += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            zyz__ubryr += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            zyz__ubryr += '    dense,\n'
            zyz__ubryr += '    new_dtype=np.float64,\n'
            zyz__ubryr += '    copy=True,\n'
            zyz__ubryr += '    nan_to_str=False,\n'
            zyz__ubryr += '    from_series=True,\n'
            zyz__ubryr += '  )\n'
        else:
            zyz__ubryr += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            zyz__ubryr += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                zyz__ubryr += '  ret = count_float[dense]\n'
            elif method == 'min':
                zyz__ubryr += '  ret = count_float[dense - 1] + 1\n'
            else:
                zyz__ubryr += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                zyz__ubryr += '  ret[na_idxs] = -1\n'
            zyz__ubryr += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            zyz__ubryr += '  div_val = arr.size - nas\n'
        else:
            zyz__ubryr += '  div_val = arr.size\n'
        zyz__ubryr += '  for i in range(len(ret)):\n'
        zyz__ubryr += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        zyz__ubryr += '  ret[na_idxs] = np.nan\n'
    zyz__ubryr += '  return ret\n'
    xosu__soj = {}
    exec(zyz__ubryr, {'np': np, 'pd': pd, 'bodo': bodo}, xosu__soj)
    return xosu__soj['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    hmdo__lgs = start
    gabz__icipv = 2 * start + 1
    ats__lgl = 2 * start + 2
    if gabz__icipv < n and not cmp_f(arr[gabz__icipv], arr[hmdo__lgs]):
        hmdo__lgs = gabz__icipv
    if ats__lgl < n and not cmp_f(arr[ats__lgl], arr[hmdo__lgs]):
        hmdo__lgs = ats__lgl
    if hmdo__lgs != start:
        arr[start], arr[hmdo__lgs] = arr[hmdo__lgs], arr[start]
        ind_arr[start], ind_arr[hmdo__lgs] = ind_arr[hmdo__lgs], ind_arr[start]
        min_heapify(arr, ind_arr, n, hmdo__lgs, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        ovbu__mopa = np.empty(k, A.dtype)
        yjsbx__ivk = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                ovbu__mopa[ind] = A[i]
                yjsbx__ivk[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            ovbu__mopa = ovbu__mopa[:ind]
            yjsbx__ivk = yjsbx__ivk[:ind]
        return ovbu__mopa, yjsbx__ivk, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        zllar__apaas = np.sort(A)
        fqpf__csogn = index_arr[np.argsort(A)]
        siytn__fdq = pd.Series(zllar__apaas).notna().values
        zllar__apaas = zllar__apaas[siytn__fdq]
        fqpf__csogn = fqpf__csogn[siytn__fdq]
        if is_largest:
            zllar__apaas = zllar__apaas[::-1]
            fqpf__csogn = fqpf__csogn[::-1]
        return np.ascontiguousarray(zllar__apaas), np.ascontiguousarray(
            fqpf__csogn)
    ovbu__mopa, yjsbx__ivk, start = select_k_nonan(A, index_arr, m, k)
    yjsbx__ivk = yjsbx__ivk[ovbu__mopa.argsort()]
    ovbu__mopa.sort()
    if not is_largest:
        ovbu__mopa = np.ascontiguousarray(ovbu__mopa[::-1])
        yjsbx__ivk = np.ascontiguousarray(yjsbx__ivk[::-1])
    for i in range(start, m):
        if cmp_f(A[i], ovbu__mopa[0]):
            ovbu__mopa[0] = A[i]
            yjsbx__ivk[0] = index_arr[i]
            min_heapify(ovbu__mopa, yjsbx__ivk, k, 0, cmp_f)
    yjsbx__ivk = yjsbx__ivk[ovbu__mopa.argsort()]
    ovbu__mopa.sort()
    if is_largest:
        ovbu__mopa = ovbu__mopa[::-1]
        yjsbx__ivk = yjsbx__ivk[::-1]
    return np.ascontiguousarray(ovbu__mopa), np.ascontiguousarray(yjsbx__ivk)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    ofx__klcnk = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    xepnt__uuv, lcf__rivv = nlargest(A, I, k, is_largest, cmp_f)
    mikq__fik = bodo.libs.distributed_api.gatherv(xepnt__uuv)
    nmsi__orh = bodo.libs.distributed_api.gatherv(lcf__rivv)
    if ofx__klcnk == MPI_ROOT:
        res, gucoi__octqz = nlargest(mikq__fik, nmsi__orh, k, is_largest, cmp_f
            )
    else:
        res = np.empty(k, A.dtype)
        gucoi__octqz = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(gucoi__octqz)
    return res, gucoi__octqz


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    eghpg__tgje, bkycd__ivws = mat.shape
    pcwos__tzd = np.empty((bkycd__ivws, bkycd__ivws), dtype=np.float64)
    for urnx__xfpf in range(bkycd__ivws):
        for yghm__kfzsj in range(urnx__xfpf + 1):
            lnvux__jljb = 0
            ylvrf__rkd = arlyb__byioh = fhomt__ipbp = ucew__aorcv = 0.0
            for i in range(eghpg__tgje):
                if np.isfinite(mat[i, urnx__xfpf]) and np.isfinite(mat[i,
                    yghm__kfzsj]):
                    bxeq__tsl = mat[i, urnx__xfpf]
                    zrz__byctn = mat[i, yghm__kfzsj]
                    lnvux__jljb += 1
                    fhomt__ipbp += bxeq__tsl
                    ucew__aorcv += zrz__byctn
            if parallel:
                lnvux__jljb = bodo.libs.distributed_api.dist_reduce(lnvux__jljb
                    , sum_op)
                fhomt__ipbp = bodo.libs.distributed_api.dist_reduce(fhomt__ipbp
                    , sum_op)
                ucew__aorcv = bodo.libs.distributed_api.dist_reduce(ucew__aorcv
                    , sum_op)
            if lnvux__jljb < minpv:
                pcwos__tzd[urnx__xfpf, yghm__kfzsj] = pcwos__tzd[
                    yghm__kfzsj, urnx__xfpf] = np.nan
            else:
                shglt__tev = fhomt__ipbp / lnvux__jljb
                vxbl__hrno = ucew__aorcv / lnvux__jljb
                fhomt__ipbp = 0.0
                for i in range(eghpg__tgje):
                    if np.isfinite(mat[i, urnx__xfpf]) and np.isfinite(mat[
                        i, yghm__kfzsj]):
                        bxeq__tsl = mat[i, urnx__xfpf] - shglt__tev
                        zrz__byctn = mat[i, yghm__kfzsj] - vxbl__hrno
                        fhomt__ipbp += bxeq__tsl * zrz__byctn
                        ylvrf__rkd += bxeq__tsl * bxeq__tsl
                        arlyb__byioh += zrz__byctn * zrz__byctn
                if parallel:
                    fhomt__ipbp = bodo.libs.distributed_api.dist_reduce(
                        fhomt__ipbp, sum_op)
                    ylvrf__rkd = bodo.libs.distributed_api.dist_reduce(
                        ylvrf__rkd, sum_op)
                    arlyb__byioh = bodo.libs.distributed_api.dist_reduce(
                        arlyb__byioh, sum_op)
                jnwab__ahcb = lnvux__jljb - 1.0 if cov else sqrt(ylvrf__rkd *
                    arlyb__byioh)
                if jnwab__ahcb != 0.0:
                    pcwos__tzd[urnx__xfpf, yghm__kfzsj] = pcwos__tzd[
                        yghm__kfzsj, urnx__xfpf] = fhomt__ipbp / jnwab__ahcb
                else:
                    pcwos__tzd[urnx__xfpf, yghm__kfzsj] = pcwos__tzd[
                        yghm__kfzsj, urnx__xfpf] = np.nan
    return pcwos__tzd


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    oef__jkprj = n != 1
    zyz__ubryr = 'def impl(data, parallel=False):\n'
    zyz__ubryr += '  if parallel:\n'
    hoaaa__hheu = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    zyz__ubryr += f'    cpp_table = arr_info_list_to_table([{hoaaa__hheu}])\n'
    zyz__ubryr += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    hyxk__cmpp = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    zyz__ubryr += f'    data = ({hyxk__cmpp},)\n'
    zyz__ubryr += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    zyz__ubryr += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    zyz__ubryr += '    bodo.libs.array.delete_table(cpp_table)\n'
    zyz__ubryr += '  n = len(data[0])\n'
    zyz__ubryr += '  out = np.empty(n, np.bool_)\n'
    zyz__ubryr += '  uniqs = dict()\n'
    if oef__jkprj:
        zyz__ubryr += '  for i in range(n):\n'
        ddgv__iref = ', '.join(f'data[{i}][i]' for i in range(n))
        ddo__fmofd = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        zyz__ubryr += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({ddgv__iref},), ({ddo__fmofd},))
"""
        zyz__ubryr += '    if val in uniqs:\n'
        zyz__ubryr += '      out[i] = True\n'
        zyz__ubryr += '    else:\n'
        zyz__ubryr += '      out[i] = False\n'
        zyz__ubryr += '      uniqs[val] = 0\n'
    else:
        zyz__ubryr += '  data = data[0]\n'
        zyz__ubryr += '  hasna = False\n'
        zyz__ubryr += '  for i in range(n):\n'
        zyz__ubryr += '    if bodo.libs.array_kernels.isna(data, i):\n'
        zyz__ubryr += '      out[i] = hasna\n'
        zyz__ubryr += '      hasna = True\n'
        zyz__ubryr += '    else:\n'
        zyz__ubryr += '      val = data[i]\n'
        zyz__ubryr += '      if val in uniqs:\n'
        zyz__ubryr += '        out[i] = True\n'
        zyz__ubryr += '      else:\n'
        zyz__ubryr += '        out[i] = False\n'
        zyz__ubryr += '        uniqs[val] = 0\n'
    zyz__ubryr += '  if parallel:\n'
    zyz__ubryr += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    zyz__ubryr += '  return out\n'
    xosu__soj = {}
    exec(zyz__ubryr, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        xosu__soj)
    impl = xosu__soj['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    dqb__klj = len(data)
    zyz__ubryr = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    zyz__ubryr += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(dqb__klj))
        )
    zyz__ubryr += '  table_total = arr_info_list_to_table(info_list_total)\n'
    zyz__ubryr += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(dqb__klj))
    for fggpb__xgo in range(dqb__klj):
        zyz__ubryr += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(fggpb__xgo, fggpb__xgo, fggpb__xgo))
    zyz__ubryr += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(dqb__klj))
    zyz__ubryr += '  delete_table(out_table)\n'
    zyz__ubryr += '  delete_table(table_total)\n'
    zyz__ubryr += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(dqb__klj)))
    xosu__soj = {}
    exec(zyz__ubryr, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, xosu__soj)
    impl = xosu__soj['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    dqb__klj = len(data)
    zyz__ubryr = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    zyz__ubryr += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(dqb__klj))
        )
    zyz__ubryr += '  table_total = arr_info_list_to_table(info_list_total)\n'
    zyz__ubryr += '  keep_i = 0\n'
    zyz__ubryr += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for fggpb__xgo in range(dqb__klj):
        zyz__ubryr += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(fggpb__xgo, fggpb__xgo, fggpb__xgo))
    zyz__ubryr += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(dqb__klj))
    zyz__ubryr += '  delete_table(out_table)\n'
    zyz__ubryr += '  delete_table(table_total)\n'
    zyz__ubryr += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(dqb__klj)))
    xosu__soj = {}
    exec(zyz__ubryr, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, xosu__soj)
    impl = xosu__soj['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        lpb__ubrvs = [array_to_info(data_arr)]
        dpcwt__fmxrd = arr_info_list_to_table(lpb__ubrvs)
        yite__cffvg = 0
        mbpb__enuqe = drop_duplicates_table(dpcwt__fmxrd, parallel, 1,
            yite__cffvg, False, True)
        out_arr = info_to_array(info_from_table(mbpb__enuqe, 0), data_arr)
        delete_table(mbpb__enuqe)
        delete_table(dpcwt__fmxrd)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    elx__kqzw = len(data.types)
    rok__cnz = [('out' + str(i)) for i in range(elx__kqzw)]
    yme__joz = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    nzg__klj = ['isna(data[{}], i)'.format(i) for i in yme__joz]
    qni__begdk = 'not ({})'.format(' or '.join(nzg__klj))
    if not is_overload_none(thresh):
        qni__begdk = '(({}) <= ({}) - thresh)'.format(' + '.join(nzg__klj),
            elx__kqzw - 1)
    elif how == 'all':
        qni__begdk = 'not ({})'.format(' and '.join(nzg__klj))
    zyz__ubryr = 'def _dropna_imp(data, how, thresh, subset):\n'
    zyz__ubryr += '  old_len = len(data[0])\n'
    zyz__ubryr += '  new_len = 0\n'
    zyz__ubryr += '  for i in range(old_len):\n'
    zyz__ubryr += '    if {}:\n'.format(qni__begdk)
    zyz__ubryr += '      new_len += 1\n'
    for i, out in enumerate(rok__cnz):
        if isinstance(data[i], bodo.CategoricalArrayType):
            zyz__ubryr += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            zyz__ubryr += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    zyz__ubryr += '  curr_ind = 0\n'
    zyz__ubryr += '  for i in range(old_len):\n'
    zyz__ubryr += '    if {}:\n'.format(qni__begdk)
    for i in range(elx__kqzw):
        zyz__ubryr += '      if isna(data[{}], i):\n'.format(i)
        zyz__ubryr += '        setna({}, curr_ind)\n'.format(rok__cnz[i])
        zyz__ubryr += '      else:\n'
        zyz__ubryr += '        {}[curr_ind] = data[{}][i]\n'.format(rok__cnz
            [i], i)
    zyz__ubryr += '      curr_ind += 1\n'
    zyz__ubryr += '  return {}\n'.format(', '.join(rok__cnz))
    xosu__soj = {}
    uhc__nogs = {'t{}'.format(i): iavs__sjjyz for i, iavs__sjjyz in
        enumerate(data.types)}
    uhc__nogs.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(zyz__ubryr, uhc__nogs, xosu__soj)
    lbkoh__apr = xosu__soj['_dropna_imp']
    return lbkoh__apr


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        kyfd__wyzx = arr.dtype
        dipty__psrd = kyfd__wyzx.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            xhi__qckb = init_nested_counts(dipty__psrd)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                xhi__qckb = add_nested_counts(xhi__qckb, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, kyfd__wyzx, xhi__qckb)
            for hpq__exoll in range(n):
                if bodo.libs.array_kernels.isna(arr, hpq__exoll):
                    setna(out_arr, hpq__exoll)
                    continue
                val = arr[hpq__exoll]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, hpq__exoll)
                    continue
                out_arr[hpq__exoll] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    tmpqn__trq = _to_readonly(arr_types.types[0])
    return all(isinstance(iavs__sjjyz, CategoricalArrayType) and 
        _to_readonly(iavs__sjjyz) == tmpqn__trq for iavs__sjjyz in
        arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        ykvjk__qarrl = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            vnqjc__wpjo = 0
            xedm__hnj = []
            for A in arr_list:
                zwy__awipg = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                xedm__hnj.append(bodo.libs.array_item_arr_ext.get_data(A))
                vnqjc__wpjo += zwy__awipg
            qain__wvi = np.empty(vnqjc__wpjo + 1, offset_type)
            kxk__dpx = bodo.libs.array_kernels.concat(xedm__hnj)
            eknv__akn = np.empty(vnqjc__wpjo + 7 >> 3, np.uint8)
            kucrh__hktqq = 0
            lahvy__umy = 0
            for A in arr_list:
                eiqw__vwt = bodo.libs.array_item_arr_ext.get_offsets(A)
                swnr__ron = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                zwy__awipg = len(A)
                isft__gfei = eiqw__vwt[zwy__awipg]
                for i in range(zwy__awipg):
                    qain__wvi[i + kucrh__hktqq] = eiqw__vwt[i] + lahvy__umy
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        swnr__ron, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eknv__akn, i +
                        kucrh__hktqq, euhf__cpzk)
                kucrh__hktqq += zwy__awipg
                lahvy__umy += isft__gfei
            qain__wvi[kucrh__hktqq] = lahvy__umy
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                vnqjc__wpjo, kxk__dpx, qain__wvi, eknv__akn)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        svez__ehtj = arr_list.dtype.names
        zyz__ubryr = 'def struct_array_concat_impl(arr_list):\n'
        zyz__ubryr += f'    n_all = 0\n'
        for i in range(len(svez__ehtj)):
            zyz__ubryr += f'    concat_list{i} = []\n'
        zyz__ubryr += '    for A in arr_list:\n'
        zyz__ubryr += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(svez__ehtj)):
            zyz__ubryr += f'        concat_list{i}.append(data_tuple[{i}])\n'
        zyz__ubryr += '        n_all += len(A)\n'
        zyz__ubryr += '    n_bytes = (n_all + 7) >> 3\n'
        zyz__ubryr += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        zyz__ubryr += '    curr_bit = 0\n'
        zyz__ubryr += '    for A in arr_list:\n'
        zyz__ubryr += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        zyz__ubryr += '        for j in range(len(A)):\n'
        zyz__ubryr += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        zyz__ubryr += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        zyz__ubryr += '            curr_bit += 1\n'
        zyz__ubryr += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        toql__qqm = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(svez__ehtj))])
        zyz__ubryr += f'        ({toql__qqm},),\n'
        zyz__ubryr += '        new_mask,\n'
        zyz__ubryr += f'        {svez__ehtj},\n'
        zyz__ubryr += '    )\n'
        xosu__soj = {}
        exec(zyz__ubryr, {'bodo': bodo, 'np': np}, xosu__soj)
        return xosu__soj['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        hsog__hpl = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            tztx__vrelt = 0
            for A in arr_list:
                tztx__vrelt += len(A)
            hpht__ujt = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                tztx__vrelt, hsog__hpl)
            crwsh__dflbv = 0
            for A in arr_list:
                for i in range(len(A)):
                    hpht__ujt[i + crwsh__dflbv] = A[i]
                crwsh__dflbv += len(A)
            return hpht__ujt
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            tztx__vrelt = 0
            for A in arr_list:
                tztx__vrelt += len(A)
            hpht__ujt = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(tztx__vrelt))
            crwsh__dflbv = 0
            for A in arr_list:
                for i in range(len(A)):
                    hpht__ujt._data[i + crwsh__dflbv] = A._data[i]
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hpht__ujt.
                        _null_bitmap, i + crwsh__dflbv, euhf__cpzk)
                crwsh__dflbv += len(A)
            return hpht__ujt
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            tztx__vrelt = 0
            for A in arr_list:
                tztx__vrelt += len(A)
            hpht__ujt = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(tztx__vrelt))
            crwsh__dflbv = 0
            for A in arr_list:
                for i in range(len(A)):
                    hpht__ujt._days_data[i + crwsh__dflbv] = A._days_data[i]
                    hpht__ujt._seconds_data[i + crwsh__dflbv
                        ] = A._seconds_data[i]
                    hpht__ujt._microseconds_data[i + crwsh__dflbv
                        ] = A._microseconds_data[i]
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hpht__ujt.
                        _null_bitmap, i + crwsh__dflbv, euhf__cpzk)
                crwsh__dflbv += len(A)
            return hpht__ujt
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        ivp__qfrn = arr_list.dtype.precision
        ptyb__rzx = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            tztx__vrelt = 0
            for A in arr_list:
                tztx__vrelt += len(A)
            hpht__ujt = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                tztx__vrelt, ivp__qfrn, ptyb__rzx)
            crwsh__dflbv = 0
            for A in arr_list:
                for i in range(len(A)):
                    hpht__ujt._data[i + crwsh__dflbv] = A._data[i]
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hpht__ujt.
                        _null_bitmap, i + crwsh__dflbv, euhf__cpzk)
                crwsh__dflbv += len(A)
            return hpht__ujt
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        iavs__sjjyz) for iavs__sjjyz in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            kxs__higea = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    kxs__higea = arr_list.types[i]
                    break
        else:
            kxs__higea = arr_list.dtype
        if kxs__higea == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                ews__ybvlc = 0
                iscot__ihw = 0
                iuejo__qivld = 0
                for A in arr_list:
                    data_arr = A._data
                    vie__zjorx = A._indices
                    iuejo__qivld += len(vie__zjorx)
                    ews__ybvlc += len(data_arr)
                    iscot__ihw += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                pqgpi__pbasr = pre_alloc_string_array(ews__ybvlc, iscot__ihw)
                ozk__qww = bodo.libs.int_arr_ext.alloc_int_array(iuejo__qivld,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(pqgpi__pbasr, -1)
                bipmw__nkbg = 0
                ybn__xfr = 0
                karb__aly = 0
                for A in arr_list:
                    data_arr = A._data
                    vie__zjorx = A._indices
                    iuejo__qivld = len(vie__zjorx)
                    bodo.libs.str_arr_ext.set_string_array_range(pqgpi__pbasr,
                        data_arr, bipmw__nkbg, ybn__xfr)
                    for i in range(iuejo__qivld):
                        if bodo.libs.array_kernels.isna(vie__zjorx, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            vie__zjorx[i]):
                            bodo.libs.array_kernels.setna(ozk__qww, 
                                karb__aly + i)
                        else:
                            ozk__qww[karb__aly + i] = bipmw__nkbg + vie__zjorx[
                                i]
                    bipmw__nkbg += len(data_arr)
                    ybn__xfr += bodo.libs.str_arr_ext.num_total_chars(data_arr)
                    karb__aly += iuejo__qivld
                out_arr = init_dict_arr(pqgpi__pbasr, ozk__qww, False, False)
                ytdi__ngtho = drop_duplicates_local_dictionary(out_arr, False)
                return ytdi__ngtho
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            ews__ybvlc = 0
            iscot__ihw = 0
            for A in arr_list:
                arr = A
                ews__ybvlc += len(arr)
                iscot__ihw += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(ews__ybvlc, kxs__higea, (
                iscot__ihw,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            bipmw__nkbg = 0
            ybn__xfr = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    bipmw__nkbg, ybn__xfr)
                bipmw__nkbg += len(arr)
                ybn__xfr += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(iavs__sjjyz.dtype, types.Integer) for
        iavs__sjjyz in arr_list.types) and any(isinstance(iavs__sjjyz,
        IntegerArrayType) for iavs__sjjyz in arr_list.types):

        def impl_int_arr_list(arr_list):
            kfnw__kkf = convert_to_nullable_tup(arr_list)
            ombr__fuf = []
            utar__ltr = 0
            for A in kfnw__kkf:
                ombr__fuf.append(A._data)
                utar__ltr += len(A)
            kxk__dpx = bodo.libs.array_kernels.concat(ombr__fuf)
            otw__ppzv = utar__ltr + 7 >> 3
            gqnye__krh = np.empty(otw__ppzv, np.uint8)
            tjwjh__qht = 0
            for A in kfnw__kkf:
                abza__ztnn = A._null_bitmap
                for hpq__exoll in range(len(A)):
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        abza__ztnn, hpq__exoll)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gqnye__krh,
                        tjwjh__qht, euhf__cpzk)
                    tjwjh__qht += 1
            return bodo.libs.int_arr_ext.init_integer_array(kxk__dpx,
                gqnye__krh)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(iavs__sjjyz.dtype == types.bool_ for
        iavs__sjjyz in arr_list.types) and any(iavs__sjjyz == boolean_array for
        iavs__sjjyz in arr_list.types):

        def impl_bool_arr_list(arr_list):
            kfnw__kkf = convert_to_nullable_tup(arr_list)
            ombr__fuf = []
            utar__ltr = 0
            for A in kfnw__kkf:
                ombr__fuf.append(A._data)
                utar__ltr += len(A)
            kxk__dpx = bodo.libs.array_kernels.concat(ombr__fuf)
            otw__ppzv = utar__ltr + 7 >> 3
            gqnye__krh = np.empty(otw__ppzv, np.uint8)
            tjwjh__qht = 0
            for A in kfnw__kkf:
                abza__ztnn = A._null_bitmap
                for hpq__exoll in range(len(A)):
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        abza__ztnn, hpq__exoll)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gqnye__krh,
                        tjwjh__qht, euhf__cpzk)
                    tjwjh__qht += 1
            return bodo.libs.bool_arr_ext.init_bool_array(kxk__dpx, gqnye__krh)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(iavs__sjjyz.dtype, types.Float) for
        iavs__sjjyz in arr_list.types) and any(isinstance(iavs__sjjyz,
        FloatingArrayType) for iavs__sjjyz in arr_list.types):

        def impl_float_arr_list(arr_list):
            kfnw__kkf = convert_to_nullable_tup(arr_list)
            ombr__fuf = []
            utar__ltr = 0
            for A in kfnw__kkf:
                ombr__fuf.append(A._data)
                utar__ltr += len(A)
            kxk__dpx = bodo.libs.array_kernels.concat(ombr__fuf)
            otw__ppzv = utar__ltr + 7 >> 3
            gqnye__krh = np.empty(otw__ppzv, np.uint8)
            tjwjh__qht = 0
            for A in kfnw__kkf:
                abza__ztnn = A._null_bitmap
                for hpq__exoll in range(len(A)):
                    euhf__cpzk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        abza__ztnn, hpq__exoll)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gqnye__krh,
                        tjwjh__qht, euhf__cpzk)
                    tjwjh__qht += 1
            return bodo.libs.float_arr_ext.init_float_array(kxk__dpx,
                gqnye__krh)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            drpy__irfv = []
            for A in arr_list:
                drpy__irfv.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                drpy__irfv), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        zng__dje = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        zyz__ubryr = 'def impl(arr_list):\n'
        zyz__ubryr += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({zng__dje}, )), arr_list[0].dtype)
"""
        gej__texfc = {}
        exec(zyz__ubryr, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, gej__texfc)
        return gej__texfc['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            utar__ltr = 0
            for A in arr_list:
                utar__ltr += len(A)
            out_arr = np.empty(utar__ltr, dtype)
            vrrvi__bve = 0
            for A in arr_list:
                n = len(A)
                out_arr[vrrvi__bve:vrrvi__bve + n] = A
                vrrvi__bve += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(iavs__sjjyz,
        (types.Array, IntegerArrayType)) and isinstance(iavs__sjjyz.dtype,
        types.Integer) for iavs__sjjyz in arr_list.types) and any(
        isinstance(iavs__sjjyz, types.Array) and isinstance(iavs__sjjyz.
        dtype, types.Float) for iavs__sjjyz in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            axrq__trdz = []
            for A in arr_list:
                axrq__trdz.append(A._data)
            fgqc__zwx = bodo.libs.array_kernels.concat(axrq__trdz)
            pcwos__tzd = bodo.libs.map_arr_ext.init_map_arr(fgqc__zwx)
            return pcwos__tzd
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        grgk__iek = all([(isinstance(akpug__prn, bodo.DatetimeArrayType) or
            isinstance(akpug__prn, types.Array) and akpug__prn.dtype ==
            bodo.datetime64ns) for akpug__prn in arr_list.types])
        if grgk__iek:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for akpug__prn in arr_list:
        if not isinstance(akpug__prn, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(iavs__sjjyz.astype(np.float64) for iavs__sjjyz in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    dqb__klj = len(arr_tup.types)
    zyz__ubryr = 'def f(arr_tup):\n'
    zyz__ubryr += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(dqb__klj)
        ), ',' if dqb__klj == 1 else '')
    xosu__soj = {}
    exec(zyz__ubryr, {'np': np}, xosu__soj)
    xgccg__kje = xosu__soj['f']
    return xgccg__kje


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    dqb__klj = len(arr_tup.types)
    uog__mznu = find_common_np_dtype(arr_tup.types)
    dipty__psrd = None
    vjea__qstk = ''
    if isinstance(uog__mznu, types.Integer):
        dipty__psrd = bodo.libs.int_arr_ext.IntDtype(uog__mznu)
        vjea__qstk = '.astype(out_dtype, False)'
    if isinstance(uog__mznu, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        dipty__psrd = bodo.libs.float_arr_ext.FloatDtype(uog__mznu)
        vjea__qstk = '.astype(out_dtype, False)'
    zyz__ubryr = 'def f(arr_tup):\n'
    zyz__ubryr += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){vjea__qstk}'
         for i in range(dqb__klj)), ',' if dqb__klj == 1 else '')
    xosu__soj = {}
    exec(zyz__ubryr, {'bodo': bodo, 'out_dtype': dipty__psrd}, xosu__soj)
    cue__evp = xosu__soj['f']
    return cue__evp


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, mapbm__emaa = build_set_seen_na(A)
        return len(s) + int(not dropna and mapbm__emaa)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        lrilu__mdi = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        gnt__idmj = len(lrilu__mdi)
        return bodo.libs.distributed_api.dist_reduce(gnt__idmj, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    pass


def accum_func(A, func_name, parallel=False):
    pass


@overload(accum_func, no_unliteral=True)
def accum_func_overload(A, func_name, parallel=False):
    assert is_overload_constant_str(func_name
        ), 'accum_func: func_name should be const'
    nvgyo__unxf = get_overload_const_str(func_name)
    assert nvgyo__unxf in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if nvgyo__unxf == 'cumsum':
        adg__gwvq = A.dtype(0)
        nlh__gvfd = np.int32(Reduce_Type.Sum.value)
        lwz__ibo = np.add
    if nvgyo__unxf == 'cumprod':
        adg__gwvq = A.dtype(1)
        nlh__gvfd = np.int32(Reduce_Type.Prod.value)
        lwz__ibo = np.multiply
    if nvgyo__unxf == 'cummin':
        if isinstance(A.dtype, types.Float):
            adg__gwvq = np.finfo(A.dtype(1).dtype).max
        else:
            adg__gwvq = np.iinfo(A.dtype(1).dtype).max
        nlh__gvfd = np.int32(Reduce_Type.Min.value)
        lwz__ibo = min
    if nvgyo__unxf == 'cummax':
        if isinstance(A.dtype, types.Float):
            adg__gwvq = np.finfo(A.dtype(1).dtype).min
        else:
            adg__gwvq = np.iinfo(A.dtype(1).dtype).min
        nlh__gvfd = np.int32(Reduce_Type.Max.value)
        lwz__ibo = max
    sgpxb__iop = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        lhi__geteu = adg__gwvq
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    lhi__geteu = lwz__ibo(lhi__geteu, A[i])
            lhi__geteu = bodo.libs.distributed_api.dist_exscan(lhi__geteu,
                nlh__gvfd)
            if bodo.get_rank() == 0:
                lhi__geteu = adg__gwvq
        out_arr = bodo.utils.utils.alloc_type(n, sgpxb__iop, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            lhi__geteu = lwz__ibo(lhi__geteu, A[i])
            out_arr[i] = lhi__geteu
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        ngev__vjo = arr_info_list_to_table([array_to_info(A)])
        rbgq__cxk = 1
        yite__cffvg = 0
        mbpb__enuqe = drop_duplicates_table(ngev__vjo, parallel, rbgq__cxk,
            yite__cffvg, dropna, True)
        out_arr = info_to_array(info_from_table(mbpb__enuqe, 0), A)
        delete_table(ngev__vjo)
        delete_table(mbpb__enuqe)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    ykvjk__qarrl = bodo.utils.typing.to_nullable_type(arr.dtype)
    hijj__ietyl = index_arr
    sgsla__gugg = hijj__ietyl.dtype

    def impl(arr, index_arr):
        n = len(arr)
        xhi__qckb = init_nested_counts(ykvjk__qarrl)
        rqlq__fhm = init_nested_counts(sgsla__gugg)
        for i in range(n):
            pwm__pazu = index_arr[i]
            if isna(arr, i):
                xhi__qckb = (xhi__qckb[0] + 1,) + xhi__qckb[1:]
                rqlq__fhm = add_nested_counts(rqlq__fhm, pwm__pazu)
                continue
            duzq__iee = arr[i]
            if len(duzq__iee) == 0:
                xhi__qckb = (xhi__qckb[0] + 1,) + xhi__qckb[1:]
                rqlq__fhm = add_nested_counts(rqlq__fhm, pwm__pazu)
                continue
            xhi__qckb = add_nested_counts(xhi__qckb, duzq__iee)
            for lkn__enro in range(len(duzq__iee)):
                rqlq__fhm = add_nested_counts(rqlq__fhm, pwm__pazu)
        out_arr = bodo.utils.utils.alloc_type(xhi__qckb[0], ykvjk__qarrl,
            xhi__qckb[1:])
        avy__viqlq = bodo.utils.utils.alloc_type(xhi__qckb[0], hijj__ietyl,
            rqlq__fhm)
        lahvy__umy = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, lahvy__umy)
                avy__viqlq[lahvy__umy] = index_arr[i]
                lahvy__umy += 1
                continue
            duzq__iee = arr[i]
            isft__gfei = len(duzq__iee)
            if isft__gfei == 0:
                setna(out_arr, lahvy__umy)
                avy__viqlq[lahvy__umy] = index_arr[i]
                lahvy__umy += 1
                continue
            out_arr[lahvy__umy:lahvy__umy + isft__gfei] = duzq__iee
            avy__viqlq[lahvy__umy:lahvy__umy + isft__gfei] = index_arr[i]
            lahvy__umy += isft__gfei
        return out_arr, avy__viqlq
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    ykvjk__qarrl = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        xhi__qckb = init_nested_counts(ykvjk__qarrl)
        for i in range(n):
            if isna(arr, i):
                xhi__qckb = (xhi__qckb[0] + 1,) + xhi__qckb[1:]
                cxo__sawjh = 1
            else:
                duzq__iee = arr[i]
                iazyt__bffi = len(duzq__iee)
                if iazyt__bffi == 0:
                    xhi__qckb = (xhi__qckb[0] + 1,) + xhi__qckb[1:]
                    cxo__sawjh = 1
                    continue
                else:
                    xhi__qckb = add_nested_counts(xhi__qckb, duzq__iee)
                    cxo__sawjh = iazyt__bffi
            if counts[i] != cxo__sawjh:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(xhi__qckb[0], ykvjk__qarrl,
            xhi__qckb[1:])
        lahvy__umy = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, lahvy__umy)
                lahvy__umy += 1
                continue
            duzq__iee = arr[i]
            isft__gfei = len(duzq__iee)
            if isft__gfei == 0:
                setna(out_arr, lahvy__umy)
                lahvy__umy += 1
                continue
            out_arr[lahvy__umy:lahvy__umy + isft__gfei] = duzq__iee
            lahvy__umy += isft__gfei
        return out_arr
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    pass


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one or is_bin_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        gdwys__viutd = 'np.empty(n, np.int64)'
        rgpxa__szxmc = 'out_arr[i] = 1'
        pccdo__lwg = 'max(len(arr[i]), 1)'
    else:
        gdwys__viutd = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        rgpxa__szxmc = 'bodo.libs.array_kernels.setna(out_arr, i)'
        pccdo__lwg = 'len(arr[i])'
    zyz__ubryr = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {gdwys__viutd}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {rgpxa__szxmc}
        else:
            out_arr[i] = {pccdo__lwg}
    return out_arr
    """
    xosu__soj = {}
    exec(zyz__ubryr, {'bodo': bodo, 'numba': numba, 'np': np}, xosu__soj)
    impl = xosu__soj['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    hijj__ietyl = index_arr
    sgsla__gugg = hijj__ietyl.dtype

    def impl(arr, pat, n, index_arr):
        myjid__pdla = pat is not None and len(pat) > 1
        if myjid__pdla:
            nfb__izu = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        gvdf__cbc = len(arr)
        ews__ybvlc = 0
        iscot__ihw = 0
        rqlq__fhm = init_nested_counts(sgsla__gugg)
        for i in range(gvdf__cbc):
            pwm__pazu = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                ews__ybvlc += 1
                rqlq__fhm = add_nested_counts(rqlq__fhm, pwm__pazu)
                continue
            if myjid__pdla:
                mgb__wuuzl = nfb__izu.split(arr[i], maxsplit=n)
            else:
                mgb__wuuzl = arr[i].split(pat, n)
            ews__ybvlc += len(mgb__wuuzl)
            for s in mgb__wuuzl:
                rqlq__fhm = add_nested_counts(rqlq__fhm, pwm__pazu)
                iscot__ihw += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ews__ybvlc,
            iscot__ihw)
        avy__viqlq = bodo.utils.utils.alloc_type(ews__ybvlc, hijj__ietyl,
            rqlq__fhm)
        taet__vzdci = 0
        for hpq__exoll in range(gvdf__cbc):
            if isna(arr, hpq__exoll):
                out_arr[taet__vzdci] = ''
                bodo.libs.array_kernels.setna(out_arr, taet__vzdci)
                avy__viqlq[taet__vzdci] = index_arr[hpq__exoll]
                taet__vzdci += 1
                continue
            if myjid__pdla:
                mgb__wuuzl = nfb__izu.split(arr[hpq__exoll], maxsplit=n)
            else:
                mgb__wuuzl = arr[hpq__exoll].split(pat, n)
            auqdw__eeji = len(mgb__wuuzl)
            out_arr[taet__vzdci:taet__vzdci + auqdw__eeji] = mgb__wuuzl
            avy__viqlq[taet__vzdci:taet__vzdci + auqdw__eeji] = index_arr[
                hpq__exoll]
            taet__vzdci += auqdw__eeji
        return out_arr, avy__viqlq
    return impl


def gen_na_array(n, arr):
    pass


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr, use_dict_arr=False):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if not isinstance(arr, (FloatingArrayType, IntegerArrayType)
        ) and isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr, use_dict_arr=False):
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                out_arr[i] = np.nan
            return out_arr
        return impl_float
    if arr == bodo.dict_str_arr_type and is_overload_true(use_dict_arr):

        def impl_dict(n, arr, use_dict_arr=False):
            sge__musby = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            urmk__jtu = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(urmk__jtu, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(sge__musby,
                urmk__jtu, True, True)
        return impl_dict
    jpdsv__jiv = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, jpdsv__jiv, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(out_arr, i)
        return out_arr
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    pass


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    xgll__vvsc = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, xgll__vvsc)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, xgll__vvsc, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    icg__bzvmb = math.ceil((stop - start) / step)
    return int(max(icg__bzvmb, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(uog__opkj, types.Complex) for uog__opkj in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            xlxi__uotb = (stop - start) / step
            icg__bzvmb = math.ceil(xlxi__uotb.real)
            ffl__uvkc = math.ceil(xlxi__uotb.imag)
            hdbi__hnywp = int(max(min(ffl__uvkc, icg__bzvmb), 0))
            arr = np.empty(hdbi__hnywp, dtype)
            for i in numba.parfors.parfor.internal_prange(hdbi__hnywp):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            hdbi__hnywp = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(hdbi__hnywp, dtype)
            for i in numba.parfors.parfor.internal_prange(hdbi__hnywp):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    pass


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        jrb__qezwq = arr,
        if not inplace:
            jrb__qezwq = arr.copy(),
        hsef__rtm = bodo.libs.str_arr_ext.to_list_if_immutable_arr(jrb__qezwq)
        pkyqo__qvuw = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True
            )
        bodo.libs.timsort.sort(hsef__rtm, 0, n, pkyqo__qvuw)
        if not ascending:
            bodo.libs.timsort.reverseRange(hsef__rtm, 0, n, pkyqo__qvuw)
        bodo.libs.str_arr_ext.cp_str_list_to_array(jrb__qezwq, hsef__rtm)
        return jrb__qezwq[0]
    return impl


def overload_array_max(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    pass


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        pcwos__tzd = []
        for i in range(n):
            if A[i]:
                pcwos__tzd.append(i + offset)
        return np.array(pcwos__tzd, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    xgll__vvsc = element_type(A)
    if xgll__vvsc == types.unicode_type:
        null_value = '""'
    elif xgll__vvsc == types.bool_:
        null_value = 'False'
    elif xgll__vvsc == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif xgll__vvsc == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    taet__vzdci = 'i'
    hiz__aabu = False
    psll__nllsg = get_overload_const_str(method)
    if psll__nllsg in ('ffill', 'pad'):
        vye__mqo = 'n'
        send_right = True
    elif psll__nllsg in ('backfill', 'bfill'):
        vye__mqo = 'n-1, -1, -1'
        send_right = False
        if xgll__vvsc == types.unicode_type:
            taet__vzdci = '(n - 1) - i'
            hiz__aabu = True
    zyz__ubryr = 'def impl(A, method, parallel=False):\n'
    zyz__ubryr += '  A = decode_if_dict_array(A)\n'
    zyz__ubryr += '  has_last_value = False\n'
    zyz__ubryr += f'  last_value = {null_value}\n'
    zyz__ubryr += '  if parallel:\n'
    zyz__ubryr += '    rank = bodo.libs.distributed_api.get_rank()\n'
    zyz__ubryr += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    zyz__ubryr += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    zyz__ubryr += '  n = len(A)\n'
    zyz__ubryr += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    zyz__ubryr += f'  for i in range({vye__mqo}):\n'
    zyz__ubryr += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    zyz__ubryr += (
        f'      bodo.libs.array_kernels.setna(out_arr, {taet__vzdci})\n')
    zyz__ubryr += '      continue\n'
    zyz__ubryr += '    s = A[i]\n'
    zyz__ubryr += '    if bodo.libs.array_kernels.isna(A, i):\n'
    zyz__ubryr += '      s = last_value\n'
    zyz__ubryr += f'    out_arr[{taet__vzdci}] = s\n'
    zyz__ubryr += '    last_value = s\n'
    zyz__ubryr += '    has_last_value = True\n'
    if hiz__aabu:
        zyz__ubryr += '  return out_arr[::-1]\n'
    else:
        zyz__ubryr += '  return out_arr\n'
    qqq__ybhpo = {}
    exec(zyz__ubryr, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, qqq__ybhpo)
    impl = qqq__ybhpo['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        goi__wuds = 0
        wzps__affhv = n_pes - 1
        phme__cmya = np.int32(rank + 1)
        kru__uyngt = np.int32(rank - 1)
        thtf__rpxo = len(in_arr) - 1
        xkih__mmcb = -1
        fwwsy__hvls = -1
    else:
        goi__wuds = n_pes - 1
        wzps__affhv = 0
        phme__cmya = np.int32(rank - 1)
        kru__uyngt = np.int32(rank + 1)
        thtf__rpxo = 0
        xkih__mmcb = len(in_arr)
        fwwsy__hvls = 1
    kwv__awdvq = np.int32(bodo.hiframes.rolling.comm_border_tag)
    ugyp__fwl = np.empty(1, dtype=np.bool_)
    nsfxx__kypvs = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    tdapn__xxcm = np.empty(1, dtype=np.bool_)
    mxl__kgxmr = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    qzck__rbfo = False
    owpl__yeno = null_value
    for i in range(thtf__rpxo, xkih__mmcb, fwwsy__hvls):
        if not isna(in_arr, i):
            qzck__rbfo = True
            owpl__yeno = in_arr[i]
            break
    if rank != goi__wuds:
        rfm__ups = bodo.libs.distributed_api.irecv(ugyp__fwl, 1, kru__uyngt,
            kwv__awdvq, True)
        bodo.libs.distributed_api.wait(rfm__ups, True)
        gobep__ztn = bodo.libs.distributed_api.irecv(nsfxx__kypvs, 1,
            kru__uyngt, kwv__awdvq, True)
        bodo.libs.distributed_api.wait(gobep__ztn, True)
        ovnw__qbiy = ugyp__fwl[0]
        elhe__feb = nsfxx__kypvs[0]
    else:
        ovnw__qbiy = False
        elhe__feb = null_value
    if qzck__rbfo:
        tdapn__xxcm[0] = qzck__rbfo
        mxl__kgxmr[0] = owpl__yeno
    else:
        tdapn__xxcm[0] = ovnw__qbiy
        mxl__kgxmr[0] = elhe__feb
    if rank != wzps__affhv:
        ems__sdx = bodo.libs.distributed_api.isend(tdapn__xxcm, 1,
            phme__cmya, kwv__awdvq, True)
        mdn__zgk = bodo.libs.distributed_api.isend(mxl__kgxmr, 1,
            phme__cmya, kwv__awdvq, True)
    return ovnw__qbiy, elhe__feb


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    qzu__yerme = {'axis': axis, 'kind': kind, 'order': order}
    qoim__hzmcx = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', qzu__yerme, qoim__hzmcx, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    xgll__vvsc = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                vie__zjorx = A._indices
                gvdf__cbc = len(vie__zjorx)
                ozk__qww = alloc_int_array(gvdf__cbc * repeats, np.int32)
                for i in range(gvdf__cbc):
                    taet__vzdci = i * repeats
                    if bodo.libs.array_kernels.isna(vie__zjorx, i):
                        for hpq__exoll in range(repeats):
                            bodo.libs.array_kernels.setna(ozk__qww, 
                                taet__vzdci + hpq__exoll)
                    else:
                        ozk__qww[taet__vzdci:taet__vzdci + repeats
                            ] = vie__zjorx[i]
                return init_dict_arr(data_arr, ozk__qww, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            gvdf__cbc = len(A)
            out_arr = bodo.utils.utils.alloc_type(gvdf__cbc * repeats,
                xgll__vvsc, (-1,))
            for i in range(gvdf__cbc):
                taet__vzdci = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for hpq__exoll in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, taet__vzdci +
                            hpq__exoll)
                else:
                    out_arr[taet__vzdci:taet__vzdci + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            vie__zjorx = A._indices
            gvdf__cbc = len(vie__zjorx)
            ozk__qww = alloc_int_array(repeats.sum(), np.int32)
            taet__vzdci = 0
            for i in range(gvdf__cbc):
                auyqx__ginw = repeats[i]
                if auyqx__ginw < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(vie__zjorx, i):
                    for hpq__exoll in range(auyqx__ginw):
                        bodo.libs.array_kernels.setna(ozk__qww, taet__vzdci +
                            hpq__exoll)
                else:
                    ozk__qww[taet__vzdci:taet__vzdci + auyqx__ginw
                        ] = vie__zjorx[i]
                taet__vzdci += auyqx__ginw
            return init_dict_arr(data_arr, ozk__qww, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        gvdf__cbc = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), xgll__vvsc, (-1,))
        taet__vzdci = 0
        for i in range(gvdf__cbc):
            auyqx__ginw = repeats[i]
            if auyqx__ginw < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for hpq__exoll in range(auyqx__ginw):
                    bodo.libs.array_kernels.setna(out_arr, taet__vzdci +
                        hpq__exoll)
            else:
                out_arr[taet__vzdci:taet__vzdci + auyqx__ginw] = A[i]
            taet__vzdci += auyqx__ginw
        return out_arr
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        kucl__rrph = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(kucl__rrph, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        snpsl__ecdz = bodo.libs.array_kernels.concat([A1, A2])
        fvvuv__uvg = bodo.libs.array_kernels.unique(snpsl__ecdz)
        return pd.Series(fvvuv__uvg).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    qzu__yerme = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    qoim__hzmcx = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', qzu__yerme, qoim__hzmcx, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        xxkfn__usnwi = bodo.libs.array_kernels.unique(A1)
        tlek__gsfz = bodo.libs.array_kernels.unique(A2)
        snpsl__ecdz = bodo.libs.array_kernels.concat([xxkfn__usnwi, tlek__gsfz]
            )
        esfs__zrdq = pd.Series(snpsl__ecdz).sort_values().values
        return slice_array_intersect1d(esfs__zrdq)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    siytn__fdq = arr[1:] == arr[:-1]
    return arr[:-1][siytn__fdq]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    kwv__awdvq = np.int32(bodo.hiframes.rolling.comm_border_tag)
    ocled__urnsq = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        cylk__ndl = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), kwv__awdvq, True)
        bodo.libs.distributed_api.wait(cylk__ndl, True)
    if rank == n_pes - 1:
        return None
    else:
        owsa__wfry = bodo.libs.distributed_api.irecv(ocled__urnsq, 1, np.
            int32(rank + 1), kwv__awdvq, True)
        bodo.libs.distributed_api.wait(owsa__wfry, True)
        return ocled__urnsq[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    siytn__fdq = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            siytn__fdq[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        tmtr__srfrl = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == tmtr__srfrl:
            siytn__fdq[n - 1] = True
    return siytn__fdq


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    qzu__yerme = {'assume_unique': assume_unique}
    qoim__hzmcx = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', qzu__yerme, qoim__hzmcx, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        xxkfn__usnwi = bodo.libs.array_kernels.unique(A1)
        tlek__gsfz = bodo.libs.array_kernels.unique(A2)
        siytn__fdq = calculate_mask_setdiff1d(xxkfn__usnwi, tlek__gsfz)
        return pd.Series(xxkfn__usnwi[siytn__fdq]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    siytn__fdq = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        siytn__fdq &= A1 != A2[i]
    return siytn__fdq


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    qzu__yerme = {'retstep': retstep, 'axis': axis}
    qoim__hzmcx = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', qzu__yerme, qoim__hzmcx, 'numpy')
    kdmx__pofj = False
    if is_overload_none(dtype):
        xgll__vvsc = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            kdmx__pofj = True
        xgll__vvsc = numba.np.numpy_support.as_dtype(dtype).type
    if kdmx__pofj:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            rqr__pjm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, xgll__vvsc)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = xgll__vvsc(np.floor(start + i * rqr__pjm))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            rqr__pjm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, xgll__vvsc)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = xgll__vvsc(start + i * rqr__pjm)
            return out_arr
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        dqb__klj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dqb__klj += A[i] == val
        return dqb__klj > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    qzu__yerme = {'axis': axis, 'out': out, 'keepdims': keepdims}
    qoim__hzmcx = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', qzu__yerme, qoim__hzmcx, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        dqb__klj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dqb__klj += int(bool(A[i]))
        return dqb__klj > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    qzu__yerme = {'axis': axis, 'out': out, 'keepdims': keepdims}
    qoim__hzmcx = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', qzu__yerme, qoim__hzmcx, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        dqb__klj = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dqb__klj += int(bool(A[i]))
        return dqb__klj == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    qzu__yerme = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    qoim__hzmcx = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', qzu__yerme, qoim__hzmcx, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        boq__oupp = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, boq__oupp)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], boq__oupp)
            return out_arr
        return impl_arr
    boq__oupp = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, boq__oupp)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    kdc__jfi = x < 0
    if kdc__jfi:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if kdc__jfi:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    yxhh__civz = isinstance(tup, (types.BaseTuple, types.List))
    gboor__wpsb = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for akpug__prn in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                akpug__prn, 'numpy.hstack()')
            yxhh__civz = yxhh__civz and bodo.utils.utils.is_array_typ(
                akpug__prn, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        yxhh__civz = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif gboor__wpsb:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        dhn__zuh = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for akpug__prn in dhn__zuh.types:
            gboor__wpsb = gboor__wpsb and bodo.utils.utils.is_array_typ(
                akpug__prn, False)
    if not (yxhh__civz or gboor__wpsb):
        return
    if gboor__wpsb:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    qzu__yerme = {'check_valid': check_valid, 'tol': tol}
    qoim__hzmcx = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', qzu__yerme,
        qoim__hzmcx, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        eghpg__tgje = mean.shape[0]
        sgfy__mrg = size, eghpg__tgje
        rrzy__dbuf = np.random.standard_normal(sgfy__mrg)
        cov = cov.astype(np.float64)
        byma__fwpc, s, dup__nei = np.linalg.svd(cov)
        res = np.dot(rrzy__dbuf, np.sqrt(s).reshape(eghpg__tgje, 1) * dup__nei)
        tyshi__wgvue = res + mean
        return tyshi__wgvue
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            yevpp__dccud = bodo.hiframes.series_kernels._get_type_max_value(arr
                )
            xuv__mkf = typing.builtins.IndexValue(-1, yevpp__dccud)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                pkm__ltn = typing.builtins.IndexValue(i, arr[i])
                xuv__mkf = min(xuv__mkf, pkm__ltn)
            return xuv__mkf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        zljqq__csk = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            qcue__lpvl = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            yevpp__dccud = zljqq__csk(len(arr.dtype.categories) + 1)
            xuv__mkf = typing.builtins.IndexValue(-1, yevpp__dccud)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                pkm__ltn = typing.builtins.IndexValue(i, qcue__lpvl[i])
                xuv__mkf = min(xuv__mkf, pkm__ltn)
            return xuv__mkf.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            yevpp__dccud = bodo.hiframes.series_kernels._get_type_min_value(arr
                )
            xuv__mkf = typing.builtins.IndexValue(-1, yevpp__dccud)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                pkm__ltn = typing.builtins.IndexValue(i, arr[i])
                xuv__mkf = max(xuv__mkf, pkm__ltn)
            return xuv__mkf.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        zljqq__csk = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            qcue__lpvl = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            yevpp__dccud = zljqq__csk(-1)
            xuv__mkf = typing.builtins.IndexValue(-1, yevpp__dccud)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                pkm__ltn = typing.builtins.IndexValue(i, qcue__lpvl[i])
                xuv__mkf = max(xuv__mkf, pkm__ltn)
            return xuv__mkf.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
