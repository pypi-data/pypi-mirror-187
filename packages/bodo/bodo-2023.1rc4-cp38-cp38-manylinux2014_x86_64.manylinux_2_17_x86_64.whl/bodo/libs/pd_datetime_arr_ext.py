"""DatetimeArray extension for Pandas DatetimeArray with timezone support."""
import operator
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoArrayIterator, BodoError, get_literal_value, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str


class PandasDatetimeTZDtype(types.Type):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        super(PandasDatetimeTZDtype, self).__init__(name=
            f'PandasDatetimeTZDtype[{tz}]')


register_model(PandasDatetimeTZDtype)(models.OpaqueModel)


@lower_constant(PandasDatetimeTZDtype)
def lower_constant_pd_datetime_tz_dtype(context, builder, typ, pyval):
    return context.get_dummy_value()


@box(PandasDatetimeTZDtype)
def box_pd_datetime_tzdtype(typ, val, c):
    jljv__yemo = c.context.insert_const_string(c.builder.module, 'pandas')
    ilf__joef = c.pyapi.import_module_noblock(jljv__yemo)
    nsfky__niakg = c.context.get_constant_generic(c.builder, types.
        unicode_type, 'ns')
    pke__iky = c.pyapi.from_native_value(types.unicode_type, nsfky__niakg,
        c.env_manager)
    if isinstance(typ.tz, str):
        ucn__zhrzh = c.context.get_constant_generic(c.builder, types.
            unicode_type, typ.tz)
        wubzg__znwr = c.pyapi.from_native_value(types.unicode_type,
            ucn__zhrzh, c.env_manager)
    else:
        rit__vvcfw = nanoseconds_to_offset(typ.tz)
        wubzg__znwr = c.pyapi.unserialize(c.pyapi.serialize_object(rit__vvcfw))
    rnc__ebpu = c.pyapi.call_method(ilf__joef, 'DatetimeTZDtype', (pke__iky,
        wubzg__znwr))
    c.pyapi.decref(pke__iky)
    c.pyapi.decref(wubzg__znwr)
    c.pyapi.decref(ilf__joef)
    c.context.nrt.decref(c.builder, typ, val)
    return rnc__ebpu


@unbox(PandasDatetimeTZDtype)
def unbox_pd_datetime_tzdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


@typeof_impl.register(pd.DatetimeTZDtype)
def typeof_pd_int_dtype(val, c):
    return PandasDatetimeTZDtype(val.tz)


def get_pytz_type_info(pytz_type):
    if isinstance(pytz_type, pytz._FixedOffset):
        prb__kyxkq = pd.Timedelta(pytz_type._offset).value
    else:
        prb__kyxkq = pytz_type.zone
        if prb__kyxkq not in pytz.all_timezones_set:
            raise BodoError(
                'Unsupported timezone type. Timezones must be a fixedOffset or contain a zone found in pytz.all_timezones'
                )
    return prb__kyxkq


def nanoseconds_to_offset(nanoseconds):
    gvzw__cra = nanoseconds // (60 * 1000 * 1000 * 1000)
    return pytz.FixedOffset(gvzw__cra)


class DatetimeArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, tz):
        if isinstance(tz, (pytz._FixedOffset, pytz.tzinfo.BaseTzInfo)):
            tz = get_pytz_type_info(tz)
        if not isinstance(tz, (int, str)):
            raise BodoError(
                'Timezone must be either a valid pytz type with a zone or a fixed offset'
                )
        self.tz = tz
        self._data_array_type = types.Array(types.NPDatetime('ns'), 1, 'C')
        self._dtype = PandasDatetimeTZDtype(tz)
        super(DatetimeArrayType, self).__init__(name=
            f'PandasDatetimeArray[{tz}]')

    @property
    def data_array_type(self):
        return self._data_array_type

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self._dtype

    def copy(self):
        return DatetimeArrayType(self.tz)


@register_model(DatetimeArrayType)
class PandasDatetimeArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jadve__mvk = [('data', fe_type.data_array_type)]
        models.StructModel.__init__(self, dmm, fe_type, jadve__mvk)


make_attribute_wrapper(DatetimeArrayType, 'data', '_data')


