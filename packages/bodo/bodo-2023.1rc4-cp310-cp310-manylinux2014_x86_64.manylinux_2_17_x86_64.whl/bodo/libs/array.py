"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_cast
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_overload_none, is_str_arr_type, raise_bodo_error, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('get_has_deduped_local_dictionary', array_ext.
    get_has_deduped_local_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('time_array_to_info', array_ext.time_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('decref_table_array', array_ext.decref_table_array)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('cross_join_table', array_ext.cross_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('convert_local_dictionary_to_global', array_ext.
    convert_local_dictionary_to_global)
ll.add_symbol('drop_duplicates_local_dictionary', array_ext.
    drop_duplicates_local_dictionary)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@lower_cast(table_type, types.voidptr)
def lower_table_type(context, builder, fromty, toty, val):
    return val


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        kave__tlg = context.make_helper(builder, arr_type, in_arr)
        in_arr = kave__tlg.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        snmk__knwy = context.make_helper(builder, arr_type, in_arr)
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='list_string_array_to_info')
        return builder.call(knp__kkp, [snmk__knwy.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                fnk__iaent = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for tslyl__ovq in arr_typ.data:
                    fnk__iaent += get_types(tslyl__ovq)
                return fnk__iaent
            elif isinstance(arr_typ, (types.Array, IntegerArrayType,
                FloatingArrayType)) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            length = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                qwxq__duhf = context.make_helper(builder, arr_typ, value=arr)
                omtgm__oubsk = get_lengths(_get_map_arr_data_type(arr_typ),
                    qwxq__duhf.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                maz__jyrqh = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                omtgm__oubsk = get_lengths(arr_typ.dtype, maz__jyrqh.data)
                omtgm__oubsk = cgutils.pack_array(builder, [maz__jyrqh.
                    n_arrays] + [builder.extract_value(omtgm__oubsk,
                    qlh__llmo) for qlh__llmo in range(omtgm__oubsk.type.count)]
                    )
            elif isinstance(arr_typ, StructArrayType):
                maz__jyrqh = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                omtgm__oubsk = []
                for qlh__llmo, tslyl__ovq in enumerate(arr_typ.data):
                    otvb__qijh = get_lengths(tslyl__ovq, builder.
                        extract_value(maz__jyrqh.data, qlh__llmo))
                    omtgm__oubsk += [builder.extract_value(otvb__qijh,
                        iit__elmqb) for iit__elmqb in range(otvb__qijh.type
                        .count)]
                omtgm__oubsk = cgutils.pack_array(builder, [length, context
                    .get_constant(types.int64, -1)] + omtgm__oubsk)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                omtgm__oubsk = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return omtgm__oubsk

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                qwxq__duhf = context.make_helper(builder, arr_typ, value=arr)
                ooi__tmhz = get_buffers(_get_map_arr_data_type(arr_typ),
                    qwxq__duhf.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                maz__jyrqh = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                oang__trml = get_buffers(arr_typ.dtype, maz__jyrqh.data)
                gzpsx__onm = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, maz__jyrqh.offsets)
                fglke__skdr = builder.bitcast(gzpsx__onm.data, lir.IntType(
                    8).as_pointer())
                jux__myk = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, maz__jyrqh.null_bitmap)
                muvfs__ioawl = builder.bitcast(jux__myk.data, lir.IntType(8
                    ).as_pointer())
                ooi__tmhz = cgutils.pack_array(builder, [fglke__skdr,
                    muvfs__ioawl] + [builder.extract_value(oang__trml,
                    qlh__llmo) for qlh__llmo in range(oang__trml.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                maz__jyrqh = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                oang__trml = []
                for qlh__llmo, tslyl__ovq in enumerate(arr_typ.data):
                    oxhlv__rlds = get_buffers(tslyl__ovq, builder.
                        extract_value(maz__jyrqh.data, qlh__llmo))
                    oang__trml += [builder.extract_value(oxhlv__rlds,
                        iit__elmqb) for iit__elmqb in range(oxhlv__rlds.
                        type.count)]
                jux__myk = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, maz__jyrqh.null_bitmap)
                muvfs__ioawl = builder.bitcast(jux__myk.data, lir.IntType(8
                    ).as_pointer())
                ooi__tmhz = cgutils.pack_array(builder, [muvfs__ioawl] +
                    oang__trml)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                hdnab__hiapa = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    hdnab__hiapa = int128_type
                elif arr_typ == datetime_date_array_type:
                    hdnab__hiapa = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                hncd__pdzd = context.make_array(types.Array(hdnab__hiapa, 1,
                    'C'))(context, builder, arr.data)
                jux__myk = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, arr.null_bitmap)
                xrxt__sluvo = builder.bitcast(hncd__pdzd.data, lir.IntType(
                    8).as_pointer())
                muvfs__ioawl = builder.bitcast(jux__myk.data, lir.IntType(8
                    ).as_pointer())
                ooi__tmhz = cgutils.pack_array(builder, [muvfs__ioawl,
                    xrxt__sluvo])
            elif arr_typ in (string_array_type, binary_array_type):
                maz__jyrqh = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                fwd__fiiy = context.make_helper(builder, offset_arr_type,
                    maz__jyrqh.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    maz__jyrqh.data).data
                xjvy__zizy = context.make_helper(builder,
                    null_bitmap_arr_type, maz__jyrqh.null_bitmap).data
                ooi__tmhz = cgutils.pack_array(builder, [builder.bitcast(
                    fwd__fiiy, lir.IntType(8).as_pointer()), builder.
                    bitcast(xjvy__zizy, lir.IntType(8).as_pointer()),
                    builder.bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                xrxt__sluvo = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                ooka__opn = lir.Constant(lir.IntType(8).as_pointer(), None)
                ooi__tmhz = cgutils.pack_array(builder, [ooka__opn,
                    xrxt__sluvo])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return ooi__tmhz

        def get_field_names(arr_typ):
            vpos__yxp = []
            if isinstance(arr_typ, StructArrayType):
                for ttvj__fsx, slthx__wfvpq in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    vpos__yxp.append(ttvj__fsx)
                    vpos__yxp += get_field_names(slthx__wfvpq)
            elif isinstance(arr_typ, ArrayItemArrayType):
                vpos__yxp += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                vpos__yxp += get_field_names(_get_map_arr_data_type(arr_typ))
            return vpos__yxp
        fnk__iaent = get_types(arr_type)
        vuwer__hcoa = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in fnk__iaent])
        xve__bzzsk = cgutils.alloca_once_value(builder, vuwer__hcoa)
        omtgm__oubsk = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, omtgm__oubsk)
        ooi__tmhz = get_buffers(arr_type, in_arr)
        pgmdi__ysnir = cgutils.alloca_once_value(builder, ooi__tmhz)
        vpos__yxp = get_field_names(arr_type)
        if len(vpos__yxp) == 0:
            vpos__yxp = ['irrelevant']
        yzgrb__jcp = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in vpos__yxp])
        ykb__khe = cgutils.alloca_once_value(builder, yzgrb__jcp)
        if isinstance(arr_type, MapArrayType):
            bzeb__iuf = _get_map_arr_data_type(arr_type)
            kxczy__tqj = context.make_helper(builder, arr_type, value=in_arr)
            mriwj__aowl = kxczy__tqj.data
        else:
            bzeb__iuf = arr_type
            mriwj__aowl = in_arr
        lpwl__kyabt = context.make_helper(builder, bzeb__iuf, mriwj__aowl)
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='nested_array_to_info')
        woexm__xdgxr = builder.call(knp__kkp, [builder.bitcast(xve__bzzsk,
            lir.IntType(32).as_pointer()), builder.bitcast(pgmdi__ysnir,
            lir.IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ykb__khe, lir.IntType(8).as_pointer()), lpwl__kyabt.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    if arr_type in (string_array_type, binary_array_type):
        sjhg__pabj = context.make_helper(builder, arr_type, in_arr)
        boyfz__ktvqd = ArrayItemArrayType(char_arr_type)
        snmk__knwy = context.make_helper(builder, boyfz__ktvqd, sjhg__pabj.data
            )
        maz__jyrqh = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        fwd__fiiy = context.make_helper(builder, offset_arr_type,
            maz__jyrqh.offsets).data
        data = context.make_helper(builder, char_arr_type, maz__jyrqh.data
            ).data
        xjvy__zizy = context.make_helper(builder, null_bitmap_arr_type,
            maz__jyrqh.null_bitmap).data
        sijve__iged = builder.zext(builder.load(builder.gep(fwd__fiiy, [
            maz__jyrqh.n_arrays])), lir.IntType(64))
        neh__encse = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='string_array_to_info')
        return builder.call(knp__kkp, [maz__jyrqh.n_arrays, sijve__iged,
            data, fwd__fiiy, xjvy__zizy, snmk__knwy.meminfo, neh__encse])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        mynk__kno = arr.data
        fhs__clbd = arr.indices
        sig = array_info_type(arr_type.data)
        qutl__vaaho = array_to_info_codegen(context, builder, sig, (
            mynk__kno,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        yvyg__ppx = array_to_info_codegen(context, builder, sig, (fhs__clbd
            ,), False)
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='dict_str_array_to_info')
        jxwf__qzo = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        rybso__mwfu = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(knp__kkp, [qutl__vaaho, yvyg__ppx, jxwf__qzo,
            rybso__mwfu])
    yresd__cdw = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        uohxd__nkpq = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        vtw__zma = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(vtw__zma, 1, 'C')
        yresd__cdw = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if yresd__cdw:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        length = builder.extract_value(arr.shape, 0)
        nosz__milev = arr_type.dtype
        olaj__qcbl = numba_to_c_type(nosz__milev)
        jjng__poh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), olaj__qcbl))
        if yresd__cdw:
            dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            knp__kkp = cgutils.get_or_insert_function(builder.module,
                dmvpq__qfg, name='categorical_array_to_info')
            return builder.call(knp__kkp, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(jjng__poh),
                uohxd__nkpq, arr.meminfo])
        else:
            dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            knp__kkp = cgutils.get_or_insert_function(builder.module,
                dmvpq__qfg, name='numpy_array_to_info')
            return builder.call(knp__kkp, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(jjng__poh), arr.
                meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        nosz__milev = arr_type.dtype
        hdnab__hiapa = nosz__milev
        if isinstance(arr_type, DecimalArrayType):
            hdnab__hiapa = int128_type
        if arr_type == datetime_date_array_type:
            hdnab__hiapa = types.int64
        hncd__pdzd = context.make_array(types.Array(hdnab__hiapa, 1, 'C'))(
            context, builder, arr.data)
        length = builder.extract_value(hncd__pdzd.shape, 0)
        xmcxt__woi = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        olaj__qcbl = numba_to_c_type(nosz__milev)
        jjng__poh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), olaj__qcbl))
        if isinstance(arr_type, DecimalArrayType):
            dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            knp__kkp = cgutils.get_or_insert_function(builder.module,
                dmvpq__qfg, name='decimal_array_to_info')
            return builder.call(knp__kkp, [length, builder.bitcast(
                hncd__pdzd.data, lir.IntType(8).as_pointer()), builder.load
                (jjng__poh), builder.bitcast(xmcxt__woi.data, lir.IntType(8
                ).as_pointer()), hncd__pdzd.meminfo, xmcxt__woi.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32)])
            knp__kkp = cgutils.get_or_insert_function(builder.module,
                dmvpq__qfg, name='time_array_to_info')
            return builder.call(knp__kkp, [length, builder.bitcast(
                hncd__pdzd.data, lir.IntType(8).as_pointer()), builder.load
                (jjng__poh), builder.bitcast(xmcxt__woi.data, lir.IntType(8
                ).as_pointer()), hncd__pdzd.meminfo, xmcxt__woi.meminfo,
                lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            knp__kkp = cgutils.get_or_insert_function(builder.module,
                dmvpq__qfg, name='nullable_array_to_info')
            return builder.call(knp__kkp, [length, builder.bitcast(
                hncd__pdzd.data, lir.IntType(8).as_pointer()), builder.load
                (jjng__poh), builder.bitcast(xmcxt__woi.data, lir.IntType(8
                ).as_pointer()), hncd__pdzd.meminfo, xmcxt__woi.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        wuncn__dduza = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        xjk__dkq = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        length = builder.extract_value(wuncn__dduza.shape, 0)
        olaj__qcbl = numba_to_c_type(arr_type.arr_type.dtype)
        jjng__poh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), olaj__qcbl))
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='interval_array_to_info')
        return builder.call(knp__kkp, [length, builder.bitcast(wuncn__dduza
            .data, lir.IntType(8).as_pointer()), builder.bitcast(xjk__dkq.
            data, lir.IntType(8).as_pointer()), builder.load(jjng__poh),
            wuncn__dduza.meminfo, xjk__dkq.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    qdkwa__tsaru = cgutils.alloca_once(builder, lir.IntType(64))
    xrxt__sluvo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    euqai__jvji = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    knp__kkp = cgutils.get_or_insert_function(builder.module, dmvpq__qfg,
        name='info_to_numpy_array')
    builder.call(knp__kkp, [in_info, qdkwa__tsaru, xrxt__sluvo, euqai__jvji])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    uxnxd__ytcg = context.get_value_type(types.intp)
    tzbl__feuep = cgutils.pack_array(builder, [builder.load(qdkwa__tsaru)],
        ty=uxnxd__ytcg)
    gay__pfjbj = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    rcgvk__ftk = cgutils.pack_array(builder, [gay__pfjbj], ty=uxnxd__ytcg)
    data = builder.bitcast(builder.load(xrxt__sluvo), context.get_data_type
        (arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=tzbl__feuep,
        strides=rcgvk__ftk, itemsize=gay__pfjbj, meminfo=builder.load(
        euqai__jvji))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    nmqia__qnor = context.make_helper(builder, arr_type)
    dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    knp__kkp = cgutils.get_or_insert_function(builder.module, dmvpq__qfg,
        name='info_to_list_string_array')
    builder.call(knp__kkp, [in_info, nmqia__qnor._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return nmqia__qnor._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    tyeyx__jwt = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        uxx__nnqc = lengths_pos
        uic__mykgc = infos_pos
        qos__zddk, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        ppr__wgg = ArrayItemArrayPayloadType(arr_typ)
        gmve__fwn = context.get_data_type(ppr__wgg)
        tfdg__uaobv = context.get_abi_sizeof(gmve__fwn)
        riobd__yehwm = define_array_item_dtor(context, builder, arr_typ,
            ppr__wgg)
        goj__lwa = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tfdg__uaobv), riobd__yehwm)
        rmji__cgz = context.nrt.meminfo_data(builder, goj__lwa)
        igho__wddam = builder.bitcast(rmji__cgz, gmve__fwn.as_pointer())
        maz__jyrqh = cgutils.create_struct_proxy(ppr__wgg)(context, builder)
        maz__jyrqh.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), uxx__nnqc)
        maz__jyrqh.data = qos__zddk
        aikwx__fzity = builder.load(array_infos_ptr)
        rsz__syp = builder.bitcast(builder.extract_value(aikwx__fzity,
            uic__mykgc), tyeyx__jwt)
        maz__jyrqh.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, rsz__syp)
        noi__hyp = builder.bitcast(builder.extract_value(aikwx__fzity, 
            uic__mykgc + 1), tyeyx__jwt)
        maz__jyrqh.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, noi__hyp)
        builder.store(maz__jyrqh._getvalue(), igho__wddam)
        snmk__knwy = context.make_helper(builder, arr_typ)
        snmk__knwy.meminfo = goj__lwa
        return snmk__knwy._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        iui__olcg = []
        uic__mykgc = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for dvbks__qddn in arr_typ.data:
            qos__zddk, lengths_pos, infos_pos = nested_to_array(context,
                builder, dvbks__qddn, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            iui__olcg.append(qos__zddk)
        ppr__wgg = StructArrayPayloadType(arr_typ.data)
        gmve__fwn = context.get_value_type(ppr__wgg)
        tfdg__uaobv = context.get_abi_sizeof(gmve__fwn)
        riobd__yehwm = define_struct_arr_dtor(context, builder, arr_typ,
            ppr__wgg)
        goj__lwa = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tfdg__uaobv), riobd__yehwm)
        rmji__cgz = context.nrt.meminfo_data(builder, goj__lwa)
        igho__wddam = builder.bitcast(rmji__cgz, gmve__fwn.as_pointer())
        maz__jyrqh = cgutils.create_struct_proxy(ppr__wgg)(context, builder)
        maz__jyrqh.data = cgutils.pack_array(builder, iui__olcg
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, iui__olcg)
        aikwx__fzity = builder.load(array_infos_ptr)
        noi__hyp = builder.bitcast(builder.extract_value(aikwx__fzity,
            uic__mykgc), tyeyx__jwt)
        maz__jyrqh.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, noi__hyp)
        builder.store(maz__jyrqh._getvalue(), igho__wddam)
        yls__rdni = context.make_helper(builder, arr_typ)
        yls__rdni.meminfo = goj__lwa
        return yls__rdni._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        aikwx__fzity = builder.load(array_infos_ptr)
        ufu__fexwh = builder.bitcast(builder.extract_value(aikwx__fzity,
            infos_pos), tyeyx__jwt)
        sjhg__pabj = context.make_helper(builder, arr_typ)
        boyfz__ktvqd = ArrayItemArrayType(char_arr_type)
        snmk__knwy = context.make_helper(builder, boyfz__ktvqd)
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_to_string_array')
        builder.call(knp__kkp, [ufu__fexwh, snmk__knwy._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        sjhg__pabj.data = snmk__knwy._getvalue()
        return sjhg__pabj._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        aikwx__fzity = builder.load(array_infos_ptr)
        ywuq__iwmw = builder.bitcast(builder.extract_value(aikwx__fzity, 
            infos_pos + 1), tyeyx__jwt)
        return _lower_info_to_array_numpy(arr_typ, context, builder, ywuq__iwmw
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        hdnab__hiapa = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            hdnab__hiapa = int128_type
        elif arr_typ == datetime_date_array_type:
            hdnab__hiapa = types.int64
        aikwx__fzity = builder.load(array_infos_ptr)
        noi__hyp = builder.bitcast(builder.extract_value(aikwx__fzity,
            infos_pos), tyeyx__jwt)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, noi__hyp)
        ywuq__iwmw = builder.bitcast(builder.extract_value(aikwx__fzity, 
            infos_pos + 1), tyeyx__jwt)
        arr.data = _lower_info_to_array_numpy(types.Array(hdnab__hiapa, 1,
            'C'), context, builder, ywuq__iwmw)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, qitvt__auz = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(dvbks__qddn) for dvbks__qddn in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(dvbks__qddn) for dvbks__qddn in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            jip__kpnv = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            jip__kpnv = _get_map_arr_data_type(arr_type)
        else:
            jip__kpnv = arr_type
        nes__ugfmc = get_num_arrays(jip__kpnv)
        omtgm__oubsk = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), 0) for qitvt__auz in range(nes__ugfmc)])
        lengths_ptr = cgutils.alloca_once_value(builder, omtgm__oubsk)
        ooka__opn = lir.Constant(lir.IntType(8).as_pointer(), None)
        mgw__abw = cgutils.pack_array(builder, [ooka__opn for qitvt__auz in
            range(get_num_infos(jip__kpnv))])
        array_infos_ptr = cgutils.alloca_once_value(builder, mgw__abw)
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_to_nested_array')
        builder.call(knp__kkp, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, qitvt__auz, qitvt__auz = nested_to_array(context, builder,
            jip__kpnv, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            kave__tlg = context.make_helper(builder, arr_type)
            kave__tlg.data = arr
            context.nrt.incref(builder, jip__kpnv, arr)
            arr = kave__tlg._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, jip__kpnv)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        sjhg__pabj = context.make_helper(builder, arr_type)
        boyfz__ktvqd = ArrayItemArrayType(char_arr_type)
        snmk__knwy = context.make_helper(builder, boyfz__ktvqd)
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_to_string_array')
        builder.call(knp__kkp, [in_info, snmk__knwy._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        sjhg__pabj.data = snmk__knwy._getvalue()
        return sjhg__pabj._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='get_nested_info')
        qutl__vaaho = builder.call(knp__kkp, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        yvyg__ppx = builder.call(knp__kkp, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        phx__dxc = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        phx__dxc.data = info_to_array_codegen(context, builder, sig, (
            qutl__vaaho, context.get_constant_null(arr_type.data)))
        swxbp__goa = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = swxbp__goa(array_info_type, swxbp__goa)
        phx__dxc.indices = info_to_array_codegen(context, builder, sig, (
            yvyg__ppx, context.get_constant_null(swxbp__goa)))
        dmvpq__qfg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='get_has_global_dictionary')
        jxwf__qzo = builder.call(knp__kkp, [in_info])
        phx__dxc.has_global_dictionary = builder.trunc(jxwf__qzo, cgutils.
            bool_t)
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='get_has_deduped_local_dictionary')
        rybso__mwfu = builder.call(knp__kkp, [in_info])
        phx__dxc.has_deduped_local_dictionary = builder.trunc(rybso__mwfu,
            cgutils.bool_t)
        return phx__dxc._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        vtw__zma = get_categories_int_type(arr_type.dtype)
        slfe__xfsyl = types.Array(vtw__zma, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(slfe__xfsyl, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            kbh__qvd = bodo.utils.utils.create_categorical_type(arr_type.
                dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(kbh__qvd))
            int_type = arr_type.dtype.int_type
            wnu__zwlw = arr_type.dtype.data.data
            eml__zzsh = context.get_constant_generic(builder, wnu__zwlw,
                kbh__qvd)
            nosz__milev = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(wnu__zwlw), [eml__zzsh])
        else:
            nosz__milev = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, nosz__milev)
        out_arr.dtype = nosz__milev
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        data = _lower_info_to_array_numpy(arr_type.data_array_type, context,
            builder, in_info)
        arr.data = data
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        hdnab__hiapa = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            hdnab__hiapa = int128_type
        elif arr_type == datetime_date_array_type:
            hdnab__hiapa = types.int64
        eiqkq__kuctv = types.Array(hdnab__hiapa, 1, 'C')
        hncd__pdzd = context.make_array(eiqkq__kuctv)(context, builder)
        ipwc__xfml = types.Array(types.uint8, 1, 'C')
        vdkyb__mzpi = context.make_array(ipwc__xfml)(context, builder)
        qdkwa__tsaru = cgutils.alloca_once(builder, lir.IntType(64))
        iio__iacz = cgutils.alloca_once(builder, lir.IntType(64))
        xrxt__sluvo = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ymiw__tzd = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        euqai__jvji = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xiulg__nab = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_to_nullable_array')
        builder.call(knp__kkp, [in_info, qdkwa__tsaru, iio__iacz,
            xrxt__sluvo, ymiw__tzd, euqai__jvji, xiulg__nab])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        uxnxd__ytcg = context.get_value_type(types.intp)
        tzbl__feuep = cgutils.pack_array(builder, [builder.load(
            qdkwa__tsaru)], ty=uxnxd__ytcg)
        gay__pfjbj = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(hdnab__hiapa)))
        rcgvk__ftk = cgutils.pack_array(builder, [gay__pfjbj], ty=uxnxd__ytcg)
        data = builder.bitcast(builder.load(xrxt__sluvo), context.
            get_data_type(hdnab__hiapa).as_pointer())
        numba.np.arrayobj.populate_array(hncd__pdzd, data=data, shape=
            tzbl__feuep, strides=rcgvk__ftk, itemsize=gay__pfjbj, meminfo=
            builder.load(euqai__jvji))
        arr.data = hncd__pdzd._getvalue()
        tzbl__feuep = cgutils.pack_array(builder, [builder.load(iio__iacz)],
            ty=uxnxd__ytcg)
        gay__pfjbj = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        rcgvk__ftk = cgutils.pack_array(builder, [gay__pfjbj], ty=uxnxd__ytcg)
        data = builder.bitcast(builder.load(ymiw__tzd), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(vdkyb__mzpi, data=data, shape=
            tzbl__feuep, strides=rcgvk__ftk, itemsize=gay__pfjbj, meminfo=
            builder.load(xiulg__nab))
        arr.null_bitmap = vdkyb__mzpi._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        wuncn__dduza = context.make_array(arr_type.arr_type)(context, builder)
        xjk__dkq = context.make_array(arr_type.arr_type)(context, builder)
        qdkwa__tsaru = cgutils.alloca_once(builder, lir.IntType(64))
        wnjn__blyl = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        rtz__urr = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        jzj__ptlk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        rml__heky = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_to_interval_array')
        builder.call(knp__kkp, [in_info, qdkwa__tsaru, wnjn__blyl, rtz__urr,
            jzj__ptlk, rml__heky])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        uxnxd__ytcg = context.get_value_type(types.intp)
        tzbl__feuep = cgutils.pack_array(builder, [builder.load(
            qdkwa__tsaru)], ty=uxnxd__ytcg)
        gay__pfjbj = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        rcgvk__ftk = cgutils.pack_array(builder, [gay__pfjbj], ty=uxnxd__ytcg)
        awicj__twhgl = builder.bitcast(builder.load(wnjn__blyl), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(wuncn__dduza, data=awicj__twhgl,
            shape=tzbl__feuep, strides=rcgvk__ftk, itemsize=gay__pfjbj,
            meminfo=builder.load(jzj__ptlk))
        arr.left = wuncn__dduza._getvalue()
        wbiru__rbrpz = builder.bitcast(builder.load(rtz__urr), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(xjk__dkq, data=wbiru__rbrpz, shape
            =tzbl__feuep, strides=rcgvk__ftk, itemsize=gay__pfjbj, meminfo=
            builder.load(rml__heky))
        arr.right = xjk__dkq._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        length, qitvt__auz = args
        olaj__qcbl = numba_to_c_type(array_type.dtype)
        jjng__poh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), olaj__qcbl))
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='alloc_numpy')
        return builder.call(knp__kkp, [length, builder.load(jjng__poh)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, upa__gwwqo = args
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='alloc_string_array')
        return builder.call(knp__kkp, [length, upa__gwwqo])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    lxjx__hca, = args
    ziu__rvgg = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], lxjx__hca)
    dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer().as_pointer(), lir.IntType(64)])
    knp__kkp = cgutils.get_or_insert_function(builder.module, dmvpq__qfg,
        name='arr_info_list_to_table')
    return builder.call(knp__kkp, [ziu__rvgg.data, ziu__rvgg.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_from_table')
        return builder.call(knp__kkp, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    otr__woxoc = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, acwv__rbzv, qitvt__auz = args
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='info_from_table')
        xwbrh__stdov = cgutils.create_struct_proxy(otr__woxoc)(context, builder
            )
        xwbrh__stdov.parent = cgutils.get_null_value(xwbrh__stdov.parent.type)
        yhqt__ubop = context.make_array(table_idx_arr_t)(context, builder,
            acwv__rbzv)
        jkfkr__rcm = context.get_constant(types.int64, -1)
        bmiyt__ulzj = context.get_constant(types.int64, 0)
        mdv__zwwlg = cgutils.alloca_once_value(builder, bmiyt__ulzj)
        for t, ncdng__bwrrc in otr__woxoc.type_to_blk.items():
            eghti__vley = context.get_constant(types.int64, len(otr__woxoc.
                block_to_arr_ind[ncdng__bwrrc]))
            qitvt__auz, fov__uiq = ListInstance.allocate_ex(context,
                builder, types.List(t), eghti__vley)
            fov__uiq.size = eghti__vley
            ixkh__sirr = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(otr__woxoc.block_to_arr_ind[
                ncdng__bwrrc], dtype=np.int64))
            dncto__maamf = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, ixkh__sirr)
            with cgutils.for_range(builder, eghti__vley) as yuhr__svpy:
                qlh__llmo = yuhr__svpy.index
                ppo__odzct = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    dncto__maamf, qlh__llmo)
                rnc__qsyhp = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, yhqt__ubop, ppo__odzct)
                rvs__sdjk = builder.icmp_unsigned('!=', rnc__qsyhp, jkfkr__rcm)
                with builder.if_else(rvs__sdjk) as (lgbue__zght, xelh__enzt):
                    with lgbue__zght:
                        dip__dri = builder.call(knp__kkp, [cpp_table,
                            rnc__qsyhp])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            dip__dri])
                        fov__uiq.inititem(qlh__llmo, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, mdv__zwwlg)
                    with xelh__enzt:
                        pnkm__phe = context.get_constant_null(t)
                        fov__uiq.inititem(qlh__llmo, pnkm__phe, incref=False)
            setattr(xwbrh__stdov, f'block_{ncdng__bwrrc}', fov__uiq.value)
        xwbrh__stdov.len = builder.load(mdv__zwwlg)
        return xwbrh__stdov._getvalue()
    return otr__woxoc(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    nfq__ldnz = out_col_inds_t.instance_type.meta
    otr__woxoc = unwrap_typeref(out_types_t.types[0])
    dutat__ibhu = [unwrap_typeref(out_types_t.types[qlh__llmo]) for
        qlh__llmo in range(1, len(out_types_t.types))]
    opqkl__pqs = {}
    qar__qujjh = get_overload_const_int(n_table_cols_t)
    jga__sgvz = {vsja__tmt: qlh__llmo for qlh__llmo, vsja__tmt in enumerate
        (nfq__ldnz)}
    if not is_overload_none(unknown_cat_arrs_t):
        jpk__ankov = {yibx__lyjow: qlh__llmo for qlh__llmo, yibx__lyjow in
            enumerate(cat_inds_t.instance_type.meta)}
    ehzc__ouva = []
    def__iotrz = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(otr__woxoc, bodo.TableType):
        def__iotrz += f'  py_table = init_table(py_table_type, False)\n'
        def__iotrz += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for vpzh__vaeee, ncdng__bwrrc in otr__woxoc.type_to_blk.items():
            etlxp__fuhzu = [jga__sgvz.get(qlh__llmo, -1) for qlh__llmo in
                otr__woxoc.block_to_arr_ind[ncdng__bwrrc]]
            opqkl__pqs[f'out_inds_{ncdng__bwrrc}'] = np.array(etlxp__fuhzu,
                np.int64)
            opqkl__pqs[f'out_type_{ncdng__bwrrc}'] = vpzh__vaeee
            opqkl__pqs[f'typ_list_{ncdng__bwrrc}'] = types.List(vpzh__vaeee)
            ibbdb__xva = f'out_type_{ncdng__bwrrc}'
            if type_has_unknown_cats(vpzh__vaeee):
                if is_overload_none(unknown_cat_arrs_t):
                    def__iotrz += f"""  in_arr_list_{ncdng__bwrrc} = get_table_block(out_types_t[0], {ncdng__bwrrc})
"""
                    ibbdb__xva = f'in_arr_list_{ncdng__bwrrc}[i]'
                else:
                    opqkl__pqs[f'cat_arr_inds_{ncdng__bwrrc}'] = np.array([
                        jpk__ankov.get(qlh__llmo, -1) for qlh__llmo in
                        otr__woxoc.block_to_arr_ind[ncdng__bwrrc]], np.int64)
                    ibbdb__xva = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{ncdng__bwrrc}[i]]')
            eghti__vley = len(otr__woxoc.block_to_arr_ind[ncdng__bwrrc])
            def__iotrz += f"""  arr_list_{ncdng__bwrrc} = alloc_list_like(typ_list_{ncdng__bwrrc}, {eghti__vley}, False)
"""
            def__iotrz += f'  for i in range(len(arr_list_{ncdng__bwrrc})):\n'
            def__iotrz += (
                f'    cpp_ind_{ncdng__bwrrc} = out_inds_{ncdng__bwrrc}[i]\n')
            def__iotrz += f'    if cpp_ind_{ncdng__bwrrc} == -1:\n'
            def__iotrz += f'      continue\n'
            def__iotrz += f"""    arr_{ncdng__bwrrc} = info_to_array(info_from_table(cpp_table, cpp_ind_{ncdng__bwrrc}), {ibbdb__xva})
"""
            def__iotrz += (
                f'    arr_list_{ncdng__bwrrc}[i] = arr_{ncdng__bwrrc}\n')
            def__iotrz += f"""  py_table = set_table_block(py_table, arr_list_{ncdng__bwrrc}, {ncdng__bwrrc})
"""
        ehzc__ouva.append('py_table')
    elif otr__woxoc != types.none:
        pzlb__edrod = jga__sgvz.get(0, -1)
        if pzlb__edrod != -1:
            opqkl__pqs[f'arr_typ_arg0'] = otr__woxoc
            ibbdb__xva = f'arr_typ_arg0'
            if type_has_unknown_cats(otr__woxoc):
                if is_overload_none(unknown_cat_arrs_t):
                    ibbdb__xva = f'out_types_t[0]'
                else:
                    ibbdb__xva = f'unknown_cat_arrs_t[{jpk__ankov[0]}]'
            def__iotrz += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {pzlb__edrod}), {ibbdb__xva})
