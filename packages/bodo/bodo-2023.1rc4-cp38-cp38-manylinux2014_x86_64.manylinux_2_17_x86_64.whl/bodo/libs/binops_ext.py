""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.series_impl import SeriesType
from bodo.hiframes.time_ext import TimeType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        if is_cmp_tz_mismatch(lhs, rhs):
            yaa__zup, ejs__vgxg = get_series_tz(lhs)
            pcen__ksrqe, ejs__vgxg = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {yaa__zup} and argument 1 has timezone {pcen__ksrqe}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        ubpn__emmv = lhs.data if isinstance(lhs, SeriesType) else lhs
        qgrhg__dnapo = rhs.data if isinstance(rhs, SeriesType) else rhs
        if ubpn__emmv in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and qgrhg__dnapo.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            ubpn__emmv = qgrhg__dnapo.dtype
        elif qgrhg__dnapo in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and ubpn__emmv.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            qgrhg__dnapo = ubpn__emmv.dtype
        nte__gkjo = ubpn__emmv, qgrhg__dnapo
        hlfh__bjm = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            qijlj__kyx = self.context.resolve_function_type(self.key,
                nte__gkjo, {}).return_type
        except Exception as jgi__anab:
            raise BodoError(hlfh__bjm)
        if is_overload_bool(qijlj__kyx):
            raise BodoError(hlfh__bjm)
        ieqlb__dxuty = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        mgsc__irnp = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        fkpef__ykoj = types.bool_
        eyf__bym = SeriesType(fkpef__ykoj, qijlj__kyx, ieqlb__dxuty, mgsc__irnp
            )
        return eyf__bym(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        beyh__qrmja = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if beyh__qrmja is None:
            beyh__qrmja = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, beyh__qrmja, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        ubpn__emmv = lhs.data if isinstance(lhs, SeriesType) else lhs
        qgrhg__dnapo = rhs.data if isinstance(rhs, SeriesType) else rhs
        nte__gkjo = ubpn__emmv, qgrhg__dnapo
        hlfh__bjm = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            qijlj__kyx = self.context.resolve_function_type(self.key,
                nte__gkjo, {}).return_type
        except Exception as uld__qdxbb:
            raise BodoError(hlfh__bjm)
        ieqlb__dxuty = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        mgsc__irnp = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        fkpef__ykoj = qijlj__kyx.dtype
        eyf__bym = SeriesType(fkpef__ykoj, qijlj__kyx, ieqlb__dxuty, mgsc__irnp
            )
        return eyf__bym(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        beyh__qrmja = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if beyh__qrmja is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                beyh__qrmja = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, beyh__qrmja, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if (isinstance(lhs, bodo.PandasTimestampType) and rhs in (
        datetime_timedelta_type, pd_timedelta_type) or lhs ==
        pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type):
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        if op not in [operator.add, operator.sub]:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add and (isinstance(lhs, bodo.DatetimeArrayType) or
            isinstance(rhs, bodo.DatetimeArrayType)):
            return (bodo.libs.pd_datetime_arr_ext.
                overload_add_operator_datetime_arr(lhs, rhs))
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        if isinstance(lhs, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ) or isinstance(rhs, bodo.libs.pd_datetime_arr_ext.
            DatetimeArrayType):
            return bodo.libs.pd_datetime_arr_ext.create_cmp_op_overload_arr(op
                )(lhs, rhs)
        if isinstance(lhs, types.Array
            ) and lhs.dtype == bodo.datetime64ns and rhs in (
            datetime_date_array_type, datetime_date_type) or lhs in (
            datetime_date_array_type, datetime_date_type) and isinstance(rhs,
            types.Array) and rhs.dtype == bodo.datetime64ns:
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_array_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            beyh__qrmja = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return beyh__qrmja(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):
            return bodo.hiframes.time_ext.create_cmp_op_overload(op)(lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            beyh__qrmja = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return beyh__qrmja(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    udz__oowie = lhs == datetime_timedelta_type and rhs == datetime_date_type
    urvop__ynwet = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return udz__oowie or urvop__ynwet


def add_timestamp(lhs, rhs):
    mmqr__cgr = isinstance(lhs, bodo.PandasTimestampType
        ) and is_timedelta_type(rhs)
    ntoci__qyzo = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return mmqr__cgr or ntoci__qyzo


def add_datetime_and_timedeltas(lhs, rhs):
    ifb__gssa = [datetime_timedelta_type, pd_timedelta_type]
    hfcuv__ojoh = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    jsz__dhnju = lhs in ifb__gssa and rhs in ifb__gssa
    run__caqo = (lhs == datetime_datetime_type and rhs in ifb__gssa or rhs ==
        datetime_datetime_type and lhs in ifb__gssa)
    return jsz__dhnju or run__caqo


def mul_string_arr_and_int(lhs, rhs):
    qgrhg__dnapo = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    ubpn__emmv = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return qgrhg__dnapo or ubpn__emmv


def mul_timedelta_and_int(lhs, rhs):
    udz__oowie = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    urvop__ynwet = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return udz__oowie or urvop__ynwet


def mul_date_offset_and_int(lhs, rhs):
    krhqd__wah = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    uet__kjbb = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return krhqd__wah or uet__kjbb


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    xdqmh__tqkl = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    oxua__sjl = week_type, month_begin_type, month_end_type
    xyfqm__lwbvw = date_offset_type,
    return rhs in oxua__sjl and isinstance(lhs, tz_aware_classes) or (rhs in
        xyfqm__lwbvw or rhs in oxua__sjl) and lhs in xdqmh__tqkl


def sub_dt_index_and_timestamp(lhs, rhs):
    xuhau__jax = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    kaay__ldzj = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return xuhau__jax or kaay__ldzj


def sub_dt_or_td(lhs, rhs):
    rcu__vxgr = lhs == datetime_date_type and rhs == datetime_timedelta_type
    wqnqx__wfa = lhs == datetime_date_type and rhs == datetime_date_type
    wdy__hmft = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return rcu__vxgr or wqnqx__wfa or wdy__hmft


def sub_datetime_and_timedeltas(lhs, rhs):
    ixc__gyklt = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    wtfjn__ocl = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return ixc__gyklt or wtfjn__ocl


def div_timedelta_and_int(lhs, rhs):
    jsz__dhnju = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    knyft__jci = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return jsz__dhnju or knyft__jci


def div_datetime_timedelta(lhs, rhs):
    jsz__dhnju = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    knyft__jci = lhs == datetime_timedelta_type and rhs == types.int64
    return jsz__dhnju or knyft__jci


def mod_timedeltas(lhs, rhs):
    cghfh__nsx = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    gubdd__tks = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return cghfh__nsx or gubdd__tks


def cmp_dt_index_to_string(lhs, rhs):
    xuhau__jax = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    kaay__ldzj = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return xuhau__jax or kaay__ldzj


def cmp_timestamp_or_date(lhs, rhs):
    pjqj__hdwgf = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    wvgi__ety = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        isinstance(rhs, bodo.hiframes.pd_timestamp_ext.PandasTimestampType))
    sliyk__gyx = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    vuod__llpz = lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns
    aiewr__fna = rhs == pd_timestamp_tz_naive_type and lhs == bodo.datetime64ns
    return pjqj__hdwgf or wvgi__ety or sliyk__gyx or vuod__llpz or aiewr__fna


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            tjp__mugr = val.data.tz
        else:
            tjp__mugr = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        tjp__mugr = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        tjp__mugr = None
    elif isinstance(val, bodo.PandasTimestampType):
        tjp__mugr = val.tz
    elif val == bodo.datetime64ns:
        tjp__mugr = None
    else:
        return None, False
    return tjp__mugr, True


def is_cmp_tz_mismatch(lhs, rhs):
    yaa__zup, caf__egcmz = get_series_tz(lhs)
    pcen__ksrqe, wmyjg__cdywr = get_series_tz(rhs)
    return caf__egcmz and wmyjg__cdywr and yaa__zup != pcen__ksrqe


def cmp_timeseries(lhs, rhs):
    ems__hdso = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    tomw__uwzy = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    asxj__zbh = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    hgn__dszv = ems__hdso or tomw__uwzy or asxj__zbh
    vgq__gpgx = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    kpj__gwq = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    imkg__zjwi = vgq__gpgx or kpj__gwq
    return hgn__dszv or imkg__zjwi


def cmp_timedeltas(lhs, rhs):
    jsz__dhnju = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in jsz__dhnju and rhs in jsz__dhnju


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    dhu__tcmek = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return dhu__tcmek


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    wslta__jmkg = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    mmwsc__zkns = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    qxvpq__mmna = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    lmq__srj = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return wslta__jmkg or mmwsc__zkns or qxvpq__mmna or lmq__srj


def args_td_and_int_array(lhs, rhs):
    qvrl__mtwfg = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    nbvz__zqij = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return qvrl__mtwfg and nbvz__zqij


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        urvop__ynwet = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        udz__oowie = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        ijgx__prne = urvop__ynwet or udz__oowie
        gqbv__yuzri = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        nsgcn__kkx = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        tvmdt__jnuam = gqbv__yuzri or nsgcn__kkx
        xpzu__suxai = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        inw__ryiu = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        gngt__mfh = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ulzr__omaat = xpzu__suxai or inw__ryiu or gngt__mfh
        zva__jmhlj = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        kzikj__dtf = isinstance(lhs, tys) or isinstance(rhs, tys)
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (ijgx__prne or tvmdt__jnuam or ulzr__omaat or zva__jmhlj or
            kzikj__dtf or vvhti__vzpfn)
    if op == operator.pow:
        yndue__cgz = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        yuzuc__ugwni = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        gngt__mfh = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return yndue__cgz or yuzuc__ugwni or gngt__mfh or vvhti__vzpfn
    if op == operator.floordiv:
        inw__ryiu = lhs in types.real_domain and rhs in types.real_domain
        xpzu__suxai = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bzxin__vssn = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        jsz__dhnju = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (inw__ryiu or xpzu__suxai or bzxin__vssn or jsz__dhnju or
            vvhti__vzpfn)
    if op == operator.truediv:
        kajbh__njhfn = lhs in machine_ints and rhs in machine_ints
        inw__ryiu = lhs in types.real_domain and rhs in types.real_domain
        gngt__mfh = lhs in types.complex_domain and rhs in types.complex_domain
        xpzu__suxai = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bzxin__vssn = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        jhgd__fclhc = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jsz__dhnju = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (kajbh__njhfn or inw__ryiu or gngt__mfh or xpzu__suxai or
            bzxin__vssn or jhgd__fclhc or jsz__dhnju or vvhti__vzpfn)
    if op == operator.mod:
        kajbh__njhfn = lhs in machine_ints and rhs in machine_ints
        inw__ryiu = lhs in types.real_domain and rhs in types.real_domain
        xpzu__suxai = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        bzxin__vssn = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (kajbh__njhfn or inw__ryiu or xpzu__suxai or bzxin__vssn or
            vvhti__vzpfn)
    if op == operator.add or op == operator.sub:
        ijgx__prne = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        fxbz__jsc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        gctpc__buzto = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        vhnk__blkn = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        xpzu__suxai = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        inw__ryiu = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        gngt__mfh = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ulzr__omaat = xpzu__suxai or inw__ryiu or gngt__mfh
        vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        aohgr__zthv = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        zva__jmhlj = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        fzsdc__oudf = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        jyzpd__vir = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        rve__tti = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        axnr__lje = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        tbkyl__xtum = fzsdc__oudf or jyzpd__vir or rve__tti or axnr__lje
        tvmdt__jnuam = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        gmtrt__okofc = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        zpax__cwf = tvmdt__jnuam or gmtrt__okofc
        ipze__ckuze = lhs == types.NPTimedelta and rhs == types.NPDatetime
        iezu__dgn = (aohgr__zthv or zva__jmhlj or tbkyl__xtum or zpax__cwf or
            ipze__ckuze)
        jipi__thkg = op == operator.add and iezu__dgn
        return (ijgx__prne or fxbz__jsc or gctpc__buzto or vhnk__blkn or
            ulzr__omaat or vvhti__vzpfn or jipi__thkg)


def cmp_op_supported_by_numba(lhs, rhs):
    vvhti__vzpfn = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    zva__jmhlj = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    ijgx__prne = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    tvtf__trv = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types
        .NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    tvmdt__jnuam = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    aohgr__zthv = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    vhnk__blkn = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    ulzr__omaat = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    fvkpm__yuxm = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    xgr__yvna = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    ply__ger = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    cvlxg__osysg = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    uxkh__epnb = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (zva__jmhlj or ijgx__prne or tvtf__trv or tvmdt__jnuam or
        aohgr__zthv or vhnk__blkn or ulzr__omaat or fvkpm__yuxm or
        xgr__yvna or ply__ger or vvhti__vzpfn or cvlxg__osysg or uxkh__epnb)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        mgh__ude = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(mgh__ude)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        mgh__ude = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(mgh__ude)


install_arith_ops()