@typeof_impl.register(pd.arrays.DatetimeArray)
def typeof_pd_datetime_array(val, c):
    if val.tz is None:
        raise BodoError(
            "Cannot support timezone naive pd.arrays.DatetimeArray. Please convert to a numpy array with .astype('datetime64[ns]')."
            )
    if val.dtype.unit != 'ns':
        raise BodoError("Timezone-aware datetime data requires 'ns' units")
    return DatetimeArrayType(val.dtype.tz)


@unbox(DatetimeArrayType)
def unbox_pd_datetime_array(typ, val, c):
    cbywx__lzs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    kogz__qdmf = c.pyapi.string_from_constant_string('datetime64[ns]')
    hwgxy__lfk = c.pyapi.call_method(val, 'to_numpy', (kogz__qdmf,))
    cbywx__lzs.data = c.unbox(typ.data_array_type, hwgxy__lfk).value
    c.pyapi.decref(hwgxy__lfk)
    mie__rqor = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cbywx__lzs._getvalue(), is_error=mie__rqor)


@box(DatetimeArrayType)
def box_pd_datetime_array(typ, val, c):
    cbywx__lzs = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.data_array_type, cbywx__lzs.data)
    nlecu__loo = c.pyapi.from_native_value(typ.data_array_type, cbywx__lzs.
        data, c.env_manager)
    nsfky__niakg = c.context.get_constant_generic(c.builder, types.
        unicode_type, 'ns')
    pke__iky = c.pyapi.from_native_value(types.unicode_type, nsfky__niakg,
        c.env_manager)
    if isinstance(typ.tz, str):
        ucn__zhrzh = c.context.get_constant_generic(c.builder, types.
            unicode_type, typ.tz)
        wubzg__znwr = c.pyapi.from_native_value(types.unicode_type,
            ucn__zhrzh, c.env_manager)
    else:
        rit__vvcfw = nanoseconds_to_offset(typ.tz)
        wubzg__znwr = c.pyapi.unserialize(c.pyapi.serialize_object(rit__vvcfw))
    jljv__yemo = c.context.insert_const_string(c.builder.module, 'pandas')
    ilf__joef = c.pyapi.import_module_noblock(jljv__yemo)
    kla__nmrp = c.pyapi.call_method(ilf__joef, 'DatetimeTZDtype', (pke__iky,
        wubzg__znwr))
    zrr__tgu = c.pyapi.object_getattr_string(ilf__joef, 'arrays')
    rnc__ebpu = c.pyapi.call_method(zrr__tgu, 'DatetimeArray', (nlecu__loo,
        kla__nmrp))
    c.pyapi.decref(nlecu__loo)
    c.pyapi.decref(pke__iky)
    c.pyapi.decref(wubzg__znwr)
    c.pyapi.decref(ilf__joef)
    c.pyapi.decref(kla__nmrp)
    c.pyapi.decref(zrr__tgu)
    c.context.nrt.decref(c.builder, typ, val)
    return rnc__ebpu


@intrinsic
def init_pandas_datetime_array(typingctx, data, tz):

    def codegen(context, builder, sig, args):
        data, tz = args
        iqgtw__xucjz = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        iqgtw__xucjz.data = data
        context.nrt.incref(builder, sig.args[0], data)
        return iqgtw__xucjz._getvalue()
    if is_overload_constant_str(tz) or is_overload_constant_int(tz):
        ucn__zhrzh = get_literal_value(tz)
    else:
        raise BodoError('tz must be a constant string or Fixed Offset')
    qcx__kmhfy = DatetimeArrayType(ucn__zhrzh)
    sig = qcx__kmhfy(qcx__kmhfy.data_array_type, tz)
    return sig, codegen


@numba.njit(no_cpython_wrapper=True)
def alloc_pd_datetime_array(n, tz):
    qgjng__mxldq = np.empty(n, dtype='datetime64[ns]')
    return init_pandas_datetime_array(qgjng__mxldq, tz)


def alloc_pd_datetime_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_pd_datetime_arr_ext_alloc_pd_datetime_array
    ) = alloc_pd_datetime_array_equiv


