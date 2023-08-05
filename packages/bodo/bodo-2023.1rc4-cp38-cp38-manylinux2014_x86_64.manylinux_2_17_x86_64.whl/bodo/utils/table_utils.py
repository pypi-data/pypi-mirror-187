"""File containing utility functions for supporting DataFrame operations with Table Format."""
from collections import defaultdict
from typing import Any, Dict, Set
import numba
import numpy as np
from numba.core import types
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_castable_arr_dtype, get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, is_method,
    used_cols=None):
    if not is_overload_constant_str(func_name) and not is_overload_none(
        func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    if not is_overload_constant_bool(is_method):
        raise_bodo_error(
            'generate_mappable_table_func(): is_method must be a constant boolean'
            )
    vod__bzmuf = not is_overload_none(func_name)
    if vod__bzmuf:
        func_name = get_overload_const_str(func_name)
        hhj__ieo = get_overload_const_bool(is_method)
    mrh__yddx = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    vzxh__pbd = mrh__yddx == types.none
    wxaux__wqlfu = len(table.arr_types)
    if vzxh__pbd:
        eewd__cyi = table
    else:
        ysfu__kyj = tuple([mrh__yddx] * wxaux__wqlfu)
        eewd__cyi = TableType(ysfu__kyj)
    was__rrhy = {'bodo': bodo, 'lst_dtype': mrh__yddx, 'table_typ': eewd__cyi}
    yliw__pdw = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if vzxh__pbd:
        yliw__pdw += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        yliw__pdw += f'  l = len(table)\n'
    else:
        yliw__pdw += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({wxaux__wqlfu}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        too__yvvl = used_cols.instance_type
        lksxv__eps = np.array(too__yvvl.meta, dtype=np.int64)
        was__rrhy['used_cols_glbl'] = lksxv__eps
        tuc__vmp = set([table.block_nums[itcht__ogg] for itcht__ogg in
            lksxv__eps])
        yliw__pdw += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        yliw__pdw += f'  used_cols_set = None\n'
        lksxv__eps = None
    yliw__pdw += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for uqj__qeau in table.type_to_blk.values():
        yliw__pdw += f"""  blk_{uqj__qeau} = bodo.hiframes.table.get_table_block(table, {uqj__qeau})
"""
        if vzxh__pbd:
            yliw__pdw += f"""  out_list_{uqj__qeau} = bodo.hiframes.table.alloc_list_like(blk_{uqj__qeau}, len(blk_{uqj__qeau}), False)
"""
            zxm__lmuod = f'out_list_{uqj__qeau}'
        else:
            zxm__lmuod = 'out_list'
        if lksxv__eps is None or uqj__qeau in tuc__vmp:
            yliw__pdw += f'  for i in range(len(blk_{uqj__qeau})):\n'
            was__rrhy[f'col_indices_{uqj__qeau}'] = np.array(table.
                block_to_arr_ind[uqj__qeau], dtype=np.int64)
            yliw__pdw += f'    col_loc = col_indices_{uqj__qeau}[i]\n'
            if lksxv__eps is not None:
                yliw__pdw += f'    if col_loc not in used_cols_set:\n'
                yliw__pdw += f'        continue\n'
            if vzxh__pbd:
                aqj__qhu = 'i'
            else:
                aqj__qhu = 'col_loc'
            if not vod__bzmuf:
                yliw__pdw += (
                    f'    {zxm__lmuod}[{aqj__qhu}] = blk_{uqj__qeau}[i]\n')
            elif hhj__ieo:
                yliw__pdw += (
                    f'    {zxm__lmuod}[{aqj__qhu}] = blk_{uqj__qeau}[i].{func_name}()\n'
                    )
            else:
                yliw__pdw += (
                    f'    {zxm__lmuod}[{aqj__qhu}] = {func_name}(blk_{uqj__qeau}[i])\n'
                    )
        if vzxh__pbd:
            yliw__pdw += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {zxm__lmuod}, {uqj__qeau})
"""
    if vzxh__pbd:
        yliw__pdw += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        yliw__pdw += '  return out_table\n'
    else:
        yliw__pdw += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)\n'
            )
    jctcx__kzfsr = {}
    exec(yliw__pdw, was__rrhy, jctcx__kzfsr)
    return jctcx__kzfsr['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    sol__pqe = args[0]
    if equiv_set.has_shape(sol__pqe):
        return ArrayAnalysis.AnalyzeResult(shape=sol__pqe, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    was__rrhy = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.distributed_api
        .Reduce_Type.Sum.value)}
    yliw__pdw = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    yliw__pdw += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for uqj__qeau in table.type_to_blk.values():
        yliw__pdw += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {uqj__qeau})\n'
            )
        was__rrhy[f'col_indices_{uqj__qeau}'] = np.array(table.
            block_to_arr_ind[uqj__qeau], dtype=np.int64)
        yliw__pdw += '  for i in range(len(blk)):\n'
        yliw__pdw += f'    col_loc = col_indices_{uqj__qeau}[i]\n'
        yliw__pdw += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    yliw__pdw += '  if parallel:\n'
    yliw__pdw += '    for i in range(start_offset, len(out_arr)):\n'
    yliw__pdw += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    jctcx__kzfsr = {}
    exec(yliw__pdw, was__rrhy, jctcx__kzfsr)
    return jctcx__kzfsr['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    wvwwl__krao = table.type_to_blk[arr_type]
    was__rrhy: Dict[str, Any] = {'bodo': bodo}
    was__rrhy['col_indices'] = np.array(table.block_to_arr_ind[wvwwl__krao],
        dtype=np.int64)
    bevi__viqal = col_nums_meta.instance_type
    was__rrhy['col_nums'] = np.array(bevi__viqal.meta, np.int64)
    yliw__pdw = 'def impl(table, col_nums_meta, arr_type):\n'
    yliw__pdw += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {wvwwl__krao})\n')
    yliw__pdw += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    yliw__pdw += '  n = len(table)\n'
    smom__rvjty = arr_type == bodo.string_array_type
    if smom__rvjty:
        yliw__pdw += '  total_chars = 0\n'
        yliw__pdw += '  for c in col_nums:\n'
        yliw__pdw += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        yliw__pdw += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        yliw__pdw += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        yliw__pdw += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        yliw__pdw += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    yliw__pdw += '  for i in range(len(col_nums)):\n'
    yliw__pdw += '    c = col_nums[i]\n'
    if not smom__rvjty:
        yliw__pdw += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    yliw__pdw += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    yliw__pdw += '    off = i * n\n'
    yliw__pdw += '    for j in range(len(arr)):\n'
    yliw__pdw += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    yliw__pdw += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    yliw__pdw += '      else:\n'
    yliw__pdw += '        out_arr[off+j] = arr[j]\n'
    yliw__pdw += '  return out_arr\n'
    elflu__smbtk = {}
    exec(yliw__pdw, was__rrhy, elflu__smbtk)
    frtb__ibkav = elflu__smbtk['impl']
    return frtb__ibkav


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    ytmha__mjouw = not is_overload_false(copy)
    jhpv__wbb = is_overload_true(copy)
    was__rrhy: Dict[str, Any] = {'bodo': bodo}
    zkcs__uxbzx = table.arr_types
    uexj__bwjr = new_table_typ.arr_types
    dhg__pyno: Set[int] = set()
    tzsoz__tvicu: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    fkxl__usru: Set[types.Type] = set()
    for itcht__ogg, nqh__gkn in enumerate(zkcs__uxbzx):
        fixf__xyi = uexj__bwjr[itcht__ogg]
        if nqh__gkn == fixf__xyi:
            fkxl__usru.add(nqh__gkn)
        else:
            dhg__pyno.add(itcht__ogg)
            tzsoz__tvicu[fixf__xyi].add(nqh__gkn)
    yliw__pdw = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    yliw__pdw += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    yliw__pdw += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    viim__gdq = set(range(len(zkcs__uxbzx)))
    ujek__mwck = viim__gdq - dhg__pyno
    if not is_overload_none(used_cols):
        too__yvvl = used_cols.instance_type
        fextx__tdt = set(too__yvvl.meta)
        dhg__pyno = dhg__pyno & fextx__tdt
        ujek__mwck = ujek__mwck & fextx__tdt
        tuc__vmp = set([table.block_nums[itcht__ogg] for itcht__ogg in
            fextx__tdt])
    else:
        fextx__tdt = None
    ffeqq__dgd = dict()
    for ytt__lgwrl in dhg__pyno:
        ohyws__ylg = table.block_nums[ytt__lgwrl]
        qicj__nlrt = new_table_typ.block_nums[ytt__lgwrl]
        if f'cast_cols_{ohyws__ylg}_{qicj__nlrt}' in ffeqq__dgd:
            ffeqq__dgd[f'cast_cols_{ohyws__ylg}_{qicj__nlrt}'].append(
                ytt__lgwrl)
        else:
            ffeqq__dgd[f'cast_cols_{ohyws__ylg}_{qicj__nlrt}'] = [ytt__lgwrl]
    for kmbf__pkjiq in table.blk_to_type:
        for qicj__nlrt in new_table_typ.blk_to_type:
            jou__fqy = ffeqq__dgd.get(f'cast_cols_{kmbf__pkjiq}_{qicj__nlrt}',
                [])
            was__rrhy[f'cast_cols_{kmbf__pkjiq}_{qicj__nlrt}'] = np.array(list
                (jou__fqy), dtype=np.int64)
            yliw__pdw += f"""  cast_cols_{kmbf__pkjiq}_{qicj__nlrt}_set = set(cast_cols_{kmbf__pkjiq}_{qicj__nlrt})
"""
    was__rrhy['copied_cols'] = np.array(list(ujek__mwck), dtype=np.int64)
    yliw__pdw += f'  copied_cols_set = set(copied_cols)\n'
    for kbw__eszi, yno__qhcd in new_table_typ.type_to_blk.items():
        was__rrhy[f'typ_list_{yno__qhcd}'] = types.List(kbw__eszi)
        yliw__pdw += f"""  out_arr_list_{yno__qhcd} = bodo.hiframes.table.alloc_list_like(typ_list_{yno__qhcd}, {len(new_table_typ.block_to_arr_ind[yno__qhcd])}, False)
"""
        if kbw__eszi in fkxl__usru:
            mihjm__plgyu = table.type_to_blk[kbw__eszi]
            if fextx__tdt is None or mihjm__plgyu in tuc__vmp:
                cxjx__zzn = table.block_to_arr_ind[mihjm__plgyu]
                vghb__tseyf = [new_table_typ.block_offsets[dgijf__ktfvr] for
                    dgijf__ktfvr in cxjx__zzn]
                was__rrhy[f'new_idx_{mihjm__plgyu}'] = np.array(vghb__tseyf,
                    np.int64)
                was__rrhy[f'orig_arr_inds_{mihjm__plgyu}'] = np.array(cxjx__zzn
                    , np.int64)
                yliw__pdw += f"""  arr_list_{mihjm__plgyu} = bodo.hiframes.table.get_table_block(table, {mihjm__plgyu})
"""
                yliw__pdw += (
                    f'  for i in range(len(arr_list_{mihjm__plgyu})):\n')
                yliw__pdw += (
                    f'    arr_ind_{mihjm__plgyu} = orig_arr_inds_{mihjm__plgyu}[i]\n'
                    )
                yliw__pdw += (
                    f'    if arr_ind_{mihjm__plgyu} not in copied_cols_set:\n')
                yliw__pdw += f'      continue\n'
                yliw__pdw += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{mihjm__plgyu}, i, arr_ind_{mihjm__plgyu})
"""
                yliw__pdw += (
                    f'    out_idx_{yno__qhcd}_{mihjm__plgyu} = new_idx_{mihjm__plgyu}[i]\n'
                    )
                yliw__pdw += (
                    f'    arr_val_{mihjm__plgyu} = arr_list_{mihjm__plgyu}[i]\n'
                    )
                if jhpv__wbb:
                    yliw__pdw += (
                        f'    arr_val_{mihjm__plgyu} = arr_val_{mihjm__plgyu}.copy()\n'
                        )
                elif ytmha__mjouw:
                    yliw__pdw += f"""    arr_val_{mihjm__plgyu} = arr_val_{mihjm__plgyu}.copy() if copy else arr_val_{yno__qhcd}
"""
                yliw__pdw += f"""    out_arr_list_{yno__qhcd}[out_idx_{yno__qhcd}_{mihjm__plgyu}] = arr_val_{mihjm__plgyu}
"""
    orli__tov = set()
    for kbw__eszi, yno__qhcd in new_table_typ.type_to_blk.items():
        if kbw__eszi in tzsoz__tvicu:
            was__rrhy[f'typ_{yno__qhcd}'] = get_castable_arr_dtype(kbw__eszi)
            nuwz__boeeb = tzsoz__tvicu[kbw__eszi]
            for zvut__mkbn in nuwz__boeeb:
                mihjm__plgyu = table.type_to_blk[zvut__mkbn]
                if fextx__tdt is None or mihjm__plgyu in tuc__vmp:
                    if (zvut__mkbn not in fkxl__usru and zvut__mkbn not in
                        orli__tov):
                        cxjx__zzn = table.block_to_arr_ind[mihjm__plgyu]
                        vghb__tseyf = [new_table_typ.block_offsets[
                            dgijf__ktfvr] for dgijf__ktfvr in cxjx__zzn]
                        was__rrhy[f'new_idx_{mihjm__plgyu}'] = np.array(
                            vghb__tseyf, np.int64)
                        was__rrhy[f'orig_arr_inds_{mihjm__plgyu}'] = np.array(
                            cxjx__zzn, np.int64)
                        yliw__pdw += f"""  arr_list_{mihjm__plgyu} = bodo.hiframes.table.get_table_block(table, {mihjm__plgyu})
"""
                    orli__tov.add(zvut__mkbn)
                    yliw__pdw += (
                        f'  for i in range(len(arr_list_{mihjm__plgyu})):\n')
                    yliw__pdw += (
                        f'    arr_ind_{mihjm__plgyu} = orig_arr_inds_{mihjm__plgyu}[i]\n'
                        )
                    yliw__pdw += f"""    if arr_ind_{mihjm__plgyu} not in cast_cols_{mihjm__plgyu}_{yno__qhcd}_set:
"""
                    yliw__pdw += f'      continue\n'
                    yliw__pdw += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{mihjm__plgyu}, i, arr_ind_{mihjm__plgyu})
"""
                    yliw__pdw += f"""    out_idx_{yno__qhcd}_{mihjm__plgyu} = new_idx_{mihjm__plgyu}[i]
"""
                    yliw__pdw += f"""    arr_val_{yno__qhcd} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{mihjm__plgyu}[i], typ_{yno__qhcd}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    yliw__pdw += f"""    out_arr_list_{yno__qhcd}[out_idx_{yno__qhcd}_{mihjm__plgyu}] = arr_val_{yno__qhcd}
"""
        yliw__pdw += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{yno__qhcd}, {yno__qhcd})
"""
    yliw__pdw += '  return out_table\n'
    jctcx__kzfsr = {}
    exec(yliw__pdw, was__rrhy, jctcx__kzfsr)
    return jctcx__kzfsr['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    sol__pqe = args[0]
    if equiv_set.has_shape(sol__pqe):
        return ArrayAnalysis.AnalyzeResult(shape=sol__pqe, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
