"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array, string_array_type
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == string_array_type:
            return string_array_type


dict_str_arr_type = DictionaryArrayType(string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yio__mtae = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, yio__mtae)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
make_attribute_wrapper(DictionaryArrayType, 'has_deduped_local_dictionary',
    '_has_deduped_local_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t, unique_dict_t):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        ynne__mjoqo, tqri__kuxev, gihc__vxcy, arskj__cthd = args
        iaf__komjj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        iaf__komjj.data = ynne__mjoqo
        iaf__komjj.indices = tqri__kuxev
        iaf__komjj.has_global_dictionary = gihc__vxcy
        iaf__komjj.has_deduped_local_dictionary = arskj__cthd
        context.nrt.incref(builder, signature.args[0], ynne__mjoqo)
        context.nrt.incref(builder, signature.args[1], tqri__kuxev)
        return iaf__komjj._getvalue()
    oplf__hzn = DictionaryArrayType(data_t)
    qxi__nomr = oplf__hzn(data_t, indices_t, types.bool_, types.bool_)
    return qxi__nomr, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    if isinstance(A, pd.arrays.ArrowStringArray) and pa.types.is_dictionary(A
        ._data.type) and (pa.types.is_string(A._data.type.value_type) or pa
        .types.is_large_string(A._data.type.value_type)) and pa.types.is_int32(
        A._data.type.index_type):
        return A._data.combine_chunks()
    return pd.array(A, 'string[pyarrow]')._data.combine_chunks(
        ).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    wpnnp__gwj = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(wpnnp__gwj, [val])
    c.pyapi.decref(wpnnp__gwj)
    iaf__komjj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zgh__cuzd = c.pyapi.object_getattr_string(val, 'dictionary')
    devir__eimyn = c.pyapi.bool_from_bool(c.context.get_constant(types.
        bool_, False))
    kelfn__dxwr = c.pyapi.call_method(zgh__cuzd, 'to_numpy', (devir__eimyn,))
    iaf__komjj.data = c.unbox(typ.data, kelfn__dxwr).value
    xawov__uoijc = c.pyapi.object_getattr_string(val, 'indices')
    utec__yqo = c.context.insert_const_string(c.builder.module, 'pandas')
    grzc__uzb = c.pyapi.import_module_noblock(utec__yqo)
    sau__osx = c.pyapi.string_from_constant_string('Int32')
    hqkq__lonow = c.pyapi.call_method(grzc__uzb, 'array', (xawov__uoijc,
        sau__osx))
    iaf__komjj.indices = c.unbox(dict_indices_arr_type, hqkq__lonow).value
    iaf__komjj.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    iaf__komjj.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(zgh__cuzd)
    c.pyapi.decref(devir__eimyn)
    c.pyapi.decref(kelfn__dxwr)
    c.pyapi.decref(xawov__uoijc)
    c.pyapi.decref(grzc__uzb)
    c.pyapi.decref(sau__osx)
    c.pyapi.decref(hqkq__lonow)
    c.pyapi.decref(val)
    cqktv__xkhy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(iaf__komjj._getvalue(), is_error=cqktv__xkhy)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    iaf__komjj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            hujwi__tes = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            dpdyv__uho = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            kzdcf__smla = 'pd_pyarrow_array_from_string_array'
            onswl__bubg = cgutils.get_or_insert_function(c.builder.module,
                dpdyv__uho, name=kzdcf__smla)
            arr = c.builder.call(onswl__bubg, [hujwi__tes])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, iaf__komjj.data)
        wej__tmnws = c.box(typ.data, iaf__komjj.data)
        rzbsa__hlf = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, iaf__komjj.indices)
        dpdyv__uho = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        onswl__bubg = cgutils.get_or_insert_function(c.builder.module,
            dpdyv__uho, name='box_dict_str_array')
        xpwsb__rdkb = cgutils.create_struct_proxy(types.Array(types.int32, 
            1, 'C'))(c.context, c.builder, rzbsa__hlf.data)
        aqqq__dysj = c.builder.extract_value(xpwsb__rdkb.shape, 0)
        sumha__hjnb = xpwsb__rdkb.data
        bsyud__fxml = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, rzbsa__hlf.null_bitmap).data
        kelfn__dxwr = c.builder.call(onswl__bubg, [aqqq__dysj, wej__tmnws,
            sumha__hjnb, bsyud__fxml])
        c.pyapi.decref(wej__tmnws)
    else:
        utec__yqo = c.context.insert_const_string(c.builder.module, 'pyarrow')
        noon__hbcaw = c.pyapi.import_module_noblock(utec__yqo)
        hla__ruxen = c.pyapi.object_getattr_string(noon__hbcaw,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, iaf__komjj.data)
        wej__tmnws = c.box(typ.data, iaf__komjj.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, iaf__komjj.
            indices)
        xawov__uoijc = c.box(dict_indices_arr_type, iaf__komjj.indices)
        sge__inmqv = c.pyapi.call_method(hla__ruxen, 'from_arrays', (
            xawov__uoijc, wej__tmnws))
        devir__eimyn = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        kelfn__dxwr = c.pyapi.call_method(sge__inmqv, 'to_numpy', (
            devir__eimyn,))
        c.pyapi.decref(noon__hbcaw)
        c.pyapi.decref(wej__tmnws)
        c.pyapi.decref(xawov__uoijc)
        c.pyapi.decref(hla__ruxen)
        c.pyapi.decref(sge__inmqv)
        c.pyapi.decref(devir__eimyn)
    c.context.nrt.decref(c.builder, typ, val)
    return kelfn__dxwr


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary, A._has_deduped_local_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    xkydm__cpfqf = pyval.dictionary.to_numpy(False)
    zctxr__xffbo = pd.array(pyval.indices, 'Int32')
    xkydm__cpfqf = context.get_constant_generic(builder, typ.data, xkydm__cpfqf
        )
    zctxr__xffbo = context.get_constant_generic(builder,
        dict_indices_arr_type, zctxr__xffbo)
    uuxe__dyw = context.get_constant(types.bool_, False)
    thnkt__dlaq = context.get_constant(types.bool_, False)
    ylfwh__jih = lir.Constant.literal_struct([xkydm__cpfqf, zctxr__xffbo,
        uuxe__dyw, thnkt__dlaq])
    return ylfwh__jih


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            hyzxh__ilc = A._indices[ind]
            return A._data[hyzxh__ilc]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        ynne__mjoqo = A._data
        tqri__kuxev = A._indices
        aqqq__dysj = len(tqri__kuxev)
        zjaz__erq = [get_str_arr_item_length(ynne__mjoqo, i) for i in range
            (len(ynne__mjoqo))]
        ybyuk__vzm = 0
        for i in range(aqqq__dysj):
            if not bodo.libs.array_kernels.isna(tqri__kuxev, i):
                ybyuk__vzm += zjaz__erq[tqri__kuxev[i]]
        oozkw__hnahb = pre_alloc_string_array(aqqq__dysj, ybyuk__vzm)
        for i in range(aqqq__dysj):
            if bodo.libs.array_kernels.isna(tqri__kuxev, i):
                bodo.libs.array_kernels.setna(oozkw__hnahb, i)
                continue
            ind = tqri__kuxev[i]
            if bodo.libs.array_kernels.isna(ynne__mjoqo, ind):
                bodo.libs.array_kernels.setna(oozkw__hnahb, i)
                continue
            oozkw__hnahb[i] = ynne__mjoqo[ind]
        return oozkw__hnahb
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    hyzxh__ilc = -1
    ynne__mjoqo = arr._data
    for i in range(len(ynne__mjoqo)):
        if bodo.libs.array_kernels.isna(ynne__mjoqo, i):
            continue
        if ynne__mjoqo[i] == val:
            hyzxh__ilc = i
            break
    return hyzxh__ilc


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    yzfd__nknl = set()
    ynne__mjoqo = arr._data
    for i in range(len(ynne__mjoqo)):
        if bodo.libs.array_kernels.isna(ynne__mjoqo, i):
            continue
        if ynne__mjoqo[i] == val:
            yzfd__nknl.add(i)
    return yzfd__nknl


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    aqqq__dysj = len(arr)
    if arr._has_deduped_local_dictionary:
        hyzxh__ilc = find_dict_ind_unique(arr, val)
        if hyzxh__ilc == -1:
            return init_bool_array(np.full(aqqq__dysj, False, np.bool_),
                arr._indices._null_bitmap.copy())
        return arr._indices == hyzxh__ilc
    else:
        vsp__tbfoq = find_dict_ind_non_unique(arr, val)
        if len(vsp__tbfoq) == 0:
            return init_bool_array(np.full(aqqq__dysj, False, np.bool_),
                arr._indices._null_bitmap.copy())
        ecjib__xlro = np.empty(aqqq__dysj, dtype=np.bool_)
        for i in range(len(arr._indices)):
            ecjib__xlro[i] = arr._indices[i] in vsp__tbfoq
        return init_bool_array(ecjib__xlro, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    aqqq__dysj = len(arr)
    if arr._has_deduped_local_dictionary:
        hyzxh__ilc = find_dict_ind_unique(arr, val)
        if hyzxh__ilc == -1:
            return init_bool_array(np.full(aqqq__dysj, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        return arr._indices != hyzxh__ilc
    else:
        vsp__tbfoq = find_dict_ind_non_unique(arr, val)
        if len(vsp__tbfoq) == 0:
            return init_bool_array(np.full(aqqq__dysj, True, np.bool_), arr
                ._indices._null_bitmap.copy())
        ecjib__xlro = np.empty(aqqq__dysj, dtype=np.bool_)
        for i in range(len(arr._indices)):
            ecjib__xlro[i] = arr._indices[i] not in vsp__tbfoq
        return init_bool_array(ecjib__xlro, arr._indices._null_bitmap.copy())


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(rhs, lhs
                )
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(rhs, lhs
                )


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        lxj__ard = arr._data
        miuy__tymbd = bodo.libs.int_arr_ext.alloc_int_array(len(lxj__ard),
            dtype)
        for eed__lwrxx in range(len(lxj__ard)):
            if bodo.libs.array_kernels.isna(lxj__ard, eed__lwrxx):
                bodo.libs.array_kernels.setna(miuy__tymbd, eed__lwrxx)
                continue
            miuy__tymbd[eed__lwrxx] = np.int64(lxj__ard[eed__lwrxx])
        aqqq__dysj = len(arr)
        tqri__kuxev = arr._indices
        oozkw__hnahb = bodo.libs.int_arr_ext.alloc_int_array(aqqq__dysj, dtype)
        for i in range(aqqq__dysj):
            if bodo.libs.array_kernels.isna(tqri__kuxev, i):
                bodo.libs.array_kernels.setna(oozkw__hnahb, i)
                continue
            oozkw__hnahb[i] = miuy__tymbd[tqri__kuxev[i]]
        return oozkw__hnahb
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    ixotb__amvcc = len(arrs)
    hwk__eftks = 'def impl(arrs, sep):\n'
    hwk__eftks += '  ind_map = {}\n'
    hwk__eftks += '  out_strs = []\n'
    hwk__eftks += '  n = len(arrs[0])\n'
    for i in range(ixotb__amvcc):
        hwk__eftks += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(ixotb__amvcc):
        hwk__eftks += f'  data{i} = arrs[{i}]._data\n'
    hwk__eftks += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    hwk__eftks += '  for i in range(n):\n'
    fgjja__iczoz = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for i in range(
        ixotb__amvcc)])
    hwk__eftks += f'    if {fgjja__iczoz}:\n'
    hwk__eftks += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    hwk__eftks += '      continue\n'
    for i in range(ixotb__amvcc):
        hwk__eftks += f'    ind{i} = indices{i}[i]\n'
    hhog__iqjhe = '(' + ', '.join(f'ind{i}' for i in range(ixotb__amvcc)) + ')'
    hwk__eftks += f'    if {hhog__iqjhe} not in ind_map:\n'
    hwk__eftks += '      out_ind = len(out_strs)\n'
    hwk__eftks += f'      ind_map[{hhog__iqjhe}] = out_ind\n'
    xjli__irwk = "''" if is_overload_none(sep) else 'sep'
    wcvs__dgpm = ', '.join([f'data{i}[ind{i}]' for i in range(ixotb__amvcc)])
    hwk__eftks += f'      v = {xjli__irwk}.join([{wcvs__dgpm}])\n'
    hwk__eftks += '      out_strs.append(v)\n'
    hwk__eftks += '    else:\n'
    hwk__eftks += f'      out_ind = ind_map[{hhog__iqjhe}]\n'
    hwk__eftks += '    out_indices[i] = out_ind\n'
    hwk__eftks += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    hwk__eftks += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    qtao__zld = {}
    exec(hwk__eftks, {'bodo': bodo, 'numba': numba, 'np': np}, qtao__zld)
    impl = qtao__zld['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    ueq__flpf = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    qxi__nomr = toty(fromty)
    imeqx__xirt = context.compile_internal(builder, ueq__flpf, qxi__nomr, (
        val,))
    return impl_ret_new_ref(context, builder, toty, imeqx__xirt)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    iaf__komjj = arr._data
    dict_arr_out = pd.to_numeric(iaf__komjj, errors, downcast)
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.utils.utils.alloc_type(zho__alzc, dict_arr_out, (-1,))
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
            continue
        hyzxh__ilc = zctxr__xffbo[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, hyzxh__ilc):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
            continue
        oozkw__hnahb[i] = dict_arr_out[hyzxh__ilc]
    return oozkw__hnahb


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    xkydm__cpfqf = arr._data
    vcel__jai = len(xkydm__cpfqf)
    iigq__roa = pre_alloc_string_array(vcel__jai, -1)
    if regex:
        hbp__wos = re.compile(pat, flags)
        for i in range(vcel__jai):
            if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
                bodo.libs.array_kernels.setna(iigq__roa, i)
                continue
            iigq__roa[i] = hbp__wos.sub(repl=repl, string=xkydm__cpfqf[i])
    else:
        for i in range(vcel__jai):
            if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
                bodo.libs.array_kernels.setna(iigq__roa, i)
                continue
            iigq__roa[i] = xkydm__cpfqf[i].replace(pat, repl)
    return init_dict_arr(iigq__roa, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    iaf__komjj = arr._data
    jjlru__dljck = len(iaf__komjj)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(jjlru__dljck)
    for i in range(jjlru__dljck):
        dict_arr_out[i] = iaf__komjj[i].startswith(pat)
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.libs.bool_arr_ext.alloc_bool_array(zho__alzc)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = dict_arr_out[zctxr__xffbo[i]]
    return oozkw__hnahb


@register_jitable
def str_endswith(arr, pat, na):
    iaf__komjj = arr._data
    jjlru__dljck = len(iaf__komjj)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(jjlru__dljck)
    for i in range(jjlru__dljck):
        dict_arr_out[i] = iaf__komjj[i].endswith(pat)
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.libs.bool_arr_ext.alloc_bool_array(zho__alzc)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = dict_arr_out[zctxr__xffbo[i]]
    return oozkw__hnahb


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    iaf__komjj = arr._data
    qke__syv = pd.Series(iaf__komjj)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(qke__syv.array, 'string')._str_contains(pat,
            case, flags, na, regex)
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.libs.bool_arr_ext.alloc_bool_array(zho__alzc)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = dict_arr_out[zctxr__xffbo[i]]
    return oozkw__hnahb


@register_jitable
def str_contains_non_regex(arr, pat, case):
    iaf__komjj = arr._data
    jjlru__dljck = len(iaf__komjj)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(jjlru__dljck)
    if not case:
        zysdw__iymdb = pat.upper()
    for i in range(jjlru__dljck):
        if case:
            dict_arr_out[i] = pat in iaf__komjj[i]
        else:
            dict_arr_out[i] = zysdw__iymdb in iaf__komjj[i].upper()
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.libs.bool_arr_ext.alloc_bool_array(zho__alzc)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = dict_arr_out[zctxr__xffbo[i]]
    return oozkw__hnahb


@numba.njit
def str_match(arr, pat, case, flags, na):
    iaf__komjj = arr._data
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    oozkw__hnahb = bodo.libs.bool_arr_ext.alloc_bool_array(zho__alzc)
    qke__syv = pd.Series(iaf__komjj)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = qke__syv.array._str_match(pat, case, flags, na)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = dict_arr_out[zctxr__xffbo[i]]
    return oozkw__hnahb


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    hwk__eftks = f"""def str_{func_name}({', '.join(func_args)}):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}({', '.join(func_args[1:])})
"""
    if can_create_non_unique:
        hwk__eftks += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        hwk__eftks += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    qtao__zld = {}
    exec(hwk__eftks, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, qtao__zld)
    return qtao__zld[f'str_{func_name}']


def _register_simple_str2str_methods():
    goj__noni = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    dlv__hsjk = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in goj__noni.keys():
        vcngh__duhod = create_simple_str2str_methods(func_name, goj__noni[
            func_name], dlv__hsjk[func_name])
        vcngh__duhod = register_jitable(vcngh__duhod)
        globals()[f'str_{func_name}'] = vcngh__duhod


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    vcel__jai = len(xkydm__cpfqf)
    zho__alzc = len(zctxr__xffbo)
    mlxeu__ens = bodo.libs.int_arr_ext.alloc_int_array(vcel__jai, np.int64)
    oozkw__hnahb = bodo.libs.int_arr_ext.alloc_int_array(zho__alzc, np.int64)
    trxiv__ggi = False
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            bodo.libs.array_kernels.setna(mlxeu__ens, i)
        else:
            mlxeu__ens[i] = xkydm__cpfqf[i].find(sub, start, end)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(mlxeu__ens, zctxr__xffbo[i]):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = mlxeu__ens[zctxr__xffbo[i]]
            if oozkw__hnahb[i] == -1:
                trxiv__ggi = True
    nmzj__esi = 'substring not found' if trxiv__ggi else ''
    synchronize_error_njit('ValueError', nmzj__esi)
    return oozkw__hnahb


@register_jitable
def str_rindex(arr, sub, start, end):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    vcel__jai = len(xkydm__cpfqf)
    zho__alzc = len(zctxr__xffbo)
    mlxeu__ens = bodo.libs.int_arr_ext.alloc_int_array(vcel__jai, np.int64)
    oozkw__hnahb = bodo.libs.int_arr_ext.alloc_int_array(zho__alzc, np.int64)
    trxiv__ggi = False
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            bodo.libs.array_kernels.setna(mlxeu__ens, i)
        else:
            mlxeu__ens[i] = xkydm__cpfqf[i].rindex(sub, start, end)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(mlxeu__ens, zctxr__xffbo[i]):
            bodo.libs.array_kernels.setna(oozkw__hnahb, i)
        else:
            oozkw__hnahb[i] = mlxeu__ens[zctxr__xffbo[i]]
            if oozkw__hnahb[i] == -1:
                trxiv__ggi = True
    nmzj__esi = 'substring not found' if trxiv__ggi else ''
    synchronize_error_njit('ValueError', nmzj__esi)
    return oozkw__hnahb


def create_find_methods(func_name):
    hwk__eftks = f"""def str_{func_name}(arr, sub, start, end):
  data_arr = arr._data
  indices_arr = arr._indices
  n_data = len(data_arr)
  n_indices = len(indices_arr)
  tmp_dict_arr = bodo.libs.int_arr_ext.alloc_int_array(n_data, np.int64)
  out_int_arr = bodo.libs.int_arr_ext.alloc_int_array(n_indices, np.int64)
  for i in range(n_data):
    if bodo.libs.array_kernels.isna(data_arr, i):
      bodo.libs.array_kernels.setna(tmp_dict_arr, i)
      continue
    tmp_dict_arr[i] = data_arr[i].{func_name}(sub, start, end)
  for i in range(n_indices):
    if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
      tmp_dict_arr, indices_arr[i]
    ):
      bodo.libs.array_kernels.setna(out_int_arr, i)
    else:
      out_int_arr[i] = tmp_dict_arr[indices_arr[i]]
  return out_int_arr"""
    qtao__zld = {}
    exec(hwk__eftks, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, qtao__zld)
    return qtao__zld[f'str_{func_name}']


def _register_find_methods():
    lupzr__hbc = ['find', 'rfind']
    for func_name in lupzr__hbc:
        vcngh__duhod = create_find_methods(func_name)
        vcngh__duhod = register_jitable(vcngh__duhod)
        globals()[f'str_{func_name}'] = vcngh__duhod


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    vcel__jai = len(xkydm__cpfqf)
    zho__alzc = len(zctxr__xffbo)
    mlxeu__ens = bodo.libs.int_arr_ext.alloc_int_array(vcel__jai, np.int64)
    xjk__yzz = bodo.libs.int_arr_ext.alloc_int_array(zho__alzc, np.int64)
    regex = re.compile(pat, flags)
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            bodo.libs.array_kernels.setna(mlxeu__ens, i)
            continue
        mlxeu__ens[i] = bodo.libs.str_ext.str_findall_count(regex,
            xkydm__cpfqf[i])
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(zctxr__xffbo, i
            ) or bodo.libs.array_kernels.isna(mlxeu__ens, zctxr__xffbo[i]):
            bodo.libs.array_kernels.setna(xjk__yzz, i)
        else:
            xjk__yzz[i] = mlxeu__ens[zctxr__xffbo[i]]
    return xjk__yzz


@register_jitable
def str_len(arr):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    zho__alzc = len(zctxr__xffbo)
    mlxeu__ens = bodo.libs.array_kernels.get_arr_lens(xkydm__cpfqf, False)
    xjk__yzz = bodo.libs.int_arr_ext.alloc_int_array(zho__alzc, np.int64)
    for i in range(zho__alzc):
        if bodo.libs.array_kernels.isna(zctxr__xffbo, i
            ) or bodo.libs.array_kernels.isna(mlxeu__ens, zctxr__xffbo[i]):
            bodo.libs.array_kernels.setna(xjk__yzz, i)
        else:
            xjk__yzz[i] = mlxeu__ens[zctxr__xffbo[i]]
    return xjk__yzz


@register_jitable
def str_slice(arr, start, stop, step):
    xkydm__cpfqf = arr._data
    vcel__jai = len(xkydm__cpfqf)
    iigq__roa = bodo.libs.str_arr_ext.pre_alloc_string_array(vcel__jai, -1)
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            bodo.libs.array_kernels.setna(iigq__roa, i)
            continue
        iigq__roa[i] = xkydm__cpfqf[i][start:stop:step]
    return init_dict_arr(iigq__roa, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    vcel__jai = len(xkydm__cpfqf)
    zho__alzc = len(zctxr__xffbo)
    iigq__roa = pre_alloc_string_array(vcel__jai, -1)
    oozkw__hnahb = pre_alloc_string_array(zho__alzc, -1)
    for eed__lwrxx in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, eed__lwrxx) or not -len(
            xkydm__cpfqf[eed__lwrxx]) <= i < len(xkydm__cpfqf[eed__lwrxx]):
            bodo.libs.array_kernels.setna(iigq__roa, eed__lwrxx)
            continue
        iigq__roa[eed__lwrxx] = xkydm__cpfqf[eed__lwrxx][i]
    for eed__lwrxx in range(zho__alzc):
        if bodo.libs.array_kernels.isna(zctxr__xffbo, eed__lwrxx
            ) or bodo.libs.array_kernels.isna(iigq__roa, zctxr__xffbo[
            eed__lwrxx]):
            bodo.libs.array_kernels.setna(oozkw__hnahb, eed__lwrxx)
            continue
        oozkw__hnahb[eed__lwrxx] = iigq__roa[zctxr__xffbo[eed__lwrxx]]
    return oozkw__hnahb


@register_jitable
def str_repeat_int(arr, repeats):
    xkydm__cpfqf = arr._data
    vcel__jai = len(xkydm__cpfqf)
    iigq__roa = pre_alloc_string_array(vcel__jai, -1)
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            bodo.libs.array_kernels.setna(iigq__roa, i)
            continue
        iigq__roa[i] = xkydm__cpfqf[i] * repeats
    return init_dict_arr(iigq__roa, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    hwk__eftks = f"""def str_{func_name}(arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    out_dict_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_data)
    out_bool_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_indices)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_dict_arr, i)
            continue
        out_dict_arr[i] = np.bool_(data_arr[i].{func_name}())
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
            data_arr, indices_arr[i]        ):
            bodo.libs.array_kernels.setna(out_bool_arr, i)
        else:
            out_bool_arr[i] = out_dict_arr[indices_arr[i]]
    return out_bool_arr"""
    qtao__zld = {}
    exec(hwk__eftks, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, qtao__zld)
    return qtao__zld[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        vcngh__duhod = create_str2bool_methods(func_name)
        vcngh__duhod = register_jitable(vcngh__duhod)
        globals()[f'str_{func_name}'] = vcngh__duhod


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    xkydm__cpfqf = arr._data
    zctxr__xffbo = arr._indices
    vcel__jai = len(xkydm__cpfqf)
    zho__alzc = len(zctxr__xffbo)
    regex = re.compile(pat, flags=flags)
    twe__wdgh = []
    for smyue__vkhaz in range(n_cols):
        twe__wdgh.append(pre_alloc_string_array(vcel__jai, -1))
    yicl__luk = bodo.libs.bool_arr_ext.alloc_bool_array(vcel__jai)
    fanv__qqd = zctxr__xffbo.copy()
    for i in range(vcel__jai):
        if bodo.libs.array_kernels.isna(xkydm__cpfqf, i):
            yicl__luk[i] = True
            for eed__lwrxx in range(n_cols):
                bodo.libs.array_kernels.setna(twe__wdgh[eed__lwrxx], i)
            continue
        rnmp__tvnhg = regex.search(xkydm__cpfqf[i])
        if rnmp__tvnhg:
            yicl__luk[i] = False
            ysi__lto = rnmp__tvnhg.groups()
            for eed__lwrxx in range(n_cols):
                twe__wdgh[eed__lwrxx][i] = ysi__lto[eed__lwrxx]
        else:
            yicl__luk[i] = True
            for eed__lwrxx in range(n_cols):
                bodo.libs.array_kernels.setna(twe__wdgh[eed__lwrxx], i)
    for i in range(zho__alzc):
        if yicl__luk[fanv__qqd[i]]:
            bodo.libs.array_kernels.setna(fanv__qqd, i)
    zuy__spcf = [init_dict_arr(twe__wdgh[i], fanv__qqd.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return zuy__spcf


def create_extractall_methods(is_multi_group):
    jrkv__ypskx = '_multi' if is_multi_group else ''
    hwk__eftks = f"""def str_extractall{jrkv__ypskx}(arr, regex, n_cols, index_arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    indices_count = [0 for _ in range(n_data)]
    for i in range(n_indices):
        if not bodo.libs.array_kernels.isna(indices_arr, i):
            indices_count[indices_arr[i]] += 1
    dict_group_count = []
    out_dict_len = out_ind_len = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        dict_group_count.append((out_dict_len, len(m)))
        out_dict_len += len(m)
        out_ind_len += indices_count[i] * len(m)
    out_dict_arr_list = []
    for _ in range(n_cols):
        out_dict_arr_list.append(pre_alloc_string_array(out_dict_len, -1))
    out_indices_arr = bodo.libs.int_arr_ext.alloc_int_array(out_ind_len, np.int32)
    out_ind_arr = bodo.utils.utils.alloc_type(out_ind_len, index_arr, (-1,))
    out_match_arr = np.empty(out_ind_len, np.int64)
    curr_ind = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        for s in m:
            for j in range(n_cols):
                out_dict_arr_list[j][curr_ind] = s{'[j]' if is_multi_group else ''}
            curr_ind += 1
    curr_ind = 0
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i):
            continue
        n_rows = dict_group_count[indices_arr[i]][1]
        for k in range(n_rows):
            out_indices_arr[curr_ind] = dict_group_count[indices_arr[i]][0] + k
            out_ind_arr[curr_ind] = index_arr[i]
            out_match_arr[curr_ind] = k
            curr_ind += 1
    out_arr_list = [
        init_dict_arr(
            out_dict_arr_list[i], out_indices_arr.copy(), arr._has_global_dictionary, False
        )
        for i in range(n_cols)
    ]
    return (out_ind_arr, out_match_arr, out_arr_list) 
"""
    qtao__zld = {}
    exec(hwk__eftks, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, qtao__zld)
    return qtao__zld[f'str_extractall{jrkv__ypskx}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        jrkv__ypskx = '_multi' if is_multi_group else ''
        vcngh__duhod = create_extractall_methods(is_multi_group)
        vcngh__duhod = register_jitable(vcngh__duhod)
        globals()[f'str_extractall{jrkv__ypskx}'] = vcngh__duhod


_register_extractall_methods()