@overload(len, no_unliteral=True)
def overload_pd_datetime_arr_len(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: len(A._data)


@lower_constant(DatetimeArrayType)
def lower_constant_pd_datetime_arr(context, builder, typ, pyval):
    uxgu__xtl = context.get_constant_generic(builder, typ.data_array_type,
        pyval.to_numpy('datetime64[ns]'))
    desph__gjb = lir.Constant.literal_struct([uxgu__xtl])
    return desph__gjb


@overload_attribute(DatetimeArrayType, 'shape')
def overload_pd_datetime_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeArrayType, 'nbytes')
def overload_pd_datetime_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(DatetimeArrayType, 'tz_convert', no_unliteral=True)
def overload_pd_datetime_tz_convert(A, tz):
    if tz == types.none:

        def impl(A, tz):
            return A._data.copy()
        return impl
    else:

        def impl(A, tz):
            return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload_method(DatetimeArrayType, 'copy', no_unliteral=True)
def overload_pd_datetime_tz_convert(A):
    tz = A.tz

    def impl(A):
        return init_pandas_datetime_array(A._data.copy(), tz)
    return impl


@overload_attribute(DatetimeArrayType, 'dtype', no_unliteral=True)
def overload_pd_datetime_dtype(A):
    tz = A.tz
    dtype = pd.DatetimeTZDtype('ns', tz)

    def impl(A):
        return dtype
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_getitem(A, ind):
    if not isinstance(A, DatetimeArrayType):
        return
    tz = A.tz
    if isinstance(ind, types.Integer):

        def impl(A, ind):
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(bodo
                .hiframes.pd_timestamp_ext.dt64_to_integer(A._data[ind]), tz)
        return impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            rzinj__dlj = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(rzinj__dlj, tz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl_int_arr(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            rzinj__dlj = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(rzinj__dlj, tz)
        return impl_int_arr
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            rzinj__dlj = ensure_contig_if_np(A._data[ind])
            return init_pandas_datetime_array(rzinj__dlj, tz)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            'operator.getitem with DatetimeArrayType is only supported with an integer index, int arr, boolean array, or slice.'
            )


@overload(operator.setitem, no_unliteral=True)
def overload_getitem(A, ind, val):
    if not isinstance(A, DatetimeArrayType):
        return
    tz = A.tz
    if isinstance(ind, types.Integer):
        if not isinstance(val, bodo.PandasTimestampType):
            raise BodoError(
                'operator.setitem with DatetimeArrayType requires a Timestamp value'
                )
        if val.tz != tz:
            raise BodoError(
                'operator.setitem with DatetimeArrayType requires the Timestamp value to share the same timezone'
                )

        def impl(A, ind, val):
            A._data[ind] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
                .value)
        return impl
    raise BodoError(
        'operator.setitem with DatetimeArrayType is only supported with an integer index'
        )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def unwrap_tz_array(A):
    if isinstance(A, DatetimeArrayType):
        return lambda A: A._data
    return lambda A: A


def unwrap_tz_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    bbpvy__awk = args[0]
    if equiv_set.has_shape(bbpvy__awk):
        return ArrayAnalysis.AnalyzeResult(shape=bbpvy__awk, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_pd_datetime_arr_ext_unwrap_tz_array
    ) = unwrap_tz_array_equiv


