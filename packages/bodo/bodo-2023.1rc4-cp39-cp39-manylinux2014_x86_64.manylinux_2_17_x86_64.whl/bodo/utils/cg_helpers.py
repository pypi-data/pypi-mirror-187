"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    jmuf__zjim = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vsmz__jyur = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    eaeq__uumds = builder.gep(null_bitmap_ptr, [jmuf__zjim], inbounds=True)
    ewkzf__ylz = builder.load(eaeq__uumds)
    ocnqv__cahns = lir.ArrayType(lir.IntType(8), 8)
    fta__eyxf = cgutils.alloca_once_value(builder, lir.Constant(
        ocnqv__cahns, (1, 2, 4, 8, 16, 32, 64, 128)))
    kdn__qpvgd = builder.load(builder.gep(fta__eyxf, [lir.Constant(lir.
        IntType(64), 0), vsmz__jyur], inbounds=True))
    if val:
        builder.store(builder.or_(ewkzf__ylz, kdn__qpvgd), eaeq__uumds)
    else:
        kdn__qpvgd = builder.xor(kdn__qpvgd, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(ewkzf__ylz, kdn__qpvgd), eaeq__uumds)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    jmuf__zjim = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vsmz__jyur = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ewkzf__ylz = builder.load(builder.gep(null_bitmap_ptr, [jmuf__zjim],
        inbounds=True))
    ocnqv__cahns = lir.ArrayType(lir.IntType(8), 8)
    fta__eyxf = cgutils.alloca_once_value(builder, lir.Constant(
        ocnqv__cahns, (1, 2, 4, 8, 16, 32, 64, 128)))
    kdn__qpvgd = builder.load(builder.gep(fta__eyxf, [lir.Constant(lir.
        IntType(64), 0), vsmz__jyur], inbounds=True))
    return builder.and_(ewkzf__ylz, kdn__qpvgd)


