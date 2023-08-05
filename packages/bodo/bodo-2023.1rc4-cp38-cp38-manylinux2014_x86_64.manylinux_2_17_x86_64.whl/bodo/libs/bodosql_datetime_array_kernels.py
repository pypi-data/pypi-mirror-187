"""
Implements datetime array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
import pandas as pd
import pytz
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


def standardize_snowflake_date_time_part(part_str):
    pass


@overload(standardize_snowflake_date_time_part)
def overload_standardize_snowflake_date_time_part(part_str):
    zznfq__tfpo = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    zgr__qthmn = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    akce__qjpb = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    erub__pdhe = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    bmitj__ffm = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    gpan__lrymh = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    oyxge__zoj = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    bdipj__ydib = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    kow__qywwa = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    oldr__gvla = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    pfpmq__nteg = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    nlly__tnmk = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    zcwe__txf = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec', 'nsecond',
        'nanoseconds', 'nanosecs', 'nseconds'])
    sjh__jsk = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    uzc__svnc = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    zgvsq__gaq = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    ufiy__tmqsc = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    pmxy__ikytv = pd.array(['timezone_hour', 'tzh'])
    dcezm__rlnha = pd.array(['timezone_minute', 'tzm'])
    qgon__vgv = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in zznfq__tfpo:
            return 'year'
        elif part_str in zgr__qthmn:
            return 'month'
        elif part_str in akce__qjpb:
            return 'day'
        elif part_str in erub__pdhe:
            return 'dayofweek'
        elif part_str in bmitj__ffm:
            return 'week'
        elif part_str in gpan__lrymh:
            return 'weekiso'
        elif part_str in oyxge__zoj:
            return 'quarter'
        elif part_str in bdipj__ydib:
            return 'hour'
        elif part_str in kow__qywwa:
            return 'minute'
        elif part_str in oldr__gvla:
            return 'second'
        elif part_str in pfpmq__nteg:
            return 'millisecond'
        elif part_str in nlly__tnmk:
            return 'microsecond'
        elif part_str in zcwe__txf:
            return 'nanosecond'
        elif part_str in sjh__jsk:
            return 'epoch_second'
        elif part_str in uzc__svnc:
            return 'epoch_millisecond'
        elif part_str in zgvsq__gaq:
            return 'epoch_microsecond'
        elif part_str in ufiy__tmqsc:
            return 'epoch_nanosecond'
        elif part_str in pmxy__ikytv:
            return 'timezone_hour'
        elif part_str in dcezm__rlnha:
            return 'timezone_minute'
        elif part_str in qgon__vgv:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for eevll__vkpg in range(len(args)):
        if isinstance(args[eevll__vkpg], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], eevll__vkpg)

    def impl(start_dt, interval):
        return add_interval_util(start_dt, interval)
    return impl


def add_interval_years(amount, start_dt):
    return


def add_interval_quarters(amount, start_dt):
    return


def add_interval_months(amount, start_dt):
    return


def add_interval_weeks(amount, start_dt):
    return


def add_interval_days(amount, start_dt):
    return


def add_interval_hours(amount, start_dt):
    return


def add_interval_minutes(amount, start_dt):
    return


def add_interval_seconds(amount, start_dt):
    return


def add_interval_milliseconds(amount, start_dt):
    return


def add_interval_microseconds(amount, start_dt):
    return


def add_interval_nanoseconds(amount, start_dt):
    return


@numba.generated_jit(nopython=True)
def dayname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.dayname_util',
            ['arr'], 0)

    def impl(arr):
        return dayname_util(arr)
    return impl


def dayofmonth(arr):
    return


def dayofweek(arr):
    return


def dayofweekiso(arr):
    return


def dayofyear(arr):
    return


def diff_day(arr0, arr1):
    return


def diff_hour(arr0, arr1):
    return


def diff_microsecond(arr0, arr1):
    return


def diff_minute(arr0, arr1):
    return


def diff_month(arr0, arr1):
    return


def diff_nanosecond(arr0, arr1):
    return


def diff_quarter(arr0, arr1):
    return


def diff_second(arr0, arr1):
    return


def diff_week(arr0, arr1):
    return


def diff_year(arr0, arr1):
    return


def get_year(arr):
    return


def get_quarter(arr):
    return


def get_month(arr):
    return


def get_week(arr):
    return


def get_hour(arr):
    return


def get_minute(arr):
    return


def get_second(arr):
    return


def get_millisecond(arr):
    return


def get_microsecond(arr):
    return


def get_nanosecond(arr):
    return


@numba.generated_jit(nopython=True)
def int_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.int_to_days_util', ['arr'], 0)

    def impl(arr):
        return int_to_days_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def last_day(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.last_day_util',
            ['arr'], 0)

    def impl(arr):
        return last_day_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def makedate(year, day):
    args = [year, day]
    for eevll__vkpg in range(2):
        if isinstance(args[eevll__vkpg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], eevll__vkpg)

    def impl(year, day):
        return makedate_util(year, day)
    return impl


@numba.generated_jit(nopython=True)
def monthname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.monthname_util',
            ['arr'], 0)

    def impl(arr):
        return monthname_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def next_day(arr0, arr1):
    args = [arr0, arr1]
    for eevll__vkpg in range(2):
        if isinstance(args[eevll__vkpg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], eevll__vkpg)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for eevll__vkpg in range(2):
        if isinstance(args[eevll__vkpg], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], eevll__vkpg)

    def impl(arr0, arr1):
        return previous_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def second_timestamp(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.second_timestamp_util', ['arr'], 0
            )

    def impl(arr):
        return second_timestamp_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def weekday(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.weekday_util',
            ['arr'], 0)

    def impl(arr):
        return weekday_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def yearofweekiso(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.yearofweekiso_util', ['arr'], 0)

    def impl(arr):
        return yearofweekiso_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def add_interval_util(start_dt, interval):
    verify_datetime_arg_allow_tz(start_dt, 'add_interval', 'start_dt')
    yaorz__gmbp = get_tz_if_exists(start_dt)
    trlj__zsfq = ['start_dt', 'interval']
    fbhc__fonfv = [start_dt, interval]
    yetrg__qljgk = [True] * 2
    lib__oyt = ''
    vbdf__ovzb = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    orp__pif = None
    if yaorz__gmbp is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(yaorz__gmbp):
            buwcb__ntdg = pytz.timezone(yaorz__gmbp)
            omlvg__zjv = np.array(buwcb__ntdg._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            srn__ipo = np.array(buwcb__ntdg._transition_info)[:, 0]
            srn__ipo = (pd.Series(srn__ipo).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            orp__pif = {'trans': omlvg__zjv, 'deltas': srn__ipo}
            lib__oyt += f'start_value = arg0.value\n'
            lib__oyt += 'end_value = start_value + arg0.value\n'
            lib__oyt += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            lib__oyt += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            lib__oyt += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            lib__oyt += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        lib__oyt += f'res[i] = arg0 + arg1\n'
        bggf__nbtze = bodo.DatetimeArrayType(yaorz__gmbp)
    else:
        jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            vbdf__ovzb else '')
        vdbj__nvq = 'bodo.utils.conversion.box_if_dt64' if vbdf__ovzb else ''
        lib__oyt = f'res[i] = {jib__mywkx}({vdbj__nvq}(arg0) + arg1)\n'
        bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, extra_globals=orp__pif)


def add_interval_years_util(amount, start_dt):
    return


def add_interval_quarters_util(amount, start_dt):
    return


def add_interval_months_util(amount, start_dt):
    return


def add_interval_weeks_util(amount, start_dt):
    return


def add_interval_days_util(amount, start_dt):
    return


def add_interval_hours_util(amount, start_dt):
    return


def add_interval_minutes_util(amount, start_dt):
    return


def add_interval_seconds_util(amount, start_dt):
    return


def add_interval_milliseconds_util(amount, start_dt):
    return


def add_interval_microseconds_util(amount, start_dt):
    return


def add_interval_nanoseconds_util(amount, start_dt):
    return


def create_add_interval_func_overload(unit):

    def overload_func(amount, start_dt):
        args = [amount, start_dt]
        for eevll__vkpg in range(2):
            if isinstance(args[eevll__vkpg], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], eevll__vkpg)
        qbxhy__lzhw = 'def impl(amount, start_dt):\n'
        qbxhy__lzhw += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        fcj__jmxe = {}
        exec(qbxhy__lzhw, {'bodo': bodo}, fcj__jmxe)
        return fcj__jmxe['impl']
    return overload_func


def create_add_interval_util_overload(unit):

    def overload_add_datetime_interval_util(amount, start_dt):
        verify_int_arg(amount, 'add_interval_' + unit, 'amount')
        if unit in ('hours', 'minutes', 'seconds', 'milliseconds',
            'microseconds', 'nanoseconds'):
            verify_time_or_datetime_arg_allow_tz(start_dt, 'add_interval_' +
                unit, 'start_dt')
        else:
            verify_datetime_arg_allow_tz(start_dt, 'add_interval_' + unit,
                'start_dt')
        yaorz__gmbp = get_tz_if_exists(start_dt)
        trlj__zsfq = ['amount', 'start_dt']
        fbhc__fonfv = [amount, start_dt]
        yetrg__qljgk = [True] * 2
        vbdf__ovzb = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        orp__pif = None
        if is_valid_time_arg(start_dt):
            fbjz__vsjdf = start_dt.precision
            if unit == 'hours':
                bev__dke = 3600000000000
            elif unit == 'minutes':
                bev__dke = 60000000000
            elif unit == 'seconds':
                bev__dke = 1000000000
            elif unit == 'milliseconds':
                fbjz__vsjdf = max(fbjz__vsjdf, 3)
                bev__dke = 1000000
            elif unit == 'microseconds':
                fbjz__vsjdf = max(fbjz__vsjdf, 6)
                bev__dke = 1000
            elif unit == 'nanoseconds':
                fbjz__vsjdf = max(fbjz__vsjdf, 9)
                bev__dke = 1
            lib__oyt = (
                f'amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {bev__dke} * arg0\n'
                )
            lib__oyt += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={fbjz__vsjdf})'
                )
            bggf__nbtze = types.Array(bodo.hiframes.time_ext.TimeType(
                fbjz__vsjdf), 1, 'C')
        elif yaorz__gmbp is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(yaorz__gmbp
                ):
                buwcb__ntdg = pytz.timezone(yaorz__gmbp)
                omlvg__zjv = np.array(buwcb__ntdg._utc_transition_times,
                    dtype='M8[ns]').view('i8')
                srn__ipo = np.array(buwcb__ntdg._transition_info)[:, 0]
                srn__ipo = (pd.Series(srn__ipo).dt.total_seconds() * 1000000000
                    ).astype(np.int64).values
                orp__pif = {'trans': omlvg__zjv, 'deltas': srn__ipo}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    lib__oyt = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    lib__oyt = f'td = pd.DateOffset({unit}=arg0)\n'
                lib__oyt += f'start_value = arg1.value\n'
                lib__oyt += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    yaorz__gmbp):
                    lib__oyt += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    lib__oyt += (
                        "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                        )
                    lib__oyt += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    lib__oyt += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    lib__oyt += 'td = pd.Timedelta(end_value - start_value)\n'
            else:
                if unit == 'nanoseconds':
                    lib__oyt = 'td = pd.Timedelta(arg0)\n'
                else:
                    lib__oyt = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    yaorz__gmbp):
                    lib__oyt += f'start_value = arg1.value\n'
                    lib__oyt += 'end_value = start_value + td.value\n'
                    lib__oyt += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    lib__oyt += (
                        "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                        )
                    lib__oyt += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    lib__oyt += 'td = pd.Timedelta(td.value + offset)\n'
            lib__oyt += f'res[i] = arg1 + td\n'
            bggf__nbtze = bodo.DatetimeArrayType(yaorz__gmbp)
        else:
            jib__mywkx = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                vbdf__ovzb else '')
            vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if vbdf__ovzb else
                '')
            if unit in ('months', 'years'):
                lib__oyt = f"""res[i] = {jib__mywkx}({vdbj__nvq}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                lib__oyt = f"""res[i] = {jib__mywkx}({vdbj__nvq}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                lib__oyt = (
                    f'res[i] = {jib__mywkx}({vdbj__nvq}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                lib__oyt = (
                    f'res[i] = {jib__mywkx}({vdbj__nvq}(arg1) + pd.Timedelta({unit}=arg0))\n'
                    )
            bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk,
            lib__oyt, bggf__nbtze, extra_globals=orp__pif)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    qdlur__jamcf = [('years', add_interval_years, add_interval_years_util),
        ('quarters', add_interval_quarters, add_interval_quarters_util), (
        'months', add_interval_months, add_interval_months_util), ('weeks',
        add_interval_weeks, add_interval_weeks_util), ('days',
        add_interval_days, add_interval_days_util), ('hours',
        add_interval_hours, add_interval_hours_util), ('minutes',
        add_interval_minutes, add_interval_minutes_util), ('seconds',
        add_interval_seconds, add_interval_seconds_util), ('milliseconds',
        add_interval_milliseconds, add_interval_milliseconds_util), (
        'microseconds', add_interval_microseconds,
        add_interval_microseconds_util), ('nanoseconds',
        add_interval_nanoseconds, add_interval_nanoseconds_util)]
    for unit, zkie__bab, pgiaz__guujb in qdlur__jamcf:
        qcox__cmj = create_add_interval_func_overload(unit)
        overload(zkie__bab)(qcox__cmj)
        wbfu__ztwqc = create_add_interval_util_overload(unit)
        overload(pgiaz__guujb)(wbfu__ztwqc)


_install_add_interval_overload()


def dayofmonth_util(arr):
    return


def dayofweek_util(arr):
    return


def dayofweekiso_util(arr):
    return


def dayofyear_util(arr):
    return


def get_year_util(arr):
    return


def get_quarter_util(arr):
    return


def get_month_util(arr):
    return


def get_week_util(arr):
    return


def get_hour_util(arr):
    return


def get_minute_util(arr):
    return


def get_second_util(arr):
    return


def get_millisecond_util(arr):
    return


def get_microsecond_util(arr):
    return


def get_nanosecond_util(arr):
    return


def create_dt_extract_fn_overload(fn_name):

    def overload_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(f'bodo.libs.bodosql_array_kernels.{fn_name}',
                ['arr'], 0)
        qbxhy__lzhw = 'def impl(arr):\n'
        qbxhy__lzhw += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        fcj__jmxe = {}
        exec(qbxhy__lzhw, {'bodo': bodo}, fcj__jmxe)
        return fcj__jmxe['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        nas__fbh = get_tz_if_exists(arr)
        vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if nas__fbh is
            None else '')
        sjfit__mutc = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        npp__pgna = {'get_year': f'{vdbj__nvq}(arg0).year', 'get_quarter':
            f'{vdbj__nvq}(arg0).quarter', 'get_month':
            f'{vdbj__nvq}(arg0).month', 'get_week':
            f'{vdbj__nvq}(arg0).week', 'get_hour':
            f'{vdbj__nvq}(arg0).hour', 'get_minute':
            f'{vdbj__nvq}(arg0).minute', 'get_second':
            f'{vdbj__nvq}(arg0).second', 'get_millisecond':
            f'{vdbj__nvq}(arg0).{sjfit__mutc}', 'get_microsecond':
            f'{vdbj__nvq}(arg0).microsecond', 'get_nanosecond':
            f'{vdbj__nvq}(arg0).nanosecond', 'dayofmonth':
            f'{vdbj__nvq}(arg0).day', 'dayofweek':
            f'({vdbj__nvq}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{vdbj__nvq}(arg0).dayofweek + 1', 'dayofyear':
            f'{vdbj__nvq}(arg0).dayofyear'}
        trlj__zsfq = ['arr']
        fbhc__fonfv = [arr]
        yetrg__qljgk = [True]
        lib__oyt = f'res[i] = {npp__pgna[fn_name]}'
        bggf__nbtze = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk,
            lib__oyt, bggf__nbtze)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    qdlur__jamcf = [('get_year', get_year, get_year_util), ('get_quarter',
        get_quarter, get_quarter_util), ('get_month', get_month,
        get_month_util), ('get_week', get_week, get_week_util), ('get_hour',
        get_hour, get_hour_util), ('get_minute', get_minute,
        get_minute_util), ('get_second', get_second, get_second_util), (
        'get_millisecond', get_millisecond, get_millisecond_util), (
        'get_microsecond', get_microsecond, get_microsecond_util), (
        'get_nanosecond', get_nanosecond, get_nanosecond_util), (
        'dayofmonth', dayofmonth, dayofmonth_util), ('dayofweek', dayofweek,
        dayofweek_util), ('dayofweekiso', dayofweekiso, dayofweekiso_util),
        ('dayofyear', dayofyear, dayofyear_util)]
    for fn_name, zkie__bab, pgiaz__guujb in qdlur__jamcf:
        qcox__cmj = create_dt_extract_fn_overload(fn_name)
        overload(zkie__bab)(qcox__cmj)
        wbfu__ztwqc = create_dt_extract_fn_util_overload(fn_name)
        overload(pgiaz__guujb)(wbfu__ztwqc)


_install_dt_extract_fn_overload()


def diff_day_util(arr0, arr1):
    return


def diff_hour_util(arr0, arr1):
    return


def diff_microsecond_util(arr0, arr1):
    return


def diff_minute_util(arr0, arr1):
    return


def diff_month_util(arr0, arr1):
    return


def diff_nanosecond_util(arr0, arr1):
    return


def diff_quarter_util(arr0, arr1):
    return


def diff_second_util(arr0, arr1):
    return


def diff_week_util(arr0, arr1):
    return


def diff_year_util(arr0, arr1):
    return


@register_jitable
def get_iso_weeks_between_years(year0, year1):
    hucet__tiedh = 1
    if year1 < year0:
        year0, year1 = year1, year0
        hucet__tiedh = -1
    ejlw__zqgnl = 0
    for hvbmh__nnss in range(year0, year1):
        ejlw__zqgnl += 52
        vkwgw__aqk = (hvbmh__nnss + hvbmh__nnss // 4 - hvbmh__nnss // 100 +
            hvbmh__nnss // 400) % 7
        amc__ydjjj = (hvbmh__nnss - 1 + (hvbmh__nnss - 1) // 4 - (
            hvbmh__nnss - 1) // 100 + (hvbmh__nnss - 1) // 400) % 7
        if vkwgw__aqk == 4 or amc__ydjjj == 3:
            ejlw__zqgnl += 1
    return hucet__tiedh * ejlw__zqgnl


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for eevll__vkpg in range(len(args)):
            if isinstance(args[eevll__vkpg], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], eevll__vkpg)
        qbxhy__lzhw = 'def impl(arr0, arr1):\n'
        qbxhy__lzhw += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        fcj__jmxe = {}
        exec(qbxhy__lzhw, {'bodo': bodo}, fcj__jmxe)
        return fcj__jmxe['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        nas__fbh = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != nas__fbh:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        trlj__zsfq = ['arr0', 'arr1']
        fbhc__fonfv = [arr0, arr1]
        yetrg__qljgk = [True] * 2
        orp__pif = None
        frow__bky = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        viyj__gtodz = {'year': ['yr_diff'], 'quarter': ['yr_diff',
            'qu_diff'], 'month': ['yr_diff', 'mo_diff'], 'week': [
            'y0, w0, _', 'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': [
            'da_diff'], 'nanosecond': ['ns_diff']}
        lib__oyt = ''
        if nas__fbh == None:
            lib__oyt += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            lib__oyt += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for mbj__qnc in viyj__gtodz.get(unit, []):
            lib__oyt += f'{mbj__qnc} = {frow__bky[mbj__qnc]}\n'
        if unit == 'nanosecond':
            bggf__nbtze = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            bggf__nbtze = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            lib__oyt += 'res[i] = yr_diff'
        elif unit == 'quarter':
            lib__oyt += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            lib__oyt += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            lib__oyt += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            lib__oyt += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            lib__oyt += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                svhu__juc = 3600000000000
            if unit == 'minute':
                svhu__juc = 60000000000
            if unit == 'second':
                svhu__juc = 1000000000
            if unit == 'microsecond':
                svhu__juc = 1000
            lib__oyt += f"""res[i] = np.floor_divide((arg1.value), ({svhu__juc})) - np.floor_divide((arg0.value), ({svhu__juc}))
"""
        return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk,
            lib__oyt, bggf__nbtze, extra_globals=orp__pif)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    qdlur__jamcf = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, zkie__bab, pgiaz__guujb in qdlur__jamcf:
        qcox__cmj = create_dt_diff_fn_overload(unit)
        overload(zkie__bab)(qcox__cmj)
        wbfu__ztwqc = create_dt_diff_fn_util_overload(unit)
        overload(pgiaz__guujb)(wbfu__ztwqc)


_install_dt_diff_fn_overload()


def date_trunc(date_or_time_part, ts_arg):
    pass


@overload(date_trunc)
def overload_date_trunc(date_or_time_part, ts_arg):
    if isinstance(date_or_time_part, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 0)
    if isinstance(ts_arg, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 1)

    def impl(date_or_time_part, ts_arg):
        return date_trunc_util(date_or_time_part, ts_arg)
    return impl


def date_trunc_util(date_or_time_part, ts_arg):
    pass


@overload(date_trunc_util)
def overload_date_trunc_util(date_or_time_part, ts_arg):
    verify_string_arg(date_or_time_part, 'DATE_TRUNC', 'date_or_time_part')
    verify_datetime_arg_allow_tz(ts_arg, 'DATE_TRUNC', 'ts_arg')
    inl__xignd = get_tz_if_exists(ts_arg)
    trlj__zsfq = ['date_or_time_part', 'ts_arg']
    fbhc__fonfv = [date_or_time_part, ts_arg]
    yetrg__qljgk = [True, True]
    vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(ts_arg, True) else '')
    lib__oyt = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if inl__xignd is None:
        lib__oyt += f'arg1 = {vdbj__nvq}(arg1)\n'
    lib__oyt += "if part_str == 'quarter':\n"
    lib__oyt += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    lib__oyt += "elif part_str == 'year':\n"
    lib__oyt += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    lib__oyt += "elif part_str == 'month':\n"
    lib__oyt += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    lib__oyt += "elif part_str == 'day':\n"
    lib__oyt += '    out_val = arg1.normalize()\n'
    lib__oyt += "elif part_str == 'week':\n"
    lib__oyt += '    if arg1.dayofweek == 0:\n'
    lib__oyt += '        out_val = arg1.normalize()\n'
    lib__oyt += '    else:\n'
    lib__oyt += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    lib__oyt += "elif part_str == 'hour':\n"
    lib__oyt += "    out_val = arg1.floor('H')\n"
    lib__oyt += "elif part_str == 'minute':\n"
    lib__oyt += "    out_val = arg1.floor('min')\n"
    lib__oyt += "elif part_str == 'second':\n"
    lib__oyt += "    out_val = arg1.floor('S')\n"
    lib__oyt += "elif part_str == 'millisecond':\n"
    lib__oyt += "    out_val = arg1.floor('ms')\n"
    lib__oyt += "elif part_str == 'microsecond':\n"
    lib__oyt += "    out_val = arg1.floor('us')\n"
    lib__oyt += "elif part_str == 'nanosecond':\n"
    lib__oyt += '    out_val = arg1\n'
    lib__oyt += 'else:\n'
    lib__oyt += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if inl__xignd is None:
        lib__oyt += f'res[i] = {jib__mywkx}(out_val)\n'
    else:
        lib__oyt += f'res[i] = out_val\n'
    if inl__xignd is None:
        bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        bggf__nbtze = bodo.DatetimeArrayType(inl__xignd)
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, extra_globals={'tz_literal': inl__xignd})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    nas__fbh = get_tz_if_exists(arr)
    vdbj__nvq = 'bodo.utils.conversion.box_if_dt64' if nas__fbh is None else ''
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    lib__oyt = f'res[i] = {vdbj__nvq}(arg0).day_name()'
    bggf__nbtze = bodo.string_array_type
    ljt__ujk = ['V']
    xmms__voq = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    orp__pif = {'day_of_week_dict_arr': xmms__voq}
    dbjb__xhmgy = 'dict_res = day_of_week_dict_arr'
    bpuga__zzwt = f'res[i] = {vdbj__nvq}(arg0).dayofweek'
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, synthesize_dict_if_vector=ljt__ujk,
        synthesize_dict_setup_text=dbjb__xhmgy, synthesize_dict_scalar_text
        =bpuga__zzwt, extra_globals=orp__pif, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    lib__oyt = f'res[i] = {jib__mywkx}(pd.Timedelta(days=arg0))'
    bggf__nbtze = np.dtype('timedelta64[ns]')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    yaorz__gmbp = get_tz_if_exists(arr)
    vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    if yaorz__gmbp is None:
        lib__oyt = (
            f'res[i] = {jib__mywkx}({vdbj__nvq}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        bggf__nbtze = np.dtype('datetime64[ns]')
    else:
        lib__oyt = 'y = arg0.year\n'
        lib__oyt += 'm = arg0.month\n'
        lib__oyt += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        lib__oyt += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(yaorz__gmbp)})\n'
            )
        bggf__nbtze = bodo.DatetimeArrayType(yaorz__gmbp)
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    trlj__zsfq = ['year', 'day']
    fbhc__fonfv = [year, day]
    yetrg__qljgk = [True] * 2
    lib__oyt = (
        f'res[i] = {jib__mywkx}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    bggf__nbtze = np.dtype('datetime64[ns]')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    nas__fbh = get_tz_if_exists(arr)
    vdbj__nvq = 'bodo.utils.conversion.box_if_dt64' if nas__fbh is None else ''
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    lib__oyt = f'res[i] = {vdbj__nvq}(arg0).month_name()'
    bggf__nbtze = bodo.string_array_type
    ljt__ujk = ['V']
    qlz__qnqzt = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    orp__pif = {'month_names_dict_arr': qlz__qnqzt}
    dbjb__xhmgy = 'dict_res = month_names_dict_arr'
    bpuga__zzwt = f'res[i] = {vdbj__nvq}(arg0).month - 1'
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, synthesize_dict_if_vector=ljt__ujk,
        synthesize_dict_setup_text=dbjb__xhmgy, synthesize_dict_scalar_text
        =bpuga__zzwt, extra_globals=orp__pif, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    ennpz__kbz = is_valid_tz_aware_datetime_arg(arr0)
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    trlj__zsfq = ['arr0', 'arr1']
    fbhc__fonfv = [arr0, arr1]
    yetrg__qljgk = [True] * 2
    ugjg__tyf = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    lib__oyt = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if ennpz__kbz:
        fqd__chru = 'arg0'
    else:
        fqd__chru = 'bodo.utils.conversion.box_if_dt64(arg0)'
    lib__oyt += f"""new_timestamp = {fqd__chru}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    lib__oyt += f'res[i] = {jib__mywkx}(new_timestamp.tz_localize(None))\n'
    bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, prefix_code=ugjg__tyf)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    ennpz__kbz = is_valid_tz_aware_datetime_arg(arr0)
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    trlj__zsfq = ['arr0', 'arr1']
    fbhc__fonfv = [arr0, arr1]
    yetrg__qljgk = [True] * 2
    ugjg__tyf = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    lib__oyt = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if ennpz__kbz:
        fqd__chru = 'arg0'
    else:
        fqd__chru = 'bodo.utils.conversion.box_if_dt64(arg0)'
    lib__oyt += f"""new_timestamp = {fqd__chru}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    lib__oyt += f'res[i] = {jib__mywkx}(new_timestamp.tz_localize(None))\n'
    bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, prefix_code=ugjg__tyf)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    jib__mywkx = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    lib__oyt = f"res[i] = {jib__mywkx}(pd.Timestamp(arg0, unit='s'))"
    bggf__nbtze = np.dtype('datetime64[ns]')
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    lib__oyt = f'dt = {vdbj__nvq}(arg0)\n'
    lib__oyt += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    bggf__nbtze = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    vdbj__nvq = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    lib__oyt = f'dt = {vdbj__nvq}(arg0)\n'
    lib__oyt += 'res[i] = dt.isocalendar()[0]'
    bggf__nbtze = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)


def to_days(arr):
    pass


@overload(to_days)
def overload_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_days_util',
            ['arr'], 0)

    def impl(arr):
        return to_days_util(arr)
    return impl


def to_days_util(arr):
    pass


@overload(to_days_util)
def overload_to_days_util(arr):
    verify_datetime_arg(arr, 'TO_DAYS', 'arr')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    ugjg__tyf = 'unix_days_to_year_zero = 719528\n'
    ugjg__tyf += 'nanoseconds_divisor = 86400000000000\n'
    bggf__nbtze = bodo.IntegerArrayType(types.int64)
    fbgcw__mhoyz = bodo.utils.utils.is_array_typ(arr, False)
    if fbgcw__mhoyz:
        lib__oyt = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        lib__oyt = '  in_value = arg0.value\n'
    lib__oyt += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, prefix_code=ugjg__tyf)


def from_days(arr):
    pass


@overload(from_days)
def overload_from_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.from_days_util',
            ['arr'], 0)

    def impl(arr):
        return from_days_util(arr)
    return impl


def from_days_util(arr):
    pass


@overload(from_days_util)
def overload_from_days_util(arr):
    verify_int_arg(arr, 'TO_DAYS', 'arr')
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    fbgcw__mhoyz = bodo.utils.utils.is_array_typ(arr, False)
    if fbgcw__mhoyz:
        bggf__nbtze = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        bggf__nbtze = bodo.pd_timestamp_tz_naive_type
    ugjg__tyf = 'unix_days_to_year_zero = 719528\n'
    ugjg__tyf += 'nanoseconds_divisor = 86400000000000\n'
    lib__oyt = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if fbgcw__mhoyz:
        lib__oyt += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        lib__oyt += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, prefix_code=ugjg__tyf)


def to_seconds(arr):
    pass


@overload(to_seconds)
def overload_to_seconds(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_seconds_util'
            , ['arr'], 0)

    def impl(arr):
        return to_seconds_util(arr)
    return impl


def to_seconds_util(arr):
    pass


@overload(to_seconds_util)
def overload_to_seconds_util(arr):
    verify_datetime_arg_allow_tz(arr, 'TO_SECONDS', 'arr')
    jzrq__mwjnj = get_tz_if_exists(arr)
    trlj__zsfq = ['arr']
    fbhc__fonfv = [arr]
    yetrg__qljgk = [True]
    ugjg__tyf = 'unix_seconds_to_year_zero = 62167219200\n'
    ugjg__tyf += 'nanoseconds_divisor = 1000000000\n'
    bggf__nbtze = bodo.IntegerArrayType(types.int64)
    fbgcw__mhoyz = bodo.utils.utils.is_array_typ(arr, False)
    if fbgcw__mhoyz and not jzrq__mwjnj:
        lib__oyt = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        lib__oyt = f'  in_value = arg0.value\n'
    lib__oyt += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze, prefix_code=ugjg__tyf)


def tz_aware_interval_add(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add)
def overload_tz_aware_interval_add(tz_arg, interval_arg):
    if isinstance(tz_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 0)
    if isinstance(interval_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 1)

    def impl(tz_arg, interval_arg):
        return tz_aware_interval_add_util(tz_arg, interval_arg)
    return impl


def tz_aware_interval_add_util(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add_util)
def overload_tz_aware_interval_add_util(tz_arg, interval_arg):
    verify_datetime_arg_require_tz(tz_arg, 'INTERVAL_ADD', 'tz_arg')
    verify_sql_interval(interval_arg, 'INTERVAL_ADD', 'interval_arg')
    jzrq__mwjnj = get_tz_if_exists(tz_arg)
    trlj__zsfq = ['tz_arg', 'interval_arg']
    fbhc__fonfv = [tz_arg, interval_arg]
    yetrg__qljgk = [True, True]
    if jzrq__mwjnj is not None:
        bggf__nbtze = bodo.DatetimeArrayType(jzrq__mwjnj)
    else:
        bggf__nbtze = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        lib__oyt = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        lib__oyt = '  timedelta = arg1\n'
    lib__oyt += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    lib__oyt += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(trlj__zsfq, fbhc__fonfv, yetrg__qljgk, lib__oyt,
        bggf__nbtze)
