"""
Implements numerical array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.utils import is_array_typ


def cbrt(arr):
    return


def ceil(arr):
    return


def factorial(arr):
    return


def floor(arr):
    return


def mod(arr0, arr1):
    return


def sign(arr):
    return


def sqrt(arr):
    return


def round(arr0, arr1):
    return


def trunc(arr0, arr1):
    return


def abs(arr):
    return


def ln(arr):
    return


def log2(arr):
    return


def log10(arr):
    return


def exp(arr):
    return


def power(arr0, arr1):
    return


def sqrt_util(arr):
    return


def square(arr):
    return


def cbrt_util(arr):
    return


def ceil_util(arr):
    return


def factorial_util(arr):
    return


def floor_util(arr):
    return


def mod_util(arr0, arr1):
    return


def sign_util(arr):
    return


def round_util(arr0, arr1):
    return


def trunc_util(arr0, arr1):
    return


def abs_util(arr):
    return


def ln_util(arr):
    return


def log2_util(arr):
    return


def log10_util(arr):
    return


def exp_util(arr):
    return


def power_util(arr0, arr1):
    return


def square_util(arr):
    return


funcs_utils_names = (abs, abs_util, 'ABS'), (cbrt, cbrt_util, 'CBRT'), (ceil,
    ceil_util, 'CEIL'), (factorial, factorial_util, 'FACTORIAL'), (floor,
    floor_util, 'FLOOR'), (ln, ln_util, 'LN'), (log2, log2_util, 'LOG2'), (
    log10, log10_util, 'LOG10'), (mod, mod_util, 'MOD'), (sign, sign_util,
    'SIGN'), (round, round_util, 'ROUND'), (trunc, trunc_util, 'TRUNC'), (exp,
    exp_util, 'EXP'), (power, power_util, 'POWER'), (sqrt, sqrt_util, 'SQRT'
    ), (square, square_util, 'SQUARE')
double_arg_funcs = 'MOD', 'TRUNC', 'POWER', 'ROUND'
single_arg_funcs = set(a[2] for a in funcs_utils_names if a[2] not in
    double_arg_funcs)
_float = {(16): types.float16, (32): types.float32, (64): types.float64}
_int = {(8): types.int8, (16): types.int16, (32): types.int32, (64): types.
    int64}
_uint = {(8): types.uint8, (16): types.uint16, (32): types.uint32, (64):
    types.uint64}


def _get_numeric_output_dtype(func_name, arr0, arr1=None):
    uwc__enzl = arr0.dtype if is_array_typ(arr0) else arr0
    olq__tttl = arr1.dtype if is_array_typ(arr1) else arr1
    rjd__roox = bodo.float64
    if (arr0 is None or uwc__enzl == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or olq__tttl ==
        bodo.none):
        return types.Array(rjd__roox, 1, 'C')
    if isinstance(uwc__enzl, types.Float):
        if isinstance(olq__tttl, types.Float):
            rjd__roox = _float[max(uwc__enzl.bitwidth, olq__tttl.bitwidth)]
        else:
            rjd__roox = uwc__enzl
    if func_name == 'SIGN':
        if isinstance(uwc__enzl, types.Integer):
            rjd__roox = uwc__enzl
    elif func_name == 'MOD':
        if isinstance(uwc__enzl, types.Integer) and isinstance(olq__tttl,
            types.Integer):
            if uwc__enzl.signed:
                if olq__tttl.signed:
                    rjd__roox = olq__tttl
                else:
                    rjd__roox = _int[min(64, olq__tttl.bitwidth * 2)]
            else:
                rjd__roox = olq__tttl
    elif func_name == 'ABS':
        if isinstance(uwc__enzl, types.Integer):
            if uwc__enzl.signed:
                rjd__roox = _uint[min(64, uwc__enzl.bitwidth * 2)]
            else:
                rjd__roox = uwc__enzl
    elif func_name == 'ROUND':
        if isinstance(uwc__enzl, (types.Float, types.Integer)):
            rjd__roox = uwc__enzl
    elif func_name == 'FACTORIAL':
        rjd__roox = bodo.int64
    if isinstance(rjd__roox, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(rjd__roox)
    else:
        return types.Array(rjd__roox, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            wvzar__xbwkc = 'def impl(arr):\n'
            wvzar__xbwkc += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            fpcre__czc = {}
            exec(wvzar__xbwkc, {'bodo': bodo}, fpcre__czc)
            return fpcre__czc['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for mfe__zddb in range(2):
                if isinstance(args[mfe__zddb], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], mfe__zddb)
            wvzar__xbwkc = 'def impl(arr0, arr1):\n'
            wvzar__xbwkc += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            fpcre__czc = {}
            exec(wvzar__xbwkc, {'bodo': bodo}, fpcre__czc)
            return fpcre__czc['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            qfrod__bbb = ['arr']
            nxxth__fjih = [arr]
            oarm__qngai = [True]
            viwar__glg = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    viwar__glg += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    viwar__glg += '  bodo.libs.array_kernels.setna(res, i)\n'
                    viwar__glg += 'else:\n'
                    viwar__glg += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    viwar__glg += f'res[i] = np.log(arg0)'
                else:
                    viwar__glg += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            rjd__roox = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai,
                viwar__glg, rjd__roox)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            qfrod__bbb = ['arr0', 'arr1']
            nxxth__fjih = [arr0, arr1]
            oarm__qngai = [True, True]
            rjd__roox = _get_numeric_output_dtype(func_name, arr0, arr1)
            viwar__glg = ''
            if func_name == 'MOD':
                viwar__glg += 'if arg1 == 0:\n'
                viwar__glg += '  bodo.libs.array_kernels.setna(res, i)\n'
                viwar__glg += 'else:\n'
                viwar__glg += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                viwar__glg += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                viwar__glg += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                viwar__glg += 'if int(arg1) == arg1:\n'
                viwar__glg += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                viwar__glg += 'else:\n'
                viwar__glg += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai,
                viwar__glg, rjd__roox)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for ogk__xyq, bolvd__swn, func_name in funcs_utils_names:
        mgem__futdz = create_numeric_func_overload(func_name)
        overload(ogk__xyq)(mgem__futdz)
        jgske__aoqh = create_numeric_util_overload(func_name)
        overload(bolvd__swn)(jgske__aoqh)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], mfe__zddb)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                mfe__zddb)

    def impl(A, B):
        return bitshiftleft_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.bitnot_util',
            ['A'], 0)

    def impl(A):
        return bitnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def bitor(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], mfe__zddb)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                mfe__zddb)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], mfe__zddb)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for mfe__zddb in range(3):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], mfe__zddb)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], mfe__zddb)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for mfe__zddb in range(4):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], mfe__zddb)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], mfe__zddb)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for mfe__zddb in range(2):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], mfe__zddb)

    def impl(arr, base):
        return log_util(arr, base)
    return impl


@numba.generated_jit(nopython=True)
def negate(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.negate_util',
            ['arr'], 0)

    def impl(arr):
        return negate_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def width_bucket(arr, min_val, max_val, num_buckets):
    args = [arr, min_val, max_val, num_buckets]
    for mfe__zddb in range(4):
        if isinstance(args[mfe__zddb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], mfe__zddb)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = arg0 & arg1'
    rjd__roox = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = arg0 << arg1'
    rjd__roox = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    qfrod__bbb = ['A']
    nxxth__fjih = [A]
    oarm__qngai = [True]
    viwar__glg = 'res[i] = ~arg0'
    if A == bodo.none:
        rjd__roox = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            spuk__hhf = A.dtype
        else:
            spuk__hhf = A
        rjd__roox = bodo.libs.int_arr_ext.IntegerArrayType(spuk__hhf)
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = arg0 | arg1'
    rjd__roox = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    if A == bodo.none:
        spuk__hhf = rjd__roox = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            spuk__hhf = A.dtype
        else:
            spuk__hhf = A
        rjd__roox = bodo.libs.int_arr_ext.IntegerArrayType(spuk__hhf)
    viwar__glg = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = arg0 ^ arg1'
    rjd__roox = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    qfrod__bbb = ['arr', 'old_base', 'new_base']
    nxxth__fjih = [arr, old_base, new_base]
    oarm__qngai = [True] * 3
    viwar__glg = 'old_val = int(arg0, arg1)\n'
    viwar__glg += 'if arg2 == 2:\n'
    viwar__glg += "   res[i] = format(old_val, 'b')\n"
    viwar__glg += 'elif arg2 == 8:\n'
    viwar__glg += "   res[i] = format(old_val, 'o')\n"
    viwar__glg += 'elif arg2 == 10:\n'
    viwar__glg += "   res[i] = format(old_val, 'd')\n"
    viwar__glg += 'elif arg2 == 16:\n'
    viwar__glg += "   res[i] = format(old_val, 'x')\n"
    viwar__glg += 'else:\n'
    viwar__glg += '   bodo.libs.array_kernels.setna(res, i)\n'
    rjd__roox = bodo.string_array_type
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    qfrod__bbb = ['A', 'B']
    nxxth__fjih = [A, B]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = (arg0 >> arg1) & 1'
    rjd__roox = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    qfrod__bbb = ['lat1', 'lon1', 'lat2', 'lon2']
    nxxth__fjih = [lat1, lon1, lat2, lon2]
    wmlb__ucnq = [True] * 4
    viwar__glg = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    kwknl__wtxuv = '(arg2 - arg0) * 0.5'
    pxc__pluu = '(arg3 - arg1) * 0.5'
    frp__sbmq = (
        f'np.square(np.sin({kwknl__wtxuv})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({pxc__pluu})))'
        )
    viwar__glg += f'res[i] = 12742.0 * np.arcsin(np.sqrt({frp__sbmq}))\n'
    rjd__roox = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, wmlb__ucnq, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    qfrod__bbb = ['arr', 'divisor']
    nxxth__fjih = [arr, divisor]
    wmlb__ucnq = [True] * 2
    viwar__glg = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    rjd__roox = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, wmlb__ucnq, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    qfrod__bbb = ['arr', 'base']
    nxxth__fjih = [arr, base]
    oarm__qngai = [True] * 2
    viwar__glg = 'res[i] = np.log(arg0) / np.log(arg1)'
    rjd__roox = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    qfrod__bbb = ['arr']
    nxxth__fjih = [arr]
    oarm__qngai = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        spuk__hhf = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        spuk__hhf = arr.data.dtype
    else:
        spuk__hhf = arr
    viwar__glg = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(spuk__hhf, 'res[i] = -arg0')
    spuk__hhf = {types.uint8: types.int16, types.uint16: types.int32, types
        .uint32: types.int64, types.uint64: types.int64}.get(spuk__hhf,
        spuk__hhf)
    if isinstance(spuk__hhf, types.Integer):
        rjd__roox = bodo.utils.typing.dtype_to_array_type(spuk__hhf)
    else:
        rjd__roox = arr
    rjd__roox = bodo.utils.typing.to_nullable_type(rjd__roox)
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    qfrod__bbb = ['arr', 'min_val', 'max_val', 'num_buckets']
    nxxth__fjih = [arr, min_val, max_val, num_buckets]
    oarm__qngai = [True] * 4
    viwar__glg = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    viwar__glg += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    viwar__glg += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    rjd__roox = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(qfrod__bbb, nxxth__fjih, oarm__qngai, viwar__glg,
        rjd__roox)
