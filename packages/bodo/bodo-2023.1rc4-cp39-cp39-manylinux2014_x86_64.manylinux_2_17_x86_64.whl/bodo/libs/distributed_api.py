import atexit
import datetime
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload, register_jitable
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    giz__fcgkc = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, giz__fcgkc, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    giz__fcgkc = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, giz__fcgkc, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            giz__fcgkc = get_type_enum(arr)
            return _isend(arr.ctypes, size, giz__fcgkc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        giz__fcgkc = np.int32(numba_to_c_type(arr.dtype))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            lbuwh__thrc = size + 7 >> 3
            hvojn__ixd = _isend(arr._data.ctypes, size, giz__fcgkc, pe, tag,
                cond)
            izgrf__ema = _isend(arr._null_bitmap.ctypes, lbuwh__thrc,
                rkzh__krbvp, pe, tag, cond)
            return hvojn__ixd, izgrf__ema
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            sxzg__nykh = arr._data
            giz__fcgkc = get_type_enum(sxzg__nykh)
            return _isend(sxzg__nykh.ctypes, size, giz__fcgkc, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        jvdz__ony = np.int32(numba_to_c_type(offset_type))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            gguy__ifgwx = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(gguy__ifgwx, pe, tag - 1)
            lbuwh__thrc = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                jvdz__ony, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), gguy__ifgwx,
                rkzh__krbvp, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                lbuwh__thrc, rkzh__krbvp, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            giz__fcgkc = get_type_enum(arr)
            return _irecv(arr.ctypes, size, giz__fcgkc, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        giz__fcgkc = np.int32(numba_to_c_type(arr.dtype))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            lbuwh__thrc = size + 7 >> 3
            hvojn__ixd = _irecv(arr._data.ctypes, size, giz__fcgkc, pe, tag,
                cond)
            izgrf__ema = _irecv(arr._null_bitmap.ctypes, lbuwh__thrc,
                rkzh__krbvp, pe, tag, cond)
            return hvojn__ixd, izgrf__ema
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            sxzg__nykh = arr._data
            giz__fcgkc = get_type_enum(sxzg__nykh)
            return _irecv(sxzg__nykh.ctypes, size, giz__fcgkc, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        jvdz__ony = np.int32(numba_to_c_type(offset_type))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            ocn__ffwku = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            ocn__ffwku = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        chj__cijws = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {ocn__ffwku}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        lmps__saqs = dict()
        exec(chj__cijws, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            jvdz__ony, 'char_typ_enum': rkzh__krbvp}, lmps__saqs)
        impl = lmps__saqs['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    giz__fcgkc = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), giz__fcgkc)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        tdgyk__rso = n_pes if rank == root or allgather else 0
        xjva__ykevw = np.empty(tdgyk__rso, dtype)
        c_gather_scalar(send.ctypes, xjva__ykevw.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return xjva__ykevw
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        trrw__ewhc = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], trrw__ewhc)
        return builder.bitcast(trrw__ewhc, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        trrw__ewhc = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(trrw__ewhc)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    tkzja__uiif = types.unliteral(value)
    if isinstance(tkzja__uiif, IndexValueType):
        tkzja__uiif = tkzja__uiif.val_typ
        orjk__ncxgc = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            orjk__ncxgc.append(types.int64)
            orjk__ncxgc.append(bodo.datetime64ns)
            orjk__ncxgc.append(bodo.timedelta64ns)
            orjk__ncxgc.append(bodo.datetime_date_type)
            orjk__ncxgc.append(bodo.TimeType)
        if tkzja__uiif not in orjk__ncxgc:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(tkzja__uiif))
    typ_enum = np.int32(numba_to_c_type(tkzja__uiif))

    def impl(value, reduce_op):
        ruj__qybm = value_to_ptr(value)
        lowl__fxs = value_to_ptr(value)
        _dist_reduce(ruj__qybm, lowl__fxs, reduce_op, typ_enum)
        return load_val_ptr(lowl__fxs, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    tkzja__uiif = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(tkzja__uiif))
    uhm__zfnzj = tkzja__uiif(0)

    def impl(value, reduce_op):
        ruj__qybm = value_to_ptr(value)
        lowl__fxs = value_to_ptr(uhm__zfnzj)
        _dist_exscan(ruj__qybm, lowl__fxs, reduce_op, typ_enum)
        return load_val_ptr(lowl__fxs, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    otmw__ijtpl = 0
    ipr__gasm = 0
    for i in range(len(recv_counts)):
        zazd__bfyor = recv_counts[i]
        lbuwh__thrc = recv_counts_nulls[i]
        hgvw__zlrn = tmp_null_bytes[otmw__ijtpl:otmw__ijtpl + lbuwh__thrc]
        for mgqm__ecm in range(zazd__bfyor):
            set_bit_to(null_bitmap_ptr, ipr__gasm, get_bit(hgvw__zlrn,
                mgqm__ecm))
            ipr__gasm += 1
        otmw__ijtpl += lbuwh__thrc


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            qct__gmsh = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                qct__gmsh, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            lafb__vafy = data.size
            recv_counts = gather_scalar(np.int32(lafb__vafy), allgather,
                root=root)
            mmb__thvg = recv_counts.sum()
            ooh__natt = empty_like_type(mmb__thvg, data)
            eiaa__saxv = np.empty(1, np.int32)
            if rank == root or allgather:
                eiaa__saxv = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(lafb__vafy), ooh__natt.ctypes,
                recv_counts.ctypes, eiaa__saxv.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return ooh__natt.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            ooh__natt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(ooh__natt)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            ooh__natt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(ooh__natt)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            lafb__vafy = len(data)
            lbuwh__thrc = lafb__vafy + 7 >> 3
            recv_counts = gather_scalar(np.int32(lafb__vafy), allgather,
                root=root)
            mmb__thvg = recv_counts.sum()
            ooh__natt = empty_like_type(mmb__thvg, data)
            eiaa__saxv = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            qvt__ctclb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                eiaa__saxv = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                qvt__ctclb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(lafb__vafy),
                ooh__natt._days_data.ctypes, recv_counts.ctypes, eiaa__saxv
                .ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(lafb__vafy),
                ooh__natt._seconds_data.ctypes, recv_counts.ctypes,
                eiaa__saxv.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(lafb__vafy),
                ooh__natt._microseconds_data.ctypes, recv_counts.ctypes,
                eiaa__saxv.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(lbuwh__thrc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, qvt__ctclb
                .ctypes, rkzh__krbvp, allgather, np.int32(root))
            copy_gathered_null_bytes(ooh__natt._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ooh__natt
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            lafb__vafy = len(data)
            lbuwh__thrc = lafb__vafy + 7 >> 3
            recv_counts = gather_scalar(np.int32(lafb__vafy), allgather,
                root=root)
            mmb__thvg = recv_counts.sum()
            ooh__natt = empty_like_type(mmb__thvg, data)
            eiaa__saxv = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            qvt__ctclb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                eiaa__saxv = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                qvt__ctclb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(lafb__vafy), ooh__natt.
                _data.ctypes, recv_counts.ctypes, eiaa__saxv.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(lbuwh__thrc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, qvt__ctclb
                .ctypes, rkzh__krbvp, allgather, np.int32(root))
            copy_gathered_null_bytes(ooh__natt._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return ooh__natt
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        bmw__wgmlw = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            mcr__tlw = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                mcr__tlw, bmw__wgmlw)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            myzvr__oeqr = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            acy__nnmle = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(myzvr__oeqr,
                acy__nnmle)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            drofd__qrhoh = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            wnge__vexhd = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wnge__vexhd, drofd__qrhoh)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        gll__orjso = np.iinfo(np.int64).max
        kdo__sjiwm = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ezj__zzllq = data._start
            vwds__pxhbp = data._stop
            if len(data) == 0:
                ezj__zzllq = gll__orjso
                vwds__pxhbp = kdo__sjiwm
            ezj__zzllq = bodo.libs.distributed_api.dist_reduce(ezj__zzllq,
                np.int32(Reduce_Type.Min.value))
            vwds__pxhbp = bodo.libs.distributed_api.dist_reduce(vwds__pxhbp,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if ezj__zzllq == gll__orjso and vwds__pxhbp == kdo__sjiwm:
                ezj__zzllq = 0
                vwds__pxhbp = 0
            pfqy__pvdi = max(0, -(-(vwds__pxhbp - ezj__zzllq) // data._step))
            if pfqy__pvdi < total_len:
                vwds__pxhbp = ezj__zzllq + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                ezj__zzllq = 0
                vwds__pxhbp = 0
            return bodo.hiframes.pd_index_ext.init_range_index(ezj__zzllq,
                vwds__pxhbp, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            cti__rrpz = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, cti__rrpz)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ooh__natt = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(ooh__natt,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        gzpw__ilkpp = {'bodo': bodo, 'get_table_block': bodo.hiframes.table
            .get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        chj__cijws = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        chj__cijws += '  T = data\n'
        chj__cijws += '  T2 = init_table(T, True)\n'
        jkzy__hey = bodo.hiframes.table.get_init_table_output_type(data, True)
        uwfhv__almn = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if uwfhv__almn:
            chj__cijws += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                jkzy__hey, gzpw__ilkpp, True))
        for njd__bpte, ekfqu__rsog in data.type_to_blk.items():
            if uwfhv__almn and njd__bpte in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif njd__bpte == bodo.dict_str_arr_type:
                assert bodo.string_array_type in jkzy__hey.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                qyf__jsagf = jkzy__hey.type_to_blk[bodo.string_array_type]
            else:
                assert njd__bpte in jkzy__hey.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                qyf__jsagf = jkzy__hey.type_to_blk[njd__bpte]
            gzpw__ilkpp[f'arr_inds_{ekfqu__rsog}'] = np.array(data.
                block_to_arr_ind[ekfqu__rsog], dtype=np.int64)
            chj__cijws += (
                f'  arr_list_{ekfqu__rsog} = get_table_block(T, {ekfqu__rsog})\n'
                )
            chj__cijws += f"""  out_arr_list_{ekfqu__rsog} = alloc_list_like(arr_list_{ekfqu__rsog}, len(arr_list_{ekfqu__rsog}), True)
"""
            chj__cijws += f'  for i in range(len(arr_list_{ekfqu__rsog})):\n'
            chj__cijws += (
                f'    arr_ind_{ekfqu__rsog} = arr_inds_{ekfqu__rsog}[i]\n')
            chj__cijws += f"""    ensure_column_unboxed(T, arr_list_{ekfqu__rsog}, i, arr_ind_{ekfqu__rsog})
"""
            chj__cijws += f"""    out_arr_{ekfqu__rsog} = bodo.gatherv(arr_list_{ekfqu__rsog}[i], allgather, warn_if_rep, root)
"""
            chj__cijws += (
                f'    out_arr_list_{ekfqu__rsog}[i] = out_arr_{ekfqu__rsog}\n')
            chj__cijws += (
                f'  T2 = set_table_block(T2, out_arr_list_{ekfqu__rsog}, {qyf__jsagf})\n'
                )
        chj__cijws += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        chj__cijws += f'  T2 = set_table_len(T2, length)\n'
        chj__cijws += f'  return T2\n'
        lmps__saqs = {}
        exec(chj__cijws, gzpw__ilkpp, lmps__saqs)
        ghxfu__ass = lmps__saqs['impl_table']
        return ghxfu__ass
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kpkg__fzyk = len(data.columns)
        if kpkg__fzyk == 0:
            xxck__zimu = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                sbci__pjhof = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    sbci__pjhof, xxck__zimu)
            return impl
        fafsj__zwpdu = ', '.join(f'g_data_{i}' for i in range(kpkg__fzyk))
        chj__cijws = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            kyere__grltt = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            fafsj__zwpdu = 'T2'
            chj__cijws += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            chj__cijws += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(kpkg__fzyk):
                chj__cijws += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                chj__cijws += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        chj__cijws += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        chj__cijws += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        chj__cijws += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(fafsj__zwpdu))
        lmps__saqs = {}
        gzpw__ilkpp = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(chj__cijws, gzpw__ilkpp, lmps__saqs)
        ogrq__col = lmps__saqs['impl_df']
        return ogrq__col
    if isinstance(data, ArrayItemArrayType):
        xenhe__rmm = np.int32(numba_to_c_type(types.int32))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            wavxd__ebs = bodo.libs.array_item_arr_ext.get_offsets(data)
            sxzg__nykh = bodo.libs.array_item_arr_ext.get_data(data)
            sxzg__nykh = sxzg__nykh[:wavxd__ebs[-1]]
            laa__lqzt = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            lafb__vafy = len(data)
            kxr__ybno = np.empty(lafb__vafy, np.uint32)
            lbuwh__thrc = lafb__vafy + 7 >> 3
            for i in range(lafb__vafy):
                kxr__ybno[i] = wavxd__ebs[i + 1] - wavxd__ebs[i]
            recv_counts = gather_scalar(np.int32(lafb__vafy), allgather,
                root=root)
            mmb__thvg = recv_counts.sum()
            eiaa__saxv = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            qvt__ctclb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                eiaa__saxv = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for qxje__gvov in range(len(recv_counts)):
                    recv_counts_nulls[qxje__gvov] = recv_counts[qxje__gvov
                        ] + 7 >> 3
                qvt__ctclb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            jjt__wngkn = np.empty(mmb__thvg + 1, np.uint32)
            xmfj__uwdjm = bodo.gatherv(sxzg__nykh, allgather, warn_if_rep, root
                )
            mmj__cmqg = np.empty(mmb__thvg + 7 >> 3, np.uint8)
            c_gatherv(kxr__ybno.ctypes, np.int32(lafb__vafy), jjt__wngkn.
                ctypes, recv_counts.ctypes, eiaa__saxv.ctypes, xenhe__rmm,
                allgather, np.int32(root))
            c_gatherv(laa__lqzt.ctypes, np.int32(lbuwh__thrc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, qvt__ctclb
                .ctypes, rkzh__krbvp, allgather, np.int32(root))
            dummy_use(data)
            zpve__dpg = np.empty(mmb__thvg + 1, np.uint64)
            convert_len_arr_to_offset(jjt__wngkn.ctypes, zpve__dpg.ctypes,
                mmb__thvg)
            copy_gathered_null_bytes(mmj__cmqg.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                mmb__thvg, xmfj__uwdjm, zpve__dpg, mmj__cmqg)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        wunn__weh = data.names
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            pvmny__dnnuh = bodo.libs.struct_arr_ext.get_data(data)
            vuz__gtcq = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            lpoev__isyg = bodo.gatherv(pvmny__dnnuh, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            lafb__vafy = len(data)
            lbuwh__thrc = lafb__vafy + 7 >> 3
            recv_counts = gather_scalar(np.int32(lafb__vafy), allgather,
                root=root)
            mmb__thvg = recv_counts.sum()
            tas__aocsj = np.empty(mmb__thvg + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            qvt__ctclb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                qvt__ctclb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(vuz__gtcq.ctypes, np.int32(lbuwh__thrc),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, qvt__ctclb
                .ctypes, rkzh__krbvp, allgather, np.int32(root))
            copy_gathered_null_bytes(tas__aocsj.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(lpoev__isyg,
                tas__aocsj, wunn__weh)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ooh__natt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(ooh__natt)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ooh__natt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(ooh__natt)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            ooh__natt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(ooh__natt)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ooh__natt = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            vha__ejdod = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            rxkyi__lve = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            ggx__mcsvg = gather_scalar(data.shape[0], allgather, root=root)
            wwp__bfkql = ggx__mcsvg.sum()
            kpkg__fzyk = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            osz__rsjy = np.empty(wwp__bfkql + 1, np.int64)
            vha__ejdod = vha__ejdod.astype(np.int64)
            osz__rsjy[0] = 0
            rtf__dia = 1
            txhf__qobd = 0
            for ifp__tvy in ggx__mcsvg:
                for syjd__pzh in range(ifp__tvy):
                    clwy__zkqjl = rxkyi__lve[txhf__qobd + 1] - rxkyi__lve[
                        txhf__qobd]
                    osz__rsjy[rtf__dia] = osz__rsjy[rtf__dia - 1] + clwy__zkqjl
                    rtf__dia += 1
                    txhf__qobd += 1
                txhf__qobd += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(ooh__natt,
                vha__ejdod, osz__rsjy, (wwp__bfkql, kpkg__fzyk))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        chj__cijws = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        chj__cijws += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo}, lmps__saqs)
        dxxw__abd = lmps__saqs['impl_tuple']
        return dxxw__abd
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as eqx__wfgez:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        chj__cijws = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        cybmr__nwydh = ', '.join([f"'{drofd__qrhoh}'" for drofd__qrhoh in
            data.names])
        hecs__uob = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        chj__cijws += f"""  return bodosql.context_ext.init_sql_context(({cybmr__nwydh}, ), ({hecs__uob}, ), data.catalog)
"""
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo, 'bodosql': bodosql}, lmps__saqs)
        eamsu__gwu = lmps__saqs['impl_bodosql_context']
        return eamsu__gwu
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as eqx__wfgez:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        chj__cijws = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        chj__cijws += f'  return data\n'
        lmps__saqs = {}
        exec(chj__cijws, {}, lmps__saqs)
        akh__fep = lmps__saqs['impl_table_path']
        return akh__fep
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    chj__cijws = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    chj__cijws += '    if random:\n'
    chj__cijws += '        if random_seed is None:\n'
    chj__cijws += '            random = 1\n'
    chj__cijws += '        else:\n'
    chj__cijws += '            random = 2\n'
    chj__cijws += '    if random_seed is None:\n'
    chj__cijws += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        jlag__hidc = data
        kpkg__fzyk = len(jlag__hidc.columns)
        for i in range(kpkg__fzyk):
            chj__cijws += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        chj__cijws += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        fafsj__zwpdu = ', '.join(f'data_{i}' for i in range(kpkg__fzyk))
        chj__cijws += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(lam__ghu) for
            lam__ghu in range(kpkg__fzyk))))
        chj__cijws += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        chj__cijws += '    if dests is None:\n'
        chj__cijws += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        chj__cijws += '    else:\n'
        chj__cijws += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for nrxx__udu in range(kpkg__fzyk):
            chj__cijws += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(nrxx__udu))
        chj__cijws += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(kpkg__fzyk))
        chj__cijws += '    delete_table(out_table)\n'
        chj__cijws += '    if parallel:\n'
        chj__cijws += '        delete_table(table_total)\n'
        fafsj__zwpdu = ', '.join('out_arr_{}'.format(i) for i in range(
            kpkg__fzyk))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        chj__cijws += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(fafsj__zwpdu, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        chj__cijws += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        chj__cijws += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        chj__cijws += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        chj__cijws += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        chj__cijws += '    if dests is None:\n'
        chj__cijws += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        chj__cijws += '    else:\n'
        chj__cijws += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        chj__cijws += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        chj__cijws += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        chj__cijws += '    delete_table(out_table)\n'
        chj__cijws += '    if parallel:\n'
        chj__cijws += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        chj__cijws += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        chj__cijws += '    if not parallel:\n'
        chj__cijws += '        return data\n'
        chj__cijws += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        chj__cijws += '    if dests is None:\n'
        chj__cijws += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        chj__cijws += '    elif bodo.get_rank() not in dests:\n'
        chj__cijws += '        dim0_local_size = 0\n'
        chj__cijws += '    else:\n'
        chj__cijws += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        chj__cijws += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        chj__cijws += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        chj__cijws += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        chj__cijws += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        chj__cijws += '    if dests is None:\n'
        chj__cijws += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        chj__cijws += '    else:\n'
        chj__cijws += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        chj__cijws += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        chj__cijws += '    delete_table(out_table)\n'
        chj__cijws += '    if parallel:\n'
        chj__cijws += '        delete_table(table_total)\n'
        chj__cijws += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    lmps__saqs = {}
    gzpw__ilkpp = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array
        .array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        gzpw__ilkpp.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(jlag__hidc.columns)})
    exec(chj__cijws, gzpw__ilkpp, lmps__saqs)
    impl = lmps__saqs['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    chj__cijws = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        chj__cijws += '    if seed is None:\n'
        chj__cijws += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        chj__cijws += '    np.random.seed(seed)\n'
        chj__cijws += '    if not parallel:\n'
        chj__cijws += '        data = data.copy()\n'
        chj__cijws += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            chj__cijws += '        data = data[:n_samples]\n'
        chj__cijws += '        return data\n'
        chj__cijws += '    else:\n'
        chj__cijws += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        chj__cijws += '        permutation = np.arange(dim0_global_size)\n'
        chj__cijws += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            chj__cijws += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            chj__cijws += '        n_samples = dim0_global_size\n'
        chj__cijws += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        chj__cijws += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        chj__cijws += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        chj__cijws += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        chj__cijws += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        chj__cijws += '        return output\n'
    else:
        chj__cijws += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            chj__cijws += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            chj__cijws += '    output = output[:local_n_samples]\n'
        chj__cijws += '    return output\n'
    lmps__saqs = {}
    exec(chj__cijws, {'np': np, 'bodo': bodo}, lmps__saqs)
    impl = lmps__saqs['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    uolps__fbez = np.empty(sendcounts_nulls.sum(), np.uint8)
    otmw__ijtpl = 0
    ipr__gasm = 0
    for xlkrt__feru in range(len(sendcounts)):
        zazd__bfyor = sendcounts[xlkrt__feru]
        lbuwh__thrc = sendcounts_nulls[xlkrt__feru]
        hgvw__zlrn = uolps__fbez[otmw__ijtpl:otmw__ijtpl + lbuwh__thrc]
        for mgqm__ecm in range(zazd__bfyor):
            set_bit_to_arr(hgvw__zlrn, mgqm__ecm, get_bit_bitmap(
                null_bitmap_ptr, ipr__gasm))
            ipr__gasm += 1
        otmw__ijtpl += lbuwh__thrc
    return uolps__fbez


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    kag__eqdr = MPI.COMM_WORLD
    data = kag__eqdr.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    pfv__mekjp = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    fxl__xhlh = (0,) * pfv__mekjp

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        tse__yyz = np.ascontiguousarray(data)
        splp__jhsj = data.ctypes
        ptoz__yfcjl = fxl__xhlh
        if rank == MPI_ROOT:
            ptoz__yfcjl = tse__yyz.shape
        ptoz__yfcjl = bcast_tuple(ptoz__yfcjl)
        mfrxp__gmx = get_tuple_prod(ptoz__yfcjl[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            ptoz__yfcjl[0])
        send_counts *= mfrxp__gmx
        lafb__vafy = send_counts[rank]
        izs__kwa = np.empty(lafb__vafy, dtype)
        eiaa__saxv = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(splp__jhsj, send_counts.ctypes, eiaa__saxv.ctypes,
            izs__kwa.ctypes, np.int32(lafb__vafy), np.int32(typ_val))
        return izs__kwa.reshape((-1,) + ptoz__yfcjl[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        wic__pikdr = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], wic__pikdr)
    if isinstance(dtype, FloatingArrayType):
        wic__pikdr = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], wic__pikdr)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        drofd__qrhoh = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=drofd__qrhoh)
        ept__dpf = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(ept__dpf)
        return pd.Index(arr, name=drofd__qrhoh)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        drofd__qrhoh = _get_name_value_for_type(dtype.name_typ)
        wunn__weh = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        jydke__knllj = tuple(get_value_for_type(t) for t in dtype.array_types)
        jydke__knllj = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in jydke__knllj)
        val = pd.MultiIndex.from_arrays(jydke__knllj, names=wunn__weh)
        val.name = drofd__qrhoh
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        drofd__qrhoh = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=drofd__qrhoh)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        jydke__knllj = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({drofd__qrhoh: arr for drofd__qrhoh, arr in zip
            (dtype.columns, jydke__knllj)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        ept__dpf = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(ept__dpf[0], ept__dpf[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in (string_array_type, binary_array_type):
        xenhe__rmm = np.int32(numba_to_c_type(types.int32))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            ocn__ffwku = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            ocn__ffwku = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        chj__cijws = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {ocn__ffwku}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        lmps__saqs = dict()
        exec(chj__cijws, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            xenhe__rmm, 'char_typ_enum': rkzh__krbvp,
            'decode_if_dict_array': decode_if_dict_array}, lmps__saqs)
        impl = lmps__saqs['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        xenhe__rmm = np.int32(numba_to_c_type(types.int32))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            mfzqs__aqx = bodo.libs.array_item_arr_ext.get_offsets(data)
            hprcr__pdv = bodo.libs.array_item_arr_ext.get_data(data)
            hprcr__pdv = hprcr__pdv[:mfzqs__aqx[-1]]
            ipqdl__fgvxo = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            vvc__thalc = bcast_scalar(len(data))
            gvpjb__taxz = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                gvpjb__taxz[i] = mfzqs__aqx[i + 1] - mfzqs__aqx[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                vvc__thalc)
            eiaa__saxv = bodo.ir.join.calc_disp(send_counts)
            ubcdt__ihqdx = np.empty(n_pes, np.int32)
            if rank == 0:
                hkuxd__ehx = 0
                for i in range(n_pes):
                    atvy__fszmz = 0
                    for syjd__pzh in range(send_counts[i]):
                        atvy__fszmz += gvpjb__taxz[hkuxd__ehx]
                        hkuxd__ehx += 1
                    ubcdt__ihqdx[i] = atvy__fszmz
            bcast(ubcdt__ihqdx)
            kojvf__ejd = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                kojvf__ejd[i] = send_counts[i] + 7 >> 3
            qvt__ctclb = bodo.ir.join.calc_disp(kojvf__ejd)
            lafb__vafy = send_counts[rank]
            ohube__lrcx = np.empty(lafb__vafy + 1, np_offset_type)
            anku__yhet = bodo.libs.distributed_api.scatterv_impl(hprcr__pdv,
                ubcdt__ihqdx)
            bwitz__moczq = lafb__vafy + 7 >> 3
            qqvuh__egy = np.empty(bwitz__moczq, np.uint8)
            jsde__fajhh = np.empty(lafb__vafy, np.uint32)
            c_scatterv(gvpjb__taxz.ctypes, send_counts.ctypes, eiaa__saxv.
                ctypes, jsde__fajhh.ctypes, np.int32(lafb__vafy), xenhe__rmm)
            convert_len_arr_to_offset(jsde__fajhh.ctypes, ohube__lrcx.
                ctypes, lafb__vafy)
            mzzeg__plnjf = get_scatter_null_bytes_buff(ipqdl__fgvxo.ctypes,
                send_counts, kojvf__ejd)
            c_scatterv(mzzeg__plnjf.ctypes, kojvf__ejd.ctypes, qvt__ctclb.
                ctypes, qqvuh__egy.ctypes, np.int32(bwitz__moczq), rkzh__krbvp)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                lafb__vafy, anku__yhet, ohube__lrcx, qqvuh__egy)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            fkm__mclhs = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            fkm__mclhs = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            fkm__mclhs = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            fkm__mclhs = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            fkm__mclhs = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            tse__yyz = data._data
            vuz__gtcq = data._null_bitmap
            nwf__nsz = len(tse__yyz)
            sgnzk__vyeqc = _scatterv_np(tse__yyz, send_counts)
            vvc__thalc = bcast_scalar(nwf__nsz)
            vtt__rdpd = len(sgnzk__vyeqc) + 7 >> 3
            xyme__ywai = np.empty(vtt__rdpd, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                vvc__thalc)
            kojvf__ejd = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                kojvf__ejd[i] = send_counts[i] + 7 >> 3
            qvt__ctclb = bodo.ir.join.calc_disp(kojvf__ejd)
            mzzeg__plnjf = get_scatter_null_bytes_buff(vuz__gtcq.ctypes,
                send_counts, kojvf__ejd)
            c_scatterv(mzzeg__plnjf.ctypes, kojvf__ejd.ctypes, qvt__ctclb.
                ctypes, xyme__ywai.ctypes, np.int32(vtt__rdpd), rkzh__krbvp)
            return fkm__mclhs(sgnzk__vyeqc, xyme__ywai)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            tam__cscbu = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            pda__laqcz = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(tam__cscbu,
                pda__laqcz)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            ezj__zzllq = data._start
            vwds__pxhbp = data._stop
            cwl__yomv = data._step
            drofd__qrhoh = data._name
            drofd__qrhoh = bcast_scalar(drofd__qrhoh)
            ezj__zzllq = bcast_scalar(ezj__zzllq)
            vwds__pxhbp = bcast_scalar(vwds__pxhbp)
            cwl__yomv = bcast_scalar(cwl__yomv)
            ylhhv__xnwi = bodo.libs.array_kernels.calc_nitems(ezj__zzllq,
                vwds__pxhbp, cwl__yomv)
            chunk_start = bodo.libs.distributed_api.get_start(ylhhv__xnwi,
                n_pes, rank)
            mudmc__zyh = bodo.libs.distributed_api.get_node_portion(ylhhv__xnwi
                , n_pes, rank)
            twx__zdqch = ezj__zzllq + cwl__yomv * chunk_start
            mwgnh__vks = ezj__zzllq + cwl__yomv * (chunk_start + mudmc__zyh)
            mwgnh__vks = min(mwgnh__vks, vwds__pxhbp)
            return bodo.hiframes.pd_index_ext.init_range_index(twx__zdqch,
                mwgnh__vks, cwl__yomv, drofd__qrhoh)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        cti__rrpz = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            tse__yyz = data._data
            drofd__qrhoh = data._name
            drofd__qrhoh = bcast_scalar(drofd__qrhoh)
            arr = bodo.libs.distributed_api.scatterv_impl(tse__yyz, send_counts
                )
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                drofd__qrhoh, cti__rrpz)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            tse__yyz = data._data
            drofd__qrhoh = data._name
            drofd__qrhoh = bcast_scalar(drofd__qrhoh)
            arr = bodo.libs.distributed_api.scatterv_impl(tse__yyz, send_counts
                )
            return bodo.utils.conversion.index_from_array(arr, drofd__qrhoh)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            ooh__natt = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            drofd__qrhoh = bcast_scalar(data._name)
            wunn__weh = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(ooh__natt,
                wunn__weh, drofd__qrhoh)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            drofd__qrhoh = bodo.hiframes.pd_series_ext.get_series_name(data)
            vvz__nidwu = bcast_scalar(drofd__qrhoh)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            wnge__vexhd = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wnge__vexhd, vvz__nidwu)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kpkg__fzyk = len(data.columns)
        kir__pdo = ColNamesMetaType(data.columns)
        chj__cijws = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            chj__cijws += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            chj__cijws += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            fafsj__zwpdu = 'g_table'
        else:
            for i in range(kpkg__fzyk):
                chj__cijws += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                chj__cijws += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            fafsj__zwpdu = ', '.join(f'g_data_{i}' for i in range(kpkg__fzyk))
        chj__cijws += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        chj__cijws += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        chj__cijws += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({fafsj__zwpdu},), g_index, __col_name_meta_scaterv_impl)
