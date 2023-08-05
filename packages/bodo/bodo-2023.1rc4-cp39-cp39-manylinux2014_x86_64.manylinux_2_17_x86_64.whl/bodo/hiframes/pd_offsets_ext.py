"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, get_days_in_month, pd_timestamp_tz_naive_type, tz_has_transition_times
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xrp__sirnf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, xrp__sirnf)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    lrxa__tzbz = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bzr__bmm = c.pyapi.long_from_longlong(lrxa__tzbz.n)
    kopzy__fzpuv = c.pyapi.from_native_value(types.boolean, lrxa__tzbz.
        normalize, c.env_manager)
    sqhm__yyoe = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    lkl__eacct = c.pyapi.call_function_objargs(sqhm__yyoe, (bzr__bmm,
        kopzy__fzpuv))
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    c.pyapi.decref(sqhm__yyoe)
    return lkl__eacct


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    bzr__bmm = c.pyapi.object_getattr_string(val, 'n')
    kopzy__fzpuv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bzr__bmm)
    normalize = c.pyapi.to_native_value(types.bool_, kopzy__fzpuv).value
    lrxa__tzbz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lrxa__tzbz.n = n
    lrxa__tzbz.normalize = normalize
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    cbwr__qndpb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lrxa__tzbz._getvalue(), is_error=cbwr__qndpb)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        lrxa__tzbz = cgutils.create_struct_proxy(typ)(context, builder)
        lrxa__tzbz.n = args[0]
        lrxa__tzbz.normalize = args[1]
        return lrxa__tzbz._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and isinstance(rhs, PandasTimestampType):
        yzmja__ykby = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    yzmja__ykby)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=yzmja__ykby)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]
        ) and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xrp__sirnf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, xrp__sirnf)


