"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        fnnmi__chfl = int(np.log2(self.dtype.bitwidth // 8))
        gimtn__xmyh = 0 if self.dtype.signed else 4
        idx = fnnmi__chfl + gimtn__xmyh
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cht__zyrmq = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, cht__zyrmq)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    izz__opiq = 8 * val.dtype.itemsize
    dzfsu__ouiuu = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(dzfsu__ouiuu, izz__opiq))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        jostp__hhih = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(jostp__hhih)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    svtnx__haopz = c.context.insert_const_string(c.builder.module, 'pandas')
    cjr__diz = c.pyapi.import_module_noblock(svtnx__haopz)
    glvfw__hxke = c.pyapi.call_method(cjr__diz, str(typ)[:-2], ())
    c.pyapi.decref(cjr__diz)
    return glvfw__hxke


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    izz__opiq = 8 * val.itemsize
    dzfsu__ouiuu = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(dzfsu__ouiuu, izz__opiq))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    bcl__thtb = n + 7 >> 3
    pwmg__wsf = np.empty(bcl__thtb, np.uint8)
    for i in range(n):
        uio__zvplx = i // 8
        pwmg__wsf[uio__zvplx] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            pwmg__wsf[uio__zvplx]) & kBitmask[i % 8]
    return pwmg__wsf


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ejbe__ajjn = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ejbe__ajjn)
    c.pyapi.decref(ejbe__ajjn)
    caj__umbxo = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bcl__thtb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    reft__qao = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [bcl__thtb])
    nph__jrmyu = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    zni__kenra = cgutils.get_or_insert_function(c.builder.module,
        nph__jrmyu, name='is_pd_int_array')
    hzejf__ysk = c.builder.call(zni__kenra, [obj])
    lbcsr__yxj = c.builder.icmp_unsigned('!=', hzejf__ysk, hzejf__ysk.type(0))
    with c.builder.if_else(lbcsr__yxj) as (htnt__cedg, cxxg__wbq):
        with htnt__cedg:
            jas__wch = c.pyapi.object_getattr_string(obj, '_data')
            caj__umbxo.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), jas__wch).value
            cjpf__ijcx = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), cjpf__ijcx).value
            c.pyapi.decref(jas__wch)
            c.pyapi.decref(cjpf__ijcx)
            fqdrl__dmgu = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            nph__jrmyu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            zni__kenra = cgutils.get_or_insert_function(c.builder.module,
                nph__jrmyu, name='mask_arr_to_bitmap')
            c.builder.call(zni__kenra, [reft__qao.data, fqdrl__dmgu.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with cxxg__wbq:
            fvu__xiru = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            nph__jrmyu = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            tpmf__adoof = cgutils.get_or_insert_function(c.builder.module,
                nph__jrmyu, name='int_array_from_sequence')
            c.builder.call(tpmf__adoof, [obj, c.builder.bitcast(fvu__xiru.
                data, lir.IntType(8).as_pointer()), reft__qao.data])
            caj__umbxo.data = fvu__xiru._getvalue()
    caj__umbxo.null_bitmap = reft__qao._getvalue()
    urqlt__ymgz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(caj__umbxo._getvalue(), is_error=urqlt__ymgz)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    caj__umbxo = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        caj__umbxo.data, c.env_manager)
    xrzzl__dsuv = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, caj__umbxo.null_bitmap).data
    ejbe__ajjn = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ejbe__ajjn)
    svtnx__haopz = c.context.insert_const_string(c.builder.module, 'numpy')
    tru__esfyj = c.pyapi.import_module_noblock(svtnx__haopz)
    etqs__vluz = c.pyapi.object_getattr_string(tru__esfyj, 'bool_')
    mask_arr = c.pyapi.call_method(tru__esfyj, 'empty', (ejbe__ajjn,
        etqs__vluz))
    sclp__ijdth = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    mwgyc__dtzo = c.pyapi.object_getattr_string(sclp__ijdth, 'data')
    ophj__gin = c.builder.inttoptr(c.pyapi.long_as_longlong(mwgyc__dtzo),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as wcklx__gobuz:
        i = wcklx__gobuz.index
        xhgkg__lhpf = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        oovy__anm = c.builder.load(cgutils.gep(c.builder, xrzzl__dsuv,
            xhgkg__lhpf))
        iyyxj__vdcv = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(oovy__anm, iyyxj__vdcv), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        xkdl__umqhv = cgutils.gep(c.builder, ophj__gin, i)
        c.builder.store(val, xkdl__umqhv)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        caj__umbxo.null_bitmap)
    svtnx__haopz = c.context.insert_const_string(c.builder.module, 'pandas')
    cjr__diz = c.pyapi.import_module_noblock(svtnx__haopz)
    qvf__dwtts = c.pyapi.object_getattr_string(cjr__diz, 'arrays')
    glvfw__hxke = c.pyapi.call_method(qvf__dwtts, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(cjr__diz)
    c.pyapi.decref(ejbe__ajjn)
    c.pyapi.decref(tru__esfyj)
    c.pyapi.decref(etqs__vluz)
    c.pyapi.decref(sclp__ijdth)
    c.pyapi.decref(mwgyc__dtzo)
    c.pyapi.decref(qvf__dwtts)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return glvfw__hxke


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        xcj__safr, eycew__vhqn = args
        caj__umbxo = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        caj__umbxo.data = xcj__safr
        caj__umbxo.null_bitmap = eycew__vhqn
        context.nrt.incref(builder, signature.args[0], xcj__safr)
        context.nrt.incref(builder, signature.args[1], eycew__vhqn)
        return caj__umbxo._getvalue()
    vqvns__zrp = IntegerArrayType(data.dtype)
    cizg__xjutq = vqvns__zrp(data, null_bitmap)
    return cizg__xjutq, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    rpd__nzr = np.empty(n, pyval.dtype.type)
    ihbxq__dcy = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        ntnq__vrc = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ihbxq__dcy, i, int(not ntnq__vrc))
        if not ntnq__vrc:
            rpd__nzr[i] = s
    aqv__wznzf = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), rpd__nzr)
    jepq__gzrtw = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ihbxq__dcy)
    return lir.Constant.literal_struct([aqv__wznzf, jepq__gzrtw])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    royl__awox = args[0]
    if equiv_set.has_shape(royl__awox):
        return ArrayAnalysis.AnalyzeResult(shape=royl__awox, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    royl__awox = args[0]
    if equiv_set.has_shape(royl__awox):
        return ArrayAnalysis.AnalyzeResult(shape=royl__awox, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    rpd__nzr = np.empty(n, dtype)
    fco__miktt = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(rpd__nzr, fco__miktt)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            wamd__zgmy, wxhk__enbv = array_getitem_bool_index(A, ind)
            return init_integer_array(wamd__zgmy, wxhk__enbv)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            wamd__zgmy, wxhk__enbv = array_getitem_int_index(A, ind)
            return init_integer_array(wamd__zgmy, wxhk__enbv)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            wamd__zgmy, wxhk__enbv = array_getitem_slice_index(A, ind)
            return init_integer_array(wamd__zgmy, wxhk__enbv)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    vrfv__feh = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    jyqyd__frvv = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if jyqyd__frvv:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(vrfv__feh)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or jyqyd__frvv):
        raise BodoError(vrfv__feh)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if isinstance(dtype, types.TypeRef):
        dtype = dtype.instance_type
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            jtfm__mkpbk = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                jtfm__mkpbk[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    jtfm__mkpbk[i] = np.nan
            return jtfm__mkpbk
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for kyvbp__rsflm in numba.np.ufunc_db.get_ufuncs():
        qte__hto = create_op_overload(kyvbp__rsflm, kyvbp__rsflm.nin)
        overload(kyvbp__rsflm, no_unliteral=True)(qte__hto)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qte__hto = create_op_overload(op, 2)
        overload(op)(qte__hto)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qte__hto = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qte__hto)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qte__hto = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qte__hto)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    auq__pys = dict(skipna=skipna, min_count=min_count)
    rvpj__bqn = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', auq__pys, rvpj__bqn)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        iyyxj__vdcv = []
        yjk__vffj = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not yjk__vffj:
                    data.append(dtype(1))
                    iyyxj__vdcv.append(False)
                    yjk__vffj = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                iyyxj__vdcv.append(True)
        wamd__zgmy = np.array(data)
        n = len(wamd__zgmy)
        bcl__thtb = n + 7 >> 3
        wxhk__enbv = np.empty(bcl__thtb, np.uint8)
        for kcyp__kvx in range(n):
            set_bit_to_arr(wxhk__enbv, kcyp__kvx, iyyxj__vdcv[kcyp__kvx])
        return init_integer_array(wamd__zgmy, wxhk__enbv)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    hvk__ilnv = numba.core.registry.cpu_target.typing_context
    dwru__miwf = hvk__ilnv.resolve_function_type(op, (types.Array(A.dtype, 
        1, 'C'),), {}).return_type
    dwru__miwf = to_nullable_type(dwru__miwf)

    def impl(A):
        n = len(A)
        rlwir__wltq = bodo.utils.utils.alloc_type(n, dwru__miwf, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(rlwir__wltq, i)
                continue
            rlwir__wltq[i] = op(A[i])
        return rlwir__wltq
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    syanw__myppb = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    msj__ydii = isinstance(lhs, (types.Number, types.Boolean))
    zllnk__syts = isinstance(rhs, (types.Number, types.Boolean))
    beii__giyn = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    ciwu__qsn = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    hvk__ilnv = numba.core.registry.cpu_target.typing_context
    dwru__miwf = hvk__ilnv.resolve_function_type(op, (beii__giyn, ciwu__qsn
        ), {}).return_type
    dwru__miwf = to_nullable_type(dwru__miwf)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    wvavx__kok = 'lhs' if msj__ydii else 'lhs[i]'
    rknej__qvac = 'rhs' if zllnk__syts else 'rhs[i]'
    jrzs__ykl = ('False' if msj__ydii else
        'bodo.libs.array_kernels.isna(lhs, i)')
    tycg__rqlol = ('False' if zllnk__syts else
        'bodo.libs.array_kernels.isna(rhs, i)')
    ykyr__efntg = 'def impl(lhs, rhs):\n'
    ykyr__efntg += '  n = len({})\n'.format('lhs' if not msj__ydii else 'rhs')
    if syanw__myppb:
        ykyr__efntg += '  out_arr = {}\n'.format('lhs' if not msj__ydii else
            'rhs')
    else:
        ykyr__efntg += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    ykyr__efntg += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    ykyr__efntg += '    if ({}\n'.format(jrzs__ykl)
    ykyr__efntg += '        or {}):\n'.format(tycg__rqlol)
    ykyr__efntg += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    ykyr__efntg += '      continue\n'
    ykyr__efntg += (
        """    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))
"""
        .format(wvavx__kok, rknej__qvac))
    ykyr__efntg += '  return out_arr\n'
    mgg__asby = {}
    exec(ykyr__efntg, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        dwru__miwf, 'op': op}, mgg__asby)
    impl = mgg__asby['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        msj__ydii = lhs in [pd_timedelta_type]
        zllnk__syts = rhs in [pd_timedelta_type]
        if msj__ydii:

            def impl(lhs, rhs):
                n = len(rhs)
                rlwir__wltq = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(rlwir__wltq, i)
                        continue
                    rlwir__wltq[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return rlwir__wltq
            return impl
        elif zllnk__syts:

            def impl(lhs, rhs):
                n = len(lhs)
                rlwir__wltq = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(rlwir__wltq, i)
                        continue
                    rlwir__wltq[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return rlwir__wltq
            return impl
    return impl
