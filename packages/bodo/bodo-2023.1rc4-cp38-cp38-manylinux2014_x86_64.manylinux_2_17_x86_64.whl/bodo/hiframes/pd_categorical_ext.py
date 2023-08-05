import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        ntlig__adod = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=ntlig__adod)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    dvl__bxrn = tuple(val.categories.values)
    elem_type = None if len(dvl__bxrn) == 0 else bodo.typeof(val.categories
        .values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(dvl__bxrn, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iwc__pjkx = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, iwc__pjkx)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    vgzoh__iyvci = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    ujnwt__wcpno = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, utoia__zcfp, utoia__zcfp = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    qwhl__bdvzk = PDCategoricalDtype(ujnwt__wcpno, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, vgzoh__iyvci)
    return qwhl__bdvzk(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cdbis__kfbd = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, cdbis__kfbd).value
    c.pyapi.decref(cdbis__kfbd)
    mkz__pkx = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, mkz__pkx).value
    c.pyapi.decref(mkz__pkx)
    vwbwk__iif = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=vwbwk__iif)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    cdbis__kfbd = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    aroi__ivj = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c
        .env_manager)
    wsa__poyo = c.context.insert_const_string(c.builder.module, 'pandas')
    eijsl__sovah = c.pyapi.import_module_noblock(wsa__poyo)
    xbit__plynf = c.pyapi.call_method(eijsl__sovah, 'CategoricalDtype', (
        aroi__ivj, cdbis__kfbd))
    c.pyapi.decref(cdbis__kfbd)
    c.pyapi.decref(aroi__ivj)
    c.pyapi.decref(eijsl__sovah)
    c.context.nrt.decref(c.builder, typ, val)
    return xbit__plynf


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rxrq__exvb = get_categories_int_type(fe_type.dtype)
        iwc__pjkx = [('dtype', fe_type.dtype), ('codes', types.Array(
            rxrq__exvb, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, iwc__pjkx)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    yskmp__rjcw = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), yskmp__rjcw
        ).value
    c.pyapi.decref(yskmp__rjcw)
    xbit__plynf = c.pyapi.object_getattr_string(val, 'dtype')
    cob__roq = c.pyapi.to_native_value(typ.dtype, xbit__plynf).value
    c.pyapi.decref(xbit__plynf)
    iggm__kvl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    iggm__kvl.codes = codes
    iggm__kvl.dtype = cob__roq
    return NativeValue(iggm__kvl._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    wvfq__kvl = get_categories_int_type(typ.dtype)
    tsr__rnn = context.get_constant_generic(builder, types.Array(wvfq__kvl,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, tsr__rnn])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    qmkg__xthme = len(cat_dtype.categories)
    if qmkg__xthme < np.iinfo(np.int8).max:
        dtype = types.int8
    elif qmkg__xthme < np.iinfo(np.int16).max:
        dtype = types.int16
    elif qmkg__xthme < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    wsa__poyo = c.context.insert_const_string(c.builder.module, 'pandas')
    eijsl__sovah = c.pyapi.import_module_noblock(wsa__poyo)
    rxrq__exvb = get_categories_int_type(dtype)
    losxe__rul = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    oqj__ifjvp = types.Array(rxrq__exvb, 1, 'C')
    c.context.nrt.incref(c.builder, oqj__ifjvp, losxe__rul.codes)
    yskmp__rjcw = c.pyapi.from_native_value(oqj__ifjvp, losxe__rul.codes, c
        .env_manager)
    c.context.nrt.incref(c.builder, dtype, losxe__rul.dtype)
    xbit__plynf = c.pyapi.from_native_value(dtype, losxe__rul.dtype, c.
        env_manager)
    gfbwt__sur = c.pyapi.borrow_none()
    tgy__ukec = c.pyapi.object_getattr_string(eijsl__sovah, 'Categorical')
    ybk__qfmal = c.pyapi.call_method(tgy__ukec, 'from_codes', (yskmp__rjcw,
        gfbwt__sur, gfbwt__sur, xbit__plynf))
    c.pyapi.decref(tgy__ukec)
    c.pyapi.decref(yskmp__rjcw)
    c.pyapi.decref(xbit__plynf)
    c.pyapi.decref(eijsl__sovah)
    c.context.nrt.decref(c.builder, typ, val)
    return ybk__qfmal


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            rgg__jodgl = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                lfxnv__coc = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), rgg__jodgl)
                return lfxnv__coc
            return impl_lit

        def impl(A, other):
            rgg__jodgl = get_code_for_value(A.dtype, other)
            lfxnv__coc = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), rgg__jodgl)
            return lfxnv__coc
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        vhz__uhq = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(vhz__uhq)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    losxe__rul = cat_dtype.categories
    n = len(losxe__rul)
    for oidc__udio in range(n):
        if losxe__rul[oidc__udio] == val:
            return oidc__udio
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    lbxkk__tvea = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if lbxkk__tvea != A.dtype.elem_type and lbxkk__tvea != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if lbxkk__tvea == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            lfxnv__coc = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for oidc__udio in numba.parfors.parfor.internal_prange(n):
                azs__uwow = codes[oidc__udio]
                if azs__uwow == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(lfxnv__coc
                            , oidc__udio)
                    else:
                        bodo.libs.array_kernels.setna(lfxnv__coc, oidc__udio)
                    continue
                lfxnv__coc[oidc__udio] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[azs__uwow]))
            return lfxnv__coc
        return impl
    oqj__ifjvp = dtype_to_array_type(lbxkk__tvea)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        lfxnv__coc = bodo.utils.utils.alloc_type(n, oqj__ifjvp, (-1,))
        for oidc__udio in numba.parfors.parfor.internal_prange(n):
            azs__uwow = codes[oidc__udio]
            if azs__uwow == -1:
                bodo.libs.array_kernels.setna(lfxnv__coc, oidc__udio)
                continue
            lfxnv__coc[oidc__udio
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[azs__uwow])
        return lfxnv__coc
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        miba__qmcin, cob__roq = args
        losxe__rul = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        losxe__rul.codes = miba__qmcin
        losxe__rul.dtype = cob__roq
        context.nrt.incref(builder, signature.args[0], miba__qmcin)
        context.nrt.incref(builder, signature.args[1], cob__roq)
        return losxe__rul._getvalue()
    iyrv__sei = CategoricalArrayType(cat_dtype)
    sig = iyrv__sei(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    mvbn__bkjt = args[0]
    if equiv_set.has_shape(mvbn__bkjt):
        return ArrayAnalysis.AnalyzeResult(shape=mvbn__bkjt, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    rxrq__exvb = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, rxrq__exvb)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            dyujb__eieay = {}
            tsr__rnn = np.empty(n + 1, np.int64)
            jfebj__janyx = {}
            vmjcc__vstyq = []
            hhc__wokgu = {}
            for oidc__udio in range(n):
                hhc__wokgu[categories[oidc__udio]] = oidc__udio
            for jbxc__hcw in to_replace:
                if jbxc__hcw != value:
                    if jbxc__hcw in hhc__wokgu:
                        if value in hhc__wokgu:
                            dyujb__eieay[jbxc__hcw] = jbxc__hcw
                            sux__xxm = hhc__wokgu[jbxc__hcw]
                            jfebj__janyx[sux__xxm] = hhc__wokgu[value]
                            vmjcc__vstyq.append(sux__xxm)
                        else:
                            dyujb__eieay[jbxc__hcw] = value
                            hhc__wokgu[value] = hhc__wokgu[jbxc__hcw]
            spjze__cmp = np.sort(np.array(vmjcc__vstyq))
            dqc__lmtg = 0
            judsu__nnwo = []
            for hoo__vhfrv in range(-1, n):
                while dqc__lmtg < len(spjze__cmp) and hoo__vhfrv > spjze__cmp[
                    dqc__lmtg]:
                    dqc__lmtg += 1
                judsu__nnwo.append(dqc__lmtg)
            for vdgdx__sgpa in range(-1, n):
                xil__tqpbf = vdgdx__sgpa
                if vdgdx__sgpa in jfebj__janyx:
                    xil__tqpbf = jfebj__janyx[vdgdx__sgpa]
                tsr__rnn[vdgdx__sgpa + 1] = xil__tqpbf - judsu__nnwo[
                    xil__tqpbf + 1]
            return dyujb__eieay, tsr__rnn, len(spjze__cmp)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for oidc__udio in range(len(new_codes_arr)):
        new_codes_arr[oidc__udio] = codes_map_arr[old_codes_arr[oidc__udio] + 1
            ]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    hvlk__jaxef = arr.dtype.ordered
    nttj__mak = arr.dtype.elem_type
    ccnoe__kftwv = get_overload_const(to_replace)
    kvj__xvn = get_overload_const(value)
    if (arr.dtype.categories is not None and ccnoe__kftwv is not
        NOT_CONSTANT and kvj__xvn is not NOT_CONSTANT):
        kmyve__jaiq, codes_map_arr, utoia__zcfp = python_build_replace_dicts(
            ccnoe__kftwv, kvj__xvn, arr.dtype.categories)
        if len(kmyve__jaiq) == 0:
            return lambda arr, to_replace, value: arr.copy()
        hospe__lcif = []
        for iqjh__mkgqr in arr.dtype.categories:
            if iqjh__mkgqr in kmyve__jaiq:
                ozbp__fkl = kmyve__jaiq[iqjh__mkgqr]
                if ozbp__fkl != iqjh__mkgqr:
                    hospe__lcif.append(ozbp__fkl)
            else:
                hospe__lcif.append(iqjh__mkgqr)
        fpktl__tjxy = bodo.utils.utils.create_categorical_type(hospe__lcif,
            arr.dtype.data.data, hvlk__jaxef)
        tam__szaf = MetaType(tuple(fpktl__tjxy))

        def impl_dtype(arr, to_replace, value):
            qqkze__jfm = init_cat_dtype(bodo.utils.conversion.
                index_from_array(fpktl__tjxy), hvlk__jaxef, None, tam__szaf)
            losxe__rul = alloc_categorical_array(len(arr.codes), qqkze__jfm)
            reassign_codes(losxe__rul.codes, arr.codes, codes_map_arr)
            return losxe__rul
        return impl_dtype
    nttj__mak = arr.dtype.elem_type
    if nttj__mak == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            dyujb__eieay, codes_map_arr, pez__cktc = build_replace_dicts(
                to_replace, value, categories.values)
            if len(dyujb__eieay) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), hvlk__jaxef,
                    None, None))
            n = len(categories)
            fpktl__tjxy = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                pez__cktc, -1)
            bqtro__swx = 0
            for hoo__vhfrv in range(n):
                cjf__jzl = categories[hoo__vhfrv]
                if cjf__jzl in dyujb__eieay:
                    qecci__fdv = dyujb__eieay[cjf__jzl]
                    if qecci__fdv != cjf__jzl:
                        fpktl__tjxy[bqtro__swx] = qecci__fdv
                        bqtro__swx += 1
                else:
                    fpktl__tjxy[bqtro__swx] = cjf__jzl
                    bqtro__swx += 1
            losxe__rul = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                fpktl__tjxy), hvlk__jaxef, None, None))
            reassign_codes(losxe__rul.codes, arr.codes, codes_map_arr)
            return losxe__rul
        return impl_str
    hhlai__btr = dtype_to_array_type(nttj__mak)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        dyujb__eieay, codes_map_arr, pez__cktc = build_replace_dicts(to_replace
            , value, categories.values)
        if len(dyujb__eieay) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), hvlk__jaxef, None, None))
        n = len(categories)
        fpktl__tjxy = bodo.utils.utils.alloc_type(n - pez__cktc, hhlai__btr,
            None)
        bqtro__swx = 0
        for oidc__udio in range(n):
            cjf__jzl = categories[oidc__udio]
            if cjf__jzl in dyujb__eieay:
                qecci__fdv = dyujb__eieay[cjf__jzl]
                if qecci__fdv != cjf__jzl:
                    fpktl__tjxy[bqtro__swx] = qecci__fdv
                    bqtro__swx += 1
            else:
                fpktl__tjxy[bqtro__swx] = cjf__jzl
                bqtro__swx += 1
        losxe__rul = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(fpktl__tjxy),
            hvlk__jaxef, None, None))
        reassign_codes(losxe__rul.codes, arr.codes, codes_map_arr)
        return losxe__rul
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    nwt__jhyq = dict()
    gzlo__bowe = 0
    for oidc__udio in range(len(vals)):
        val = vals[oidc__udio]
        if val in nwt__jhyq:
            continue
        nwt__jhyq[val] = gzlo__bowe
        gzlo__bowe += 1
    return nwt__jhyq


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    nwt__jhyq = dict()
    for oidc__udio in range(len(vals)):
        val = vals[oidc__udio]
        nwt__jhyq[val] = oidc__udio
    return nwt__jhyq


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    xrngy__dqxvb = dict(fastpath=fastpath)
    ipyhr__shg = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', xrngy__dqxvb, ipyhr__shg)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        zbrak__akivc = get_overload_const(categories)
        if zbrak__akivc is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                hpb__ihbx = False
            else:
                hpb__ihbx = get_overload_const_bool(ordered)
            dwfmu__pizcj = pd.CategoricalDtype(pd.array(zbrak__akivc),
                hpb__ihbx).categories.array
            rag__bdcy = MetaType(tuple(dwfmu__pizcj))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                qqkze__jfm = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(dwfmu__pizcj), hpb__ihbx, None, rag__bdcy)
                return bodo.utils.conversion.fix_arr_dtype(data, qqkze__jfm)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            dvl__bxrn = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                dvl__bxrn, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            bvw__widxm = arr.codes[ind]
            return arr.dtype.categories[max(bvw__widxm, 0)]
        return categorical_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
            )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for oidc__udio in range(len(arr1)):
        if arr1[oidc__udio] != arr2[oidc__udio]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    pnmj__uhgyf = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    ipp__uhnq = not isinstance(val, CategoricalArrayType) and is_iterable_type(
        val) and is_common_scalar_dtype([val.dtype, arr.dtype.elem_type]
        ) and not (isinstance(arr.dtype.elem_type, types.Integer) and
        isinstance(val.dtype, types.Float))
    phld__xpnb = categorical_arrs_match(arr, val)
    shp__vgjpr = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    bti__pnaxo = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not pnmj__uhgyf:
            raise BodoError(shp__vgjpr)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            bvw__widxm = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = bvw__widxm
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (pnmj__uhgyf or ipp__uhnq or phld__xpnb !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(shp__vgjpr)
        if phld__xpnb == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bti__pnaxo)
        if pnmj__uhgyf:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lph__ijrs = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for hoo__vhfrv in range(n):
                    arr.codes[ind[hoo__vhfrv]] = lph__ijrs
            return impl_scalar
        if phld__xpnb == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for oidc__udio in range(n):
                    arr.codes[ind[oidc__udio]] = val.codes[oidc__udio]
            return impl_arr_ind_mask
        if phld__xpnb == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bti__pnaxo)
                n = len(val.codes)
                for oidc__udio in range(n):
                    arr.codes[ind[oidc__udio]] = val.codes[oidc__udio]
            return impl_arr_ind_mask
        if ipp__uhnq:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for hoo__vhfrv in range(n):
                    bpq__wwsi = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[hoo__vhfrv]))
                    if bpq__wwsi not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    bvw__widxm = categories.get_loc(bpq__wwsi)
                    arr.codes[ind[hoo__vhfrv]] = bvw__widxm
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (pnmj__uhgyf or ipp__uhnq or phld__xpnb !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(shp__vgjpr)
        if phld__xpnb == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bti__pnaxo)
        if pnmj__uhgyf:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lph__ijrs = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for hoo__vhfrv in range(n):
                    if ind[hoo__vhfrv]:
                        arr.codes[hoo__vhfrv] = lph__ijrs
            return impl_scalar
        if phld__xpnb == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                ymq__gkfw = 0
                for oidc__udio in range(n):
                    if ind[oidc__udio]:
                        arr.codes[oidc__udio] = val.codes[ymq__gkfw]
                        ymq__gkfw += 1
            return impl_bool_ind_mask
        if phld__xpnb == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bti__pnaxo)
                n = len(ind)
                ymq__gkfw = 0
                for oidc__udio in range(n):
                    if ind[oidc__udio]:
                        arr.codes[oidc__udio] = val.codes[ymq__gkfw]
                        ymq__gkfw += 1
            return impl_bool_ind_mask
        if ipp__uhnq:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                ymq__gkfw = 0
                categories = arr.dtype.categories
                for hoo__vhfrv in range(n):
                    if ind[hoo__vhfrv]:
                        bpq__wwsi = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[ymq__gkfw]))
                        if bpq__wwsi not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        bvw__widxm = categories.get_loc(bpq__wwsi)
                        arr.codes[hoo__vhfrv] = bvw__widxm
                        ymq__gkfw += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (pnmj__uhgyf or ipp__uhnq or phld__xpnb !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(shp__vgjpr)
        if phld__xpnb == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(bti__pnaxo)
        if pnmj__uhgyf:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                lph__ijrs = arr.dtype.categories.get_loc(val)
                updus__rmg = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for hoo__vhfrv in range(updus__rmg.start, updus__rmg.stop,
                    updus__rmg.step):
                    arr.codes[hoo__vhfrv] = lph__ijrs
            return impl_scalar
        if phld__xpnb == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if phld__xpnb == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(bti__pnaxo)
                arr.codes[ind] = val.codes
            return impl_arr
        if ipp__uhnq:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                updus__rmg = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                ymq__gkfw = 0
                for hoo__vhfrv in range(updus__rmg.start, updus__rmg.stop,
                    updus__rmg.step):
                    bpq__wwsi = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[ymq__gkfw]))
                    if bpq__wwsi not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    bvw__widxm = categories.get_loc(bpq__wwsi)
                    arr.codes[hoo__vhfrv] = bvw__widxm
                    ymq__gkfw += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