@box(MonthEndType)
def box_month_end(typ, val, c):
    lvazb__lul = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bzr__bmm = c.pyapi.long_from_longlong(lvazb__lul.n)
    kopzy__fzpuv = c.pyapi.from_native_value(types.boolean, lvazb__lul.
        normalize, c.env_manager)
    rrcfz__sdxb = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    lkl__eacct = c.pyapi.call_function_objargs(rrcfz__sdxb, (bzr__bmm,
        kopzy__fzpuv))
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    c.pyapi.decref(rrcfz__sdxb)
    return lkl__eacct


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    bzr__bmm = c.pyapi.object_getattr_string(val, 'n')
    kopzy__fzpuv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bzr__bmm)
    normalize = c.pyapi.to_native_value(types.bool_, kopzy__fzpuv).value
    lvazb__lul = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lvazb__lul.n = n
    lvazb__lul.normalize = normalize
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    cbwr__qndpb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lvazb__lul._getvalue(), is_error=cbwr__qndpb)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        lvazb__lul = cgutils.create_struct_proxy(typ)(context, builder)
        lvazb__lul.n = args[0]
        lvazb__lul.normalize = args[1]
        return lvazb__lul._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        lvazb__lul = get_days_in_month(year, month)
        if lvazb__lul > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and isinstance(rhs, PandasTimestampType):
        yzmja__ykby = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    yzmja__ykby)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=yzmja__ykby)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]) and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xrp__sirnf = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, xrp__sirnf)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    ytyf__hyi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    lnw__wkgk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for glga__dsfd, vqxnb__cfjt in enumerate(date_offset_fields):
        c.builder.store(getattr(ytyf__hyi, vqxnb__cfjt), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(lnw__wkgk, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * glga__dsfd)), lir.IntType(64)
            .as_pointer()))
    mysfh__ksc = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    gst__irgxa = cgutils.get_or_insert_function(c.builder.module,
        mysfh__ksc, name='box_date_offset')
    hubbl__igfra = c.builder.call(gst__irgxa, [ytyf__hyi.n, ytyf__hyi.
        normalize, lnw__wkgk, ytyf__hyi.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return hubbl__igfra


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    bzr__bmm = c.pyapi.object_getattr_string(val, 'n')
    kopzy__fzpuv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(bzr__bmm)
    normalize = c.pyapi.to_native_value(types.bool_, kopzy__fzpuv).value
    lnw__wkgk = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    mysfh__ksc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    odo__awbnt = cgutils.get_or_insert_function(c.builder.module,
        mysfh__ksc, name='unbox_date_offset')
    has_kws = c.builder.call(odo__awbnt, [val, lnw__wkgk])
    ytyf__hyi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ytyf__hyi.n = n
    ytyf__hyi.normalize = normalize
    for glga__dsfd, vqxnb__cfjt in enumerate(date_offset_fields):
        setattr(ytyf__hyi, vqxnb__cfjt, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(lnw__wkgk, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * glga__dsfd)), lir.IntType(64)
            .as_pointer())))
    ytyf__hyi.has_kws = has_kws
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    cbwr__qndpb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ytyf__hyi._getvalue(), is_error=cbwr__qndpb)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    duhtt__fbqk = [n, normalize]
    has_kws = False
    wvjp__phm = [0] * 9 + [-1] * 9
    for glga__dsfd, vqxnb__cfjt in enumerate(date_offset_fields):
        if hasattr(pyval, vqxnb__cfjt):
            ydhp__rnrnx = context.get_constant(types.int64, getattr(pyval,
                vqxnb__cfjt))
            has_kws = True
        else:
            ydhp__rnrnx = context.get_constant(types.int64, wvjp__phm[
                glga__dsfd])
        duhtt__fbqk.append(ydhp__rnrnx)
    has_kws = context.get_constant(types.boolean, has_kws)
    duhtt__fbqk.append(has_kws)
    return lir.Constant.literal_struct(duhtt__fbqk)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    yuyra__ntxq = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for kae__oewl in yuyra__ntxq:
        if not is_overload_none(kae__oewl):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ytyf__hyi = cgutils.create_struct_proxy(typ)(context, builder)
        ytyf__hyi.n = args[0]
        ytyf__hyi.normalize = args[1]
        ytyf__hyi.years = args[2]
        ytyf__hyi.months = args[3]
        ytyf__hyi.weeks = args[4]
        ytyf__hyi.days = args[5]
        ytyf__hyi.hours = args[6]
        ytyf__hyi.minutes = args[7]
        ytyf__hyi.seconds = args[8]
        ytyf__hyi.microseconds = args[9]
        ytyf__hyi.nanoseconds = args[10]
        ytyf__hyi.year = args[11]
        ytyf__hyi.month = args[12]
        ytyf__hyi.day = args[13]
        ytyf__hyi.weekday = args[14]
        ytyf__hyi.hour = args[15]
        ytyf__hyi.minute = args[16]
        ytyf__hyi.second = args[17]
        ytyf__hyi.microsecond = args[18]
        ytyf__hyi.nanosecond = args[19]
        ytyf__hyi.has_kws = args[20]
        return ytyf__hyi._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        rvyi__hppzt = -1 if dateoffset.n < 0 else 1
        for jfceo__ejr in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += rvyi__hppzt * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += rvyi__hppzt * dateoffset._months
            year, month, lwxzu__ysz = calculate_month_end_date(year, month,
                day, 0)
            if day > lwxzu__ysz:
                day = lwxzu__ysz
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            td = pd.Timedelta(days=dateoffset._days + 7 * dateoffset._weeks,
                hours=dateoffset._hours, minutes=dateoffset._minutes,
                seconds=dateoffset._seconds, microseconds=dateoffset.
                _microseconds)
            td = td + pd.Timedelta(dateoffset._nanoseconds, unit='ns')
            if rvyi__hppzt == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                cljnw__uot = ts.weekday()
                weg__los = (dateoffset._weekday - cljnw__uot) % 7
                ts = ts + pd.Timedelta(days=weg__los)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_tz_naive_type,
        datetime_date_type] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs in [date_offset_type,
        month_begin_type, month_end_type, week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xrp__sirnf = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, xrp__sirnf)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        ypf__byl = -1 if weekday is None else weekday
        return init_week(n, normalize, ypf__byl)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        yirss__llx = cgutils.create_struct_proxy(typ)(context, builder)
        yirss__llx.n = args[0]
        yirss__llx.normalize = args[1]
        yirss__llx.weekday = args[2]
        return yirss__llx._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    yirss__llx = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    bzr__bmm = c.pyapi.long_from_longlong(yirss__llx.n)
    kopzy__fzpuv = c.pyapi.from_native_value(types.boolean, yirss__llx.
        normalize, c.env_manager)
    bdac__qja = c.pyapi.long_from_longlong(yirss__llx.weekday)
    rau__ugaj = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    wpgo__jgi = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), yirss__llx.weekday)
    with c.builder.if_else(wpgo__jgi) as (igdp__ovcro, meuix__bmsb):
        with igdp__ovcro:
            udw__hxwj = c.pyapi.call_function_objargs(rau__ugaj, (bzr__bmm,
                kopzy__fzpuv, bdac__qja))
            jidhk__peu = c.builder.block
        with meuix__bmsb:
            zhiz__biv = c.pyapi.call_function_objargs(rau__ugaj, (bzr__bmm,
                kopzy__fzpuv))
            ljf__kdo = c.builder.block
    lkl__eacct = c.builder.phi(udw__hxwj.type)
    lkl__eacct.add_incoming(udw__hxwj, jidhk__peu)
    lkl__eacct.add_incoming(zhiz__biv, ljf__kdo)
    c.pyapi.decref(bdac__qja)
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    c.pyapi.decref(rau__ugaj)
    return lkl__eacct


