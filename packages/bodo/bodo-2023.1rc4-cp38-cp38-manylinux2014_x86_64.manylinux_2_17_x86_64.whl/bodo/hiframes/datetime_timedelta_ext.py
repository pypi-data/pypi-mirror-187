"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gbs__fmi = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, gbs__fmi)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    bxyef__lntih = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    blt__bjx = c.pyapi.long_from_longlong(bxyef__lntih.value)
    dphjd__qyusc = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(dphjd__qyusc, (blt__bjx,))
    c.pyapi.decref(blt__bjx)
    c.pyapi.decref(dphjd__qyusc)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    blt__bjx = c.pyapi.object_getattr_string(val, 'value')
    rwni__nluz = c.pyapi.long_as_longlong(blt__bjx)
    bxyef__lntih = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bxyef__lntih.value = rwni__nluz
    c.pyapi.decref(blt__bjx)
    uips__wan = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bxyef__lntih._getvalue(), is_error=uips__wan)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            zktdu__itr = 1000 * microseconds
            return init_pd_timedelta(zktdu__itr)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            zktdu__itr = 1000 * microseconds
            return init_pd_timedelta(zktdu__itr)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    zpgd__mwuuq, vgz__adyi = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * zpgd__mwuuq)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            eotey__ack = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + eotey__ack
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            mrvpc__fgq = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = mrvpc__fgq + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            ejgsf__xorrj = rhs.toordinal()
            qhraq__ddmj = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            hyrk__sgsvk = rhs.microsecond
            fne__mkkm = lhs.value // 1000
            ybofb__lcvo = lhs.nanoseconds
            xcyy__scseu = hyrk__sgsvk + fne__mkkm
            vxpzn__qajo = 1000000 * (ejgsf__xorrj * 86400 + qhraq__ddmj
                ) + xcyy__scseu
            whzp__uxfd = ybofb__lcvo
            return compute_pd_timestamp(vxpzn__qajo, whzp__uxfd)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            garg__mts = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            garg__mts = garg__mts + lhs
            jzccp__kpgvc, pulka__tkgvr = divmod(garg__mts.seconds, 3600)
            cfxy__npqmv, sey__wgyp = divmod(pulka__tkgvr, 60)
            if 0 < garg__mts.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(garg__mts
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    jzccp__kpgvc, cfxy__npqmv, sey__wgyp, garg__mts.
                    microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            garg__mts = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            garg__mts = garg__mts + rhs
            jzccp__kpgvc, pulka__tkgvr = divmod(garg__mts.seconds, 3600)
            cfxy__npqmv, sey__wgyp = divmod(pulka__tkgvr, 60)
            if 0 < garg__mts.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(garg__mts
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    jzccp__kpgvc, cfxy__npqmv, sey__wgyp, garg__mts.
                    microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            hembd__spi = lhs.value - rhs.value
            return pd.Timedelta(hembd__spi)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            zvu__upiuc = lhs
            numba.parfors.parfor.init_prange()
            n = len(zvu__upiuc)
            A = alloc_datetime_timedelta_array(n)
            for byuk__nihbg in numba.parfors.parfor.internal_prange(n):
                A[byuk__nihbg] = zvu__upiuc[byuk__nihbg] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            clswq__clwoc = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, clswq__clwoc)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            sesce__oxb, clswq__clwoc = divmod(lhs.value, rhs.value)
            return sesce__oxb, pd.Timedelta(clswq__clwoc)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gbs__fmi = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, gbs__fmi)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    bxyef__lntih = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pdse__kjd = c.pyapi.long_from_longlong(bxyef__lntih.days)
    gaztq__vnmqk = c.pyapi.long_from_longlong(bxyef__lntih.seconds)
    nvhs__jqym = c.pyapi.long_from_longlong(bxyef__lntih.microseconds)
    dphjd__qyusc = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(dphjd__qyusc, (pdse__kjd,
        gaztq__vnmqk, nvhs__jqym))
    c.pyapi.decref(pdse__kjd)
    c.pyapi.decref(gaztq__vnmqk)
    c.pyapi.decref(nvhs__jqym)
    c.pyapi.decref(dphjd__qyusc)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    pdse__kjd = c.pyapi.object_getattr_string(val, 'days')
    gaztq__vnmqk = c.pyapi.object_getattr_string(val, 'seconds')
    nvhs__jqym = c.pyapi.object_getattr_string(val, 'microseconds')
    legc__fjdm = c.pyapi.long_as_longlong(pdse__kjd)
    mjdu__djlss = c.pyapi.long_as_longlong(gaztq__vnmqk)
    qxk__ajbpq = c.pyapi.long_as_longlong(nvhs__jqym)
    bxyef__lntih = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bxyef__lntih.days = legc__fjdm
    bxyef__lntih.seconds = mjdu__djlss
    bxyef__lntih.microseconds = qxk__ajbpq
    c.pyapi.decref(pdse__kjd)
    c.pyapi.decref(gaztq__vnmqk)
    c.pyapi.decref(nvhs__jqym)
    uips__wan = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bxyef__lntih._getvalue(), is_error=uips__wan)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    sesce__oxb, clswq__clwoc = divmod(a, b)
    clswq__clwoc *= 2
    xlxu__czf = clswq__clwoc > b if b > 0 else clswq__clwoc < b
    if xlxu__czf or clswq__clwoc == b and sesce__oxb % 2 == 1:
        sesce__oxb += 1
    return sesce__oxb


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                gxehp__mus = _cmp(_getstate(lhs), _getstate(rhs))
                return op(gxehp__mus, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            sesce__oxb, clswq__clwoc = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return sesce__oxb, datetime.timedelta(0, 0, clswq__clwoc)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    bpvza__rpj = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != bpvza__rpj
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gbs__fmi = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, gbs__fmi)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    ymv__nasy = types.Array(types.intp, 1, 'C')
    rnj__sbxf = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ymv__nasy, [n])
    nty__cdey = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ymv__nasy, [n])
    butah__iwovh = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ymv__nasy, [n])
    xhzwf__sxjns = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    vqbc__gyulk = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [xhzwf__sxjns])
    aav__vqic = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    wyxf__xuj = cgutils.get_or_insert_function(c.builder.module, aav__vqic,
        name='unbox_datetime_timedelta_array')
    c.builder.call(wyxf__xuj, [val, n, rnj__sbxf.data, nty__cdey.data,
        butah__iwovh.data, vqbc__gyulk.data])
    agy__bbps = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    agy__bbps.days_data = rnj__sbxf._getvalue()
    agy__bbps.seconds_data = nty__cdey._getvalue()
    agy__bbps.microseconds_data = butah__iwovh._getvalue()
    agy__bbps.null_bitmap = vqbc__gyulk._getvalue()
    uips__wan = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(agy__bbps._getvalue(), is_error=uips__wan)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    zvu__upiuc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    rnj__sbxf = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, zvu__upiuc.days_data)
    nty__cdey = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, zvu__upiuc.seconds_data).data
    butah__iwovh = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, zvu__upiuc.microseconds_data).data
    nps__yzecp = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, zvu__upiuc.null_bitmap).data
    n = c.builder.extract_value(rnj__sbxf.shape, 0)
    aav__vqic = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    uzje__htv = cgutils.get_or_insert_function(c.builder.module, aav__vqic,
        name='box_datetime_timedelta_array')
    gef__zfl = c.builder.call(uzje__htv, [n, rnj__sbxf.data, nty__cdey,
        butah__iwovh, nps__yzecp])
    c.context.nrt.decref(c.builder, typ, val)
    return gef__zfl


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        cgv__ikh, djjq__nnd, fkkwl__njvaf, guscc__izz = args
        hav__qhrx = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        hav__qhrx.days_data = cgv__ikh
        hav__qhrx.seconds_data = djjq__nnd
        hav__qhrx.microseconds_data = fkkwl__njvaf
        hav__qhrx.null_bitmap = guscc__izz
        context.nrt.incref(builder, signature.args[0], cgv__ikh)
        context.nrt.incref(builder, signature.args[1], djjq__nnd)
        context.nrt.incref(builder, signature.args[2], fkkwl__njvaf)
        context.nrt.incref(builder, signature.args[3], guscc__izz)
        return hav__qhrx._getvalue()
    tyj__udwab = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return tyj__udwab, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    rnj__sbxf = np.empty(n, np.int64)
    nty__cdey = np.empty(n, np.int64)
    butah__iwovh = np.empty(n, np.int64)
    ostyw__uet = np.empty(n + 7 >> 3, np.uint8)
    for byuk__nihbg, s in enumerate(pyval):
        clh__kxtmu = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ostyw__uet, byuk__nihbg, int(
            not clh__kxtmu))
        if not clh__kxtmu:
            rnj__sbxf[byuk__nihbg] = s.days
            nty__cdey[byuk__nihbg] = s.seconds
            butah__iwovh[byuk__nihbg] = s.microseconds
    dojr__yzzgb = context.get_constant_generic(builder, days_data_type,
        rnj__sbxf)
    eixgu__dtj = context.get_constant_generic(builder, seconds_data_type,
        nty__cdey)
    rusma__odo = context.get_constant_generic(builder,
        microseconds_data_type, butah__iwovh)
    lhoaj__qaqr = context.get_constant_generic(builder, nulls_type, ostyw__uet)
    return lir.Constant.literal_struct([dojr__yzzgb, eixgu__dtj, rusma__odo,
        lhoaj__qaqr])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    rnj__sbxf = np.empty(n, dtype=np.int64)
    nty__cdey = np.empty(n, dtype=np.int64)
    butah__iwovh = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(rnj__sbxf, nty__cdey, butah__iwovh,
        nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            mupn__saa = bodo.utils.conversion.coerce_to_array(ind)
            ibhzj__xlxq = A._null_bitmap
            edg__rsrcn = A._days_data[mupn__saa]
            vgkmt__cicwt = A._seconds_data[mupn__saa]
            fvg__htk = A._microseconds_data[mupn__saa]
            n = len(edg__rsrcn)
            huqqt__fngrz = get_new_null_mask_bool_index(ibhzj__xlxq, ind, n)
            return init_datetime_timedelta_array(edg__rsrcn, vgkmt__cicwt,
                fvg__htk, huqqt__fngrz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            mupn__saa = bodo.utils.conversion.coerce_to_array(ind)
            ibhzj__xlxq = A._null_bitmap
            edg__rsrcn = A._days_data[mupn__saa]
            vgkmt__cicwt = A._seconds_data[mupn__saa]
            fvg__htk = A._microseconds_data[mupn__saa]
            n = len(edg__rsrcn)
            huqqt__fngrz = get_new_null_mask_int_index(ibhzj__xlxq,
                mupn__saa, n)
            return init_datetime_timedelta_array(edg__rsrcn, vgkmt__cicwt,
                fvg__htk, huqqt__fngrz)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            ibhzj__xlxq = A._null_bitmap
            edg__rsrcn = np.ascontiguousarray(A._days_data[ind])
            vgkmt__cicwt = np.ascontiguousarray(A._seconds_data[ind])
            fvg__htk = np.ascontiguousarray(A._microseconds_data[ind])
            huqqt__fngrz = get_new_null_mask_slice_index(ibhzj__xlxq, ind, n)
            return init_datetime_timedelta_array(edg__rsrcn, vgkmt__cicwt,
                fvg__htk, huqqt__fngrz)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    lcf__ejdd = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(lcf__ejdd)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(lcf__ejdd)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for byuk__nihbg in range(n):
                    A._days_data[ind[byuk__nihbg]] = val._days
                    A._seconds_data[ind[byuk__nihbg]] = val._seconds
                    A._microseconds_data[ind[byuk__nihbg]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[byuk__nihbg], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for byuk__nihbg in range(n):
                    A._days_data[ind[byuk__nihbg]] = val._days_data[byuk__nihbg
                        ]
                    A._seconds_data[ind[byuk__nihbg]] = val._seconds_data[
                        byuk__nihbg]
                    A._microseconds_data[ind[byuk__nihbg]
                        ] = val._microseconds_data[byuk__nihbg]
                    ish__pyww = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, byuk__nihbg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[byuk__nihbg], ish__pyww)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for byuk__nihbg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, byuk__nihbg
                        ) and ind[byuk__nihbg]:
                        A._days_data[byuk__nihbg] = val._days
                        A._seconds_data[byuk__nihbg] = val._seconds
                        A._microseconds_data[byuk__nihbg] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            byuk__nihbg, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                vqs__exx = 0
                for byuk__nihbg in range(n):
                    if not bodo.libs.array_kernels.isna(ind, byuk__nihbg
                        ) and ind[byuk__nihbg]:
                        A._days_data[byuk__nihbg] = val._days_data[vqs__exx]
                        A._seconds_data[byuk__nihbg] = val._seconds_data[
                            vqs__exx]
                        A._microseconds_data[byuk__nihbg
                            ] = val._microseconds_data[vqs__exx]
                        ish__pyww = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, vqs__exx)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            byuk__nihbg, ish__pyww)
                        vqs__exx += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                phd__ztxo = numba.cpython.unicode._normalize_slice(ind, len(A))
                for byuk__nihbg in range(phd__ztxo.start, phd__ztxo.stop,
                    phd__ztxo.step):
                    A._days_data[byuk__nihbg] = val._days
                    A._seconds_data[byuk__nihbg] = val._seconds
                    A._microseconds_data[byuk__nihbg] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        byuk__nihbg, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                ensuj__pkxw = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, ensuj__pkxw,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            zvu__upiuc = arg1
            numba.parfors.parfor.init_prange()
            n = len(zvu__upiuc)
            A = alloc_datetime_timedelta_array(n)
            for byuk__nihbg in numba.parfors.parfor.internal_prange(n):
                A[byuk__nihbg] = zvu__upiuc[byuk__nihbg] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            ahz__exy = True
        else:
            ahz__exy = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                rvgq__qyp = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for byuk__nihbg in numba.parfors.parfor.internal_prange(n):
                    echg__blxa = bodo.libs.array_kernels.isna(lhs, byuk__nihbg)
                    ucmr__xiq = bodo.libs.array_kernels.isna(rhs, byuk__nihbg)
                    if echg__blxa or ucmr__xiq:
                        rtqnm__wuhpw = ahz__exy
                    else:
                        rtqnm__wuhpw = op(lhs[byuk__nihbg], rhs[byuk__nihbg])
                    rvgq__qyp[byuk__nihbg] = rtqnm__wuhpw
                return rvgq__qyp
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                rvgq__qyp = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for byuk__nihbg in numba.parfors.parfor.internal_prange(n):
                    ish__pyww = bodo.libs.array_kernels.isna(lhs, byuk__nihbg)
                    if ish__pyww:
                        rtqnm__wuhpw = ahz__exy
                    else:
                        rtqnm__wuhpw = op(lhs[byuk__nihbg], rhs)
                    rvgq__qyp[byuk__nihbg] = rtqnm__wuhpw
                return rvgq__qyp
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                rvgq__qyp = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for byuk__nihbg in numba.parfors.parfor.internal_prange(n):
                    ish__pyww = bodo.libs.array_kernels.isna(rhs, byuk__nihbg)
                    if ish__pyww:
                        rtqnm__wuhpw = ahz__exy
                    else:
                        rtqnm__wuhpw = op(lhs, rhs[byuk__nihbg])
                    rvgq__qyp[byuk__nihbg] = rtqnm__wuhpw
                return rvgq__qyp
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for cjwm__msax in timedelta_unsupported_attrs:
        qydq__oxuay = 'pandas.Timedelta.' + cjwm__msax
        overload_attribute(PDTimeDeltaType, cjwm__msax)(
            create_unsupported_overload(qydq__oxuay))
    for oavs__tudv in timedelta_unsupported_methods:
        qydq__oxuay = 'pandas.Timedelta.' + oavs__tudv
        overload_method(PDTimeDeltaType, oavs__tudv)(
            create_unsupported_overload(qydq__oxuay + '()'))


_intstall_pd_timedelta_unsupported()
