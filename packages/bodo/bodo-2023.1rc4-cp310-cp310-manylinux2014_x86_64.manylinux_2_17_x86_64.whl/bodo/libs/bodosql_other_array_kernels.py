"""
Implements miscellaneous array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


@numba.generated_jit(nopython=True)
def booland(A, B):
    args = [A, B]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], klfq__cfhrv)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], klfq__cfhrv)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], klfq__cfhrv)

    def impl(A, B):
        return boolxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.boolnot_util',
            ['A'], 0)

    def impl(A):
        return boolnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def cond(arr, ifbranch, elsebranch):
    args = [arr, ifbranch, elsebranch]
    for klfq__cfhrv in range(3):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], klfq__cfhrv)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], klfq__cfhrv)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    bkd__eihx = ['A', 'B']
    pcpd__rky = [A, B]
    sxws__dkf = [False] * 2
    if A == bodo.none:
        sxws__dkf = [False, True]
        ixuu__lascu = 'if arg1 != 0:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = False\n'
    elif B == bodo.none:
        sxws__dkf = [True, False]
        ixuu__lascu = 'if arg0 != 0:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ixuu__lascu = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += 'else:\n'
            ixuu__lascu += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            ixuu__lascu = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += 'else:\n'
            ixuu__lascu += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        ixuu__lascu = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        ixuu__lascu = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    yhozv__ghen = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    bkd__eihx = ['A', 'B']
    pcpd__rky = [A, B]
    sxws__dkf = [False] * 2
    if A == bodo.none:
        sxws__dkf = [False, True]
        ixuu__lascu = 'if arg1 == 0:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = True\n'
    elif B == bodo.none:
        sxws__dkf = [True, False]
        ixuu__lascu = 'if arg0 == 0:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ixuu__lascu = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ixuu__lascu += '   res[i] = True\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            ixuu__lascu += '   res[i] = True\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += 'else:\n'
            ixuu__lascu += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            ixuu__lascu = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            ixuu__lascu += '   res[i] = True\n'
            ixuu__lascu += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += 'else:\n'
            ixuu__lascu += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        ixuu__lascu = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        ixuu__lascu += '   res[i] = True\n'
        ixuu__lascu += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        ixuu__lascu = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    yhozv__ghen = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    bkd__eihx = ['A', 'B']
    pcpd__rky = [A, B]
    sxws__dkf = [True] * 2
    ixuu__lascu = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    yhozv__ghen = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    bkd__eihx = ['A']
    pcpd__rky = [A]
    sxws__dkf = [True]
    ixuu__lascu = 'res[i] = arg0 == 0'
    yhozv__ghen = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], klfq__cfhrv)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], klfq__cfhrv)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for klfq__cfhrv in range(2):
        if isinstance(args[klfq__cfhrv], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], klfq__cfhrv)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    bkd__eihx = ['arr', 'ifbranch', 'elsebranch']
    pcpd__rky = [arr, ifbranch, elsebranch]
    sxws__dkf = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        ixuu__lascu = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        ixuu__lascu = 'if arg0:\n'
    else:
        ixuu__lascu = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            ixuu__lascu += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            ixuu__lascu += '      bodo.libs.array_kernels.setna(res, i)\n'
            ixuu__lascu += '   else:\n'
            ixuu__lascu += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            ixuu__lascu += '   res[i] = arg1\n'
        ixuu__lascu += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        ixuu__lascu += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        ixuu__lascu += '      bodo.libs.array_kernels.setna(res, i)\n'
        ixuu__lascu += '   else:\n'
        ixuu__lascu += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        ixuu__lascu += '   res[i] = arg2\n'
    yhozv__ghen = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    bkd__eihx = ['A', 'B']
    pcpd__rky = [A, B]
    sxws__dkf = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            ixuu__lascu = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            ixuu__lascu = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            ixuu__lascu = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            ixuu__lascu = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            ixuu__lascu = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            ixuu__lascu = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            ixuu__lascu += '   res[i] = True\n'
            ixuu__lascu += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            ixuu__lascu += '   res[i] = False\n'
            ixuu__lascu += 'else:\n'
            ixuu__lascu += '   res[i] = arg0 == arg1'
        else:
            ixuu__lascu = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        ixuu__lascu = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        ixuu__lascu = 'res[i] = arg0 == arg1'
    yhozv__ghen = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    bkd__eihx = ['arr0', 'arr1']
    pcpd__rky = [arr0, arr1]
    sxws__dkf = [True, False]
    if arr1 == bodo.none:
        ixuu__lascu = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        ixuu__lascu = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        ixuu__lascu += '   res[i] = arg0\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        ixuu__lascu = 'if arg0 != arg1:\n'
        ixuu__lascu += '   res[i] = arg0\n'
        ixuu__lascu += 'else:\n'
        ixuu__lascu += '   bodo.libs.array_kernels.setna(res, i)'
    yhozv__ghen = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(bkd__eihx, pcpd__rky, sxws__dkf, ixuu__lascu,
        yhozv__ghen)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    bkd__eihx = ['y', 'x']
    pcpd__rky = [y, x]
    yrwb__mfr = [True] * 2
    ixuu__lascu = 'res[i] = arg1'
    yhozv__ghen = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(bkd__eihx, pcpd__rky, yrwb__mfr, ixuu__lascu,
        yhozv__ghen)