"""
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            kir__pdo}, lmps__saqs)
        ogrq__col = lmps__saqs['impl_df']
        return ogrq__col
    if isinstance(data, bodo.TableType):
        chj__cijws = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        chj__cijws += '  T = data\n'
        chj__cijws += '  T2 = init_table(T, False)\n'
        chj__cijws += '  l = 0\n'
        gzpw__ilkpp = {}
        for dzqk__kfi in data.type_to_blk.values():
            gzpw__ilkpp[f'arr_inds_{dzqk__kfi}'] = np.array(data.
                block_to_arr_ind[dzqk__kfi], dtype=np.int64)
            chj__cijws += (
                f'  arr_list_{dzqk__kfi} = get_table_block(T, {dzqk__kfi})\n')
            chj__cijws += f"""  out_arr_list_{dzqk__kfi} = alloc_list_like(arr_list_{dzqk__kfi}, len(arr_list_{dzqk__kfi}), False)
"""
            chj__cijws += f'  for i in range(len(arr_list_{dzqk__kfi})):\n'
            chj__cijws += (
                f'    arr_ind_{dzqk__kfi} = arr_inds_{dzqk__kfi}[i]\n')
            chj__cijws += f"""    ensure_column_unboxed(T, arr_list_{dzqk__kfi}, i, arr_ind_{dzqk__kfi})
