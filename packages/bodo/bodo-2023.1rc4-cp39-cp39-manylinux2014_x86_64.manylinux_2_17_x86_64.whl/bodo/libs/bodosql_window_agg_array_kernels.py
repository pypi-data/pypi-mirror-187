"""
Implements window/aggregation array kernels that are specific to BodoSQL.
Specifically, window/aggregation array kernels that do not concern window
frames.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, raise_bodo_error


def rank_sql(arr_tup, method='average', pct=False):
    return


@overload(rank_sql, no_unliteral=True)
def overload_rank_sql(arr_tup, method='average', pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    bfib__oih = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        bfib__oih += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        bfib__oih += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for zimnk__xffaa in range(1, len(arr_tup)):
            bfib__oih += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{zimnk__xffaa}]) 
"""
        bfib__oih += '  dense = obs.cumsum()\n'
        if method == 'dense':
            bfib__oih += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            bfib__oih += '    dense,\n'
            bfib__oih += '    new_dtype=np.float64,\n'
            bfib__oih += '    copy=True,\n'
            bfib__oih += '    nan_to_str=False,\n'
            bfib__oih += '    from_series=True,\n'
            bfib__oih += '  )\n'
        else:
            bfib__oih += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            bfib__oih += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                bfib__oih += '  ret = count_float[dense]\n'
            elif method == 'min':
                bfib__oih += '  ret = count_float[dense - 1] + 1\n'
            else:
                bfib__oih += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            bfib__oih += '  div_val = np.max(ret)\n'
        else:
            bfib__oih += '  div_val = len(arr_tup[0])\n'
        bfib__oih += '  for i in range(len(ret)):\n'
        bfib__oih += '    ret[i] = ret[i] / div_val\n'
    bfib__oih += '  return ret\n'
    hrwjs__uybn = {}
    exec(bfib__oih, {'np': np, 'pd': pd, 'bodo': bodo}, hrwjs__uybn)
    return hrwjs__uybn['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        iod__uuxeq = bodo.hiframes.pd_series_ext.get_series_data(S)
        ldmm__lkfqk = len(iod__uuxeq)
        epouy__ykffr = bodo.utils.utils.alloc_type(ldmm__lkfqk, types.
            uint64, -1)
        nae__divl = -1
        for zimnk__xffaa in range(ldmm__lkfqk):
            epouy__ykffr[zimnk__xffaa] = 0
            if not bodo.libs.array_kernels.isna(iod__uuxeq, zimnk__xffaa):
                nae__divl = zimnk__xffaa
                break
        if nae__divl != -1:
            pkos__pwnst = iod__uuxeq[nae__divl]
            for zimnk__xffaa in range(nae__divl + 1, ldmm__lkfqk):
                if bodo.libs.array_kernels.isna(iod__uuxeq, zimnk__xffaa
                    ) or iod__uuxeq[zimnk__xffaa] == pkos__pwnst:
                    epouy__ykffr[zimnk__xffaa] = epouy__ykffr[zimnk__xffaa - 1]
                else:
                    pkos__pwnst = iod__uuxeq[zimnk__xffaa]
                    epouy__ykffr[zimnk__xffaa] = epouy__ykffr[zimnk__xffaa - 1
                        ] + 1
        return bodo.hiframes.pd_series_ext.init_series(epouy__ykffr, bodo.
            hiframes.pd_index_ext.init_range_index(0, ldmm__lkfqk, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    wpwc__omgs = 'res[i] = total'
    rua__gsilk = 'constant_value = S.sum()'
    nokg__xjlul = 'total = 0'
    krnm__yiyfi = 'total += elem'
    hrwga__mcdpz = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        ciar__wqz = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        ciar__wqz = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, setup_block=
        nokg__xjlul, enter_block=krnm__yiyfi, exit_block=hrwga__mcdpz)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    wpwc__omgs = 'res[i] = in_window'
    rua__gsilk = 'constant_value = S.count()'
    iyf__klv = 'res[i] = 0'
    ciar__wqz = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, empty_block=iyf__klv
        )


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    wpwc__omgs = 'res[i] = total / in_window'
    rua__gsilk = 'constant_value = S.mean()'
    ciar__wqz = types.Array(bodo.float64, 1, 'C')
    nokg__xjlul = 'total = 0'
    krnm__yiyfi = 'total += elem'
    hrwga__mcdpz = 'total -= elem'
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, setup_block=
        nokg__xjlul, enter_block=krnm__yiyfi, exit_block=hrwga__mcdpz)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    wpwc__omgs = 'res[i] = np.median(arr2)'
    rua__gsilk = 'constant_value = S.median()'
    ciar__wqz = types.Array(bodo.float64, 1, 'C')
    nokg__xjlul = 'arr2 = np.zeros(0, dtype=np.float64)'
    krnm__yiyfi = 'arr2 = np.append(arr2, elem)'
    hrwga__mcdpz = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, setup_block=
        nokg__xjlul, enter_block=krnm__yiyfi, exit_block=hrwga__mcdpz)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        ciar__wqz = S.data
    else:
        ciar__wqz = S
    wpwc__omgs = 'bestVal, bestCount = None, 0\n'
    wpwc__omgs += 'for key in counts:\n'
    wpwc__omgs += '   if counts[key] > bestCount:\n'
    wpwc__omgs += '      bestVal, bestCount = key, counts[key]\n'
    wpwc__omgs += 'res[i] = bestVal'
    rua__gsilk = 'counts = {arr[0]: 0}\n'
    rua__gsilk += 'for i in range(len(S)):\n'
    rua__gsilk += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    rua__gsilk += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    rua__gsilk += wpwc__omgs.replace('res[i]', 'constant_value')
    nokg__xjlul = 'counts = {arr[0]: 0}'
    krnm__yiyfi = 'counts[elem] = counts.get(elem, 0) + 1'
    hrwga__mcdpz = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, setup_block=
        nokg__xjlul, enter_block=krnm__yiyfi, exit_block=hrwga__mcdpz)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    wpwc__omgs = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    wpwc__omgs += '   bodo.libs.array_kernels.setna(res, i)\n'
    wpwc__omgs += 'else:\n'
    wpwc__omgs += '   res[i] = arr[i] / total'
    rua__gsilk = None
    ciar__wqz = types.Array(bodo.float64, 1, 'C')
    nokg__xjlul = 'total = 0'
    krnm__yiyfi = 'total += elem'
    hrwga__mcdpz = 'total -= elem'
    return gen_windowed(wpwc__omgs, rua__gsilk, ciar__wqz, setup_block=
        nokg__xjlul, enter_block=krnm__yiyfi, exit_block=hrwga__mcdpz)
