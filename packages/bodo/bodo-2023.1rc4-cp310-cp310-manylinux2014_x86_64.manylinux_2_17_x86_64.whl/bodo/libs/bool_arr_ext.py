"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cxv__gbd = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, cxv__gbd)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    wtw__bejb = c.context.insert_const_string(c.builder.module, 'pandas')
    mkps__fxi = c.pyapi.import_module_noblock(wtw__bejb)
    puf__xruw = c.pyapi.call_method(mkps__fxi, 'BooleanDtype', ())
    c.pyapi.decref(mkps__fxi)
    return puf__xruw


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    ckn__ushah = n + 7 >> 3
    return np.full(ckn__ushah, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    kret__lsrf = c.context.typing_context.resolve_value_type(func)
    gqxd__zltzl = kret__lsrf.get_call_type(c.context.typing_context,
        arg_typs, {})
    ylii__mlmga = c.context.get_function(kret__lsrf, gqxd__zltzl)
    ratew__oui = c.context.call_conv.get_function_type(gqxd__zltzl.
        return_type, gqxd__zltzl.args)
    pvwx__flbj = c.builder.module
    lmro__zvbj = lir.Function(pvwx__flbj, ratew__oui, name=pvwx__flbj.
        get_unique_name('.func_conv'))
    lmro__zvbj.linkage = 'internal'
    egop__tpgvu = lir.IRBuilder(lmro__zvbj.append_basic_block())
    mwgli__aps = c.context.call_conv.decode_arguments(egop__tpgvu,
        gqxd__zltzl.args, lmro__zvbj)
    mtubt__oleb = ylii__mlmga(egop__tpgvu, mwgli__aps)
    c.context.call_conv.return_value(egop__tpgvu, mtubt__oleb)
    ndi__zbzd, dhe__ovzgg = c.context.call_conv.call_function(c.builder,
        lmro__zvbj, gqxd__zltzl.return_type, gqxd__zltzl.args, args)
    return dhe__ovzgg


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    qxxs__sknnd = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(qxxs__sknnd)
    c.pyapi.decref(qxxs__sknnd)
    ratew__oui = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    nglup__jzfcb = cgutils.get_or_insert_function(c.builder.module,
        ratew__oui, name='is_bool_array')
    ratew__oui = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    lmro__zvbj = cgutils.get_or_insert_function(c.builder.module,
        ratew__oui, name='is_pd_boolean_array')
    dht__npwwh = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mfim__wcv = c.builder.call(lmro__zvbj, [obj])
    zjaac__drbgw = c.builder.icmp_unsigned('!=', mfim__wcv, mfim__wcv.type(0))
    with c.builder.if_else(zjaac__drbgw) as (zgv__nejk, nbnr__kzb):
        with zgv__nejk:
            iqyw__aji = c.pyapi.object_getattr_string(obj, '_data')
            dht__npwwh.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), iqyw__aji).value
            vrysg__bagqm = c.pyapi.object_getattr_string(obj, '_mask')
            lwf__xtxzp = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), vrysg__bagqm).value
            ckn__ushah = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            ivc__omb = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, lwf__xtxzp)
            kvydx__mvl = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [ckn__ushah])
            ratew__oui = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            lmro__zvbj = cgutils.get_or_insert_function(c.builder.module,
                ratew__oui, name='mask_arr_to_bitmap')
            c.builder.call(lmro__zvbj, [kvydx__mvl.data, ivc__omb.data, n])
            dht__npwwh.null_bitmap = kvydx__mvl._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), lwf__xtxzp)
            c.pyapi.decref(iqyw__aji)
            c.pyapi.decref(vrysg__bagqm)
        with nbnr__kzb:
            bzkol__jxvl = c.builder.call(nglup__jzfcb, [obj])
            ltrql__jclw = c.builder.icmp_unsigned('!=', bzkol__jxvl,
                bzkol__jxvl.type(0))
            with c.builder.if_else(ltrql__jclw) as (anun__solsw, ruo__xuxj):
                with anun__solsw:
                    dht__npwwh.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    dht__npwwh.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with ruo__xuxj:
                    dht__npwwh.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    ckn__ushah = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    dht__npwwh.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [ckn__ushah])._getvalue()
                    sdy__dgixe = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, dht__npwwh.data
                        ).data
                    iyniy__pal = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, dht__npwwh.
                        null_bitmap).data
                    ratew__oui = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    lmro__zvbj = cgutils.get_or_insert_function(c.builder.
                        module, ratew__oui, name='unbox_bool_array_obj')
                    c.builder.call(lmro__zvbj, [obj, sdy__dgixe, iyniy__pal, n]
                        )
    return NativeValue(dht__npwwh._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    dht__npwwh = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        dht__npwwh.data, c.env_manager)
    cantx__cvolh = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, dht__npwwh.null_bitmap).data
    qxxs__sknnd = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(qxxs__sknnd)
    wtw__bejb = c.context.insert_const_string(c.builder.module, 'numpy')
    rfz__pjy = c.pyapi.import_module_noblock(wtw__bejb)
    fzbn__ojjg = c.pyapi.object_getattr_string(rfz__pjy, 'bool_')
    lwf__xtxzp = c.pyapi.call_method(rfz__pjy, 'empty', (qxxs__sknnd,
        fzbn__ojjg))
    jlm__kzq = c.pyapi.object_getattr_string(lwf__xtxzp, 'ctypes')
    dicr__nob = c.pyapi.object_getattr_string(jlm__kzq, 'data')
    jltp__pnai = c.builder.inttoptr(c.pyapi.long_as_longlong(dicr__nob),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as dft__jxi:
        abk__swqc = dft__jxi.index
        wsyg__zkk = c.builder.lshr(abk__swqc, lir.Constant(lir.IntType(64), 3))
        lilj__wthai = c.builder.load(cgutils.gep(c.builder, cantx__cvolh,
            wsyg__zkk))
        vjze__dgmqo = c.builder.trunc(c.builder.and_(abk__swqc, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(lilj__wthai, vjze__dgmqo), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        jfhz__vcj = cgutils.gep(c.builder, jltp__pnai, abk__swqc)
        c.builder.store(val, jfhz__vcj)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        dht__npwwh.null_bitmap)
    wtw__bejb = c.context.insert_const_string(c.builder.module, 'pandas')
    mkps__fxi = c.pyapi.import_module_noblock(wtw__bejb)
    jhpeu__puf = c.pyapi.object_getattr_string(mkps__fxi, 'arrays')
    puf__xruw = c.pyapi.call_method(jhpeu__puf, 'BooleanArray', (data,
        lwf__xtxzp))
    c.pyapi.decref(mkps__fxi)
    c.pyapi.decref(qxxs__sknnd)
    c.pyapi.decref(rfz__pjy)
    c.pyapi.decref(fzbn__ojjg)
    c.pyapi.decref(jlm__kzq)
    c.pyapi.decref(dicr__nob)
    c.pyapi.decref(jhpeu__puf)
    c.pyapi.decref(data)
    c.pyapi.decref(lwf__xtxzp)
    return puf__xruw


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    dgiqg__dmn = np.empty(n, np.bool_)
    ctk__kqcai = np.empty(n + 7 >> 3, np.uint8)
    for abk__swqc, s in enumerate(pyval):
        cvy__bgdx = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ctk__kqcai, abk__swqc, int(not
            cvy__bgdx))
        if not cvy__bgdx:
            dgiqg__dmn[abk__swqc] = s
    tixy__etlq = context.get_constant_generic(builder, data_type, dgiqg__dmn)
    name__lsau = context.get_constant_generic(builder, nulls_type, ctk__kqcai)
    return lir.Constant.literal_struct([tixy__etlq, name__lsau])


def lower_init_bool_array(context, builder, signature, args):
    cawov__qgi, dwhw__azt = args
    dht__npwwh = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    dht__npwwh.data = cawov__qgi
    dht__npwwh.null_bitmap = dwhw__azt
    context.nrt.incref(builder, signature.args[0], cawov__qgi)
    context.nrt.incref(builder, signature.args[1], dwhw__azt)
    return dht__npwwh._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zpax__ludyi = args[0]
    if equiv_set.has_shape(zpax__ludyi):
        return ArrayAnalysis.AnalyzeResult(shape=zpax__ludyi, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zpax__ludyi = args[0]
    if equiv_set.has_shape(zpax__ludyi):
        return ArrayAnalysis.AnalyzeResult(shape=zpax__ludyi, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    dgiqg__dmn = np.empty(n, dtype=np.bool_)
    lloet__csm = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(dgiqg__dmn, lloet__csm)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            hvu__phls, ngj__buw = array_getitem_bool_index(A, ind)
            return init_bool_array(hvu__phls, ngj__buw)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            hvu__phls, ngj__buw = array_getitem_int_index(A, ind)
            return init_bool_array(hvu__phls, ngj__buw)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            hvu__phls, ngj__buw = array_getitem_slice_index(A, ind)
            return init_bool_array(hvu__phls, ngj__buw)
        return impl_slice
    if ind != boolean_array:
        raise BodoError(
            f'getitem for BooleanArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    tczj__sqm = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(tczj__sqm)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(tczj__sqm)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'size')
def overload_bool_arr_size(A):
    return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for abk__swqc in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, abk__swqc):
                val = A[abk__swqc]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            irmm__imf = np.empty(n, nb_dtype)
            for abk__swqc in numba.parfors.parfor.internal_prange(n):
                irmm__imf[abk__swqc] = data[abk__swqc]
                if bodo.libs.array_kernels.isna(A, abk__swqc):
                    irmm__imf[abk__swqc] = np.nan
            return irmm__imf
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        irmm__imf = np.empty(n, dtype=np.bool_)
        for abk__swqc in numba.parfors.parfor.internal_prange(n):
            irmm__imf[abk__swqc] = data[abk__swqc]
            if bodo.libs.array_kernels.isna(A, abk__swqc):
                irmm__imf[abk__swqc] = value
        return irmm__imf
    return impl


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    vasst__tsz = op.__name__
    vasst__tsz = ufunc_aliases.get(vasst__tsz, vasst__tsz)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for upoac__skpg in numba.np.ufunc_db.get_ufuncs():
        hvnp__ywvsc = create_op_overload(upoac__skpg, upoac__skpg.nin)
        overload(upoac__skpg, no_unliteral=True)(hvnp__ywvsc)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        hvnp__ywvsc = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(hvnp__ywvsc)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        hvnp__ywvsc = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(hvnp__ywvsc)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        hvnp__ywvsc = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(hvnp__ywvsc)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        vjze__dgmqo = []
        xkxv__dlas = False
        fvm__vwos = False
        zrz__nfm = False
        for abk__swqc in range(len(A)):
            if bodo.libs.array_kernels.isna(A, abk__swqc):
                if not xkxv__dlas:
                    data.append(False)
                    vjze__dgmqo.append(False)
                    xkxv__dlas = True
                continue
            val = A[abk__swqc]
            if val and not fvm__vwos:
                data.append(True)
                vjze__dgmqo.append(True)
                fvm__vwos = True
            if not val and not zrz__nfm:
                data.append(False)
                vjze__dgmqo.append(True)
                zrz__nfm = True
            if xkxv__dlas and fvm__vwos and zrz__nfm:
                break
        hvu__phls = np.array(data)
        n = len(hvu__phls)
        ckn__ushah = 1
        ngj__buw = np.empty(ckn__ushah, np.uint8)
        for dql__jhwmp in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(ngj__buw, dql__jhwmp,
                vjze__dgmqo[dql__jhwmp])
        return init_bool_array(hvu__phls, ngj__buw)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType, bodo.libs.float_arr_ext.
        FloatingArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        libs.array_item_arr_ext.ArrayItemArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.tuple_arr_ext.TupleArrayType, bodo.
        CategoricalArrayType, bodo.TimeArrayType, bodo.DecimalArrayType,
        bodo.DatetimeArrayType)) or A in (string_array_type, bodo.hiframes.
        split_impl.string_array_split_view_type, boolean_array, bodo.
        datetime_date_array_type, bodo.datetime_timedelta_array_type, bodo.
        binary_array_type)):

        def impl(A, ind):
            bzfq__hqjgb = bodo.utils.conversion.nullable_bool_to_bool_na_false(
                ind)
            return A[bzfq__hqjgb]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    puf__xruw = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, puf__xruw)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    gpc__vcpvs = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        orou__dkq = bodo.utils.utils.is_array_typ(val1, False)
        wlc__ywbds = bodo.utils.utils.is_array_typ(val2, False)
        qma__bek = 'val1' if orou__dkq else 'val2'
        wpb__gcth = 'def impl(val1, val2):\n'
        wpb__gcth += f'  n = len({qma__bek})\n'
        wpb__gcth += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        wpb__gcth += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if orou__dkq:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            tegya__smv = 'val1[i]'
        else:
            null1 = 'False\n'
            tegya__smv = 'val1'
        if wlc__ywbds:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            ueb__ntsv = 'val2[i]'
        else:
            null2 = 'False\n'
            ueb__ntsv = 'val2'
        if gpc__vcpvs:
            wpb__gcth += f"""    result, isna_val = compute_or_body({null1}, {null2}, {tegya__smv}, {ueb__ntsv})
"""
        else:
            wpb__gcth += f"""    result, isna_val = compute_and_body({null1}, {null2}, {tegya__smv}, {ueb__ntsv})
"""
        wpb__gcth += '    out_arr[i] = result\n'
        wpb__gcth += '    if isna_val:\n'
        wpb__gcth += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        wpb__gcth += '      continue\n'
        wpb__gcth += '  return out_arr\n'
        ozne__rnbue = {}
        exec(wpb__gcth, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, ozne__rnbue)
        impl = ozne__rnbue['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        ilddu__xvek = boolean_array
        return ilddu__xvek(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    kpgk__mpbzh = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return kpgk__mpbzh


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        jqon__yhx = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(jqon__yhx)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(jqon__yhx)


_install_nullable_logical_lowering()
