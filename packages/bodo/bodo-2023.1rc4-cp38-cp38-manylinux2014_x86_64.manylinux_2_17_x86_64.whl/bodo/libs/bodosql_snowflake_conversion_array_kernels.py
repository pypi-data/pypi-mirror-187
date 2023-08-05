"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_literal_value, get_overload_const_bool, is_literal_type, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True)
def try_to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean_util(arr, _try=False):
    verify_string_numeric_arg(arr, 'TO_BOOLEAN', 'arr')
    siqdv__folp = is_valid_string_arg(arr)
    kio__lyqz = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        mucky__pqx = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if siqdv__folp:
            mjyqf__frix = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            mjyqf__frix = 'value must be a valid numeric expression'
        mucky__pqx = (
            f'raise ValueError("invalid value for boolean conversion: {mjyqf__frix}")'
            )
    nwov__oniy = ['arr', '_try']
    hjakl__anw = [arr, _try]
    old__qoeaq = [True, False]
    jkxxp__hfaot = None
    if siqdv__folp:
        jkxxp__hfaot = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        jkxxp__hfaot += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if siqdv__folp:
        pvd__wqv = 's = arg0.lower()\n'
        pvd__wqv += f'is_true_val = s in true_vals\n'
        pvd__wqv += f'res[i] = is_true_val\n'
        pvd__wqv += f'if not (is_true_val or s in false_vals):\n'
        pvd__wqv += f'  {mucky__pqx}\n'
    elif kio__lyqz:
        pvd__wqv = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        pvd__wqv += f'  {mucky__pqx}\n'
        pvd__wqv += 'else:\n'
        pvd__wqv += f'  res[i] = bool(arg0)\n'
    else:
        pvd__wqv = f'res[i] = bool(arg0)'
    lrqn__trp = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp, prefix_code=jkxxp__hfaot)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for pvq__rztds in range(2):
        if isinstance(args[pvq__rztds], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'],
                pvq__rztds)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for pvq__rztds in range(2):
        if isinstance(args[pvq__rztds], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], pvq__rztds
                )

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_char', [
            'arr'], 0)

    def impl(arr):
        return to_char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def to_char_util(arr):
    nwov__oniy = ['arr']
    hjakl__anw = [arr]
    old__qoeaq = [True]
    if is_valid_binary_arg(arr):
        pvd__wqv = 'with bodo.objmode(r=bodo.string_type):\n'
        pvd__wqv += '  r = arg0.hex()\n'
        pvd__wqv += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        pvd__wqv = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        pvd__wqv += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        pvd__wqv += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        pvd__wqv += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        pvd__wqv += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        pvd__wqv += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        pvd__wqv += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        pvd__wqv += 'if arg0.nanosecond > 0:\n'
        pvd__wqv += "  part_str = part_str + '.' + ms_str + us_str + ns_str\n"
        pvd__wqv += 'elif arg0.microsecond > 0:\n'
        pvd__wqv += "  part_str = part_str + '.' + ms_str + us_str\n"
        pvd__wqv += 'elif arg0.millisecond > 0:\n'
        pvd__wqv += "  part_str = part_str + '.' + ms_str\n"
        pvd__wqv += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        pvd__wqv = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        pvd__wqv += 'with bodo.objmode(r=bodo.string_type):\n'
        pvd__wqv += '    r = str(v)\n'
        pvd__wqv += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            pvd__wqv = "tz_raw = arg0.strftime('%z')\n"
            pvd__wqv += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            pvd__wqv += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            pvd__wqv = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        pvd__wqv = 'if np.isinf(arg0):\n'
        pvd__wqv += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        pvd__wqv += 'elif np.isnan(arg0):\n'
        pvd__wqv += "  res[i] = 'NaN'\n"
        pvd__wqv += 'else:\n'
        pvd__wqv += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        pvd__wqv = "res[i] = 'true' if arg0 else 'false'"
    else:
        hqofc__lqp = {(8): np.int8, (16): np.int16, (32): np.int32, (64):
            np.int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                uoqyn__xolea = arr.dtype.bitwidth
            else:
                uoqyn__xolea = arr.bitwidth
            pvd__wqv = (
                f'if arg0 == {np.iinfo(hqofc__lqp[uoqyn__xolea]).min}:\n')
            pvd__wqv += (
                f"  res[i] = '{np.iinfo(hqofc__lqp[uoqyn__xolea]).min}'\n")
            pvd__wqv += 'else:\n'
            pvd__wqv += '  res[i] = str(arg0)'
        else:
            pvd__wqv = 'res[i] = str(arg0)'
    lrqn__trp = bodo.string_array_type
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            fjf__xxlu = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            fjf__xxlu = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            fjf__xxlu = pd.to_datetime(val, unit='us')
        else:
            fjf__xxlu = pd.to_datetime(val, unit='ns')
        return fjf__xxlu
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            fjf__xxlu = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            fjf__xxlu = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            fjf__xxlu = pd.Timestamp(val, unit='us')
        else:
            fjf__xxlu = pd.Timestamp(val, unit='ns')
        return fjf__xxlu
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        lrrnk__zpjvb = val.split(' ')[0]
        if len(lrrnk__zpjvb) < 10:
            return False, None
        else:
            uknnn__keaji = lrrnk__zpjvb.count('/') in [0, 2]
            guvzv__lbl = lrrnk__zpjvb.count('-') in [0, 2]
            if not (uknnn__keaji and guvzv__lbl):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        iul__txq = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(iul__txq):
            success_flag = False
        else:
            ret_val = iul__txq
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        conhm__hwmd = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        conhm__hwmd = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        ropvk__khvrv = ''
    else:
        ropvk__khvrv = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    ehxy__qtbem = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    cqyo__omei = 'unbox_if_tz_naive_timestamp' if ehxy__qtbem else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        pvd__wqv = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        pvd__wqv += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        pvd__wqv += 'if not was_successful:\n'
        pvd__wqv += f'  {conhm__hwmd}\n'
        pvd__wqv += 'else:\n'
        pvd__wqv += f'  res[i] = {cqyo__omei}(tmp_val{ropvk__khvrv})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        pvd__wqv = 'arg0 = str(arg0)\n'
        pvd__wqv += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        pvd__wqv += (
            f'   res[i] = {cqyo__omei}(int_to_datetime(np.int64(arg0)){ropvk__khvrv})\n'
            )
        pvd__wqv += 'else:\n'
        pvd__wqv += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        pvd__wqv += '   if not was_successful:\n'
        pvd__wqv += f'      {conhm__hwmd}\n'
        pvd__wqv += '   else:\n'
        pvd__wqv += f'      res[i] = {cqyo__omei}(tmp_val{ropvk__khvrv})\n'
    elif is_valid_int_arg(conversionVal):
        pvd__wqv = (
            f'res[i] = {cqyo__omei}(int_to_datetime(arg0){ropvk__khvrv})\n')
    elif is_valid_float_arg(conversionVal):
        pvd__wqv = (
            f'res[i] = {cqyo__omei}(float_to_datetime(arg0){ropvk__khvrv})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        pvd__wqv = f'res[i] = {cqyo__omei}(pd.Timestamp(arg0){ropvk__khvrv})\n'
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        pvd__wqv = f'res[i] = arg0{ropvk__khvrv}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    nwov__oniy = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    hjakl__anw = [conversionVal, optionalConversionFormatString,
        errorOnFail, _keep_time]
    old__qoeaq = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        lrqn__trp = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        lrqn__trp = types.Array(bodo.datetime64ns, 1, 'C')
    dauh__aicco = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp, extra_globals=dauh__aicco)


