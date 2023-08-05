"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contiguous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
use_pd_pyarrow_string_array = True
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@typeof_impl.register(pd.arrays.ArrowStringArray)
def typeof_pyarrow_string_array(val, c):
    if pa.types.is_dictionary(val._data.combine_chunks().type):
        return bodo.dict_str_arr_type
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kiwax__kln = ArrayItemArrayType(char_arr_type)
        lsjy__vffpg = [('data', kiwax__kln)]
        models.StructModel.__init__(self, dmm, fe_type, lsjy__vffpg)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        zmfec__viar, = args
        fthqw__zerba = context.make_helper(builder, string_array_type)
        fthqw__zerba.data = zmfec__viar
        context.nrt.incref(builder, data_typ, zmfec__viar)
        return fthqw__zerba._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    cdv__rnb = c.context.insert_const_string(c.builder.module, 'pandas')
    exmpk__xbqvy = c.pyapi.import_module_noblock(cdv__rnb)
    wtg__qoywz = c.pyapi.call_method(exmpk__xbqvy, 'StringDtype', ())
    c.pyapi.decref(exmpk__xbqvy)
    return wtg__qoywz


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        ouzfl__xenoi = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if ouzfl__xenoi is not None:
            return ouzfl__xenoi
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                oevz__pmyf = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(oevz__pmyf)
                for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                oevz__pmyf = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(oevz__pmyf)
                for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                oevz__pmyf = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(oevz__pmyf)
                for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    zrgs__umdjt = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    yin__oox = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and yin__oox or zrgs__umdjt and is_str_arr_type(rhs
        ):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    qhagh__ffut = context.make_helper(builder, arr_typ, arr_value)
    kiwax__kln = ArrayItemArrayType(char_arr_type)
    qmf__kbqlu = _get_array_item_arr_payload(context, builder, kiwax__kln,
        qhagh__ffut.data)
    return qmf__kbqlu


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return qmf__kbqlu.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@numba.njit
def check_offsets(str_arr):
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    n_chars = bodo.libs.str_arr_ext.num_total_chars(str_arr)
    for i in range(bodo.libs.array_item_arr_ext.get_n_arrays(str_arr._data)):
        if offsets[i] > n_chars or offsets[i + 1] - offsets[i] < 0:
            print('wrong offset found', i, offsets[i])
            break


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dfb__etti = context.make_helper(builder, offset_arr_type,
            qmf__kbqlu.offsets).data
        return _get_num_total_chars(builder, dfb__etti, qmf__kbqlu.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        tzox__dvjhl = context.make_helper(builder, offset_arr_type,
            qmf__kbqlu.offsets)
        aksc__rhsf = context.make_helper(builder, offset_ctypes_type)
        aksc__rhsf.data = builder.bitcast(tzox__dvjhl.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        aksc__rhsf.meminfo = tzox__dvjhl.meminfo
        wtg__qoywz = aksc__rhsf._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            wtg__qoywz)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        zmfec__viar = context.make_helper(builder, char_arr_type,
            qmf__kbqlu.data)
        aksc__rhsf = context.make_helper(builder, data_ctypes_type)
        aksc__rhsf.data = zmfec__viar.data
        aksc__rhsf.meminfo = zmfec__viar.meminfo
        wtg__qoywz = aksc__rhsf._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, wtg__qoywz
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        hyx__ilkny, ind = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            hyx__ilkny, sig.args[0])
        zmfec__viar = context.make_helper(builder, char_arr_type,
            qmf__kbqlu.data)
        aksc__rhsf = context.make_helper(builder, data_ctypes_type)
        aksc__rhsf.data = builder.gep(zmfec__viar.data, [ind])
        aksc__rhsf.meminfo = zmfec__viar.meminfo
        wtg__qoywz = aksc__rhsf._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, wtg__qoywz
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        vkhvk__rvver, ccr__zhwq, uep__yshuf, vyi__tgs = args
        exqe__neg = builder.bitcast(builder.gep(vkhvk__rvver, [ccr__zhwq]),
            lir.IntType(8).as_pointer())
        hhnn__xen = builder.bitcast(builder.gep(uep__yshuf, [vyi__tgs]),
            lir.IntType(8).as_pointer())
        gljai__unh = builder.load(hhnn__xen)
        builder.store(gljai__unh, exqe__neg)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ihsp__tmpb = context.make_helper(builder, null_bitmap_arr_type,
            qmf__kbqlu.null_bitmap)
        aksc__rhsf = context.make_helper(builder, data_ctypes_type)
        aksc__rhsf.data = ihsp__tmpb.data
        aksc__rhsf.meminfo = ihsp__tmpb.meminfo
        wtg__qoywz = aksc__rhsf._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, wtg__qoywz
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dfb__etti = context.make_helper(builder, offset_arr_type,
            qmf__kbqlu.offsets).data
        return builder.load(builder.gep(dfb__etti, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, qmf__kbqlu.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        efkq__qdm, ind = args
        if in_bitmap_typ == data_ctypes_type:
            aksc__rhsf = context.make_helper(builder, data_ctypes_type,
                efkq__qdm)
            efkq__qdm = aksc__rhsf.data
        return builder.load(builder.gep(efkq__qdm, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        efkq__qdm, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            aksc__rhsf = context.make_helper(builder, data_ctypes_type,
                efkq__qdm)
            efkq__qdm = aksc__rhsf.data
        builder.store(val, builder.gep(efkq__qdm, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        mzjzp__aslll = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ugrg__rgfn = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        gvgi__exap = context.make_helper(builder, offset_arr_type,
            mzjzp__aslll.offsets).data
        qytl__dbc = context.make_helper(builder, offset_arr_type,
            ugrg__rgfn.offsets).data
        qmz__kxgkg = context.make_helper(builder, char_arr_type,
            mzjzp__aslll.data).data
        dtvqy__ubnq = context.make_helper(builder, char_arr_type,
            ugrg__rgfn.data).data
        qkwnb__mgu = context.make_helper(builder, null_bitmap_arr_type,
            mzjzp__aslll.null_bitmap).data
        pfk__ctt = context.make_helper(builder, null_bitmap_arr_type,
            ugrg__rgfn.null_bitmap).data
        gjbfy__zpirx = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, qytl__dbc, gvgi__exap, gjbfy__zpirx)
        cgutils.memcpy(builder, dtvqy__ubnq, qmz__kxgkg, builder.load(
            builder.gep(gvgi__exap, [ind])))
        xspfx__vkiac = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        ihbtu__fdngv = builder.lshr(xspfx__vkiac, lir.Constant(lir.IntType(
            64), 3))
        cgutils.memcpy(builder, pfk__ctt, qkwnb__mgu, ihbtu__fdngv)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        mzjzp__aslll = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ugrg__rgfn = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        gvgi__exap = context.make_helper(builder, offset_arr_type,
            mzjzp__aslll.offsets).data
        qmz__kxgkg = context.make_helper(builder, char_arr_type,
            mzjzp__aslll.data).data
        dtvqy__ubnq = context.make_helper(builder, char_arr_type,
            ugrg__rgfn.data).data
        num_total_chars = _get_num_total_chars(builder, gvgi__exap,
            mzjzp__aslll.n_arrays)
        cgutils.memcpy(builder, dtvqy__ubnq, qmz__kxgkg, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        mzjzp__aslll = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ugrg__rgfn = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        gvgi__exap = context.make_helper(builder, offset_arr_type,
            mzjzp__aslll.offsets).data
        qytl__dbc = context.make_helper(builder, offset_arr_type,
            ugrg__rgfn.offsets).data
        qkwnb__mgu = context.make_helper(builder, null_bitmap_arr_type,
            mzjzp__aslll.null_bitmap).data
        oevz__pmyf = mzjzp__aslll.n_arrays
        ajkti__nlbq = context.get_constant(offset_type, 0)
        mfuok__pwjn = cgutils.alloca_once_value(builder, ajkti__nlbq)
        with cgutils.for_range(builder, oevz__pmyf) as ktg__acx:
            atu__iavff = lower_is_na(context, builder, qkwnb__mgu, ktg__acx
                .index)
            with cgutils.if_likely(builder, builder.not_(atu__iavff)):
                usuwr__bmkoe = builder.load(builder.gep(gvgi__exap, [
                    ktg__acx.index]))
                fqt__drb = builder.load(mfuok__pwjn)
                builder.store(usuwr__bmkoe, builder.gep(qytl__dbc, [fqt__drb]))
                builder.store(builder.add(fqt__drb, lir.Constant(context.
                    get_value_type(offset_type), 1)), mfuok__pwjn)
        fqt__drb = builder.load(mfuok__pwjn)
        usuwr__bmkoe = builder.load(builder.gep(gvgi__exap, [oevz__pmyf]))
        builder.store(usuwr__bmkoe, builder.gep(qytl__dbc, [fqt__drb]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ssa__opmlq, ind, str, mkuyu__jwayu = args
        ssa__opmlq = context.make_array(sig.args[0])(context, builder,
            ssa__opmlq)
        iads__iue = builder.gep(ssa__opmlq.data, [ind])
        cgutils.raw_memcpy(builder, iads__iue, str, mkuyu__jwayu, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        iads__iue, ind, wfhhh__zxgh, mkuyu__jwayu = args
        iads__iue = builder.gep(iads__iue, [ind])
        cgutils.raw_memcpy(builder, iads__iue, wfhhh__zxgh, mkuyu__jwayu, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            trfkc__naj = A._data
            return np.int64(getitem_str_offset(trfkc__naj, idx + 1) -
                getitem_str_offset(trfkc__naj, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    hubdz__xzzec = np.int64(getitem_str_offset(A, i))
    urxwe__tzm = np.int64(getitem_str_offset(A, i + 1))
    l = urxwe__tzm - hubdz__xzzec
    lhgy__agx = get_data_ptr_ind(A, hubdz__xzzec)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(lhgy__agx, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.generated_jit(no_cpython_wrapper=True, nopython=True)
def get_str_arr_item_copy(B, j, A, i):
    if B != string_array_type:
        raise BodoError(
            'get_str_arr_item_copy(): Output array must be a string array')
    if not is_str_arr_type(A):
        raise BodoError(
            'get_str_arr_item_copy(): Input array must be a string array or dictionary encoded array'
            )
    if A == bodo.dict_str_arr_type:
        gvqph__tfyw = 'in_str_arr = A._data'
        dbzaq__gwqv = 'input_index = A._indices[i]'
    else:
        gvqph__tfyw = 'in_str_arr = A'
        dbzaq__gwqv = 'input_index = i'
    rzt__uyg = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {gvqph__tfyw}
        {dbzaq__gwqv}

        # set NA
        if bodo.libs.array_kernels.isna(A, i):
            str_arr_set_na(B, j)
            return
        else:
            str_arr_set_not_na(B, j)

        # get input array offsets
        in_start_offset = getitem_str_offset(in_str_arr, input_index)
        in_end_offset = getitem_str_offset(in_str_arr, input_index + 1)
        val_len = in_end_offset - in_start_offset

        # set output offset
        out_start_offset = getitem_str_offset(B, j)
        out_end_offset = out_start_offset + val_len
        setitem_str_offset(B, j + 1, out_end_offset)

        # copy data
        if val_len != 0:
            # ensure required space in output array
            data_arr = B._data
            bodo.libs.array_item_arr_ext.ensure_data_capacity(
                data_arr, np.int64(out_start_offset), np.int64(out_end_offset)
            )
            out_data_ptr = get_data_ptr(B).data
            in_data_ptr = get_data_ptr(in_str_arr).data
            memcpy_region(
                out_data_ptr,
                out_start_offset,
                in_data_ptr,
                in_start_offset,
                val_len,
                1,
            )"""
    tsc__ysuxt = {}
    exec(rzt__uyg, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, tsc__ysuxt)
    impl = tsc__ysuxt['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    oevz__pmyf = len(str_arr)
    ewnoh__hjpvj = np.empty(oevz__pmyf, np.bool_)
    for i in range(oevz__pmyf):
        ewnoh__hjpvj[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return ewnoh__hjpvj


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            oevz__pmyf = len(data)
            l = []
            for i in range(oevz__pmyf):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        bcj__zcyq = data.count
        fyqs__vlg = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(bcj__zcyq)]
        if is_overload_true(str_null_bools):
            fyqs__vlg += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(bcj__zcyq) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        rzt__uyg = 'def f(data, str_null_bools=None):\n'
        rzt__uyg += '  return ({}{})\n'.format(', '.join(fyqs__vlg), ',' if
            bcj__zcyq == 1 else '')
        tsc__ysuxt = {}
        exec(rzt__uyg, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, tsc__ysuxt)
        eyj__rmmp = tsc__ysuxt['f']
        return eyj__rmmp
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                oevz__pmyf = len(list_data)
                for i in range(oevz__pmyf):
                    wfhhh__zxgh = list_data[i]
                    str_arr[i] = wfhhh__zxgh
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                oevz__pmyf = len(list_data)
                for i in range(oevz__pmyf):
                    wfhhh__zxgh = list_data[i]
                    str_arr[i] = wfhhh__zxgh
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        bcj__zcyq = str_arr.count
        wwh__znoc = 0
        rzt__uyg = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(bcj__zcyq):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                rzt__uyg += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, bcj__zcyq + wwh__znoc))
                wwh__znoc += 1
            else:
                rzt__uyg += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        rzt__uyg += '  return\n'
        tsc__ysuxt = {}
        exec(rzt__uyg, {'cp_str_list_to_array': cp_str_list_to_array},
            tsc__ysuxt)
        kkymn__ykz = tsc__ysuxt['f']
        return kkymn__ykz
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            oevz__pmyf = len(str_list)
            str_arr = pre_alloc_string_array(oevz__pmyf, -1)
            for i in range(oevz__pmyf):
                wfhhh__zxgh = str_list[i]
                str_arr[i] = wfhhh__zxgh
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            oevz__pmyf = len(A)
            meepf__sottx = 0
            for i in range(oevz__pmyf):
                wfhhh__zxgh = A[i]
                meepf__sottx += get_utf8_size(wfhhh__zxgh)
            return meepf__sottx
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        oevz__pmyf = len(arr)
        n_chars = num_total_chars(arr)
        zoh__ionh = pre_alloc_string_array(oevz__pmyf, np.int64(n_chars))
        copy_str_arr_slice(zoh__ionh, arr, oevz__pmyf)
        return zoh__ionh
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('pd_pyarrow_array_from_string_array', hstr_ext.
    pd_pyarrow_array_from_string_array)
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
ll.add_symbol('str_to_dict_str_array', hstr_ext.str_to_dict_str_array)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    rzt__uyg = 'def f(in_seq):\n'
    rzt__uyg += '    n_strs = len(in_seq)\n'
    rzt__uyg += '    A = pre_alloc_string_array(n_strs, -1)\n'
    rzt__uyg += '    return A\n'
    tsc__ysuxt = {}
    exec(rzt__uyg, {'pre_alloc_string_array': pre_alloc_string_array},
        tsc__ysuxt)
    jhyyy__vbr = tsc__ysuxt['f']
    return jhyyy__vbr


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        rhje__fngs = 'pre_alloc_binary_array'
    else:
        rhje__fngs = 'pre_alloc_string_array'
    rzt__uyg = 'def f(in_seq):\n'
    rzt__uyg += '    n_strs = len(in_seq)\n'
    rzt__uyg += f'    A = {rhje__fngs}(n_strs, -1)\n'
    rzt__uyg += '    for i in range(n_strs):\n'
    rzt__uyg += '        A[i] = in_seq[i]\n'
    rzt__uyg += '    return A\n'
    tsc__ysuxt = {}
    exec(rzt__uyg, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, tsc__ysuxt)
    jhyyy__vbr = tsc__ysuxt['f']
    return jhyyy__vbr


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        rcquc__ndhb = builder.add(qmf__kbqlu.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        snily__sijiw = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        ihbtu__fdngv = builder.mul(rcquc__ndhb, snily__sijiw)
        oqxa__svbgc = context.make_array(offset_arr_type)(context, builder,
            qmf__kbqlu.offsets).data
        cgutils.memset(builder, oqxa__svbgc, ihbtu__fdngv, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        jid__gcqee = qmf__kbqlu.n_arrays
        ihbtu__fdngv = builder.lshr(builder.add(jid__gcqee, lir.Constant(
            lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        tovpm__zmyr = context.make_array(null_bitmap_arr_type)(context,
            builder, qmf__kbqlu.null_bitmap).data
        cgutils.memset(builder, tovpm__zmyr, ihbtu__fdngv, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    xel__pavv = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        ktii__meb = len(len_arr)
        for i in range(ktii__meb):
            offsets[i] = xel__pavv
            xel__pavv += len_arr[i]
        offsets[ktii__meb] = xel__pavv
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    mvd__rpy = i // 8
    ysop__nso = getitem_str_bitmap(bits, mvd__rpy)
    ysop__nso ^= np.uint8(-np.uint8(bit_is_set) ^ ysop__nso) & kBitmask[i % 8]
    setitem_str_bitmap(bits, mvd__rpy, ysop__nso)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    wkae__vftdh = get_null_bitmap_ptr(out_str_arr)
    yrq__unus = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        vxhq__xvc = get_bit_bitmap(yrq__unus, j)
        set_bit_to(wkae__vftdh, out_start + j, vxhq__xvc)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, hyx__ilkny, ooshg__cdg, bba__nnyey = args
        mzjzp__aslll = _get_str_binary_arr_payload(context, builder,
            hyx__ilkny, string_array_type)
        ugrg__rgfn = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        gvgi__exap = context.make_helper(builder, offset_arr_type,
            mzjzp__aslll.offsets).data
        qytl__dbc = context.make_helper(builder, offset_arr_type,
            ugrg__rgfn.offsets).data
        qmz__kxgkg = context.make_helper(builder, char_arr_type,
            mzjzp__aslll.data).data
        dtvqy__ubnq = context.make_helper(builder, char_arr_type,
            ugrg__rgfn.data).data
        num_total_chars = _get_num_total_chars(builder, gvgi__exap,
            mzjzp__aslll.n_arrays)
        edsqz__cuzc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        igcfh__wnvue = cgutils.get_or_insert_function(builder.module,
            edsqz__cuzc, name='set_string_array_range')
        builder.call(igcfh__wnvue, [qytl__dbc, dtvqy__ubnq, gvgi__exap,
            qmz__kxgkg, ooshg__cdg, bba__nnyey, mzjzp__aslll.n_arrays,
            num_total_chars])
        xirf__sxm = context.typing_context.resolve_value_type(copy_nulls_range)
        fsdh__blfo = xirf__sxm.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        tgjh__phjv = context.get_function(xirf__sxm, fsdh__blfo)
        tgjh__phjv(builder, (out_arr, hyx__ilkny, ooshg__cdg))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    eyi__kmxa = c.context.make_helper(c.builder, typ, val)
    kiwax__kln = ArrayItemArrayType(char_arr_type)
    qmf__kbqlu = _get_array_item_arr_payload(c.context, c.builder,
        kiwax__kln, eyi__kmxa.data)
    bnj__zpqnk = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    hzeub__rdqgn = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        hzeub__rdqgn = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        kcfxp__sokl = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        edsqz__cuzc = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        hzeub__rdqgn = 'pd_pyarrow_array_from_string_array'
        xokc__mea = cgutils.get_or_insert_function(c.builder.module,
            edsqz__cuzc, name=hzeub__rdqgn)
        arr = c.builder.call(xokc__mea, [kcfxp__sokl])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    edsqz__cuzc = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    xokc__mea = cgutils.get_or_insert_function(c.builder.module,
        edsqz__cuzc, name=hzeub__rdqgn)
    dfb__etti = c.context.make_array(offset_arr_type)(c.context, c.builder,
        qmf__kbqlu.offsets).data
    lhgy__agx = c.context.make_array(char_arr_type)(c.context, c.builder,
        qmf__kbqlu.data).data
    tovpm__zmyr = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, qmf__kbqlu.null_bitmap).data
    arr = c.builder.call(xokc__mea, [qmf__kbqlu.n_arrays, dfb__etti,
        lhgy__agx, tovpm__zmyr, bnj__zpqnk])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        tovpm__zmyr = context.make_array(null_bitmap_arr_type)(context,
            builder, qmf__kbqlu.null_bitmap).data
        zskg__wqg = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        txr__max = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        ysop__nso = builder.load(builder.gep(tovpm__zmyr, [zskg__wqg],
            inbounds=True))
        gjhxy__oewq = lir.ArrayType(lir.IntType(8), 8)
        guzlz__flab = cgutils.alloca_once_value(builder, lir.Constant(
            gjhxy__oewq, (1, 2, 4, 8, 16, 32, 64, 128)))
        apbq__ekybp = builder.load(builder.gep(guzlz__flab, [lir.Constant(
            lir.IntType(64), 0), txr__max], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(ysop__nso,
            apbq__ekybp), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        zskg__wqg = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        txr__max = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        tovpm__zmyr = context.make_array(null_bitmap_arr_type)(context,
            builder, qmf__kbqlu.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, qmf__kbqlu.
            offsets).data
        yxzi__rvau = builder.gep(tovpm__zmyr, [zskg__wqg], inbounds=True)
        ysop__nso = builder.load(yxzi__rvau)
        gjhxy__oewq = lir.ArrayType(lir.IntType(8), 8)
        guzlz__flab = cgutils.alloca_once_value(builder, lir.Constant(
            gjhxy__oewq, (1, 2, 4, 8, 16, 32, 64, 128)))
        apbq__ekybp = builder.load(builder.gep(guzlz__flab, [lir.Constant(
            lir.IntType(64), 0), txr__max], inbounds=True))
        apbq__ekybp = builder.xor(apbq__ekybp, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(ysop__nso, apbq__ekybp), yxzi__rvau)
        rpl__sbcg = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        bxt__emrp = builder.icmp_unsigned('!=', rpl__sbcg, qmf__kbqlu.n_arrays)
        with builder.if_then(bxt__emrp):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [rpl__sbcg]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        zskg__wqg = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        txr__max = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        tovpm__zmyr = context.make_array(null_bitmap_arr_type)(context,
            builder, qmf__kbqlu.null_bitmap).data
        yxzi__rvau = builder.gep(tovpm__zmyr, [zskg__wqg], inbounds=True)
        ysop__nso = builder.load(yxzi__rvau)
        gjhxy__oewq = lir.ArrayType(lir.IntType(8), 8)
        guzlz__flab = cgutils.alloca_once_value(builder, lir.Constant(
            gjhxy__oewq, (1, 2, 4, 8, 16, 32, 64, 128)))
        apbq__ekybp = builder.load(builder.gep(guzlz__flab, [lir.Constant(
            lir.IntType(64), 0), txr__max], inbounds=True))
        builder.store(builder.or_(ysop__nso, apbq__ekybp), yxzi__rvau)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ihbtu__fdngv = builder.udiv(builder.add(qmf__kbqlu.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        tovpm__zmyr = context.make_array(null_bitmap_arr_type)(context,
            builder, qmf__kbqlu.null_bitmap).data
        cgutils.memset(builder, tovpm__zmyr, ihbtu__fdngv, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    rkdz__ctqlv = context.make_helper(builder, string_array_type, str_arr)
    kiwax__kln = ArrayItemArrayType(char_arr_type)
    ylsy__jfatc = context.make_helper(builder, kiwax__kln, rkdz__ctqlv.data)
    fxkm__niq = ArrayItemArrayPayloadType(kiwax__kln)
    xsxg__rmgp = context.nrt.meminfo_data(builder, ylsy__jfatc.meminfo)
    qed__rqpbn = builder.bitcast(xsxg__rmgp, context.get_value_type(
        fxkm__niq).as_pointer())
    return qed__rqpbn


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        thhm__imozm, kdg__enk = args
        gelep__yzsft = _get_str_binary_arr_data_payload_ptr(context,
            builder, kdg__enk)
        eax__pmjwk = _get_str_binary_arr_data_payload_ptr(context, builder,
            thhm__imozm)
        hea__qza = _get_str_binary_arr_payload(context, builder, kdg__enk,
            sig.args[1])
        plm__jifv = _get_str_binary_arr_payload(context, builder,
            thhm__imozm, sig.args[0])
        context.nrt.incref(builder, char_arr_type, hea__qza.data)
        context.nrt.incref(builder, offset_arr_type, hea__qza.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, hea__qza.null_bitmap)
        context.nrt.decref(builder, char_arr_type, plm__jifv.data)
        context.nrt.decref(builder, offset_arr_type, plm__jifv.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, plm__jifv.null_bitmap
            )
        builder.store(builder.load(gelep__yzsft), eax__pmjwk)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        oevz__pmyf = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return oevz__pmyf
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, iads__iue, zckg__zzbhb = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, qmf__kbqlu.
            offsets).data
        data = context.make_helper(builder, char_arr_type, qmf__kbqlu.data
            ).data
        edsqz__cuzc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        cps__wnfvb = cgutils.get_or_insert_function(builder.module,
            edsqz__cuzc, name='setitem_string_array')
        nlo__wenpt = context.get_constant(types.int32, -1)
        lby__xcd = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, qmf__kbqlu
            .n_arrays)
        builder.call(cps__wnfvb, [offsets, data, num_total_chars, builder.
            extract_value(iads__iue, 0), zckg__zzbhb, nlo__wenpt, lby__xcd,
            ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    edsqz__cuzc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    mwsb__rpkjv = cgutils.get_or_insert_function(builder.module,
        edsqz__cuzc, name='is_na')
    return builder.call(mwsb__rpkjv, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        exqe__neg, hhnn__xen, bcj__zcyq, evnp__pxon = args
        cgutils.raw_memcpy(builder, exqe__neg, hhnn__xen, bcj__zcyq, evnp__pxon
            )
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        yaoab__ggg, ljb__eeip = unicode_to_utf8_and_len(val)
        ckbzb__ilgpm = getitem_str_offset(A, ind)
        uth__ivjl = getitem_str_offset(A, ind + 1)
        hgz__olf = uth__ivjl - ckbzb__ilgpm
        if hgz__olf != ljb__eeip:
            return False
        iads__iue = get_data_ptr_ind(A, ckbzb__ilgpm)
        return memcmp(iads__iue, yaoab__ggg, ljb__eeip) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        ckbzb__ilgpm = getitem_str_offset(A, ind)
        hgz__olf = bodo.libs.str_ext.int_to_str_len(val)
        lblet__ibij = ckbzb__ilgpm + hgz__olf
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ckbzb__ilgpm, lblet__ibij)
        iads__iue = get_data_ptr_ind(A, ckbzb__ilgpm)
        inplace_int64_to_str(iads__iue, hgz__olf, val)
        setitem_str_offset(A, ind + 1, ckbzb__ilgpm + hgz__olf)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        iads__iue, = args
        ejwh__gfsu = context.insert_const_string(builder.module, '<NA>')
        ixyks__efc = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, iads__iue, ejwh__gfsu, ixyks__efc, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    huvgp__jmogq = len('<NA>')

    def impl(A, ind):
        ckbzb__ilgpm = getitem_str_offset(A, ind)
        lblet__ibij = ckbzb__ilgpm + huvgp__jmogq
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ckbzb__ilgpm, lblet__ibij)
        iads__iue = get_data_ptr_ind(A, ckbzb__ilgpm)
        inplace_set_NA_str(iads__iue)
        setitem_str_offset(A, ind + 1, ckbzb__ilgpm + huvgp__jmogq)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            ckbzb__ilgpm = getitem_str_offset(A, ind)
            uth__ivjl = getitem_str_offset(A, ind + 1)
            zckg__zzbhb = uth__ivjl - ckbzb__ilgpm
            iads__iue = get_data_ptr_ind(A, ckbzb__ilgpm)
            xwu__raqeg = decode_utf8(iads__iue, zckg__zzbhb)
            return xwu__raqeg
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            oevz__pmyf = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(oevz__pmyf):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            tble__vcs = get_data_ptr(out_arr).data
            pysrh__mcbyu = get_data_ptr(A).data
            wwh__znoc = 0
            fqt__drb = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(oevz__pmyf):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    hhsc__fwirj = get_str_arr_item_length(A, i)
                    if hhsc__fwirj == 0:
                        pass
                    elif hhsc__fwirj == 1:
                        copy_single_char(tble__vcs, fqt__drb, pysrh__mcbyu,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(tble__vcs, fqt__drb, pysrh__mcbyu,
                            getitem_str_offset(A, i), hhsc__fwirj, 1)
                    fqt__drb += hhsc__fwirj
                    setitem_str_offset(out_arr, wwh__znoc + 1, fqt__drb)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, wwh__znoc)
                    else:
                        str_arr_set_not_na(out_arr, wwh__znoc)
                    wwh__znoc += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            oevz__pmyf = len(ind)
            n_chars = 0
            for i in range(oevz__pmyf):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(oevz__pmyf, n_chars)
            tble__vcs = get_data_ptr(out_arr).data
            pysrh__mcbyu = get_data_ptr(A).data
            fqt__drb = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(oevz__pmyf):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                opqy__cyamp = ind[i]
                hhsc__fwirj = get_str_arr_item_length(A, opqy__cyamp)
                if hhsc__fwirj == 0:
                    pass
                elif hhsc__fwirj == 1:
                    copy_single_char(tble__vcs, fqt__drb, pysrh__mcbyu,
                        getitem_str_offset(A, opqy__cyamp))
                else:
                    memcpy_region(tble__vcs, fqt__drb, pysrh__mcbyu,
                        getitem_str_offset(A, opqy__cyamp), hhsc__fwirj, 1)
                fqt__drb += hhsc__fwirj
                setitem_str_offset(out_arr, i + 1, fqt__drb)
                if str_arr_is_na(A, opqy__cyamp):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            oevz__pmyf = len(A)
            jmwpx__umjik = numba.cpython.unicode._normalize_slice(ind,
                oevz__pmyf)
            eva__hxlov = numba.cpython.unicode._slice_span(jmwpx__umjik)
            if jmwpx__umjik.step == 1:
                ckbzb__ilgpm = getitem_str_offset(A, jmwpx__umjik.start)
                uth__ivjl = getitem_str_offset(A, jmwpx__umjik.stop)
                n_chars = uth__ivjl - ckbzb__ilgpm
                zoh__ionh = pre_alloc_string_array(eva__hxlov, np.int64(
                    n_chars))
                for i in range(eva__hxlov):
                    zoh__ionh[i] = A[jmwpx__umjik.start + i]
                    if str_arr_is_na(A, jmwpx__umjik.start + i):
                        str_arr_set_na(zoh__ionh, i)
                return zoh__ionh
            else:
                zoh__ionh = pre_alloc_string_array(eva__hxlov, -1)
                for i in range(eva__hxlov):
                    zoh__ionh[i] = A[jmwpx__umjik.start + i * jmwpx__umjik.step
                        ]
                    if str_arr_is_na(A, jmwpx__umjik.start + i *
                        jmwpx__umjik.step):
                        str_arr_set_na(zoh__ionh, i)
                return zoh__ionh
        return str_arr_slice_impl
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    fla__pnby = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(fla__pnby)
        oicq__yedwz = 4

        def impl_scalar(A, idx, val):
            ggax__vbrb = (val._length if val._is_ascii else oicq__yedwz *
                val._length)
            zmfec__viar = A._data
            ckbzb__ilgpm = np.int64(getitem_str_offset(A, idx))
            lblet__ibij = ckbzb__ilgpm + ggax__vbrb
            bodo.libs.array_item_arr_ext.ensure_data_capacity(zmfec__viar,
                ckbzb__ilgpm, lblet__ibij)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                lblet__ibij, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                jmwpx__umjik = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                hubdz__xzzec = jmwpx__umjik.start
                zmfec__viar = A._data
                ckbzb__ilgpm = np.int64(getitem_str_offset(A, hubdz__xzzec))
                lblet__ibij = ckbzb__ilgpm + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(zmfec__viar,
                    ckbzb__ilgpm, lblet__ibij)
                set_string_array_range(A, val, hubdz__xzzec, ckbzb__ilgpm)
                tlew__crh = 0
                for i in range(jmwpx__umjik.start, jmwpx__umjik.stop,
                    jmwpx__umjik.step):
                    if str_arr_is_na(val, tlew__crh):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    tlew__crh += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                vawvs__nxcx = str_list_to_array(val)
                A[idx] = vawvs__nxcx
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                jmwpx__umjik = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(jmwpx__umjik.start, jmwpx__umjik.stop,
                    jmwpx__umjik.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(fla__pnby)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                oevz__pmyf = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(oevz__pmyf, -1)
                for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                oevz__pmyf = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(oevz__pmyf, -1)
                xjhti__vmeu = 0
                for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, xjhti__vmeu):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, xjhti__vmeu)
                        else:
                            out_arr[i] = str(val[xjhti__vmeu])
                        xjhti__vmeu += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(fla__pnby)
    raise BodoError(fla__pnby)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    tdplr__zdcx = parse_dtype(dtype, 'StringArray.astype')
    if A == tdplr__zdcx:
        return lambda A, dtype, copy=True: A
    if not isinstance(tdplr__zdcx, (types.Float, types.Integer)
        ) and tdplr__zdcx not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(tdplr__zdcx, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            oevz__pmyf = len(A)
            B = np.empty(oevz__pmyf, tdplr__zdcx)
            for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif tdplr__zdcx == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            oevz__pmyf = len(A)
            B = np.empty(oevz__pmyf, tdplr__zdcx)
            for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif tdplr__zdcx == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            oevz__pmyf = len(A)
            B = np.empty(oevz__pmyf, tdplr__zdcx)
            for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif tdplr__zdcx == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            oevz__pmyf = len(A)
            B = np.empty(oevz__pmyf, tdplr__zdcx)
            for i in numba.parfors.parfor.internal_prange(oevz__pmyf):
                B[i] = int(A[i])
            return B
        return impl_int


@numba.jit
def str_arr_to_dict_str_arr(A):
    return str_arr_to_dict_str_arr_cpp(A)


@intrinsic
def str_arr_to_dict_str_arr_cpp(typingctx, str_arr_t):

    def codegen(context, builder, sig, args):
        str_arr, = args
        ypiuh__szbd = bodo.libs.array.array_to_info_codegen(context,
            builder, bodo.libs.array.array_info_type(sig.args[0]), (str_arr
            ,), False)
        edsqz__cuzc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        wmi__knwko = cgutils.get_or_insert_function(builder.module,
            edsqz__cuzc, name='str_to_dict_str_array')
        bzta__juj = builder.call(wmi__knwko, [ypiuh__szbd])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        trfkc__naj = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (bzta__juj, context.get_constant_null(sig.
            return_type)))
        return trfkc__naj
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        iads__iue, zckg__zzbhb = args
        qjxtx__igcl = context.get_python_api(builder)
        gpkch__whxf = qjxtx__igcl.string_from_string_and_size(iads__iue,
            zckg__zzbhb)
        xuv__ewi = qjxtx__igcl.to_native_value(string_type, gpkch__whxf).value
        awp__zynt = cgutils.create_struct_proxy(string_type)(context,
            builder, xuv__ewi)
        awp__zynt.hash = awp__zynt.hash.type(-1)
        qjxtx__igcl.decref(gpkch__whxf)
        return awp__zynt._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        yrmn__ixjfs, arr, ind, wnt__rdp = args
        qmf__kbqlu = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, qmf__kbqlu.
            offsets).data
        data = context.make_helper(builder, char_arr_type, qmf__kbqlu.data
            ).data
        edsqz__cuzc = lir.FunctionType(lir.IntType(32), [yrmn__ixjfs.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        nnb__rgy = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            nnb__rgy = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        ihl__oxh = cgutils.get_or_insert_function(builder.module,
            edsqz__cuzc, nnb__rgy)
        return builder.call(ihl__oxh, [yrmn__ixjfs, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    bnj__zpqnk = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    edsqz__cuzc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    zfed__ybpup = cgutils.get_or_insert_function(c.builder.module,
        edsqz__cuzc, name='string_array_from_sequence')
    hlv__jiwet = c.builder.call(zfed__ybpup, [val, bnj__zpqnk])
    kiwax__kln = ArrayItemArrayType(char_arr_type)
    ylsy__jfatc = c.context.make_helper(c.builder, kiwax__kln)
    ylsy__jfatc.meminfo = hlv__jiwet
    rkdz__ctqlv = c.context.make_helper(c.builder, typ)
    zmfec__viar = ylsy__jfatc._getvalue()
    rkdz__ctqlv.data = zmfec__viar
    faptb__mtr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rkdz__ctqlv._getvalue(), is_error=faptb__mtr)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    oevz__pmyf = len(pyval)
    fqt__drb = 0
    ejhdu__fmja = np.empty(oevz__pmyf + 1, np_offset_type)
    pnptr__whfp = []
    rulm__nqks = np.empty(oevz__pmyf + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        ejhdu__fmja[i] = fqt__drb
        ddv__wdq = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(rulm__nqks, i, int(not ddv__wdq))
        if ddv__wdq:
            continue
        gbw__vedsh = list(s.encode()) if isinstance(s, str) else list(s)
        pnptr__whfp.extend(gbw__vedsh)
        fqt__drb += len(gbw__vedsh)
    ejhdu__fmja[oevz__pmyf] = fqt__drb
    idy__bfsj = np.array(pnptr__whfp, np.uint8)
    nly__xokk = context.get_constant(types.int64, oevz__pmyf)
    jkrsm__nubz = context.get_constant_generic(builder, char_arr_type,
        idy__bfsj)
    shvv__qwou = context.get_constant_generic(builder, offset_arr_type,
        ejhdu__fmja)
    tnjf__tubt = context.get_constant_generic(builder, null_bitmap_arr_type,
        rulm__nqks)
    qmf__kbqlu = lir.Constant.literal_struct([nly__xokk, jkrsm__nubz,
        shvv__qwou, tnjf__tubt])
    qmf__kbqlu = cgutils.global_constant(builder, '.const.payload', qmf__kbqlu
        ).bitcast(cgutils.voidptr_t)
    odx__oqcx = context.get_constant(types.int64, -1)
    pejd__avvxm = context.get_constant_null(types.voidptr)
    bynog__majkl = lir.Constant.literal_struct([odx__oqcx, pejd__avvxm,
        pejd__avvxm, qmf__kbqlu, odx__oqcx])
    bynog__majkl = cgutils.global_constant(builder, '.const.meminfo',
        bynog__majkl).bitcast(cgutils.voidptr_t)
    zmfec__viar = lir.Constant.literal_struct([bynog__majkl])
    rkdz__ctqlv = lir.Constant.literal_struct([zmfec__viar])
    return rkdz__ctqlv


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
