"""
Implements array kernels that are specific to BodoSQL which have a variable
number of arguments
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import is_str_arr_type, raise_bodo_error


def coalesce(A):
    return


@overload(coalesce)
def overload_coalesce(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Coalesce argument must be a tuple')
    for hgjr__rcci in range(len(A)):
        if isinstance(A[hgjr__rcci], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=hgjr__rcci, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    elv__apfv = None
    skm__fel = []
    ixth__qbq = False
    for hgjr__rcci in range(len(A)):
        if A[hgjr__rcci] == bodo.none:
            skm__fel.append(hgjr__rcci)
        elif not bodo.utils.utils.is_array_typ(A[hgjr__rcci]):
            for vyx__uqlmu in range(hgjr__rcci + 1, len(A)):
                skm__fel.append(vyx__uqlmu)
                if bodo.utils.utils.is_array_typ(A[vyx__uqlmu]):
                    elv__apfv = f'A[{vyx__uqlmu}]'
                    ixth__qbq = True
            break
        else:
            ixth__qbq = True
    rwise__qwpt = [f'A{hgjr__rcci}' for hgjr__rcci in range(len(A)) if 
        hgjr__rcci not in skm__fel]
    zkcu__yhx = [A[hgjr__rcci] for hgjr__rcci in range(len(A)) if 
        hgjr__rcci not in skm__fel]
    kfpd__ynyq = get_common_broadcasted_type(zkcu__yhx, 'COALESCE')
    nri__flbzq = ixth__qbq and is_str_arr_type(kfpd__ynyq)
    neekj__ryew = [False] * (len(A) - len(skm__fel))
    ltnp__kiyo = False
    if nri__flbzq:
        ltnp__kiyo = True
        for vyx__uqlmu, hxege__yillj in enumerate(zkcu__yhx):
            ltnp__kiyo = ltnp__kiyo and (hxege__yillj == bodo.string_type or
                hxege__yillj == bodo.dict_str_arr_type or isinstance(
                hxege__yillj, bodo.SeriesType) and hxege__yillj.data ==
                bodo.dict_str_arr_type)
    zrw__tfnt = ''
    wme__hfr = True
    dcpd__vdzc = False
    dalo__fujoe = 0
    kwd__ddnbt = None
    if ltnp__kiyo:
        kwd__ddnbt = 'num_strings = 0\n'
        kwd__ddnbt += 'num_chars = 0\n'
        kwd__ddnbt += 'is_dict_global = True\n'
        for hgjr__rcci in range(len(A)):
            if hgjr__rcci in skm__fel:
                dalo__fujoe += 1
                continue
            elif zkcu__yhx[hgjr__rcci - dalo__fujoe] != bodo.string_type:
                kwd__ddnbt += (
                    f'old_indices{hgjr__rcci - dalo__fujoe} = A{hgjr__rcci}._indices\n'
                    )
                kwd__ddnbt += (
                    f'old_data{hgjr__rcci - dalo__fujoe} = A{hgjr__rcci}._data\n'
                    )
                kwd__ddnbt += f"""is_dict_global = is_dict_global and A{hgjr__rcci}._has_global_dictionary
"""
                kwd__ddnbt += (
                    f'index_offset{hgjr__rcci - dalo__fujoe} = num_strings\n')
                kwd__ddnbt += (
                    f'num_strings += len(old_data{hgjr__rcci - dalo__fujoe})\n'
                    )
                kwd__ddnbt += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{hgjr__rcci - dalo__fujoe})
"""
            else:
                kwd__ddnbt += f'num_strings += 1\n'
                kwd__ddnbt += (
                    f'num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{hgjr__rcci})\n'
                    )
    dalo__fujoe = 0
    for hgjr__rcci in range(len(A)):
        if hgjr__rcci in skm__fel:
            dalo__fujoe += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[hgjr__rcci]):
            zhlqf__tbygl = 'if' if wme__hfr else 'elif'
            zrw__tfnt += (
                f'{zhlqf__tbygl} not bodo.libs.array_kernels.isna(A{hgjr__rcci}, i):\n'
                )
            if ltnp__kiyo:
                zrw__tfnt += f"""   res[i] = old_indices{hgjr__rcci - dalo__fujoe}[i] + index_offset{hgjr__rcci - dalo__fujoe}
"""
            elif nri__flbzq:
                zrw__tfnt += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{hgjr__rcci}, i)
