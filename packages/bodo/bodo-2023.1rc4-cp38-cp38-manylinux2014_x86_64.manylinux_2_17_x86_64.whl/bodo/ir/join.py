"""IR node for the join and merge"""
from collections import defaultdict
from typing import Dict, List, Literal, Optional, Set, Tuple, Union
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic
import bodo
from bodo.hiframes.table import TableType
from bodo.ir.connector import trim_extra_used_columns
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, cross_join_table, delete_table, hash_join_table, py_data_to_cpp_table
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import INDEX_SENTINEL, BodoError, MetaType, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        gasy__ftyzk = func.signature
        aucrg__weqp = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        wmyq__kyf = cgutils.get_or_insert_function(builder.module,
            aucrg__weqp, sym._literal_value)
        builder.call(wmyq__kyf, [context.get_constant_null(gasy__ftyzk.args
            [0]), context.get_constant_null(gasy__ftyzk.args[1]), context.
            get_constant_null(gasy__ftyzk.args[2]), context.
            get_constant_null(gasy__ftyzk.args[3]), context.
            get_constant_null(gasy__ftyzk.args[4]), context.
            get_constant_null(gasy__ftyzk.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


HOW_OPTIONS = Literal['inner', 'left', 'right', 'outer', 'asof', 'cross']


class Join(ir.Stmt):

    def __init__(self, left_keys: Union[List[str], str], right_keys: Union[
        List[str], str], out_data_vars: List[ir.Var], out_df_type: bodo.
        DataFrameType, left_vars: List[ir.Var], left_df_type: bodo.
        DataFrameType, right_vars: List[ir.Var], right_df_type: bodo.
        DataFrameType, how: HOW_OPTIONS, suffix_left: str, suffix_right:
        str, loc: ir.Loc, is_left: bool, is_right: bool, is_join: bool,
        left_index: bool, right_index: bool, indicator_col_num: int,
        is_na_equal: bool, gen_cond_expr: str, left_len_var: ir.Var,
        right_len_var: ir.Var):
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.out_col_names = out_df_type.columns
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator_col_num = indicator_col_num
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_len_var = left_len_var
        self.right_len_var = right_len_var
        self.n_out_table_cols = len(self.out_col_names)
        self.out_used_cols = set(range(self.n_out_table_cols))
        if self.out_data_vars[1] is not None:
            self.out_used_cols.add(self.n_out_table_cols)
        deapi__wtj = left_df_type.columns
        gstzc__yca = right_df_type.columns
        self.left_col_names = deapi__wtj
        self.right_col_names = gstzc__yca
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(deapi__wtj) if self.is_left_table else 0
        self.n_right_table_cols = len(gstzc__yca) if self.is_right_table else 0
        zdi__bztpt = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        ter__vuky = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(zdi__bztpt)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(ter__vuky)
        self.left_var_map = {ule__jib: vosp__qqde for vosp__qqde, ule__jib in
            enumerate(deapi__wtj)}
        self.right_var_map = {ule__jib: vosp__qqde for vosp__qqde, ule__jib in
            enumerate(gstzc__yca)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = zdi__bztpt
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = ter__vuky
        self.left_key_set = set(self.left_var_map[ule__jib] for ule__jib in
            left_keys)
        self.right_key_set = set(self.right_var_map[ule__jib] for ule__jib in
            right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[ule__jib] for
                ule__jib in deapi__wtj if f'(left.{ule__jib})' in gen_cond_expr
                )
            self.right_cond_cols = set(self.right_var_map[ule__jib] for
                ule__jib in gstzc__yca if f'(right.{ule__jib})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        fok__xhz: int = -1
        xxqx__bpyrw = set(left_keys) & set(right_keys)
        wszhn__qkd = set(deapi__wtj) & set(gstzc__yca)
        lla__gse = wszhn__qkd - xxqx__bpyrw
        ohsfq__gqhg: Dict[int, (Literal['left', 'right'], int)] = {}
        sgr__bsw: Dict[int, int] = {}
        cjir__gxd: Dict[int, int] = {}
        for vosp__qqde, ule__jib in enumerate(deapi__wtj):
            if ule__jib in lla__gse:
                oft__isfui = str(ule__jib) + suffix_left
                ajj__euz = out_df_type.column_index[oft__isfui]
                if (right_index and not left_index and vosp__qqde in self.
                    left_key_set):
                    fok__xhz = out_df_type.column_index[ule__jib]
                    ohsfq__gqhg[fok__xhz] = 'left', vosp__qqde
            else:
                ajj__euz = out_df_type.column_index[ule__jib]
            ohsfq__gqhg[ajj__euz] = 'left', vosp__qqde
            sgr__bsw[vosp__qqde] = ajj__euz
        for vosp__qqde, ule__jib in enumerate(gstzc__yca):
            if ule__jib not in xxqx__bpyrw:
                if ule__jib in lla__gse:
                    osl__botej = str(ule__jib) + suffix_right
                    ajj__euz = out_df_type.column_index[osl__botej]
                    if (left_index and not right_index and vosp__qqde in
                        self.right_key_set):
                        fok__xhz = out_df_type.column_index[ule__jib]
                        ohsfq__gqhg[fok__xhz] = 'right', vosp__qqde
                else:
                    ajj__euz = out_df_type.column_index[ule__jib]
                ohsfq__gqhg[ajj__euz] = 'right', vosp__qqde
                cjir__gxd[vosp__qqde] = ajj__euz
        if self.left_vars[-1] is not None:
            sgr__bsw[zdi__bztpt] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            cjir__gxd[ter__vuky] = self.n_out_table_cols
        self.out_to_input_col_map = ohsfq__gqhg
        self.left_to_output_map = sgr__bsw
        self.right_to_output_map = cjir__gxd
        self.extra_data_col_num = fok__xhz
        if self.out_data_vars[1] is not None:
            def__xiaqb = 'left' if right_index else 'right'
            if def__xiaqb == 'left':
                hqi__adau = zdi__bztpt
            elif def__xiaqb == 'right':
                hqi__adau = ter__vuky
        else:
            def__xiaqb = None
            hqi__adau = -1
        self.index_source = def__xiaqb
        self.index_col_num = hqi__adau
        fsxnl__hcj = []
        pzp__yls = len(left_keys)
        for zrav__usrz in range(pzp__yls):
            jex__gupf = left_keys[zrav__usrz]
            yjsjy__cbgle = right_keys[zrav__usrz]
            fsxnl__hcj.append(jex__gupf == yjsjy__cbgle)
        self.vect_same_key = fsxnl__hcj

    @property
    def has_live_left_table_var(self):
        return self.is_left_table and self.left_vars[0] is not None

    @property
    def has_live_right_table_var(self):
        return self.is_right_table and self.right_vars[0] is not None

    @property
    def has_live_out_table_var(self):
        return self.out_data_vars[0] is not None

    @property
    def has_live_out_index_var(self):
        return self.out_data_vars[1] is not None

    def get_out_table_var(self):
        return self.out_data_vars[0]

    def get_out_index_var(self):
        return self.out_data_vars[1]

    def get_live_left_vars(self):
        vars = []
        for ppbtp__ugz in self.left_vars:
            if ppbtp__ugz is not None:
                vars.append(ppbtp__ugz)
        return vars

    def get_live_right_vars(self):
        vars = []
        for ppbtp__ugz in self.right_vars:
            if ppbtp__ugz is not None:
                vars.append(ppbtp__ugz)
        return vars

    def get_live_out_vars(self):
        vars = []
        for ppbtp__ugz in self.out_data_vars:
            if ppbtp__ugz is not None:
                vars.append(ppbtp__ugz)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        vypjb__wjzsk = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[vypjb__wjzsk])
                vypjb__wjzsk += 1
            else:
                left_vars.append(None)
            start = 1
        qayoh__fxq = max(self.n_left_table_cols - 1, 0)
        for vosp__qqde in range(start, len(self.left_vars)):
            if vosp__qqde + qayoh__fxq in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[vypjb__wjzsk])
                vypjb__wjzsk += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        vypjb__wjzsk = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[vypjb__wjzsk])
                vypjb__wjzsk += 1
            else:
                right_vars.append(None)
            start = 1
        qayoh__fxq = max(self.n_right_table_cols - 1, 0)
        for vosp__qqde in range(start, len(self.right_vars)):
            if vosp__qqde + qayoh__fxq in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[vypjb__wjzsk])
                vypjb__wjzsk += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        rmyqe__qbox = [self.has_live_out_table_var, self.has_live_out_index_var
            ]
        vypjb__wjzsk = 0
        for vosp__qqde in range(len(self.out_data_vars)):
            if not rmyqe__qbox[vosp__qqde]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[vypjb__wjzsk])
                vypjb__wjzsk += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {vosp__qqde for vosp__qqde in self.out_used_cols if 
            vosp__qqde < self.n_out_table_cols}

    def __repr__(self):
        mqmi__egoc = ', '.join([f'{ule__jib}' for ule__jib in self.
            left_col_names])
        kzpv__eyz = f'left={{{mqmi__egoc}}}'
        mqmi__egoc = ', '.join([f'{ule__jib}' for ule__jib in self.
            right_col_names])
        sqd__fbuo = f'right={{{mqmi__egoc}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, kzpv__eyz, sqd__fbuo)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    nwkjq__visfs = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    cuj__sdxyo = []
    yobac__wvz = join_node.get_live_left_vars()
    for heh__axxad in yobac__wvz:
        ttc__autrt = typemap[heh__axxad.name]
        xbhr__cjwd = equiv_set.get_shape(heh__axxad)
        if xbhr__cjwd:
            cuj__sdxyo.append(xbhr__cjwd[0])
    if len(cuj__sdxyo) > 1:
        equiv_set.insert_equiv(*cuj__sdxyo)
    cuj__sdxyo = []
    yobac__wvz = list(join_node.get_live_right_vars())
    for heh__axxad in yobac__wvz:
        ttc__autrt = typemap[heh__axxad.name]
        xbhr__cjwd = equiv_set.get_shape(heh__axxad)
        if xbhr__cjwd:
            cuj__sdxyo.append(xbhr__cjwd[0])
    if len(cuj__sdxyo) > 1:
        equiv_set.insert_equiv(*cuj__sdxyo)
    cuj__sdxyo = []
    for txa__kmmx in join_node.get_live_out_vars():
        ttc__autrt = typemap[txa__kmmx.name]
        ymjtw__mkxk = array_analysis._gen_shape_call(equiv_set, txa__kmmx,
            ttc__autrt.ndim, None, nwkjq__visfs)
        equiv_set.insert_equiv(txa__kmmx, ymjtw__mkxk)
        cuj__sdxyo.append(ymjtw__mkxk[0])
        equiv_set.define(txa__kmmx, set())
    if len(cuj__sdxyo) > 1:
        equiv_set.insert_equiv(*cuj__sdxyo)
    return [], nwkjq__visfs


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    xksx__uxc = Distribution.OneD
    vscp__igbqv = Distribution.OneD
    for heh__axxad in join_node.get_live_left_vars():
        xksx__uxc = Distribution(min(xksx__uxc.value, array_dists[
            heh__axxad.name].value))
    for heh__axxad in join_node.get_live_right_vars():
        vscp__igbqv = Distribution(min(vscp__igbqv.value, array_dists[
            heh__axxad.name].value))
    suesw__wer = Distribution.OneD_Var
    for txa__kmmx in join_node.get_live_out_vars():
        if txa__kmmx.name in array_dists:
            suesw__wer = Distribution(min(suesw__wer.value, array_dists[
                txa__kmmx.name].value))
    umx__atn = Distribution(min(suesw__wer.value, xksx__uxc.value))
    qmjrc__nyayt = Distribution(min(suesw__wer.value, vscp__igbqv.value))
    suesw__wer = Distribution(max(umx__atn.value, qmjrc__nyayt.value))
    for txa__kmmx in join_node.get_live_out_vars():
        array_dists[txa__kmmx.name] = suesw__wer
    if suesw__wer != Distribution.OneD_Var:
        xksx__uxc = suesw__wer
        vscp__igbqv = suesw__wer
    for heh__axxad in join_node.get_live_left_vars():
        array_dists[heh__axxad.name] = xksx__uxc
    for heh__axxad in join_node.get_live_right_vars():
        array_dists[heh__axxad.name] = vscp__igbqv
    join_node.left_dist = xksx__uxc
    join_node.right_dist = vscp__igbqv


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(ppbtp__ugz, callback,
        cbdata) for ppbtp__ugz in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(ppbtp__ugz, callback,
        cbdata) for ppbtp__ugz in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(ppbtp__ugz, callback,
        cbdata) for ppbtp__ugz in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = visit_vars_inner(join_node.left_len_var,
            callback, cbdata)
        join_node.right_len_var = visit_vars_inner(join_node.right_len_var,
            callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def _is_cross_join_len(join_node):
    return (join_node.how == 'cross' and not join_node.out_used_cols and
        join_node.has_live_out_table_var and not join_node.
        has_live_out_index_var)


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if join_node.has_live_out_table_var:
        tgqd__rqu = []
        elv__trj = join_node.get_out_table_var()
        if elv__trj.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for hmerr__xbimb in join_node.out_to_input_col_map.keys():
            if hmerr__xbimb in join_node.out_used_cols:
                continue
            tgqd__rqu.append(hmerr__xbimb)
            if join_node.indicator_col_num == hmerr__xbimb:
                join_node.indicator_col_num = -1
                continue
            if hmerr__xbimb == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            cbwag__pmk, hmerr__xbimb = join_node.out_to_input_col_map[
                hmerr__xbimb]
            if cbwag__pmk == 'left':
                if (hmerr__xbimb not in join_node.left_key_set and 
                    hmerr__xbimb not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(hmerr__xbimb)
                    if not join_node.is_left_table:
                        join_node.left_vars[hmerr__xbimb] = None
            elif cbwag__pmk == 'right':
                if (hmerr__xbimb not in join_node.right_key_set and 
                    hmerr__xbimb not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(hmerr__xbimb)
                    if not join_node.is_right_table:
                        join_node.right_vars[hmerr__xbimb] = None
        for vosp__qqde in tgqd__rqu:
            del join_node.out_to_input_col_map[vosp__qqde]
        if join_node.is_left_table:
            tztr__sufbx = set(range(join_node.n_left_table_cols))
            bcwc__feic = not bool(tztr__sufbx - join_node.left_dead_var_inds)
            if bcwc__feic:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            tztr__sufbx = set(range(join_node.n_right_table_cols))
            bcwc__feic = not bool(tztr__sufbx - join_node.right_dead_var_inds)
            if bcwc__feic:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        xsciq__otfd = join_node.get_out_index_var()
        if xsciq__otfd.name not in lives:
            join_node.out_data_vars[1] = None
            join_node.out_used_cols.remove(join_node.n_out_table_cols)
            if join_node.index_source == 'left':
                if (join_node.index_col_num not in join_node.left_key_set and
                    join_node.index_col_num not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(join_node.index_col_num)
                    join_node.left_vars[-1] = None
            elif join_node.index_col_num not in join_node.right_key_set and join_node.index_col_num not in join_node.right_cond_cols:
                join_node.right_dead_var_inds.add(join_node.index_col_num)
                join_node.right_vars[-1] = None
    if not (join_node.has_live_out_table_var or join_node.
        has_live_out_index_var):
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_remove_dead_column(join_node, column_live_map, equiv_vars, typemap):
    ubv__jwzwo = False
    if join_node.has_live_out_table_var:
        yski__rno = join_node.get_out_table_var().name
        jnqpw__kbh, ousp__adqs, oflc__diyw = get_live_column_nums_block(
            column_live_map, equiv_vars, yski__rno)
        if not (ousp__adqs or oflc__diyw):
            jnqpw__kbh = trim_extra_used_columns(jnqpw__kbh, join_node.
                n_out_table_cols)
            dihr__iiyco = join_node.get_out_table_used_cols()
            if len(jnqpw__kbh) != len(dihr__iiyco):
                ubv__jwzwo = not (join_node.is_left_table and join_node.
                    is_right_table)
                lkmm__abl = dihr__iiyco - jnqpw__kbh
                join_node.out_used_cols = join_node.out_used_cols - lkmm__abl
    return ubv__jwzwo


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        xign__jdqy = join_node.get_out_table_var()
        nrkxl__hauy, ousp__adqs, oflc__diyw = _compute_table_column_uses(
            xign__jdqy.name, table_col_use_map, equiv_vars)
    else:
        nrkxl__hauy, ousp__adqs, oflc__diyw = set(), False, False
    if join_node.has_live_left_table_var:
        vpi__vlcfu = join_node.left_vars[0].name
        wija__okhpv, kjl__uqa, sjh__pxrbx = block_use_map[vpi__vlcfu]
        if not (kjl__uqa or sjh__pxrbx):
            rxvnr__jsj = set([join_node.out_to_input_col_map[vosp__qqde][1] for
                vosp__qqde in nrkxl__hauy if join_node.out_to_input_col_map
                [vosp__qqde][0] == 'left'])
            mpha__vtwnc = set(vosp__qqde for vosp__qqde in join_node.
                left_key_set | join_node.left_cond_cols if vosp__qqde <
                join_node.n_left_table_cols)
            if not (ousp__adqs or oflc__diyw):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (rxvnr__jsj | mpha__vtwnc)
            block_use_map[vpi__vlcfu] = (wija__okhpv | rxvnr__jsj |
                mpha__vtwnc, ousp__adqs or oflc__diyw, False)
    if join_node.has_live_right_table_var:
        lzyl__qcr = join_node.right_vars[0].name
        wija__okhpv, kjl__uqa, sjh__pxrbx = block_use_map[lzyl__qcr]
        if not (kjl__uqa or sjh__pxrbx):
            wvlpt__ukw = set([join_node.out_to_input_col_map[vosp__qqde][1] for
                vosp__qqde in nrkxl__hauy if join_node.out_to_input_col_map
                [vosp__qqde][0] == 'right'])
            padi__whwn = set(vosp__qqde for vosp__qqde in join_node.
                right_key_set | join_node.right_cond_cols if vosp__qqde <
                join_node.n_right_table_cols)
            if not (ousp__adqs or oflc__diyw):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (wvlpt__ukw | padi__whwn)
            block_use_map[lzyl__qcr] = (wija__okhpv | wvlpt__ukw |
                padi__whwn, ousp__adqs or oflc__diyw, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({almwy__gccb.name for almwy__gccb in join_node.
        get_live_left_vars()})
    use_set.update({almwy__gccb.name for almwy__gccb in join_node.
        get_live_right_vars()})
    def_set.update({almwy__gccb.name for almwy__gccb in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    divb__tskyi = set(almwy__gccb.name for almwy__gccb in join_node.
        get_live_out_vars())
    return set(), divb__tskyi


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(ppbtp__ugz, var_dict) for
        ppbtp__ugz in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(ppbtp__ugz, var_dict) for
        ppbtp__ugz in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(ppbtp__ugz,
        var_dict) for ppbtp__ugz in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for heh__axxad in join_node.get_live_out_vars():
        definitions[heh__axxad.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    zksfb__gark = 'bodo.libs.distributed_api.get_size()'
    qfj__jcrwj = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {zksfb__gark}, {qfj__jcrwj})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {zksfb__gark}, {qfj__jcrwj})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    joz__vhqv = {}
    exec(func_text, {}, joz__vhqv)
    cpwos__yelc = joz__vhqv['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    yvc__ucmj = [join_node.left_len_var, join_node.right_len_var]
    pdd__pfp = tuple(typemap[almwy__gccb.name] for almwy__gccb in yvc__ucmj)
    uuf__ihig = compile_to_numba_ir(cpwos__yelc, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pdd__pfp, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(uuf__ihig, yvc__ucmj)
    gnk__oqded = uuf__ihig.body[:-3]
    gnk__oqded[-1].target = join_node.out_data_vars[0]
    return gnk__oqded


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    yobac__wvz = join_node.right_vars if left_is_dead else join_node.left_vars
    rft__jmiw = ', '.join(f't{vosp__qqde}' for vosp__qqde in range(len(
        yobac__wvz)) if yobac__wvz[vosp__qqde] is not None)
    cvdc__qjx = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    ont__wcuwr = (join_node.is_right_table if left_is_dead else join_node.
        is_left_table)
    ktfsr__xrg = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    cmr__waqf = [(f'get_table_data(t0, {vosp__qqde})' if ont__wcuwr else
        f't{vosp__qqde}') for vosp__qqde in range(cvdc__qjx)]
    kivo__wzui = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({cmr__waqf[vosp__qqde]}, repeats)'
         if vosp__qqde not in ktfsr__xrg else 'None' for vosp__qqde in
        range(cvdc__qjx))
    axd__npe = len(out_table_type.arr_types)
    ajao__dep = [join_node.out_to_input_col_map.get(vosp__qqde, (-1, -1))[1
        ] for vosp__qqde in range(axd__npe)]
    zksfb__gark = 'bodo.libs.distributed_api.get_size()'
    qfj__jcrwj = 'bodo.libs.distributed_api.get_rank()'
    hnf__bsxpj = 'left_len' if left_is_dead else 'right_len'
    ucq__hbm = right_parallel if left_is_dead else left_parallel
    dhilt__tir = left_parallel if left_is_dead else right_parallel
    sfmo__xcfa = not ucq__hbm and dhilt__tir
    byyv__boe = (
        f'bodo.libs.distributed_api.get_node_portion({hnf__bsxpj}, {zksfb__gark}, {qfj__jcrwj})'
         if sfmo__xcfa else hnf__bsxpj)
    func_text = f'def f({rft__jmiw}, left_len, right_len):\n'
    func_text += f'  repeats = {byyv__boe}\n'
    func_text += f'  out_data = ({kivo__wzui},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {cvdc__qjx}, out_table_type, used_cols)
"""
    joz__vhqv = {}
    exec(func_text, {}, joz__vhqv)
    cpwos__yelc = joz__vhqv['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(ajao__dep)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    yvc__ucmj = [almwy__gccb for almwy__gccb in yobac__wvz if almwy__gccb
         is not None] + [join_node.left_len_var, join_node.right_len_var]
    pdd__pfp = tuple(typemap[almwy__gccb.name] for almwy__gccb in yvc__ucmj)
    uuf__ihig = compile_to_numba_ir(cpwos__yelc, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pdd__pfp, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(uuf__ihig, yvc__ucmj)
    gnk__oqded = uuf__ihig.body[:-3]
    gnk__oqded[-1].target = join_node.out_data_vars[0]
    return gnk__oqded


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        rqvqq__mqx = join_node.loc.strformat()
        enn__ldmk = [join_node.left_col_names[vosp__qqde] for vosp__qqde in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        redrl__vpzca = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', redrl__vpzca,
            rqvqq__mqx, enn__ldmk)
        zkn__nus = [join_node.right_col_names[vosp__qqde] for vosp__qqde in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        redrl__vpzca = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', redrl__vpzca,
            rqvqq__mqx, zkn__nus)
        kvtcc__dqx = [join_node.out_col_names[vosp__qqde] for vosp__qqde in
            sorted(join_node.get_out_table_used_cols())]
        redrl__vpzca = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', redrl__vpzca,
            rqvqq__mqx, kvtcc__dqx)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    pzp__yls = len(join_node.left_keys)
    out_physical_to_logical_list = []
    if join_node.has_live_out_table_var:
        out_table_type = typemap[join_node.get_out_table_var().name]
    else:
        out_table_type = types.none
    if join_node.has_live_out_index_var:
        index_col_type = typemap[join_node.get_out_index_var().name]
    else:
        index_col_type = types.none
    if _is_cross_join_len(join_node):
        return _gen_cross_join_len(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel)
    elif join_node.how == 'cross' and all(vosp__qqde in join_node.
        left_dead_var_inds for vosp__qqde in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(vosp__qqde in join_node.
        right_dead_var_inds for vosp__qqde in range(len(join_node.
        right_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            False)
    if join_node.extra_data_col_num != -1:
        out_physical_to_logical_list.append(join_node.extra_data_col_num)
    left_key_in_output = []
    right_key_in_output = []
    left_used_key_nums = set()
    right_used_key_nums = set()
    tat__eudb = set()
    xzur__mhp = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    blsk__hkyt = 0
    iohdm__yqse = 0
    wupm__rpr = []
    for xhk__qsks, ule__jib in enumerate(join_node.left_keys):
        efur__gtb = join_node.left_var_map[ule__jib]
        if not join_node.is_left_table:
            wupm__rpr.append(join_node.left_vars[efur__gtb])
        rmyqe__qbox = 1
        ajj__euz = join_node.left_to_output_map[efur__gtb]
        if ule__jib == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == efur__gtb):
                out_physical_to_logical_list.append(ajj__euz)
                left_used_key_nums.add(xhk__qsks)
                tat__eudb.add(efur__gtb)
            else:
                rmyqe__qbox = 0
        elif ajj__euz not in join_node.out_used_cols:
            rmyqe__qbox = 0
        elif efur__gtb in tat__eudb:
            rmyqe__qbox = 0
        else:
            left_used_key_nums.add(xhk__qsks)
            tat__eudb.add(efur__gtb)
            out_physical_to_logical_list.append(ajj__euz)
        left_physical_to_logical_list.append(efur__gtb)
        left_logical_physical_map[efur__gtb] = blsk__hkyt
        blsk__hkyt += 1
        left_key_in_output.append(rmyqe__qbox)
    wupm__rpr = tuple(wupm__rpr)
    kieh__ktdv = []
    for vosp__qqde in range(len(join_node.left_col_names)):
        if (vosp__qqde not in join_node.left_dead_var_inds and vosp__qqde
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                almwy__gccb = join_node.left_vars[vosp__qqde]
                kieh__ktdv.append(almwy__gccb)
            rfbrj__mkxmg = 1
            okj__wiijn = 1
            ajj__euz = join_node.left_to_output_map[vosp__qqde]
            if vosp__qqde in join_node.left_cond_cols:
                if ajj__euz not in join_node.out_used_cols:
                    rfbrj__mkxmg = 0
                left_key_in_output.append(rfbrj__mkxmg)
            elif vosp__qqde in join_node.left_dead_var_inds:
                rfbrj__mkxmg = 0
                okj__wiijn = 0
            if rfbrj__mkxmg:
                out_physical_to_logical_list.append(ajj__euz)
            if okj__wiijn:
                left_physical_to_logical_list.append(vosp__qqde)
                left_logical_physical_map[vosp__qqde] = blsk__hkyt
                blsk__hkyt += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            kieh__ktdv.append(join_node.left_vars[join_node.index_col_num])
        ajj__euz = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(ajj__euz)
        left_physical_to_logical_list.append(join_node.index_col_num)
    kieh__ktdv = tuple(kieh__ktdv)
    if join_node.is_left_table:
        kieh__ktdv = tuple(join_node.get_live_left_vars())
    bxyj__ajxp = []
    for xhk__qsks, ule__jib in enumerate(join_node.right_keys):
        efur__gtb = join_node.right_var_map[ule__jib]
        if not join_node.is_right_table:
            bxyj__ajxp.append(join_node.right_vars[efur__gtb])
        if not join_node.vect_same_key[xhk__qsks] and not join_node.is_join:
            rmyqe__qbox = 1
            if efur__gtb not in join_node.right_to_output_map:
                rmyqe__qbox = 0
            else:
                ajj__euz = join_node.right_to_output_map[efur__gtb]
                if ule__jib == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        efur__gtb):
                        out_physical_to_logical_list.append(ajj__euz)
                        right_used_key_nums.add(xhk__qsks)
                        xzur__mhp.add(efur__gtb)
                    else:
                        rmyqe__qbox = 0
                elif ajj__euz not in join_node.out_used_cols:
                    rmyqe__qbox = 0
                elif efur__gtb in xzur__mhp:
                    rmyqe__qbox = 0
                else:
                    right_used_key_nums.add(xhk__qsks)
                    xzur__mhp.add(efur__gtb)
                    out_physical_to_logical_list.append(ajj__euz)
            right_key_in_output.append(rmyqe__qbox)
        right_physical_to_logical_list.append(efur__gtb)
        right_logical_physical_map[efur__gtb] = iohdm__yqse
        iohdm__yqse += 1
    bxyj__ajxp = tuple(bxyj__ajxp)
    bzp__gsz = []
    for vosp__qqde in range(len(join_node.right_col_names)):
        if (vosp__qqde not in join_node.right_dead_var_inds and vosp__qqde
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                bzp__gsz.append(join_node.right_vars[vosp__qqde])
            rfbrj__mkxmg = 1
            okj__wiijn = 1
            ajj__euz = join_node.right_to_output_map[vosp__qqde]
            if vosp__qqde in join_node.right_cond_cols:
                if ajj__euz not in join_node.out_used_cols:
                    rfbrj__mkxmg = 0
                right_key_in_output.append(rfbrj__mkxmg)
            elif vosp__qqde in join_node.right_dead_var_inds:
                rfbrj__mkxmg = 0
                okj__wiijn = 0
            if rfbrj__mkxmg:
                out_physical_to_logical_list.append(ajj__euz)
            if okj__wiijn:
                right_physical_to_logical_list.append(vosp__qqde)
                right_logical_physical_map[vosp__qqde] = iohdm__yqse
                iohdm__yqse += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            bzp__gsz.append(join_node.right_vars[join_node.index_col_num])
        ajj__euz = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(ajj__euz)
        right_physical_to_logical_list.append(join_node.index_col_num)
    bzp__gsz = tuple(bzp__gsz)
    if join_node.is_right_table:
        bzp__gsz = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    yvc__ucmj = wupm__rpr + bxyj__ajxp + kieh__ktdv + bzp__gsz
    pdd__pfp = tuple(typemap[almwy__gccb.name] for almwy__gccb in yvc__ucmj)
    left_other_names = tuple('t1_c' + str(vosp__qqde) for vosp__qqde in
        range(len(kieh__ktdv)))
    right_other_names = tuple('t2_c' + str(vosp__qqde) for vosp__qqde in
        range(len(bzp__gsz)))
    if join_node.is_left_table:
        gmup__twqyp = ()
    else:
        gmup__twqyp = tuple('t1_key' + str(vosp__qqde) for vosp__qqde in
            range(pzp__yls))
    if join_node.is_right_table:
        zeuju__hdhn = ()
    else:
        zeuju__hdhn = tuple('t2_key' + str(vosp__qqde) for vosp__qqde in
            range(pzp__yls))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(gmup__twqyp + zeuju__hdhn +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            vorn__zqz = typemap[join_node.left_vars[0].name]
        else:
            vorn__zqz = types.none
        for uoyid__frza in left_physical_to_logical_list:
            if uoyid__frza < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                ttc__autrt = vorn__zqz.arr_types[uoyid__frza]
            else:
                ttc__autrt = typemap[join_node.left_vars[-1].name]
            if uoyid__frza in join_node.left_key_set:
                left_key_types.append(ttc__autrt)
            else:
                left_other_types.append(ttc__autrt)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[almwy__gccb.name] for almwy__gccb in
            wupm__rpr)
        left_other_types = tuple([typemap[ule__jib.name] for ule__jib in
            kieh__ktdv])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            vorn__zqz = typemap[join_node.right_vars[0].name]
        else:
            vorn__zqz = types.none
        for uoyid__frza in right_physical_to_logical_list:
            if uoyid__frza < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                ttc__autrt = vorn__zqz.arr_types[uoyid__frza]
            else:
                ttc__autrt = typemap[join_node.right_vars[-1].name]
            if uoyid__frza in join_node.right_key_set:
                right_key_types.append(ttc__autrt)
            else:
                right_other_types.append(ttc__autrt)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[almwy__gccb.name] for almwy__gccb in
            bxyj__ajxp)
        right_other_types = tuple([typemap[ule__jib.name] for ule__jib in
            bzp__gsz])
    matched_key_types = []
    for vosp__qqde in range(pzp__yls):
        eaz__kbfgh = _match_join_key_types(left_key_types[vosp__qqde],
            right_key_types[vosp__qqde], loc)
        glbs[f'key_type_{vosp__qqde}'] = eaz__kbfgh
        matched_key_types.append(eaz__kbfgh)
    if join_node.is_left_table:
        jzxiq__zioai = determine_table_cast_map(matched_key_types,
            left_key_types, None, {vosp__qqde: join_node.left_var_map[
            jon__ivq] for vosp__qqde, jon__ivq in enumerate(join_node.
            left_keys)}, True)
        if jzxiq__zioai:
            tygkg__bna = False
            xvko__ozw = False
            aoj__zpd = None
            if join_node.has_live_left_table_var:
                dkka__hkf = list(typemap[join_node.left_vars[0].name].arr_types
                    )
            else:
                dkka__hkf = None
            for hmerr__xbimb, ttc__autrt in jzxiq__zioai.items():
                if hmerr__xbimb < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    dkka__hkf[hmerr__xbimb] = ttc__autrt
                    tygkg__bna = True
                else:
                    aoj__zpd = ttc__autrt
                    xvko__ozw = True
            if tygkg__bna:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(dkka__hkf))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if xvko__ozw:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = aoj__zpd
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({gmup__twqyp[vosp__qqde]}, key_type_{vosp__qqde})'
             if left_key_types[vosp__qqde] != matched_key_types[vosp__qqde]
             else f'{gmup__twqyp[vosp__qqde]}' for vosp__qqde in range(
            pzp__yls)), ',' if pzp__yls != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        jzxiq__zioai = determine_table_cast_map(matched_key_types,
            right_key_types, None, {vosp__qqde: join_node.right_var_map[
            jon__ivq] for vosp__qqde, jon__ivq in enumerate(join_node.
            right_keys)}, True)
        if jzxiq__zioai:
            tygkg__bna = False
            xvko__ozw = False
            aoj__zpd = None
            if join_node.has_live_right_table_var:
                dkka__hkf = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                dkka__hkf = None
            for hmerr__xbimb, ttc__autrt in jzxiq__zioai.items():
                if hmerr__xbimb < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    dkka__hkf[hmerr__xbimb] = ttc__autrt
                    tygkg__bna = True
                else:
                    aoj__zpd = ttc__autrt
                    xvko__ozw = True
            if tygkg__bna:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(dkka__hkf))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if xvko__ozw:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = aoj__zpd
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({zeuju__hdhn[vosp__qqde]}, key_type_{vosp__qqde})'
             if right_key_types[vosp__qqde] != matched_key_types[vosp__qqde
            ] else f'{zeuju__hdhn[vosp__qqde]}' for vosp__qqde in range(
            pzp__yls)), ',' if pzp__yls != 0 else '')
        func_text += '    data_right = ({}{})\n'.format(','.join(
            right_other_names), ',' if len(right_other_names) != 0 else '')
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap,
        left_logical_physical_map, right_logical_physical_map))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel, 'pd.merge_asof requires both left and right to be replicated or distributed'
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_join_cpp_call(join_node, left_key_types,
            right_key_types, matched_key_types, left_other_names,
            right_other_names, left_other_types, right_other_types,
            left_key_in_output, right_key_in_output, left_parallel,
            right_parallel, glbs, out_physical_to_logical_list,
            out_table_type, index_col_type, join_node.
            get_out_table_used_cols(), left_used_key_nums,
            right_used_key_nums, general_cond_cfunc, left_col_nums,
            right_col_nums, left_physical_to_logical_list,
            right_physical_to_logical_list)
    if join_node.how == 'asof':
        for vosp__qqde in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(vosp__qqde,
                vosp__qqde)
        for vosp__qqde in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                vosp__qqde, vosp__qqde)
        for vosp__qqde in range(pzp__yls):
            func_text += (
                f'    t1_keys_{vosp__qqde} = out_t1_keys[{vosp__qqde}]\n')
        for vosp__qqde in range(pzp__yls):
            func_text += (
                f'    t2_keys_{vosp__qqde} = out_t2_keys[{vosp__qqde}]\n')
    joz__vhqv = {}
    exec(func_text, {}, joz__vhqv)
    cpwos__yelc = joz__vhqv['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'cross_join_table': cross_join_table, 'hash_join_table':
        hash_join_table, 'delete_table': delete_table,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr, 'key_in_output': np.array
        (left_key_in_output + right_key_in_output, dtype=np.bool_),
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    uuf__ihig = compile_to_numba_ir(cpwos__yelc, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=pdd__pfp, typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(uuf__ihig, yvc__ucmj)
    gnk__oqded = uuf__ihig.body[:-3]
    if join_node.has_live_out_index_var:
        gnk__oqded[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        gnk__oqded[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        gnk__oqded.pop(-1)
    elif not join_node.has_live_out_table_var:
        gnk__oqded.pop(-2)
    return gnk__oqded


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    fqkr__odp = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{fqkr__odp}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        left_logical_physical_map, join_node.left_var_map, typemap,
        join_node.left_vars, table_getitem_funcs, func_text, 'left',
        join_node.left_key_set, na_check_name, join_node.is_left_table)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        right_logical_physical_map, join_node.right_var_map, typemap,
        join_node.right_vars, table_getitem_funcs, func_text, 'right',
        join_node.right_key_set, na_check_name, join_node.is_right_table)
    expr = expr.replace(' & ', ' and ').replace(' | ', ' or ')
    func_text += f'  return {expr}'
    joz__vhqv = {}
    exec(func_text, table_getitem_funcs, joz__vhqv)
    pii__ykclr = joz__vhqv[f'bodo_join_gen_cond{fqkr__odp}']
    vzut__lro = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    pugay__ywfrv = numba.cfunc(vzut__lro, nopython=True)(pii__ykclr)
    join_gen_cond_cfunc[pugay__ywfrv.native_name] = pugay__ywfrv
    join_gen_cond_cfunc_addr[pugay__ywfrv.native_name] = pugay__ywfrv.address
    return pugay__ywfrv, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    yco__faz = []
    for ule__jib, ntl__qpak in name_to_var_map.items():
        omf__rfw = f'({table_name}.{ule__jib})'
        if omf__rfw not in expr:
            continue
        hlbq__vlfx = f'getitem_{table_name}_val_{ntl__qpak}'
        if is_table_var:
            ele__toavc = typemap[col_vars[0].name].arr_types[ntl__qpak]
        else:
            ele__toavc = typemap[col_vars[ntl__qpak].name]
        if is_str_arr_type(ele__toavc) or ele__toavc == bodo.binary_array_type:
            kka__nnj = f'{hlbq__vlfx}({table_name}_table, {table_name}_ind)\n'
        else:
            kka__nnj = f'{hlbq__vlfx}({table_name}_data1, {table_name}_ind)\n'
        dmolj__qxpz = logical_to_physical_ind[ntl__qpak]
        table_getitem_funcs[hlbq__vlfx
            ] = bodo.libs.array._gen_row_access_intrinsic(ele__toavc,
            dmolj__qxpz)
        expr = expr.replace(omf__rfw, kka__nnj)
        uphy__dgmqe = f'({na_check_name}.{table_name}.{ule__jib})'
        if uphy__dgmqe in expr:
            yswe__ajeku = f'nacheck_{table_name}_val_{ntl__qpak}'
            hpxb__ytwhp = f'_bodo_isna_{table_name}_val_{ntl__qpak}'
            if isinstance(ele__toavc, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or ele__toavc in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(ele__toavc):
                func_text += f"""  {hpxb__ytwhp} = {yswe__ajeku}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {hpxb__ytwhp} = {yswe__ajeku}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[yswe__ajeku
                ] = bodo.libs.array._gen_row_na_check_intrinsic(ele__toavc,
                dmolj__qxpz)
            expr = expr.replace(uphy__dgmqe, hpxb__ytwhp)
        if ntl__qpak not in key_set:
            yco__faz.append(dmolj__qxpz)
    return expr, func_text, yco__faz


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as zjnp__wrf:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    rbpkh__yoy = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[almwy__gccb.name] in rbpkh__yoy for
        almwy__gccb in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in rbpkh__yoy
    right_parallel = all(array_dists[almwy__gccb.name] in rbpkh__yoy for
        almwy__gccb in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in rbpkh__yoy
    if not left_parallel:
        assert not any(array_dists[almwy__gccb.name] in rbpkh__yoy for
            almwy__gccb in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[almwy__gccb.name] in rbpkh__yoy for
            almwy__gccb in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[almwy__gccb.name] in rbpkh__yoy for
            almwy__gccb in join_node.get_live_out_vars())
    return left_parallel, right_parallel


def _gen_join_cpp_call(join_node, left_key_types, right_key_types,
    matched_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, left_key_in_output,
    right_key_in_output, left_parallel, right_parallel, glbs,
    out_physical_to_logical_list, out_table_type, index_col_type,
    out_table_used_cols, left_used_key_nums, right_used_key_nums,
    general_cond_cfunc, left_col_nums, right_col_nums,
    left_physical_to_logical_list, right_physical_to_logical_list):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    whc__ezzs = set(left_col_nums)
    uoq__gsop = set(right_col_nums)
    fsxnl__hcj = join_node.vect_same_key
    hebq__aiapb = []
    for vosp__qqde in range(len(left_key_types)):
        if left_key_in_output[vosp__qqde]:
            hebq__aiapb.append(needs_typechange(matched_key_types[
                vosp__qqde], join_node.is_right, fsxnl__hcj[vosp__qqde]))
    rpshh__jred = len(left_key_types)
    luwo__bhwe = 0
    duzxp__nba = left_physical_to_logical_list[len(left_key_types):]
    for vosp__qqde, uoyid__frza in enumerate(duzxp__nba):
        hvxfp__dhtpr = True
        if uoyid__frza in whc__ezzs:
            hvxfp__dhtpr = left_key_in_output[rpshh__jred]
            rpshh__jred += 1
        if hvxfp__dhtpr:
            hebq__aiapb.append(needs_typechange(left_other_types[vosp__qqde
                ], join_node.is_right, False))
    for vosp__qqde in range(len(right_key_types)):
        if not fsxnl__hcj[vosp__qqde] and not join_node.is_join:
            if right_key_in_output[luwo__bhwe]:
                hebq__aiapb.append(needs_typechange(matched_key_types[
                    vosp__qqde], join_node.is_left, False))
            luwo__bhwe += 1
    mme__loow = right_physical_to_logical_list[len(right_key_types):]
    for vosp__qqde, uoyid__frza in enumerate(mme__loow):
        hvxfp__dhtpr = True
        if uoyid__frza in uoq__gsop:
            hvxfp__dhtpr = right_key_in_output[luwo__bhwe]
            luwo__bhwe += 1
        if hvxfp__dhtpr:
            hebq__aiapb.append(needs_typechange(right_other_types[
                vosp__qqde], join_node.is_left, False))
    pzp__yls = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            llq__hleo = left_other_names[1:]
            elv__trj = left_other_names[0]
        else:
            llq__hleo = left_other_names
            elv__trj = None
        ngtoc__svn = '()' if len(llq__hleo) == 0 else f'({llq__hleo[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({elv__trj}, {ngtoc__svn}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        rly__tvjd = []
        for vosp__qqde in range(pzp__yls):
            rly__tvjd.append('t1_keys[{}]'.format(vosp__qqde))
        for vosp__qqde in range(len(left_other_names)):
            rly__tvjd.append('data_left[{}]'.format(vosp__qqde))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(uwwcg__rukgk) for uwwcg__rukgk in
            rly__tvjd))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            kwxbi__quxo = right_other_names[1:]
            elv__trj = right_other_names[0]
        else:
            kwxbi__quxo = right_other_names
            elv__trj = None
        ngtoc__svn = '()' if len(kwxbi__quxo) == 0 else f'({kwxbi__quxo[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({elv__trj}, {ngtoc__svn}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        jmj__dtxda = []
        for vosp__qqde in range(pzp__yls):
            jmj__dtxda.append('t2_keys[{}]'.format(vosp__qqde))
        for vosp__qqde in range(len(right_other_names)):
            jmj__dtxda.append('data_right[{}]'.format(vosp__qqde))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(uwwcg__rukgk) for uwwcg__rukgk in
            jmj__dtxda))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(fsxnl__hcj, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(hebq__aiapb, dtype=np.int64)
    glbs['left_table_cond_columns'] = np.array(left_col_nums if len(
        left_col_nums) > 0 else [-1], dtype=np.int64)
    glbs['right_table_cond_columns'] = np.array(right_col_nums if len(
        right_col_nums) > 0 else [-1], dtype=np.int64)
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    if join_node.how == 'cross' or not join_node.left_keys:
        func_text += f"""    out_table = cross_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {join_node.is_left}, {join_node.is_right}, key_in_output.ctypes, use_nullable_arr_type.ctypes, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    else:
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {pzp__yls}, {len(duzxp__nba)}, {len(mme__loow)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    rpvse__gmxh = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {rpvse__gmxh}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        vypjb__wjzsk = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{vypjb__wjzsk}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        cgigm__cch = {}
        for vosp__qqde, jon__ivq in enumerate(join_node.left_keys):
            if vosp__qqde in left_used_key_nums:
                obwsw__aivhi = join_node.left_var_map[jon__ivq]
                cgigm__cch[vosp__qqde] = join_node.left_to_output_map[
                    obwsw__aivhi]
        jzxiq__zioai = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, cgigm__cch, False)
        tsudy__ptuhh = {}
        for vosp__qqde, jon__ivq in enumerate(join_node.right_keys):
            if vosp__qqde in right_used_key_nums:
                obwsw__aivhi = join_node.right_var_map[jon__ivq]
                tsudy__ptuhh[vosp__qqde] = join_node.right_to_output_map[
                    obwsw__aivhi]
        jzxiq__zioai.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, tsudy__ptuhh, False))
        tygkg__bna = False
        xvko__ozw = False
        if join_node.has_live_out_table_var:
            dkka__hkf = list(out_table_type.arr_types)
        else:
            dkka__hkf = None
        for hmerr__xbimb, ttc__autrt in jzxiq__zioai.items():
            if hmerr__xbimb < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                dkka__hkf[hmerr__xbimb] = ttc__autrt
                tygkg__bna = True
            else:
                aoj__zpd = ttc__autrt
                xvko__ozw = True
        if tygkg__bna:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            miit__nhq = bodo.TableType(tuple(dkka__hkf))
            glbs['py_table_type'] = miit__nhq
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if xvko__ozw:
            glbs['index_col_type'] = aoj__zpd
            glbs['index_cast_type'] = index_col_type
            func_text += (
                f'    index_var = bodo.utils.utils.astype(index_var, index_cast_type)\n'
                )
    func_text += f'    out_table = T\n'
    func_text += f'    out_index = index_var\n'
    return func_text


def determine_table_cast_map(matched_key_types: List[types.Type], key_types:
    List[types.Type], used_key_nums: Optional[Set[int]], output_map: Dict[
    int, int], convert_dict_col: bool):
    jzxiq__zioai: Dict[int, types.Type] = {}
    pzp__yls = len(matched_key_types)
    for vosp__qqde in range(pzp__yls):
        if used_key_nums is None or vosp__qqde in used_key_nums:
            if matched_key_types[vosp__qqde] != key_types[vosp__qqde] and (
                convert_dict_col or key_types[vosp__qqde] != bodo.
                dict_str_arr_type):
                vypjb__wjzsk = output_map[vosp__qqde]
                jzxiq__zioai[vypjb__wjzsk] = matched_key_types[vosp__qqde]
    return jzxiq__zioai


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    zksfb__gark = bodo.libs.distributed_api.get_size()
    efim__hnf = np.empty(zksfb__gark, left_key_arrs[0].dtype)
    rjn__ucwvx = np.empty(zksfb__gark, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(efim__hnf, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(rjn__ucwvx, left_key_arrs[0][-1])
    sqh__iuy = np.zeros(zksfb__gark, np.int32)
    gaf__ooej = np.zeros(zksfb__gark, np.int32)
    jhshr__prod = np.zeros(zksfb__gark, np.int32)
    jfh__dhm = right_key_arrs[0][0]
    cvhk__izyjc = right_key_arrs[0][-1]
    qayoh__fxq = -1
    vosp__qqde = 0
    while vosp__qqde < zksfb__gark - 1 and rjn__ucwvx[vosp__qqde] < jfh__dhm:
        vosp__qqde += 1
    while vosp__qqde < zksfb__gark and efim__hnf[vosp__qqde] <= cvhk__izyjc:
        qayoh__fxq, qdkxs__uhlcy = _count_overlap(right_key_arrs[0],
            efim__hnf[vosp__qqde], rjn__ucwvx[vosp__qqde])
        if qayoh__fxq != 0:
            qayoh__fxq -= 1
            qdkxs__uhlcy += 1
        sqh__iuy[vosp__qqde] = qdkxs__uhlcy
        gaf__ooej[vosp__qqde] = qayoh__fxq
        vosp__qqde += 1
    while vosp__qqde < zksfb__gark:
        sqh__iuy[vosp__qqde] = 1
        gaf__ooej[vosp__qqde] = len(right_key_arrs[0]) - 1
        vosp__qqde += 1
    bodo.libs.distributed_api.alltoall(sqh__iuy, jhshr__prod, 1)
    nscy__wdalq = jhshr__prod.sum()
    ymld__xlq = np.empty(nscy__wdalq, right_key_arrs[0].dtype)
    xqbck__qwqh = alloc_arr_tup(nscy__wdalq, right_data)
    ekv__hfz = bodo.ir.join.calc_disp(jhshr__prod)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], ymld__xlq,
        sqh__iuy, jhshr__prod, gaf__ooej, ekv__hfz)
    bodo.libs.distributed_api.alltoallv_tup(right_data, xqbck__qwqh,
        sqh__iuy, jhshr__prod, gaf__ooej, ekv__hfz)
    return (ymld__xlq,), xqbck__qwqh


@numba.njit
def _count_overlap(r_key_arr, start, end):
    qdkxs__uhlcy = 0
    qayoh__fxq = 0
    mleqn__syrow = 0
    while mleqn__syrow < len(r_key_arr) and r_key_arr[mleqn__syrow] < start:
        qayoh__fxq += 1
        mleqn__syrow += 1
    while mleqn__syrow < len(r_key_arr) and start <= r_key_arr[mleqn__syrow
        ] <= end:
        mleqn__syrow += 1
        qdkxs__uhlcy += 1
    return qayoh__fxq, qdkxs__uhlcy


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    dhgu__qctp = np.empty_like(arr)
    dhgu__qctp[0] = 0
    for vosp__qqde in range(1, len(arr)):
        dhgu__qctp[vosp__qqde] = dhgu__qctp[vosp__qqde - 1] + arr[
            vosp__qqde - 1]
    return dhgu__qctp


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    itu__uzm = len(left_keys[0])
    rvpl__jivc = len(right_keys[0])
    nfmwi__pkf = alloc_arr_tup(itu__uzm, left_keys)
    ama__ldgl = alloc_arr_tup(itu__uzm, right_keys)
    attma__tef = alloc_arr_tup(itu__uzm, data_left)
    qey__efc = alloc_arr_tup(itu__uzm, data_right)
    kxlg__zjxz = 0
    nvwe__zgxdl = 0
    for kxlg__zjxz in range(itu__uzm):
        if nvwe__zgxdl < 0:
            nvwe__zgxdl = 0
        while nvwe__zgxdl < rvpl__jivc and getitem_arr_tup(right_keys,
            nvwe__zgxdl) <= getitem_arr_tup(left_keys, kxlg__zjxz):
            nvwe__zgxdl += 1
        nvwe__zgxdl -= 1
        setitem_arr_tup(nfmwi__pkf, kxlg__zjxz, getitem_arr_tup(left_keys,
            kxlg__zjxz))
        setitem_arr_tup(attma__tef, kxlg__zjxz, getitem_arr_tup(data_left,
            kxlg__zjxz))
        if nvwe__zgxdl >= 0:
            setitem_arr_tup(ama__ldgl, kxlg__zjxz, getitem_arr_tup(
                right_keys, nvwe__zgxdl))
            setitem_arr_tup(qey__efc, kxlg__zjxz, getitem_arr_tup(
                data_right, nvwe__zgxdl))
        else:
            bodo.libs.array_kernels.setna_tup(ama__ldgl, kxlg__zjxz)
            bodo.libs.array_kernels.setna_tup(qey__efc, kxlg__zjxz)
    return nfmwi__pkf, ama__ldgl, attma__tef, qey__efc
