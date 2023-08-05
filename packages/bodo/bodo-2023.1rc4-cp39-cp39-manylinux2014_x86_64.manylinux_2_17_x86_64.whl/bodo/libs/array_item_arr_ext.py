"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pbrx__fpv = [('n_arrays', types.int64), ('data', fe_type.array_type
            .dtype), ('offsets', types.Array(offset_type, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, pbrx__fpv)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        pbrx__fpv = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, pbrx__fpv)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    poyf__lkemx = builder.module
    quv__jui = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    oouy__ixii = cgutils.get_or_insert_function(poyf__lkemx, quv__jui, name
        ='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not oouy__ixii.is_declaration:
        return oouy__ixii
    oouy__ixii.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(oouy__ixii.append_basic_block())
    ytbq__yuen = oouy__ixii.args[0]
    dhla__aqdq = context.get_value_type(payload_type).as_pointer()
    mntv__epa = builder.bitcast(ytbq__yuen, dhla__aqdq)
    ogi__kga = context.make_helper(builder, payload_type, ref=mntv__epa)
    context.nrt.decref(builder, array_item_type.dtype, ogi__kga.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), ogi__kga.
        offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), ogi__kga.
        null_bitmap)
    builder.ret_void()
    return oouy__ixii


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    pnyyr__fqk = context.get_value_type(payload_type)
    deuy__rtu = context.get_abi_sizeof(pnyyr__fqk)
    wljfa__pwkn = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    joi__zamt = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, deuy__rtu), wljfa__pwkn)
    chpv__dnx = context.nrt.meminfo_data(builder, joi__zamt)
    jpd__yijv = builder.bitcast(chpv__dnx, pnyyr__fqk.as_pointer())
    ogi__kga = cgutils.create_struct_proxy(payload_type)(context, builder)
    ogi__kga.n_arrays = n_arrays
    pht__vpde = n_elems.type.count
    zif__yum = builder.extract_value(n_elems, 0)
    nmstq__dabso = cgutils.alloca_once_value(builder, zif__yum)
    ybwb__luqye = builder.icmp_signed('==', zif__yum, lir.Constant(zif__yum
        .type, -1))
    with builder.if_then(ybwb__luqye):
        builder.store(n_arrays, nmstq__dabso)
    n_elems = cgutils.pack_array(builder, [builder.load(nmstq__dabso)] + [
        builder.extract_value(n_elems, zsoe__xiqg) for zsoe__xiqg in range(
        1, pht__vpde)])
    ogi__kga.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    jjci__jnmho = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    ccj__uwzp = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [jjci__jnmho])
    offsets_ptr = ccj__uwzp.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    ogi__kga.offsets = ccj__uwzp._getvalue()
    eegd__wmwr = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    uyzq__nxusp = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [eegd__wmwr])
    null_bitmap_ptr = uyzq__nxusp.data
    ogi__kga.null_bitmap = uyzq__nxusp._getvalue()
    builder.store(ogi__kga._getvalue(), jpd__yijv)
    return joi__zamt, ogi__kga.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    hcwg__dzbwb, xoil__hotg = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    anl__itxd = context.insert_const_string(builder.module, 'pandas')
    gidx__sqq = c.pyapi.import_module_noblock(anl__itxd)
    ubvyc__jyrw = c.pyapi.object_getattr_string(gidx__sqq, 'NA')
    zfitd__yvn = c.context.get_constant(offset_type, 0)
    builder.store(zfitd__yvn, offsets_ptr)
    sisfk__ramn = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as eqrt__chf:
        tkx__crtu = eqrt__chf.index
        item_ind = builder.load(sisfk__ramn)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [tkx__crtu]))
        arr_obj = seq_getitem(builder, context, val, tkx__crtu)
        set_bitmap_bit(builder, null_bitmap_ptr, tkx__crtu, 0)
        cqom__shq = is_na_value(builder, context, arr_obj, ubvyc__jyrw)
        ogiv__figok = builder.icmp_unsigned('!=', cqom__shq, lir.Constant(
            cqom__shq.type, 1))
        with builder.if_then(ogiv__figok):
            set_bitmap_bit(builder, null_bitmap_ptr, tkx__crtu, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), sisfk__ramn)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(sisfk__ramn), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(gidx__sqq)
    c.pyapi.decref(ubvyc__jyrw)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    zkeh__dgb = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if zkeh__dgb:
        quv__jui = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        rys__wklb = cgutils.get_or_insert_function(c.builder.module,
            quv__jui, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(rys__wklb,
            [val])])
    else:
        pkciu__obdv = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            pkciu__obdv, zsoe__xiqg) for zsoe__xiqg in range(1, pkciu__obdv
            .type.count)])
    joi__zamt, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if zkeh__dgb:
        oym__imf = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        jmtm__whweb = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        quv__jui = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        oouy__ixii = cgutils.get_or_insert_function(c.builder.module,
            quv__jui, name='array_item_array_from_sequence')
        c.builder.call(oouy__ixii, [val, c.builder.bitcast(jmtm__whweb, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), oym__imf)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    gatl__lak = c.context.make_helper(c.builder, typ)
    gatl__lak.meminfo = joi__zamt
    hov__ltwnz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gatl__lak._getvalue(), is_error=hov__ltwnz)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    gatl__lak = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    chpv__dnx = context.nrt.meminfo_data(builder, gatl__lak.meminfo)
    jpd__yijv = builder.bitcast(chpv__dnx, context.get_value_type(
        payload_type).as_pointer())
    ogi__kga = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(jpd__yijv))
    return ogi__kga


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    anl__itxd = context.insert_const_string(builder.module, 'numpy')
    lzi__xun = c.pyapi.import_module_noblock(anl__itxd)
    hpqw__fgwbz = c.pyapi.object_getattr_string(lzi__xun, 'object_')
    nixbi__ook = c.pyapi.long_from_longlong(n_arrays)
    dcdy__wirmu = c.pyapi.call_method(lzi__xun, 'ndarray', (nixbi__ook,
        hpqw__fgwbz))
    moc__zvaq = c.pyapi.object_getattr_string(lzi__xun, 'nan')
    sisfk__ramn = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as eqrt__chf:
        tkx__crtu = eqrt__chf.index
        pyarray_setitem(builder, context, dcdy__wirmu, tkx__crtu, moc__zvaq)
        aur__uvgji = get_bitmap_bit(builder, null_bitmap_ptr, tkx__crtu)
        mti__hrzfs = builder.icmp_unsigned('!=', aur__uvgji, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(mti__hrzfs):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(tkx__crtu, lir.Constant(tkx__crtu
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                tkx__crtu]))), lir.IntType(64))
            item_ind = builder.load(sisfk__ramn)
            hcwg__dzbwb, dcgk__bao = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), sisfk__ramn)
            arr_obj = c.pyapi.from_native_value(typ.dtype, dcgk__bao, c.
                env_manager)
            pyarray_setitem(builder, context, dcdy__wirmu, tkx__crtu, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(lzi__xun)
    c.pyapi.decref(hpqw__fgwbz)
    c.pyapi.decref(nixbi__ook)
    c.pyapi.decref(moc__zvaq)
    return dcdy__wirmu


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    ogi__kga = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = ogi__kga.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), ogi__kga.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), ogi__kga.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        oym__imf = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        jmtm__whweb = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        quv__jui = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        tde__mcsqr = cgutils.get_or_insert_function(c.builder.module,
            quv__jui, name='np_array_from_array_item_array')
        arr = c.builder.call(tde__mcsqr, [ogi__kga.n_arrays, c.builder.
            bitcast(jmtm__whweb, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), oym__imf)])
    else:
        arr = _box_array_item_array_generic(typ, c, ogi__kga.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    hfdv__uuel, atonf__mgyj, nvu__foa = args
    vsd__dnqo = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    szce__wmd = sig.args[1]
    if not isinstance(szce__wmd, types.UniTuple):
        atonf__mgyj = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for nvu__foa in range(vsd__dnqo)])
    elif szce__wmd.count < vsd__dnqo:
        atonf__mgyj = cgutils.pack_array(builder, [builder.extract_value(
            atonf__mgyj, zsoe__xiqg) for zsoe__xiqg in range(szce__wmd.
            count)] + [lir.Constant(lir.IntType(64), -1) for nvu__foa in
            range(vsd__dnqo - szce__wmd.count)])
    joi__zamt, nvu__foa, nvu__foa, nvu__foa = construct_array_item_array(
        context, builder, array_item_type, hfdv__uuel, atonf__mgyj)
    gatl__lak = context.make_helper(builder, array_item_type)
    gatl__lak.meminfo = joi__zamt
    return gatl__lak._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, woi__lfjtm, ccj__uwzp, uyzq__nxusp = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    pnyyr__fqk = context.get_value_type(payload_type)
    deuy__rtu = context.get_abi_sizeof(pnyyr__fqk)
    wljfa__pwkn = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    joi__zamt = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, deuy__rtu), wljfa__pwkn)
    chpv__dnx = context.nrt.meminfo_data(builder, joi__zamt)
    jpd__yijv = builder.bitcast(chpv__dnx, pnyyr__fqk.as_pointer())
    ogi__kga = cgutils.create_struct_proxy(payload_type)(context, builder)
    ogi__kga.n_arrays = n_arrays
    ogi__kga.data = woi__lfjtm
    ogi__kga.offsets = ccj__uwzp
    ogi__kga.null_bitmap = uyzq__nxusp
    builder.store(ogi__kga._getvalue(), jpd__yijv)
    context.nrt.incref(builder, signature.args[1], woi__lfjtm)
    context.nrt.incref(builder, signature.args[2], ccj__uwzp)
    context.nrt.incref(builder, signature.args[3], uyzq__nxusp)
    gatl__lak = context.make_helper(builder, array_item_type)
    gatl__lak.meminfo = joi__zamt
    return gatl__lak._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    ygjd__exp = ArrayItemArrayType(data_type)
    sig = ygjd__exp(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ogi__kga = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ogi__kga.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        ogi__kga = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        jmtm__whweb = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, ogi__kga.offsets).data
        ccj__uwzp = builder.bitcast(jmtm__whweb, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(ccj__uwzp, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ogi__kga = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ogi__kga.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ogi__kga = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            ogi__kga.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        ogi__kga = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return ogi__kga.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, bsac__cryy = args
        gatl__lak = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        chpv__dnx = context.nrt.meminfo_data(builder, gatl__lak.meminfo)
        jpd__yijv = builder.bitcast(chpv__dnx, context.get_value_type(
            payload_type).as_pointer())
        ogi__kga = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(jpd__yijv))
        context.nrt.decref(builder, data_typ, ogi__kga.data)
        ogi__kga.data = bsac__cryy
        context.nrt.incref(builder, data_typ, bsac__cryy)
        builder.store(ogi__kga._getvalue(), jpd__yijv)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    woi__lfjtm = get_data(arr)
    dlqqd__euv = len(woi__lfjtm)
    if dlqqd__euv < new_size:
        sjz__zhil = max(2 * dlqqd__euv, new_size)
        bsac__cryy = bodo.libs.array_kernels.resize_and_copy(woi__lfjtm,
            old_size, sjz__zhil)
        replace_data_arr(arr, bsac__cryy)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    woi__lfjtm = get_data(arr)
    ccj__uwzp = get_offsets(arr)
    icz__bhge = len(woi__lfjtm)
    aja__pqw = ccj__uwzp[-1]
    if icz__bhge != aja__pqw:
        bsac__cryy = bodo.libs.array_kernels.resize_and_copy(woi__lfjtm,
            aja__pqw, aja__pqw)
        replace_data_arr(arr, bsac__cryy)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ccj__uwzp = get_offsets(arr)
            woi__lfjtm = get_data(arr)
            kbky__ejd = ccj__uwzp[ind]
            finug__nvy = ccj__uwzp[ind + 1]
            return woi__lfjtm[kbky__ejd:finug__nvy]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        eyy__lnj = arr.dtype

        def impl_bool(arr, ind):
            qbut__uaih = len(arr)
            if qbut__uaih != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            uyzq__nxusp = get_null_bitmap(arr)
            n_arrays = 0
            zzy__gjw = init_nested_counts(eyy__lnj)
            for zsoe__xiqg in range(qbut__uaih):
                if ind[zsoe__xiqg]:
                    n_arrays += 1
                    vqdzt__nczqk = arr[zsoe__xiqg]
                    zzy__gjw = add_nested_counts(zzy__gjw, vqdzt__nczqk)
            dcdy__wirmu = pre_alloc_array_item_array(n_arrays, zzy__gjw,
                eyy__lnj)
            niiav__bsiyb = get_null_bitmap(dcdy__wirmu)
            zwoas__kmju = 0
            for jej__sawb in range(qbut__uaih):
                if ind[jej__sawb]:
                    dcdy__wirmu[zwoas__kmju] = arr[jej__sawb]
                    vef__gpmf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        uyzq__nxusp, jej__sawb)
                    bodo.libs.int_arr_ext.set_bit_to_arr(niiav__bsiyb,
                        zwoas__kmju, vef__gpmf)
                    zwoas__kmju += 1
            return dcdy__wirmu
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        eyy__lnj = arr.dtype

        def impl_int(arr, ind):
            uyzq__nxusp = get_null_bitmap(arr)
            qbut__uaih = len(ind)
            n_arrays = qbut__uaih
            zzy__gjw = init_nested_counts(eyy__lnj)
            for obp__vdbn in range(qbut__uaih):
                zsoe__xiqg = ind[obp__vdbn]
                vqdzt__nczqk = arr[zsoe__xiqg]
                zzy__gjw = add_nested_counts(zzy__gjw, vqdzt__nczqk)
            dcdy__wirmu = pre_alloc_array_item_array(n_arrays, zzy__gjw,
                eyy__lnj)
            niiav__bsiyb = get_null_bitmap(dcdy__wirmu)
            for vlqt__uijz in range(qbut__uaih):
                jej__sawb = ind[vlqt__uijz]
                dcdy__wirmu[vlqt__uijz] = arr[jej__sawb]
                vef__gpmf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    uyzq__nxusp, jej__sawb)
                bodo.libs.int_arr_ext.set_bit_to_arr(niiav__bsiyb,
                    vlqt__uijz, vef__gpmf)
            return dcdy__wirmu
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            qbut__uaih = len(arr)
            pobs__igtm = numba.cpython.unicode._normalize_slice(ind, qbut__uaih
                )
            vibcg__cgyff = np.arange(pobs__igtm.start, pobs__igtm.stop,
                pobs__igtm.step)
            return arr[vibcg__cgyff]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            ccj__uwzp = get_offsets(A)
            uyzq__nxusp = get_null_bitmap(A)
            if idx == 0:
                ccj__uwzp[0] = 0
            n_items = len(val)
            dyoga__bww = ccj__uwzp[idx] + n_items
            ensure_data_capacity(A, ccj__uwzp[idx], dyoga__bww)
            woi__lfjtm = get_data(A)
            ccj__uwzp[idx + 1] = ccj__uwzp[idx] + n_items
            woi__lfjtm[ccj__uwzp[idx]:ccj__uwzp[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(uyzq__nxusp, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            pobs__igtm = numba.cpython.unicode._normalize_slice(idx, len(A))
            for zsoe__xiqg in range(pobs__igtm.start, pobs__igtm.stop,
                pobs__igtm.step):
                A[zsoe__xiqg] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            ccj__uwzp = get_offsets(A)
            uyzq__nxusp = get_null_bitmap(A)
            vfyi__yuo = get_offsets(val)
            xwlo__plv = get_data(val)
            lxmsp__zpn = get_null_bitmap(val)
            qbut__uaih = len(A)
            pobs__igtm = numba.cpython.unicode._normalize_slice(idx, qbut__uaih
                )
            ucct__mkgbj, vcgeq__iiibe = pobs__igtm.start, pobs__igtm.stop
            assert pobs__igtm.step == 1
            if ucct__mkgbj == 0:
                ccj__uwzp[ucct__mkgbj] = 0
            vfpj__veuv = ccj__uwzp[ucct__mkgbj]
            dyoga__bww = vfpj__veuv + len(xwlo__plv)
            ensure_data_capacity(A, vfpj__veuv, dyoga__bww)
            woi__lfjtm = get_data(A)
            woi__lfjtm[vfpj__veuv:vfpj__veuv + len(xwlo__plv)] = xwlo__plv
            ccj__uwzp[ucct__mkgbj:vcgeq__iiibe + 1] = vfyi__yuo + vfpj__veuv
            mhvw__esg = 0
            for zsoe__xiqg in range(ucct__mkgbj, vcgeq__iiibe):
                vef__gpmf = bodo.libs.int_arr_ext.get_bit_bitmap_arr(lxmsp__zpn
                    , mhvw__esg)
                bodo.libs.int_arr_ext.set_bit_to_arr(uyzq__nxusp,
                    zsoe__xiqg, vef__gpmf)
                mhvw__esg += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
