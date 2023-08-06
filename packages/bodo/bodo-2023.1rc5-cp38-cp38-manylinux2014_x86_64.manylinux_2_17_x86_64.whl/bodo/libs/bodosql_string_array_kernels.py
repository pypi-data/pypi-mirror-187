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
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.contains',
                ['arr', 'contains'], fukay__imvw)

    def impl(arr, pattern):
        return contains_util(arr, pattern)
    return impl


@numba.generated_jit(nopython=True)
def contains_util(arr, pattern):
    verify_string_binary_arg(arr, 'CONTAINS', 'arr')
    verify_string_binary_arg(pattern, 'CONTAINS', 'pattern')
    ecxm__ahxrg = bodo.boolean_array
    xnsj__pofc = ['arr', 'pattern']
    abrge__cdpr = [arr, pattern]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'res[i] = arg1 in arg0\n'
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], fukay__imvw)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], fukay__imvw)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def endswith(source, suffix):
    args = [source, suffix]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.endswith',
                ['source', 'suffix'], fukay__imvw)

    def impl(source, suffix):
        return endswith_util(source, suffix)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], fukay__imvw)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], fukay__imvw)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def insert(source, pos, length, inject):
    args = [source, pos, length, inject]
    for fukay__imvw in range(4):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.insert',
                ['source', 'pos', 'length', 'inject'], fukay__imvw)

    def impl(source, pos, length, inject):
        return insert_util(source, pos, length, inject)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], fukay__imvw)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], fukay__imvw)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], fukay__imvw)

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
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.position',
                ['substr', 'source', 'start'], fukay__imvw)

    def impl(substr, source, start):
        return position_util(substr, source, start)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], fukay__imvw)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], fukay__imvw)

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
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], fukay__imvw)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], fukay__imvw)

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
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], fukay__imvw)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def startswith(source, prefix):
    args = [source, prefix]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.startswith',
                ['source', 'prefix'], fukay__imvw)

    def impl(source, prefix):
        return startswith_util(source, prefix)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for fukay__imvw in range(2):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], fukay__imvw)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], fukay__imvw)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], fukay__imvw)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], fukay__imvw)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for fukay__imvw in range(3):
        if isinstance(args[fukay__imvw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], fukay__imvw)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    xnsj__pofc = ['arr']
    abrge__cdpr = [arr]
    miic__xptis = [True]
    ktjpt__brkz = 'if 0 <= arg0 <= 127:\n'
    ktjpt__brkz += '   res[i] = chr(arg0)\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   bodo.libs.array_kernels.setna(res, i)\n'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    xnsj__pofc = ['arr', 'delim']
    abrge__cdpr = [arr, delim]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'capitalized = arg0[:1].upper()\n'
    ktjpt__brkz += 'for j in range(1, len(arg0)):\n'
    ktjpt__brkz += '   if arg0[j-1] in arg1:\n'
    ktjpt__brkz += '      capitalized += arg0[j].upper()\n'
    ktjpt__brkz += '   else:\n'
    ktjpt__brkz += '      capitalized += arg0[j].lower()\n'
    ktjpt__brkz += 'res[i] = capitalized'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    xnsj__pofc = ['arr', 'target']
    abrge__cdpr = [arr, target]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'res[i] = arg0.find(arg1) + 1'
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    xuk__mrzg, jhx__wawq = len(s), len(t)
    xlc__pdsgc, qirs__nrbj = 1, 0
    arr = np.zeros((2, xuk__mrzg + 1), dtype=np.uint32)
    arr[0, :] = np.arange(xuk__mrzg + 1)
    for fukay__imvw in range(1, jhx__wawq + 1):
        arr[xlc__pdsgc, 0] = fukay__imvw
        for kjs__bbqc in range(1, xuk__mrzg + 1):
            if s[kjs__bbqc - 1] == t[fukay__imvw - 1]:
                arr[xlc__pdsgc, kjs__bbqc] = arr[qirs__nrbj, kjs__bbqc - 1]
            else:
                arr[xlc__pdsgc, kjs__bbqc] = 1 + min(arr[xlc__pdsgc, 
                    kjs__bbqc - 1], arr[qirs__nrbj, kjs__bbqc], arr[
                    qirs__nrbj, kjs__bbqc - 1])
        xlc__pdsgc, qirs__nrbj = qirs__nrbj, xlc__pdsgc
    return arr[jhx__wawq % 2, xuk__mrzg]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    xuk__mrzg, jhx__wawq = len(s), len(t)
    if xuk__mrzg <= maxDistance and jhx__wawq <= maxDistance:
        return min_edit_distance(s, t)
    xlc__pdsgc, qirs__nrbj = 1, 0
    arr = np.zeros((2, xuk__mrzg + 1), dtype=np.uint32)
    arr[0, :] = np.arange(xuk__mrzg + 1)
    for fukay__imvw in range(1, jhx__wawq + 1):
        arr[xlc__pdsgc, 0] = fukay__imvw
        for kjs__bbqc in range(1, xuk__mrzg + 1):
            if s[kjs__bbqc - 1] == t[fukay__imvw - 1]:
                arr[xlc__pdsgc, kjs__bbqc] = arr[qirs__nrbj, kjs__bbqc - 1]
            else:
                arr[xlc__pdsgc, kjs__bbqc] = 1 + min(arr[xlc__pdsgc, 
                    kjs__bbqc - 1], arr[qirs__nrbj, kjs__bbqc], arr[
                    qirs__nrbj, kjs__bbqc - 1])
        if (arr[xlc__pdsgc] >= maxDistance).all():
            return maxDistance
        xlc__pdsgc, qirs__nrbj = qirs__nrbj, xlc__pdsgc
    return min(arr[jhx__wawq % 2, xuk__mrzg], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    xnsj__pofc = ['s', 't']
    abrge__cdpr = [s, t]
    miic__xptis = [True] * 2
    ktjpt__brkz = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    xnsj__pofc = ['s', 't', 'maxDistance']
    abrge__cdpr = [s, t, maxDistance]
    miic__xptis = [True] * 3
    ktjpt__brkz = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def endswith_util(source, suffix):
    qodnh__lrvkj = verify_string_binary_arg(source, 'endswith', 'source')
    if qodnh__lrvkj != verify_string_binary_arg(suffix, 'endswith', 'suffix'):
        raise bodo.utils.typing.BodoError(
            'String and suffix must both be strings or both binary')
    xnsj__pofc = ['source', 'suffix']
    abrge__cdpr = [source, suffix]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'res[i] = arg0.endswith(arg1)'
    ecxm__ahxrg = bodo.boolean_array
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    xnsj__pofc = ['arr', 'places']
    abrge__cdpr = [arr, places]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'prec = max(arg1, 0)\n'
    ktjpt__brkz += "res[i] = format(arg0, f',.{prec}f')"
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def insert_util(arr, pos, length, inject):
    qodnh__lrvkj = verify_string_binary_arg(arr, 'INSERT', 'arr')
    verify_int_arg(pos, 'INSERT', 'pos')
    verify_int_arg(length, 'INSERT', 'length')
    if qodnh__lrvkj != verify_string_binary_arg(inject, 'INSERT', 'inject'):
        raise bodo.utils.typing.BodoError(
            'String and injected value must both be strings or both binary')
    xnsj__pofc = ['arr', 'pos', 'length', 'inject']
    abrge__cdpr = [arr, pos, length, inject]
    miic__xptis = [True] * 4
    ktjpt__brkz = 'prefixIndex = max(arg1-1, 0)\n'
    ktjpt__brkz += 'suffixIndex = prefixIndex + max(arg2, 0)\n'
    ktjpt__brkz += 'res[i] = arg0[:prefixIndex] + arg3 + arg0[suffixIndex:]'
    ecxm__ahxrg = (bodo.string_array_type if qodnh__lrvkj else bodo.
        binary_array_type)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        qodnh__lrvkj = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        qskks__zkbwj = "''" if qodnh__lrvkj else "b''"
        xnsj__pofc = ['arr', 'n_chars']
        abrge__cdpr = [arr, n_chars]
        miic__xptis = [True] * 2
        ktjpt__brkz = 'if arg1 <= 0:\n'
        ktjpt__brkz += f'   res[i] = {qskks__zkbwj}\n'
        ktjpt__brkz += 'else:\n'
        if func_name == 'LEFT':
            ktjpt__brkz += '   res[i] = arg0[:arg1]\n'
        elif func_name == 'RIGHT':
            ktjpt__brkz += '   res[i] = arg0[-arg1:]\n'
        ecxm__ahxrg = (bodo.string_array_type if qodnh__lrvkj else bodo.
            binary_array_type)
        return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis,
            ktjpt__brkz, ecxm__ahxrg, may_cause_duplicate_dict_array_values
            =True)
    return overload_left_right_util