@unbox(WeekType)
def unbox_week(typ, val, c):
    bzr__bmm = c.pyapi.object_getattr_string(val, 'n')
    kopzy__fzpuv = c.pyapi.object_getattr_string(val, 'normalize')
    bdac__qja = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(bzr__bmm)
    normalize = c.pyapi.to_native_value(types.bool_, kopzy__fzpuv).value
    hkkny__xqy = c.pyapi.make_none()
    zme__scf = c.builder.icmp_unsigned('==', bdac__qja, hkkny__xqy)
    with c.builder.if_else(zme__scf) as (meuix__bmsb, igdp__ovcro):
        with igdp__ovcro:
            udw__hxwj = c.pyapi.long_as_longlong(bdac__qja)
            jidhk__peu = c.builder.block
        with meuix__bmsb:
            zhiz__biv = lir.Constant(lir.IntType(64), -1)
            ljf__kdo = c.builder.block
    lkl__eacct = c.builder.phi(udw__hxwj.type)
    lkl__eacct.add_incoming(udw__hxwj, jidhk__peu)
    lkl__eacct.add_incoming(zhiz__biv, ljf__kdo)
    yirss__llx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yirss__llx.n = n
    yirss__llx.normalize = normalize
    yirss__llx.weekday = lkl__eacct
    c.pyapi.decref(bzr__bmm)
    c.pyapi.decref(kopzy__fzpuv)
    c.pyapi.decref(bdac__qja)
    cbwr__qndpb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yirss__llx._getvalue(), is_error=cbwr__qndpb)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                ylnkl__bzz = rhs.normalize()
            else:
                ylnkl__bzz = rhs
            jhevm__cgly = calculate_week_date(lhs.n, lhs.weekday, ylnkl__bzz)
            return ylnkl__bzz + jhevm__cgly
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                ylnkl__bzz = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                ylnkl__bzz = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            jhevm__cgly = calculate_week_date(lhs.n, lhs.weekday, ylnkl__bzz)
            return ylnkl__bzz + jhevm__cgly
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            jhevm__cgly = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + jhevm__cgly
        return impl
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def calculate_week_date(n, weekday, input_date_or_ts):
    pass


