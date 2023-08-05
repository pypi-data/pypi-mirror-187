"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        wha__vjij = arr.copy(dtype=types.float64)
        return signature(wha__vjij, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    pgj__btpyd = get_overload_const_str(fname)
    if pgj__btpyd not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (pgj__btpyd))
    if pgj__btpyd in ('median', 'min', 'max'):
        eebya__mrg = 'def kernel_func(A):\n'
        eebya__mrg += '  if np.isnan(A).sum() != 0: return np.nan\n'
        eebya__mrg += '  return np.{}(A)\n'.format(pgj__btpyd)
        dro__tnv = {}
        exec(eebya__mrg, {'np': np}, dro__tnv)
        kernel_func = register_jitable(dro__tnv['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        pgj__btpyd]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    pgj__btpyd = get_overload_const_str(fname)
    if pgj__btpyd not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(pgj__btpyd))
    if pgj__btpyd in ('median', 'min', 'max'):
        eebya__mrg = 'def kernel_func(A):\n'
        eebya__mrg += '  arr  = dropna(A)\n'
        eebya__mrg += '  if len(arr) == 0: return np.nan\n'
        eebya__mrg += '  return np.{}(arr)\n'.format(pgj__btpyd)
        dro__tnv = {}
        exec(eebya__mrg, {'np': np, 'dropna': _dropna}, dro__tnv)
        kernel_func = register_jitable(dro__tnv['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        pgj__btpyd]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        kpolz__uvjdi = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            ozsen__tiome) = kpolz__uvjdi
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(ozsen__tiome, True)
            for hrpy__bhu in range(0, halo_size):
                data = add_obs(r_recv_buff[hrpy__bhu], *data)
                pse__chv = in_arr[N + hrpy__bhu - win]
                data = remove_obs(pse__chv, *data)
                output[N + hrpy__bhu - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for hrpy__bhu in range(0, halo_size):
                data = add_obs(l_recv_buff[hrpy__bhu], *data)
            for hrpy__bhu in range(0, win - 1):
                data = add_obs(in_arr[hrpy__bhu], *data)
                if hrpy__bhu > offset:
                    pse__chv = l_recv_buff[hrpy__bhu - offset - 1]
                    data = remove_obs(pse__chv, *data)
                if hrpy__bhu >= offset:
                    output[hrpy__bhu - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    yxqj__ximlb = max(minp, 1) - 1
    yxqj__ximlb = min(yxqj__ximlb, N)
    for hrpy__bhu in range(0, yxqj__ximlb):
        data = add_obs(in_arr[hrpy__bhu], *data)
        if hrpy__bhu >= offset:
            output[hrpy__bhu - offset] = calc_out(minp, *data)
    for hrpy__bhu in range(yxqj__ximlb, N):
        val = in_arr[hrpy__bhu]
        data = add_obs(val, *data)
        if hrpy__bhu > win - 1:
            pse__chv = in_arr[hrpy__bhu - win]
            data = remove_obs(pse__chv, *data)
        output[hrpy__bhu - offset] = calc_out(minp, *data)
    svz__udc = data
    for hrpy__bhu in range(N, N + offset):
        if hrpy__bhu > win - 1:
            pse__chv = in_arr[hrpy__bhu - win]
            data = remove_obs(pse__chv, *data)
        output[hrpy__bhu - offset] = calc_out(minp, *data)
    return output, svz__udc


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        kpolz__uvjdi = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            ozsen__tiome) = kpolz__uvjdi
        if raw == False:
            wibkq__dgjv = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, chlb__ogvpt, qytil__nflx,
                tifje__jfh, raej__aays) = wibkq__dgjv
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(qytil__nflx, chlb__ogvpt, rank, n_pes, True,
                center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(ozsen__tiome, True)
            if raw == False:
                bodo.libs.distributed_api.wait(raej__aays, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(tifje__jfh, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            svz__udc = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            rec__pslt = 0
            for hrpy__bhu in range(max(N - offset, 0), N):
                data = svz__udc[rec__pslt:rec__pslt + win]
                if win - np.isnan(data).sum() < minp:
                    output[hrpy__bhu] = np.nan
                else:
                    output[hrpy__bhu] = kernel_func(data)
                rec__pslt += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        svz__udc = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        sdg__qgo = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        rec__pslt = 0
        for hrpy__bhu in range(max(N - offset, 0), N):
            data = svz__udc[rec__pslt:rec__pslt + win]
            if win - np.isnan(data).sum() < minp:
                output[hrpy__bhu] = np.nan
            else:
                output[hrpy__bhu] = kernel_func(pd.Series(data, sdg__qgo[
                    rec__pslt:rec__pslt + win]))
            rec__pslt += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            svz__udc = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for hrpy__bhu in range(0, win - offset - 1):
                data = svz__udc[hrpy__bhu:hrpy__bhu + win]
                if win - np.isnan(data).sum() < minp:
                    output[hrpy__bhu] = np.nan
                else:
                    output[hrpy__bhu] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        svz__udc = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        sdg__qgo = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for hrpy__bhu in range(0, win - offset - 1):
            data = svz__udc[hrpy__bhu:hrpy__bhu + win]
            if win - np.isnan(data).sum() < minp:
                output[hrpy__bhu] = np.nan
            else:
                output[hrpy__bhu] = kernel_func(pd.Series(data, sdg__qgo[
                    hrpy__bhu:hrpy__bhu + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for hrpy__bhu in range(0, N):
            start = max(hrpy__bhu - win + 1 + offset, 0)
            end = min(hrpy__bhu + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[hrpy__bhu] = np.nan
            else:
                output[hrpy__bhu] = apply_func(kernel_func, data, index_arr,
                    start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        kpolz__uvjdi = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, xpfg__booyx, l_recv_req,
            tiwl__vlng) = kpolz__uvjdi
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(xpfg__booyx, xpfg__booyx, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tiwl__vlng, True)
            num_zero_starts = 0
            for hrpy__bhu in range(0, N):
                if start[hrpy__bhu] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for pcopv__xkyhd in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[pcopv__xkyhd], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for hrpy__bhu in range(1, num_zero_starts):
                s = recv_starts[hrpy__bhu]
                bbvq__mob = end[hrpy__bhu]
                for pcopv__xkyhd in range(recv_starts[hrpy__bhu - 1], s):
                    data = remove_obs(l_recv_buff[pcopv__xkyhd], *data)
                for pcopv__xkyhd in range(end[hrpy__bhu - 1], bbvq__mob):
                    data = add_obs(in_arr[pcopv__xkyhd], *data)
                output[hrpy__bhu] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    tdej__azpl = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    qaqy__esih = tdej__azpl[0] - win
    if left_closed:
        qaqy__esih -= 1
    recv_starts[0] = halo_size
    for pcopv__xkyhd in range(0, halo_size):
        if l_recv_t_buff[pcopv__xkyhd] > qaqy__esih:
            recv_starts[0] = pcopv__xkyhd
            break
    for hrpy__bhu in range(1, num_zero_starts):
        qaqy__esih = tdej__azpl[hrpy__bhu] - win
        if left_closed:
            qaqy__esih -= 1
        recv_starts[hrpy__bhu] = halo_size
        for pcopv__xkyhd in range(recv_starts[hrpy__bhu - 1], halo_size):
            if l_recv_t_buff[pcopv__xkyhd] > qaqy__esih:
                recv_starts[hrpy__bhu] = pcopv__xkyhd
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for pcopv__xkyhd in range(start[0], end[0]):
        data = add_obs(in_arr[pcopv__xkyhd], *data)
    output[0] = calc_out(minp, *data)
    for hrpy__bhu in range(1, N):
        s = start[hrpy__bhu]
        bbvq__mob = end[hrpy__bhu]
        for pcopv__xkyhd in range(start[hrpy__bhu - 1], s):
            data = remove_obs(in_arr[pcopv__xkyhd], *data)
        for pcopv__xkyhd in range(end[hrpy__bhu - 1], bbvq__mob):
            data = add_obs(in_arr[pcopv__xkyhd], *data)
        output[hrpy__bhu] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        kpolz__uvjdi = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, xpfg__booyx, l_recv_req,
            tiwl__vlng) = kpolz__uvjdi
        if raw == False:
            wibkq__dgjv = _border_icomm_var(index_arr, on_arr, rank, n_pes, win
                )
            (l_recv_buff_idx, skvn__wuf, qytil__nflx, tewk__rfnc,
                tifje__jfh, jlo__ztl) = wibkq__dgjv
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(xpfg__booyx, xpfg__booyx, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(qytil__nflx, qytil__nflx, rank, n_pes, True, 
                False)
            _border_send_wait(tewk__rfnc, tewk__rfnc, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tiwl__vlng, True)
            if raw == False:
                bodo.libs.distributed_api.wait(tifje__jfh, True)
                bodo.libs.distributed_api.wait(jlo__ztl, True)
            num_zero_starts = 0
            for hrpy__bhu in range(0, N):
                if start[hrpy__bhu] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for hrpy__bhu in range(0, num_zero_starts):
                nnkw__rqs = recv_starts[hrpy__bhu]
                tjye__rdct = np.concatenate((l_recv_buff[nnkw__rqs:],
                    in_arr[:hrpy__bhu + 1]))
                if len(tjye__rdct) - np.isnan(tjye__rdct).sum() >= minp:
                    output[hrpy__bhu] = kernel_func(tjye__rdct)
                else:
                    output[hrpy__bhu] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for hrpy__bhu in range(0, num_zero_starts):
            nnkw__rqs = recv_starts[hrpy__bhu]
            tjye__rdct = np.concatenate((l_recv_buff[nnkw__rqs:], in_arr[:
                hrpy__bhu + 1]))
            podo__weii = np.concatenate((l_recv_buff_idx[nnkw__rqs:],
                index_arr[:hrpy__bhu + 1]))
            if len(tjye__rdct) - np.isnan(tjye__rdct).sum() >= minp:
                output[hrpy__bhu] = kernel_func(pd.Series(tjye__rdct,
                    podo__weii))
            else:
                output[hrpy__bhu] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for hrpy__bhu in range(0, N):
        s = start[hrpy__bhu]
        bbvq__mob = end[hrpy__bhu]
        data = in_arr[s:bbvq__mob]
        if bbvq__mob - s - np.isnan(data).sum() >= minp:
            output[hrpy__bhu] = kernel_func(data)
        else:
            output[hrpy__bhu] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for hrpy__bhu in range(0, N):
        s = start[hrpy__bhu]
        bbvq__mob = end[hrpy__bhu]
        data = in_arr[s:bbvq__mob]
        if bbvq__mob - s - np.isnan(data).sum() >= minp:
            output[hrpy__bhu] = kernel_func(pd.Series(data, index_arr[s:
                bbvq__mob]))
        else:
            output[hrpy__bhu] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    tdej__azpl = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for hrpy__bhu in range(1, N):
        oiro__iww = tdej__azpl[hrpy__bhu]
        qaqy__esih = tdej__azpl[hrpy__bhu] - win
        if left_closed:
            qaqy__esih -= 1
        start[hrpy__bhu] = hrpy__bhu
        for pcopv__xkyhd in range(start[hrpy__bhu - 1], hrpy__bhu):
            if tdej__azpl[pcopv__xkyhd] > qaqy__esih:
                start[hrpy__bhu] = pcopv__xkyhd
                break
        if tdej__azpl[end[hrpy__bhu - 1]] <= oiro__iww:
            end[hrpy__bhu] = hrpy__bhu + 1
        else:
            end[hrpy__bhu] = end[hrpy__bhu - 1]
        if not right_closed:
            end[hrpy__bhu] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        aboto__sdxvs = sum_x / nobs
        if neg_ct == 0 and aboto__sdxvs < 0.0:
            aboto__sdxvs = 0
        elif neg_ct == nobs and aboto__sdxvs > 0.0:
            aboto__sdxvs = 0
    else:
        aboto__sdxvs = np.nan
    return aboto__sdxvs


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        bmpyz__avuop = val - mean_x
        mean_x += bmpyz__avuop / nobs
        ssqdm_x += (nobs - 1) * bmpyz__avuop ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            bmpyz__avuop = val - mean_x
            mean_x -= bmpyz__avuop / nobs
            ssqdm_x -= (nobs + 1) * bmpyz__avuop ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    bbv__dnu = 1.0
    aboto__sdxvs = np.nan
    if nobs >= minp and nobs > bbv__dnu:
        if nobs == 1:
            aboto__sdxvs = 0.0
        else:
            aboto__sdxvs = ssqdm_x / (nobs - bbv__dnu)
            if aboto__sdxvs < 0.0:
                aboto__sdxvs = 0.0
    return aboto__sdxvs


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    mpetr__gwd = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(mpetr__gwd)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift(in_arr, shift, parallel, default_fill_value=None):
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel, default_fill_value=None):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel, default_fill_value=None):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,), fill_value=default_fill_value)
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes,
                default_fill_value)
        kpolz__uvjdi = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            ozsen__tiome) = kpolz__uvjdi
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str, default_fill_value)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(ozsen__tiome, True)
                for hrpy__bhu in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, hrpy__bhu):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            hrpy__bhu)
                        continue
                    output[N - halo_size + hrpy__bhu] = r_recv_buff[hrpy__bhu]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False,
    default_fill_value=None):
    N = len(in_arr)
    ecxqw__tnq = 1 if shift > 0 else -1
    shift = ecxqw__tnq * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
        else:
            for hrpy__bhu in range(shift):
                output[hrpy__bhu
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    start = max(shift, 0)
    end = min(N, N + shift)
    for hrpy__bhu in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, hrpy__bhu - shift):
            bodo.libs.array_kernels.setna(output, hrpy__bhu)
            continue
        output[hrpy__bhu] = in_arr[hrpy__bhu - shift]
    if shift < 0:
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
        else:
            for hrpy__bhu in range(end, N):
                output[hrpy__bhu
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for hrpy__bhu in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, hrpy__bhu):
                bodo.libs.array_kernels.setna(output, hrpy__bhu)
                continue
            output[hrpy__bhu] = l_recv_buff[hrpy__bhu]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.FloatingArrayType, bodo.DecimalArrayType, bodo.DatetimeArrayType)
        ) or arr_type in (bodo.boolean_array, bodo.datetime_date_array_type,
        bodo.string_array_type, bodo.binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        kpolz__uvjdi = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            ozsen__tiome) = kpolz__uvjdi
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for hrpy__bhu in range(0, halo_size):
                    ign__zgo = l_recv_buff[hrpy__bhu]
                    output[hrpy__bhu] = (in_arr[hrpy__bhu] - ign__zgo
                        ) / ign__zgo
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(ozsen__tiome, True)
                for hrpy__bhu in range(0, halo_size):
                    ign__zgo = r_recv_buff[hrpy__bhu]
                    output[N - halo_size + hrpy__bhu] = (in_arr[N -
                        halo_size + hrpy__bhu] - ign__zgo) / ign__zgo
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    ncbbm__wgce = np.nan
    if arr.dtype == types.float32:
        ncbbm__wgce = np.float32('nan')

    def impl(arr):
        for hrpy__bhu in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, hrpy__bhu):
                return arr[hrpy__bhu]
        return ncbbm__wgce
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    ncbbm__wgce = np.nan
    if arr.dtype == types.float32:
        ncbbm__wgce = np.float32('nan')

    def impl(arr):
        jkr__umkv = len(arr)
        for hrpy__bhu in range(len(arr)):
            rec__pslt = jkr__umkv - hrpy__bhu - 1
            if not bodo.libs.array_kernels.isna(arr, rec__pslt):
                return arr[rec__pslt]
        return ncbbm__wgce
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    ecxqw__tnq = 1 if shift > 0 else -1
    shift = ecxqw__tnq * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        eyvxc__ucfn = get_first_non_na(in_arr[:shift])
        rfwh__zjz = get_last_non_na(in_arr[:shift])
    else:
        eyvxc__ucfn = get_last_non_na(in_arr[:-shift])
        rfwh__zjz = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for hrpy__bhu in range(start, end):
        ign__zgo = in_arr[hrpy__bhu - shift]
        if np.isnan(ign__zgo):
            ign__zgo = eyvxc__ucfn
        else:
            eyvxc__ucfn = ign__zgo
        val = in_arr[hrpy__bhu]
        if np.isnan(val):
            val = rfwh__zjz
        else:
            rfwh__zjz = val
        output[hrpy__bhu] = val / ign__zgo - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    sjlm__twg = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), sjlm__twg, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), sjlm__twg, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), sjlm__twg, True)
    if send_left and rank != n_pes - 1:
        ozsen__tiome = bodo.libs.distributed_api.irecv(r_recv_buff,
            halo_size, np.int32(rank + 1), sjlm__twg, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        ozsen__tiome)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    sjlm__twg = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for pcopv__xkyhd in range(-2, -N, -1):
        ohv__ixwa = on_arr[pcopv__xkyhd]
        if end - ohv__ixwa >= win_size:
            halo_size = -pcopv__xkyhd
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), sjlm__twg
            )
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), sjlm__twg, True)
        xpfg__booyx = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), sjlm__twg, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), sjlm__twg)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), sjlm__twg, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        tiwl__vlng = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), sjlm__twg, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, xpfg__booyx, l_recv_req,
        tiwl__vlng)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    wyx__bsd = bodo.libs.distributed_api.dist_reduce(int(N <= 2 * halo_size +
        1), np.int32(Reduce_Type.Sum.value))
    return wyx__bsd != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        oye__xon, nrds__kpbp = roll_fixed_linear_generic_seq(bra__zlwc, win,
            minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        oye__xon = np.empty(ngtar__chj, np.float64)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    xhu__vjz = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        oye__xon = roll_fixed_apply_seq(bra__zlwc, xhu__vjz, win, minp,
            center, kernel_func, raw)
    else:
        oye__xon = np.empty(ngtar__chj, np.float64)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes, default_fill_value):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        oye__xon = alloc_shift(len(bra__zlwc), bra__zlwc, (-1,), fill_value
            =default_fill_value)
        shift_seq(bra__zlwc, shift, oye__xon, default_fill_value=
            default_fill_value)
        yffcp__fcl = bcast_n_chars_if_str_binary_arr(oye__xon)
    else:
        yffcp__fcl = bcast_n_chars_if_str_binary_arr(in_arr)
        oye__xon = alloc_shift(ngtar__chj, in_arr, (yffcp__fcl,),
            fill_value=default_fill_value)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        oye__xon = pct_change_seq(bra__zlwc, shift)
    else:
        oye__xon = alloc_pct_change(ngtar__chj, in_arr)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        mqlv__rddmf = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        ljsu__zce = end - start
        mqlv__rddmf = int(ljsu__zce <= win_size)
    wyx__bsd = bodo.libs.distributed_api.dist_reduce(mqlv__rddmf, np.int32(
        Reduce_Type.Sum.value))
    return wyx__bsd != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    hiwci__gjf = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(hiwci__gjf, ngtar__chj, win, False, True)
        oye__xon = roll_var_linear_generic_seq(bra__zlwc, hiwci__gjf, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        oye__xon = np.empty(ngtar__chj, np.float64)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    ngtar__chj = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bra__zlwc = bodo.libs.distributed_api.gatherv(in_arr)
    hiwci__gjf = bodo.libs.distributed_api.gatherv(on_arr)
    xhu__vjz = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(hiwci__gjf, ngtar__chj, win, False, True)
        oye__xon = roll_variable_apply_seq(bra__zlwc, hiwci__gjf, xhu__vjz,
            win, minp, start, end, kernel_func, raw)
    else:
        oye__xon = np.empty(ngtar__chj, np.float64)
    bodo.libs.distributed_api.bcast(oye__xon)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return oye__xon[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    zorhr__iuza = len(arr)
    keidc__udmn = zorhr__iuza - np.isnan(arr).sum()
    A = np.empty(keidc__udmn, arr.dtype)
    bkcg__vfy = 0
    for hrpy__bhu in range(zorhr__iuza):
        val = arr[hrpy__bhu]
        if not np.isnan(val):
            A[bkcg__vfy] = val
            bkcg__vfy += 1
    return A


def alloc_shift(n, A, s=None, fill_value=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None, fill_value=None):
    if not isinstance(A, types.Array):
        return (lambda n, A, s=None, fill_value=None: bodo.utils.utils.
            alloc_type(n, A, s))
    if isinstance(A.dtype, types.Integer) and not isinstance(fill_value,
        types.Integer):
        return lambda n, A, s=None, fill_value=None: np.empty(n, np.float64)
    return lambda n, A, s=None, fill_value=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: bodo.utils.utils.alloc_type(n, A, (-1,))


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