"""
            ehzc__ouva.append('out_arg0')
    for qlh__llmo, t in enumerate(dutat__ibhu):
        pzlb__edrod = jga__sgvz.get(qar__qujjh + qlh__llmo, -1)
        if pzlb__edrod != -1:
            opqkl__pqs[f'extra_arr_type_{qlh__llmo}'] = t
            ibbdb__xva = f'extra_arr_type_{qlh__llmo}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    ibbdb__xva = f'out_types_t[{qlh__llmo + 1}]'
                else:
                    ibbdb__xva = (
                        f'unknown_cat_arrs_t[{jpk__ankov[qar__qujjh + qlh__llmo]}]'
                        )
            def__iotrz += f"""  out_{qlh__llmo} = info_to_array(info_from_table(cpp_table, {pzlb__edrod}), {ibbdb__xva})
"""
            ehzc__ouva.append(f'out_{qlh__llmo}')
    fhv__ddix = ',' if len(ehzc__ouva) == 1 else ''
    def__iotrz += f"  return ({', '.join(ehzc__ouva)}{fhv__ddix})\n"
    opqkl__pqs.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(nfq__ldnz), 'py_table_type': otr__woxoc})
    ipxes__fxvx = {}
    exec(def__iotrz, opqkl__pqs, ipxes__fxvx)
    return ipxes__fxvx['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    otr__woxoc = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, qitvt__auz = args
        tzobw__ycuij = cgutils.create_struct_proxy(otr__woxoc)(context,
            builder, py_table)
        if otr__woxoc.has_runtime_cols:
            jbd__cpha = lir.Constant(lir.IntType(64), 0)
            for ncdng__bwrrc, t in enumerate(otr__woxoc.arr_types):
                kdv__svi = getattr(tzobw__ycuij, f'block_{ncdng__bwrrc}')
                vmjsw__pcel = ListInstance(context, builder, types.List(t),
                    kdv__svi)
                jbd__cpha = builder.add(jbd__cpha, vmjsw__pcel.size)
        else:
            jbd__cpha = lir.Constant(lir.IntType(64), len(otr__woxoc.arr_types)
                )
        qitvt__auz, brfn__adgaa = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), jbd__cpha)
        brfn__adgaa.size = jbd__cpha
        if otr__woxoc.has_runtime_cols:
            ybg__gvp = lir.Constant(lir.IntType(64), 0)
            for ncdng__bwrrc, t in enumerate(otr__woxoc.arr_types):
                kdv__svi = getattr(tzobw__ycuij, f'block_{ncdng__bwrrc}')
                vmjsw__pcel = ListInstance(context, builder, types.List(t),
                    kdv__svi)
                eghti__vley = vmjsw__pcel.size
                with cgutils.for_range(builder, eghti__vley) as yuhr__svpy:
                    qlh__llmo = yuhr__svpy.index
                    arr = vmjsw__pcel.getitem(qlh__llmo)
                    sbvwp__qtxr = signature(array_info_type, t)
                    tmols__kwbl = arr,
                    woach__tawv = array_to_info_codegen(context, builder,
                        sbvwp__qtxr, tmols__kwbl)
                    brfn__adgaa.inititem(builder.add(ybg__gvp, qlh__llmo),
                        woach__tawv, incref=False)
                ybg__gvp = builder.add(ybg__gvp, eghti__vley)
        else:
            for t, ncdng__bwrrc in otr__woxoc.type_to_blk.items():
                eghti__vley = context.get_constant(types.int64, len(
                    otr__woxoc.block_to_arr_ind[ncdng__bwrrc]))
                kdv__svi = getattr(tzobw__ycuij, f'block_{ncdng__bwrrc}')
                vmjsw__pcel = ListInstance(context, builder, types.List(t),
                    kdv__svi)
                ixkh__sirr = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(otr__woxoc.
                    block_to_arr_ind[ncdng__bwrrc], dtype=np.int64))
                dncto__maamf = context.make_array(types.Array(types.int64, 
                    1, 'C'))(context, builder, ixkh__sirr)
                with cgutils.for_range(builder, eghti__vley) as yuhr__svpy:
                    qlh__llmo = yuhr__svpy.index
                    ppo__odzct = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        dncto__maamf, qlh__llmo)
                    kftx__rudt = signature(types.none, otr__woxoc, types.
                        List(t), types.int64, types.int64)
                    wurxg__pdc = py_table, kdv__svi, qlh__llmo, ppo__odzct
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, kftx__rudt, wurxg__pdc)
                    arr = vmjsw__pcel.getitem(qlh__llmo)
                    sbvwp__qtxr = signature(array_info_type, t)
                    tmols__kwbl = arr,
                    woach__tawv = array_to_info_codegen(context, builder,
                        sbvwp__qtxr, tmols__kwbl)
                    brfn__adgaa.inititem(ppo__odzct, woach__tawv, incref=False)
        gzj__qjia = brfn__adgaa.value
        ebu__aljv = signature(table_type, types.List(array_info_type))
        tdsli__vukk = gzj__qjia,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            ebu__aljv, tdsli__vukk)
        context.nrt.decref(builder, types.List(array_info_type), gzj__qjia)
        return cpp_table
    return table_type(otr__woxoc, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    maton__lwdzj = in_col_inds_t.instance_type.meta
    opqkl__pqs = {}
    qar__qujjh = get_overload_const_int(n_table_cols_t)
    nxi__mgei = defaultdict(list)
    jga__sgvz = {}
    for qlh__llmo, vsja__tmt in enumerate(maton__lwdzj):
        if vsja__tmt in jga__sgvz:
            nxi__mgei[vsja__tmt].append(qlh__llmo)
        else:
            jga__sgvz[vsja__tmt] = qlh__llmo
    def__iotrz = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    def__iotrz += (
        f'  cpp_arr_list = alloc_empty_list_type({len(maton__lwdzj)}, array_info_type)\n'
        )
    if py_table != types.none:
        for ncdng__bwrrc in py_table.type_to_blk.values():
            etlxp__fuhzu = [jga__sgvz.get(qlh__llmo, -1) for qlh__llmo in
                py_table.block_to_arr_ind[ncdng__bwrrc]]
            opqkl__pqs[f'out_inds_{ncdng__bwrrc}'] = np.array(etlxp__fuhzu,
                np.int64)
            opqkl__pqs[f'arr_inds_{ncdng__bwrrc}'] = np.array(py_table.
                block_to_arr_ind[ncdng__bwrrc], np.int64)
            def__iotrz += (
                f'  arr_list_{ncdng__bwrrc} = get_table_block(py_table, {ncdng__bwrrc})\n'
                )
            def__iotrz += f'  for i in range(len(arr_list_{ncdng__bwrrc})):\n'
            def__iotrz += (
                f'    out_arr_ind_{ncdng__bwrrc} = out_inds_{ncdng__bwrrc}[i]\n'
                )
            def__iotrz += f'    if out_arr_ind_{ncdng__bwrrc} == -1:\n'
            def__iotrz += f'      continue\n'
            def__iotrz += (
                f'    arr_ind_{ncdng__bwrrc} = arr_inds_{ncdng__bwrrc}[i]\n')
            def__iotrz += f"""    ensure_column_unboxed(py_table, arr_list_{ncdng__bwrrc}, i, arr_ind_{ncdng__bwrrc})