def pyarray_check(builder, context, obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    rovds__clwxg = lir.FunctionType(lir.IntType(32), [istad__wdc])
    ezof__enr = cgutils.get_or_insert_function(builder.module, rovds__clwxg,
        name='is_np_array')
    return builder.call(ezof__enr, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    istad__wdc = context.get_argument_type(types.pyobject)
    vmq__zsg = context.get_value_type(types.intp)
    rutjz__whb = lir.FunctionType(lir.IntType(8).as_pointer(), [istad__wdc,
        vmq__zsg])
    wqd__heiu = cgutils.get_or_insert_function(builder.module, rutjz__whb,
        name='array_getptr1')
    krvq__ojay = lir.FunctionType(istad__wdc, [istad__wdc, lir.IntType(8).
        as_pointer()])
    rsud__vaq = cgutils.get_or_insert_function(builder.module, krvq__ojay,
        name='array_getitem')
    gwe__eaim = builder.call(wqd__heiu, [arr_obj, ind])
    return builder.call(rsud__vaq, [arr_obj, gwe__eaim])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    vmq__zsg = context.get_value_type(types.intp)
    rutjz__whb = lir.FunctionType(lir.IntType(8).as_pointer(), [istad__wdc,
        vmq__zsg])
    wqd__heiu = cgutils.get_or_insert_function(builder.module, rutjz__whb,
        name='array_getptr1')
    gnhiu__kbqzh = lir.FunctionType(lir.VoidType(), [istad__wdc, lir.
        IntType(8).as_pointer(), istad__wdc])
    bclbp__hwr = cgutils.get_or_insert_function(builder.module,
        gnhiu__kbqzh, name='array_setitem')
    gwe__eaim = builder.call(wqd__heiu, [arr_obj, ind])
    builder.call(bclbp__hwr, [arr_obj, gwe__eaim, val_obj])


def seq_getitem(builder, context, obj, ind):
    istad__wdc = context.get_argument_type(types.pyobject)
    vmq__zsg = context.get_value_type(types.intp)
    tjms__yfkwt = lir.FunctionType(istad__wdc, [istad__wdc, vmq__zsg])
    jovj__bato = cgutils.get_or_insert_function(builder.module, tjms__yfkwt,
        name='seq_getitem')
    return builder.call(jovj__bato, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    istad__wdc = context.get_argument_type(types.pyobject)
    yqhdx__esp = lir.FunctionType(lir.IntType(32), [istad__wdc, istad__wdc])
    wtyxy__pjfwh = cgutils.get_or_insert_function(builder.module,
        yqhdx__esp, name='is_na_value')
    return builder.call(wtyxy__pjfwh, [val, C_NA])


def list_check(builder, context, obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    obeu__ydx = context.get_value_type(types.int32)
    ciw__tnfi = lir.FunctionType(obeu__ydx, [istad__wdc])
    imij__ponj = cgutils.get_or_insert_function(builder.module, ciw__tnfi,
        name='list_check')
    return builder.call(imij__ponj, [obj])


def dict_keys(builder, context, obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    ciw__tnfi = lir.FunctionType(istad__wdc, [istad__wdc])
    imij__ponj = cgutils.get_or_insert_function(builder.module, ciw__tnfi,
        name='dict_keys')
    return builder.call(imij__ponj, [obj])


def dict_values(builder, context, obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    ciw__tnfi = lir.FunctionType(istad__wdc, [istad__wdc])
    imij__ponj = cgutils.get_or_insert_function(builder.module, ciw__tnfi,
        name='dict_values')
    return builder.call(imij__ponj, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    istad__wdc = context.get_argument_type(types.pyobject)
    ciw__tnfi = lir.FunctionType(lir.VoidType(), [istad__wdc, istad__wdc])
    imij__ponj = cgutils.get_or_insert_function(builder.module, ciw__tnfi,
        name='dict_merge_from_seq2')
    builder.call(imij__ponj, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    hydp__xpw = cgutils.alloca_once_value(builder, val)
    maeo__tyvxl = list_check(builder, context, val)
    dci__fqmdc = builder.icmp_unsigned('!=', maeo__tyvxl, lir.Constant(
        maeo__tyvxl.type, 0))
    with builder.if_then(dci__fqmdc):
        tyio__scf = context.insert_const_string(builder.module, 'numpy')
        joozk__owb = c.pyapi.import_module_noblock(tyio__scf)
        qehw__rvnzu = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            qehw__rvnzu = str(typ.dtype)
        yfp__gjoby = c.pyapi.object_getattr_string(joozk__owb, qehw__rvnzu)
        jon__nbmgs = builder.load(hydp__xpw)
        ybw__kogs = c.pyapi.call_method(joozk__owb, 'asarray', (jon__nbmgs,
            yfp__gjoby))
        builder.store(ybw__kogs, hydp__xpw)
        c.pyapi.decref(joozk__owb)
        c.pyapi.decref(yfp__gjoby)
    val = builder.load(hydp__xpw)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        pgb__lhndn = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        oqg__dacmu, gbir__gbvtx = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [pgb__lhndn])
        context.nrt.decref(builder, typ, pgb__lhndn)
        return cgutils.pack_array(builder, [gbir__gbvtx])
    if isinstance(typ, (StructType, types.BaseTuple)):
        tyio__scf = context.insert_const_string(builder.module, 'pandas')
        psr__wbuwf = c.pyapi.import_module_noblock(tyio__scf)
        C_NA = c.pyapi.object_getattr_string(psr__wbuwf, 'NA')
        faosv__vce = bodo.utils.transform.get_type_alloc_counts(typ)
        otls__kki = context.make_tuple(builder, types.Tuple(faosv__vce * [
            types.int64]), faosv__vce * [context.get_constant(types.int64, 0)])
        mxfp__lhcax = cgutils.alloca_once_value(builder, otls__kki)
        wrbv__vks = 0
        yjqr__giiq = typ.data if isinstance(typ, StructType) else typ.types
        for lpcql__wegwr, t in enumerate(yjqr__giiq):
            npcdo__xsj = bodo.utils.transform.get_type_alloc_counts(t)
            if npcdo__xsj == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    lpcql__wegwr])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, lpcql__wegwr)
            pzsu__pvtk = is_na_value(builder, context, val_obj, C_NA)
            ozh__bwth = builder.icmp_unsigned('!=', pzsu__pvtk, lir.
                Constant(pzsu__pvtk.type, 1))
            with builder.if_then(ozh__bwth):
                otls__kki = builder.load(mxfp__lhcax)
                rgw__pyygk = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for lpcql__wegwr in range(npcdo__xsj):
                    mnixj__gicsr = builder.extract_value(otls__kki, 
                        wrbv__vks + lpcql__wegwr)
                    jlzu__anjsu = builder.extract_value(rgw__pyygk,
                        lpcql__wegwr)
                    otls__kki = builder.insert_value(otls__kki, builder.add
                        (mnixj__gicsr, jlzu__anjsu), wrbv__vks + lpcql__wegwr)
                builder.store(otls__kki, mxfp__lhcax)
            wrbv__vks += npcdo__xsj
        c.pyapi.decref(psr__wbuwf)
        c.pyapi.decref(C_NA)
        return builder.load(mxfp__lhcax)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    tyio__scf = context.insert_const_string(builder.module, 'pandas')
    psr__wbuwf = c.pyapi.import_module_noblock(tyio__scf)
    C_NA = c.pyapi.object_getattr_string(psr__wbuwf, 'NA')
    faosv__vce = bodo.utils.transform.get_type_alloc_counts(typ)
    otls__kki = context.make_tuple(builder, types.Tuple(faosv__vce * [types
        .int64]), [n] + (faosv__vce - 1) * [context.get_constant(types.
        int64, 0)])
    mxfp__lhcax = cgutils.alloca_once_value(builder, otls__kki)
    with cgutils.for_range(builder, n) as erc__xys:
        ezbjq__gwvx = erc__xys.index
        wqvi__mdqjz = seq_getitem(builder, context, arr_obj, ezbjq__gwvx)
        pzsu__pvtk = is_na_value(builder, context, wqvi__mdqjz, C_NA)
        ozh__bwth = builder.icmp_unsigned('!=', pzsu__pvtk, lir.Constant(
            pzsu__pvtk.type, 1))
        with builder.if_then(ozh__bwth):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                otls__kki = builder.load(mxfp__lhcax)
                rgw__pyygk = get_array_elem_counts(c, builder, context,
                    wqvi__mdqjz, typ.dtype)
                for lpcql__wegwr in range(faosv__vce - 1):
                    mnixj__gicsr = builder.extract_value(otls__kki, 
                        lpcql__wegwr + 1)
                    jlzu__anjsu = builder.extract_value(rgw__pyygk,
                        lpcql__wegwr)
                    otls__kki = builder.insert_value(otls__kki, builder.add
                        (mnixj__gicsr, jlzu__anjsu), lpcql__wegwr + 1)
                builder.store(otls__kki, mxfp__lhcax)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                wrbv__vks = 1
                for lpcql__wegwr, t in enumerate(typ.data):
                    npcdo__xsj = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if npcdo__xsj == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(wqvi__mdqjz,
                            lpcql__wegwr)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(wqvi__mdqjz,
                            typ.names[lpcql__wegwr])
                    pzsu__pvtk = is_na_value(builder, context, val_obj, C_NA)
                    ozh__bwth = builder.icmp_unsigned('!=', pzsu__pvtk, lir
                        .Constant(pzsu__pvtk.type, 1))
                    with builder.if_then(ozh__bwth):
                        otls__kki = builder.load(mxfp__lhcax)
                        rgw__pyygk = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for lpcql__wegwr in range(npcdo__xsj):
                            mnixj__gicsr = builder.extract_value(otls__kki,
                                wrbv__vks + lpcql__wegwr)
                            jlzu__anjsu = builder.extract_value(rgw__pyygk,
                                lpcql__wegwr)
                            otls__kki = builder.insert_value(otls__kki,
                                builder.add(mnixj__gicsr, jlzu__anjsu), 
                                wrbv__vks + lpcql__wegwr)
                        builder.store(otls__kki, mxfp__lhcax)
                    wrbv__vks += npcdo__xsj
            else:
                assert isinstance(typ, MapArrayType), typ
                otls__kki = builder.load(mxfp__lhcax)
                dnu__nxy = dict_keys(builder, context, wqvi__mdqjz)
                xra__gob = dict_values(builder, context, wqvi__mdqjz)
                gawzn__jqh = get_array_elem_counts(c, builder, context,
                    dnu__nxy, typ.key_arr_type)
                canhd__ioqq = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for lpcql__wegwr in range(1, canhd__ioqq + 1):
                    mnixj__gicsr = builder.extract_value(otls__kki,
                        lpcql__wegwr)
                    jlzu__anjsu = builder.extract_value(gawzn__jqh, 
                        lpcql__wegwr - 1)
                    otls__kki = builder.insert_value(otls__kki, builder.add
                        (mnixj__gicsr, jlzu__anjsu), lpcql__wegwr)
                bsww__pmj = get_array_elem_counts(c, builder, context,
                    xra__gob, typ.value_arr_type)
                for lpcql__wegwr in range(canhd__ioqq + 1, faosv__vce):
                    mnixj__gicsr = builder.extract_value(otls__kki,
                        lpcql__wegwr)
                    jlzu__anjsu = builder.extract_value(bsww__pmj, 
                        lpcql__wegwr - canhd__ioqq)
                    otls__kki = builder.insert_value(otls__kki, builder.add
                        (mnixj__gicsr, jlzu__anjsu), lpcql__wegwr)
                builder.store(otls__kki, mxfp__lhcax)
                c.pyapi.decref(dnu__nxy)
                c.pyapi.decref(xra__gob)
        c.pyapi.decref(wqvi__mdqjz)
    c.pyapi.decref(psr__wbuwf)
    c.pyapi.decref(C_NA)
    return builder.load(mxfp__lhcax)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    hcn__ajlng = n_elems.type.count
    assert hcn__ajlng >= 1
    yonbw__oykt = builder.extract_value(n_elems, 0)
    if hcn__ajlng != 1:
        bpe__ykw = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, lpcql__wegwr) for lpcql__wegwr in range(1, hcn__ajlng)])
        lnjb__dyyl = types.Tuple([types.int64] * (hcn__ajlng - 1))
    else:
        bpe__ykw = context.get_dummy_value()
        lnjb__dyyl = types.none
    iuan__akabk = types.TypeRef(arr_type)
    obvmy__qejxn = arr_type(types.int64, iuan__akabk, lnjb__dyyl)
    args = [yonbw__oykt, context.get_dummy_value(), bpe__ykw]
    lmi__ajhgd = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        oqg__dacmu, oqz__djkw = c.pyapi.call_jit_code(lmi__ajhgd,
            obvmy__qejxn, args)
    else:
        oqz__djkw = context.compile_internal(builder, lmi__ajhgd,
            obvmy__qejxn, args)
    return oqz__djkw


def is_ll_eq(builder, val1, val2):
    eggz__fxch = val1.type.pointee
    zvs__lzy = val2.type.pointee
    assert eggz__fxch == zvs__lzy, 'invalid llvm value comparison'
    if isinstance(eggz__fxch, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(eggz__fxch.elements) if isinstance(eggz__fxch, lir.
            BaseStructType) else eggz__fxch.count
        upney__glf = lir.Constant(lir.IntType(1), 1)
        for lpcql__wegwr in range(n_elems):
            fqq__slx = lir.IntType(32)(0)
            fxtnc__gnw = lir.IntType(32)(lpcql__wegwr)
            hvuc__ovagt = builder.gep(val1, [fqq__slx, fxtnc__gnw],
                inbounds=True)
            hoae__yxm = builder.gep(val2, [fqq__slx, fxtnc__gnw], inbounds=True
                )
            upney__glf = builder.and_(upney__glf, is_ll_eq(builder,
                hvuc__ovagt, hoae__yxm))
        return upney__glf
    ktg__lun = builder.load(val1)
    ecn__khx = builder.load(val2)
    if ktg__lun.type in (lir.FloatType(), lir.DoubleType()):
        djqon__kab = 32 if ktg__lun.type == lir.FloatType() else 64
        ktg__lun = builder.bitcast(ktg__lun, lir.IntType(djqon__kab))
        ecn__khx = builder.bitcast(ecn__khx, lir.IntType(djqon__kab))
    return builder.icmp_unsigned('==', ktg__lun, ecn__khx)
