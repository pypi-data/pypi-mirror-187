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
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], fbhd__fayy)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], fbhd__fayy)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], fbhd__fayy)

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
    for fbhd__fayy in range(3):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], fbhd__fayy)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], fbhd__fayy)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    damx__pymf = ['A', 'B']
    khx__qsyw = [A, B]
    hegqi__vcrnt = [False] * 2
    if A == bodo.none:
        hegqi__vcrnt = [False, True]
        vlt__ary = 'if arg1 != 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = False\n'
    elif B == bodo.none:
        hegqi__vcrnt = [True, False]
        vlt__ary = 'if arg0 != 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            vlt__ary = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += 'else:\n'
            vlt__ary += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            vlt__ary = 'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n'
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += 'else:\n'
            vlt__ary += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        vlt__ary = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        vlt__ary = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    yeexm__vrdzg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    damx__pymf = ['A', 'B']
    khx__qsyw = [A, B]
    hegqi__vcrnt = [False] * 2
    if A == bodo.none:
        hegqi__vcrnt = [False, True]
        vlt__ary = 'if arg1 == 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = True\n'
    elif B == bodo.none:
        hegqi__vcrnt = [True, False]
        vlt__ary = 'if arg0 == 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            vlt__ary = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            vlt__ary += '   res[i] = True\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            vlt__ary += '   res[i] = True\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += 'else:\n'
            vlt__ary += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            vlt__ary = 'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n'
            vlt__ary += '   res[i] = True\n'
            vlt__ary += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += 'else:\n'
            vlt__ary += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        vlt__ary = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        vlt__ary += '   res[i] = True\n'
        vlt__ary += 'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        vlt__ary = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    yeexm__vrdzg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    damx__pymf = ['A', 'B']
    khx__qsyw = [A, B]
    hegqi__vcrnt = [True] * 2
    vlt__ary = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    yeexm__vrdzg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    damx__pymf = ['A']
    khx__qsyw = [A]
    hegqi__vcrnt = [True]
    vlt__ary = 'res[i] = arg0 == 0'
    yeexm__vrdzg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], fbhd__fayy)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], fbhd__fayy)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for fbhd__fayy in range(2):
        if isinstance(args[fbhd__fayy], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], fbhd__fayy)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    damx__pymf = ['arr', 'ifbranch', 'elsebranch']
    khx__qsyw = [arr, ifbranch, elsebranch]
    hegqi__vcrnt = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        vlt__ary = 'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n'
    elif arr != bodo.none:
        vlt__ary = 'if arg0:\n'
    else:
        vlt__ary = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            vlt__ary += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            vlt__ary += '      bodo.libs.array_kernels.setna(res, i)\n'
            vlt__ary += '   else:\n'
            vlt__ary += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            vlt__ary += '   res[i] = arg1\n'
        vlt__ary += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        vlt__ary += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        vlt__ary += '      bodo.libs.array_kernels.setna(res, i)\n'
        vlt__ary += '   else:\n'
        vlt__ary += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        vlt__ary += '   res[i] = arg2\n'
    yeexm__vrdzg = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    damx__pymf = ['A', 'B']
    khx__qsyw = [A, B]
    hegqi__vcrnt = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            vlt__ary = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            vlt__ary = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            vlt__ary = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            vlt__ary = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            vlt__ary = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            vlt__ary = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            vlt__ary += '   res[i] = True\n'
            vlt__ary += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            vlt__ary += '   res[i] = False\n'
            vlt__ary += 'else:\n'
            vlt__ary += '   res[i] = arg0 == arg1'
        else:
            vlt__ary = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        vlt__ary = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        vlt__ary = 'res[i] = arg0 == arg1'
    yeexm__vrdzg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    damx__pymf = ['arr0', 'arr1']
    khx__qsyw = [arr0, arr1]
    hegqi__vcrnt = [True, False]
    if arr1 == bodo.none:
        vlt__ary = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        vlt__ary = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        vlt__ary += '   res[i] = arg0\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        vlt__ary = 'if arg0 != arg1:\n'
        vlt__ary += '   res[i] = arg0\n'
        vlt__ary += 'else:\n'
        vlt__ary += '   bodo.libs.array_kernels.setna(res, i)'
    yeexm__vrdzg = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(damx__pymf, khx__qsyw, hegqi__vcrnt, vlt__ary,
        yeexm__vrdzg)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    damx__pymf = ['y', 'x']
    khx__qsyw = [y, x]
    khx__srhi = [True] * 2
    vlt__ary = 'res[i] = arg1'
    yeexm__vrdzg = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(damx__pymf, khx__qsyw, khx__srhi, vlt__ary,
        yeexm__vrdzg)
