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
        gmzsm__iyq = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, gmzsm__iyq)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    bpg__etzcr = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jkwv__fpok = c.pyapi.long_from_longlong(bpg__etzcr.value)
    gsh__svtu = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(gsh__svtu, (jkwv__fpok,))
    c.pyapi.decref(jkwv__fpok)
    c.pyapi.decref(gsh__svtu)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    jkwv__fpok = c.pyapi.object_getattr_string(val, 'value')
    wsh__dqjn = c.pyapi.long_as_longlong(jkwv__fpok)
    bpg__etzcr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bpg__etzcr.value = wsh__dqjn
    c.pyapi.decref(jkwv__fpok)
    sdeg__rdisl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bpg__etzcr._getvalue(), is_error=sdeg__rdisl)


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
            kilmh__vwcja = 1000 * microseconds
            return init_pd_timedelta(kilmh__vwcja)
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
            kilmh__vwcja = 1000 * microseconds
            return init_pd_timedelta(kilmh__vwcja)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    wqo__lqx, kgnf__faek = pd._libs.tslibs.conversion.precision_from_unit(unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * wqo__lqx)
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
            kkbrz__cbl = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + kkbrz__cbl
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ncz__hli = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = ncz__hli + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            hooc__otjb = rhs.toordinal()
            lvj__clmqs = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            rrce__lyhcx = rhs.microsecond
            fnmj__vnbb = lhs.value // 1000
            fjsqu__tvf = lhs.nanoseconds
            slnsd__edxzf = rrce__lyhcx + fnmj__vnbb
            ndqs__vdx = 1000000 * (hooc__otjb * 86400 + lvj__clmqs
                ) + slnsd__edxzf
            lon__lhlmm = fjsqu__tvf
            return compute_pd_timestamp(ndqs__vdx, lon__lhlmm)
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
            sppz__loer = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            sppz__loer = sppz__loer + lhs
            ajip__vzjr, krp__ysv = divmod(sppz__loer.seconds, 3600)
            mluau__jzjcz, kraqz__cniti = divmod(krp__ysv, 60)
            if 0 < sppz__loer.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(sppz__loer
                    .days)
                return datetime.datetime(d.year, d.month, d.day, ajip__vzjr,
                    mluau__jzjcz, kraqz__cniti, sppz__loer.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            sppz__loer = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            sppz__loer = sppz__loer + rhs
            ajip__vzjr, krp__ysv = divmod(sppz__loer.seconds, 3600)
            mluau__jzjcz, kraqz__cniti = divmod(krp__ysv, 60)
            if 0 < sppz__loer.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(sppz__loer
                    .days)
                return datetime.datetime(d.year, d.month, d.day, ajip__vzjr,
                    mluau__jzjcz, kraqz__cniti, sppz__loer.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            fitdg__ookvs = lhs.value - rhs.value
            return pd.Timedelta(fitdg__ookvs)
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
            gmfl__ranq = lhs
            numba.parfors.parfor.init_prange()
            n = len(gmfl__ranq)
            A = alloc_datetime_timedelta_array(n)
            for zge__mnjwf in numba.parfors.parfor.internal_prange(n):
                A[zge__mnjwf] = gmfl__ranq[zge__mnjwf] - rhs
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
            faren__hzb = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, faren__hzb)
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
            ahqmp__inacm, faren__hzb = divmod(lhs.value, rhs.value)
            return ahqmp__inacm, pd.Timedelta(faren__hzb)
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
        gmzsm__iyq = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, gmzsm__iyq)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    bpg__etzcr = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    yak__tmd = c.pyapi.long_from_longlong(bpg__etzcr.days)
    snj__ntx = c.pyapi.long_from_longlong(bpg__etzcr.seconds)
    gibl__wtfcd = c.pyapi.long_from_longlong(bpg__etzcr.microseconds)
    gsh__svtu = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(gsh__svtu, (yak__tmd, snj__ntx,
        gibl__wtfcd))
    c.pyapi.decref(yak__tmd)
    c.pyapi.decref(snj__ntx)
    c.pyapi.decref(gibl__wtfcd)
    c.pyapi.decref(gsh__svtu)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    yak__tmd = c.pyapi.object_getattr_string(val, 'days')
    snj__ntx = c.pyapi.object_getattr_string(val, 'seconds')
    gibl__wtfcd = c.pyapi.object_getattr_string(val, 'microseconds')
    vtug__jlbc = c.pyapi.long_as_longlong(yak__tmd)
    ptjx__qjrh = c.pyapi.long_as_longlong(snj__ntx)
    care__trlr = c.pyapi.long_as_longlong(gibl__wtfcd)
    bpg__etzcr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bpg__etzcr.days = vtug__jlbc
    bpg__etzcr.seconds = ptjx__qjrh
    bpg__etzcr.microseconds = care__trlr
    c.pyapi.decref(yak__tmd)
    c.pyapi.decref(snj__ntx)
    c.pyapi.decref(gibl__wtfcd)
    sdeg__rdisl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bpg__etzcr._getvalue(), is_error=sdeg__rdisl)


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
    ahqmp__inacm, faren__hzb = divmod(a, b)
    faren__hzb *= 2
    wkuvy__trw = faren__hzb > b if b > 0 else faren__hzb < b
    if wkuvy__trw or faren__hzb == b and ahqmp__inacm % 2 == 1:
        ahqmp__inacm += 1
    return ahqmp__inacm


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
                stn__fwey = _cmp(_getstate(lhs), _getstate(rhs))
                return op(stn__fwey, 0)
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
            ahqmp__inacm, faren__hzb = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return ahqmp__inacm, datetime.timedelta(0, 0, faren__hzb)
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
    qjfh__jujkd = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != qjfh__jujkd
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
        gmzsm__iyq = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, gmzsm__iyq)


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
    iexj__kvn = types.Array(types.intp, 1, 'C')
    stqm__rrvj = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        iexj__kvn, [n])
    clal__wtf = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        iexj__kvn, [n])
    wge__oru = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        iexj__kvn, [n])
    xrxb__zsgoo = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    qvor__wxiz = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [xrxb__zsgoo])
    nnul__txfs = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    div__llutt = cgutils.get_or_insert_function(c.builder.module,
        nnul__txfs, name='unbox_datetime_timedelta_array')
    c.builder.call(div__llutt, [val, n, stqm__rrvj.data, clal__wtf.data,
        wge__oru.data, qvor__wxiz.data])
    yvgfn__qnr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yvgfn__qnr.days_data = stqm__rrvj._getvalue()
    yvgfn__qnr.seconds_data = clal__wtf._getvalue()
    yvgfn__qnr.microseconds_data = wge__oru._getvalue()
    yvgfn__qnr.null_bitmap = qvor__wxiz._getvalue()
    sdeg__rdisl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yvgfn__qnr._getvalue(), is_error=sdeg__rdisl)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    gmfl__ranq = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    stqm__rrvj = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, gmfl__ranq.days_data)
    clal__wtf = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, gmfl__ranq.seconds_data).data
    wge__oru = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, gmfl__ranq.microseconds_data).data
    rqv__qwfgj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, gmfl__ranq.null_bitmap).data
    n = c.builder.extract_value(stqm__rrvj.shape, 0)
    nnul__txfs = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    mowb__qjk = cgutils.get_or_insert_function(c.builder.module, nnul__txfs,
        name='box_datetime_timedelta_array')
    yuvxl__mukgj = c.builder.call(mowb__qjk, [n, stqm__rrvj.data, clal__wtf,
        wge__oru, rqv__qwfgj])
    c.context.nrt.decref(c.builder, typ, val)
    return yuvxl__mukgj


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        isguo__qkz, iwnta__jebd, miq__hjie, exp__pefo = args
        aga__kdoe = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        aga__kdoe.days_data = isguo__qkz
        aga__kdoe.seconds_data = iwnta__jebd
        aga__kdoe.microseconds_data = miq__hjie
        aga__kdoe.null_bitmap = exp__pefo
        context.nrt.incref(builder, signature.args[0], isguo__qkz)
        context.nrt.incref(builder, signature.args[1], iwnta__jebd)
        context.nrt.incref(builder, signature.args[2], miq__hjie)
        context.nrt.incref(builder, signature.args[3], exp__pefo)
        return aga__kdoe._getvalue()
    eemoy__vmw = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return eemoy__vmw, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    stqm__rrvj = np.empty(n, np.int64)
    clal__wtf = np.empty(n, np.int64)
    wge__oru = np.empty(n, np.int64)
    jxqe__bisjs = np.empty(n + 7 >> 3, np.uint8)
    for zge__mnjwf, s in enumerate(pyval):
        jonz__pmb = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(jxqe__bisjs, zge__mnjwf, int(
            not jonz__pmb))
        if not jonz__pmb:
            stqm__rrvj[zge__mnjwf] = s.days
            clal__wtf[zge__mnjwf] = s.seconds
            wge__oru[zge__mnjwf] = s.microseconds
    wdq__gzhzu = context.get_constant_generic(builder, days_data_type,
        stqm__rrvj)
    wpf__fjd = context.get_constant_generic(builder, seconds_data_type,
        clal__wtf)
    ycgo__dmqb = context.get_constant_generic(builder,
        microseconds_data_type, wge__oru)
    bzd__krok = context.get_constant_generic(builder, nulls_type, jxqe__bisjs)
    return lir.Constant.literal_struct([wdq__gzhzu, wpf__fjd, ycgo__dmqb,
        bzd__krok])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    stqm__rrvj = np.empty(n, dtype=np.int64)
    clal__wtf = np.empty(n, dtype=np.int64)
    wge__oru = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(stqm__rrvj, clal__wtf, wge__oru, nulls
        )


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
            lfizy__hsslb = bodo.utils.conversion.coerce_to_array(ind)
            zqwfk__jsmb = A._null_bitmap
            rkc__xgly = A._days_data[lfizy__hsslb]
            aoqs__yris = A._seconds_data[lfizy__hsslb]
            bytc__vqr = A._microseconds_data[lfizy__hsslb]
            n = len(rkc__xgly)
            ngvf__hsj = get_new_null_mask_bool_index(zqwfk__jsmb, ind, n)
            return init_datetime_timedelta_array(rkc__xgly, aoqs__yris,
                bytc__vqr, ngvf__hsj)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            lfizy__hsslb = bodo.utils.conversion.coerce_to_array(ind)
            zqwfk__jsmb = A._null_bitmap
            rkc__xgly = A._days_data[lfizy__hsslb]
            aoqs__yris = A._seconds_data[lfizy__hsslb]
            bytc__vqr = A._microseconds_data[lfizy__hsslb]
            n = len(rkc__xgly)
            ngvf__hsj = get_new_null_mask_int_index(zqwfk__jsmb,
                lfizy__hsslb, n)
            return init_datetime_timedelta_array(rkc__xgly, aoqs__yris,
                bytc__vqr, ngvf__hsj)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            zqwfk__jsmb = A._null_bitmap
            rkc__xgly = np.ascontiguousarray(A._days_data[ind])
            aoqs__yris = np.ascontiguousarray(A._seconds_data[ind])
            bytc__vqr = np.ascontiguousarray(A._microseconds_data[ind])
            ngvf__hsj = get_new_null_mask_slice_index(zqwfk__jsmb, ind, n)
            return init_datetime_timedelta_array(rkc__xgly, aoqs__yris,
                bytc__vqr, ngvf__hsj)
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
    xqb__lggcg = (
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
            raise BodoError(xqb__lggcg)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(xqb__lggcg)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for zge__mnjwf in range(n):
                    A._days_data[ind[zge__mnjwf]] = val._days
                    A._seconds_data[ind[zge__mnjwf]] = val._seconds
                    A._microseconds_data[ind[zge__mnjwf]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[zge__mnjwf], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for zge__mnjwf in range(n):
                    A._days_data[ind[zge__mnjwf]] = val._days_data[zge__mnjwf]
                    A._seconds_data[ind[zge__mnjwf]] = val._seconds_data[
                        zge__mnjwf]
                    A._microseconds_data[ind[zge__mnjwf]
                        ] = val._microseconds_data[zge__mnjwf]
                    oltcw__puok = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, zge__mnjwf)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[zge__mnjwf], oltcw__puok)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for zge__mnjwf in range(n):
                    if not bodo.libs.array_kernels.isna(ind, zge__mnjwf
                        ) and ind[zge__mnjwf]:
                        A._days_data[zge__mnjwf] = val._days
                        A._seconds_data[zge__mnjwf] = val._seconds
                        A._microseconds_data[zge__mnjwf] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            zge__mnjwf, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                veuo__muyy = 0
                for zge__mnjwf in range(n):
                    if not bodo.libs.array_kernels.isna(ind, zge__mnjwf
                        ) and ind[zge__mnjwf]:
                        A._days_data[zge__mnjwf] = val._days_data[veuo__muyy]
                        A._seconds_data[zge__mnjwf] = val._seconds_data[
                            veuo__muyy]
                        A._microseconds_data[zge__mnjwf
                            ] = val._microseconds_data[veuo__muyy]
                        oltcw__puok = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, veuo__muyy)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            zge__mnjwf, oltcw__puok)
                        veuo__muyy += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                mxwux__kcmc = numba.cpython.unicode._normalize_slice(ind,
                    len(A))
                for zge__mnjwf in range(mxwux__kcmc.start, mxwux__kcmc.stop,
                    mxwux__kcmc.step):
                    A._days_data[zge__mnjwf] = val._days
                    A._seconds_data[zge__mnjwf] = val._seconds
                    A._microseconds_data[zge__mnjwf] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        zge__mnjwf, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                gel__dbvr = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, gel__dbvr, ind, n
                    )
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
            gmfl__ranq = arg1
            numba.parfors.parfor.init_prange()
            n = len(gmfl__ranq)
            A = alloc_datetime_timedelta_array(n)
            for zge__mnjwf in numba.parfors.parfor.internal_prange(n):
                A[zge__mnjwf] = gmfl__ranq[zge__mnjwf] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            lgy__tzos = True
        else:
            lgy__tzos = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                zahj__rtje = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for zge__mnjwf in numba.parfors.parfor.internal_prange(n):
                    ryyem__vmw = bodo.libs.array_kernels.isna(lhs, zge__mnjwf)
                    cmn__zmxs = bodo.libs.array_kernels.isna(rhs, zge__mnjwf)
                    if ryyem__vmw or cmn__zmxs:
                        uuzk__ydgzq = lgy__tzos
                    else:
                        uuzk__ydgzq = op(lhs[zge__mnjwf], rhs[zge__mnjwf])
                    zahj__rtje[zge__mnjwf] = uuzk__ydgzq
                return zahj__rtje
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                zahj__rtje = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for zge__mnjwf in numba.parfors.parfor.internal_prange(n):
                    oltcw__puok = bodo.libs.array_kernels.isna(lhs, zge__mnjwf)
                    if oltcw__puok:
                        uuzk__ydgzq = lgy__tzos
                    else:
                        uuzk__ydgzq = op(lhs[zge__mnjwf], rhs)
                    zahj__rtje[zge__mnjwf] = uuzk__ydgzq
                return zahj__rtje
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                zahj__rtje = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for zge__mnjwf in numba.parfors.parfor.internal_prange(n):
                    oltcw__puok = bodo.libs.array_kernels.isna(rhs, zge__mnjwf)
                    if oltcw__puok:
                        uuzk__ydgzq = lgy__tzos
                    else:
                        uuzk__ydgzq = op(lhs, rhs[zge__mnjwf])
                    zahj__rtje[zge__mnjwf] = uuzk__ydgzq
                return zahj__rtje
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for mgk__eld in timedelta_unsupported_attrs:
        eikv__bgv = 'pandas.Timedelta.' + mgk__eld
        overload_attribute(PDTimeDeltaType, mgk__eld)(
            create_unsupported_overload(eikv__bgv))
    for xsbmu__cuj in timedelta_unsupported_methods:
        eikv__bgv = 'pandas.Timedelta.' + xsbmu__cuj
        overload_method(PDTimeDeltaType, xsbmu__cuj)(
            create_unsupported_overload(eikv__bgv + '()'))


_intstall_pd_timedelta_unsupported()
