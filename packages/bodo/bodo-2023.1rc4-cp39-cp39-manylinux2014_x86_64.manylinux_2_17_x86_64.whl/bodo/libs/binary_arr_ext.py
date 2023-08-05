"""Array implementation for binary (bytes) objects, which are usually immutable.
It is equivalent to string array, except that it stores a 'bytes' object for each
element instead of 'str'.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, overload, overload_attribute, overload_method
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.utils.typing import BodoError, is_list_like_index_type
_bytes_fromhex = types.ExternalFunction('bytes_fromhex', types.int64(types.
    voidptr, types.voidptr, types.uint64))
ll.add_symbol('bytes_to_hex', hstr_ext.bytes_to_hex)
ll.add_symbol('bytes_fromhex', hstr_ext.bytes_fromhex)
bytes_type = types.Bytes(types.uint8, 1, 'C', readonly=True)
ll.add_symbol('setitem_binary_array', hstr_ext.setitem_binary_array)
char_type = types.uint8
setitem_binary_array = types.ExternalFunction('setitem_binary_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, types.intp))


@overload(len)
def bytes_len_overload(bytes_obj):
    if isinstance(bytes_obj, types.Bytes):
        return lambda bytes_obj: bytes_obj._nitems


@overload(operator.getitem, no_unliteral=True)
def bytes_getitem(byte_obj, ind):
    if not isinstance(byte_obj, types.Bytes):
        return
    if isinstance(ind, types.SliceType):

        def impl(byte_obj, ind):
            arr = cast_bytes_uint8array(byte_obj)
            wtgcb__xki = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(wtgcb__xki)
        return impl


class BinaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(BinaryArrayType, self).__init__(name='BinaryArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return bytes_type

    def copy(self):
        return BinaryArrayType()

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


binary_array_type = BinaryArrayType()


@overload(len, no_unliteral=True)
def bin_arr_len_overload(bin_arr):
    if bin_arr == binary_array_type:
        return lambda bin_arr: len(bin_arr._data)


make_attribute_wrapper(types.Bytes, 'nitems', '_nitems')


@overload_attribute(BinaryArrayType, 'size')
def bin_arr_size_overload(bin_arr):
    return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'shape')
def bin_arr_shape_overload(bin_arr):
    return lambda bin_arr: (len(bin_arr._data),)


@overload_attribute(BinaryArrayType, 'nbytes')
def bin_arr_nbytes_overload(bin_arr):
    return lambda bin_arr: bin_arr._data.nbytes


@overload_attribute(BinaryArrayType, 'ndim')
def overload_bin_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BinaryArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: np.dtype('O')


@numba.njit
def pre_alloc_binary_array(n_bytestrs, n_chars):
    if n_chars is None:
        n_chars = -1
    bin_arr = init_binary_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_bytestrs), (np.int64(n_chars)
        ,), bodo.libs.str_arr_ext.char_arr_type))
    if n_chars == 0:
        bodo.libs.str_arr_ext.set_all_offsets_to_0(bin_arr)
    return bin_arr


@intrinsic
def init_binary_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        jwov__kwv, = args
        rxrw__onj = context.make_helper(builder, binary_array_type)
        rxrw__onj.data = jwov__kwv
        context.nrt.incref(builder, data_typ, jwov__kwv)
        return rxrw__onj._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        gphk__aroww = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        yjlum__bmyn = args[1]
        ppdc__rfc = cgutils.create_struct_proxy(bytes_type)(context, builder)
        ppdc__rfc.meminfo = context.nrt.meminfo_alloc(builder, yjlum__bmyn)
        ppdc__rfc.nitems = yjlum__bmyn
        ppdc__rfc.itemsize = lir.Constant(ppdc__rfc.itemsize.type, 1)
        ppdc__rfc.data = context.nrt.meminfo_data(builder, ppdc__rfc.meminfo)
        ppdc__rfc.parent = cgutils.get_null_value(ppdc__rfc.parent.type)
        ppdc__rfc.shape = cgutils.pack_array(builder, [yjlum__bmyn],
            context.get_value_type(types.intp))
        ppdc__rfc.strides = gphk__aroww.strides
        cgutils.memcpy(builder, ppdc__rfc.data, gphk__aroww.data, yjlum__bmyn)
        return ppdc__rfc._getvalue()
    return bytes_type(data_typ, length_type), codegen


@intrinsic
def cast_bytes_uint8array(typingctx, data_typ):
    assert data_typ == bytes_type

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return types.Array(types.uint8, 1, 'C')(data_typ), codegen


@intrinsic
def cast_uint8array_bytes(typingctx, data_typ):
    assert data_typ == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return bytes_type(data_typ), codegen


@overload_method(BinaryArrayType, 'copy', no_unliteral=True)
def binary_arr_copy_overload(arr):

    def copy_impl(arr):
        return init_binary_arr(arr._data.copy())
    return copy_impl


@overload_method(types.Bytes, 'hex')
def binary_arr_hex(arr):
    bxyt__tmtra = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        yjlum__bmyn = len(arr) * 2
        output = numba.cpython.unicode._empty_string(bxyt__tmtra,
            yjlum__bmyn, 1)
        bytes_to_hex(output, arr)
        return output
    return impl


@lower_cast(types.CPointer(types.uint8), types.voidptr)
def cast_uint8_array_to_voidptr(context, builder, fromty, toty, val):
    return val


make_attribute_wrapper(types.Bytes, 'data', '_data')


@overload_method(types.Bytes, '__hash__')
def bytes_hash(arr):

    def impl(arr):
        return numba.cpython.hashing._Py_HashBytes(arr._data, len(arr))
    return impl


@intrinsic
def bytes_to_hex(typingctx, output, arr):

    def codegen(context, builder, sig, args):
        gaxa__rons = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        qikke__ryygw = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        eol__zao = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        hmux__lrbq = cgutils.get_or_insert_function(builder.module,
            eol__zao, name='bytes_to_hex')
        builder.call(hmux__lrbq, (gaxa__rons.data, qikke__ryygw.data,
            qikke__ryygw.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            qhil__svt = arr._data[ind]
            return init_bytes_type(qhil__svt, len(qhil__svt))
        return impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind) and (ind.
        dtype == types.bool_ or isinstance(ind.dtype, types.Integer)
        ) or isinstance(ind, types.SliceType):
        return lambda arr, ind: init_binary_arr(arr._data[ind])
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for Binary Array with indexing type {ind} not supported.'
            )


def bytes_fromhex(hex_str):
    pass


@overload(bytes_fromhex)
def overload_bytes_fromhex(hex_str):
    hex_str = types.unliteral(hex_str)
    if hex_str == bodo.string_type:
        bxyt__tmtra = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != bxyt__tmtra:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            jwov__kwv = np.empty(len(hex_str) // 2, np.uint8)
            yjlum__bmyn = _bytes_fromhex(jwov__kwv.ctypes, hex_str._data,
                len(hex_str))
            jepne__bxkuj = init_bytes_type(jwov__kwv, yjlum__bmyn)
            return jepne__bxkuj
        return impl
    raise BodoError(f'bytes.fromhex not supported with argument type {hex_str}'
        )


def binary_list_to_array(binary_list):
    return binary_list


@overload(binary_list_to_array, no_unliteral=True)
def binary_list_to_array_overload(binary_list):
    if isinstance(binary_list, types.List
        ) and binary_list.dtype == bodo.bytes_type:

        def binary_list_impl(binary_list):
            uen__dngf = len(binary_list)
            uojq__vnur = pre_alloc_binary_array(uen__dngf, -1)
            for uhdoa__nto in range(uen__dngf):
                owi__uwj = binary_list[uhdoa__nto]
                uojq__vnur[uhdoa__nto] = owi__uwj
            return uojq__vnur
        return binary_list_impl
    raise BodoError(
        f'Error, binary_list_to_array not supported for type {binary_list}')


@overload(operator.setitem)
def binary_arr_setitem(arr, ind, val):
    from bodo.libs.str_arr_ext import get_data_ptr, get_offset_ptr, getitem_str_offset, num_total_chars, set_string_array_range, str_arr_is_na, str_arr_set_na, str_arr_set_not_na
    if arr != binary_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    uieb__hwkru = (
        f'Binary array setitem with index {ind} and value {val} not supported.'
        )
    if isinstance(ind, types.Integer):
        if val != bytes_type:
            raise BodoError(uieb__hwkru)
        toal__lntxu = numba.njit(lambda a: None)

        def impl(arr, ind, val):
            jwov__kwv = arr._data
            emm__jue = cast_bytes_uint8array(val)
            aiz__upg = len(emm__jue)
            xia__jup = np.int64(getitem_str_offset(arr, ind))
            tih__pxgjk = xia__jup + aiz__upg
            bodo.libs.array_item_arr_ext.ensure_data_capacity(jwov__kwv,
                xia__jup, tih__pxgjk)
            setitem_binary_array(get_offset_ptr(arr), get_data_ptr(arr),
                tih__pxgjk, emm__jue.ctypes, aiz__upg, ind)
            str_arr_set_not_na(arr, ind)
            toal__lntxu(arr)
            toal__lntxu(val)
        return impl
    elif isinstance(ind, types.SliceType):
        if val == binary_array_type:

            def impl_slice(arr, ind, val):
                haysw__awdq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                rfri__zkgpz = haysw__awdq.start
                jwov__kwv = arr._data
                xia__jup = np.int64(getitem_str_offset(arr, rfri__zkgpz))
                tih__pxgjk = xia__jup + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(jwov__kwv,
                    xia__jup, tih__pxgjk)
                set_string_array_range(arr, val, rfri__zkgpz, xia__jup)
                rwn__pijmm = 0
                for uhdoa__nto in range(haysw__awdq.start, haysw__awdq.stop,
                    haysw__awdq.step):
                    if str_arr_is_na(val, rwn__pijmm):
                        str_arr_set_na(arr, uhdoa__nto)
                    else:
                        str_arr_set_not_na(arr, uhdoa__nto)
                    rwn__pijmm += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == bytes_type:

            def impl_slice_list(arr, ind, val):
                elc__voys = binary_list_to_array(val)
                arr[ind] = elc__voys
            return impl_slice_list
        elif val == bytes_type:

            def impl_slice(arr, ind, val):
                haysw__awdq = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for uhdoa__nto in range(haysw__awdq.start, haysw__awdq.stop,
                    haysw__awdq.step):
                    arr[uhdoa__nto] = val
            return impl_slice
    raise BodoError(uieb__hwkru)


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        cujt__nyd = lhs == binary_array_type
        tbbif__qjfhk = rhs == binary_array_type
        stk__gax = 'lhs' if cujt__nyd else 'rhs'
        jux__vsfii = 'def impl(lhs, rhs):\n'
        jux__vsfii += '  numba.parfors.parfor.init_prange()\n'
        jux__vsfii += f'  n = len({stk__gax})\n'
        jux__vsfii += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        jux__vsfii += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        nhm__hxtcj = []
        if cujt__nyd:
            nhm__hxtcj.append('bodo.libs.array_kernels.isna(lhs, i)')
        if tbbif__qjfhk:
            nhm__hxtcj.append('bodo.libs.array_kernels.isna(rhs, i)')
        jux__vsfii += f"    if {' or '.join(nhm__hxtcj)}:\n"
        jux__vsfii += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        jux__vsfii += '      continue\n'
        vyrnm__lax = 'lhs[i]' if cujt__nyd else 'lhs'
        gvleq__zwd = 'rhs[i]' if tbbif__qjfhk else 'rhs'
        jux__vsfii += f'    out_arr[i] = op({vyrnm__lax}, {gvleq__zwd})\n'
        jux__vsfii += '  return out_arr\n'
        ibwl__wfj = {}
        exec(jux__vsfii, {'bodo': bodo, 'numba': numba, 'op': op}, ibwl__wfj)
        return ibwl__wfj['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
