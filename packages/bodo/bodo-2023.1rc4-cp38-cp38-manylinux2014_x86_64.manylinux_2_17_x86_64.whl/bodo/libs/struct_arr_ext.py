"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.time_ext import TimeType
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(jszyt__sdg, False) for jszyt__sdg in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(jszyt__sdg,
                str) for jszyt__sdg in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(jfw__sqycm.dtype for jfw__sqycm in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(jszyt__sdg) for jszyt__sdg in d.keys())
        data = tuple(dtype_to_array_type(jfw__sqycm) for jfw__sqycm in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(jszyt__sdg, False) for jszyt__sdg in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yuwd__qme = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, yuwd__qme)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        yuwd__qme = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yuwd__qme)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    vgkc__hkhl = builder.module
    jdx__ldt = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    pfrm__syfb = cgutils.get_or_insert_function(vgkc__hkhl, jdx__ldt, name=
        '.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not pfrm__syfb.is_declaration:
        return pfrm__syfb
    pfrm__syfb.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(pfrm__syfb.append_basic_block())
    kjgc__cduby = pfrm__syfb.args[0]
    oezw__jffo = context.get_value_type(payload_type).as_pointer()
    tbpl__igrcb = builder.bitcast(kjgc__cduby, oezw__jffo)
    xiu__ntfu = context.make_helper(builder, payload_type, ref=tbpl__igrcb)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), xiu__ntfu.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), xiu__ntfu
        .null_bitmap)
    builder.ret_void()
    return pfrm__syfb


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    zvtfn__hodc = context.get_value_type(payload_type)
    jjb__soui = context.get_abi_sizeof(zvtfn__hodc)
    ioxi__fvipt = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    zzkaf__xklfn = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jjb__soui), ioxi__fvipt)
    rrgn__bmbfa = context.nrt.meminfo_data(builder, zzkaf__xklfn)
    fgiot__pby = builder.bitcast(rrgn__bmbfa, zvtfn__hodc.as_pointer())
    xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    bjie__qzzm = 0
    for arr_typ in struct_arr_type.data:
        lyp__ztuc = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        mbazs__etqhc = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(bjie__qzzm, bjie__qzzm +
            lyp__ztuc)])
        arr = gen_allocate_array(context, builder, arr_typ, mbazs__etqhc, c)
        arrs.append(arr)
        bjie__qzzm += lyp__ztuc
    xiu__ntfu.data = cgutils.pack_array(builder, arrs) if types.is_homogeneous(
        *struct_arr_type.data) else cgutils.pack_struct(builder, arrs)
    vwf__scg = builder.udiv(builder.add(n_structs, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    hsivk__rojfk = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [vwf__scg])
    null_bitmap_ptr = hsivk__rojfk.data
    xiu__ntfu.null_bitmap = hsivk__rojfk._getvalue()
    builder.store(xiu__ntfu._getvalue(), fgiot__pby)
    return zzkaf__xklfn, xiu__ntfu.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    jdil__cfpjz = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        nggll__snns = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            nggll__snns)
        jdil__cfpjz.append(arr.data)
    lzsi__xdgho = cgutils.pack_array(c.builder, jdil__cfpjz
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, jdil__cfpjz)
    kyk__xygs = cgutils.alloca_once_value(c.builder, lzsi__xdgho)
    ybk__tpcm = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(jszyt__sdg.dtype)) for jszyt__sdg in data_typ]
    sux__wkc = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, ybk__tpcm))
    tyohv__loo = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, jszyt__sdg) for jszyt__sdg in
        names])
    djni__htk = cgutils.alloca_once_value(c.builder, tyohv__loo)
    return kyk__xygs, sux__wkc, djni__htk


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    cvnc__uymqd = all(isinstance(jfw__sqycm, types.Array) and (jfw__sqycm.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(jfw__sqycm.dtype, TimeType)) for
        jfw__sqycm in typ.data)
    if cvnc__uymqd:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        tdhs__gqmh = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            tdhs__gqmh, i) for i in range(1, tdhs__gqmh.type.count)], lir.
            IntType(64))
    zzkaf__xklfn, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if cvnc__uymqd:
        kyk__xygs, sux__wkc, djni__htk = _get_C_API_ptrs(c, data_tup, typ.
            data, typ.names)
        jdx__ldt = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        pfrm__syfb = cgutils.get_or_insert_function(c.builder.module,
            jdx__ldt, name='struct_array_from_sequence')
        c.builder.call(pfrm__syfb, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(kyk__xygs, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(sux__wkc, lir
            .IntType(8).as_pointer()), c.builder.bitcast(djni__htk, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    qtv__hks = c.context.make_helper(c.builder, typ)
    qtv__hks.meminfo = zzkaf__xklfn
    wwyqq__kji = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qtv__hks._getvalue(), is_error=wwyqq__kji)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    rea__pmq = context.insert_const_string(builder.module, 'pandas')
    rtf__tdsxb = c.pyapi.import_module_noblock(rea__pmq)
    vhw__dtntg = c.pyapi.object_getattr_string(rtf__tdsxb, 'NA')
    with cgutils.for_range(builder, n_structs) as afxdj__cagb:
        tprw__pxtg = afxdj__cagb.index
        vux__qin = seq_getitem(builder, context, val, tprw__pxtg)
        set_bitmap_bit(builder, null_bitmap_ptr, tprw__pxtg, 0)
        for xng__lrt in range(len(typ.data)):
            arr_typ = typ.data[xng__lrt]
            data_arr = builder.extract_value(data_tup, xng__lrt)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            hyio__amibu, ouex__qhh = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, tprw__pxtg])
        dlth__lnww = is_na_value(builder, context, vux__qin, vhw__dtntg)
        qxfwq__jsfkc = builder.icmp_unsigned('!=', dlth__lnww, lir.Constant
            (dlth__lnww.type, 1))
        with builder.if_then(qxfwq__jsfkc):
            set_bitmap_bit(builder, null_bitmap_ptr, tprw__pxtg, 1)
            for xng__lrt in range(len(typ.data)):
                arr_typ = typ.data[xng__lrt]
                if is_tuple_array:
                    zfovj__gcyb = c.pyapi.tuple_getitem(vux__qin, xng__lrt)
                else:
                    zfovj__gcyb = c.pyapi.dict_getitem_string(vux__qin, typ
                        .names[xng__lrt])
                dlth__lnww = is_na_value(builder, context, zfovj__gcyb,
                    vhw__dtntg)
                qxfwq__jsfkc = builder.icmp_unsigned('!=', dlth__lnww, lir.
                    Constant(dlth__lnww.type, 1))
                with builder.if_then(qxfwq__jsfkc):
                    zfovj__gcyb = to_arr_obj_if_list_obj(c, context,
                        builder, zfovj__gcyb, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        zfovj__gcyb).value
                    data_arr = builder.extract_value(data_tup, xng__lrt)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    hyio__amibu, ouex__qhh = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, tprw__pxtg, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(vux__qin)
    c.pyapi.decref(rtf__tdsxb)
    c.pyapi.decref(vhw__dtntg)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    qtv__hks = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    rrgn__bmbfa = context.nrt.meminfo_data(builder, qtv__hks.meminfo)
    fgiot__pby = builder.bitcast(rrgn__bmbfa, context.get_value_type(
        payload_type).as_pointer())
    xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(fgiot__pby))
    return xiu__ntfu


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    xiu__ntfu = _get_struct_arr_payload(c.context, c.builder, typ, val)
    hyio__amibu, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), xiu__ntfu.null_bitmap).data
    cvnc__uymqd = all(isinstance(jfw__sqycm, types.Array) and (jfw__sqycm.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(jfw__sqycm.dtype, TimeType)) for
        jfw__sqycm in typ.data)
    if cvnc__uymqd:
        kyk__xygs, sux__wkc, djni__htk = _get_C_API_ptrs(c, xiu__ntfu.data,
            typ.data, typ.names)
        jdx__ldt = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        vetft__ygqgn = cgutils.get_or_insert_function(c.builder.module,
            jdx__ldt, name='np_array_from_struct_array')
        arr = c.builder.call(vetft__ygqgn, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(kyk__xygs, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            sux__wkc, lir.IntType(8).as_pointer()), c.builder.bitcast(
            djni__htk, lir.IntType(8).as_pointer()), c.context.get_constant
            (types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, xiu__ntfu.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    rea__pmq = context.insert_const_string(builder.module, 'numpy')
    aqu__djurp = c.pyapi.import_module_noblock(rea__pmq)
    wna__qxw = c.pyapi.object_getattr_string(aqu__djurp, 'object_')
    tadvp__qdno = c.pyapi.long_from_longlong(length)
    vvf__soiqz = c.pyapi.call_method(aqu__djurp, 'ndarray', (tadvp__qdno,
        wna__qxw))
    owvg__wst = c.pyapi.object_getattr_string(aqu__djurp, 'nan')
    with cgutils.for_range(builder, length) as afxdj__cagb:
        tprw__pxtg = afxdj__cagb.index
        pyarray_setitem(builder, context, vvf__soiqz, tprw__pxtg, owvg__wst)
        esik__xjnt = get_bitmap_bit(builder, null_bitmap_ptr, tprw__pxtg)
        zracw__pee = builder.icmp_unsigned('!=', esik__xjnt, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(zracw__pee):
            if is_tuple_array:
                vux__qin = c.pyapi.tuple_new(len(typ.data))
            else:
                vux__qin = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(owvg__wst)
                    c.pyapi.tuple_setitem(vux__qin, i, owvg__wst)
                else:
                    c.pyapi.dict_setitem_string(vux__qin, typ.names[i],
                        owvg__wst)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                hyio__amibu, iqu__lzx = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, tprw__pxtg])
                with builder.if_then(iqu__lzx):
                    hyio__amibu, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, tprw__pxtg])
                    ilkx__odav = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(vux__qin, i, ilkx__odav)
                    else:
                        c.pyapi.dict_setitem_string(vux__qin, typ.names[i],
                            ilkx__odav)
                        c.pyapi.decref(ilkx__odav)
            pyarray_setitem(builder, context, vvf__soiqz, tprw__pxtg, vux__qin)
            c.pyapi.decref(vux__qin)
    c.pyapi.decref(aqu__djurp)
    c.pyapi.decref(wna__qxw)
    c.pyapi.decref(tadvp__qdno)
    c.pyapi.decref(owvg__wst)
    return vvf__soiqz


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    clq__unh = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if clq__unh == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for cwrp__vcppv in range(clq__unh)])
    elif nested_counts_type.count < clq__unh:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for cwrp__vcppv in range(
            clq__unh - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(jfw__sqycm) for jfw__sqycm in
            names_typ.types)
    pqulc__zwh = tuple(jfw__sqycm.instance_type for jfw__sqycm in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(pqulc__zwh, names)

    def codegen(context, builder, sig, args):
        vun__wqj, nested_counts, cwrp__vcppv, cwrp__vcppv = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        zzkaf__xklfn, cwrp__vcppv, cwrp__vcppv = construct_struct_array(context
            , builder, struct_arr_type, vun__wqj, nested_counts)
        qtv__hks = context.make_helper(builder, struct_arr_type)
        qtv__hks.meminfo = zzkaf__xklfn
        return qtv__hks._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(jszyt__sdg, str) for
            jszyt__sdg in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yuwd__qme = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, yuwd__qme)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        yuwd__qme = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yuwd__qme)