def cast_tz_naive_to_tz_aware(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_naive_to_tz_aware', [
            'arr', 'tz'], 0)

    def impl(arr, tz):
        return cast_tz_naive_to_tz_aware_util(arr, tz)
    return impl


def cast_tz_naive_to_tz_aware_util(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware_util, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    verify_datetime_arg(arr, 'cast_tz_naive_to_tz_aware', 'arr')
    nwov__oniy = ['arr', 'tz']
    hjakl__anw = [arr, tz]
    old__qoeaq = [True, False]
    nbsg__nlto = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr) else '')
    pvd__wqv = f'res[i] = {nbsg__nlto}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    lrqn__trp = bodo.DatetimeArrayType(tz)
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp)


def cast_tz_aware_to_tz_naive(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_aware_to_tz_naive', [
            'arr', 'normalize'], 0)

    def impl(arr, normalize):
        return cast_tz_aware_to_tz_naive_util(arr, normalize)
    return impl


def cast_tz_aware_to_tz_naive_util(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive_util, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive_util(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    normalize = get_overload_const_bool(normalize)
    verify_datetime_arg_require_tz(arr, 'cast_tz_aware_to_tz_naive', 'arr')
    nwov__oniy = ['arr', 'normalize']
    hjakl__anw = [arr, normalize]
    old__qoeaq = [True, False]
    cqyo__omei = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    pvd__wqv = ''
    if normalize:
        pvd__wqv += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        pvd__wqv += 'ts = arg0.tz_localize(None)\n'
    pvd__wqv += f'res[i] = {cqyo__omei}(ts)'
    lrqn__trp = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp)


def cast_str_to_tz_aware(arr, tz):
    pass


@overload(cast_str_to_tz_aware, no_unliteral=True)
def overload_cast_str_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_str_to_tz_aware', ['arr',
            'tz'], 0)

    def impl(arr, tz):
        return cast_str_to_tz_aware_util(arr, tz)
    return impl


def cast_str_to_tz_aware_util(arr, tz):
    pass


@overload(cast_str_to_tz_aware_util, no_unliteral=True)
def overload_cast_str_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    verify_string_arg(arr, 'cast_str_to_tz_aware', 'arr')
    nwov__oniy = ['arr', 'tz']
    hjakl__anw = [arr, tz]
    old__qoeaq = [True, False]
    pvd__wqv = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    lrqn__trp = bodo.DatetimeArrayType(tz)
    return gen_vectorized(nwov__oniy, hjakl__anw, old__qoeaq, pvd__wqv,
        lrqn__trp)
