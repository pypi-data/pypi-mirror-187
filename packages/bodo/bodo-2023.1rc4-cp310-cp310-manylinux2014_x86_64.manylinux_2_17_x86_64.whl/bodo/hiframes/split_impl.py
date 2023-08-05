import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mob__tfpw = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, mob__tfpw)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    lshe__acnfy = context.get_value_type(str_arr_split_view_payload_type)
    roax__wfn = context.get_abi_sizeof(lshe__acnfy)
    yeoyx__otjpp = context.get_value_type(types.voidptr)
    zgk__homzl = context.get_value_type(types.uintp)
    ulcak__lxrkd = lir.FunctionType(lir.VoidType(), [yeoyx__otjpp,
        zgk__homzl, yeoyx__otjpp])
    vqn__wucy = cgutils.get_or_insert_function(builder.module, ulcak__lxrkd,
        name='dtor_str_arr_split_view')
    zkbp__dygj = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, roax__wfn), vqn__wucy)
    vdg__plb = context.nrt.meminfo_data(builder, zkbp__dygj)
    zhzr__lxvu = builder.bitcast(vdg__plb, lshe__acnfy.as_pointer())
    return zkbp__dygj, zhzr__lxvu


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        idjuv__dur, bsg__xonj = args
        zkbp__dygj, zhzr__lxvu = construct_str_arr_split_view(context, builder)
        xftz__mxduw = _get_str_binary_arr_payload(context, builder,
            idjuv__dur, string_array_type)
        kgbij__jcpod = lir.FunctionType(lir.VoidType(), [zhzr__lxvu.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        vtg__twf = cgutils.get_or_insert_function(builder.module,
            kgbij__jcpod, name='str_arr_split_view_impl')
        dusdp__ggm = context.make_helper(builder, offset_arr_type,
            xftz__mxduw.offsets).data
        yqet__qzun = context.make_helper(builder, char_arr_type,
            xftz__mxduw.data).data
        ktg__fbhu = context.make_helper(builder, null_bitmap_arr_type,
            xftz__mxduw.null_bitmap).data
        con__gdeaz = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(vtg__twf, [zhzr__lxvu, xftz__mxduw.n_arrays,
            dusdp__ggm, yqet__qzun, ktg__fbhu, con__gdeaz])
        itd__auabw = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zhzr__lxvu))
        orcfe__fyo = context.make_helper(builder, string_array_split_view_type)
        orcfe__fyo.num_items = xftz__mxduw.n_arrays
        orcfe__fyo.index_offsets = itd__auabw.index_offsets
        orcfe__fyo.data_offsets = itd__auabw.data_offsets
        orcfe__fyo.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [idjuv__dur])
        orcfe__fyo.null_bitmap = itd__auabw.null_bitmap
        orcfe__fyo.meminfo = zkbp__dygj
        tbhj__ckksj = orcfe__fyo._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, tbhj__ckksj)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    ygv__zijrm = context.make_helper(builder, string_array_split_view_type, val
        )
    cbgj__ubb = context.insert_const_string(builder.module, 'numpy')
    zvbee__xmar = c.pyapi.import_module_noblock(cbgj__ubb)
    dtype = c.pyapi.object_getattr_string(zvbee__xmar, 'object_')
    jnvax__eqefe = builder.sext(ygv__zijrm.num_items, c.pyapi.longlong)
    uaw__lotqp = c.pyapi.long_from_longlong(jnvax__eqefe)
    voklk__fmwl = c.pyapi.call_method(zvbee__xmar, 'ndarray', (uaw__lotqp,
        dtype))
    cywkf__huxh = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    uvj__kaac = c.pyapi._get_function(cywkf__huxh, name='array_getptr1')
    rvxn__sea = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    aahc__fvoea = c.pyapi._get_function(rvxn__sea, name='array_setitem')
    gfip__pten = c.pyapi.object_getattr_string(zvbee__xmar, 'nan')
    with cgutils.for_range(builder, ygv__zijrm.num_items) as pup__uzhdz:
        str_ind = pup__uzhdz.index
        zexug__zhvh = builder.sext(builder.load(builder.gep(ygv__zijrm.
            index_offsets, [str_ind])), lir.IntType(64))
        dzvu__zoj = builder.sext(builder.load(builder.gep(ygv__zijrm.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        ktam__igs = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        xclfd__ycg = builder.gep(ygv__zijrm.null_bitmap, [ktam__igs])
        obedg__uppo = builder.load(xclfd__ycg)
        ztd__tlvl = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(obedg__uppo, ztd__tlvl), lir.
            Constant(lir.IntType(8), 1))
        mnhzq__guwaq = builder.sub(dzvu__zoj, zexug__zhvh)
        mnhzq__guwaq = builder.sub(mnhzq__guwaq, mnhzq__guwaq.type(1))
        zli__ssgmm = builder.call(uvj__kaac, [voklk__fmwl, str_ind])
        xuov__dcpy = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(xuov__dcpy) as (kmz__qooit, lidpc__icoz):
            with kmz__qooit:
                cuhab__bzdm = c.pyapi.list_new(mnhzq__guwaq)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    cuhab__bzdm), likely=True):
                    with cgutils.for_range(c.builder, mnhzq__guwaq
                        ) as pup__uzhdz:
                        wktwn__epg = builder.add(zexug__zhvh, pup__uzhdz.index)
                        data_start = builder.load(builder.gep(ygv__zijrm.
                            data_offsets, [wktwn__epg]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        wzx__ghsp = builder.load(builder.gep(ygv__zijrm.
                            data_offsets, [builder.add(wktwn__epg,
                            wktwn__epg.type(1))]))
                        tyt__gima = builder.gep(builder.extract_value(
                            ygv__zijrm.data, 0), [data_start])
                        mff__etp = builder.sext(builder.sub(wzx__ghsp,
                            data_start), lir.IntType(64))
                        huq__ykwam = c.pyapi.string_from_string_and_size(
                            tyt__gima, mff__etp)
                        c.pyapi.list_setitem(cuhab__bzdm, pup__uzhdz.index,
                            huq__ykwam)
                builder.call(aahc__fvoea, [voklk__fmwl, zli__ssgmm,
                    cuhab__bzdm])
            with lidpc__icoz:
                builder.call(aahc__fvoea, [voklk__fmwl, zli__ssgmm, gfip__pten]
                    )
    c.pyapi.decref(zvbee__xmar)
    c.pyapi.decref(dtype)
    c.pyapi.decref(gfip__pten)
    return voklk__fmwl


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        guny__eurmq, zse__ctf, tyt__gima = args
        zkbp__dygj, zhzr__lxvu = construct_str_arr_split_view(context, builder)
        kgbij__jcpod = lir.FunctionType(lir.VoidType(), [zhzr__lxvu.type,
            lir.IntType(64), lir.IntType(64)])
        vtg__twf = cgutils.get_or_insert_function(builder.module,
            kgbij__jcpod, name='str_arr_split_view_alloc')
        builder.call(vtg__twf, [zhzr__lxvu, guny__eurmq, zse__ctf])
        itd__auabw = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(zhzr__lxvu))
        orcfe__fyo = context.make_helper(builder, string_array_split_view_type)
        orcfe__fyo.num_items = guny__eurmq
        orcfe__fyo.index_offsets = itd__auabw.index_offsets
        orcfe__fyo.data_offsets = itd__auabw.data_offsets
        orcfe__fyo.data = tyt__gima
        orcfe__fyo.null_bitmap = itd__auabw.null_bitmap
        context.nrt.incref(builder, data_t, tyt__gima)
        orcfe__fyo.meminfo = zkbp__dygj
        tbhj__ckksj = orcfe__fyo._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, tbhj__ckksj)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        kaxnl__iygp, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            kaxnl__iygp = builder.extract_value(kaxnl__iygp, 0)
        return builder.bitcast(builder.gep(kaxnl__iygp, [ind]), lir.IntType
            (8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        kaxnl__iygp, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            kaxnl__iygp = builder.extract_value(kaxnl__iygp, 0)
        return builder.load(builder.gep(kaxnl__iygp, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        kaxnl__iygp, ind, kkmr__zyv = args
        encx__plmja = builder.gep(kaxnl__iygp, [ind])
        builder.store(kkmr__zyv, encx__plmja)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        jovem__ciuam, ind = args
        eram__xuy = context.make_helper(builder, arr_ctypes_t, jovem__ciuam)
        lvkhs__sfmg = context.make_helper(builder, arr_ctypes_t)
        lvkhs__sfmg.data = builder.gep(eram__xuy.data, [ind])
        lvkhs__sfmg.meminfo = eram__xuy.meminfo
        itg__pybqq = lvkhs__sfmg._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, itg__pybqq)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    nnzt__bpncg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not nnzt__bpncg:
        return 0, 0, 0
    wktwn__epg = getitem_c_arr(arr._index_offsets, item_ind)
    pvtr__kvnjb = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    ynma__yxg = pvtr__kvnjb - wktwn__epg
    if str_ind >= ynma__yxg:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, wktwn__epg + str_ind)
    data_start += 1
    if wktwn__epg + str_ind == 0:
        data_start = 0
    wzx__ghsp = getitem_c_arr(arr._data_offsets, wktwn__epg + str_ind + 1)
    tcixk__ism = wzx__ghsp - data_start
    return 1, data_start, tcixk__ism


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        kab__eewz = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            wktwn__epg = getitem_c_arr(A._index_offsets, ind)
            pvtr__kvnjb = getitem_c_arr(A._index_offsets, ind + 1)
            xgeo__ettvl = pvtr__kvnjb - wktwn__epg - 1
            idjuv__dur = bodo.libs.str_arr_ext.pre_alloc_string_array(
                xgeo__ettvl, -1)
            for yiidu__ntiax in range(xgeo__ettvl):
                data_start = getitem_c_arr(A._data_offsets, wktwn__epg +
                    yiidu__ntiax)
                data_start += 1
                if wktwn__epg + yiidu__ntiax == 0:
                    data_start = 0
                wzx__ghsp = getitem_c_arr(A._data_offsets, wktwn__epg +
                    yiidu__ntiax + 1)
                tcixk__ism = wzx__ghsp - data_start
                encx__plmja = get_array_ctypes_ptr(A._data, data_start)
                dddzv__dtvb = bodo.libs.str_arr_ext.decode_utf8(encx__plmja,
                    tcixk__ism)
                idjuv__dur[yiidu__ntiax] = dddzv__dtvb
            return idjuv__dur
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        qkd__wbwq = offset_type.bitwidth // 8

        def _impl(A, ind):
            xgeo__ettvl = len(A)
            if xgeo__ettvl != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            guny__eurmq = 0
            zse__ctf = 0
            for yiidu__ntiax in range(xgeo__ettvl):
                if ind[yiidu__ntiax]:
                    guny__eurmq += 1
                    wktwn__epg = getitem_c_arr(A._index_offsets, yiidu__ntiax)
                    pvtr__kvnjb = getitem_c_arr(A._index_offsets, 
                        yiidu__ntiax + 1)
                    zse__ctf += pvtr__kvnjb - wktwn__epg
            voklk__fmwl = pre_alloc_str_arr_view(guny__eurmq, zse__ctf, A._data
                )
            item_ind = 0
            pvccw__lpzk = 0
            for yiidu__ntiax in range(xgeo__ettvl):
                if ind[yiidu__ntiax]:
                    wktwn__epg = getitem_c_arr(A._index_offsets, yiidu__ntiax)
                    pvtr__kvnjb = getitem_c_arr(A._index_offsets, 
                        yiidu__ntiax + 1)
                    vwa__gckpc = pvtr__kvnjb - wktwn__epg
                    setitem_c_arr(voklk__fmwl._index_offsets, item_ind,
                        pvccw__lpzk)
                    encx__plmja = get_c_arr_ptr(A._data_offsets, wktwn__epg)
                    xby__zwp = get_c_arr_ptr(voklk__fmwl._data_offsets,
                        pvccw__lpzk)
                    _memcpy(xby__zwp, encx__plmja, vwa__gckpc, qkd__wbwq)
                    nnzt__bpncg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, yiidu__ntiax)
                    bodo.libs.int_arr_ext.set_bit_to_arr(voklk__fmwl.
                        _null_bitmap, item_ind, nnzt__bpncg)
                    item_ind += 1
                    pvccw__lpzk += vwa__gckpc
            setitem_c_arr(voklk__fmwl._index_offsets, item_ind, pvccw__lpzk)
            return voklk__fmwl
        return _impl