def create_cmp_op_overload_arr(op):
    from bodo.hiframes.pd_timestamp_ext import PandasTimestampType

    def overload_datetime_arr_cmp(lhs, rhs):
        if not (isinstance(lhs, DatetimeArrayType) or isinstance(rhs,
            DatetimeArrayType)):
            return
        if isinstance(lhs, DatetimeArrayType) and (isinstance(rhs,
            PandasTimestampType) or rhs == bodo.datetime_date_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                cnksu__bejd = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qttgq__ssrfc in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, qttgq__ssrfc):
                        bodo.libs.array_kernels.setna(cnksu__bejd, qttgq__ssrfc
                            )
                    else:
                        cnksu__bejd[qttgq__ssrfc] = op(lhs[qttgq__ssrfc], rhs)
                return cnksu__bejd
            return impl
        elif (isinstance(lhs, PandasTimestampType) or lhs == bodo.
            datetime_date_type) and isinstance(rhs, DatetimeArrayType):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                cnksu__bejd = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qttgq__ssrfc in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, qttgq__ssrfc):
                        bodo.libs.array_kernels.setna(cnksu__bejd, qttgq__ssrfc
                            )
                    else:
                        cnksu__bejd[qttgq__ssrfc] = op(lhs, rhs[qttgq__ssrfc])
                return cnksu__bejd
            return impl
        elif (isinstance(lhs, DatetimeArrayType) or lhs == bodo.
            datetime_date_array_type) and (isinstance(rhs,
            DatetimeArrayType) or rhs == bodo.datetime_date_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                cnksu__bejd = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qttgq__ssrfc in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, qttgq__ssrfc
                        ) or bodo.libs.array_kernels.isna(rhs, qttgq__ssrfc):
                        bodo.libs.array_kernels.setna(cnksu__bejd, qttgq__ssrfc
                            )
                    else:
                        cnksu__bejd[qttgq__ssrfc] = op(lhs[qttgq__ssrfc],
                            rhs[qttgq__ssrfc])
                return cnksu__bejd
            return impl
        elif isinstance(lhs, DatetimeArrayType) and (isinstance(rhs, types.
            Array) and rhs.dtype == bodo.datetime64ns):
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {lhs.tz} and argument 1 is timezone-naive. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        elif (isinstance(lhs, types.Array) and lhs.dtype == bodo.datetime64ns
            ) and isinstance(rhs, DatetimeArrayType):
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 is timezone-naive and argument 1 has timezone {rhs.tz}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
    return overload_datetime_arr_cmp


def overload_add_operator_datetime_arr(lhs, rhs):
    if isinstance(lhs, DatetimeArrayType):
        if rhs == bodo.week_type:
            sbwgx__ngf = lhs.tz

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                cnksu__bejd = (bodo.libs.pd_datetime_arr_ext.
                    alloc_pd_datetime_array(n, sbwgx__ngf))
                for qttgq__ssrfc in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, qttgq__ssrfc):
                        bodo.libs.array_kernels.setna(cnksu__bejd, qttgq__ssrfc
                            )
                    else:
                        cnksu__bejd[qttgq__ssrfc] = lhs[qttgq__ssrfc] + rhs
                return cnksu__bejd
            return impl
        else:
            raise BodoError(
                f'add operator not supported between Timezone-aware timestamp and {rhs}. Please convert to timezone naive with ts.tz_convert(None)'
                )
    elif lhs == bodo.week_type:
        sbwgx__ngf = rhs.tz

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            n = len(rhs)
            cnksu__bejd = (bodo.libs.pd_datetime_arr_ext.
                alloc_pd_datetime_array(n, sbwgx__ngf))
            for qttgq__ssrfc in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(rhs, qttgq__ssrfc):
                    bodo.libs.array_kernels.setna(cnksu__bejd, qttgq__ssrfc)
                else:
                    cnksu__bejd[qttgq__ssrfc] = lhs + rhs[qttgq__ssrfc]
            return cnksu__bejd
        return impl
    else:
        raise BodoError(
            f'add operator not supported between {lhs} and Timezone-aware timestamp. Please convert to timezone naive with ts.tz_convert(None)'
            )


@register_jitable
def convert_months_offset_to_days(curr_year, curr_month, curr_day, num_months):
    pcz__htr = curr_month + num_months - 1
    yyanv__emy = pcz__htr % 12 + 1
    hlml__zgp = pcz__htr // 12
    lbvmq__gcor = curr_year + hlml__zgp
    nnne__dnpoc = bodo.hiframes.pd_timestamp_ext.get_days_in_month(lbvmq__gcor,
        yyanv__emy)
    xdpt__tqnq = min(nnne__dnpoc, curr_day)
    wlsf__pvqd = pd.Timestamp(year=curr_year, month=curr_month, day=curr_day)
    lsafb__ndgr = pd.Timestamp(year=lbvmq__gcor, month=yyanv__emy, day=
        xdpt__tqnq)
    return lsafb__ndgr - wlsf__pvqd
