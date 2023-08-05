"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import BodoError


def cast_float64(arr):
    return


def cast_float64_util(arr):
    return


def cast_float32(arr):
    return


def cast_float32_util(arr):
    return


def cast_int64(arr):
    return


def cast_int64_util(arr):
    return


def cast_int32(arr):
    return


def cast_int32_util(arr):
    return


def cast_int16(arr):
    return


def cast_int16_util(arr):
    return


def cast_int8(arr):
    return


def cast_int8_util(arr):
    return


def cast_boolean(arr):
    return


def cast_char(arr):
    return


def cast_date(arr):
    return arr


def cast_timestamp(arr):
    return


def cast_interval(arr):
    return


def cast_interval_util(arr):
    return


cast_funcs_utils_names = (cast_float64, cast_float64_util, 'float64'), (
    cast_float32, cast_float32_util, 'float32'), (cast_int64,
    cast_int64_util, 'int64'), (cast_int32, cast_int32_util, 'int32'), (
    cast_int16, cast_int16_util, 'int16'), (cast_int8, cast_int8_util, 'int8'
    ), (cast_boolean, None, 'boolean'), (cast_char, None, 'char'), (cast_date,
    None, 'date'), (cast_timestamp, None, 'timestamp'), (cast_interval,
    cast_interval, 'interval')
fname_to_equiv = {'float64': 'np.float64', 'float32': 'np.float32', 'int64':
    'np.int64', 'int32': 'np.int32', 'int16': 'np.int16', 'int8': 'np.int8',
    'interval': 'pd.to_timedelta'}
fname_to_dtype = {'float64': types.Array(bodo.float64, 1, 'C'), 'float32':
    types.Array(bodo.float32, 1, 'C'), 'int64': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int64), 'int32': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int32), 'int16': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int16), 'int8': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int8), 'interval': np.dtype('timedelta64[ns]')}


def create_cast_func_overload(func_name):

    def overload_cast_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(
                f'bodo.libs.bodosql_array_kernels.cast_{func_name}', ['arr'], 0
                )
        secda__yfj = 'def impl(arr):\n'
        if func_name == 'boolean':
            secda__yfj += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_boolean_util(arr, numba.literally(True))
"""
        elif func_name == 'char':
            secda__yfj += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_char_util(arr)
"""
        elif func_name == 'date':
            secda__yfj += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(True), numba.literally(False))
"""
        elif func_name == 'timestamp':
            secda__yfj += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(False), numba.literally(True))
"""
        else:
            secda__yfj += (
                f'  return bodo.libs.bodosql_array_kernels.cast_{func_name}_util(arr)'
                )
        wsboz__dfr = {}
        exec(secda__yfj, {'bodo': bodo, 'numba': numba}, wsboz__dfr)
        return wsboz__dfr['impl']
    return overload_cast_func


def create_cast_util_overload(func_name):

    def overload_cast_util(arr):
        jsw__gxmas = ['arr']
        lsy__uxonp = [arr]
        fsqm__rra = [True]
        ckk__dowzj = ''
        if func_name[:3
            ] == 'int' and func_name != 'interval' and not is_valid_boolean_arg(
            arr):
            if is_valid_int_arg(arr):
                ckk__dowzj += """if arg0 < np.iinfo(np.int64).min or arg0 > np.iinfo(np.int64).max:
"""
                ckk__dowzj += '  bodo.libs.array_kernels.setna(res, i)\n'
                ckk__dowzj += 'else:\n'
                ckk__dowzj += f'  res[i] = {fname_to_equiv[func_name]}(arg0)\n'
            else:
                if is_valid_string_arg(arr):
                    ckk__dowzj = 'i_val = 0\n'
                    ckk__dowzj += 'f_val = np.float64(arg0)\n'
                    ckk__dowzj += """is_valid = not (pd.isna(f_val) or np.isinf(f_val) or f_val < np.iinfo(np.int64).min or f_val > np.iinfo(np.int64).max)
"""
                    ckk__dowzj += 'is_int = (f_val % 1 == 0)\n'
                    ckk__dowzj += 'if not (is_valid and is_int):\n'
                    ckk__dowzj += '  val = f_val\n'
                    ckk__dowzj += 'else:\n'
                    ckk__dowzj += '  val = np.int64(arg0)\n'
                    ckk__dowzj += '  i_val = np.int64(arg0)\n'
                else:
                    if not is_valid_float_arg(arr):
                        raise BodoError(
                            'only strings, floats, booleans, and ints can be cast to ints'
                            )
                    ckk__dowzj += 'val = arg0\n'
                    ckk__dowzj += """is_valid = not(pd.isna(val) or np.isinf(val) or val < np.iinfo(np.int64).min or val > np.iinfo(np.int64).max)
"""
                    ckk__dowzj += 'is_int = (val % 1 == 0)\n'
                ckk__dowzj += 'if not is_valid:\n'
                ckk__dowzj += '  bodo.libs.array_kernels.setna(res, i)\n'
                ckk__dowzj += 'else:\n'
                if is_valid_float_arg(arr):
                    ckk__dowzj += '  i_val = np.int64(val)\n'
                ckk__dowzj += '  if not is_int:\n'
                ckk__dowzj += (
                    '    ans = np.int64(np.sign(val) * np.floor(np.abs(val) + 0.5))\n'
                    )
                ckk__dowzj += '  else:\n'
                ckk__dowzj += '    ans = i_val\n'
                if func_name == 'int64':
                    ckk__dowzj += f'  res[i] = ans\n'
                else:
                    ckk__dowzj += (
                        f'  res[i] = {fname_to_equiv[func_name]}(ans)')
        elif func_name == 'interval':
            khr__vvtz = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
                .utils.utils.is_array_typ(arr, True) else '')
            ckk__dowzj += f'res[i] = {khr__vvtz}(pd.to_timedelta(arg0))'
        else:
            ckk__dowzj += f'res[i] = {fname_to_equiv[func_name]}(arg0)'
        iko__jglt = fname_to_dtype[func_name]
        return gen_vectorized(jsw__gxmas, lsy__uxonp, fsqm__rra, ckk__dowzj,
            iko__jglt)
    return overload_cast_util


def _install_cast_func_overloads(funcs_utils_names):
    for kfftn__agvou, fqq__xcwp, nblx__xsmm in funcs_utils_names:
        overload(kfftn__agvou)(create_cast_func_overload(nblx__xsmm))
        if nblx__xsmm not in ('boolean', 'char', 'date', 'timestamp'):
            overload(fqq__xcwp)(create_cast_util_overload(nblx__xsmm))


_install_cast_func_overloads(cast_funcs_utils_names)
