"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    wqv__wnhb = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(wqv__wnhb)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jvdh__txn = _get_map_arr_data_type(fe_type)
        aykxq__oci = [('data', jvdh__txn)]
        models.StructModel.__init__(self, dmm, fe_type, aykxq__oci)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    ynp__dfs = all(isinstance(doz__zzmtl, types.Array) and doz__zzmtl.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        doz__zzmtl in (typ.key_arr_type, typ.value_arr_type))
    if ynp__dfs:
        idg__azbdp = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        jahj__sir = cgutils.get_or_insert_function(c.builder.module,
            idg__azbdp, name='count_total_elems_list_array')
        ova__ltys = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            jahj__sir, [val])])
    else:
        ova__ltys = get_array_elem_counts(c, c.builder, c.context, val, typ)
    jvdh__txn = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, jvdh__txn, ova__ltys, c
        )
    heqm__fqev = _get_array_item_arr_payload(c.context, c.builder,
        jvdh__txn, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, heqm__fqev.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, heqm__fqev.offsets).data
    gbwlc__rfku = _get_struct_arr_payload(c.context, c.builder, jvdh__txn.
        dtype, heqm__fqev.data)
    key_arr = c.builder.extract_value(gbwlc__rfku.data, 0)
    value_arr = c.builder.extract_value(gbwlc__rfku.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    aqd__krj, cdp__qqnra = c.pyapi.call_jit_code(lambda A: A.fill(255), sig,
        [gbwlc__rfku.null_bitmap])
    if ynp__dfs:
        egzet__mcswz = c.context.make_array(jvdh__txn.dtype.data[0])(c.
            context, c.builder, key_arr).data
        hlsn__mydxa = c.context.make_array(jvdh__txn.dtype.data[1])(c.
            context, c.builder, value_arr).data
        idg__azbdp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        gvg__oqdk = cgutils.get_or_insert_function(c.builder.module,
            idg__azbdp, name='map_array_from_sequence')
        yml__jxtb = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        wiuf__kemf = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(gvg__oqdk, [val, c.builder.bitcast(egzet__mcswz, lir
            .IntType(8).as_pointer()), c.builder.bitcast(hlsn__mydxa, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), yml__jxtb), lir.Constant(lir.IntType(
            32), wiuf__kemf)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    itmty__azvxj = c.context.make_helper(c.builder, typ)
    itmty__azvxj.data = data_arr
    cil__iiog = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(itmty__azvxj._getvalue(), is_error=cil__iiog)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    lezgp__qrnz = context.insert_const_string(builder.module, 'pandas')
    xbujj__jrw = c.pyapi.import_module_noblock(lezgp__qrnz)
    wdi__vbwc = c.pyapi.object_getattr_string(xbujj__jrw, 'NA')
    tthr__zcqjt = c.context.get_constant(offset_type, 0)
    builder.store(tthr__zcqjt, offsets_ptr)
    cwa__wqpn = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as bnt__axkj:
        thk__vvmcc = bnt__axkj.index
        item_ind = builder.load(cwa__wqpn)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [thk__vvmcc]))
        shra__leq = seq_getitem(builder, context, val, thk__vvmcc)
        set_bitmap_bit(builder, null_bitmap_ptr, thk__vvmcc, 0)
        tlnhn__cmwh = is_na_value(builder, context, shra__leq, wdi__vbwc)
        rax__qkn = builder.icmp_unsigned('!=', tlnhn__cmwh, lir.Constant(
            tlnhn__cmwh.type, 1))
        with builder.if_then(rax__qkn):
            set_bitmap_bit(builder, null_bitmap_ptr, thk__vvmcc, 1)
            abmss__tsikl = dict_keys(builder, context, shra__leq)
            cigy__lttdn = dict_values(builder, context, shra__leq)
            n_items = bodo.utils.utils.object_length(c, abmss__tsikl)
            _unbox_array_item_array_copy_data(typ.key_arr_type,
                abmss__tsikl, c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                cigy__lttdn, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), cwa__wqpn)
            c.pyapi.decref(abmss__tsikl)
            c.pyapi.decref(cigy__lttdn)
        c.pyapi.decref(shra__leq)
    builder.store(builder.trunc(builder.load(cwa__wqpn), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(xbujj__jrw)
    c.pyapi.decref(wdi__vbwc)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    itmty__azvxj = c.context.make_helper(c.builder, typ, val)
    data_arr = itmty__azvxj.data
    jvdh__txn = _get_map_arr_data_type(typ)
    heqm__fqev = _get_array_item_arr_payload(c.context, c.builder,
        jvdh__txn, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, heqm__fqev.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, heqm__fqev.offsets).data
    gbwlc__rfku = _get_struct_arr_payload(c.context, c.builder, jvdh__txn.
        dtype, heqm__fqev.data)
    key_arr = c.builder.extract_value(gbwlc__rfku.data, 0)
    value_arr = c.builder.extract_value(gbwlc__rfku.data, 1)
    if all(isinstance(doz__zzmtl, types.Array) and doz__zzmtl.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        doz__zzmtl in (typ.key_arr_type, typ.value_arr_type)):
        egzet__mcswz = c.context.make_array(jvdh__txn.dtype.data[0])(c.
            context, c.builder, key_arr).data
        hlsn__mydxa = c.context.make_array(jvdh__txn.dtype.data[1])(c.
            context, c.builder, value_arr).data
        idg__azbdp = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        drj__ulms = cgutils.get_or_insert_function(c.builder.module,
            idg__azbdp, name='np_array_from_map_array')
        yml__jxtb = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        wiuf__kemf = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(drj__ulms, [heqm__fqev.n_arrays, c.builder.
            bitcast(egzet__mcswz, lir.IntType(8).as_pointer()), c.builder.
            bitcast(hlsn__mydxa, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), yml__jxtb), lir.
            Constant(lir.IntType(32), wiuf__kemf)])
    else:
        arr = _box_map_array_generic(typ, c, heqm__fqev.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    lezgp__qrnz = context.insert_const_string(builder.module, 'numpy')
    loeo__rlnj = c.pyapi.import_module_noblock(lezgp__qrnz)
    vbxto__bkd = c.pyapi.object_getattr_string(loeo__rlnj, 'object_')
    pmte__ppgfe = c.pyapi.long_from_longlong(n_maps)
    glfnb__crzai = c.pyapi.call_method(loeo__rlnj, 'ndarray', (pmte__ppgfe,
        vbxto__bkd))
    bjqud__eldg = c.pyapi.object_getattr_string(loeo__rlnj, 'nan')
    zst__ucs = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    cwa__wqpn = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_maps) as bnt__axkj:
        qir__pccwg = bnt__axkj.index
        pyarray_setitem(builder, context, glfnb__crzai, qir__pccwg, bjqud__eldg
            )
        wei__nwpa = get_bitmap_bit(builder, null_bitmap_ptr, qir__pccwg)
        cydem__oexe = builder.icmp_unsigned('!=', wei__nwpa, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(cydem__oexe):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(qir__pccwg, lir.Constant(
                qir__pccwg.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [qir__pccwg]))), lir.IntType(64))
            item_ind = builder.load(cwa__wqpn)
            shra__leq = c.pyapi.dict_new()
            wrvt__mfs = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            aqd__krj, nbva__bkqdq = c.pyapi.call_jit_code(wrvt__mfs, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            aqd__krj, vyosb__ddyhm = c.pyapi.call_jit_code(wrvt__mfs, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            lhlv__tgi = c.pyapi.from_native_value(typ.key_arr_type,
                nbva__bkqdq, c.env_manager)
            sawek__frrb = c.pyapi.from_native_value(typ.value_arr_type,
                vyosb__ddyhm, c.env_manager)
            xgwok__qzz = c.pyapi.call_function_objargs(zst__ucs, (lhlv__tgi,
                sawek__frrb))
            dict_merge_from_seq2(builder, context, shra__leq, xgwok__qzz)
            builder.store(builder.add(item_ind, n_items), cwa__wqpn)
            pyarray_setitem(builder, context, glfnb__crzai, qir__pccwg,
                shra__leq)
            c.pyapi.decref(xgwok__qzz)
            c.pyapi.decref(lhlv__tgi)
            c.pyapi.decref(sawek__frrb)
            c.pyapi.decref(shra__leq)
    c.pyapi.decref(zst__ucs)
    c.pyapi.decref(loeo__rlnj)
    c.pyapi.decref(vbxto__bkd)
    c.pyapi.decref(pmte__ppgfe)
    c.pyapi.decref(bjqud__eldg)
    return glfnb__crzai


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    itmty__azvxj = context.make_helper(builder, sig.return_type)
    itmty__azvxj.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return itmty__azvxj._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    yfq__nxzw = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return yfq__nxzw(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    razc__oyit = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(razc__oyit)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    hntyf__boqe = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            mze__imtet = val.keys()
            uncz__mmi = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), hntyf__boqe, ('key', 'value'))
            for yqy__caa, pml__hyt in enumerate(mze__imtet):
                uncz__mmi[yqy__caa] = bodo.libs.struct_arr_ext.init_struct((
                    pml__hyt, val[pml__hyt]), ('key', 'value'))
            arr._data[ind] = uncz__mmi
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            juos__pzd = dict()
            bquyl__chhb = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            uncz__mmi = bodo.libs.array_item_arr_ext.get_data(arr._data)
            otx__zdm, qhy__ljt = bodo.libs.struct_arr_ext.get_data(uncz__mmi)
            pjg__phj = bquyl__chhb[ind]
            wzp__ahrg = bquyl__chhb[ind + 1]
            for yqy__caa in range(pjg__phj, wzp__ahrg):
                juos__pzd[otx__zdm[yqy__caa]] = qhy__ljt[yqy__caa]
            return juos__pzd
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
