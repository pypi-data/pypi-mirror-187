"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_bin_arr_type, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        aqs__fpom = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(aqs__fpom)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jcuwp__urlg = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, jcuwp__urlg)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        hftds__eldz, = args
        osfm__dniyz = signature.return_type
        peg__lorwp = cgutils.create_struct_proxy(osfm__dniyz)(context, builder)
        peg__lorwp.obj = hftds__eldz
        context.nrt.incref(builder, signature.args[0], hftds__eldz)
        return peg__lorwp._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data,
        ArrayItemArrayType) or is_bin_arr_type(S.data)):
        raise_bodo_error(
            'Series.str: input should be a series of string/binary or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_len_dict_impl(S_str):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(irt__uzj)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(irt__uzj, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(irt__uzj, pat
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(irt__uzj, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    orun__pxdcs = S_str.stype.data
    if (orun__pxdcs != string_array_split_view_type and not is_str_arr_type
        (orun__pxdcs)) and not isinstance(orun__pxdcs, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(orun__pxdcs, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(irt__uzj, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_get_array_impl
    if orun__pxdcs == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(irt__uzj)
            vmycy__qvlr = 0
            for mxme__qdjhf in numba.parfors.parfor.internal_prange(n):
                kyerx__ksea, kyerx__ksea, ifzy__anbrs = get_split_view_index(
                    irt__uzj, mxme__qdjhf, i)
                vmycy__qvlr += ifzy__anbrs
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, vmycy__qvlr)
            for vsn__fsw in numba.parfors.parfor.internal_prange(n):
                wrif__rjl, nxba__fah, ifzy__anbrs = get_split_view_index(
                    irt__uzj, vsn__fsw, i)
                if wrif__rjl == 0:
                    bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
                    zdg__czi = get_split_view_data_ptr(irt__uzj, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, vsn__fsw)
                    zdg__czi = get_split_view_data_ptr(irt__uzj, nxba__fah)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr, vsn__fsw,
                    zdg__czi, ifzy__anbrs)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(irt__uzj, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(irt__uzj)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(irt__uzj, vsn__fsw) or not len(
                irt__uzj[vsn__fsw]) > i >= -len(irt__uzj[vsn__fsw]):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            else:
                out_arr[vsn__fsw] = irt__uzj[vsn__fsw][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    orun__pxdcs = S_str.stype.data
    if (orun__pxdcs != string_array_split_view_type and orun__pxdcs !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        orun__pxdcs)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(mago__zhh)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            else:
                kyoi__oyhwu = mago__zhh[vsn__fsw]
                out_arr[vsn__fsw] = sep.join(kyoi__oyhwu)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(irt__uzj, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            nosx__lvkx = re.compile(pat, flags)
            suym__uclde = len(irt__uzj)
            out_arr = pre_alloc_string_array(suym__uclde, -1)
            for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
                if bodo.libs.array_kernels.isna(irt__uzj, vsn__fsw):
                    out_arr[vsn__fsw] = ''
                    bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
                    continue
                out_arr[vsn__fsw] = nosx__lvkx.sub(repl, irt__uzj[vsn__fsw])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(irt__uzj)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(suym__uclde, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(irt__uzj, vsn__fsw):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
                continue
            out_arr[vsn__fsw] = irt__uzj[vsn__fsw].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = pd.array(S.array, 'string')._str_contains(pat, case,
            flags, na, regex)
    return out_arr


@numba.njit
def series_match_regex(S, pat, case, flags, na):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_match(pat, case, flags, na)
    return out_arr


def is_regex_unsupported(pat):
    qol__zlcv = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(qau__ycmdq in pat) for qau__ycmdq in qol__zlcv])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    zsly__bwqui = re.IGNORECASE.value
    nkor__djwz = 'def impl(\n'
    nkor__djwz += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    nkor__djwz += '):\n'
    nkor__djwz += '  S = S_str._obj\n'
    nkor__djwz += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    nkor__djwz += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    nkor__djwz += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    nkor__djwz += '  l = len(arr)\n'
    nkor__djwz += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                nkor__djwz += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                nkor__djwz += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            nkor__djwz += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        nkor__djwz += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        nkor__djwz += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            nkor__djwz += '  upper_pat = pat.upper()\n'
        nkor__djwz += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        nkor__djwz += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        nkor__djwz += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        nkor__djwz += '      else: \n'
        if is_overload_true(case):
            nkor__djwz += '          out_arr[i] = pat in arr[i]\n'
        else:
            nkor__djwz += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    nkor__djwz += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ytq__jzbe = {}
    exec(nkor__djwz, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': zsly__bwqui, 'get_search_regex':
        get_search_regex}, ytq__jzbe)
    impl = ytq__jzbe['impl']
    return impl


@overload_method(SeriesStrMethodType, 'match', inline='always',
    no_unliteral=True)
def overload_str_method_match(S_str, pat, case=True, flags=0, na=np.nan):
    not_supported_arg_check('match', 'na', na, np.nan)
    str_arg_check('match', 'pat', pat)
    int_arg_check('match', 'flags', flags)
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.match(): 'case' argument should be a constant boolean")
    zsly__bwqui = re.IGNORECASE.value
    nkor__djwz = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    nkor__djwz += '        S = S_str._obj\n'
    nkor__djwz += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    nkor__djwz += '        l = len(arr)\n'
    nkor__djwz += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    nkor__djwz += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        nkor__djwz += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        nkor__djwz += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        nkor__djwz += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        nkor__djwz += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    nkor__djwz += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ytq__jzbe = {}
    exec(nkor__djwz, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': zsly__bwqui, 'get_search_regex':
        get_search_regex}, ytq__jzbe)
    impl = ytq__jzbe['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    nkor__djwz = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    nkor__djwz += '  S = S_str._obj\n'
    nkor__djwz += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    nkor__djwz += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    nkor__djwz += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    nkor__djwz += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        nkor__djwz += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(sfc__xpwcv ==
        bodo.dict_str_arr_type for sfc__xpwcv in others.data):
        nud__tuz = ', '.join(f'data{i}' for i in range(len(others.columns)))
        nkor__djwz += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {nud__tuz}), sep)\n'
            )
    else:
        vwor__ssggj = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        nkor__djwz += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        nkor__djwz += '  numba.parfors.parfor.init_prange()\n'
        nkor__djwz += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        nkor__djwz += f'      if {vwor__ssggj}:\n'
        nkor__djwz += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        nkor__djwz += '          continue\n'
        athkm__vigzs = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range
            (len(others.columns))])
        vejh__jyal = "''" if is_overload_none(sep) else 'sep'
        nkor__djwz += (
            f'      out_arr[i] = {vejh__jyal}.join([{athkm__vigzs}])\n')
    nkor__djwz += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ytq__jzbe = {}
    exec(nkor__djwz, {'bodo': bodo, 'numba': numba}, ytq__jzbe)
    impl = ytq__jzbe['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(irt__uzj, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        nosx__lvkx = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(suym__uclde, np.int64)
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(nosx__lvkx, mago__zhh[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_find_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(irt__uzj, sub, start, end
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(suym__uclde, np.int64)
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rfind_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(irt__uzj, sub, start,
                end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(suym__uclde, np.int64)
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'index', inline='always',
    no_unliteral=True)
def overload_str_method_index(S_str, sub, start=0, end=None):
    str_arg_check('index', 'sub', sub)
    int_arg_check('index', 'start', start)
    if not is_overload_none(end):
        int_arg_check('index', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_index_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(irt__uzj, sub, start,
                end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(suym__uclde, np.int64)
        numba.parfors.parfor.init_prange()
        quxp__nhroj = False
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].find(sub, start, end)
                if out_arr[i] == -1:
                    quxp__nhroj = True
        uksxr__evxj = 'substring not found' if quxp__nhroj else ''
        synchronize_error_njit('ValueError', uksxr__evxj)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'rindex', inline='always',
    no_unliteral=True)
def overload_str_method_rindex(S_str, sub, start=0, end=None):
    str_arg_check('rindex', 'sub', sub)
    int_arg_check('rindex', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rindex', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rindex_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(irt__uzj, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(suym__uclde, np.int64)
        numba.parfors.parfor.init_prange()
        quxp__nhroj = False
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    quxp__nhroj = True
        uksxr__evxj = 'substring not found' if quxp__nhroj else ''
        synchronize_error_njit('ValueError', uksxr__evxj)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            else:
                if stop is not None:
                    nmrgy__gvut = mago__zhh[vsn__fsw][stop:]
                else:
                    nmrgy__gvut = ''
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw][:start
                    ] + repl + nmrgy__gvut
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
                avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
                aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(irt__uzj,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    avw__bnbva, aqs__fpom)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            suym__uclde = len(mago__zhh)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde,
                -1)
            for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
                if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                    bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
                else:
                    out_arr[vsn__fsw] = mago__zhh[vsn__fsw] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return impl
    elif is_overload_constant_list(repeats):
        bbus__sminn = get_overload_const_list(repeats)
        cfnuy__jadx = all([isinstance(qua__qbk, int) for qua__qbk in
            bbus__sminn])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        cfnuy__jadx = True
    else:
        cfnuy__jadx = False
    if cfnuy__jadx:

        def impl(S_str, repeats):
            S = S_str._obj
            mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            xpo__vlcof = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            suym__uclde = len(mago__zhh)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde,
                -1)
            for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
                if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                    bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
                else:
                    out_arr[vsn__fsw] = mago__zhh[vsn__fsw] * xpo__vlcof[
                        vsn__fsw]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    nkor__djwz = f"""def dict_impl(S_str, width, fillchar=' '):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr, width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
def impl(S_str, width, fillchar=' '):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    numba.parfors.parfor.init_prange()
    l = len(str_arr)
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
    for j in numba.parfors.parfor.internal_prange(l):
        if bodo.libs.array_kernels.isna(str_arr, j):
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}(width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    ytq__jzbe = {}
    qxg__ynyyh = {'bodo': bodo, 'numba': numba}
    exec(nkor__djwz, qxg__ynyyh, ytq__jzbe)
    impl = ytq__jzbe['impl']
    por__rvo = ytq__jzbe['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return por__rvo
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for oabd__ftezi in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(oabd__ftezi)
        overload_method(SeriesStrMethodType, oabd__ftezi, inline='always',
            no_unliteral=True)(impl)


_install_ljust_rjust_center()


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_pad_dict_impl(S_str, width, side='left', fillchar=' '):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(irt__uzj, width,
                    fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(irt__uzj, width,
                    fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(irt__uzj, width,
                    fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            elif side == 'left':
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw].rjust(width, fillchar)
            elif side == 'right':
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw].ljust(width, fillchar)
            elif side == 'both':
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw].center(width, fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(irt__uzj, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            else:
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_slice_dict_impl(S_str, start=None, stop=None, step=None):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(irt__uzj, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(suym__uclde, -1)
        for vsn__fsw in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, vsn__fsw):
                out_arr[vsn__fsw] = ''
                bodo.libs.array_kernels.setna(out_arr, vsn__fsw)
            else:
                out_arr[vsn__fsw] = mago__zhh[vsn__fsw][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(irt__uzj, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(suym__uclde)
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
            avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
            aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(irt__uzj, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                avw__bnbva, aqs__fpom)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mago__zhh = bodo.hiframes.pd_series_ext.get_series_data(S)
        aqs__fpom = bodo.hiframes.pd_series_ext.get_series_name(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        suym__uclde = len(mago__zhh)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(suym__uclde)
        for i in numba.parfors.parfor.internal_prange(suym__uclde):
            if bodo.libs.array_kernels.isna(mago__zhh, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mago__zhh[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, avw__bnbva,
            aqs__fpom)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    vvqdh__pwz, regex = _get_column_names_from_regex(pat, flags, 'extract')
    xkzbw__zbehi = len(vvqdh__pwz)
    if S_str.stype.data == bodo.dict_str_arr_type:
        nkor__djwz = 'def impl(S_str, pat, flags=0, expand=True):\n'
        nkor__djwz += '  S = S_str._obj\n'
        nkor__djwz += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nkor__djwz += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nkor__djwz += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nkor__djwz += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {xkzbw__zbehi})
"""
        for i in range(xkzbw__zbehi):
            nkor__djwz += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        nkor__djwz = 'def impl(S_str, pat, flags=0, expand=True):\n'
        nkor__djwz += '  regex = re.compile(pat, flags=flags)\n'
        nkor__djwz += '  S = S_str._obj\n'
        nkor__djwz += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nkor__djwz += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nkor__djwz += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nkor__djwz += '  numba.parfors.parfor.init_prange()\n'
        nkor__djwz += '  n = len(str_arr)\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        nkor__djwz += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        nkor__djwz += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += "          out_arr_{}[j] = ''\n".format(i)
            nkor__djwz += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        nkor__djwz += '      else:\n'
        nkor__djwz += '          m = regex.search(str_arr[j])\n'
        nkor__djwz += '          if m:\n'
        nkor__djwz += '            g = m.groups()\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        nkor__djwz += '          else:\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += "            out_arr_{}[j] = ''\n".format(i)
            nkor__djwz += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        aqs__fpom = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        nkor__djwz += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(aqs__fpom))
        ytq__jzbe = {}
        exec(nkor__djwz, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, ytq__jzbe)
        impl = ytq__jzbe['impl']
        return impl
    gjuyw__inwtp = ', '.join('out_arr_{}'.format(i) for i in range(
        xkzbw__zbehi))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(nkor__djwz, vvqdh__pwz,
        gjuyw__inwtp, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    vvqdh__pwz, kyerx__ksea = _get_column_names_from_regex(pat, flags,
        'extractall')
    xkzbw__zbehi = len(vvqdh__pwz)
    xeq__wbpy = isinstance(S_str.stype.index, StringIndexType)
    pbsxf__aepkr = xkzbw__zbehi > 1
    gll__zgsm = '_multi' if pbsxf__aepkr else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        nkor__djwz = 'def impl(S_str, pat, flags=0):\n'
        nkor__djwz += '  S = S_str._obj\n'
        nkor__djwz += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nkor__djwz += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nkor__djwz += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nkor__djwz += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        nkor__djwz += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        nkor__djwz += '  regex = re.compile(pat, flags=flags)\n'
        nkor__djwz += '  out_ind_arr, out_match_arr, out_arr_list = '
        nkor__djwz += f'bodo.libs.dict_arr_ext.str_extractall{gll__zgsm}(\n'
        nkor__djwz += f'arr, regex, {xkzbw__zbehi}, index_arr)\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += f'  out_arr_{i} = out_arr_list[{i}]\n'
        nkor__djwz += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        nkor__djwz += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        nkor__djwz = 'def impl(S_str, pat, flags=0):\n'
        nkor__djwz += '  regex = re.compile(pat, flags=flags)\n'
        nkor__djwz += '  S = S_str._obj\n'
        nkor__djwz += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        nkor__djwz += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        nkor__djwz += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        nkor__djwz += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        nkor__djwz += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        nkor__djwz += '  numba.parfors.parfor.init_prange()\n'
        nkor__djwz += '  n = len(str_arr)\n'
        nkor__djwz += '  out_n_l = [0]\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += '  num_chars_{} = 0\n'.format(i)
        if xeq__wbpy:
            nkor__djwz += '  index_num_chars = 0\n'
        nkor__djwz += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if xeq__wbpy:
            nkor__djwz += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        nkor__djwz += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        nkor__djwz += '          continue\n'
        nkor__djwz += '      m = regex.findall(str_arr[i])\n'
        nkor__djwz += '      out_n_l[0] += len(m)\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += '      l_{} = 0\n'.format(i)
        nkor__djwz += '      for s in m:\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += '        l_{} += get_utf8_size(s{})\n'.format(i, 
                '[{}]'.format(i) if xkzbw__zbehi > 1 else '')
        for i in range(xkzbw__zbehi):
            nkor__djwz += '      num_chars_{0} += l_{0}\n'.format(i)
        nkor__djwz += (
            '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
            )
        for i in range(xkzbw__zbehi):
            nkor__djwz += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if xeq__wbpy:
            nkor__djwz += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            nkor__djwz += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        nkor__djwz += '  out_match_arr = np.empty(out_n, np.int64)\n'
        nkor__djwz += '  out_ind = 0\n'
        nkor__djwz += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        nkor__djwz += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        nkor__djwz += '          continue\n'
        nkor__djwz += '      m = regex.findall(str_arr[j])\n'
        nkor__djwz += '      for k, s in enumerate(m):\n'
        for i in range(xkzbw__zbehi):
            nkor__djwz += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if xkzbw__zbehi > 1 else ''))
        nkor__djwz += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        nkor__djwz += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        nkor__djwz += '        out_ind += 1\n'
        nkor__djwz += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        nkor__djwz += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    gjuyw__inwtp = ', '.join('out_arr_{}'.format(i) for i in range(
        xkzbw__zbehi))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(nkor__djwz, vvqdh__pwz,
        gjuyw__inwtp, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    anlm__ksyu = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    vvqdh__pwz = [anlm__ksyu.get(1 + i, i) for i in range(regex.groups)]
    return vvqdh__pwz, regex


def create_str2str_methods_overload(func_name):
    hmwuz__iojnn = func_name in ['lstrip', 'rstrip', 'strip']
    nkor__djwz = f"""def f({'S_str, to_strip=None' if hmwuz__iojnn else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if hmwuz__iojnn else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if hmwuz__iojnn else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    nkor__djwz += f"""def _dict_impl({'S_str, to_strip=None' if hmwuz__iojnn else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if hmwuz__iojnn else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    ytq__jzbe = {}
    exec(nkor__djwz, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, ytq__jzbe)
    dbn__jhbh = ytq__jzbe['f']
    ykq__iuc = ytq__jzbe['_dict_impl']
    if hmwuz__iojnn:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return ykq__iuc
            return dbn__jhbh
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return ykq__iuc
            return dbn__jhbh
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    nkor__djwz = 'def dict_impl(S_str):\n'
    nkor__djwz += '    S = S_str._obj\n'
    nkor__djwz += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    nkor__djwz += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    nkor__djwz += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    nkor__djwz += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    nkor__djwz += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nkor__djwz += 'def impl(S_str):\n'
    nkor__djwz += '    S = S_str._obj\n'
    nkor__djwz += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    nkor__djwz += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    nkor__djwz += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    nkor__djwz += '    numba.parfors.parfor.init_prange()\n'
    nkor__djwz += '    l = len(str_arr)\n'
    nkor__djwz += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    nkor__djwz += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    nkor__djwz += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    nkor__djwz += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    nkor__djwz += '        else:\n'
    nkor__djwz += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    nkor__djwz += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    nkor__djwz += '      out_arr,index, name)\n'
    ytq__jzbe = {}
    exec(nkor__djwz, {'bodo': bodo, 'numba': numba, 'np': np}, ytq__jzbe)
    impl = ytq__jzbe['impl']
    por__rvo = ytq__jzbe['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return por__rvo
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for gcnlw__yxvtf in bodo.hiframes.pd_series_ext.str2str_methods:
        knrj__elqjo = create_str2str_methods_overload(gcnlw__yxvtf)
        overload_method(SeriesStrMethodType, gcnlw__yxvtf, inline='always',
            no_unliteral=True)(knrj__elqjo)


def _install_str2bool_methods():
    for gcnlw__yxvtf in bodo.hiframes.pd_series_ext.str2bool_methods:
        knrj__elqjo = create_str2bool_methods_overload(gcnlw__yxvtf)
        overload_method(SeriesStrMethodType, gcnlw__yxvtf, inline='always',
            no_unliteral=True)(knrj__elqjo)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        aqs__fpom = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(aqs__fpom)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jcuwp__urlg = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, jcuwp__urlg)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        hftds__eldz, = args
        ihlsu__tkjnd = signature.return_type
        eoi__igjj = cgutils.create_struct_proxy(ihlsu__tkjnd)(context, builder)
        eoi__igjj.obj = hftds__eldz
        context.nrt.incref(builder, signature.args[0], hftds__eldz)
        return eoi__igjj._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        irt__uzj = bodo.hiframes.pd_series_ext.get_series_data(S)
        avw__bnbva = bodo.hiframes.pd_series_ext.get_series_index(S)
        aqs__fpom = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(irt__uzj),
            avw__bnbva, aqs__fpom)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for fkk__rzno in unsupported_cat_attrs:
        iuewt__soy = 'Series.cat.' + fkk__rzno
        overload_attribute(SeriesCatMethodType, fkk__rzno)(
            create_unsupported_overload(iuewt__soy))
    for dnmgx__whvs in unsupported_cat_methods:
        iuewt__soy = 'Series.cat.' + dnmgx__whvs
        overload_method(SeriesCatMethodType, dnmgx__whvs)(
            create_unsupported_overload(iuewt__soy))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for dnmgx__whvs in unsupported_str_methods:
        iuewt__soy = 'Series.str.' + dnmgx__whvs
        overload_method(SeriesStrMethodType, dnmgx__whvs)(
            create_unsupported_overload(iuewt__soy))


_install_strseries_unsupported()
