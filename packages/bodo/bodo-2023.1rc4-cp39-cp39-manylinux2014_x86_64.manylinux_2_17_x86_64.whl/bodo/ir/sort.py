"""IR node for the data sorting"""
from collections import defaultdict
from typing import List, Set, Tuple, Union
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_data_to_cpp_table, sort_values_table
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import MetaType, is_overload_none, type_has_unknown_cats
from bodo.utils.utils import gen_getitem


class Sort(ir.Stmt):

    def __init__(self, df_in: str, df_out: str, in_vars: List[ir.Var],
        out_vars: List[ir.Var], key_inds: Tuple[int], inplace: bool, loc:
        ir.Loc, ascending_list: Union[List[bool], bool]=True, na_position:
        Union[List[str], str]='last', _bodo_chunk_bounds: Union[ir.Var,
        None]=None, is_table_format: bool=False, num_table_arrays: int=0):
        self.df_in = df_in
        self.df_out = df_out
        self.in_vars = in_vars
        self.out_vars = out_vars
        self.key_inds = key_inds
        self.inplace = inplace
        self._bodo_chunk_bounds = _bodo_chunk_bounds
        self.is_table_format = is_table_format
        self.num_table_arrays = num_table_arrays
        self.dead_var_inds: Set[int] = set()
        self.dead_key_var_inds: Set[int] = set()
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_inds)
            else:
                self.na_position_b = (False,) * len(key_inds)
        else:
            self.na_position_b = tuple([(True if iuf__ropbf == 'last' else 
                False) for iuf__ropbf in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [yptqx__lyeoq for yptqx__lyeoq in self.in_vars if 
            yptqx__lyeoq is not None]

    def get_live_out_vars(self):
        return [yptqx__lyeoq for yptqx__lyeoq in self.out_vars if 
            yptqx__lyeoq is not None]

    def __repr__(self):
        hrsgm__jhukp = ', '.join(yptqx__lyeoq.name for yptqx__lyeoq in self
            .get_live_in_vars())
        swhow__smuw = f'{self.df_in}{{{hrsgm__jhukp}}}'
        stbx__zat = ', '.join(yptqx__lyeoq.name for yptqx__lyeoq in self.
            get_live_out_vars())
        oazvw__vugfp = f'{self.df_out}{{{stbx__zat}}}'
        return f'Sort (keys: {self.key_inds}): {swhow__smuw} {oazvw__vugfp}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    iued__ekalf = []
    for qky__fxyi in sort_node.get_live_in_vars():
        lazbf__wegg = equiv_set.get_shape(qky__fxyi)
        if lazbf__wegg is not None:
            iued__ekalf.append(lazbf__wegg[0])
    if len(iued__ekalf) > 1:
        equiv_set.insert_equiv(*iued__ekalf)
    blx__race = []
    iued__ekalf = []
    for qky__fxyi in sort_node.get_live_out_vars():
        dofdy__yrtgn = typemap[qky__fxyi.name]
        pswyc__ffnb = array_analysis._gen_shape_call(equiv_set, qky__fxyi,
            dofdy__yrtgn.ndim, None, blx__race)
        equiv_set.insert_equiv(qky__fxyi, pswyc__ffnb)
        iued__ekalf.append(pswyc__ffnb[0])
        equiv_set.define(qky__fxyi, set())
    if len(iued__ekalf) > 1:
        equiv_set.insert_equiv(*iued__ekalf)
    return [], blx__race


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    dkyd__rrdvr = sort_node.get_live_in_vars()
    cnx__xpuit = sort_node.get_live_out_vars()
    imgnk__jgq = Distribution.OneD
    for qky__fxyi in dkyd__rrdvr:
        imgnk__jgq = Distribution(min(imgnk__jgq.value, array_dists[
            qky__fxyi.name].value))
    tie__oozp = Distribution(min(imgnk__jgq.value, Distribution.OneD_Var.value)
        )
    for qky__fxyi in cnx__xpuit:
        if qky__fxyi.name in array_dists:
            tie__oozp = Distribution(min(tie__oozp.value, array_dists[
                qky__fxyi.name].value))
    if tie__oozp != Distribution.OneD_Var:
        imgnk__jgq = tie__oozp
    for qky__fxyi in dkyd__rrdvr:
        array_dists[qky__fxyi.name] = imgnk__jgq
    for qky__fxyi in cnx__xpuit:
        array_dists[qky__fxyi.name] = tie__oozp


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for lkd__cfjso, uxh__kxa in enumerate(sort_node.out_vars):
        auplh__czcf = sort_node.in_vars[lkd__cfjso]
        if auplh__czcf is not None and uxh__kxa is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=uxh__kxa
                .name, src=auplh__czcf.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for qky__fxyi in sort_node.get_live_out_vars():
            definitions[qky__fxyi.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for lkd__cfjso in range(len(sort_node.in_vars)):
        if sort_node.in_vars[lkd__cfjso] is not None:
            sort_node.in_vars[lkd__cfjso] = visit_vars_inner(sort_node.
                in_vars[lkd__cfjso], callback, cbdata)
        if sort_node.out_vars[lkd__cfjso] is not None:
            sort_node.out_vars[lkd__cfjso] = visit_vars_inner(sort_node.
                out_vars[lkd__cfjso], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        uhkke__mveyj = sort_node.out_vars[0]
        if uhkke__mveyj is not None and uhkke__mveyj.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            tzu__qvayj = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & tzu__qvayj)
            sort_node.dead_var_inds.update(dead_cols - tzu__qvayj)
            if len(tzu__qvayj & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for lkd__cfjso in range(1, len(sort_node.out_vars)):
            yptqx__lyeoq = sort_node.out_vars[lkd__cfjso]
            if yptqx__lyeoq is not None and yptqx__lyeoq.name not in lives:
                sort_node.out_vars[lkd__cfjso] = None
                chewa__qzd = sort_node.num_table_arrays + lkd__cfjso - 1
                if chewa__qzd in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(chewa__qzd)
                else:
                    sort_node.dead_var_inds.add(chewa__qzd)
                    sort_node.in_vars[lkd__cfjso] = None
    else:
        for lkd__cfjso in range(len(sort_node.out_vars)):
            yptqx__lyeoq = sort_node.out_vars[lkd__cfjso]
            if yptqx__lyeoq is not None and yptqx__lyeoq.name not in lives:
                sort_node.out_vars[lkd__cfjso] = None
                if lkd__cfjso in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(lkd__cfjso)
                else:
                    sort_node.dead_var_inds.add(lkd__cfjso)
                    sort_node.in_vars[lkd__cfjso] = None
    if all(yptqx__lyeoq is None for yptqx__lyeoq in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({yptqx__lyeoq.name for yptqx__lyeoq in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({yptqx__lyeoq.name for yptqx__lyeoq in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    omhi__rlatg = set()
    if not sort_node.inplace:
        omhi__rlatg.update({yptqx__lyeoq.name for yptqx__lyeoq in sort_node
            .get_live_out_vars()})
    return set(), omhi__rlatg


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for lkd__cfjso in range(len(sort_node.in_vars)):
        if sort_node.in_vars[lkd__cfjso] is not None:
            sort_node.in_vars[lkd__cfjso] = replace_vars_inner(sort_node.
                in_vars[lkd__cfjso], var_dict)
        if sort_node.out_vars[lkd__cfjso] is not None:
            sort_node.out_vars[lkd__cfjso] = replace_vars_inner(sort_node.
                out_vars[lkd__cfjso], var_dict)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = replace_vars_inner(sort_node.
            _bodo_chunk_bounds, var_dict)


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    in_vars = sort_node.get_live_in_vars()
    out_vars = sort_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for yptqx__lyeoq in (in_vars + out_vars):
            if array_dists[yptqx__lyeoq.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                yptqx__lyeoq.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        lcg__ergwy = []
        for yptqx__lyeoq in in_vars:
            qht__hmkve = _copy_array_nodes(yptqx__lyeoq, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            lcg__ergwy.append(qht__hmkve)
        in_vars = lcg__ergwy
    out_types = [(typemap[yptqx__lyeoq.name] if yptqx__lyeoq is not None else
        types.none) for yptqx__lyeoq in sort_node.out_vars]
    rpne__wpb, ljmqq__btnk = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    qaxsa__bzfs = {}
    exec(rpne__wpb, {}, qaxsa__bzfs)
    bef__trdjb = qaxsa__bzfs['f']
    ljmqq__btnk.update({'bodo': bodo, 'np': np, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'py_data_to_cpp_table':
        py_data_to_cpp_table, 'cpp_table_to_py_data': cpp_table_to_py_data})
    ljmqq__btnk.update({f'out_type{lkd__cfjso}': out_types[lkd__cfjso] for
        lkd__cfjso in range(len(out_types))})
    kjbt__awm = sort_node._bodo_chunk_bounds
    hzwg__dvob = kjbt__awm
    if kjbt__awm is None:
        loc = sort_node.loc
        hzwg__dvob = ir.Var(ir.Scope(None, loc), mk_unique_var(
            '$bounds_none'), loc)
        typemap[hzwg__dvob.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), hzwg__dvob, loc))
    rlmtg__bfg = compile_to_numba_ir(bef__trdjb, ljmqq__btnk, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[yptqx__lyeoq
        .name] for yptqx__lyeoq in in_vars) + (typemap[hzwg__dvob.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(rlmtg__bfg, in_vars + [hzwg__dvob])
    ipitg__rdsf = rlmtg__bfg.body[-2].value.value
    nodes += rlmtg__bfg.body[:-2]
    for lkd__cfjso, yptqx__lyeoq in enumerate(out_vars):
        gen_getitem(yptqx__lyeoq, ipitg__rdsf, lkd__cfjso, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    vkj__qyd = lambda arr: arr.copy()
    tdmz__lwwd = None
    if isinstance(typemap[var.name], TableType):
        ypxo__req = len(typemap[var.name].arr_types)
        tdmz__lwwd = set(range(ypxo__req)) - dead_cols
        tdmz__lwwd = MetaType(tuple(sorted(tdmz__lwwd)))
        vkj__qyd = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    rlmtg__bfg = compile_to_numba_ir(vkj__qyd, {'bodo': bodo, 'types':
        types, '_used_columns': tdmz__lwwd}, typingctx=typingctx, targetctx
        =targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(rlmtg__bfg, [var])
    nodes += rlmtg__bfg.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    xfqe__qwwmu = len(sort_node.key_inds)
    hctz__lwrwr = len(sort_node.in_vars)
    axnb__euulz = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + hctz__lwrwr - 1 if sort_node.
        is_table_format else hctz__lwrwr)
    rva__rrdx, prrbh__atai, pzk__paij = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    omrjr__ysns = []
    if sort_node.is_table_format:
        omrjr__ysns.append('arg0')
        for lkd__cfjso in range(1, hctz__lwrwr):
            chewa__qzd = sort_node.num_table_arrays + lkd__cfjso - 1
            if chewa__qzd not in sort_node.dead_var_inds:
                omrjr__ysns.append(f'arg{chewa__qzd}')
    else:
        for lkd__cfjso in range(n_cols):
            if lkd__cfjso not in sort_node.dead_var_inds:
                omrjr__ysns.append(f'arg{lkd__cfjso}')
    rpne__wpb = f"def f({', '.join(omrjr__ysns)}, bounds_in):\n"
    if sort_node.is_table_format:
        zbm__lho = ',' if hctz__lwrwr - 1 == 1 else ''
        asv__sxa = []
        for lkd__cfjso in range(sort_node.num_table_arrays, n_cols):
            if lkd__cfjso in sort_node.dead_var_inds:
                asv__sxa.append('None')
            else:
                asv__sxa.append(f'arg{lkd__cfjso}')
        rpne__wpb += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(asv__sxa)}{zbm__lho}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        kgzkd__vpir = {mldm__wzq: lkd__cfjso for lkd__cfjso, mldm__wzq in
            enumerate(rva__rrdx)}
        kua__buz = [None] * len(rva__rrdx)
        for lkd__cfjso in range(n_cols):
            ykgz__ifpe = kgzkd__vpir.get(lkd__cfjso, -1)
            if ykgz__ifpe != -1:
                kua__buz[ykgz__ifpe] = f'array_to_info(arg{lkd__cfjso})'
        rpne__wpb += '  info_list_total = [{}]\n'.format(','.join(kua__buz))
        rpne__wpb += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    rpne__wpb += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if igncz__dioif else '0' for igncz__dioif in sort_node.
        ascending_list))
    rpne__wpb += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if igncz__dioif else '0' for igncz__dioif in sort_node.
        na_position_b))
    rpne__wpb += '  dead_keys = np.array([{}], np.int64)\n'.format(','.join
        ('1' if lkd__cfjso in pzk__paij else '0' for lkd__cfjso in range(
        xfqe__qwwmu)))
    rpne__wpb += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    sivyc__lim = sort_node._bodo_chunk_bounds
    oyu__gzdt = '0' if sivyc__lim is None or is_overload_none(typemap[
        sivyc__lim.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    rpne__wpb += f"""  out_cpp_table = sort_values_table(in_cpp_table, {xfqe__qwwmu}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {oyu__gzdt}, {parallel})
"""
    if sort_node.is_table_format:
        zbm__lho = ',' if axnb__euulz == 1 else ''
        auz__zwzhs = (
            f"({', '.join(f'out_type{lkd__cfjso}' if not type_has_unknown_cats(out_types[lkd__cfjso]) else f'arg{lkd__cfjso}' for lkd__cfjso in range(axnb__euulz))}{zbm__lho})"
            )
        rpne__wpb += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {auz__zwzhs}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        kgzkd__vpir = {mldm__wzq: lkd__cfjso for lkd__cfjso, mldm__wzq in
            enumerate(prrbh__atai)}
        kua__buz = []
        for lkd__cfjso in range(n_cols):
            ykgz__ifpe = kgzkd__vpir.get(lkd__cfjso, -1)
            if ykgz__ifpe != -1:
                ljhl__tyfz = (f'out_type{lkd__cfjso}' if not
                    type_has_unknown_cats(out_types[lkd__cfjso]) else
                    f'arg{lkd__cfjso}')
                rpne__wpb += f"""  out{lkd__cfjso} = info_to_array(info_from_table(out_cpp_table, {ykgz__ifpe}), {ljhl__tyfz})
"""
                kua__buz.append(f'out{lkd__cfjso}')
        zbm__lho = ',' if len(kua__buz) == 1 else ''
        vraw__zbkp = f"({', '.join(kua__buz)}{zbm__lho})"
        rpne__wpb += f'  out_data = {vraw__zbkp}\n'
    rpne__wpb += '  delete_table(out_cpp_table)\n'
    rpne__wpb += '  delete_table(in_cpp_table)\n'
    rpne__wpb += f'  return out_data\n'
    return rpne__wpb, {'in_col_inds': MetaType(tuple(rva__rrdx)),
        'out_col_inds': MetaType(tuple(prrbh__atai))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    rva__rrdx = []
    prrbh__atai = []
    pzk__paij = []
    for mldm__wzq, lkd__cfjso in enumerate(key_inds):
        rva__rrdx.append(lkd__cfjso)
        if lkd__cfjso in dead_key_var_inds:
            pzk__paij.append(mldm__wzq)
        else:
            prrbh__atai.append(lkd__cfjso)
    for lkd__cfjso in range(n_cols):
        if lkd__cfjso in dead_var_inds or lkd__cfjso in key_inds:
            continue
        rva__rrdx.append(lkd__cfjso)
        prrbh__atai.append(lkd__cfjso)
    return rva__rrdx, prrbh__atai, pzk__paij


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    bfqv__sjpuh = sort_node.in_vars[0].name
    guys__rhh = sort_node.out_vars[0].name
    btvq__pcv, ffut__abg, flky__pmnwb = block_use_map[bfqv__sjpuh]
    if ffut__abg or flky__pmnwb:
        return
    gkah__aqwp, wbd__jou, irch__txqj = _compute_table_column_uses(guys__rhh,
        table_col_use_map, equiv_vars)
    vkq__xao = set(lkd__cfjso for lkd__cfjso in sort_node.key_inds if 
        lkd__cfjso < sort_node.num_table_arrays)
    block_use_map[bfqv__sjpuh
        ] = btvq__pcv | gkah__aqwp | vkq__xao, wbd__jou or irch__txqj, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    ypxo__req = sort_node.num_table_arrays
    guys__rhh = sort_node.out_vars[0].name
    tdmz__lwwd = _find_used_columns(guys__rhh, ypxo__req, column_live_map,
        equiv_vars)
    if tdmz__lwwd is None:
        return False
    mcgmf__ghx = set(range(ypxo__req)) - tdmz__lwwd
    vkq__xao = set(lkd__cfjso for lkd__cfjso in sort_node.key_inds if 
        lkd__cfjso < ypxo__req)
    sskp__mnay = sort_node.dead_key_var_inds | mcgmf__ghx & vkq__xao
    wsn__nlmnh = sort_node.dead_var_inds | mcgmf__ghx - vkq__xao
    azkp__icha = (sskp__mnay != sort_node.dead_key_var_inds) | (wsn__nlmnh !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = sskp__mnay
    sort_node.dead_var_inds = wsn__nlmnh
    return azkp__icha


remove_dead_column_extensions[Sort] = sort_remove_dead_column
