"""
Implements array kernels that are specific to BodoSQL. These kernels require special codegen
that cannot be done through the the normal gen_vectorized path
"""
import numpy as np
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import unopt_argument
from bodo.utils.typing import dtype_to_array_type, get_common_scalar_dtype, is_nullable, is_scalar_type, raise_bodo_error
from bodo.utils.utils import is_array_typ


def is_in(arr_to_check, arr_search_vals, is_parallel=False):
    pass


def is_in_util(arr_to_check, arr_search_vals, is_parallel=False):
    pass


@overload(is_in)
def is_in_overload(arr_to_check, arr_search_vals, is_parallel=False):
    args = [arr_to_check, arr_search_vals]
    for xsayk__qghyb in range(2):
        if isinstance(args[xsayk__qghyb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.is_in',
                ['arr_to_check', 'arr_search_vals', 'is_parallel=False'],
                xsayk__qghyb)

    def impl(arr_to_check, arr_search_vals, is_parallel=False):
        return is_in_util(arr_to_check, arr_search_vals, is_parallel)
    return impl


@overload(is_in_util)
def is_in_util_overload(arr_to_check, arr_search_vals, is_parallel=False):
    assert is_array_typ(arr_search_vals
        ), f"expected argument 'arr_search_vals' to be array type. Found: {arr_search_vals}"
    if arr_to_check == types.none:

        def impl(arr_to_check, arr_search_vals, is_parallel=False):
            return None
        return impl
    if arr_to_check == arr_search_vals:
        """If the types match, we don't have to do any casting, we can just use the array isin kernel"""

        def impl(arr_to_check, arr_search_vals, is_parallel=False):
            mhsth__llkz = len(arr_to_check)
            fgpu__qlgx = np.empty(mhsth__llkz, np.bool_)
            bodo.libs.array.array_isin(fgpu__qlgx, arr_to_check,
                arr_search_vals, is_parallel)
            bln__rvnh = bodo.libs.bool_arr_ext.alloc_bool_array(mhsth__llkz)
            for xsayk__qghyb in range(len(arr_to_check)):
                if bodo.libs.array_kernels.isna(arr_to_check, xsayk__qghyb):
                    bodo.libs.array_kernels.setna(bln__rvnh, xsayk__qghyb)
                else:
                    bln__rvnh[xsayk__qghyb] = fgpu__qlgx[xsayk__qghyb]
            return bln__rvnh
        return impl
    elif arr_to_check == bodo.dict_str_arr_type:
        """
        Special implementation to handle dict encoded arrays.
        In this case, instead of converting arr_to_check to regular string array, we convert
        arr_search_vals to dict encoded.
        This allows us to do a specialized implementation for
        array_isin c++.

        Test for this path can be found here:
        bodo/tests/bodosql_array_kernel_tests/test_bodosql_special_handling_array_kernels.py::test_is_in_dict_enc_string
        """
        assert arr_search_vals.dtype == bodo.string_type, 'Internal error: arr_to_check is dict encoded, but arr_search_vals does not have string dtype'

        def impl(arr_to_check, arr_search_vals, is_parallel=False):
            mhsth__llkz = len(arr_to_check)
            fgpu__qlgx = np.empty(mhsth__llkz, np.bool_)
            arr_search_vals = bodo.libs.str_arr_ext.str_arr_to_dict_str_arr(
                arr_search_vals)
            bodo.libs.array.array_isin(fgpu__qlgx, arr_to_check,
                arr_search_vals, is_parallel)
            bln__rvnh = bodo.libs.bool_arr_ext.alloc_bool_array(mhsth__llkz)
            for xsayk__qghyb in range(len(arr_to_check)):
                if bodo.libs.array_kernels.isna(arr_to_check, xsayk__qghyb):
                    bodo.libs.array_kernels.setna(bln__rvnh, xsayk__qghyb)
                else:
                    bln__rvnh[xsayk__qghyb] = fgpu__qlgx[xsayk__qghyb]
            return bln__rvnh
        return impl
    yet__owntf = arr_to_check.dtype if is_array_typ(arr_to_check
        ) else arr_to_check
    edo__vtuw = arr_search_vals.dtype
    hqxr__gxbre, hrgue__mafe = get_common_scalar_dtype([yet__owntf, edo__vtuw])
    assert hrgue__mafe, 'Internal error in is_in_util: arguments do not have a common scalar dtype'
    krnye__xdogk = is_nullable(arr_to_check) or is_nullable(arr_search_vals)
    if isinstance(hqxr__gxbre, types.Integer) and krnye__xdogk:
        hqxr__gxbre = bodo.libs.int_arr_ext.IntDtype(hqxr__gxbre)
    mrpuv__mcxk = dtype_to_array_type(hqxr__gxbre, krnye__xdogk)
    if krnye__xdogk:
        assert is_nullable(mrpuv__mcxk
            ), 'Internal error in is_in_util: unified_array_type is not nullable, but is required to be'
    if is_array_typ(arr_to_check):

        def impl(arr_to_check, arr_search_vals, is_parallel=False):
            mhsth__llkz = len(arr_to_check)
            fgpu__qlgx = np.empty(mhsth__llkz, np.bool_)
            arr_to_check = bodo.utils.conversion.fix_arr_dtype(arr_to_check,
                hqxr__gxbre, nan_to_str=False)
            arr_search_vals = bodo.utils.conversion.fix_arr_dtype(
                arr_search_vals, hqxr__gxbre, nan_to_str=False)
            bodo.libs.array.array_isin(fgpu__qlgx, arr_to_check,
                arr_search_vals, is_parallel)
            bln__rvnh = bodo.libs.bool_arr_ext.alloc_bool_array(mhsth__llkz)
            for xsayk__qghyb in range(len(arr_to_check)):
                if bodo.libs.array_kernels.isna(arr_to_check, xsayk__qghyb):
                    bodo.libs.array_kernels.setna(bln__rvnh, xsayk__qghyb)
                else:
                    bln__rvnh[xsayk__qghyb] = fgpu__qlgx[xsayk__qghyb]
            return bln__rvnh
        return impl
    elif is_scalar_type(arr_to_check):

        def impl(arr_to_check, arr_search_vals, is_parallel=False):
            arr_to_check = bodo.utils.conversion.fix_arr_dtype(bodo.utils.
                conversion.coerce_to_array(arr_to_check, scalar_to_arr_len=
                1, use_nullable_array=krnye__xdogk), hqxr__gxbre)
            fgpu__qlgx = np.empty(1, np.bool_)
            bodo.libs.array.array_isin(fgpu__qlgx, arr_to_check,
                arr_search_vals, is_parallel)
            return fgpu__qlgx[0]
        return impl
    else:
        raise_bodo_error(
            f'is_in_util expects array or scalar input for arg0. Found {arr_to_check}'
            )