def _install_left_right_overload():
    for omsi__cfa, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')
        ):
        ykjzs__xwudy = create_left_right_util_overload(func_name)
        overload(omsi__cfa)(ykjzs__xwudy)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        ziwn__ree = verify_string_binary_arg(pad_string, func_name,
            'pad_string')
        qodnh__lrvkj = verify_string_binary_arg(arr, func_name, 'arr')
        if qodnh__lrvkj != ziwn__ree:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        ecxm__ahxrg = (bodo.string_array_type if qodnh__lrvkj else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            hdy__foyn = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            hdy__foyn = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        xnsj__pofc = ['arr', 'length', 'pad_string']
        abrge__cdpr = [arr, length, pad_string]
        miic__xptis = [True] * 3
        qskks__zkbwj = "''" if qodnh__lrvkj else "b''"
        ktjpt__brkz = f"""                if arg1 <= 0:
                    res[i] = {qskks__zkbwj}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {hdy__foyn}"""
        return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis,
            ktjpt__brkz, ecxm__ahxrg, may_cause_duplicate_dict_array_values
            =True)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for omsi__cfa, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        ykjzs__xwudy = create_lpad_rpad_util_overload(func_name)
        overload(omsi__cfa)(ykjzs__xwudy)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    xnsj__pofc = ['arr']
    abrge__cdpr = [arr]
    miic__xptis = [True]
    ktjpt__brkz = 'if len(arg0) == 0:\n'
    ktjpt__brkz += '   bodo.libs.array_kernels.setna(res, i)\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   res[i] = ord(arg0[0])'
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def position_util(substr, source, start):
    ljgeg__wkc = verify_string_binary_arg(substr, 'POSITION', 'substr')
    if ljgeg__wkc != verify_string_binary_arg(source, 'POSITION', 'source'):
        raise bodo.utils.typing.BodoError(
            'Substring and source must be both strings or both binary')
    verify_int_arg(start, 'POSITION', 'start')
    assert ljgeg__wkc, '[BE-3717] Support binary find with 3 args'
    xnsj__pofc = ['substr', 'source', 'start']
    abrge__cdpr = [substr, source, start]
    miic__xptis = [True] * 3
    ktjpt__brkz = 'res[i] = arg1.find(arg0, arg2 - 1) + 1'
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    xnsj__pofc = ['arr', 'repeats']
    abrge__cdpr = [arr, repeats]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'if arg1 <= 0:\n'
    ktjpt__brkz += "   res[i] = ''\n"
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   res[i] = arg0 * arg1'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    xnsj__pofc = ['arr', 'to_replace', 'replace_with']
    abrge__cdpr = [arr, to_replace, replace_with]
    miic__xptis = [True] * 3
    ktjpt__brkz = "if arg1 == '':\n"
    ktjpt__brkz += '   res[i] = arg0\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   res[i] = arg0.replace(arg1, arg2)'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    qodnh__lrvkj = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    xnsj__pofc = ['arr']
    abrge__cdpr = [arr]
    miic__xptis = [True]
    ktjpt__brkz = 'res[i] = arg0[::-1]'
    ecxm__ahxrg = bodo.string_array_type
    ecxm__ahxrg = (bodo.string_array_type if qodnh__lrvkj else bodo.
        binary_array_type)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def rtrimmed_length_util(arr):
    verify_string_arg(arr, 'RTRIMMED_LENGTH', 'arr')
    xnsj__pofc = ['arr']
    abrge__cdpr = [arr]
    miic__xptis = [True]
    ktjpt__brkz = "res[i] = len(arg0.rstrip(' '))"
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    xnsj__pofc = ['n_chars']
    abrge__cdpr = [n_chars]
    miic__xptis = [True]
    ktjpt__brkz = 'if arg0 <= 0:\n'
    ktjpt__brkz += "   res[i] = ''\n"
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += "   res[i] = ' ' * arg0"
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    xnsj__pofc = ['source', 'delim', 'part']
    abrge__cdpr = [source, delim, part]
    miic__xptis = [True] * 3
    ktjpt__brkz = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    ktjpt__brkz += 'if abs(arg2) > len(tokens):\n'
    ktjpt__brkz += "    res[i] = ''\n"
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def startswith_util(source, prefix):
    qodnh__lrvkj = verify_string_binary_arg(source, 'startswith', 'source')
    if qodnh__lrvkj != verify_string_binary_arg(prefix, 'startswith', 'prefix'
        ):
        raise bodo.utils.typing.BodoError(
            'String and prefix must both be strings or both binary')
    xnsj__pofc = ['source', 'prefix']
    abrge__cdpr = [source, prefix]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'res[i] = arg0.startswith(arg1)'
    ecxm__ahxrg = bodo.boolean_array
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    xnsj__pofc = ['arr0', 'arr1']
    abrge__cdpr = [arr0, arr1]
    miic__xptis = [True] * 2
    ktjpt__brkz = 'if arg0 < arg1:\n'
    ktjpt__brkz += '   res[i] = -1\n'
    ktjpt__brkz += 'elif arg0 > arg1:\n'
    ktjpt__brkz += '   res[i] = 1\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   res[i] = 0\n'
    ecxm__ahxrg = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    xnsj__pofc = ['source', 'delim', 'part']
    abrge__cdpr = [source, delim, part]
    miic__xptis = [True] * 3
    ktjpt__brkz = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    ktjpt__brkz += '   bodo.libs.array_kernels.setna(res, i)\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   tokens = []\n'
    ktjpt__brkz += "   buffer = ''\n"
    ktjpt__brkz += '   for j in range(len(arg0)):\n'
    ktjpt__brkz += '      if arg0[j] in arg1:\n'
    ktjpt__brkz += "         if buffer != '':"
    ktjpt__brkz += '            tokens.append(buffer)\n'
    ktjpt__brkz += "         buffer = ''\n"
    ktjpt__brkz += '      else:\n'
    ktjpt__brkz += '         buffer += arg0[j]\n'
    ktjpt__brkz += "   if buffer != '':\n"
    ktjpt__brkz += '      tokens.append(buffer)\n'
    ktjpt__brkz += '   if arg2 > len(tokens):\n'
    ktjpt__brkz += '      bodo.libs.array_kernels.setna(res, i)\n'
    ktjpt__brkz += '   else:\n'
    ktjpt__brkz += '      res[i] = tokens[arg2-1]\n'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    qodnh__lrvkj = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    ecxm__ahxrg = (bodo.string_array_type if qodnh__lrvkj else bodo.
        binary_array_type)
    xnsj__pofc = ['arr', 'start', 'length']
    abrge__cdpr = [arr, start, length]
    miic__xptis = [True] * 3
    ktjpt__brkz = 'if arg2 <= 0:\n'
    ktjpt__brkz += "   res[i] = ''\n" if qodnh__lrvkj else "   res[i] = b''\n"
    ktjpt__brkz += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    ktjpt__brkz += '   res[i] = arg0[arg1:]\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   if arg1 > 0: arg1 -= 1\n'
    ktjpt__brkz += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    xnsj__pofc = ['arr', 'delimiter', 'occurrences']
    abrge__cdpr = [arr, delimiter, occurrences]
    miic__xptis = [True] * 3
    ktjpt__brkz = "if arg1 == '' or arg2 == 0:\n"
    ktjpt__brkz += "   res[i] = ''\n"
    ktjpt__brkz += 'elif arg2 >= 0:\n'
    ktjpt__brkz += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    ktjpt__brkz += 'else:\n'
    ktjpt__brkz += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    xnsj__pofc = ['arr', 'source', 'target']
    abrge__cdpr = [arr, source, target]
    miic__xptis = [True] * 3
    ktjpt__brkz = "translated = ''\n"
    ktjpt__brkz += 'for char in arg0:\n'
    ktjpt__brkz += '   index = arg1.find(char)\n'
    ktjpt__brkz += '   if index == -1:\n'
    ktjpt__brkz += '      translated += char\n'
    ktjpt__brkz += '   elif index < len(arg2):\n'
    ktjpt__brkz += '      translated += arg2[index]\n'
    ktjpt__brkz += 'res[i] = translated'
    ecxm__ahxrg = bodo.string_array_type
    return gen_vectorized(xnsj__pofc, abrge__cdpr, miic__xptis, ktjpt__brkz,
        ecxm__ahxrg, may_cause_duplicate_dict_array_values=True)