"""
            else:
                zrw__tfnt += f'   res[i] = arg{hgjr__rcci - dalo__fujoe}\n'
            wme__hfr = False
        else:
            assert not dcpd__vdzc, 'should not encounter more than one scalar due to dead column pruning'
            ffwf__frqpa = ''
            if not wme__hfr:
                zrw__tfnt += 'else:\n'
                ffwf__frqpa = '   '
            if ltnp__kiyo:
                zrw__tfnt += f'{ffwf__frqpa}res[i] = num_strings - 1\n'
            else:
                zrw__tfnt += (
                    f'{ffwf__frqpa}res[i] = arg{hgjr__rcci - dalo__fujoe}\n')
            dcpd__vdzc = True
            break
    if not dcpd__vdzc:
        if not wme__hfr:
            zrw__tfnt += 'else:\n'
            zrw__tfnt += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            zrw__tfnt += 'bodo.libs.array_kernels.setna(res, i)'
    jtx__ehka = None
    if ltnp__kiyo:
        dalo__fujoe = 0
        jtx__ehka = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        jtx__ehka += 'curr_index = 0\n'
        for hgjr__rcci in range(len(A)):
            if hgjr__rcci in skm__fel:
                dalo__fujoe += 1
            elif zkcu__yhx[hgjr__rcci - dalo__fujoe] != bodo.string_type:
                jtx__ehka += (
                    f'section_len = len(old_data{hgjr__rcci - dalo__fujoe})\n')
                jtx__ehka += f'for l in range(section_len):\n'
                jtx__ehka += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{hgjr__rcci - dalo__fujoe}, l)
"""
                jtx__ehka += f'curr_index += section_len\n'
            else:
                jtx__ehka += f'dict_data[curr_index] = A{hgjr__rcci}\n'
                jtx__ehka += f'curr_index += 1\n'
        jtx__ehka += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        jtx__ehka += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    nxpjb__gazku = 'A'
    vcc__zowr = {f'A{hgjr__rcci}': f'A[{hgjr__rcci}]' for hgjr__rcci in
        range(len(A)) if hgjr__rcci not in skm__fel}
    if ltnp__kiyo:
        kfpd__ynyq = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(rwise__qwpt, zkcu__yhx, neekj__ryew, zrw__tfnt,
        kfpd__ynyq, nxpjb__gazku, vcc__zowr, elv__apfv,
        support_dict_encoding=False, prefix_code=kwd__ddnbt, suffix_code=
        jtx__ehka, alloc_array_scalars=not nri__flbzq)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for hgjr__rcci in range(len(A)):
        if isinstance(A[hgjr__rcci], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=hgjr__rcci, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    rwise__qwpt = [f'A{hgjr__rcci}' for hgjr__rcci in range(len(A))]
    zkcu__yhx = [A[hgjr__rcci] for hgjr__rcci in range(len(A))]
    neekj__ryew = [False] * len(A)
    zrw__tfnt = ''
    for hgjr__rcci in range(1, len(A) - 1, 2):
        zhlqf__tbygl = 'if' if len(zrw__tfnt) == 0 else 'elif'
        if A[hgjr__rcci + 1] == bodo.none:
            nnoyo__rzbww = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[hgjr__rcci + 1]):
            nnoyo__rzbww = f"""   if bodo.libs.array_kernels.isna({rwise__qwpt[hgjr__rcci + 1]}, i):
"""
            nnoyo__rzbww += f'      bodo.libs.array_kernels.setna(res, i)\n'
            nnoyo__rzbww += f'   else:\n'
            nnoyo__rzbww += f'      res[i] = arg{hgjr__rcci + 1}\n'
        else:
            nnoyo__rzbww = f'   res[i] = arg{hgjr__rcci + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            hgjr__rcci]) or A[hgjr__rcci] == bodo.none):
            if A[hgjr__rcci] == bodo.none:
                zrw__tfnt += f'{zhlqf__tbygl} True:\n'
                zrw__tfnt += nnoyo__rzbww
                break
            else:
                zrw__tfnt += f"""{zhlqf__tbygl} bodo.libs.array_kernels.isna({rwise__qwpt[hgjr__rcci]}, i):
"""
                zrw__tfnt += nnoyo__rzbww
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[hgjr__rcci]):
                zrw__tfnt += f"""{zhlqf__tbygl} (bodo.libs.array_kernels.isna({rwise__qwpt[0]}, i) and bodo.libs.array_kernels.isna({rwise__qwpt[hgjr__rcci]}, i)) or (not bodo.libs.array_kernels.isna({rwise__qwpt[0]}, i) and not bodo.libs.array_kernels.isna({rwise__qwpt[hgjr__rcci]}, i) and arg0 == arg{hgjr__rcci}):
"""
                zrw__tfnt += nnoyo__rzbww
            elif A[hgjr__rcci] == bodo.none:
                zrw__tfnt += (
                    f'{zhlqf__tbygl} bodo.libs.array_kernels.isna({rwise__qwpt[0]}, i):\n'
                    )
                zrw__tfnt += nnoyo__rzbww
            else:
                zrw__tfnt += f"""{zhlqf__tbygl} (not bodo.libs.array_kernels.isna({rwise__qwpt[0]}, i)) and arg0 == arg{hgjr__rcci}:
"""
                zrw__tfnt += nnoyo__rzbww
        elif A[hgjr__rcci] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[hgjr__rcci]):
            zrw__tfnt += f"""{zhlqf__tbygl} (not bodo.libs.array_kernels.isna({rwise__qwpt[hgjr__rcci]}, i)) and arg0 == arg{hgjr__rcci}:
"""
            zrw__tfnt += nnoyo__rzbww
        else:
            zrw__tfnt += f'{zhlqf__tbygl} arg0 == arg{hgjr__rcci}:\n'
            zrw__tfnt += nnoyo__rzbww
    if len(zrw__tfnt) > 0:
        zrw__tfnt += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            zrw__tfnt += (
                f'   if bodo.libs.array_kernels.isna({rwise__qwpt[-1]}, i):\n')
            zrw__tfnt += '      bodo.libs.array_kernels.setna(res, i)\n'
            zrw__tfnt += '   else:\n'
        zrw__tfnt += f'      res[i] = arg{len(A) - 1}'
    else:
        zrw__tfnt += '   bodo.libs.array_kernels.setna(res, i)'
    nxpjb__gazku = 'A'
    vcc__zowr = {f'A{hgjr__rcci}': f'A[{hgjr__rcci}]' for hgjr__rcci in
        range(len(A))}
    if len(zkcu__yhx) % 2 == 0:
        boi__dsfar = [zkcu__yhx[0]] + zkcu__yhx[1:-1:2]
        igv__xog = zkcu__yhx[2::2] + [zkcu__yhx[-1]]
    else:
        boi__dsfar = [zkcu__yhx[0]] + zkcu__yhx[1::2]
        igv__xog = zkcu__yhx[2::2]
    vwnuy__kfjg = get_common_broadcasted_type(boi__dsfar, 'DECODE')
    kfpd__ynyq = get_common_broadcasted_type(igv__xog, 'DECODE')
    if kfpd__ynyq == bodo.none:
        kfpd__ynyq = vwnuy__kfjg
    dwedb__jpez = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in boi__dsfar and len(zkcu__yhx) % 2 == 1
    return gen_vectorized(rwise__qwpt, zkcu__yhx, neekj__ryew, zrw__tfnt,
        kfpd__ynyq, nxpjb__gazku, vcc__zowr, support_dict_encoding=dwedb__jpez)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for hgjr__rcci in range(len(A)):
        if isinstance(A[hgjr__rcci], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=hgjr__rcci, container_length
                =len(A))
    if isinstance(sep, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
            ['A', 'sep'], 1)

    def impl(A, sep):
        return concat_ws_util(A, sep)
    return impl


