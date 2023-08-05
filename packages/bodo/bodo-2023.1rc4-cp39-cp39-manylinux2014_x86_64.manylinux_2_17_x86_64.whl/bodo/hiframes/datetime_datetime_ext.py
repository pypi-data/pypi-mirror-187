import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ytqjr__rytlz = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, ytqjr__rytlz)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    pvwv__eqi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    cxam__frsai = c.pyapi.long_from_longlong(pvwv__eqi.year)
    zaci__wbjbk = c.pyapi.long_from_longlong(pvwv__eqi.month)
    ela__qshkn = c.pyapi.long_from_longlong(pvwv__eqi.day)
    qfwc__rwy = c.pyapi.long_from_longlong(pvwv__eqi.hour)
    hkhy__bvk = c.pyapi.long_from_longlong(pvwv__eqi.minute)
    lyy__xagcl = c.pyapi.long_from_longlong(pvwv__eqi.second)
    ave__yco = c.pyapi.long_from_longlong(pvwv__eqi.microsecond)
    ljvf__ebr = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    jki__jti = c.pyapi.call_function_objargs(ljvf__ebr, (cxam__frsai,
        zaci__wbjbk, ela__qshkn, qfwc__rwy, hkhy__bvk, lyy__xagcl, ave__yco))
    c.pyapi.decref(cxam__frsai)
    c.pyapi.decref(zaci__wbjbk)
    c.pyapi.decref(ela__qshkn)
    c.pyapi.decref(qfwc__rwy)
    c.pyapi.decref(hkhy__bvk)
    c.pyapi.decref(lyy__xagcl)
    c.pyapi.decref(ave__yco)
    c.pyapi.decref(ljvf__ebr)
    return jki__jti


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    cxam__frsai = c.pyapi.object_getattr_string(val, 'year')
    zaci__wbjbk = c.pyapi.object_getattr_string(val, 'month')
    ela__qshkn = c.pyapi.object_getattr_string(val, 'day')
    qfwc__rwy = c.pyapi.object_getattr_string(val, 'hour')
    hkhy__bvk = c.pyapi.object_getattr_string(val, 'minute')
    lyy__xagcl = c.pyapi.object_getattr_string(val, 'second')
    ave__yco = c.pyapi.object_getattr_string(val, 'microsecond')
    pvwv__eqi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pvwv__eqi.year = c.pyapi.long_as_longlong(cxam__frsai)
    pvwv__eqi.month = c.pyapi.long_as_longlong(zaci__wbjbk)
    pvwv__eqi.day = c.pyapi.long_as_longlong(ela__qshkn)
    pvwv__eqi.hour = c.pyapi.long_as_longlong(qfwc__rwy)
    pvwv__eqi.minute = c.pyapi.long_as_longlong(hkhy__bvk)
    pvwv__eqi.second = c.pyapi.long_as_longlong(lyy__xagcl)
    pvwv__eqi.microsecond = c.pyapi.long_as_longlong(ave__yco)
    c.pyapi.decref(cxam__frsai)
    c.pyapi.decref(zaci__wbjbk)
    c.pyapi.decref(ela__qshkn)
    c.pyapi.decref(qfwc__rwy)
    c.pyapi.decref(hkhy__bvk)
    c.pyapi.decref(lyy__xagcl)
    c.pyapi.decref(ave__yco)
    cnt__perj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pvwv__eqi._getvalue(), is_error=cnt__perj)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        pvwv__eqi = cgutils.create_struct_proxy(typ)(context, builder)
        pvwv__eqi.year = args[0]
        pvwv__eqi.month = args[1]
        pvwv__eqi.day = args[2]
        pvwv__eqi.hour = args[3]
        pvwv__eqi.minute = args[4]
        pvwv__eqi.second = args[5]
        pvwv__eqi.microsecond = args[6]
        return pvwv__eqi._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, nde__rfi = lhs.year, rhs.year
                drdx__ctrai, bntax__mnh = lhs.month, rhs.month
                d, qbu__terrl = lhs.day, rhs.day
                qrz__sbw, eeyxd__ggw = lhs.hour, rhs.hour
                jze__gdk, iii__deqw = lhs.minute, rhs.minute
                rhl__tcxz, uck__etjhp = lhs.second, rhs.second
                sprp__vsd, ohxgh__tzeg = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, drdx__ctrai, d, qrz__sbw, jze__gdk,
                    rhl__tcxz, sprp__vsd), (nde__rfi, bntax__mnh,
                    qbu__terrl, eeyxd__ggw, iii__deqw, uck__etjhp,
                    ohxgh__tzeg)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            qlrjj__obx = lhs.toordinal()
            gszdp__omi = rhs.toordinal()
            vjeac__zvrz = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            hfowv__sbs = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            mtre__kvq = datetime.timedelta(qlrjj__obx - gszdp__omi, 
                vjeac__zvrz - hfowv__sbs, lhs.microsecond - rhs.microsecond)
            return mtre__kvq
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    hftgf__gqwwm = context.make_helper(builder, fromty, value=val)
    dboqy__oqlic = cgutils.as_bool_bit(builder, hftgf__gqwwm.valid)
    with builder.if_else(dboqy__oqlic) as (ijhns__ynpo, eyktj__tcb):
        with ijhns__ynpo:
            nhfq__jsile = context.cast(builder, hftgf__gqwwm.data, fromty.
                type, toty)
            mtu__cavj = builder.block
        with eyktj__tcb:
            zisz__wzty = numba.np.npdatetime.NAT
            egeln__rymz = builder.block
    jki__jti = builder.phi(nhfq__jsile.type)
    jki__jti.add_incoming(nhfq__jsile, mtu__cavj)
    jki__jti.add_incoming(zisz__wzty, egeln__rymz)
    return jki__jti
