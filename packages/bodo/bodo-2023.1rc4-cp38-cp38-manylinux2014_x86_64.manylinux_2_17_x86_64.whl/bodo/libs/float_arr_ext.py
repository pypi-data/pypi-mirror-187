"""Nullable float array corresponding to Pandas FloatingArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import os
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
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('is_pd_float_array', array_ext.is_pd_float_array)
ll.add_symbol('float_array_from_sequence', array_ext.float_array_from_sequence)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
_use_nullable_float = int(os.environ.get('BODO_USE_NULLABLE_FLOAT', '0'))


class FloatingArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(FloatingArrayType, self).__init__(name=
            f'FloatingArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return FloatingArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        return pd.Float64Dtype(
            ) if self.dtype == types.float64 else pd.Float32Dtype()


@register_model(FloatingArrayType)
class FloatingArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gzu__byso = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, gzu__byso)


make_attribute_wrapper(FloatingArrayType, 'data', '_data')
make_attribute_wrapper(FloatingArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.FloatingArray)
def _typeof_pd_float_array(val, c):
    dtype = types.float32 if val.dtype == pd.Float32Dtype() else types.float64
    return FloatingArrayType(dtype)


class FloatDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Float)
        self.dtype = dtype
        fdm__hojjt = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(fdm__hojjt)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    xdo__jaog = c.context.insert_const_string(c.builder.module, 'pandas')
    ufkj__siskf = c.pyapi.import_module_noblock(xdo__jaog)
    sbtl__bur = c.pyapi.call_method(ufkj__siskf, str(typ)[:-2], ())
    c.pyapi.decref(ufkj__siskf)
    return sbtl__bur


@unbox(FloatDtype)
def unbox_floatdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_float_dtype(val, c):
    dtype = types.float32 if val == pd.Float32Dtype() else types.float64
    return FloatDtype(dtype)


def _register_float_dtype(t):
    typeof_impl.register(t)(typeof_pd_float_dtype)
    float_dtype = typeof_pd_float_dtype(t(), None)
    type_callable(t)(lambda c: lambda : float_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


_register_float_dtype(pd.Float32Dtype)
_register_float_dtype(pd.Float64Dtype)


@unbox(FloatingArrayType)
def unbox_float_array(typ, obj, c):
    fskcb__jjkq = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(fskcb__jjkq)
    c.pyapi.decref(fskcb__jjkq)
    yaqa__ivyc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jya__lnsu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    rfr__qsd = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types.
        Array(types.uint8, 1, 'C'), [jya__lnsu])
    groa__lrf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    yvx__wzl = cgutils.get_or_insert_function(c.builder.module, groa__lrf,
        name='is_pd_float_array')
    ehb__xxgda = c.builder.call(yvx__wzl, [obj])
    udzag__qauo = c.builder.icmp_unsigned('!=', ehb__xxgda, ehb__xxgda.type(0))
    with c.builder.if_else(udzag__qauo) as (lqse__bgda, zftv__wibz):
        with lqse__bgda:
            cegxf__eqxa = c.pyapi.object_getattr_string(obj, '_data')
            yaqa__ivyc.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), cegxf__eqxa).value
            ayqio__hwjtn = c.pyapi.object_getattr_string(obj, '_mask')
            msng__zir = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ayqio__hwjtn).value
            c.pyapi.decref(cegxf__eqxa)
            c.pyapi.decref(ayqio__hwjtn)
            uqksm__bwdkg = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, msng__zir)
            groa__lrf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            yvx__wzl = cgutils.get_or_insert_function(c.builder.module,
                groa__lrf, name='mask_arr_to_bitmap')
            c.builder.call(yvx__wzl, [rfr__qsd.data, uqksm__bwdkg.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), msng__zir)
        with zftv__wibz:
            vxk__xngbm = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            groa__lrf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            xwqds__xml = cgutils.get_or_insert_function(c.builder.module,
                groa__lrf, name='float_array_from_sequence')
            c.builder.call(xwqds__xml, [obj, c.builder.bitcast(vxk__xngbm.
                data, lir.IntType(8).as_pointer()), rfr__qsd.data])
            yaqa__ivyc.data = vxk__xngbm._getvalue()
    yaqa__ivyc.null_bitmap = rfr__qsd._getvalue()
    usvwe__rmlz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yaqa__ivyc._getvalue(), is_error=usvwe__rmlz)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    yaqa__ivyc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        yaqa__ivyc.data, c.env_manager)
    oof__dyc = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, yaqa__ivyc.null_bitmap).data
    fskcb__jjkq = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(fskcb__jjkq)
    xdo__jaog = c.context.insert_const_string(c.builder.module, 'numpy')
    sjak__lvje = c.pyapi.import_module_noblock(xdo__jaog)
    vjbn__rstwt = c.pyapi.object_getattr_string(sjak__lvje, 'bool_')
    msng__zir = c.pyapi.call_method(sjak__lvje, 'empty', (fskcb__jjkq,
        vjbn__rstwt))
    mbdu__oyqx = c.pyapi.object_getattr_string(msng__zir, 'ctypes')
    jyxl__gpev = c.pyapi.object_getattr_string(mbdu__oyqx, 'data')
    ppqte__olb = c.builder.inttoptr(c.pyapi.long_as_longlong(jyxl__gpev),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as bloxa__wrf:
        skulr__molxw = bloxa__wrf.index
        eaijk__uodwn = c.builder.lshr(skulr__molxw, lir.Constant(lir.
            IntType(64), 3))
        ali__acv = c.builder.load(cgutils.gep(c.builder, oof__dyc,
            eaijk__uodwn))
        qpvs__bvkoo = c.builder.trunc(c.builder.and_(skulr__molxw, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(ali__acv, qpvs__bvkoo), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        svtru__zvj = cgutils.gep(c.builder, ppqte__olb, skulr__molxw)
        c.builder.store(val, svtru__zvj)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        yaqa__ivyc.null_bitmap)
    xdo__jaog = c.context.insert_const_string(c.builder.module, 'pandas')
    ufkj__siskf = c.pyapi.import_module_noblock(xdo__jaog)
    oyzwj__dgjex = c.pyapi.object_getattr_string(ufkj__siskf, 'arrays')
    sbtl__bur = c.pyapi.call_method(oyzwj__dgjex, 'FloatingArray', (data,
        msng__zir))
    c.pyapi.decref(ufkj__siskf)
    c.pyapi.decref(fskcb__jjkq)
    c.pyapi.decref(sjak__lvje)
    c.pyapi.decref(vjbn__rstwt)
    c.pyapi.decref(mbdu__oyqx)
    c.pyapi.decref(jyxl__gpev)
    c.pyapi.decref(oyzwj__dgjex)
    c.pyapi.decref(data)
    c.pyapi.decref(msng__zir)
    return sbtl__bur


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dzrf__noq, cmy__pap = args
        yaqa__ivyc = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        yaqa__ivyc.data = dzrf__noq
        yaqa__ivyc.null_bitmap = cmy__pap
        context.nrt.incref(builder, signature.args[0], dzrf__noq)
        context.nrt.incref(builder, signature.args[1], cmy__pap)
        return yaqa__ivyc._getvalue()
    gnugp__plg = FloatingArrayType(data.dtype)
    buhdv__jkeid = gnugp__plg(data, null_bitmap)
    return buhdv__jkeid, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    pdq__rohz = np.empty(n, pyval.dtype.type)
    iej__gyua = np.empty(n + 7 >> 3, np.uint8)
    for skulr__molxw, s in enumerate(pyval):
        qwa__dxgxm = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(iej__gyua, skulr__molxw, int(
            not qwa__dxgxm))
        if not qwa__dxgxm:
            pdq__rohz[skulr__molxw] = s
    rhqcv__fzo = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), pdq__rohz)
    mzyq__syxef = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), iej__gyua)
    return lir.Constant.literal_struct([rhqcv__fzo, mzyq__syxef])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    fodo__flg = args[0]
    if equiv_set.has_shape(fodo__flg):
        return ArrayAnalysis.AnalyzeResult(shape=fodo__flg, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fodo__flg = args[0]
    if equiv_set.has_shape(fodo__flg):
        return ArrayAnalysis.AnalyzeResult(shape=fodo__flg, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_init_float_array = (
    init_float_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_float_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_float_array',
    'bodo.libs.float_arr_ext'] = alias_ext_init_float_array
numba.core.ir_utils.alias_func_extensions['get_float_arr_data',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_float_arr_bitmap',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_float_array(n, dtype):
    pdq__rohz = np.empty(n, dtype)
    aejis__pjjjw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(pdq__rohz, aejis__pjjjw)


def alloc_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_alloc_float_array
    ) = alloc_float_array_equiv


@overload(operator.getitem, no_unliteral=True)
def float_arr_getitem(A, ind):
    if not isinstance(A, FloatingArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            oyip__ngvcv, iaqbu__erbf = array_getitem_bool_index(A, ind)
            return init_float_array(oyip__ngvcv, iaqbu__erbf)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            oyip__ngvcv, iaqbu__erbf = array_getitem_int_index(A, ind)
            return init_float_array(oyip__ngvcv, iaqbu__erbf)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            oyip__ngvcv, iaqbu__erbf = array_getitem_slice_index(A, ind)
            return init_float_array(oyip__ngvcv, iaqbu__erbf)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def float_arr_setitem(A, idx, val):
    if not isinstance(A, FloatingArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    nrs__ije = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    btazf__jtls = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if btazf__jtls:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(nrs__ije)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or btazf__jtls):
        raise BodoError(nrs__ije)
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
        f'setitem for FloatingArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_float_arr_len(A):
    if isinstance(A, FloatingArrayType):
        return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'shape')
def overload_float_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(FloatingArrayType, 'dtype')
def overload_float_arr_dtype(A):
    dtype_class = (pd.Float32Dtype if A.dtype == types.float32 else pd.
        Float64Dtype)
    return lambda A: dtype_class()


@overload_attribute(FloatingArrayType, 'ndim')
def overload_float_arr_ndim(A):
    return lambda A: 1


@overload_attribute(FloatingArrayType, 'size')
def overload_float_size(A):
    return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'nbytes')
def float_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(FloatingArrayType, 'copy', no_unliteral=True)
def overload_float_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.float_arr_ext.init_float_array(
            bodo.libs.float_arr_ext.get_float_arr_data(A).copy(), bodo.libs
            .float_arr_ext.get_float_arr_bitmap(A).copy())


@overload_method(FloatingArrayType, 'astype', no_unliteral=True)
def overload_float_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "FloatingArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, FloatDtype) and A.dtype == dtype.dtype:
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
    if isinstance(dtype, FloatDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
            init_float_array(bodo.libs.float_arr_ext.get_float_arr_data(A).
            astype(np_dtype), bodo.libs.float_arr_ext.get_float_arr_bitmap(
            A).copy()))
    if isinstance(dtype, bodo.libs.int_arr_ext.IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.float_arr_ext.get_float_arr_data(A
            ).astype(np_dtype), bodo.libs.float_arr_ext.
            get_float_arr_bitmap(A).copy()))
    nb_dtype = parse_dtype(dtype, 'FloatingArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.float_arr_ext.get_float_arr_data(A)
            n = len(data)
            nyrr__ews = np.empty(n, nb_dtype)
            for skulr__molxw in numba.parfors.parfor.internal_prange(n):
                nyrr__ews[skulr__molxw] = data[skulr__molxw]
                if bodo.libs.array_kernels.isna(A, skulr__molxw):
                    nyrr__ews[skulr__molxw] = np.nan
            return nyrr__ews
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
        get_float_arr_data(A).astype(nb_dtype))


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_float_arr_op_nin_1(A):
            if isinstance(A, FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_float_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
                FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for twmip__eeafi in numba.np.ufunc_db.get_ufuncs():
        gzhky__ydii = create_op_overload(twmip__eeafi, twmip__eeafi.nin)
        overload(twmip__eeafi, no_unliteral=True)(gzhky__ydii)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        gzhky__ydii = create_op_overload(op, 2)
        overload(op)(gzhky__ydii)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        gzhky__ydii = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(gzhky__ydii)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        gzhky__ydii = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(gzhky__ydii)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    vcg__elk = dict(skipna=skipna, min_count=min_count)
    yjkwy__zel = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', vcg__elk, yjkwy__zel)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for skulr__molxw in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, skulr__molxw):
                val = A[skulr__molxw]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        qpvs__bvkoo = []
        aien__sfs = False
        s = set()
        for skulr__molxw in range(len(A)):
            val = A[skulr__molxw]
            if bodo.libs.array_kernels.isna(A, skulr__molxw):
                if not aien__sfs:
                    data.append(dtype(1))
                    qpvs__bvkoo.append(False)
                    aien__sfs = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                qpvs__bvkoo.append(True)
        oyip__ngvcv = np.array(data)
        n = len(oyip__ngvcv)
        jya__lnsu = n + 7 >> 3
        iaqbu__erbf = np.empty(jya__lnsu, np.uint8)
        for gnx__kmx in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(iaqbu__erbf, gnx__kmx,
                qpvs__bvkoo[gnx__kmx])
        return init_float_array(oyip__ngvcv, iaqbu__erbf)
    return impl_float_arr