def define_struct_dtor(context, builder, struct_type, payload_type):
    vgkc__hkhl = builder.module
    jdx__ldt = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    pfrm__syfb = cgutils.get_or_insert_function(vgkc__hkhl, jdx__ldt, name=
        '.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not pfrm__syfb.is_declaration:
        return pfrm__syfb
    pfrm__syfb.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(pfrm__syfb.append_basic_block())
    kjgc__cduby = pfrm__syfb.args[0]
    oezw__jffo = context.get_value_type(payload_type).as_pointer()
    tbpl__igrcb = builder.bitcast(kjgc__cduby, oezw__jffo)
    xiu__ntfu = context.make_helper(builder, payload_type, ref=tbpl__igrcb)
    for i in range(len(struct_type.data)):
        fbkxr__bfo = builder.extract_value(xiu__ntfu.null_bitmap, i)
        zracw__pee = builder.icmp_unsigned('==', fbkxr__bfo, lir.Constant(
            fbkxr__bfo.type, 1))
        with builder.if_then(zracw__pee):
            val = builder.extract_value(xiu__ntfu.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return pfrm__syfb


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    rrgn__bmbfa = context.nrt.meminfo_data(builder, struct.meminfo)
    fgiot__pby = builder.bitcast(rrgn__bmbfa, context.get_value_type(
        payload_type).as_pointer())
    xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(fgiot__pby))
    return xiu__ntfu, fgiot__pby


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    rea__pmq = context.insert_const_string(builder.module, 'pandas')
    rtf__tdsxb = c.pyapi.import_module_noblock(rea__pmq)
    vhw__dtntg = c.pyapi.object_getattr_string(rtf__tdsxb, 'NA')
    hhtzu__hsjba = []
    nulls = []
    for i, jfw__sqycm in enumerate(typ.data):
        ilkx__odav = c.pyapi.dict_getitem_string(val, typ.names[i])
        lsqti__ojor = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        shoq__brwtt = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(jfw__sqycm)))
        dlth__lnww = is_na_value(builder, context, ilkx__odav, vhw__dtntg)
        zracw__pee = builder.icmp_unsigned('!=', dlth__lnww, lir.Constant(
            dlth__lnww.type, 1))
        with builder.if_then(zracw__pee):
            builder.store(context.get_constant(types.uint8, 1), lsqti__ojor)
            field_val = c.pyapi.to_native_value(jfw__sqycm, ilkx__odav).value
            builder.store(field_val, shoq__brwtt)
        hhtzu__hsjba.append(builder.load(shoq__brwtt))
        nulls.append(builder.load(lsqti__ojor))
    c.pyapi.decref(rtf__tdsxb)
    c.pyapi.decref(vhw__dtntg)
    zzkaf__xklfn = construct_struct(context, builder, typ, hhtzu__hsjba, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = zzkaf__xklfn
    wwyqq__kji = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=wwyqq__kji)


