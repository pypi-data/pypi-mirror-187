"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    cheld__auvx = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for ewt__omql in cheld__auvx:
        pattern = pattern.replace(ewt__omql, cheld__auvx[ewt__omql])
    return pattern


def make_flag_bitvector(flags):
    vswu__pieu = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            vswu__pieu = vswu__pieu | re.I
    if 'm' in flags:
        vswu__pieu = vswu__pieu | re.M
    if 's' in flags:
        vswu__pieu = vswu__pieu | re.S
    return vswu__pieu


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for ohmy__tlncn in range(4):
        if isinstance(args[ohmy__tlncn], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], ohmy__tlncn)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for ohmy__tlncn in range(7):
        if isinstance(args[ohmy__tlncn], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], ohmy__tlncn)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for ohmy__tlncn in range(3):
        if isinstance(args[ohmy__tlncn], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], ohmy__tlncn)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for ohmy__tlncn in range(6):
        if isinstance(args[ohmy__tlncn], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], ohmy__tlncn)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for ohmy__tlncn in range(6):
        if isinstance(args[ohmy__tlncn], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                ohmy__tlncn)

    def impl(arr, pattern, position, occurrence, flags, group):
        return regexp_substr_util(arr, numba.literally(pattern), position,
            occurrence, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_count_util(arr, pattern, position, flags):
    verify_string_arg(arr, 'REGEXP_COUNT', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_COUNT', 'pattern')
    verify_int_arg(position, 'REGEXP_COUNT', 'position')
    verify_scalar_string_arg(flags, 'REGEXP_COUNT', 'flags')
    yie__ukbjo = ['arr', 'pattern', 'position', 'flags']
    duul__supco = [arr, pattern, position, flags]
    xqsc__nnzvd = [True] * 4
    phsej__ktok = bodo.utils.typing.get_overload_const_str(pattern)
    vjbn__wow = posix_to_re(phsej__ktok)
    xmhg__rxxs = bodo.utils.typing.get_overload_const_str(flags)
    vcfgj__pgrsx = make_flag_bitvector(xmhg__rxxs)
    efrn__ponvc = '\n'
    xaxu__pys = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xaxu__pys += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        efrn__ponvc += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if vjbn__wow == '':
        xaxu__pys += 'res[i] = 0'
    else:
        efrn__ponvc += f'r = re.compile({repr(vjbn__wow)}, {vcfgj__pgrsx})'
        xaxu__pys += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    dyivl__bsfo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(yie__ukbjo, duul__supco, xqsc__nnzvd, xaxu__pys,
        dyivl__bsfo, prefix_code=efrn__ponvc)


@numba.generated_jit(nopython=True)
def regexp_instr_util(arr, pattern, position, occurrence, option, flags, group
    ):
    verify_string_arg(arr, 'REGEXP_INSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_INSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_INSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_INSTR', 'occurrence')
    verify_int_arg(option, 'REGEXP_INSTR', 'option')
    verify_scalar_string_arg(flags, 'REGEXP_INSTR', 'flags')
    verify_int_arg(group, 'REGEXP_INSTR', 'group')
    yie__ukbjo = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    duul__supco = [arr, pattern, position, occurrence, option, flags, group]
    xqsc__nnzvd = [True] * 7
    phsej__ktok = bodo.utils.typing.get_overload_const_str(pattern)
    vjbn__wow = posix_to_re(phsej__ktok)
    tlr__eavm = re.compile(phsej__ktok).groups
    xmhg__rxxs = bodo.utils.typing.get_overload_const_str(flags)
    vcfgj__pgrsx = make_flag_bitvector(xmhg__rxxs)
    efrn__ponvc = '\n'
    xaxu__pys = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xaxu__pys += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        efrn__ponvc += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xaxu__pys += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        efrn__ponvc += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        xaxu__pys += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        efrn__ponvc += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in xmhg__rxxs:
        if bodo.utils.utils.is_array_typ(group, True):
            xaxu__pys += f"""if not (1 <= arg6 <= {tlr__eavm}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            efrn__ponvc += f"""if not (1 <= group <= {tlr__eavm}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if vjbn__wow == '':
        xaxu__pys += 'res[i] = 0'
    else:
        efrn__ponvc += f'r = re.compile({repr(vjbn__wow)}, {vcfgj__pgrsx})'
        xaxu__pys += 'arg0 = arg0[arg2-1:]\n'
        xaxu__pys += 'res[i] = 0\n'
        xaxu__pys += 'offset = arg2\n'
        xaxu__pys += 'for j in range(arg3):\n'
        xaxu__pys += '   match = r.search(arg0)\n'
        xaxu__pys += '   if match is None:\n'
        xaxu__pys += '      res[i] = 0\n'
        xaxu__pys += '      break\n'
        xaxu__pys += '   start, end = match.span()\n'
        xaxu__pys += '   if j == arg3 - 1:\n'
        if 'e' in xmhg__rxxs:
            xaxu__pys += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            xaxu__pys += '      res[i] = offset + match.span()[arg4]\n'
        xaxu__pys += '   else:\n'
        xaxu__pys += '      offset += end\n'
        xaxu__pys += '      arg0 = arg0[end:]\n'
    dyivl__bsfo = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(yie__ukbjo, duul__supco, xqsc__nnzvd, xaxu__pys,
        dyivl__bsfo, prefix_code=efrn__ponvc)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    yie__ukbjo = ['arr', 'pattern', 'flags']
    duul__supco = [arr, pattern, flags]
    xqsc__nnzvd = [True] * 3
    phsej__ktok = bodo.utils.typing.get_overload_const_str(pattern)
    vjbn__wow = posix_to_re(phsej__ktok)
    xmhg__rxxs = bodo.utils.typing.get_overload_const_str(flags)
    vcfgj__pgrsx = make_flag_bitvector(xmhg__rxxs)
    if vjbn__wow == '':
        efrn__ponvc = None
        xaxu__pys = 'res[i] = len(arg0) == 0'
    else:
        efrn__ponvc = f'r = re.compile({repr(vjbn__wow)}, {vcfgj__pgrsx})'
        xaxu__pys = 'if r.fullmatch(arg0) is None:\n'
        xaxu__pys += '   res[i] = False\n'
        xaxu__pys += 'else:\n'
        xaxu__pys += '   res[i] = True\n'
    dyivl__bsfo = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(yie__ukbjo, duul__supco, xqsc__nnzvd, xaxu__pys,
        dyivl__bsfo, prefix_code=efrn__ponvc)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    yie__ukbjo = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    duul__supco = [arr, pattern, replacement, position, occurrence, flags]
    xqsc__nnzvd = [True] * 6
    phsej__ktok = bodo.utils.typing.get_overload_const_str(pattern)
    vjbn__wow = posix_to_re(phsej__ktok)
    xmhg__rxxs = bodo.utils.typing.get_overload_const_str(flags)
    vcfgj__pgrsx = make_flag_bitvector(xmhg__rxxs)
    efrn__ponvc = '\n'
    xaxu__pys = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xaxu__pys += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        efrn__ponvc += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xaxu__pys += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        efrn__ponvc += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if vjbn__wow == '':
        xaxu__pys += 'res[i] = arg0'
    else:
        efrn__ponvc += f'r = re.compile({repr(vjbn__wow)}, {vcfgj__pgrsx})'
        xaxu__pys += 'result = arg0[:arg3-1]\n'
        xaxu__pys += 'arg0 = arg0[arg3-1:]\n'
        xaxu__pys += 'if arg4 == 0:\n'
        xaxu__pys += '   res[i] = result + r.sub(arg2, arg0)\n'
        xaxu__pys += 'else:\n'
        xaxu__pys += '   nomatch = False\n'
        xaxu__pys += '   for j in range(arg4 - 1):\n'
        xaxu__pys += '      match = r.search(arg0)\n'
        xaxu__pys += '      if match is None:\n'
        xaxu__pys += '         res[i] = result + arg0\n'
        xaxu__pys += '         nomatch = True\n'
        xaxu__pys += '         break\n'
        xaxu__pys += '      _, end = match.span()\n'
        xaxu__pys += '      result += arg0[:end]\n'
        xaxu__pys += '      arg0 = arg0[end:]\n'
        xaxu__pys += '   if nomatch == False:\n'
        xaxu__pys += '      result += r.sub(arg2, arg0, count=1)\n'
        xaxu__pys += '      res[i] = result'
    dyivl__bsfo = bodo.string_array_type
    return gen_vectorized(yie__ukbjo, duul__supco, xqsc__nnzvd, xaxu__pys,
        dyivl__bsfo, prefix_code=efrn__ponvc)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    yie__ukbjo = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    duul__supco = [arr, pattern, position, occurrence, flags, group]
    xqsc__nnzvd = [True] * 6
    phsej__ktok = bodo.utils.typing.get_overload_const_str(pattern)
    vjbn__wow = posix_to_re(phsej__ktok)
    tlr__eavm = re.compile(phsej__ktok).groups
    xmhg__rxxs = bodo.utils.typing.get_overload_const_str(flags)
    vcfgj__pgrsx = make_flag_bitvector(xmhg__rxxs)
    efrn__ponvc = '\n'
    xaxu__pys = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xaxu__pys += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        efrn__ponvc += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xaxu__pys += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        efrn__ponvc += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in xmhg__rxxs:
        if bodo.utils.utils.is_array_typ(group, True):
            xaxu__pys += f"""if not (1 <= arg5 <= {tlr__eavm}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            efrn__ponvc += f"""if not (1 <= group <= {tlr__eavm}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if vjbn__wow == '':
        xaxu__pys += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        efrn__ponvc += f'r = re.compile({repr(vjbn__wow)}, {vcfgj__pgrsx})'
        if 'e' in xmhg__rxxs:
            xaxu__pys += 'matches = r.findall(arg0[arg2-1:])\n'
            xaxu__pys += f'if len(matches) < arg3:\n'
            xaxu__pys += '   bodo.libs.array_kernels.setna(res, i)\n'
            xaxu__pys += 'else:\n'
            if tlr__eavm == 1:
                xaxu__pys += '   res[i] = matches[arg3-1]\n'
            else:
                xaxu__pys += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            xaxu__pys += 'arg0 = str(arg0)[arg2-1:]\n'
            xaxu__pys += 'for j in range(arg3):\n'
            xaxu__pys += '   match = r.search(arg0)\n'
            xaxu__pys += '   if match is None:\n'
            xaxu__pys += '      bodo.libs.array_kernels.setna(res, i)\n'
            xaxu__pys += '      break\n'
            xaxu__pys += '   start, end = match.span()\n'
            xaxu__pys += '   if j == arg3 - 1:\n'
            xaxu__pys += '      res[i] = arg0[start:end]\n'
            xaxu__pys += '   else:\n'
            xaxu__pys += '      arg0 = arg0[end:]\n'
    dyivl__bsfo = bodo.string_array_type
    return gen_vectorized(yie__ukbjo, duul__supco, xqsc__nnzvd, xaxu__pys,
        dyivl__bsfo, prefix_code=efrn__ponvc)