def concat_ws_util(A, sep):
    return


@overload(concat_ws_util, no_unliteral=True)
def overload_concat_ws_util(A, sep):
    if len(A) == 0:
        raise_bodo_error('Cannot concatenate 0 columns')
    rwise__qwpt = []
    zkcu__yhx = []
    for hgjr__rcci, ilbr__wkrsw in enumerate(A):
        vqcaw__ssfiv = f'A{hgjr__rcci}'
        verify_string_arg(ilbr__wkrsw, 'CONCAT_WS', vqcaw__ssfiv)
        rwise__qwpt.append(vqcaw__ssfiv)
        zkcu__yhx.append(ilbr__wkrsw)
    rwise__qwpt.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    zkcu__yhx.append(sep)
    neekj__ryew = [True] * len(rwise__qwpt)
    kfpd__ynyq = bodo.string_array_type
    nxpjb__gazku = 'A, sep'
    vcc__zowr = {f'A{hgjr__rcci}': f'A[{hgjr__rcci}]' for hgjr__rcci in
        range(len(A))}
    sccha__pjf = ','.join([f'arg{hgjr__rcci}' for hgjr__rcci in range(len(A))])
    zrw__tfnt = f'  res[i] = arg{len(A)}.join([{sccha__pjf}])\n'
    return gen_vectorized(rwise__qwpt, zkcu__yhx, neekj__ryew, zrw__tfnt,
        kfpd__ynyq, nxpjb__gazku, vcc__zowr)
