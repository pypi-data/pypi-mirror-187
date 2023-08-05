import datetime
import operator
import warnings
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_nan, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
from bodo.utils.utils import is_null_value
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')
idx_cpy_arg_defaults = dict(deep=False, dtype=None, names=None)
idx_typ_to_format_str_map = dict()


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        if isinstance(val.dtype, pd.core.arrays.integer._IntegerDtype):
            nhi__qbkvl = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(nhi__qbkvl)
        else:
            dtype = types.int64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), IntegerArrayType(dtype))
    if val.inferred_type == 'floating' or pd._libs.lib.infer_dtype(val, True
        ) == 'floating':
        if isinstance(val.dtype, (pd.Float32Dtype, pd.Float64Dtype)):
            nhi__qbkvl = val.dtype.numpy_dtype
            dtype = numba.np.numpy_support.from_dtype(nhi__qbkvl)
        else:
            dtype = types.float64
        return NumericIndexType(dtype, get_val_type_maybe_str_literal(val.
            name), FloatingArrayType(dtype))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C'
            ) if data is None else data
        super(DatetimeIndexType, self).__init__(name=
            f'DatetimeIndex({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def tzval(self):
        return self.data.tz if isinstance(self.data, bodo.DatetimeArrayType
            ) else None

    def copy(self):
        return DatetimeIndexType(self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, bodo.hiframes.
            pd_timestamp_ext.PandasTimestampType(self.tzval))

    @property
    def pandas_type_name(self):
        return self.data.dtype.type_name

    @property
    def numpy_type_name(self):
        return str(self.data.dtype)


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    if isinstance(val.dtype, pd.DatetimeTZDtype):
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name),
            DatetimeArrayType(val.tz))
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    wqj__upal = idx_typ_to_format_str_map[DatetimeIndexType].format('copy()')
    check_unsupported_args('copy', txbf__uarz, idx_cpy_arg_defaults, fn_str
        =wqj__upal, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_datetime_index(A._data.
                copy(), A._name)
    return impl


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    dyz__eerx = c.pyapi.import_module_noblock(enkrv__detyn)
    enxes__oew = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, enxes__oew.data)
    lolq__cjdz = c.pyapi.from_native_value(typ.data, enxes__oew.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, enxes__oew.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, enxes__oew.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([lolq__cjdz])
    rpg__szobi = c.pyapi.object_getattr_string(dyz__eerx, 'DatetimeIndex')
    kws = c.pyapi.dict_pack([('name', rnf__llyv)])
    nllyu__nhxia = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(lolq__cjdz)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(dyz__eerx)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nllyu__nhxia


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        agpt__oxcxk = c.pyapi.object_getattr_string(val, 'array')
    else:
        agpt__oxcxk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, agpt__oxcxk).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    dtype = _dt_index_data_typ.dtype
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    plcba__tjph.dict = zmjeo__khhr
    c.pyapi.decref(agpt__oxcxk)
    c.pyapi.decref(rnf__llyv)
    return NativeValue(plcba__tjph._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ttl__wup, amf__eyfm = args
        enxes__oew = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        enxes__oew.data = ttl__wup
        enxes__oew.name = amf__eyfm
        context.nrt.incref(builder, signature.args[0], ttl__wup)
        context.nrt.incref(builder, signature.args[1], amf__eyfm)
        dtype = _dt_index_data_typ.dtype
        enxes__oew.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return enxes__oew._getvalue()
    wfz__foc = DatetimeIndexType(name, data)
    sig = signature(wfz__foc, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    cjn__ltm = args[0]
    if equiv_set.has_shape(cjn__ltm):
        return ArrayAnalysis.AnalyzeResult(shape=cjn__ltm, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    pqv__pgou = 'def impl(dti):\n'
    pqv__pgou += '    numba.parfors.parfor.init_prange()\n'
    pqv__pgou += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    pqv__pgou += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    pqv__pgou += '    n = len(A)\n'
    pqv__pgou += '    S = np.empty(n, np.int64)\n'
    pqv__pgou += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    pqv__pgou += '        val = A[i]\n'
    pqv__pgou += '        ts = bodo.utils.conversion.box_if_dt64(val)\n'
    if field in ['weekday']:
        pqv__pgou += '        S[i] = ts.' + field + '()\n'
    else:
        pqv__pgou += '        S[i] = ts.' + field + '\n'
    pqv__pgou += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    oabp__flzcb = {}
    exec(pqv__pgou, {'numba': numba, 'np': np, 'bodo': bodo}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        aajz__oku = len(A)
        S = np.empty(aajz__oku, np.bool_)
        for i in numba.parfors.parfor.internal_prange(aajz__oku):
            val = A[i]
            iel__kvrk = bodo.utils.conversion.box_if_dt64(val)
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(iel__kvrk.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        aajz__oku = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(aajz__oku
            )
        for i in numba.parfors.parfor.internal_prange(aajz__oku):
            val = A[i]
            iel__kvrk = bodo.utils.conversion.box_if_dt64(val)
            S[i] = datetime.date(iel__kvrk.year, iel__kvrk.month, iel__kvrk.day
                )
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.min()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        ocyi__qfjdo = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(ocyi__qfjdo)):
            if not bodo.libs.array_kernels.isna(ocyi__qfjdo, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ocyi__qfjdo[i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(dti,
        'Index.max()')

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        ocyi__qfjdo = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(ocyi__qfjdo)):
            if not bodo.libs.array_kernels.isna(ocyi__qfjdo, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ocyi__qfjdo[i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):

    def impl(A, tz):
        return init_datetime_index(A._data.tz_convert(tz), A._name)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, tz=None, normalize=
    False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False,
    dtype=None, copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.DatetimeIndex()')
    ecalw__jpqna = dict(freq=freq, tz=tz, normalize=normalize, closed=
        closed, ambiguous=ambiguous, dayfirst=dayfirst, yearfirst=yearfirst,
        dtype=dtype, copy=copy)
    zbfeh__dabb = dict(freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False)
    check_unsupported_args('pandas.DatetimeIndex', ecalw__jpqna,
        zbfeh__dabb, package_name='pandas', module_name='Index')

    def f(data=None, freq=None, tz=None, normalize=False, closed=None,
        ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None,
        copy=False, name=None):
        unbi__lmx = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(unbi__lmx)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        qqydw__xhpp = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            ocyi__qfjdo = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            aajz__oku = len(ocyi__qfjdo)
            S = np.empty(aajz__oku, qqydw__xhpp)
            xfre__cje = rhs.value
            for i in numba.parfors.parfor.internal_prange(aajz__oku):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ocyi__qfjdo[i]) - xfre__cje)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        qqydw__xhpp = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            ocyi__qfjdo = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            aajz__oku = len(ocyi__qfjdo)
            S = np.empty(aajz__oku, qqydw__xhpp)
            xfre__cje = lhs.value
            for i in numba.parfors.parfor.internal_prange(aajz__oku):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    xfre__cje - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(ocyi__qfjdo[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    hom__vhig = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    pqv__pgou = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        pqv__pgou += '  dt_index, _str = lhs, rhs\n'
        vzcxg__ajzgw = 'arr[i] {} other'.format(hom__vhig)
    else:
        pqv__pgou += '  dt_index, _str = rhs, lhs\n'
        vzcxg__ajzgw = 'other {} arr[i]'.format(hom__vhig)
    pqv__pgou += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    pqv__pgou += '  l = len(arr)\n'
    pqv__pgou += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    pqv__pgou += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    pqv__pgou += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    pqv__pgou += '    S[i] = {}\n'.format(vzcxg__ajzgw)
    pqv__pgou += '  return S\n'
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'numba': numba, 'np': np}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'pandas.Index()')
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    if not is_overload_none(dtype):
        lvf__rxf = parse_dtype(dtype, 'pandas.Index')
        jrvh__ats = False
    else:
        lvf__rxf = getattr(data, 'dtype', None)
        jrvh__ats = True
    if isinstance(lvf__rxf, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType) or lvf__rxf == types.NPDatetime(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType) or lvf__rxf == types.NPTimedelta(
        'ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(lvf__rxf, (types.Integer, types.Float, types.Boolean)):
            if jrvh__ats:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    unbi__lmx = bodo.utils.conversion.coerce_to_array(data)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        unbi__lmx, name)
            else:

                def impl(data=None, dtype=None, copy=False, name=None,
                    tupleize_cols=True):
                    unbi__lmx = bodo.utils.conversion.coerce_to_array(data)
                    ldx__krbii = bodo.utils.conversion.fix_arr_dtype(unbi__lmx,
                        lvf__rxf)
                    return bodo.hiframes.pd_index_ext.init_numeric_index(
                        ldx__krbii, name)
        elif lvf__rxf in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                oeau__iaj = bodo.hiframes.pd_index_ext.get_index_data(dti)
                val = oeau__iaj[ind]
                return bodo.utils.conversion.box_if_dt64(val)
            return impl
        else:

            def impl(dti, ind):
                oeau__iaj = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                buoo__zxyt = oeau__iaj[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(
                    buoo__zxyt, name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            dbxc__tao = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(dbxc__tao[ind])
        return impl

    def impl(I, ind):
        dbxc__tao = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        buoo__zxyt = dbxc__tao[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(buoo__zxyt, name
            )
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_categorical_index_getitem(I, ind):
    if not isinstance(I, CategoricalIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            yrno__fec = bodo.hiframes.pd_index_ext.get_index_data(I)
            val = yrno__fec[ind]
            return val
        return impl
    if isinstance(ind, types.SliceType):

        def impl(I, ind):
            yrno__fec = bodo.hiframes.pd_index_ext.get_index_data(I)
            name = bodo.hiframes.pd_index_ext.get_index_name(I)
            buoo__zxyt = yrno__fec[ind]
            return bodo.hiframes.pd_index_ext.init_categorical_index(buoo__zxyt
                , name)
        return impl
    raise BodoError(
        f'pd.CategoricalIndex.__getitem__: unsupported index type {ind}')


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    jpfbr__ttcuo = False
    dthn__oggmj = False
    if closed is None:
        jpfbr__ttcuo = True
        dthn__oggmj = True
    elif closed == 'left':
        jpfbr__ttcuo = True
    elif closed == 'right':
        dthn__oggmj = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return jpfbr__ttcuo, dthn__oggmj


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, inline='always')
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    ecalw__jpqna = dict(tz=tz, normalize=normalize, closed=closed)
    zbfeh__dabb = dict(tz=None, normalize=False, closed=None)
    check_unsupported_args('pandas.date_range', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='General')
    if not is_overload_none(tz):
        raise_bodo_error('pd.date_range(): tz argument not supported yet')
    gcpjw__ucuau = ''
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
        gcpjw__ucuau = "  freq = 'D'\n"
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise_bodo_error(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )
    pqv__pgou = """def f(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None):
"""
    pqv__pgou += gcpjw__ucuau
    if is_overload_none(start):
        pqv__pgou += "  start_t = pd.Timestamp('1800-01-03')\n"
    else:
        pqv__pgou += '  start_t = pd.Timestamp(start)\n'
    if is_overload_none(end):
        pqv__pgou += "  end_t = pd.Timestamp('1800-01-03')\n"
    else:
        pqv__pgou += '  end_t = pd.Timestamp(end)\n'
    if not is_overload_none(freq):
        pqv__pgou += (
            '  stride = bodo.hiframes.pd_index_ext.to_offset_value(freq)\n')
        if is_overload_none(periods):
            pqv__pgou += '  b = start_t.value\n'
            pqv__pgou += (
                '  e = b + (end_t.value - b) // stride * stride + stride // 2 + 1\n'
                )
        elif not is_overload_none(start):
            pqv__pgou += '  b = start_t.value\n'
            pqv__pgou += '  addend = np.int64(periods) * np.int64(stride)\n'
            pqv__pgou += '  e = np.int64(b) + addend\n'
        elif not is_overload_none(end):
            pqv__pgou += '  e = end_t.value + stride\n'
            pqv__pgou += '  addend = np.int64(periods) * np.int64(-stride)\n'
            pqv__pgou += '  b = np.int64(e) + addend\n'
        else:
            raise_bodo_error(
                "at least 'start' or 'end' should be specified if a 'period' is given."
                )
        pqv__pgou += '  arr = np.arange(b, e, stride, np.int64)\n'
    else:
        pqv__pgou += '  delta = end_t.value - start_t.value\n'
        pqv__pgou += '  step = delta / (periods - 1)\n'
        pqv__pgou += '  arr1 = np.arange(0, periods, 1, np.float64)\n'
        pqv__pgou += '  arr1 *= step\n'
        pqv__pgou += '  arr1 += start_t.value\n'
        pqv__pgou += '  arr = arr1.astype(np.int64)\n'
        pqv__pgou += '  arr[-1] = end_t.value\n'
    pqv__pgou += '  A = bodo.utils.conversion.convert_to_dt64ns(arr)\n'
    pqv__pgou += (
        '  return bodo.hiframes.pd_index_ext.init_datetime_index(A, name)\n')
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'np': np, 'pd': pd}, oabp__flzcb)
    f = oabp__flzcb['f']
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        kfqhw__lxau = pd.Timedelta('1 day')
        if start is not None:
            kfqhw__lxau = pd.Timedelta(start)
        hjzwo__mzm = pd.Timedelta('1 day')
        if end is not None:
            hjzwo__mzm = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        jpfbr__ttcuo, dthn__oggmj = (bodo.hiframes.pd_index_ext.
            validate_endpoints(closed))
        if freq is not None:
            cgrv__zhyy = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = kfqhw__lxau.value
                yfeap__zym = b + (hjzwo__mzm.value - b
                    ) // cgrv__zhyy * cgrv__zhyy + cgrv__zhyy // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = kfqhw__lxau.value
                cks__bjse = np.int64(periods) * np.int64(cgrv__zhyy)
                yfeap__zym = np.int64(b) + cks__bjse
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                yfeap__zym = hjzwo__mzm.value + cgrv__zhyy
                cks__bjse = np.int64(periods) * np.int64(-cgrv__zhyy)
                b = np.int64(yfeap__zym) + cks__bjse
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            yczec__qqg = np.arange(b, yfeap__zym, cgrv__zhyy, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            kzdx__hha = hjzwo__mzm.value - kfqhw__lxau.value
            step = kzdx__hha / (periods - 1)
            gfyj__ydc = np.arange(0, periods, 1, np.float64)
            gfyj__ydc *= step
            gfyj__ydc += kfqhw__lxau.value
            yczec__qqg = gfyj__ydc.astype(np.int64)
            yczec__qqg[-1] = hjzwo__mzm.value
        if not jpfbr__ttcuo and len(yczec__qqg) and yczec__qqg[0
            ] == kfqhw__lxau.value:
            yczec__qqg = yczec__qqg[1:]
        if not dthn__oggmj and len(yczec__qqg) and yczec__qqg[-1
            ] == hjzwo__mzm.value:
            yczec__qqg = yczec__qqg[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(yczec__qqg)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):
    bsz__kyoey = ColNamesMetaType(('year', 'week', 'day'))

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        aajz__oku = len(A)
        theow__gnut = bodo.libs.int_arr_ext.alloc_int_array(aajz__oku, np.
            uint32)
        zif__zwn = bodo.libs.int_arr_ext.alloc_int_array(aajz__oku, np.uint32)
        tju__xfxy = bodo.libs.int_arr_ext.alloc_int_array(aajz__oku, np.uint32)
        for i in numba.parfors.parfor.internal_prange(aajz__oku):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(theow__gnut, i)
                bodo.libs.array_kernels.setna(zif__zwn, i)
                bodo.libs.array_kernels.setna(tju__xfxy, i)
                continue
            theow__gnut[i], zif__zwn[i], tju__xfxy[i
                ] = bodo.utils.conversion.box_if_dt64(A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((theow__gnut,
            zif__zwn, tju__xfxy), idx, bsz__kyoey)
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C'
            ) if data is None else data
        super(TimedeltaIndexType, self).__init__(name=
            f'TimedeltaIndexType({name_typ}, {self.data})')
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ, self.data

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, bodo.pd_timedelta_type
            )

    @property
    def pandas_type_name(self):
        return 'timedelta'

    @property
    def numpy_type_name(self):
        return 'timedelta64[ns]'


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', _timedelta_index_data_typ), ('name', fe_type.
            name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, nhbb__txv)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    dyz__eerx = c.pyapi.import_module_noblock(enkrv__detyn)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    lolq__cjdz = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([lolq__cjdz])
    kws = c.pyapi.dict_pack([('name', rnf__llyv)])
    rpg__szobi = c.pyapi.object_getattr_string(dyz__eerx, 'TimedeltaIndex')
    nllyu__nhxia = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(lolq__cjdz)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(dyz__eerx)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nllyu__nhxia


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    cfsds__dykk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, cfsds__dykk
        ).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(cfsds__dykk)
    c.pyapi.decref(rnf__llyv)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    dtype = _timedelta_index_data_typ.dtype
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ttl__wup, amf__eyfm = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = ttl__wup
        timedelta_index.name = amf__eyfm
        context.nrt.incref(builder, signature.args[0], ttl__wup)
        context.nrt.incref(builder, signature.args[1], amf__eyfm)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    wfz__foc = TimedeltaIndexType(name)
    sig = signature(wfz__foc, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    wqj__upal = idx_typ_to_format_str_map[TimedeltaIndexType].format('copy()')
    check_unsupported_args('TimedeltaIndex.copy', txbf__uarz,
        idx_cpy_arg_defaults, fn_str=wqj__upal, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_timedelta_index(A._data.
                copy(), A._name)
    return impl


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        aajz__oku = len(data)
        avazy__fgd = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(aajz__oku):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            avazy__fgd = min(avazy__fgd, val)
        gtmpg__kqzrl = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            avazy__fgd)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(gtmpg__kqzrl, count
            )
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        aajz__oku = len(data)
        uzu__lcg = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(aajz__oku):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            uzu__lcg = max(uzu__lcg, val)
        gtmpg__kqzrl = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            uzu__lcg)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(gtmpg__kqzrl, count
            )
    return impl


def gen_tdi_field_impl(field):
    pqv__pgou = 'def impl(tdi):\n'
    pqv__pgou += '    numba.parfors.parfor.init_prange()\n'
    pqv__pgou += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    pqv__pgou += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    pqv__pgou += '    n = len(A)\n'
    pqv__pgou += '    S = np.empty(n, np.int64)\n'
    pqv__pgou += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    pqv__pgou += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        pqv__pgou += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        pqv__pgou += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        pqv__pgou += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        pqv__pgou += '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n'
    else:
        assert False, 'invalid timedelta field'
    pqv__pgou += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    oabp__flzcb = {}
    exec(pqv__pgou, {'numba': numba, 'np': np, 'bodo': bodo}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, dtype=None,
    copy=False, name=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    ecalw__jpqna = dict(unit=unit, freq=freq, dtype=dtype, copy=copy)
    zbfeh__dabb = dict(unit=None, freq=None, dtype=None, copy=False)
    check_unsupported_args('pandas.TimedeltaIndex', ecalw__jpqna,
        zbfeh__dabb, package_name='pandas', module_name='Index')

    def impl(data=None, unit=None, freq=None, dtype=None, copy=False, name=None
        ):
        unbi__lmx = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(unbi__lmx)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        if name_typ is None:
            name_typ = types.none
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name=f'RangeIndexType({name_typ})'
            )
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('start', types.int64), ('stop', types.int64), ('step',
            types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    wqj__upal = idx_typ_to_format_str_map[RangeIndexType].format('copy()')
    check_unsupported_args('RangeIndex.copy', txbf__uarz,
        idx_cpy_arg_defaults, fn_str=wqj__upal, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_range_index(A._start, A.
                _stop, A._step, A._name)
    return impl


@box(RangeIndexType)
def box_range_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    hvx__rojhl = c.pyapi.import_module_noblock(enkrv__detyn)
    gdt__cvxeh = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    mwgad__amw = c.pyapi.from_native_value(types.int64, gdt__cvxeh.start, c
        .env_manager)
    pwtyo__ksaa = c.pyapi.from_native_value(types.int64, gdt__cvxeh.stop, c
        .env_manager)
    rqlz__babok = c.pyapi.from_native_value(types.int64, gdt__cvxeh.step, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, gdt__cvxeh.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, gdt__cvxeh.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([mwgad__amw, pwtyo__ksaa, rqlz__babok])
    kws = c.pyapi.dict_pack([('name', rnf__llyv)])
    rpg__szobi = c.pyapi.object_getattr_string(hvx__rojhl, 'RangeIndex')
    lddh__wexht = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(mwgad__amw)
    c.pyapi.decref(pwtyo__ksaa)
    c.pyapi.decref(rqlz__babok)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(hvx__rojhl)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return lddh__wexht


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name
    zemnj__ejjp = is_overload_constant_int(step) and get_overload_const_int(
        step) == 0

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        if zemnj__ejjp:
            raise_bodo_error('Step must not be zero')
        jxiz__gthax = cgutils.is_scalar_zero(builder, args[2])
        zxd__nuvl = context.get_python_api(builder)
        with builder.if_then(jxiz__gthax):
            zxd__nuvl.err_format('PyExc_ValueError', 'Step must not be zero')
            val = context.get_constant(types.int32, -1)
            builder.ret(val)
        gdt__cvxeh = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        gdt__cvxeh.start = args[0]
        gdt__cvxeh.stop = args[1]
        gdt__cvxeh.step = args[2]
        gdt__cvxeh.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return gdt__cvxeh._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, dbag__zwgk = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    mwgad__amw = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, mwgad__amw).value
    pwtyo__ksaa = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, pwtyo__ksaa).value
    rqlz__babok = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, rqlz__babok).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(mwgad__amw)
    c.pyapi.decref(pwtyo__ksaa)
    c.pyapi.decref(rqlz__babok)
    c.pyapi.decref(rnf__llyv)
    gdt__cvxeh = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gdt__cvxeh.start = start
    gdt__cvxeh.stop = stop
    gdt__cvxeh.step = step
    gdt__cvxeh.name = name
    return NativeValue(gdt__cvxeh._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    return lir.Constant.literal_struct([start, stop, step, name])


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None):

    def _ensure_int_or_none(value, field):
        yqxto__gpj = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(yqxto__gpj.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        yqxto__gpj = 'RangeIndex(...) must be called with integers'
        raise BodoError(yqxto__gpj)
    sapa__rlg = 'start'
    rhrmc__wwt = 'stop'
    baage__mncvm = 'step'
    if is_overload_none(start):
        sapa__rlg = '0'
    if is_overload_none(stop):
        rhrmc__wwt = 'start'
        sapa__rlg = '0'
    if is_overload_none(step):
        baage__mncvm = '1'
    pqv__pgou = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None):
"""
    pqv__pgou += '  return init_range_index({}, {}, {}, name)\n'.format(
        sapa__rlg, rhrmc__wwt, baage__mncvm)
    oabp__flzcb = {}
    exec(pqv__pgou, {'init_range_index': init_range_index}, oabp__flzcb)
    zfdju__stysi = oabp__flzcb['_pd_range_index_imp']
    return zfdju__stysi


@overload(pd.CategoricalIndex, no_unliteral=True, inline='always')
def categorical_index_overload(data=None, categories=None, ordered=None,
    dtype=None, copy=False, name=None):
    raise BodoError('pd.CategoricalIndex() initializer not yet supported.')


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                tifvb__vwd = numba.cpython.unicode._normalize_slice(idx, len(I)
                    )
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * tifvb__vwd.start
                stop = I._start + I._step * tifvb__vwd.stop
                step = I._step * tifvb__vwd.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'period[{self.freq}]'


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', bodo.IntegerArrayType(types.int64)), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    freq = A.freq
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    wqj__upal = idx_typ_to_format_str_map[PeriodIndexType].format('copy()')
    check_unsupported_args('PeriodIndex.copy', txbf__uarz,
        idx_cpy_arg_defaults, fn_str=wqj__upal, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), name, freq)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_period_index(A._data.
                copy(), A._name, freq)
    return impl


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ttl__wup, amf__eyfm, dbag__zwgk = args
        lumnm__uxc = signature.return_type
        vuoaw__ivb = cgutils.create_struct_proxy(lumnm__uxc)(context, builder)
        vuoaw__ivb.data = ttl__wup
        vuoaw__ivb.name = amf__eyfm
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        vuoaw__ivb.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return vuoaw__ivb._getvalue()
    lieub__vnw = get_overload_const_str(freq)
    wfz__foc = PeriodIndexType(lieub__vnw, name)
    sig = signature(wfz__foc, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    hvx__rojhl = c.pyapi.import_module_noblock(enkrv__detyn)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, bodo.IntegerArrayType(types.int64),
        plcba__tjph.data)
    agpt__oxcxk = c.pyapi.from_native_value(bodo.IntegerArrayType(types.
        int64), plcba__tjph.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, plcba__tjph.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, plcba__tjph.name, c
        .env_manager)
    zuo__pfvf = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', agpt__oxcxk), ('name', rnf__llyv),
        ('freq', zuo__pfvf)])
    rpg__szobi = c.pyapi.object_getattr_string(hvx__rojhl, 'PeriodIndex')
    lddh__wexht = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(agpt__oxcxk)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(zuo__pfvf)
    c.pyapi.decref(hvx__rojhl)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return lddh__wexht


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = bodo.IntegerArrayType(types.int64)
    zqwlj__gsrd = c.pyapi.object_getattr_string(val, 'asi8')
    wuh__dir = c.pyapi.call_method(val, 'isna', ())
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    dyz__eerx = c.pyapi.import_module_noblock(enkrv__detyn)
    prgc__qacr = c.pyapi.object_getattr_string(dyz__eerx, 'arrays')
    agpt__oxcxk = c.pyapi.call_method(prgc__qacr, 'IntegerArray', (
        zqwlj__gsrd, wuh__dir))
    data = c.pyapi.to_native_value(arr_typ, agpt__oxcxk).value
    c.pyapi.decref(zqwlj__gsrd)
    c.pyapi.decref(wuh__dir)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(dyz__eerx)
    c.pyapi.decref(prgc__qacr)
    c.pyapi.decref(agpt__oxcxk)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


class CategoricalIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'categorical'

    @property
    def numpy_type_name(self):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        return str(get_categories_int_type(self.dtype))

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self, self.dtype.elem_type)


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        udsjp__vtc = get_categories_int_type(fe_type.data.dtype)
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(udsjp__vtc, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type, nhbb__txv
            )


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    dyz__eerx = c.pyapi.import_module_noblock(enkrv__detyn)
    fpagn__yttad = numba.core.cgutils.create_struct_proxy(typ)(c.context, c
        .builder, val)
    c.context.nrt.incref(c.builder, typ.data, fpagn__yttad.data)
    lolq__cjdz = c.pyapi.from_native_value(typ.data, fpagn__yttad.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, fpagn__yttad.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, fpagn__yttad.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([lolq__cjdz])
    kws = c.pyapi.dict_pack([('name', rnf__llyv)])
    rpg__szobi = c.pyapi.object_getattr_string(dyz__eerx, 'CategoricalIndex')
    nllyu__nhxia = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(lolq__cjdz)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(dyz__eerx)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nllyu__nhxia


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    cfsds__dykk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, cfsds__dykk).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(cfsds__dykk)
    c.pyapi.decref(rnf__llyv)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        ttl__wup, amf__eyfm = args
        fpagn__yttad = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        fpagn__yttad.data = ttl__wup
        fpagn__yttad.name = amf__eyfm
        context.nrt.incref(builder, signature.args[0], ttl__wup)
        context.nrt.incref(builder, signature.args[1], amf__eyfm)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        fpagn__yttad.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return fpagn__yttad._getvalue()
    wfz__foc = CategoricalIndexType(data, name)
    sig = signature(wfz__foc, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    wqj__upal = idx_typ_to_format_str_map[CategoricalIndexType].format('copy()'
        )
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('CategoricalIndex.copy', txbf__uarz,
        idx_cpy_arg_defaults, fn_str=wqj__upal, package_name='pandas',
        module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_categorical_index(A.
                _data.copy(), A._name)
    return impl


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return f'interval[{self.data.arr_type.dtype}, right]'


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, nhbb__txv)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    dyz__eerx = c.pyapi.import_module_noblock(enkrv__detyn)
    svt__onoii = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, svt__onoii.data)
    lolq__cjdz = c.pyapi.from_native_value(typ.data, svt__onoii.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, svt__onoii.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, svt__onoii.name, c.
        env_manager)
    args = c.pyapi.tuple_pack([lolq__cjdz])
    kws = c.pyapi.dict_pack([('name', rnf__llyv)])
    rpg__szobi = c.pyapi.object_getattr_string(dyz__eerx, 'IntervalIndex')
    nllyu__nhxia = c.pyapi.call(rpg__szobi, args, kws)
    c.pyapi.decref(lolq__cjdz)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(dyz__eerx)
    c.pyapi.decref(rpg__szobi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nllyu__nhxia


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    cfsds__dykk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, cfsds__dykk).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(cfsds__dykk)
    c.pyapi.decref(rnf__llyv)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        ttl__wup, amf__eyfm = args
        svt__onoii = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        svt__onoii.data = ttl__wup
        svt__onoii.name = amf__eyfm
        context.nrt.incref(builder, signature.args[0], ttl__wup)
        context.nrt.incref(builder, signature.args[1], amf__eyfm)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        svt__onoii.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return svt__onoii._getvalue()
    wfz__foc = IntervalIndexType(data, name)
    sig = signature(wfz__foc, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    Int64Index = pd.Int64Index
    UInt64Index = pd.UInt64Index
    Float64Index = pd.Float64Index


@typeof_impl.register(Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A, name=None, deep=False, dtype=None, names
    =None):
    wqj__upal = idx_typ_to_format_str_map[NumericIndexType].format('copy()')
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', txbf__uarz, idx_cpy_arg_defaults,
        fn_str=wqj__upal, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    hvx__rojhl = c.pyapi.import_module_noblock(enkrv__detyn)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, plcba__tjph.data)
    agpt__oxcxk = c.pyapi.from_native_value(typ.data, plcba__tjph.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, plcba__tjph.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, plcba__tjph.name, c
        .env_manager)
    znnlu__kfkum = c.pyapi.make_none()
    ftwe__uajhr = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    lddh__wexht = c.pyapi.call_method(hvx__rojhl, 'Index', (agpt__oxcxk,
        znnlu__kfkum, ftwe__uajhr, rnf__llyv))
    c.pyapi.decref(agpt__oxcxk)
    c.pyapi.decref(znnlu__kfkum)
    c.pyapi.decref(ftwe__uajhr)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(hvx__rojhl)
    c.context.nrt.decref(c.builder, typ, val)
    return lddh__wexht


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        lumnm__uxc = signature.return_type
        plcba__tjph = cgutils.create_struct_proxy(lumnm__uxc)(context, builder)
        plcba__tjph.data = args[0]
        plcba__tjph.name = args[1]
        context.nrt.incref(builder, lumnm__uxc.data, args[0])
        context.nrt.incref(builder, lumnm__uxc.name_typ, args[1])
        dtype = lumnm__uxc.dtype
        plcba__tjph.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return plcba__tjph._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    cfsds__dykk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, cfsds__dykk).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(cfsds__dykk)
    c.pyapi.decref(rnf__llyv)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    dtype = typ.dtype
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


def create_numeric_constructor(func, func_str, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None):
        ntgjp__yzo = dict(dtype=dtype)
        qed__trqc = dict(dtype=None)
        check_unsupported_args(func_str, ntgjp__yzo, qed__trqc,
            package_name='pandas', module_name='Index')
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None):
                unbi__lmx = bodo.utils.conversion.coerce_to_ndarray(data)
                oztxh__lwz = bodo.utils.conversion.fix_arr_dtype(unbi__lmx,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(oztxh__lwz
                    , name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None):
                unbi__lmx = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    unbi__lmx = unbi__lmx.copy()
                oztxh__lwz = bodo.utils.conversion.fix_arr_dtype(unbi__lmx,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(oztxh__lwz
                    , name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, func_str, default_dtype in ((Int64Index, 'pandas.Int64Index',
        np.int64), (UInt64Index, 'pandas.UInt64Index', np.uint64), (
        Float64Index, 'pandas.Float64Index', np.float64)):
        overload_impl = create_numeric_constructor(func, func_str,
            default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type if data_typ is None else data_typ
        super(StringIndexType, self).__init__(name=
            f'StringIndexType({name_typ}, {self.data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ, self.data)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None, data_typ=None):
        assert data_typ is None or data_typ == binary_array_type, 'data_typ must be binary_array_type'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', binary_array_type), ('name', fe_type.name_typ
            ), ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    vhaj__zrgl = typ.data
    scalar_type = typ.data.dtype
    cfsds__dykk = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(vhaj__zrgl, cfsds__dykk).value
    rnf__llyv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rnf__llyv).value
    c.pyapi.decref(cfsds__dykk)
    c.pyapi.decref(rnf__llyv)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    plcba__tjph.data = data
    plcba__tjph.name = name
    yeiax__fcoft, zmjeo__khhr = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    plcba__tjph.dict = zmjeo__khhr
    return NativeValue(plcba__tjph._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    vhaj__zrgl = typ.data
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    hvx__rojhl = c.pyapi.import_module_noblock(enkrv__detyn)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, vhaj__zrgl, plcba__tjph.data)
    agpt__oxcxk = c.pyapi.from_native_value(vhaj__zrgl, plcba__tjph.data, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, plcba__tjph.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, plcba__tjph.name, c
        .env_manager)
    znnlu__kfkum = c.pyapi.make_none()
    ftwe__uajhr = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    lddh__wexht = c.pyapi.call_method(hvx__rojhl, 'Index', (agpt__oxcxk,
        znnlu__kfkum, ftwe__uajhr, rnf__llyv))
    c.pyapi.decref(agpt__oxcxk)
    c.pyapi.decref(znnlu__kfkum)
    c.pyapi.decref(ftwe__uajhr)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(hvx__rojhl)
    c.context.nrt.decref(c.builder, typ, val)
    return lddh__wexht


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name,
        data)(data, name)
    jng__pos = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, jng__pos


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        nxt__mbz = 'bytes_type'
    else:
        nxt__mbz = 'string_type'
    pqv__pgou = 'def impl(context, builder, signature, args):\n'
    pqv__pgou += '    assert len(args) == 2\n'
    pqv__pgou += '    index_typ = signature.return_type\n'
    pqv__pgou += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    pqv__pgou += '    index_val.data = args[0]\n'
    pqv__pgou += '    index_val.name = args[1]\n'
    pqv__pgou += '    # increase refcount of stored values\n'
    pqv__pgou += (
        '    context.nrt.incref(builder, signature.args[0], args[0])\n')
    pqv__pgou += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    pqv__pgou += '    # create empty dict for get_loc hashmap\n'
    pqv__pgou += '    index_val.dict = context.compile_internal(\n'
    pqv__pgou += '       builder,\n'
    pqv__pgou += (
        f'       lambda: numba.typed.Dict.empty({nxt__mbz}, types.int64),\n')
    pqv__pgou += f'        types.DictType({nxt__mbz}, types.int64)(), [],)\n'
    pqv__pgou += '    return index_val._getvalue()\n'
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A, name=None, deep=False, dtype=None,
    names=None):
    typ = type(A)
    wqj__upal = idx_typ_to_format_str_map[typ].format('copy()')
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', txbf__uarz, idx_cpy_arg_defaults,
        fn_str=wqj__upal, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_binary_str_index(A._data
                .copy(), A._name)
    return impl


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(IntervalIndexType, 'name')
@overload_attribute(CategoricalIndexType, 'name')
@overload_attribute(MultiIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if is_str_arr_type(arr_typ):
        return StringIndexType(name_typ, arr_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType,
        FloatingArrayType, bodo.CategoricalArrayType)) or arr_typ in (bodo.
        datetime_date_array_type, bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.DatetimeArrayType):
        return DatetimeIndexType(name_typ, arr_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


def _verify_setop_compatible(func_name, I, other):
    if not is_pd_index_type(other) and not isinstance(other, (SeriesType,
        types.Array)):
        raise BodoError(
            f'pd.Index.{func_name}(): unsupported type for argument other: {other}'
            )
    exofq__zwz = I.dtype if not isinstance(I, RangeIndexType) else types.int64
    mwp__ucavc = other.dtype if not isinstance(other, RangeIndexType
        ) else types.int64
    if exofq__zwz != mwp__ucavc:
        raise BodoError(
            f'Index.{func_name}(): incompatible types {exofq__zwz} and {mwp__ucavc}'
            )


@overload_method(NumericIndexType, 'union', inline='always')
@overload_method(StringIndexType, 'union', inline='always')
@overload_method(BinaryIndexType, 'union', inline='always')
@overload_method(DatetimeIndexType, 'union', inline='always')
@overload_method(TimedeltaIndexType, 'union', inline='always')
@overload_method(RangeIndexType, 'union', inline='always')
def overload_index_union(I, other, sort=None):
    ecalw__jpqna = dict(sort=sort)
    tfg__axyh = dict(sort=None)
    check_unsupported_args('Index.union', ecalw__jpqna, tfg__axyh,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('union', I, other)
    sope__zgnc = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        zhlz__kgx = bodo.utils.conversion.coerce_to_array(I)
        anbsy__gyn = bodo.utils.conversion.coerce_to_array(other)
        ifkz__rcbn = bodo.libs.array_kernels.concat([zhlz__kgx, anbsy__gyn])
        hfq__ldxfi = bodo.libs.array_kernels.unique(ifkz__rcbn)
        return sope__zgnc(hfq__ldxfi, None)
    return impl


@overload_method(NumericIndexType, 'intersection', inline='always')
@overload_method(StringIndexType, 'intersection', inline='always')
@overload_method(BinaryIndexType, 'intersection', inline='always')
@overload_method(DatetimeIndexType, 'intersection', inline='always')
@overload_method(TimedeltaIndexType, 'intersection', inline='always')
@overload_method(RangeIndexType, 'intersection', inline='always')
def overload_index_intersection(I, other, sort=None):
    ecalw__jpqna = dict(sort=sort)
    tfg__axyh = dict(sort=None)
    check_unsupported_args('Index.intersection', ecalw__jpqna, tfg__axyh,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('intersection', I, other)
    sope__zgnc = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        zhlz__kgx = bodo.utils.conversion.coerce_to_array(I)
        anbsy__gyn = bodo.utils.conversion.coerce_to_array(other)
        jhmiu__bkbj = bodo.libs.array_kernels.unique(zhlz__kgx)
        yvwu__qphh = bodo.libs.array_kernels.unique(anbsy__gyn)
        ifkz__rcbn = bodo.libs.array_kernels.concat([jhmiu__bkbj, yvwu__qphh])
        bchgk__karf = pd.Series(ifkz__rcbn).sort_values().values
        dqhc__ubyt = bodo.libs.array_kernels.intersection_mask(bchgk__karf)
        return sope__zgnc(bchgk__karf[dqhc__ubyt], None)
    return impl


@overload_method(NumericIndexType, 'difference', inline='always')
@overload_method(StringIndexType, 'difference', inline='always')
@overload_method(BinaryIndexType, 'difference', inline='always')
@overload_method(DatetimeIndexType, 'difference', inline='always')
@overload_method(TimedeltaIndexType, 'difference', inline='always')
@overload_method(RangeIndexType, 'difference', inline='always')
def overload_index_difference(I, other, sort=None):
    ecalw__jpqna = dict(sort=sort)
    tfg__axyh = dict(sort=None)
    check_unsupported_args('Index.difference', ecalw__jpqna, tfg__axyh,
        package_name='pandas', module_name='Index')
    _verify_setop_compatible('difference', I, other)
    sope__zgnc = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, sort=None):
        zhlz__kgx = bodo.utils.conversion.coerce_to_array(I)
        anbsy__gyn = bodo.utils.conversion.coerce_to_array(other)
        jhmiu__bkbj = bodo.libs.array_kernels.unique(zhlz__kgx)
        yvwu__qphh = bodo.libs.array_kernels.unique(anbsy__gyn)
        dqhc__ubyt = np.empty(len(jhmiu__bkbj), np.bool_)
        bodo.libs.array.array_isin(dqhc__ubyt, jhmiu__bkbj, yvwu__qphh, False)
        return sope__zgnc(jhmiu__bkbj[~dqhc__ubyt], None)
    return impl


@overload_method(NumericIndexType, 'symmetric_difference', inline='always')
@overload_method(StringIndexType, 'symmetric_difference', inline='always')
@overload_method(BinaryIndexType, 'symmetric_difference', inline='always')
@overload_method(DatetimeIndexType, 'symmetric_difference', inline='always')
@overload_method(TimedeltaIndexType, 'symmetric_difference', inline='always')
@overload_method(RangeIndexType, 'symmetric_difference', inline='always')
def overload_index_symmetric_difference(I, other, result_name=None, sort=None):
    ecalw__jpqna = dict(result_name=result_name, sort=sort)
    tfg__axyh = dict(result_name=None, sort=None)
    check_unsupported_args('Index.symmetric_difference', ecalw__jpqna,
        tfg__axyh, package_name='pandas', module_name='Index')
    _verify_setop_compatible('symmetric_difference', I, other)
    sope__zgnc = get_index_constructor(I) if not isinstance(I, RangeIndexType
        ) else init_numeric_index

    def impl(I, other, result_name=None, sort=None):
        zhlz__kgx = bodo.utils.conversion.coerce_to_array(I)
        anbsy__gyn = bodo.utils.conversion.coerce_to_array(other)
        jhmiu__bkbj = bodo.libs.array_kernels.unique(zhlz__kgx)
        yvwu__qphh = bodo.libs.array_kernels.unique(anbsy__gyn)
        ygww__tfm = np.empty(len(jhmiu__bkbj), np.bool_)
        wvuz__jdbl = np.empty(len(yvwu__qphh), np.bool_)
        bodo.libs.array.array_isin(ygww__tfm, jhmiu__bkbj, yvwu__qphh, False)
        bodo.libs.array.array_isin(wvuz__jdbl, yvwu__qphh, jhmiu__bkbj, False)
        vskv__gmsrq = bodo.libs.array_kernels.concat([jhmiu__bkbj[~
            ygww__tfm], yvwu__qphh[~wvuz__jdbl]])
        return sope__zgnc(vskv__gmsrq, None)
    return impl


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices, axis=0, allow_fill=True, fill_value=None):
    ecalw__jpqna = dict(axis=axis, allow_fill=allow_fill, fill_value=fill_value
        )
    tfg__axyh = dict(axis=0, allow_fill=True, fill_value=None)
    check_unsupported_args('Index.take', ecalw__jpqna, tfg__axyh,
        package_name='pandas', module_name='Index')
    return lambda I, indices: I[indices]


def _init_engine(I, ban_unique=True):
    pass


@overload(_init_engine)
def overload_init_engine(I, ban_unique=True):
    if isinstance(I, CategoricalIndexType):

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(yczec__qqg)):
                    if not bodo.libs.array_kernels.isna(yczec__qqg, i):
                        val = (bodo.hiframes.pd_categorical_ext.
                            get_code_for_value(yczec__qqg.dtype, yczec__qqg[i])
                            )
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl
    else:

        def impl(I, ban_unique=True):
            if len(I) > 0 and not I._dict:
                yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
                for i in range(len(yczec__qqg)):
                    if not bodo.libs.array_kernels.isna(yczec__qqg, i):
                        val = yczec__qqg[i]
                        if ban_unique and val in I._dict:
                            raise ValueError(
                                'Index.get_loc(): non-unique Index not supported yet'
                                )
                        I._dict[val] = i
        return impl


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)
    if isinstance(I, CategoricalIndexType):

        def impl(I, val):
            key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
            if not is_null_value(I._dict):
                _init_engine(I, False)
                yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
                gmlgy__taz = (bodo.hiframes.pd_categorical_ext.
                    get_code_for_value(yczec__qqg.dtype, key))
                return gmlgy__taz in I._dict
            else:
                yqxto__gpj = (
                    'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                    )
                warnings.warn(yqxto__gpj)
                yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
                ind = -1
                for i in range(len(yczec__qqg)):
                    if not bodo.libs.array_kernels.isna(yczec__qqg, i):
                        if yczec__qqg[i] == key:
                            ind = i
            return ind != -1
        return impl

    def impl(I, val):
        key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        if not is_null_value(I._dict):
            _init_engine(I, False)
            return key in I._dict
        else:
            yqxto__gpj = (
                'Global Index objects can be slow (pass as argument to JIT function for better performance).'
                )
            warnings.warn(yqxto__gpj)
            yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(yczec__qqg)):
                if not bodo.libs.array_kernels.isna(yczec__qqg, i):
                    if yczec__qqg[i] == key:
                        ind = i
        return ind != -1
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    ecalw__jpqna = dict(method=method, tolerance=tolerance)
    zbfeh__dabb = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    key = types.unliteral(key)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.get_loc')
    if key == pd_timestamp_tz_naive_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        key = bodo.utils.conversion.unbox_if_tz_naive_timestamp(key)
        if not is_null_value(I._dict):
            _init_engine(I)
            ind = I._dict.get(key, -1)
        else:
            yqxto__gpj = (
                'Index.get_loc() can be slow for global Index objects (pass as argument to JIT function for better performance).'
                )
            warnings.warn(yqxto__gpj)
            yczec__qqg = bodo.utils.conversion.coerce_to_array(I)
            ind = -1
            for i in range(len(yczec__qqg)):
                if yczec__qqg[i] == key:
                    if ind != -1:
                        raise ValueError(
                            'Index.get_loc(): non-unique Index not supported yet'
                            )
                    ind = i
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


def create_isna_specific_method(overload_name):

    def overload_index_isna_specific_method(I):
        nlyza__iqku = overload_name in {'isna', 'isnull'}
        if isinstance(I, RangeIndexType):

            def impl(I):
                numba.parfors.parfor.init_prange()
                aajz__oku = len(I)
                bmcg__tkbq = np.empty(aajz__oku, np.bool_)
                for i in numba.parfors.parfor.internal_prange(aajz__oku):
                    bmcg__tkbq[i] = not nlyza__iqku
                return bmcg__tkbq
            return impl
        pqv__pgou = f"""def impl(I):
    numba.parfors.parfor.init_prange()
    arr = bodo.hiframes.pd_index_ext.get_index_data(I)
    n = len(arr)
    out_arr = np.empty(n, np.bool_)
    for i in numba.parfors.parfor.internal_prange(n):
       out_arr[i] = {'' if nlyza__iqku else 'not '}bodo.libs.array_kernels.isna(arr, i)
    return out_arr
"""
        oabp__flzcb = {}
        exec(pqv__pgou, {'bodo': bodo, 'np': np, 'numba': numba}, oabp__flzcb)
        impl = oabp__flzcb['impl']
        return impl
    return overload_index_isna_specific_method


isna_overload_types = (RangeIndexType, NumericIndexType, StringIndexType,
    BinaryIndexType, CategoricalIndexType, PeriodIndexType,
    DatetimeIndexType, TimedeltaIndexType)
isna_specific_methods = 'isna', 'notna', 'isnull', 'notnull'


def _install_isna_specific_methods():
    for wqi__ssdj in isna_overload_types:
        for overload_name in isna_specific_methods:
            overload_impl = create_isna_specific_method(overload_name)
            overload_method(wqi__ssdj, overload_name, no_unliteral=True,
                inline='always')(overload_impl)


_install_isna_specific_methods()


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I, 'Index.values'
        )
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType, HeterogeneousIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload(len, no_unliteral=True)
def overload_multi_index_len(I):
    if isinstance(I, MultiIndexType):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I)[0])


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@overload_attribute(MultiIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)[0]),)


@overload_attribute(NumericIndexType, 'is_monotonic', inline='always')
@overload_attribute(RangeIndexType, 'is_monotonic', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic', inline='always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic', inline='always')
@overload_attribute(NumericIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_increasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_increasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_increasing', inline=
    'always')
def overload_index_is_montonic(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_increasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(yczec__qqg, 1)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step > 0 or len(I) <= 1
        return impl


@overload_attribute(NumericIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(RangeIndexType, 'is_monotonic_decreasing', inline='always')
@overload_attribute(DatetimeIndexType, 'is_monotonic_decreasing', inline=
    'always')
@overload_attribute(TimedeltaIndexType, 'is_monotonic_decreasing', inline=
    'always')
def overload_index_is_montonic_decreasing(I):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.is_monotonic_decreasing')
    if isinstance(I, (NumericIndexType, DatetimeIndexType, TimedeltaIndexType)
        ):

        def impl(I):
            yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
            return bodo.libs.array_kernels.series_monotonicity(yczec__qqg, 2)
        return impl
    elif isinstance(I, RangeIndexType):

        def impl(I):
            return I._step < 0 or len(I) <= 1
        return impl


@overload_method(NumericIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(StringIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(PeriodIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(CategoricalIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(BinaryIndexType, 'duplicated', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'duplicated', inline='always',
    no_unliteral=True)
def overload_index_duplicated(I, keep='first'):
    if isinstance(I, RangeIndexType):

        def impl(I, keep='first'):
            return np.zeros(len(I), np.bool_)
        return impl

    def impl(I, keep='first'):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        bmcg__tkbq = bodo.libs.array_kernels.duplicated((yczec__qqg,))
        return bmcg__tkbq
    return impl


@overload_method(NumericIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'any', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'any', no_unliteral=True, inline='always')
def overload_index_any(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            return len(I) > 0 and (I._start != 0 or len(I) > 1)
        return impl

    def impl(I):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(NumericIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'all', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'all', no_unliteral=True, inline='always')
def overload_index_all(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            return len(I) == 0 or I._step > 0 and (I._start > 0 or I._stop <= 0
                ) or I._step < 0 and (I._start < 0 or I._stop >= 0
                ) or I._start % I._step != 0
        return impl

    def impl(I):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(RangeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(NumericIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(StringIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(BinaryIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(CategoricalIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(PeriodIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'drop_duplicates', no_unliteral=True,
    inline='always')
def overload_index_drop_duplicates(I, keep='first'):
    ecalw__jpqna = dict(keep=keep)
    zbfeh__dabb = dict(keep='first')
    check_unsupported_args('Index.drop_duplicates', ecalw__jpqna,
        zbfeh__dabb, package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):
        return lambda I, keep='first': I.copy()
    pqv__pgou = """def impl(I, keep='first'):
    data = bodo.hiframes.pd_index_ext.get_index_data(I)
    arr = bodo.libs.array_kernels.drop_duplicates_array(data)
    name = bodo.hiframes.pd_index_ext.get_index_name(I)
"""
    if isinstance(I, PeriodIndexType):
        pqv__pgou += f"""    return bodo.hiframes.pd_index_ext.init_period_index(arr, name, '{I.freq}')
"""
    else:
        pqv__pgou += (
            '    return bodo.utils.conversion.index_from_array(arr, name)')
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    cjn__ltm = args[0]
    if isinstance(self.typemap[cjn__ltm.name], (HeterogeneousIndexType,
        MultiIndexType)):
        return None
    if equiv_set.has_shape(cjn__ltm):
        return ArrayAnalysis.AnalyzeResult(shape=cjn__ltm, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    ecalw__jpqna = dict(na_action=na_action)
    voz__gbim = dict(na_action=None)
    check_unsupported_args('Index.map', ecalw__jpqna, voz__gbim,
        package_name='pandas', module_name='Index')
    dtype = I.dtype
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'DatetimeIndex.map')
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_tz_naive_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    jjxdz__ukml = numba.core.registry.cpu_target.typing_context
    lopro__atyj = numba.core.registry.cpu_target.target_context
    try:
        non__uqqy = get_const_func_output_type(mapper, (dtype,), {},
            jjxdz__ukml, lopro__atyj)
    except Exception as yfeap__zym:
        raise_bodo_error(get_udf_error_msg('Index.map()', yfeap__zym))
    opcr__pdj = get_udf_out_arr_type(non__uqqy)
    func = get_overload_const_func(mapper, None)
    pqv__pgou = 'def f(I, mapper, na_action=None):\n'
    pqv__pgou += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    pqv__pgou += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    pqv__pgou += '  numba.parfors.parfor.init_prange()\n'
    pqv__pgou += '  n = len(A)\n'
    pqv__pgou += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    pqv__pgou += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    pqv__pgou += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    pqv__pgou += '    v = map_func(t2)\n'
    pqv__pgou += (
        '    S[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(v)\n')
    pqv__pgou += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    hwn__dazzx = bodo.compiler.udf_jit(func)
    oabp__flzcb = {}
    exec(pqv__pgou, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': hwn__dazzx, '_arr_typ': opcr__pdj, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'data_arr_type': opcr__pdj.dtype},
        oabp__flzcb)
    f = oabp__flzcb['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    uyh__lnh, pbhrz__qmvp = sig.args
    if uyh__lnh != pbhrz__qmvp:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    uyh__lnh, pbhrz__qmvp = sig.args
    if uyh__lnh != pbhrz__qmvp:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):
            pqv__pgou = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(lhs)\n'
                )
            if rhs in [bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type, bodo.hiframes.pd_timestamp_ext.
                pd_timedelta_type]:
                pqv__pgou += """  dt = bodo.utils.conversion.unbox_if_tz_naive_timestamp(rhs)
  return op(arr, dt)
"""
            else:
                pqv__pgou += """  rhs_arr = bodo.utils.conversion.get_array_if_series_or_index(rhs)
  return op(arr, rhs_arr)
"""
            oabp__flzcb = {}
            exec(pqv__pgou, {'bodo': bodo, 'op': op}, oabp__flzcb)
            impl = oabp__flzcb['impl']
            return impl
        if is_index_type(rhs):
            pqv__pgou = (
                'def impl(lhs, rhs):\n  arr = bodo.utils.conversion.coerce_to_array(rhs)\n'
                )
            if lhs in [bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type, bodo.hiframes.pd_timestamp_ext.
                pd_timedelta_type]:
                pqv__pgou += """  dt = bodo.utils.conversion.unbox_if_tz_naive_timestamp(lhs)
  return op(dt, arr)
"""
            else:
                pqv__pgou += """  lhs_arr = bodo.utils.conversion.get_array_if_series_or_index(lhs)
  return op(lhs_arr, arr)
"""
            oabp__flzcb = {}
            exec(pqv__pgou, {'bodo': bodo, 'op': op}, oabp__flzcb)
            impl = oabp__flzcb['impl']
            return impl
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    yczec__qqg = bodo.utils.conversion.coerce_to_array(data)
                    ajoq__qxc = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    bmcg__tkbq = op(yczec__qqg, ajoq__qxc)
                    return bmcg__tkbq
                return impl3
            count = len(lhs.data.types)
            pqv__pgou = 'def f(lhs, rhs):\n'
            pqv__pgou += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            oabp__flzcb = {}
            exec(pqv__pgou, {'op': op, 'np': np}, oabp__flzcb)
            impl = oabp__flzcb['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    yczec__qqg = bodo.utils.conversion.coerce_to_array(data)
                    ajoq__qxc = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    bmcg__tkbq = op(ajoq__qxc, yczec__qqg)
                    return bmcg__tkbq
                return impl4
            count = len(rhs.data.types)
            pqv__pgou = 'def f(lhs, rhs):\n'
            pqv__pgou += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            oabp__flzcb = {}
            exec(pqv__pgou, {'op': op, 'np': np}, oabp__flzcb)
            impl = oabp__flzcb['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


@numba.njit(no_cpython_wrapper=True)
def range_index_to_numeric(I):
    return init_numeric_index(np.arange(I._start, I._stop, I._step), bodo.
        hiframes.pd_index_ext.get_index_name(I))


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_typ=None):
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_typ})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_typ)

    @property
    def key(self):
        return self.data, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def pandas_type_name(self):
        return 'object'

    @property
    def numpy_type_name(self):
        return 'object'


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nhbb__txv = [('data', fe_type.data), ('name', fe_type.name_typ)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, nhbb__txv)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A, name=None, deep=False, dtype=None, names=None
    ):
    wqj__upal = idx_typ_to_format_str_map[HeterogeneousIndexType].format(
        'copy()')
    txbf__uarz = dict(deep=deep, dtype=dtype, names=names)
    check_unsupported_args('Index.copy', txbf__uarz, idx_cpy_arg_defaults,
        fn_str=wqj__upal, package_name='pandas', module_name='Index')
    if not is_overload_none(name):

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), name)
    else:

        def impl(A, name=None, deep=False, dtype=None, names=None):
            return bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
                copy(), A._name)
    return impl


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    enkrv__detyn = c.context.insert_const_string(c.builder.module, 'pandas')
    hvx__rojhl = c.pyapi.import_module_noblock(enkrv__detyn)
    plcba__tjph = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, plcba__tjph.data)
    agpt__oxcxk = c.pyapi.from_native_value(typ.data, plcba__tjph.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, plcba__tjph.name)
    rnf__llyv = c.pyapi.from_native_value(typ.name_typ, plcba__tjph.name, c
        .env_manager)
    znnlu__kfkum = c.pyapi.make_none()
    ftwe__uajhr = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    lddh__wexht = c.pyapi.call_method(hvx__rojhl, 'Index', (agpt__oxcxk,
        znnlu__kfkum, ftwe__uajhr, rnf__llyv))
    c.pyapi.decref(agpt__oxcxk)
    c.pyapi.decref(znnlu__kfkum)
    c.pyapi.decref(ftwe__uajhr)
    c.pyapi.decref(rnf__llyv)
    c.pyapi.decref(hvx__rojhl)
    c.context.nrt.decref(c.builder, typ, val)
    return lddh__wexht


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        lumnm__uxc = signature.return_type
        plcba__tjph = cgutils.create_struct_proxy(lumnm__uxc)(context, builder)
        plcba__tjph.data = args[0]
        plcba__tjph.name = args[1]
        context.nrt.incref(builder, lumnm__uxc.data, args[0])
        context.nrt.incref(builder, lumnm__uxc.name_typ, args[1])
        return plcba__tjph._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
@overload_attribute(MultiIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    elif isinstance(I, MultiIndexType):
        pqv__pgou = 'def _impl_nbytes(I):\n'
        pqv__pgou += '    total = 0\n'
        pqv__pgou += '    data = I._data\n'
        for i in range(I.nlevels):
            pqv__pgou += f'    total += data[{i}].nbytes\n'
        pqv__pgou += '    return total\n'
        zfhj__grsml = {}
        exec(pqv__pgou, {}, zfhj__grsml)
        return zfhj__grsml['_impl_nbytes']
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload_method(NumericIndexType, 'to_series', inline='always')
@overload_method(DatetimeIndexType, 'to_series', inline='always')
@overload_method(TimedeltaIndexType, 'to_series', inline='always')
@overload_method(RangeIndexType, 'to_series', inline='always')
@overload_method(StringIndexType, 'to_series', inline='always')
@overload_method(BinaryIndexType, 'to_series', inline='always')
@overload_method(CategoricalIndexType, 'to_series', inline='always')
def overload_index_to_series(I, index=None, name=None):
    if not (is_overload_constant_str(name) or is_overload_constant_int(name
        ) or is_overload_none(name)):
        raise_bodo_error(
            f'Index.to_series(): only constant string/int are supported for argument name'
            )
    if is_overload_none(name):
        blwsh__ionfw = 'bodo.hiframes.pd_index_ext.get_index_name(I)'
    else:
        blwsh__ionfw = 'name'
    pqv__pgou = 'def impl(I, index=None, name=None):\n'
    pqv__pgou += '    data = bodo.utils.conversion.index_to_array(I)\n'
    if is_overload_none(index):
        pqv__pgou += '    new_index = I\n'
    elif is_pd_index_type(index):
        pqv__pgou += '    new_index = index\n'
    elif isinstance(index, SeriesType):
        pqv__pgou += '    arr = bodo.utils.conversion.coerce_to_array(index)\n'
        pqv__pgou += (
            '    index_name = bodo.hiframes.pd_series_ext.get_series_name(index)\n'
            )
        pqv__pgou += (
            '    new_index = bodo.utils.conversion.index_from_array(arr, index_name)\n'
            )
    elif bodo.utils.utils.is_array_typ(index, False):
        pqv__pgou += (
            '    new_index = bodo.utils.conversion.index_from_array(index)\n')
    elif isinstance(index, (types.List, types.BaseTuple)):
        pqv__pgou += '    arr = bodo.utils.conversion.coerce_to_array(index)\n'
        pqv__pgou += (
            '    new_index = bodo.utils.conversion.index_from_array(arr)\n')
    else:
        raise_bodo_error(
            f'Index.to_series(): unsupported type for argument index: {type(index).__name__}'
            )
    pqv__pgou += f'    new_name = {blwsh__ionfw}\n'
    pqv__pgou += (
        '    return bodo.hiframes.pd_series_ext.init_series(data, new_index, new_name)'
        )
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'np': np}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(NumericIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(DatetimeIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(TimedeltaIndexType, 'to_frame', inline='always',
    no_unliteral=True)
@overload_method(RangeIndexType, 'to_frame', inline='always', no_unliteral=True
    )
@overload_method(StringIndexType, 'to_frame', inline='always', no_unliteral
    =True)
@overload_method(BinaryIndexType, 'to_frame', inline='always', no_unliteral
    =True)
@overload_method(CategoricalIndexType, 'to_frame', inline='always',
    no_unliteral=True)
def overload_index_to_frame(I, index=True, name=None):
    if is_overload_true(index):
        sbjv__bga = 'I'
    elif is_overload_false(index):
        sbjv__bga = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(I), 1, None)')
    elif not isinstance(index, types.Boolean):
        raise_bodo_error(
            'Index.to_frame(): index argument must be a constant boolean')
    else:
        raise_bodo_error(
            'Index.to_frame(): index argument must be a compile time constant')
    pqv__pgou = 'def impl(I, index=True, name=None):\n'
    pqv__pgou += '    data = bodo.utils.conversion.index_to_array(I)\n'
    pqv__pgou += f'    new_index = {sbjv__bga}\n'
    if is_overload_none(name) and I.name_typ == types.none:
        xrpo__lul = ColNamesMetaType((0,))
    elif is_overload_none(name):
        xrpo__lul = ColNamesMetaType((I.name_typ,))
    elif is_overload_constant_str(name):
        xrpo__lul = ColNamesMetaType((get_overload_const_str(name),))
    elif is_overload_constant_int(name):
        xrpo__lul = ColNamesMetaType((get_overload_const_int(name),))
    else:
        raise_bodo_error(
            f'Index.to_frame(): only constant string/int are supported for argument name'
            )
    pqv__pgou += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((data,), new_index, __col_name_meta_value)
"""
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'np': np, '__col_name_meta_value':
        xrpo__lul}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(MultiIndexType, 'to_frame', inline='always', no_unliteral=True
    )
def overload_multi_index_to_frame(I, index=True, name=None):
    if is_overload_true(index):
        sbjv__bga = 'I'
    elif is_overload_false(index):
        sbjv__bga = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(I), 1, None)')
    elif not isinstance(index, types.Boolean):
        raise_bodo_error(
            'MultiIndex.to_frame(): index argument must be a constant boolean')
    else:
        raise_bodo_error(
            'MultiIndex.to_frame(): index argument must be a compile time constant'
            )
    pqv__pgou = 'def impl(I, index=True, name=None):\n'
    pqv__pgou += '    data = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    pqv__pgou += f'    new_index = {sbjv__bga}\n'
    fld__cipwf = len(I.array_types)
    if is_overload_none(name) and I.names_typ == (types.none,) * fld__cipwf:
        xrpo__lul = ColNamesMetaType(tuple(range(fld__cipwf)))
    elif is_overload_none(name):
        xrpo__lul = ColNamesMetaType(I.names_typ)
    elif is_overload_constant_tuple(name) or is_overload_constant_list(name):
        if is_overload_constant_list(name):
            names = tuple(get_overload_const_list(name))
        else:
            names = get_overload_const_tuple(name)
        if fld__cipwf != len(names):
            raise_bodo_error(
                f'MultiIndex.to_frame(): expected {fld__cipwf} names, not {len(names)}'
                )
        if all(is_overload_constant_str(kdf__jxd) or
            is_overload_constant_int(kdf__jxd) for kdf__jxd in names):
            xrpo__lul = ColNamesMetaType(names)
        else:
            raise_bodo_error(
                'MultiIndex.to_frame(): only constant string/int list/tuple are supported for argument name'
                )
    else:
        raise_bodo_error(
            'MultiIndex.to_frame(): only constant string/int list/tuple are supported for argument name'
            )
    pqv__pgou += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(data, new_index, __col_name_meta_value,)
"""
    oabp__flzcb = {}
    exec(pqv__pgou, {'bodo': bodo, 'np': np, '__col_name_meta_value':
        xrpo__lul}, oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(NumericIndexType, 'to_numpy', inline='always')
@overload_method(DatetimeIndexType, 'to_numpy', inline='always')
@overload_method(TimedeltaIndexType, 'to_numpy', inline='always')
@overload_method(RangeIndexType, 'to_numpy', inline='always')
@overload_method(StringIndexType, 'to_numpy', inline='always')
@overload_method(BinaryIndexType, 'to_numpy', inline='always')
@overload_method(CategoricalIndexType, 'to_numpy', inline='always')
@overload_method(IntervalIndexType, 'to_numpy', inline='always')
def overload_index_to_numpy(I, dtype=None, copy=False, na_value=None):
    ecalw__jpqna = dict(dtype=dtype, na_value=na_value)
    zbfeh__dabb = dict(dtype=None, na_value=None)
    check_unsupported_args('Index.to_numpy', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if not is_overload_bool(copy):
        raise_bodo_error('Index.to_numpy(): copy argument must be a boolean')
    if isinstance(I, RangeIndexType):

        def impl(I, dtype=None, copy=False, na_value=None):
            return np.arange(I._start, I._stop, I._step)
        return impl
    if is_overload_true(copy):

        def impl(I, dtype=None, copy=False, na_value=None):
            return bodo.hiframes.pd_index_ext.get_index_data(I).copy()
        return impl
    if is_overload_false(copy):

        def impl(I, dtype=None, copy=False, na_value=None):
            return bodo.hiframes.pd_index_ext.get_index_data(I)
        return impl

    def impl(I, dtype=None, copy=False, na_value=None):
        data = bodo.hiframes.pd_index_ext.get_index_data(I)
        return data.copy() if copy else data
    return impl


@overload_method(NumericIndexType, 'to_list', inline='always')
@overload_method(RangeIndexType, 'to_list', inline='always')
@overload_method(StringIndexType, 'to_list', inline='always')
@overload_method(BinaryIndexType, 'to_list', inline='always')
@overload_method(CategoricalIndexType, 'to_list', inline='always')
@overload_method(DatetimeIndexType, 'to_list', inline='always')
@overload_method(TimedeltaIndexType, 'to_list', inline='always')
@overload_method(NumericIndexType, 'tolist', inline='always')
@overload_method(RangeIndexType, 'tolist', inline='always')
@overload_method(StringIndexType, 'tolist', inline='always')
@overload_method(BinaryIndexType, 'tolist', inline='always')
@overload_method(CategoricalIndexType, 'tolist', inline='always')
@overload_method(DatetimeIndexType, 'tolist', inline='always')
@overload_method(TimedeltaIndexType, 'tolist', inline='always')
def overload_index_to_list(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            iskao__xzhz = list()
            for i in range(I._start, I._stop, I.step):
                iskao__xzhz.append(i)
            return iskao__xzhz
        return impl

    def impl(I):
        iskao__xzhz = list()
        for i in range(len(I)):
            iskao__xzhz.append(I[i])
        return iskao__xzhz
    return impl


@overload_attribute(NumericIndexType, 'T')
@overload_attribute(DatetimeIndexType, 'T')
@overload_attribute(TimedeltaIndexType, 'T')
@overload_attribute(RangeIndexType, 'T')
@overload_attribute(StringIndexType, 'T')
@overload_attribute(BinaryIndexType, 'T')
@overload_attribute(CategoricalIndexType, 'T')
@overload_attribute(PeriodIndexType, 'T')
@overload_attribute(MultiIndexType, 'T')
@overload_attribute(IntervalIndexType, 'T')
def overload_T(I):
    return lambda I: I


@overload_attribute(NumericIndexType, 'size')
@overload_attribute(DatetimeIndexType, 'size')
@overload_attribute(TimedeltaIndexType, 'size')
@overload_attribute(RangeIndexType, 'size')
@overload_attribute(StringIndexType, 'size')
@overload_attribute(BinaryIndexType, 'size')
@overload_attribute(CategoricalIndexType, 'size')
@overload_attribute(PeriodIndexType, 'size')
@overload_attribute(MultiIndexType, 'size')
@overload_attribute(IntervalIndexType, 'size')
def overload_size(I):
    return lambda I: len(I)


@overload_attribute(NumericIndexType, 'ndim')
@overload_attribute(DatetimeIndexType, 'ndim')
@overload_attribute(TimedeltaIndexType, 'ndim')
@overload_attribute(RangeIndexType, 'ndim')
@overload_attribute(StringIndexType, 'ndim')
@overload_attribute(BinaryIndexType, 'ndim')
@overload_attribute(CategoricalIndexType, 'ndim')
@overload_attribute(PeriodIndexType, 'ndim')
@overload_attribute(MultiIndexType, 'ndim')
@overload_attribute(IntervalIndexType, 'ndim')
def overload_ndim(I):
    return lambda I: 1


@overload_attribute(NumericIndexType, 'nlevels')
@overload_attribute(DatetimeIndexType, 'nlevels')
@overload_attribute(TimedeltaIndexType, 'nlevels')
@overload_attribute(RangeIndexType, 'nlevels')
@overload_attribute(StringIndexType, 'nlevels')
@overload_attribute(BinaryIndexType, 'nlevels')
@overload_attribute(CategoricalIndexType, 'nlevels')
@overload_attribute(PeriodIndexType, 'nlevels')
@overload_attribute(MultiIndexType, 'nlevels')
@overload_attribute(IntervalIndexType, 'nlevels')
def overload_nlevels(I):
    if isinstance(I, MultiIndexType):
        return lambda I: len(I._data)
    return lambda I: 1


@overload_attribute(NumericIndexType, 'empty')
@overload_attribute(DatetimeIndexType, 'empty')
@overload_attribute(TimedeltaIndexType, 'empty')
@overload_attribute(RangeIndexType, 'empty')
@overload_attribute(StringIndexType, 'empty')
@overload_attribute(BinaryIndexType, 'empty')
@overload_attribute(CategoricalIndexType, 'empty')
@overload_attribute(PeriodIndexType, 'empty')
@overload_attribute(MultiIndexType, 'empty')
@overload_attribute(IntervalIndexType, 'empty')
def overload_empty(I):
    return lambda I: len(I) == 0


@overload_attribute(NumericIndexType, 'is_all_dates')
@overload_attribute(DatetimeIndexType, 'is_all_dates')
@overload_attribute(TimedeltaIndexType, 'is_all_dates')
@overload_attribute(RangeIndexType, 'is_all_dates')
@overload_attribute(StringIndexType, 'is_all_dates')
@overload_attribute(BinaryIndexType, 'is_all_dates')
@overload_attribute(CategoricalIndexType, 'is_all_dates')
@overload_attribute(PeriodIndexType, 'is_all_dates')
@overload_attribute(MultiIndexType, 'is_all_dates')
@overload_attribute(IntervalIndexType, 'is_all_dates')
def overload_is_all_dates(I):
    if isinstance(I, (DatetimeIndexType, TimedeltaIndexType, PeriodIndexType)):
        return lambda I: True
    else:
        return lambda I: False


@overload_attribute(NumericIndexType, 'inferred_type')
@overload_attribute(DatetimeIndexType, 'inferred_type')
@overload_attribute(TimedeltaIndexType, 'inferred_type')
@overload_attribute(RangeIndexType, 'inferred_type')
@overload_attribute(StringIndexType, 'inferred_type')
@overload_attribute(BinaryIndexType, 'inferred_type')
@overload_attribute(CategoricalIndexType, 'inferred_type')
@overload_attribute(PeriodIndexType, 'inferred_type')
@overload_attribute(MultiIndexType, 'inferred_type')
@overload_attribute(IntervalIndexType, 'inferred_type')
def overload_inferred_type(I):
    if isinstance(I, NumericIndexType):
        if isinstance(I.dtype, types.Integer):
            return lambda I: 'integer'
        elif isinstance(I.dtype, types.Float):
            return lambda I: 'floating'
        elif isinstance(I.dtype, types.Boolean):
            return lambda I: 'boolean'
        return
    if isinstance(I, StringIndexType):

        def impl(I):
            if len(I._data) == 0:
                return 'empty'
            return 'string'
        return impl
    pmug__owld = {DatetimeIndexType: 'datetime64', TimedeltaIndexType:
        'timedelta64', RangeIndexType: 'integer', BinaryIndexType: 'bytes',
        CategoricalIndexType: 'categorical', PeriodIndexType: 'period',
        IntervalIndexType: 'interval', MultiIndexType: 'mixed'}
    inferred_type = pmug__owld[type(I)]
    return lambda I: inferred_type


@overload_attribute(NumericIndexType, 'dtype')
@overload_attribute(DatetimeIndexType, 'dtype')
@overload_attribute(TimedeltaIndexType, 'dtype')
@overload_attribute(RangeIndexType, 'dtype')
@overload_attribute(StringIndexType, 'dtype')
@overload_attribute(BinaryIndexType, 'dtype')
@overload_attribute(CategoricalIndexType, 'dtype')
@overload_attribute(MultiIndexType, 'dtype')
def overload_inferred_type(I):
    if isinstance(I, NumericIndexType):
        if isinstance(I.dtype, types.Boolean):
            return lambda I: np.dtype('O')
        dtype = I.dtype
        return lambda I: dtype
    if isinstance(I, CategoricalIndexType):
        dtype = bodo.utils.utils.create_categorical_type(I.dtype.categories,
            I.data, I.dtype.ordered)
        return lambda I: dtype
    glqr__hgi = {DatetimeIndexType: np.dtype('datetime64[ns]'),
        TimedeltaIndexType: np.dtype('timedelta64[ns]'), RangeIndexType: np
        .dtype('int64'), StringIndexType: np.dtype('O'), BinaryIndexType:
        np.dtype('O'), MultiIndexType: np.dtype('O')}
    dtype = glqr__hgi[type(I)]
    return lambda I: dtype


@overload_attribute(NumericIndexType, 'names')
@overload_attribute(DatetimeIndexType, 'names')
@overload_attribute(TimedeltaIndexType, 'names')
@overload_attribute(RangeIndexType, 'names')
@overload_attribute(StringIndexType, 'names')
@overload_attribute(BinaryIndexType, 'names')
@overload_attribute(CategoricalIndexType, 'names')
@overload_attribute(IntervalIndexType, 'names')
@overload_attribute(PeriodIndexType, 'names')
@overload_attribute(MultiIndexType, 'names')
def overload_names(I):
    if isinstance(I, MultiIndexType):
        return lambda I: I._names
    return lambda I: (I._name,)


@overload_method(NumericIndexType, 'rename', inline='always')
@overload_method(DatetimeIndexType, 'rename', inline='always')
@overload_method(TimedeltaIndexType, 'rename', inline='always')
@overload_method(RangeIndexType, 'rename', inline='always')
@overload_method(StringIndexType, 'rename', inline='always')
@overload_method(BinaryIndexType, 'rename', inline='always')
@overload_method(CategoricalIndexType, 'rename', inline='always')
@overload_method(PeriodIndexType, 'rename', inline='always')
@overload_method(IntervalIndexType, 'rename', inline='always')
@overload_method(HeterogeneousIndexType, 'rename', inline='always')
def overload_rename(I, name, inplace=False):
    if is_overload_true(inplace):
        raise BodoError('Index.rename(): inplace index renaming unsupported')
    return init_index_from_index(I, name)


def init_index_from_index(I, name):
    rgj__emd = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index}
    if type(I) in rgj__emd:
        init_func = rgj__emd[type(I)]
        return lambda I, name, inplace=False: init_func(bodo.hiframes.
            pd_index_ext.get_index_data(I).copy(), name)
    if isinstance(I, RangeIndexType):
        return lambda I, name, inplace=False: I.copy(name=name)
    if isinstance(I, PeriodIndexType):
        freq = I.freq
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_period_index(bodo.hiframes.pd_index_ext.get_index_data(I).
            copy(), name, freq))
    if isinstance(I, HeterogeneousIndexType):
        return (lambda I, name, inplace=False: bodo.hiframes.pd_index_ext.
            init_heter_index(bodo.hiframes.pd_index_ext.get_index_data(I),
            name))
    raise_bodo_error(f'init_index(): Unknown type {type(I)}')


def get_index_constructor(I):
    wywoe__tbp = {NumericIndexType: bodo.hiframes.pd_index_ext.
        init_numeric_index, DatetimeIndexType: bodo.hiframes.pd_index_ext.
        init_datetime_index, TimedeltaIndexType: bodo.hiframes.pd_index_ext
        .init_timedelta_index, StringIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, BinaryIndexType: bodo.hiframes.pd_index_ext.
        init_binary_str_index, CategoricalIndexType: bodo.hiframes.
        pd_index_ext.init_categorical_index, IntervalIndexType: bodo.
        hiframes.pd_index_ext.init_interval_index, RangeIndexType: bodo.
        hiframes.pd_index_ext.init_range_index}
    if type(I) in wywoe__tbp:
        return wywoe__tbp[type(I)]
    raise BodoError(
        f'Unsupported type for standard Index constructor: {type(I)}')


@overload_method(NumericIndexType, 'min', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'min', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'min', no_unliteral=True, inline=
    'always')
def overload_index_min(I, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('Index.min', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=None, skipna=True):
            hxuku__sukkj = len(I)
            if hxuku__sukkj == 0:
                return np.nan
            if I._step < 0:
                return I._start + I._step * (hxuku__sukkj - 1)
            else:
                return I._start
        return impl
    if isinstance(I, CategoricalIndexType):
        if not I.dtype.ordered:
            raise BodoError(
                'Index.min(): only ordered categoricals are possible')

    def impl(I, axis=None, skipna=True):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_min(yczec__qqg)
    return impl


@overload_method(NumericIndexType, 'max', no_unliteral=True, inline='always')
@overload_method(RangeIndexType, 'max', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'max', no_unliteral=True, inline=
    'always')
def overload_index_max(I, axis=None, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=None, skipna=True)
    check_unsupported_args('Index.max', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=None, skipna=True):
            hxuku__sukkj = len(I)
            if hxuku__sukkj == 0:
                return np.nan
            if I._step > 0:
                return I._start + I._step * (hxuku__sukkj - 1)
            else:
                return I._start
        return impl
    if isinstance(I, CategoricalIndexType):
        if not I.dtype.ordered:
            raise BodoError(
                'Index.max(): only ordered categoricals are possible')

    def impl(I, axis=None, skipna=True):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        return bodo.libs.array_ops.array_op_max(yczec__qqg)
    return impl


@overload_method(NumericIndexType, 'argmin', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'argmin', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'argmin', no_unliteral=True, inline='always')
@overload_method(PeriodIndexType, 'argmin', no_unliteral=True, inline='always')
def overload_index_argmin(I, axis=0, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=0, skipna=True)
    check_unsupported_args('Index.argmin', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.argmin()')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, skipna=True):
            return (I._step < 0) * (len(I) - 1)
        return impl
    if isinstance(I, CategoricalIndexType) and not I.dtype.ordered:
        raise BodoError(
            'Index.argmin(): only ordered categoricals are possible')

    def impl(I, axis=0, skipna=True):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        index = init_numeric_index(np.arange(len(yczec__qqg)))
        return bodo.libs.array_ops.array_op_idxmin(yczec__qqg, index)
    return impl


@overload_method(NumericIndexType, 'argmax', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'argmax', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'argmax', no_unliteral=True, inline=
    'always')
@overload_method(PeriodIndexType, 'argmax', no_unliteral=True, inline='always')
def overload_index_argmax(I, axis=0, skipna=True):
    ecalw__jpqna = dict(axis=axis, skipna=skipna)
    zbfeh__dabb = dict(axis=0, skipna=True)
    check_unsupported_args('Index.argmax', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.argmax()')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, skipna=True):
            return (I._step > 0) * (len(I) - 1)
        return impl
    if isinstance(I, CategoricalIndexType) and not I.dtype.ordered:
        raise BodoError(
            'Index.argmax(): only ordered categoricals are possible')

    def impl(I, axis=0, skipna=True):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        index = np.arange(len(yczec__qqg))
        return bodo.libs.array_ops.array_op_idxmax(yczec__qqg, index)
    return impl


@overload_method(NumericIndexType, 'unique', no_unliteral=True, inline='always'
    )
@overload_method(BinaryIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'unique', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(IntervalIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(DatetimeIndexType, 'unique', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'unique', no_unliteral=True, inline=
    'always')
def overload_index_unique(I):
    sope__zgnc = get_index_constructor(I)

    def impl(I):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        vpfx__isii = bodo.libs.array_kernels.unique(yczec__qqg)
        return sope__zgnc(vpfx__isii, name)
    return impl


@overload_method(RangeIndexType, 'unique', no_unliteral=True, inline='always')
def overload_range_index_unique(I):

    def impl(I):
        return I.copy()
    return impl


@overload_method(NumericIndexType, 'nunique', inline='always')
@overload_method(BinaryIndexType, 'nunique', inline='always')
@overload_method(StringIndexType, 'nunique', inline='always')
@overload_method(CategoricalIndexType, 'nunique', inline='always')
@overload_method(DatetimeIndexType, 'nunique', inline='always')
@overload_method(TimedeltaIndexType, 'nunique', inline='always')
@overload_method(PeriodIndexType, 'nunique', inline='always')
def overload_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        aajz__oku = bodo.libs.array_kernels.nunique(yczec__qqg, dropna)
        return aajz__oku
    return impl


@overload_method(RangeIndexType, 'nunique', inline='always')
def overload_range_index_nunique(I, dropna=True):

    def impl(I, dropna=True):
        start = I._start
        stop = I._stop
        step = I._step
        return max(0, -(-(stop - start) // step))
    return impl


@overload_method(NumericIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'isin', no_unliteral=True, inline='always')
@overload_method(TimedeltaIndexType, 'isin', no_unliteral=True, inline='always'
    )
def overload_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            hjrs__enr = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_index_ext.get_index_data(I)
            aajz__oku = len(A)
            bmcg__tkbq = np.empty(aajz__oku, np.bool_)
            bodo.libs.array.array_isin(bmcg__tkbq, A, hjrs__enr, False)
            return bmcg__tkbq
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = bodo.hiframes.pd_index_ext.get_index_data(I)
        bmcg__tkbq = bodo.libs.array_ops.array_op_isin(A, values)
        return bmcg__tkbq
    return impl


@overload_method(RangeIndexType, 'isin', no_unliteral=True, inline='always')
def overload_range_index_isin(I, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(I, values):
            hjrs__enr = bodo.utils.conversion.coerce_to_array(values)
            A = np.arange(I.start, I.stop, I.step)
            aajz__oku = len(A)
            bmcg__tkbq = np.empty(aajz__oku, np.bool_)
            bodo.libs.array.array_isin(bmcg__tkbq, A, hjrs__enr, False)
            return bmcg__tkbq
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Index.isin(): 'values' parameter should be a set or a list")

    def impl(I, values):
        A = np.arange(I.start, I.stop, I.step)
        bmcg__tkbq = bodo.libs.array_ops.array_op_isin(A, values)
        return bmcg__tkbq
    return impl


@register_jitable
def order_range(I, ascending):
    step = I._step
    if ascending == (step > 0):
        return I.copy()
    else:
        start = I._start
        stop = I._stop
        name = get_index_name(I)
        hxuku__sukkj = len(I)
        jdzvc__vonrz = start + step * (hxuku__sukkj - 1)
        wuesw__knshm = jdzvc__vonrz - step * hxuku__sukkj
        return init_range_index(jdzvc__vonrz, wuesw__knshm, -step, name)


@overload_method(NumericIndexType, 'sort_values', no_unliteral=True, inline
    ='always')
@overload_method(BinaryIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
@overload_method(StringIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(DatetimeIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(TimedeltaIndexType, 'sort_values', no_unliteral=True,
    inline='always')
@overload_method(RangeIndexType, 'sort_values', no_unliteral=True, inline=
    'always')
def overload_index_sort_values(I, return_indexer=False, ascending=True,
    na_position='last', key=None):
    ecalw__jpqna = dict(return_indexer=return_indexer, key=key)
    zbfeh__dabb = dict(return_indexer=False, key=None)
    check_unsupported_args('Index.sort_values', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Index.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Index.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    if isinstance(I, RangeIndexType):

        def impl(I, return_indexer=False, ascending=True, na_position=
            'last', key=None):
            return order_range(I, ascending)
        return impl
    sope__zgnc = get_index_constructor(I)
    idin__xmzd = ColNamesMetaType(('$_bodo_col_',))

    def impl(I, return_indexer=False, ascending=True, na_position='last',
        key=None):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = get_index_name(I)
        index = init_range_index(0, len(yczec__qqg), 1, None)
        dvz__hmxaq = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            yczec__qqg,), index, idin__xmzd)
        bxmm__sqsb = dvz__hmxaq.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=False, na_position=na_position)
        bmcg__tkbq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            bxmm__sqsb, 0)
        return sope__zgnc(bmcg__tkbq, name)
    return impl


@overload_method(NumericIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(BinaryIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(CategoricalIndexType, 'argsort', no_unliteral=True, inline
    ='always')
@overload_method(DatetimeIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'argsort', no_unliteral=True, inline=
    'always')
@overload_method(PeriodIndexType, 'argsort', no_unliteral=True, inline='always'
    )
@overload_method(RangeIndexType, 'argsort', no_unliteral=True, inline='always')
def overload_index_argsort(I, axis=0, kind='quicksort', order=None):
    ecalw__jpqna = dict(axis=axis, kind=kind, order=order)
    zbfeh__dabb = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Index.argsort', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    if isinstance(I, RangeIndexType):

        def impl(I, axis=0, kind='quicksort', order=None):
            if I._step > 0:
                return np.arange(0, len(I), 1)
            else:
                return np.arange(len(I) - 1, -1, -1)
        return impl

    def impl(I, axis=0, kind='quicksort', order=None):
        yczec__qqg = bodo.hiframes.pd_index_ext.get_index_data(I)
        bmcg__tkbq = bodo.hiframes.series_impl.argsort(yczec__qqg)
        return bmcg__tkbq
    return impl


@overload_method(NumericIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(StringIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(BinaryIndexType, 'where', no_unliteral=True, inline='always')
@overload_method(DatetimeIndexType, 'where', no_unliteral=True, inline='always'
    )
@overload_method(TimedeltaIndexType, 'where', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'where', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'where', no_unliteral=True, inline='always')
def overload_index_where(I, cond, other=np.nan):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Index.where()')
    bodo.hiframes.series_impl._validate_arguments_mask_where('where',
        'Index', I, cond, other, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False)
    if is_overload_constant_nan(other):
        fet__zrcxa = 'None'
    else:
        fet__zrcxa = 'other'
    pqv__pgou = 'def impl(I, cond, other=np.nan):\n'
    if isinstance(I, RangeIndexType):
        pqv__pgou += '  arr = np.arange(I._start, I._stop, I._step)\n'
        sope__zgnc = 'init_numeric_index'
    else:
        pqv__pgou += '  arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    pqv__pgou += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    pqv__pgou += (
        f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {fet__zrcxa})\n'
        )
    pqv__pgou += f'  return constructor(out_arr, name)\n'
    oabp__flzcb = {}
    sope__zgnc = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(pqv__pgou, {'bodo': bodo, 'np': np, 'constructor': sope__zgnc},
        oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(NumericIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(StringIndexType, 'putmask', no_unliteral=True, inline='always'
    )
@overload_method(BinaryIndexType, 'putmask', no_unliteral=True, inline='always'
    )
@overload_method(DatetimeIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'putmask', no_unliteral=True, inline=
    'always')
@overload_method(CategoricalIndexType, 'putmask', no_unliteral=True, inline
    ='always')
@overload_method(RangeIndexType, 'putmask', no_unliteral=True, inline='always')
def overload_index_putmask(I, cond, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.putmask()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Index.putmask()')
    bodo.hiframes.series_impl._validate_arguments_mask_where('putmask',
        'Index', I, cond, other, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False)
    if is_overload_constant_nan(other):
        fet__zrcxa = 'None'
    else:
        fet__zrcxa = 'other'
    pqv__pgou = 'def impl(I, cond, other):\n'
    pqv__pgou += '  cond = ~cond\n'
    if isinstance(I, RangeIndexType):
        pqv__pgou += '  arr = np.arange(I._start, I._stop, I._step)\n'
    else:
        pqv__pgou += '  arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    pqv__pgou += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    pqv__pgou += (
        f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {fet__zrcxa})\n'
        )
    pqv__pgou += f'  return constructor(out_arr, name)\n'
    oabp__flzcb = {}
    sope__zgnc = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(pqv__pgou, {'bodo': bodo, 'np': np, 'constructor': sope__zgnc},
        oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(NumericIndexType, 'repeat', no_unliteral=True, inline='always'
    )
@overload_method(StringIndexType, 'repeat', no_unliteral=True, inline='always')
@overload_method(CategoricalIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(DatetimeIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(TimedeltaIndexType, 'repeat', no_unliteral=True, inline=
    'always')
@overload_method(RangeIndexType, 'repeat', no_unliteral=True, inline='always')
def overload_index_repeat(I, repeats, axis=None):
    ecalw__jpqna = dict(axis=axis)
    zbfeh__dabb = dict(axis=None)
    check_unsupported_args('Index.repeat', ecalw__jpqna, zbfeh__dabb,
        package_name='pandas', module_name='Index')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(I,
        'Index.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Index.repeat(): 'repeats' should be an integer or array of integers"
            )
    pqv__pgou = 'def impl(I, repeats, axis=None):\n'
    if not isinstance(repeats, types.Integer):
        pqv__pgou += (
            '    repeats = bodo.utils.conversion.coerce_to_array(repeats)\n')
    if isinstance(I, RangeIndexType):
        pqv__pgou += '    arr = np.arange(I._start, I._stop, I._step)\n'
    else:
        pqv__pgou += '    arr = bodo.hiframes.pd_index_ext.get_index_data(I)\n'
    pqv__pgou += '    name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    pqv__pgou += (
        '    out_arr = bodo.libs.array_kernels.repeat_kernel(arr, repeats)\n')
    pqv__pgou += '    return constructor(out_arr, name)'
    oabp__flzcb = {}
    sope__zgnc = init_numeric_index if isinstance(I, RangeIndexType
        ) else get_index_constructor(I)
    exec(pqv__pgou, {'bodo': bodo, 'np': np, 'constructor': sope__zgnc},
        oabp__flzcb)
    impl = oabp__flzcb['impl']
    return impl


@overload_method(NumericIndexType, 'is_integer', inline='always')
def overload_is_integer_numeric(I):
    truth = isinstance(I.dtype, types.Integer)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_floating', inline='always')
def overload_is_floating_numeric(I):
    truth = isinstance(I.dtype, types.Float)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_boolean', inline='always')
def overload_is_boolean_numeric(I):
    truth = isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_numeric', inline='always')
def overload_is_numeric_numeric(I):
    truth = not isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(NumericIndexType, 'is_object', inline='always')
def overload_is_object_numeric(I):
    truth = isinstance(I.dtype, types.Boolean)
    return lambda I: truth


@overload_method(StringIndexType, 'is_object', inline='always')
@overload_method(BinaryIndexType, 'is_object', inline='always')
@overload_method(RangeIndexType, 'is_numeric', inline='always')
@overload_method(RangeIndexType, 'is_integer', inline='always')
@overload_method(CategoricalIndexType, 'is_categorical', inline='always')
@overload_method(IntervalIndexType, 'is_interval', inline='always')
@overload_method(MultiIndexType, 'is_object', inline='always')
def overload_is_methods_true(I):
    return lambda I: True


@overload_method(NumericIndexType, 'is_categorical', inline='always')
@overload_method(NumericIndexType, 'is_interval', inline='always')
@overload_method(StringIndexType, 'is_boolean', inline='always')
@overload_method(StringIndexType, 'is_floating', inline='always')
@overload_method(StringIndexType, 'is_categorical', inline='always')
@overload_method(StringIndexType, 'is_integer', inline='always')
@overload_method(StringIndexType, 'is_interval', inline='always')
@overload_method(StringIndexType, 'is_numeric', inline='always')
@overload_method(BinaryIndexType, 'is_boolean', inline='always')
@overload_method(BinaryIndexType, 'is_floating', inline='always')
@overload_method(BinaryIndexType, 'is_categorical', inline='always')
@overload_method(BinaryIndexType, 'is_integer', inline='always')
@overload_method(BinaryIndexType, 'is_interval', inline='always')
@overload_method(BinaryIndexType, 'is_numeric', inline='always')
@overload_method(DatetimeIndexType, 'is_boolean', inline='always')
@overload_method(DatetimeIndexType, 'is_floating', inline='always')
@overload_method(DatetimeIndexType, 'is_categorical', inline='always')
@overload_method(DatetimeIndexType, 'is_integer', inline='always')
@overload_method(DatetimeIndexType, 'is_interval', inline='always')
@overload_method(DatetimeIndexType, 'is_numeric', inline='always')
@overload_method(DatetimeIndexType, 'is_object', inline='always')
@overload_method(TimedeltaIndexType, 'is_boolean', inline='always')
@overload_method(TimedeltaIndexType, 'is_floating', inline='always')
@overload_method(TimedeltaIndexType, 'is_categorical', inline='always')
@overload_method(TimedeltaIndexType, 'is_integer', inline='always')
@overload_method(TimedeltaIndexType, 'is_interval', inline='always')
@overload_method(TimedeltaIndexType, 'is_numeric', inline='always')
@overload_method(TimedeltaIndexType, 'is_object', inline='always')
@overload_method(RangeIndexType, 'is_boolean', inline='always')
@overload_method(RangeIndexType, 'is_floating', inline='always')
@overload_method(RangeIndexType, 'is_categorical', inline='always')
@overload_method(RangeIndexType, 'is_interval', inline='always')
@overload_method(RangeIndexType, 'is_object', inline='always')
@overload_method(IntervalIndexType, 'is_boolean', inline='always')
@overload_method(IntervalIndexType, 'is_floating', inline='always')
@overload_method(IntervalIndexType, 'is_categorical', inline='always')
@overload_method(IntervalIndexType, 'is_integer', inline='always')
@overload_method(IntervalIndexType, 'is_numeric', inline='always')
@overload_method(IntervalIndexType, 'is_object', inline='always')
@overload_method(CategoricalIndexType, 'is_boolean', inline='always')
@overload_method(CategoricalIndexType, 'is_floating', inline='always')
@overload_method(CategoricalIndexType, 'is_integer', inline='always')
@overload_method(CategoricalIndexType, 'is_interval', inline='always')
@overload_method(CategoricalIndexType, 'is_numeric', inline='always')
@overload_method(CategoricalIndexType, 'is_object', inline='always')
@overload_method(PeriodIndexType, 'is_boolean', inline='always')
@overload_method(PeriodIndexType, 'is_floating', inline='always')
@overload_method(PeriodIndexType, 'is_categorical', inline='always')
@overload_method(PeriodIndexType, 'is_integer', inline='always')
@overload_method(PeriodIndexType, 'is_interval', inline='always')
@overload_method(PeriodIndexType, 'is_numeric', inline='always')
@overload_method(PeriodIndexType, 'is_object', inline='always')
@overload_method(MultiIndexType, 'is_boolean', inline='always')
@overload_method(MultiIndexType, 'is_floating', inline='always')
@overload_method(MultiIndexType, 'is_categorical', inline='always')
@overload_method(MultiIndexType, 'is_integer', inline='always')
@overload_method(MultiIndexType, 'is_interval', inline='always')
@overload_method(MultiIndexType, 'is_numeric', inline='always')
def overload_is_methods_false(I):
    return lambda I: False


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    if isinstance(ty.data, bodo.DatetimeArrayType):
        data = context.get_constant_generic(builder, ty.data, pyval.array)
    else:
        data = context.get_constant_generic(builder, types.Array(types.
            int64, 1, 'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    ymyu__nmst = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, ymyu__nmst])


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, bodo.IntegerArrayType(
        types.int64), pd.arrays.IntegerArray(pyval.asi8, pyval.isna()))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    ymyu__nmst = context.get_constant_null(types.DictType(types.int64,
        types.int64))
    return lir.Constant.literal_struct([data, name, ymyu__nmst])


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    dtype = ty.dtype
    ymyu__nmst = context.get_constant_null(types.DictType(dtype, types.int64))
    return lir.Constant.literal_struct([data, name, ymyu__nmst])


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    vhaj__zrgl = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, vhaj__zrgl, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    ymyu__nmst = context.get_constant_null(types.DictType(scalar_type,
        types.int64))
    return lir.Constant.literal_struct([data, name, ymyu__nmst])


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [hfc__axcb] = sig.args
    [index] = args
    wbs__yngj = context.make_helper(builder, hfc__axcb, value=index)
    nyj__gjbe = context.make_helper(builder, sig.return_type)
    lga__gff = cgutils.alloca_once_value(builder, wbs__yngj.start)
    lbltp__ahkl = context.get_constant(types.intp, 0)
    ctjok__rjov = cgutils.alloca_once_value(builder, lbltp__ahkl)
    nyj__gjbe.iter = lga__gff
    nyj__gjbe.stop = wbs__yngj.stop
    nyj__gjbe.step = wbs__yngj.step
    nyj__gjbe.count = ctjok__rjov
    zzbw__mkipr = builder.sub(wbs__yngj.stop, wbs__yngj.start)
    idzxy__uldyv = context.get_constant(types.intp, 1)
    qpa__ickou = builder.icmp_signed('>', zzbw__mkipr, lbltp__ahkl)
    zsfo__hgxpb = builder.icmp_signed('>', wbs__yngj.step, lbltp__ahkl)
    wsxw__awxlv = builder.not_(builder.xor(qpa__ickou, zsfo__hgxpb))
    with builder.if_then(wsxw__awxlv):
        xubx__dwhze = builder.srem(zzbw__mkipr, wbs__yngj.step)
        xubx__dwhze = builder.select(qpa__ickou, xubx__dwhze, builder.neg(
            xubx__dwhze))
        kyjq__iwao = builder.icmp_signed('>', xubx__dwhze, lbltp__ahkl)
        hebkg__wofv = builder.add(builder.sdiv(zzbw__mkipr, wbs__yngj.step),
            builder.select(kyjq__iwao, idzxy__uldyv, lbltp__ahkl))
        builder.store(hebkg__wofv, ctjok__rjov)
    nllyu__nhxia = nyj__gjbe._getvalue()
    fyp__cfp = impl_ret_new_ref(context, builder, sig.return_type, nllyu__nhxia
        )
    return fyp__cfp


def _install_index_getiter():
    index_types = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in index_types:
        lower_builtin('getiter', typ)(numba.np.arrayobj.getiter_array)


_install_index_getiter()
index_unsupported_methods = ['append', 'asof', 'asof_locs', 'astype',
    'delete', 'drop', 'droplevel', 'dropna', 'equals', 'factorize',
    'fillna', 'format', 'get_indexer', 'get_indexer_for',
    'get_indexer_non_unique', 'get_level_values', 'get_slice_bound',
    'get_value', 'groupby', 'holds_integer', 'identical', 'insert', 'is_',
    'is_mixed', 'is_type_compatible', 'item', 'join', 'memory_usage',
    'ravel', 'reindex', 'searchsorted', 'set_names', 'set_value', 'shift',
    'slice_indexer', 'slice_locs', 'sort', 'sortlevel', 'str',
    'to_flat_index', 'to_native_types', 'transpose', 'value_counts', 'view']
index_unsupported_atrs = ['array', 'asi8', 'has_duplicates', 'hasnans',
    'is_unique']
cat_idx_unsupported_atrs = ['codes', 'categories', 'ordered',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing']
cat_idx_unsupported_methods = ['rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered', 'get_loc', 'isin',
    'all', 'any', 'union', 'intersection', 'difference', 'symmetric_difference'
    ]
interval_idx_unsupported_atrs = ['closed', 'is_empty',
    'is_non_overlapping_monotonic', 'is_overlapping', 'left', 'right',
    'mid', 'length', 'values', 'nbytes', 'is_monotonic',
    'is_monotonic_increasing', 'is_monotonic_decreasing', 'dtype']
interval_idx_unsupported_methods = ['contains', 'copy', 'overlaps',
    'set_closed', 'to_tuples', 'take', 'get_loc', 'isna', 'isnull', 'map',
    'isin', 'all', 'any', 'argsort', 'sort_values', 'argmax', 'argmin',
    'where', 'putmask', 'nunique', 'union', 'intersection', 'difference',
    'symmetric_difference', 'to_series', 'to_frame', 'to_list', 'tolist',
    'repeat', 'min', 'max']
multi_index_unsupported_atrs = ['levshape', 'levels', 'codes', 'dtypes',
    'values', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
multi_index_unsupported_methods = ['copy', 'set_levels', 'set_codes',
    'swaplevel', 'reorder_levels', 'remove_unused_levels', 'get_loc',
    'get_locs', 'get_loc_level', 'take', 'isna', 'isnull', 'map', 'isin',
    'unique', 'all', 'any', 'argsort', 'sort_values', 'argmax', 'argmin',
    'where', 'putmask', 'nunique', 'union', 'intersection', 'difference',
    'symmetric_difference', 'to_series', 'to_list', 'tolist', 'to_numpy',
    'repeat', 'min', 'max']
dt_index_unsupported_atrs = ['time', 'timez', 'tz', 'freq', 'freqstr',
    'inferred_freq']
dt_index_unsupported_methods = ['normalize', 'strftime', 'snap',
    'tz_localize', 'round', 'floor', 'ceil', 'to_period', 'to_perioddelta',
    'to_pydatetime', 'month_name', 'day_name', 'mean', 'indexer_at_time',
    'indexer_between', 'indexer_between_time', 'all', 'any']
td_index_unsupported_atrs = ['components', 'inferred_freq']
td_index_unsupported_methods = ['to_pydatetime', 'round', 'floor', 'ceil',
    'mean', 'all', 'any']
period_index_unsupported_atrs = ['day', 'dayofweek', 'day_of_week',
    'dayofyear', 'day_of_year', 'days_in_month', 'daysinmonth', 'freq',
    'freqstr', 'hour', 'is_leap_year', 'minute', 'month', 'quarter',
    'second', 'week', 'weekday', 'weekofyear', 'year', 'end_time', 'qyear',
    'start_time', 'is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing', 'dtype']
period_index_unsupported_methods = ['asfreq', 'strftime', 'to_timestamp',
    'isin', 'unique', 'all', 'any', 'where', 'putmask', 'sort_values',
    'union', 'intersection', 'difference', 'symmetric_difference',
    'to_series', 'to_frame', 'to_numpy', 'to_list', 'tolist', 'repeat',
    'min', 'max']
string_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
string_index_unsupported_methods = ['min', 'max']
binary_index_unsupported_atrs = ['is_monotonic', 'is_monotonic_increasing',
    'is_monotonic_decreasing']
binary_index_unsupported_methods = ['repeat', 'min', 'max']
index_types = [('pandas.RangeIndex.{}', RangeIndexType), (
    'pandas.Index.{} with numeric data', NumericIndexType), (
    'pandas.Index.{} with string data', StringIndexType), (
    'pandas.Index.{} with binary data', BinaryIndexType), (
    'pandas.TimedeltaIndex.{}', TimedeltaIndexType), (
    'pandas.IntervalIndex.{}', IntervalIndexType), (
    'pandas.CategoricalIndex.{}', CategoricalIndexType), (
    'pandas.PeriodIndex.{}', PeriodIndexType), ('pandas.DatetimeIndex.{}',
    DatetimeIndexType), ('pandas.MultiIndex.{}', MultiIndexType)]
for name, typ in index_types:
    idx_typ_to_format_str_map[typ] = name


def _install_index_unsupported():
    for elxo__krf in index_unsupported_methods:
        for hkp__hutjx, typ in index_types:
            overload_method(typ, elxo__krf, no_unliteral=True)(
                create_unsupported_overload(hkp__hutjx.format(elxo__krf +
                '()')))
    for mwiq__xry in index_unsupported_atrs:
        for hkp__hutjx, typ in index_types:
            overload_attribute(typ, mwiq__xry, no_unliteral=True)(
                create_unsupported_overload(hkp__hutjx.format(mwiq__xry)))
    kfwxm__rix = [(StringIndexType, string_index_unsupported_atrs), (
        BinaryIndexType, binary_index_unsupported_atrs), (
        CategoricalIndexType, cat_idx_unsupported_atrs), (IntervalIndexType,
        interval_idx_unsupported_atrs), (MultiIndexType,
        multi_index_unsupported_atrs), (DatetimeIndexType,
        dt_index_unsupported_atrs), (TimedeltaIndexType,
        td_index_unsupported_atrs), (PeriodIndexType,
        period_index_unsupported_atrs)]
    rgn__ilk = [(CategoricalIndexType, cat_idx_unsupported_methods), (
        IntervalIndexType, interval_idx_unsupported_methods), (
        MultiIndexType, multi_index_unsupported_methods), (
        DatetimeIndexType, dt_index_unsupported_methods), (
        TimedeltaIndexType, td_index_unsupported_methods), (PeriodIndexType,
        period_index_unsupported_methods), (BinaryIndexType,
        binary_index_unsupported_methods), (StringIndexType,
        string_index_unsupported_methods)]
    for typ, rmvb__pcav in rgn__ilk:
        hkp__hutjx = idx_typ_to_format_str_map[typ]
        for dzbk__agn in rmvb__pcav:
            overload_method(typ, dzbk__agn, no_unliteral=True)(
                create_unsupported_overload(hkp__hutjx.format(dzbk__agn +
                '()')))
    for typ, ukhob__uvhr in kfwxm__rix:
        hkp__hutjx = idx_typ_to_format_str_map[typ]
        for mwiq__xry in ukhob__uvhr:
            overload_attribute(typ, mwiq__xry, no_unliteral=True)(
                create_unsupported_overload(hkp__hutjx.format(mwiq__xry)))


_install_index_unsupported()