@overload(calculate_week_date)
def overload_calculate_week_date(n, weekday, input_date_or_ts):
    if isinstance(input_date_or_ts, PandasTimestampType
        ) and tz_has_transition_times(input_date_or_ts.tz):

        def impl_tz_aware(n, weekday, input_date_or_ts):
            if weekday == -1:
                td = pd.Timedelta(weeks=n)
            else:
                xifgj__qink = input_date_or_ts.weekday()
                if weekday != xifgj__qink:
                    casz__bwoer = (weekday - xifgj__qink) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=casz__bwoer)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            xifgj__qink = input_date_or_ts.weekday()
            if weekday != xifgj__qink:
                casz__bwoer = (weekday - xifgj__qink) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=casz__bwoer)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        azv__rtq = pytz.timezone(ts.tz)
        hjry__wka = np.array(azv__rtq._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        iea__wag = np.array(azv__rtq._transition_info)[:, 0]
        iea__wag = (pd.Series(iea__wag).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            pkkiw__cctur = ts.value
            zjju__zbblz = pkkiw__cctur + td.value
            tsmw__aoo = np.searchsorted(hjry__wka, pkkiw__cctur, side='right'
                ) - 1
            xhi__nvc = np.searchsorted(hjry__wka, zjju__zbblz, side='right'
                ) - 1
            casz__bwoer = iea__wag[tsmw__aoo] - iea__wag[xhi__nvc]
            return pd.Timedelta(td.value + casz__bwoer)
        return impl_tz_aware
    else:
        return lambda ts, td: td


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for glvi__xxx in date_offset_unsupported_attrs:
        tzm__dgf = 'pandas.tseries.offsets.DateOffset.' + glvi__xxx
        overload_attribute(DateOffsetType, glvi__xxx)(
            create_unsupported_overload(tzm__dgf))
    for glvi__xxx in date_offset_unsupported:
        tzm__dgf = 'pandas.tseries.offsets.DateOffset.' + glvi__xxx
        overload_method(DateOffsetType, glvi__xxx)(create_unsupported_overload
            (tzm__dgf))


def _install_month_begin_unsupported():
    for glvi__xxx in month_begin_unsupported_attrs:
        tzm__dgf = 'pandas.tseries.offsets.MonthBegin.' + glvi__xxx
        overload_attribute(MonthBeginType, glvi__xxx)(
            create_unsupported_overload(tzm__dgf))
    for glvi__xxx in month_begin_unsupported:
        tzm__dgf = 'pandas.tseries.offsets.MonthBegin.' + glvi__xxx
        overload_method(MonthBeginType, glvi__xxx)(create_unsupported_overload
            (tzm__dgf))


def _install_month_end_unsupported():
    for glvi__xxx in date_offset_unsupported_attrs:
        tzm__dgf = 'pandas.tseries.offsets.MonthEnd.' + glvi__xxx
        overload_attribute(MonthEndType, glvi__xxx)(create_unsupported_overload
            (tzm__dgf))
    for glvi__xxx in date_offset_unsupported:
        tzm__dgf = 'pandas.tseries.offsets.MonthEnd.' + glvi__xxx
        overload_method(MonthEndType, glvi__xxx)(create_unsupported_overload
            (tzm__dgf))


def _install_week_unsupported():
    for glvi__xxx in week_unsupported_attrs:
        tzm__dgf = 'pandas.tseries.offsets.Week.' + glvi__xxx
        overload_attribute(WeekType, glvi__xxx)(create_unsupported_overload
            (tzm__dgf))
    for glvi__xxx in week_unsupported:
        tzm__dgf = 'pandas.tseries.offsets.Week.' + glvi__xxx
        overload_method(WeekType, glvi__xxx)(create_unsupported_overload(
            tzm__dgf))


def _install_offsets_unsupported():
    for ydhp__rnrnx in offsets_unsupported:
        tzm__dgf = 'pandas.tseries.offsets.' + ydhp__rnrnx.__name__
        overload(ydhp__rnrnx)(create_unsupported_overload(tzm__dgf))


def _install_frequencies_unsupported():
    for ydhp__rnrnx in frequencies_unsupported:
        tzm__dgf = 'pandas.tseries.frequencies.' + ydhp__rnrnx.__name__
        overload(ydhp__rnrnx)(create_unsupported_overload(tzm__dgf))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
