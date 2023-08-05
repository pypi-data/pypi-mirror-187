"""
Implements string array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.char_util',
            ['arr'], 0)

    def impl(arr):
        return char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def contains(arr, pattern):
    args = [arr, pattern]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], xtsyc__yxyg)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    oory__rutu = bodo.boolean_array
    bgvaw__tuk = ['arr', 'pattern']
    hneb__eaw = [arr, pattern]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], xtsyc__yxyg)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], xtsyc__yxyg)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], xtsyc__yxyg)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], xtsyc__yxyg)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], xtsyc__yxyg)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for xtsyc__yxyg in range(4):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], xtsyc__yxyg)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], xtsyc__yxyg)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], xtsyc__yxyg)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], xtsyc__yxyg)

    def impl(arr, length, padstr):
        return lpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def ord_ascii(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.ord_ascii_util',
            ['arr'], 0)

    def impl(arr):
        return ord_ascii_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def position(substr, source, start):
    args = [substr, source, start]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], xtsyc__yxyg)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], xtsyc__yxyg)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], xtsyc__yxyg)

    def impl(arr, to_replace, replace_with):
        return replace_util(arr, to_replace, replace_with)
    return impl


@numba.generated_jit(nopython=True)
def reverse(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.reverse_util',
            ['arr'], 0)

    def impl(arr):
        return reverse_util(arr)
    return impl


def right(arr, n_chars):
    return


@overload(right)
def overload_right(arr, n_chars):
    args = [arr, n_chars]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], xtsyc__yxyg)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], xtsyc__yxyg)

    def impl(arr, length, padstr):
        return rpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def rtrimmed_length(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.rtrimmed_length_util', ['arr'], 0)

    def impl(arr):
        return rtrimmed_length_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def space(n_chars):
    if isinstance(n_chars, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.space_util',
            ['n_chars'], 0)

    def impl(n_chars):
        return space_util(n_chars)
    return impl


@numba.generated_jit(nopython=True)
def split_part(source, delim, part):
    args = [source, delim, part]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], xtsyc__yxyg)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], xtsyc__yxyg)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for xtsyc__yxyg in range(2):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], xtsyc__yxyg)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], xtsyc__yxyg)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], xtsyc__yxyg)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], xtsyc__yxyg)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for xtsyc__yxyg in range(3):
        if isinstance(args[xtsyc__yxyg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], xtsyc__yxyg)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    bgvaw__tuk = ['arr']
    hneb__eaw = [arr]
    vbli__wpz = [True]
    rehfz__ikvd = 'if 0 <= arg0 <= 127:\n'
    rehfz__ikvd += '   res[i] = chr(arg0)\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   bodo.libs.array_kernels.setna(res, i)\n'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    bgvaw__tuk = ['arr', 'delim']
    hneb__eaw = [arr, delim]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'capitalized = arg0[:1].upper()\n'
    rehfz__ikvd += 'for j in range(1, len(arg0)):\n'
    rehfz__ikvd += '   if arg0[j-1] in arg1:\n'
    rehfz__ikvd += '      capitalized += arg0[j].upper()\n'
    rehfz__ikvd += '   else:\n'
    rehfz__ikvd += '      capitalized += arg0[j].lower()\n'
    rehfz__ikvd += 'res[i] = capitalized'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    bgvaw__tuk = ['arr', 'target']
    hneb__eaw = [arr, target]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'res[i] = arg0.find(arg1) + 1'
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    ggrin__vszzy, diz__gxl = len(s), len(t)
    icww__jeftu, pijfi__fytk = 1, 0
    arr = np.zeros((2, ggrin__vszzy + 1), dtype=np.uint32)
    arr[0, :] = np.arange(ggrin__vszzy + 1)
    for xtsyc__yxyg in range(1, diz__gxl + 1):
        arr[icww__jeftu, 0] = xtsyc__yxyg
        for qgp__plidk in range(1, ggrin__vszzy + 1):
            if s[qgp__plidk - 1] == t[xtsyc__yxyg - 1]:
                arr[icww__jeftu, qgp__plidk] = arr[pijfi__fytk, qgp__plidk - 1]
            else:
                arr[icww__jeftu, qgp__plidk] = 1 + min(arr[icww__jeftu, 
                    qgp__plidk - 1], arr[pijfi__fytk, qgp__plidk], arr[
                    pijfi__fytk, qgp__plidk - 1])
        icww__jeftu, pijfi__fytk = pijfi__fytk, icww__jeftu
    return arr[diz__gxl % 2, ggrin__vszzy]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    ggrin__vszzy, diz__gxl = len(s), len(t)
    if ggrin__vszzy <= maxDistance and diz__gxl <= maxDistance:
        return min_edit_distance(s, t)
    icww__jeftu, pijfi__fytk = 1, 0
    arr = np.zeros((2, ggrin__vszzy + 1), dtype=np.uint32)
    arr[0, :] = np.arange(ggrin__vszzy + 1)
    for xtsyc__yxyg in range(1, diz__gxl + 1):
        arr[icww__jeftu, 0] = xtsyc__yxyg
        for qgp__plidk in range(1, ggrin__vszzy + 1):
            if s[qgp__plidk - 1] == t[xtsyc__yxyg - 1]:
                arr[icww__jeftu, qgp__plidk] = arr[pijfi__fytk, qgp__plidk - 1]
            else:
                arr[icww__jeftu, qgp__plidk] = 1 + min(arr[icww__jeftu, 
                    qgp__plidk - 1], arr[pijfi__fytk, qgp__plidk], arr[
                    pijfi__fytk, qgp__plidk - 1])
        if (arr[icww__jeftu] >= maxDistance).all():
            return maxDistance
        icww__jeftu, pijfi__fytk = pijfi__fytk, icww__jeftu
    return min(arr[diz__gxl % 2, ggrin__vszzy], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    bgvaw__tuk = ['s', 't']
    hneb__eaw = [s, t]
    vbli__wpz = [True] * 2
    rehfz__ikvd = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    bgvaw__tuk = ['s', 't', 'maxDistance']
    hneb__eaw = [s, t, maxDistance]
    vbli__wpz = [True] * 3
    rehfz__ikvd = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    evbup__lppm = verify_string_binary_arg(source, 'endswith', 'source')
    if evbup__lppm != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    bgvaw__tuk = ['source', 'suffix']
    hneb__eaw = [source, suffix]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'res[i] = arg0.endswith(arg1)'
    oory__rutu = bodo.boolean_array
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    bgvaw__tuk = ['arr', 'places']
    hneb__eaw = [arr, places]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'prec = max(arg1, 0)\n'
    rehfz__ikvd += "res[i] = format(arg0, f',.{prec}f')"
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    evbup__lppm = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if evbup__lppm != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    bgvaw__tuk = ['arr', 'pos', 'length', 'inject']
    hneb__eaw = [arr, pos, length, inject]
    vbli__wpz = [True] * 4
    rehfz__ikvd = 'prefixIndex = max(arg1-1, 0)\n'
    rehfz__ikvd += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    rehfz__ikvd += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    oory__rutu = (bodo.string_array_type if evbup__lppm else bodo.
        binary_array_type)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        evbup__lppm = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        cpr__fsen = "''" if evbup__lppm else "b''"
        bgvaw__tuk = ['arr', 'n_chars']
        hneb__eaw = [arr, n_chars]
        vbli__wpz = [True] * 2
        rehfz__ikvd = 'if arg1 <= 0:\n'
        rehfz__ikvd += f'   res[i] = {cpr__fsen}\n'
        rehfz__ikvd += 'else:\n'
        if func_name == 'LEFT':
            rehfz__ikvd += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            rehfz__ikvd += '   res[i] = arg0[-arg1:]\n'
        oory__rutu = (bodo.string_array_type if evbup__lppm else bodo.
            binary_array_type)
        return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
            oory__rutu, may_cause_duplicate_dict_array_values=True)
    return overload_left_right_util


def _install_left_right_overload():
    for qshai__nlrto, func_name in zip((left_util, right_util), ('LEFT',
        'RIGHT')):
        pzsfv__uvbx = create_left_right_util_overload(func_name)
        overload(qshai__nlrto)(pzsfv__uvbx)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        ird__vnas = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        evbup__lppm = verify_string_binary_arg(arr, func_name, 'arr')
        if evbup__lppm != ird__vnas:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        oory__rutu = (bodo.string_array_type if evbup__lppm else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            ijjy__inyfc = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            ijjy__inyfc = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        bgvaw__tuk = ['arr', 'length', 'pad_string']
        hneb__eaw = [arr, length, pad_string]
        vbli__wpz = [True] * 3
        cpr__fsen = "''" if evbup__lppm else "b''"
        rehfz__ikvd = f"""                if arg1 <= 0:
                    res[i] = {cpr__fsen}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {ijjy__inyfc}"""
        return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
            oory__rutu, may_cause_duplicate_dict_array_values=True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for qshai__nlrto, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')
        ):
        pzsfv__uvbx = create_lpad_rpad_util_overload(func_name)
        overload(qshai__nlrto)(pzsfv__uvbx)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    bgvaw__tuk = ['arr']
    hneb__eaw = [arr]
    vbli__wpz = [True]
    rehfz__ikvd = 'if len(arg0) == 0:\n'
    rehfz__ikvd += '   bodo.libs.array_kernels.setna(res, i)\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   res[i] = ord(arg0[0])'
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    vuohv__dcdl = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if vuohv__dcdl != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert vuohv__dcdl, '[BE-3717] Support binary find with 3 args'
    bgvaw__tuk = ['substr', 'source', 'start']
    hneb__eaw = [substr, source, start]
    vbli__wpz = [True] * 3
    rehfz__ikvd = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    bgvaw__tuk = ['arr', 'repeats']
    hneb__eaw = [arr, repeats]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'if arg1 <= 0:\n'
    rehfz__ikvd += "   res[i] = ''\n"
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   res[i] = arg0 * arg1'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    bgvaw__tuk = ['arr', 'to_replace', 'replace_with']
    hneb__eaw = [arr, to_replace, replace_with]
    vbli__wpz = [True] * 3
    rehfz__ikvd = "if arg1 == '':\n"
    rehfz__ikvd += '   res[i] = arg0\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   res[i] = arg0.replace(arg1, arg2)'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    evbup__lppm = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    bgvaw__tuk = ['arr']
    hneb__eaw = [arr]
    vbli__wpz = [True]
    rehfz__ikvd = 'res[i] = arg0[::-1]'
    oory__rutu = bodo.string_array_type
    oory__rutu = (bodo.string_array_type if evbup__lppm else bodo.
        binary_array_type)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    bgvaw__tuk = ['arr']
    hneb__eaw = [arr]
    vbli__wpz = [True]
    rehfz__ikvd = "res[i] = len(arg0.rstrip(' '))"
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    bgvaw__tuk = ['n_chars']
    hneb__eaw = [n_chars]
    vbli__wpz = [True]
    rehfz__ikvd = 'if arg0 <= 0:\n'
    rehfz__ikvd += "   res[i] = ''\n"
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += "   res[i] = ' ' * arg0"
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    bgvaw__tuk = ['source', 'delim', 'part']
    hneb__eaw = [source, delim, part]
    vbli__wpz = [True] * 3
    rehfz__ikvd = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    rehfz__ikvd += 'if abs(arg2) > len(tokens):\n'
    rehfz__ikvd += "    res[i] = ''\n"
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    evbup__lppm = verify_string_binary_arg(source, 'startswith', 'source')
    if evbup__lppm != verify_string_binary_arg(prefix, 'startswith', 'prefix'):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    bgvaw__tuk = ['source', 'prefix']
    hneb__eaw = [source, prefix]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'res[i] = arg0.startswith(arg1)'
    oory__rutu = bodo.boolean_array
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    bgvaw__tuk = ['arr0', 'arr1']
    hneb__eaw = [arr0, arr1]
    vbli__wpz = [True] * 2
    rehfz__ikvd = 'if arg0 < arg1:\n'
    rehfz__ikvd += '   res[i] = -1\n'
    rehfz__ikvd += 'elif arg0 > arg1:\n'
    rehfz__ikvd += '   res[i] = 1\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   res[i] = 0\n'
    oory__rutu = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    bgvaw__tuk = ['source', 'delim', 'part']
    hneb__eaw = [source, delim, part]
    vbli__wpz = [True] * 3
    rehfz__ikvd = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    rehfz__ikvd += '   bodo.libs.array_kernels.setna(res, i)\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   tokens = []\n'
    rehfz__ikvd += "   buffer = ''\n"
    rehfz__ikvd += '   for j in range(len(arg0)):\n'
    rehfz__ikvd += '      if arg0[j] in arg1:\n'
    rehfz__ikvd += "         if buffer != '':"
    rehfz__ikvd += '            tokens.append(buffer)\n'
    rehfz__ikvd += "         buffer = ''\n"
    rehfz__ikvd += '      else:\n'
    rehfz__ikvd += '         buffer += arg0[j]\n'
    rehfz__ikvd += "   if buffer != '':\n"
    rehfz__ikvd += '      tokens.append(buffer)\n'
    rehfz__ikvd += '   if arg2 > len(tokens):\n'
    rehfz__ikvd += '      bodo.libs.array_kernels.setna(res, i)\n'
    rehfz__ikvd += '   else:\n'
    rehfz__ikvd += '      res[i] = tokens[arg2-1]\n'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    evbup__lppm = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    oory__rutu = (bodo.string_array_type if evbup__lppm else bodo.
        binary_array_type)
    bgvaw__tuk = ['arr', 'start', 'length']
    hneb__eaw = [arr, start, length]
    vbli__wpz = [True] * 3
    rehfz__ikvd = 'if arg2 <= 0:\n'
    rehfz__ikvd += "   res[i] = ''\n" if evbup__lppm else "   res[i] = b''\n"
    rehfz__ikvd += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    rehfz__ikvd += '   res[i] = arg0[arg1:]\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   if arg1 > 0: arg1 -= 1\n'
    rehfz__ikvd += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    bgvaw__tuk = ['arr', 'delimiter', 'occurrences']
    hneb__eaw = [arr, delimiter, occurrences]
    vbli__wpz = [True] * 3
    rehfz__ikvd = "if arg1 == '' or arg2 == 0:\n"
    rehfz__ikvd += "   res[i] = ''\n"
    rehfz__ikvd += 'elif arg2 >= 0:\n'
    rehfz__ikvd += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    rehfz__ikvd += 'else:\n'
    rehfz__ikvd += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    bgvaw__tuk = ['arr', 'source', 'target']
    hneb__eaw = [arr, source, target]
    vbli__wpz = [True] * 3
    rehfz__ikvd = "translated = ''\n"
    rehfz__ikvd += 'for char in arg0:\n'
    rehfz__ikvd += '   index = arg1.find(char)\n'
    rehfz__ikvd += '   if index == -1:\n'
    rehfz__ikvd += '      translated += char\n'
    rehfz__ikvd += '   elif index < len(arg2):\n'
    rehfz__ikvd += '      translated += arg2[index]\n'
    rehfz__ikvd += 'res[i] = translated'
    oory__rutu = bodo.string_array_type
    return gen_vectorized(bgvaw__tuk, hneb__eaw, vbli__wpz, rehfz__ikvd,
        oory__rutu, may_cause_duplicate_dict_array_values=True)