"""
            chj__cijws += f"""    out_arr_{dzqk__kfi} = bodo.libs.distributed_api.scatterv_impl(arr_list_{dzqk__kfi}[i], send_counts)
"""
            chj__cijws += (
                f'    out_arr_list_{dzqk__kfi}[i] = out_arr_{dzqk__kfi}\n')
            chj__cijws += f'    l = len(out_arr_{dzqk__kfi})\n'
            chj__cijws += (
                f'  T2 = set_table_block(T2, out_arr_list_{dzqk__kfi}, {dzqk__kfi})\n'
                )
        chj__cijws += f'  T2 = set_table_len(T2, l)\n'
        chj__cijws += f'  return T2\n'
        gzpw__ilkpp.update({'bodo': bodo, 'init_table': bodo.hiframes.table
            .init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        lmps__saqs = {}
        exec(chj__cijws, gzpw__ilkpp, lmps__saqs)
        return lmps__saqs['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                zxe__tzj = data._data
                bodo.libs.distributed_api.bcast_scalar(len(zxe__tzj))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(zxe__tzj)))
            else:
                pfqy__pvdi = bodo.libs.distributed_api.bcast_scalar(0)
                gguy__ifgwx = bodo.libs.distributed_api.bcast_scalar(0)
                zxe__tzj = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    pfqy__pvdi, gguy__ifgwx)
            bodo.libs.distributed_api.bcast(zxe__tzj)
            uwy__wzquu = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(zxe__tzj,
                uwy__wzquu, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            qct__gmsh = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                qct__gmsh, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        chj__cijws = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        chj__cijws += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo}, lmps__saqs)
        dxxw__abd = lmps__saqs['impl_tuple']
        return dxxw__abd
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType)) or data in (
        boolean_array, datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if isinstance(data, DatetimeArrayType):

        def bcast_impl_tz_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            return
        return bcast_impl_tz_arr
    if is_str_arr_type(data) or data == binary_array_type:
        jvdz__ony = np.int32(numba_to_c_type(offset_type))
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            lafb__vafy = len(data)
            bzuno__efawv = num_total_chars(data)
            assert lafb__vafy < INT_MAX
            assert bzuno__efawv < INT_MAX
            oigd__uymx = get_offset_ptr(data)
            splp__jhsj = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            lbuwh__thrc = lafb__vafy + 7 >> 3
            c_bcast(oigd__uymx, np.int32(lafb__vafy + 1), jvdz__ony, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(splp__jhsj, np.int32(bzuno__efawv), rkzh__krbvp, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(lbuwh__thrc), rkzh__krbvp, np
                .array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                wzinn__auvn = 0
                zqf__aqyu = np.empty(0, np.uint8).ctypes
            else:
                zqf__aqyu, wzinn__auvn = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            wzinn__auvn = bodo.libs.distributed_api.bcast_scalar(wzinn__auvn,
                root)
            if rank != root:
                gaal__uhyj = np.empty(wzinn__auvn + 1, np.uint8)
                gaal__uhyj[wzinn__auvn] = 0
                zqf__aqyu = gaal__uhyj.ctypes
            c_bcast(zqf__aqyu, np.int32(wzinn__auvn), rkzh__krbvp, np.array
                ([-1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(zqf__aqyu, wzinn__auvn)
        return impl_str
    typ_val = numba_to_c_type(val)
    chj__cijws = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    lmps__saqs = {}
    exec(chj__cijws, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, lmps__saqs)
    eqa__sxk = lmps__saqs['bcast_scalar_impl']
    return eqa__sxk


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    oykh__baza = len(val)
    chj__cijws = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    chj__cijws += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(oykh__baza)),
        ',' if oykh__baza else '')
    lmps__saqs = {}
    exec(chj__cijws, {'bcast_scalar': bcast_scalar}, lmps__saqs)
    pgud__vvcf = lmps__saqs['bcast_tuple_impl']
    return pgud__vvcf


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            lafb__vafy = bcast_scalar(len(arr), root)
            sik__tugo = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(lafb__vafy, sik__tugo)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):
    if not idx.has_step:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            twx__zdqch = max(arr_start, slice_index.start) - arr_start
            mwgnh__vks = max(slice_index.stop - arr_start, 0)
            return slice(twx__zdqch, mwgnh__vks)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            ezj__zzllq = slice_index.start
            cwl__yomv = slice_index.step
            ewbw__dytv = (0 if cwl__yomv == 1 or ezj__zzllq > arr_start else
                abs(cwl__yomv - arr_start % cwl__yomv) % cwl__yomv)
            twx__zdqch = max(arr_start, slice_index.start
                ) - arr_start + ewbw__dytv
            mwgnh__vks = max(slice_index.stop - arr_start, 0)
            return slice(twx__zdqch, mwgnh__vks, cwl__yomv)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        kemro__kqtit = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[kemro__kqtit])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        genh__bphq = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        rkzh__krbvp = np.int32(numba_to_c_type(types.uint8))
        dvgj__nsi = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            ilpie__bhlv = np.int32(10)
            tag = np.int32(11)
            ody__oyd = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                sxzg__nykh = arr._data
                ckujj__iybh = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    sxzg__nykh, ind)
                wcd__fceo = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    sxzg__nykh, ind + 1)
                length = wcd__fceo - ckujj__iybh
                trrw__ewhc = sxzg__nykh[ind]
                ody__oyd[0] = length
                isend(ody__oyd, np.int32(1), root, ilpie__bhlv, True)
                isend(trrw__ewhc, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(dvgj__nsi,
                genh__bphq, 0, 1)
            pfqy__pvdi = 0
            if rank == root:
                pfqy__pvdi = recv(np.int64, ANY_SOURCE, ilpie__bhlv)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    dvgj__nsi, genh__bphq, pfqy__pvdi, 1)
                splp__jhsj = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(splp__jhsj, np.int32(pfqy__pvdi), rkzh__krbvp,
                    ANY_SOURCE, tag)
            dummy_use(ody__oyd)
            pfqy__pvdi = bcast_scalar(pfqy__pvdi)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    dvgj__nsi, genh__bphq, pfqy__pvdi, 1)
            splp__jhsj = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(splp__jhsj, np.int32(pfqy__pvdi), rkzh__krbvp, np.array
                ([-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, pfqy__pvdi)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        wcsu__tpw = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, wcsu__tpw)
            if arr_start <= ind < arr_start + len(arr):
                qct__gmsh = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = qct__gmsh[ind - arr_start]
                send_arr = np.full(1, data, wcsu__tpw)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = wcsu__tpw(-1)
            if rank == root:
                val = recv(wcsu__tpw, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            xio__vednv = arr.dtype.categories[max(val, 0)]
            return xio__vednv
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        kzxvd__inhv = arr.tz

        def tz_aware_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                data = arr[ind - arr_start].value
                send_arr = np.full(1, data)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = 0
            if rank == root:
                val = recv(np.int64, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(val,
                kzxvd__inhv)
        return tz_aware_getitem_impl
    cwt__wfal = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, cwt__wfal)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, cwt__wfal)[0]
        if rank == root:
            val = recv(cwt__wfal, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


def get_chunk_bounds(A):
    pass


@overload(get_chunk_bounds, jit_options={'cache': True})
def get_chunk_bounds_overload(A):
    if not (isinstance(A, types.Array) and isinstance(A.dtype, types.Integer)):
        raise BodoError(
            'get_chunk_bounds() only supports Numpy int input currently.')

    def impl(A):
        n_pes = get_size()
        hshl__sprwa = np.empty(n_pes, np.int64)
        asulh__ngbud = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        pnm__djedy = 1
        if len(A) != 0:
            val = A[-1]
            pnm__djedy = 0
        allgather(hshl__sprwa, np.int64(val))
        allgather(asulh__ngbud, pnm__djedy)
        for i, pnm__djedy in enumerate(asulh__ngbud):
            if pnm__djedy and i != 0:
                hshl__sprwa[i] = hshl__sprwa[i - 1]
        return hshl__sprwa
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    hngv__suk = get_type_enum(out_data)
    assert typ_enum == hngv__suk
    if isinstance(send_data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or send_data in (boolean_array,
        datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    chj__cijws = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        chj__cijws += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    chj__cijws += '  return\n'
    lmps__saqs = {}
    exec(chj__cijws, {'alltoallv': alltoallv}, lmps__saqs)
    krsv__asch = lmps__saqs['f']
    return krsv__asch


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    ezj__zzllq = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return ezj__zzllq, count


@numba.njit
def get_start(total_size, pes, rank):
    xjva__ykevw = total_size % pes
    suz__wob = (total_size - xjva__ykevw) // pes
    return rank * suz__wob + min(rank, xjva__ykevw)


@numba.njit
def get_end(total_size, pes, rank):
    xjva__ykevw = total_size % pes
    suz__wob = (total_size - xjva__ykevw) // pes
    return (rank + 1) * suz__wob + min(rank + 1, xjva__ykevw)


@numba.njit
def get_node_portion(total_size, pes, rank):
    xjva__ykevw = total_size % pes
    suz__wob = (total_size - xjva__ykevw) // pes
    if rank < xjva__ykevw:
        return suz__wob + 1
    else:
        return suz__wob


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    uhm__zfnzj = in_arr.dtype(0)
    yghze__nbwt = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        atvy__fszmz = uhm__zfnzj
        for liooz__pmol in np.nditer(in_arr):
            atvy__fszmz += liooz__pmol.item()
        xqe__mvzxk = dist_exscan(atvy__fszmz, yghze__nbwt)
        for i in range(in_arr.size):
            xqe__mvzxk += in_arr[i]
            out_arr[i] = xqe__mvzxk
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    bdye__rvmoz = in_arr.dtype(1)
    yghze__nbwt = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        atvy__fszmz = bdye__rvmoz
        for liooz__pmol in np.nditer(in_arr):
            atvy__fszmz *= liooz__pmol.item()
        xqe__mvzxk = dist_exscan(atvy__fszmz, yghze__nbwt)
        if get_rank() == 0:
            xqe__mvzxk = bdye__rvmoz
        for i in range(in_arr.size):
            xqe__mvzxk *= in_arr[i]
            out_arr[i] = xqe__mvzxk
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        bdye__rvmoz = np.finfo(in_arr.dtype(1).dtype).max
    else:
        bdye__rvmoz = np.iinfo(in_arr.dtype(1).dtype).max
    yghze__nbwt = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        atvy__fszmz = bdye__rvmoz
        for liooz__pmol in np.nditer(in_arr):
            atvy__fszmz = min(atvy__fszmz, liooz__pmol.item())
        xqe__mvzxk = dist_exscan(atvy__fszmz, yghze__nbwt)
        if get_rank() == 0:
            xqe__mvzxk = bdye__rvmoz
        for i in range(in_arr.size):
            xqe__mvzxk = min(xqe__mvzxk, in_arr[i])
            out_arr[i] = xqe__mvzxk
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        bdye__rvmoz = np.finfo(in_arr.dtype(1).dtype).min
    else:
        bdye__rvmoz = np.iinfo(in_arr.dtype(1).dtype).min
    bdye__rvmoz = in_arr.dtype(1)
    yghze__nbwt = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        atvy__fszmz = bdye__rvmoz
        for liooz__pmol in np.nditer(in_arr):
            atvy__fszmz = max(atvy__fszmz, liooz__pmol.item())
        xqe__mvzxk = dist_exscan(atvy__fszmz, yghze__nbwt)
        if get_rank() == 0:
            xqe__mvzxk = bdye__rvmoz
        for i in range(in_arr.size):
            xqe__mvzxk = max(xqe__mvzxk, in_arr[i])
            out_arr[i] = xqe__mvzxk
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    giz__fcgkc = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), giz__fcgkc)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ehbu__apz = args[0]
    if equiv_set.has_shape(ehbu__apz):
        return ArrayAnalysis.AnalyzeResult(shape=ehbu__apz, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    hkgef__dby = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for 
        i, cfe__gxcs in enumerate(args) if is_array_typ(cfe__gxcs) or
        isinstance(cfe__gxcs, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    chj__cijws = f"""def impl(*args):
    if {hkgef__dby} or bodo.get_rank() == 0:
        print(*args)"""
    lmps__saqs = {}
    exec(chj__cijws, globals(), lmps__saqs)
    impl = lmps__saqs['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        mspim__hgsnr = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        chj__cijws = 'def f(req, cond=True):\n'
        chj__cijws += f'  return {mspim__hgsnr}\n'
        lmps__saqs = {}
        exec(chj__cijws, {'_wait': _wait}, lmps__saqs)
        impl = lmps__saqs['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        xjva__ykevw = 1
        for a in t:
            xjva__ykevw *= a
        return xjva__ykevw
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    cvey__ttvjv = np.ascontiguousarray(in_arr)
    tftjk__dibx = get_tuple_prod(cvey__ttvjv.shape[1:])
    vddue__dcdtx = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        jzc__iig = np.array(dest_ranks, dtype=np.int32)
    else:
        jzc__iig = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, cvey__ttvjv.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * vddue__dcdtx, 
        dtype_size * tftjk__dibx, len(jzc__iig), jzc__iig.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp, types.int64))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len,
    n_samples):
    kgnes__rscz = np.ascontiguousarray(rhs)
    jvd__abrkp = get_tuple_prod(kgnes__rscz.shape[1:])
    tzn__pzhcn = dtype_size * jvd__abrkp
    permutation_array_index(lhs.ctypes, lhs_len, tzn__pzhcn, kgnes__rscz.
        ctypes, kgnes__rscz.shape[0], p.ctypes, p_len, n_samples)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def disconnect_hdfs_njit():
    disconnect_hdfs()


@numba.njit
def call_finalize():
    finalize()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        chj__cijws = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, lmps__saqs)
        eqa__sxk = lmps__saqs['bcast_scalar_impl']
        return eqa__sxk
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        kpkg__fzyk = len(data.columns)
        fafsj__zwpdu = ', '.join('g_data_{}'.format(i) for i in range(
            kpkg__fzyk))
        uzon__kumyg = ColNamesMetaType(data.columns)
        chj__cijws = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(kpkg__fzyk):
            chj__cijws += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            chj__cijws += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        chj__cijws += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        chj__cijws += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        chj__cijws += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(fafsj__zwpdu))
        lmps__saqs = {}
        exec(chj__cijws, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            uzon__kumyg}, lmps__saqs)
        ogrq__col = lmps__saqs['impl_df']
        return ogrq__col
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            ezj__zzllq = data._start
            vwds__pxhbp = data._stop
            cwl__yomv = data._step
            drofd__qrhoh = data._name
            drofd__qrhoh = bcast_scalar(drofd__qrhoh, root)
            ezj__zzllq = bcast_scalar(ezj__zzllq, root)
            vwds__pxhbp = bcast_scalar(vwds__pxhbp, root)
            cwl__yomv = bcast_scalar(cwl__yomv, root)
            ylhhv__xnwi = bodo.libs.array_kernels.calc_nitems(ezj__zzllq,
                vwds__pxhbp, cwl__yomv)
            chunk_start = bodo.libs.distributed_api.get_start(ylhhv__xnwi,
                n_pes, rank)
            mudmc__zyh = bodo.libs.distributed_api.get_node_portion(ylhhv__xnwi
                , n_pes, rank)
            twx__zdqch = ezj__zzllq + cwl__yomv * chunk_start
            mwgnh__vks = ezj__zzllq + cwl__yomv * (chunk_start + mudmc__zyh)
            mwgnh__vks = min(mwgnh__vks, vwds__pxhbp)
            return bodo.hiframes.pd_index_ext.init_range_index(twx__zdqch,
                mwgnh__vks, cwl__yomv, drofd__qrhoh)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            tse__yyz = data._data
            drofd__qrhoh = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(tse__yyz,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, drofd__qrhoh)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            drofd__qrhoh = bodo.hiframes.pd_series_ext.get_series_name(data)
            vvz__nidwu = bodo.libs.distributed_api.bcast_comm_impl(drofd__qrhoh
                , comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            wnge__vexhd = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                wnge__vexhd, vvz__nidwu)
        return impl_series
    if isinstance(data, types.BaseTuple):
        chj__cijws = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        chj__cijws += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        lmps__saqs = {}
        exec(chj__cijws, {'bcast_comm_impl': bcast_comm_impl}, lmps__saqs)
        dxxw__abd = lmps__saqs['impl_tuple']
        return dxxw__abd
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    pfv__mekjp = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    fxl__xhlh = (0,) * pfv__mekjp

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        tse__yyz = np.ascontiguousarray(data)
        splp__jhsj = data.ctypes
        ptoz__yfcjl = fxl__xhlh
        if rank == root:
            ptoz__yfcjl = tse__yyz.shape
        ptoz__yfcjl = bcast_tuple(ptoz__yfcjl, root)
        mfrxp__gmx = get_tuple_prod(ptoz__yfcjl[1:])
        send_counts = ptoz__yfcjl[0] * mfrxp__gmx
        izs__kwa = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(splp__jhsj, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(izs__kwa.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return izs__kwa.reshape((-1,) + ptoz__yfcjl[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        kag__eqdr = MPI.COMM_WORLD
        idh__aizvy = MPI.Get_processor_name()
        sgv__egmhj = kag__eqdr.allgather(idh__aizvy)
        node_ranks = defaultdict(list)
        for i, lnyls__nazij in enumerate(sgv__egmhj):
            node_ranks[lnyls__nazij].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    kag__eqdr = MPI.COMM_WORLD
    tmcf__quz = kag__eqdr.Get_group()
    cthah__slw = tmcf__quz.Incl(comm_ranks)
    afvl__zsh = kag__eqdr.Create_group(cthah__slw)
    return afvl__zsh


def get_nodes_first_ranks():
    hscw__hzqkf = get_host_ranks()
    return np.array([dcva__eobos[0] for dcva__eobos in hscw__hzqkf.values()
        ], dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