"""
            def__iotrz += f"""    cpp_arr_list[out_arr_ind_{ncdng__bwrrc}] = array_to_info(arr_list_{ncdng__bwrrc}[i])
"""
        for hux__whf, wahoh__mkp in nxi__mgei.items():
            if hux__whf < qar__qujjh:
                ncdng__bwrrc = py_table.block_nums[hux__whf]
                znvco__auiw = py_table.block_offsets[hux__whf]
                for pzlb__edrod in wahoh__mkp:
                    def__iotrz += f"""  cpp_arr_list[{pzlb__edrod}] = array_to_info(arr_list_{ncdng__bwrrc}[{znvco__auiw}])
"""
    for qlh__llmo in range(len(extra_arrs_tup)):
        efvn__zenyu = jga__sgvz.get(qar__qujjh + qlh__llmo, -1)
        if efvn__zenyu != -1:
            btg__qze = [efvn__zenyu] + nxi__mgei.get(qar__qujjh + qlh__llmo, []
                )
            for pzlb__edrod in btg__qze:
                def__iotrz += f"""  cpp_arr_list[{pzlb__edrod}] = array_to_info(extra_arrs_tup[{qlh__llmo}])
"""
    def__iotrz += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    opqkl__pqs.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    ipxes__fxvx = {}
    exec(def__iotrz, opqkl__pqs, ipxes__fxvx)
    return ipxes__fxvx['impl']


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))
decref_table_array = types.ExternalFunction('decref_table_array', types.
    void(table_type, types.int32))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='delete_table')
        builder.call(knp__kkp, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='shuffle_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        dmvpq__qfg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='delete_shuffle_info')
        return builder.call(knp__kkp, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='reverse_shuffle_table')
        return builder.call(knp__kkp, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    key_in_out_t, same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    extra_data_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='hash_join_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.int64, types.voidptr, types.int64, types.voidptr
        ), codegen


@intrinsic
def cross_join_table(typingctx, left_table_t, right_table_t,
    left_parallel_t, right_parallel_t, is_left_t, is_right_t,
    key_in_output_t, need_typechange_t, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type, 'cross_join_table: cpp table type expected'
    assert right_table_t == table_type, 'cross_join_table: cpp table type expected'

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='cross_join_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return woexm__xdgxr
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='sort_values_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='sample_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='shuffle_renormalization')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='shuffle_renormalization_group')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='drop_duplicates_table')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb,
    udf_table_dummy_t, n_out_rows_t, n_shuffle_keys_t):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        knp__kkp = cgutils.get_or_insert_function(builder.module,
            dmvpq__qfg, name='groupby_and_aggregate')
        woexm__xdgxr = builder.call(knp__kkp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return woexm__xdgxr
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t, types.voidptr, types.int64), codegen


_drop_duplicates_local_dictionary = types.ExternalFunction(
    'drop_duplicates_local_dictionary', types.void(array_info_type, types.
    bool_))


@numba.njit(no_cpython_wrapper=True)
def drop_duplicates_local_dictionary(dict_arr, sort_dictionary):
    qad__qjgy = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(qad__qjgy, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(qad__qjgy, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    qad__qjgy = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(qad__qjgy, is_parallel, sort_dictionary
        )
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(qad__qjgy, bodo.dict_str_arr_type)
    return out_arr


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    grocf__uiuut = array_to_info(in_arr)
    oqyz__vxsc = array_to_info(in_values)
    uss__nyk = array_to_info(out_arr)
    dvayc__stni = arr_info_list_to_table([grocf__uiuut, oqyz__vxsc, uss__nyk])
    _array_isin(uss__nyk, grocf__uiuut, oqyz__vxsc, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(dvayc__stni)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    grocf__uiuut = array_to_info(in_arr)
    uss__nyk = array_to_info(out_arr)
    _get_search_regex(grocf__uiuut, case, match, pat, uss__nyk)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    gwvzl__wccs = col_array_typ.dtype
    if isinstance(gwvzl__wccs, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or gwvzl__wccs in [bodo
        .datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(gwvzl__wccs, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            gwvzl__wccs = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                xwbrh__stdov, halxc__rfqvp = args
                xwbrh__stdov = builder.bitcast(xwbrh__stdov, lir.IntType(8)
                    .as_pointer().as_pointer())
                hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                bbflt__huyaw = builder.load(builder.gep(xwbrh__stdov, [
                    hdzpa__uso]))
                bbflt__huyaw = builder.bitcast(bbflt__huyaw, context.
                    get_data_type(gwvzl__wccs).as_pointer())
                return context.unpack_value(builder, gwvzl__wccs, builder.
                    gep(bbflt__huyaw, [halxc__rfqvp]))
            return gwvzl__wccs(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                xwbrh__stdov, halxc__rfqvp = args
                xwbrh__stdov = builder.bitcast(xwbrh__stdov, lir.IntType(8)
                    .as_pointer().as_pointer())
                hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                bbflt__huyaw = builder.load(builder.gep(xwbrh__stdov, [
                    hdzpa__uso]))
                dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                puh__fkzf = cgutils.get_or_insert_function(builder.module,
                    dmvpq__qfg, name='array_info_getitem')
                pxrj__iksfm = cgutils.alloca_once(builder, lir.IntType(64))
                args = bbflt__huyaw, halxc__rfqvp, pxrj__iksfm
                xrxt__sluvo = builder.call(puh__fkzf, args)
                drm__cvckr = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    drm__cvckr, [xrxt__sluvo, builder.load(pxrj__iksfm)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                kdp__rtrli = lir.Constant(lir.IntType(64), 1)
                zsq__hvdmw = lir.Constant(lir.IntType(64), 2)
                xwbrh__stdov, halxc__rfqvp = args
                xwbrh__stdov = builder.bitcast(xwbrh__stdov, lir.IntType(8)
                    .as_pointer().as_pointer())
                hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                bbflt__huyaw = builder.load(builder.gep(xwbrh__stdov, [
                    hdzpa__uso]))
                dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                aveym__jzw = cgutils.get_or_insert_function(builder.module,
                    dmvpq__qfg, name='get_nested_info')
                args = bbflt__huyaw, zsq__hvdmw
                jlaxe__svz = builder.call(aveym__jzw, args)
                dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                iiz__hjn = cgutils.get_or_insert_function(builder.module,
                    dmvpq__qfg, name='array_info_getdata1')
                args = jlaxe__svz,
                giji__oylph = builder.call(iiz__hjn, args)
                giji__oylph = builder.bitcast(giji__oylph, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                msc__kklys = builder.sext(builder.load(builder.gep(
                    giji__oylph, [halxc__rfqvp])), lir.IntType(64))
                args = bbflt__huyaw, kdp__rtrli
                odtd__nshun = builder.call(aveym__jzw, args)
                dmvpq__qfg = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                puh__fkzf = cgutils.get_or_insert_function(builder.module,
                    dmvpq__qfg, name='array_info_getitem')
                pxrj__iksfm = cgutils.alloca_once(builder, lir.IntType(64))
                args = odtd__nshun, msc__kklys, pxrj__iksfm
                xrxt__sluvo = builder.call(puh__fkzf, args)
                drm__cvckr = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    drm__cvckr, [xrxt__sluvo, builder.load(pxrj__iksfm)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{gwvzl__wccs}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                bob__sivx, halxc__rfqvp = args
                bob__sivx = builder.bitcast(bob__sivx, lir.IntType(8).
                    as_pointer().as_pointer())
                hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                bbflt__huyaw = builder.load(builder.gep(bob__sivx, [
                    hdzpa__uso]))
                xjvy__zizy = builder.bitcast(bbflt__huyaw, context.
                    get_data_type(types.bool_).as_pointer())
                xiqx__ire = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    xjvy__zizy, halxc__rfqvp)
                mcpvr__dby = builder.icmp_unsigned('!=', xiqx__ire, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(mcpvr__dby, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        gwvzl__wccs = col_array_dtype.dtype
        if gwvzl__wccs in [bodo.datetime64ns, bodo.timedelta64ns
            ] or isinstance(gwvzl__wccs, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            if isinstance(gwvzl__wccs, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                gwvzl__wccs = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    xwbrh__stdov, halxc__rfqvp = args
                    xwbrh__stdov = builder.bitcast(xwbrh__stdov, lir.
                        IntType(8).as_pointer().as_pointer())
                    hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                    bbflt__huyaw = builder.load(builder.gep(xwbrh__stdov, [
                        hdzpa__uso]))
                    bbflt__huyaw = builder.bitcast(bbflt__huyaw, context.
                        get_data_type(gwvzl__wccs).as_pointer())
                    ajkgf__qseb = builder.load(builder.gep(bbflt__huyaw, [
                        halxc__rfqvp]))
                    mcpvr__dby = builder.icmp_unsigned('!=', ajkgf__qseb,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(mcpvr__dby, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(gwvzl__wccs, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    xwbrh__stdov, halxc__rfqvp = args
                    xwbrh__stdov = builder.bitcast(xwbrh__stdov, lir.
                        IntType(8).as_pointer().as_pointer())
                    hdzpa__uso = lir.Constant(lir.IntType(64), c_ind)
                    bbflt__huyaw = builder.load(builder.gep(xwbrh__stdov, [
                        hdzpa__uso]))
                    bbflt__huyaw = builder.bitcast(bbflt__huyaw, context.
                        get_data_type(gwvzl__wccs).as_pointer())
                    ajkgf__qseb = builder.load(builder.gep(bbflt__huyaw, [
                        halxc__rfqvp]))
                    nogmv__paxbi = signature(types.bool_, gwvzl__wccs)
                    xiqx__ire = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, nogmv__paxbi, (ajkgf__qseb,))
                    return builder.not_(builder.sext(xiqx__ire, lir.IntType(8))
                        )
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