@box(StructType)
def box_struct(typ, val, c):
    fxo__dghj = c.pyapi.dict_new(len(typ.data))
    xiu__ntfu, cwrp__vcppv = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(fxo__dghj, typ.names[i], c.pyapi.
            borrow_none())
        fbkxr__bfo = c.builder.extract_value(xiu__ntfu.null_bitmap, i)
        zracw__pee = c.builder.icmp_unsigned('==', fbkxr__bfo, lir.Constant
            (fbkxr__bfo.type, 1))
        with c.builder.if_then(zracw__pee):
            gdg__vbc = c.builder.extract_value(xiu__ntfu.data, i)
            c.context.nrt.incref(c.builder, val_typ, gdg__vbc)
            zfovj__gcyb = c.pyapi.from_native_value(val_typ, gdg__vbc, c.
                env_manager)
            c.pyapi.dict_setitem_string(fxo__dghj, typ.names[i], zfovj__gcyb)
            c.pyapi.decref(zfovj__gcyb)
    c.context.nrt.decref(c.builder, typ, val)
    return fxo__dghj


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(jfw__sqycm) for jfw__sqycm in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, gjlxj__qas = args
        payload_type = StructPayloadType(struct_type.data)
        zvtfn__hodc = context.get_value_type(payload_type)
        jjb__soui = context.get_abi_sizeof(zvtfn__hodc)
        ioxi__fvipt = define_struct_dtor(context, builder, struct_type,
            payload_type)
        zzkaf__xklfn = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jjb__soui), ioxi__fvipt)
        rrgn__bmbfa = context.nrt.meminfo_data(builder, zzkaf__xklfn)
        fgiot__pby = builder.bitcast(rrgn__bmbfa, zvtfn__hodc.as_pointer())
        xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder)
        xiu__ntfu.data = data
        xiu__ntfu.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for cwrp__vcppv in range(len(
            data_typ.types))])
        builder.store(xiu__ntfu._getvalue(), fgiot__pby)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = zzkaf__xklfn
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        xiu__ntfu, cwrp__vcppv = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xiu__ntfu.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        xiu__ntfu, cwrp__vcppv = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xiu__ntfu.null_bitmap)
    jef__zjo = types.UniTuple(types.int8, len(struct_typ.data))
    return jef__zjo(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, cwrp__vcppv, val = args
        xiu__ntfu, fgiot__pby = _get_struct_payload(context, builder,
            struct_typ, struct)
        uokb__szd = xiu__ntfu.data
        eavwk__hqkzz = builder.insert_value(uokb__szd, val, field_ind)
        mbrd__igig = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, mbrd__igig, uokb__szd)
        context.nrt.incref(builder, mbrd__igig, eavwk__hqkzz)
        xiu__ntfu.data = eavwk__hqkzz
        builder.store(xiu__ntfu._getvalue(), fgiot__pby)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    tqzi__fkofz = get_overload_const_str(ind)
    if tqzi__fkofz not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            tqzi__fkofz, struct))
    return struct.names.index(tqzi__fkofz)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    zvtfn__hodc = context.get_value_type(payload_type)
    jjb__soui = context.get_abi_sizeof(zvtfn__hodc)
    ioxi__fvipt = define_struct_dtor(context, builder, struct_type,
        payload_type)
    zzkaf__xklfn = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jjb__soui), ioxi__fvipt)
    rrgn__bmbfa = context.nrt.meminfo_data(builder, zzkaf__xklfn)
    fgiot__pby = builder.bitcast(rrgn__bmbfa, zvtfn__hodc.as_pointer())
    xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder)
    xiu__ntfu.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    xiu__ntfu.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(xiu__ntfu._getvalue(), fgiot__pby)
    return zzkaf__xklfn


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    occ__uoa = tuple(d.dtype for d in struct_arr_typ.data)
    xsjlk__zwtn = StructType(occ__uoa, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        tddk__dge, ind = args
        xiu__ntfu = _get_struct_arr_payload(context, builder,
            struct_arr_typ, tddk__dge)
        hhtzu__hsjba = []
        jab__aagb = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            nggll__snns = builder.extract_value(xiu__ntfu.data, i)
            eaggl__jxjqu = context.compile_internal(builder, lambda arr,
                ind: np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                nggll__snns, ind])
            jab__aagb.append(eaggl__jxjqu)
            ufu__luvi = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            zracw__pee = builder.icmp_unsigned('==', eaggl__jxjqu, lir.
                Constant(eaggl__jxjqu.type, 1))
            with builder.if_then(zracw__pee):
                ysn__okky = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    nggll__snns, ind])
                builder.store(ysn__okky, ufu__luvi)
            hhtzu__hsjba.append(builder.load(ufu__luvi))
        if isinstance(xsjlk__zwtn, types.DictType):
            maife__pez = [context.insert_const_string(builder.module,
                zeo__yxk) for zeo__yxk in struct_arr_typ.names]
            rogu__cqhem = cgutils.pack_array(builder, hhtzu__hsjba)
            ncqdz__kpiix = cgutils.pack_array(builder, maife__pez)

            def impl(names, vals):
                d = {}
                for i, zeo__yxk in enumerate(names):
                    d[zeo__yxk] = vals[i]
                return d
            vrxbg__lqmd = context.compile_internal(builder, impl,
                xsjlk__zwtn(types.Tuple(tuple(types.StringLiteral(zeo__yxk) for
                zeo__yxk in struct_arr_typ.names)), types.Tuple(occ__uoa)),
                [ncqdz__kpiix, rogu__cqhem])
            context.nrt.decref(builder, types.BaseTuple.from_types(occ__uoa
                ), rogu__cqhem)
            return vrxbg__lqmd
        zzkaf__xklfn = construct_struct(context, builder, xsjlk__zwtn,
            hhtzu__hsjba, jab__aagb)
        struct = context.make_helper(builder, xsjlk__zwtn)
        struct.meminfo = zzkaf__xklfn
        return struct._getvalue()
    return xsjlk__zwtn(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xiu__ntfu = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xiu__ntfu.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xiu__ntfu = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xiu__ntfu.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(jfw__sqycm) for jfw__sqycm in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, hsivk__rojfk, gjlxj__qas = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        zvtfn__hodc = context.get_value_type(payload_type)
        jjb__soui = context.get_abi_sizeof(zvtfn__hodc)
        ioxi__fvipt = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        zzkaf__xklfn = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, jjb__soui), ioxi__fvipt)
        rrgn__bmbfa = context.nrt.meminfo_data(builder, zzkaf__xklfn)
        fgiot__pby = builder.bitcast(rrgn__bmbfa, zvtfn__hodc.as_pointer())
        xiu__ntfu = cgutils.create_struct_proxy(payload_type)(context, builder)
        xiu__ntfu.data = data
        xiu__ntfu.null_bitmap = hsivk__rojfk
        builder.store(xiu__ntfu._getvalue(), fgiot__pby)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, hsivk__rojfk)
        qtv__hks = context.make_helper(builder, struct_arr_type)
        qtv__hks.meminfo = zzkaf__xklfn
        return qtv__hks._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    if ind != bodo.boolean_array:
        rco__hujfj = len(arr.data)
        ntsr__iudw = 'def impl(arr, ind):\n'
        ntsr__iudw += '  data = get_data(arr)\n'
        ntsr__iudw += '  null_bitmap = get_null_bitmap(arr)\n'
        if is_list_like_index_type(ind) and ind.dtype == types.bool_:
            ntsr__iudw += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
        elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.
            Integer):
            ntsr__iudw += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
        elif isinstance(ind, types.SliceType):
            ntsr__iudw += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
        else:
            raise BodoError('invalid index {} in struct array indexing'.
                format(ind))
        ntsr__iudw += (
            '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.
            format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
            i in range(rco__hujfj)), ', '.join("'{}'".format(zeo__yxk) for
            zeo__yxk in arr.names)))
        hgyn__gknju = {}
        exec(ntsr__iudw, {'init_struct_arr': init_struct_arr, 'get_data':
            get_data, 'get_null_bitmap': get_null_bitmap,
            'ensure_contig_if_np': bodo.utils.conversion.
            ensure_contig_if_np, 'get_new_null_mask_bool_index': bodo.utils
            .indexing.get_new_null_mask_bool_index,
            'get_new_null_mask_int_index': bodo.utils.indexing.
            get_new_null_mask_int_index, 'get_new_null_mask_slice_index':
            bodo.utils.indexing.get_new_null_mask_slice_index}, hgyn__gknju)
        impl = hgyn__gknju['impl']
        return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        rco__hujfj = len(arr.data)
        ntsr__iudw = 'def impl(arr, ind, val):\n'
        ntsr__iudw += '  data = get_data(arr)\n'
        ntsr__iudw += '  null_bitmap = get_null_bitmap(arr)\n'
        ntsr__iudw += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(rco__hujfj):
            if isinstance(val, StructType):
                ntsr__iudw += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                ntsr__iudw += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                ntsr__iudw += '  else:\n'
                ntsr__iudw += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                ntsr__iudw += "  data[{}][ind] = val['{}']\n".format(i, arr
                    .names[i])
        hgyn__gknju = {}
        exec(ntsr__iudw, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, hgyn__gknju)
        impl = hgyn__gknju['impl']
        return impl
    if isinstance(ind, types.SliceType):
        rco__hujfj = len(arr.data)
        ntsr__iudw = 'def impl(arr, ind, val):\n'
        ntsr__iudw += '  data = get_data(arr)\n'
        ntsr__iudw += '  null_bitmap = get_null_bitmap(arr)\n'
        ntsr__iudw += '  val_data = get_data(val)\n'
        ntsr__iudw += '  val_null_bitmap = get_null_bitmap(val)\n'
        ntsr__iudw += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(rco__hujfj):
            ntsr__iudw += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        hgyn__gknju = {}
        exec(ntsr__iudw, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, hgyn__gknju)
        impl = hgyn__gknju['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    ntsr__iudw = 'def impl(A):\n'
    ntsr__iudw += '  total_nbytes = 0\n'
    ntsr__iudw += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        ntsr__iudw += f'  total_nbytes += data[{i}].nbytes\n'
    ntsr__iudw += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    ntsr__iudw += '  return total_nbytes\n'
    hgyn__gknju = {}
    exec(ntsr__iudw, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, hgyn__gknju)
    impl = hgyn__gknju['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        hsivk__rojfk = get_null_bitmap(A)
        fnju__xxb = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        aae__sjp = hsivk__rojfk.copy()
        return init_struct_arr(fnju__xxb, aae__sjp, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(jszyt__sdg.copy() for jszyt__sdg in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    omqz__tew = arrs.count
    ntsr__iudw = 'def f(arrs):\n'
    ntsr__iudw += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(omqz__tew)))
    hgyn__gknju = {}
    exec(ntsr__iudw, {}, hgyn__gknju)
    impl = hgyn__gknju['f']
    return impl
