"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        peep_hole_fuse_tuple_adds(state.func_ir)
        return True


def peep_hole_fuse_tuple_adds(func_ir):
    for wyox__vyyrp in func_ir.blocks.values():
        new_body = []
        cgvj__cgg = {}
        for vzvh__wunb, cjqv__rws in enumerate(wyox__vyyrp.body):
            fkd__lwjd = None
            if isinstance(cjqv__rws, ir.Assign) and isinstance(cjqv__rws.
                value, ir.Expr):
                rts__umuh = cjqv__rws.target.name
                if cjqv__rws.value.op == 'build_tuple':
                    fkd__lwjd = rts__umuh
                    cgvj__cgg[rts__umuh] = cjqv__rws.value.items
                elif cjqv__rws.value.op == 'binop' and cjqv__rws.value.fn == operator.add and cjqv__rws.value.lhs.name in cgvj__cgg and cjqv__rws.value.rhs.name in cgvj__cgg:
                    fkd__lwjd = rts__umuh
                    new_items = cgvj__cgg[cjqv__rws.value.lhs.name
                        ] + cgvj__cgg[cjqv__rws.value.rhs.name]
                    cmzi__wlmtj = ir.Expr.build_tuple(new_items, cjqv__rws.
                        value.loc)
                    cgvj__cgg[rts__umuh] = new_items
                    del cgvj__cgg[cjqv__rws.value.lhs.name]
                    del cgvj__cgg[cjqv__rws.value.rhs.name]
                    if cjqv__rws.value in func_ir._definitions[rts__umuh]:
                        func_ir._definitions[rts__umuh].remove(cjqv__rws.value)
                    func_ir._definitions[rts__umuh].append(cmzi__wlmtj)
                    cjqv__rws = ir.Assign(cmzi__wlmtj, cjqv__rws.target,
                        cjqv__rws.loc)
            for ueydv__dajo in cjqv__rws.list_vars():
                if (ueydv__dajo.name in cgvj__cgg and ueydv__dajo.name !=
                    fkd__lwjd):
                    del cgvj__cgg[ueydv__dajo.name]
            new_body.append(cjqv__rws)
        wyox__vyyrp.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    ohuq__dbrr = keyword_expr.items.copy()
    jnzrz__lgbni = keyword_expr.value_indexes
    for fyz__gpq, zhm__tnye in jnzrz__lgbni.items():
        ohuq__dbrr[zhm__tnye] = fyz__gpq, ohuq__dbrr[zhm__tnye][1]
    new_body[buildmap_idx] = None
    return ohuq__dbrr


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    nxe__tytsi = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    ohuq__dbrr = []
    mlbln__gde = buildmap_idx + 1
    while mlbln__gde <= search_end:
        hhplv__qjnz = body[mlbln__gde]
        if not (isinstance(hhplv__qjnz, ir.Assign) and isinstance(
            hhplv__qjnz.value, ir.Const)):
            raise UnsupportedError(nxe__tytsi)
        ico__swwuc = hhplv__qjnz.target.name
        qcj__kkb = hhplv__qjnz.value.value
        mlbln__gde += 1
        iggk__stm = True
        while mlbln__gde <= search_end and iggk__stm:
            rdcuc__rrmc = body[mlbln__gde]
            if (isinstance(rdcuc__rrmc, ir.Assign) and isinstance(
                rdcuc__rrmc.value, ir.Expr) and rdcuc__rrmc.value.op ==
                'getattr' and rdcuc__rrmc.value.value.name == buildmap_name and
                rdcuc__rrmc.value.attr == '__setitem__'):
                iggk__stm = False
            else:
                mlbln__gde += 1
        if iggk__stm or mlbln__gde == search_end:
            raise UnsupportedError(nxe__tytsi)
        erc__swy = body[mlbln__gde + 1]
        if not (isinstance(erc__swy, ir.Assign) and isinstance(erc__swy.
            value, ir.Expr) and erc__swy.value.op == 'call' and erc__swy.
            value.func.name == rdcuc__rrmc.target.name and len(erc__swy.
            value.args) == 2 and erc__swy.value.args[0].name == ico__swwuc):
            raise UnsupportedError(nxe__tytsi)
        xwu__inzyd = erc__swy.value.args[1]
        ohuq__dbrr.append((qcj__kkb, xwu__inzyd))
        new_body[mlbln__gde] = None
        new_body[mlbln__gde + 1] = None
        mlbln__gde += 2
    return ohuq__dbrr


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    nxe__tytsi = 'CALL_FUNCTION_EX with **kwargs not supported'
    mlbln__gde = 0
    wog__grvu = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        xsnaz__uikr = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        xsnaz__uikr = vararg_stmt.target.name
    ztj__oviih = True
    while search_end >= mlbln__gde and ztj__oviih:
        daus__vpj = body[search_end]
        if (isinstance(daus__vpj, ir.Assign) and daus__vpj.target.name ==
            xsnaz__uikr and isinstance(daus__vpj.value, ir.Expr) and 
            daus__vpj.value.op == 'build_tuple' and not daus__vpj.value.items):
            ztj__oviih = False
            new_body[search_end] = None
        else:
            if search_end == mlbln__gde or not (isinstance(daus__vpj, ir.
                Assign) and daus__vpj.target.name == xsnaz__uikr and
                isinstance(daus__vpj.value, ir.Expr) and daus__vpj.value.op ==
                'binop' and daus__vpj.value.fn == operator.add):
                raise UnsupportedError(nxe__tytsi)
            ilgl__tsp = daus__vpj.value.lhs.name
            zfszu__flljp = daus__vpj.value.rhs.name
            aob__zca = body[search_end - 1]
            if not (isinstance(aob__zca, ir.Assign) and isinstance(aob__zca
                .value, ir.Expr) and aob__zca.value.op == 'build_tuple' and
                len(aob__zca.value.items) == 1):
                raise UnsupportedError(nxe__tytsi)
            if aob__zca.target.name == ilgl__tsp:
                xsnaz__uikr = zfszu__flljp
            elif aob__zca.target.name == zfszu__flljp:
                xsnaz__uikr = ilgl__tsp
            else:
                raise UnsupportedError(nxe__tytsi)
            wog__grvu.append(aob__zca.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            pwk__hzhtn = True
            while search_end >= mlbln__gde and pwk__hzhtn:
                dbrnu__xnwj = body[search_end]
                if isinstance(dbrnu__xnwj, ir.Assign
                    ) and dbrnu__xnwj.target.name == xsnaz__uikr:
                    pwk__hzhtn = False
                else:
                    search_end -= 1
    if ztj__oviih:
        raise UnsupportedError(nxe__tytsi)
    return wog__grvu[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    nxe__tytsi = 'CALL_FUNCTION_EX with **kwargs not supported'
    for wyox__vyyrp in func_ir.blocks.values():
        uhn__hwhvn = False
        new_body = []
        for vzvh__wunb, cjqv__rws in enumerate(wyox__vyyrp.body):
            if (isinstance(cjqv__rws, ir.Assign) and isinstance(cjqv__rws.
                value, ir.Expr) and cjqv__rws.value.op == 'call' and 
                cjqv__rws.value.varkwarg is not None):
                uhn__hwhvn = True
                plnue__dozer = cjqv__rws.value
                args = plnue__dozer.args
                ohuq__dbrr = plnue__dozer.kws
                kasse__nqwu = plnue__dozer.vararg
                fud__zlcmz = plnue__dozer.varkwarg
                sstmm__pan = vzvh__wunb - 1
                nzxw__bze = sstmm__pan
                btscr__dhhz = None
                tmi__dfm = True
                while nzxw__bze >= 0 and tmi__dfm:
                    btscr__dhhz = wyox__vyyrp.body[nzxw__bze]
                    if isinstance(btscr__dhhz, ir.Assign
                        ) and btscr__dhhz.target.name == fud__zlcmz.name:
                        tmi__dfm = False
                    else:
                        nzxw__bze -= 1
                if ohuq__dbrr or tmi__dfm or not (isinstance(btscr__dhhz.
                    value, ir.Expr) and btscr__dhhz.value.op == 'build_map'):
                    raise UnsupportedError(nxe__tytsi)
                if btscr__dhhz.value.items:
                    ohuq__dbrr = _call_function_ex_replace_kws_small(
                        btscr__dhhz.value, new_body, nzxw__bze)
                else:
                    ohuq__dbrr = _call_function_ex_replace_kws_large(
                        wyox__vyyrp.body, fud__zlcmz.name, nzxw__bze, 
                        vzvh__wunb - 1, new_body)
                sstmm__pan = nzxw__bze
                if kasse__nqwu is not None:
                    if args:
                        raise UnsupportedError(nxe__tytsi)
                    jww__dgja = sstmm__pan
                    dwn__pwck = None
                    tmi__dfm = True
                    while jww__dgja >= 0 and tmi__dfm:
                        dwn__pwck = wyox__vyyrp.body[jww__dgja]
                        if isinstance(dwn__pwck, ir.Assign
                            ) and dwn__pwck.target.name == kasse__nqwu.name:
                            tmi__dfm = False
                        else:
                            jww__dgja -= 1
                    if tmi__dfm:
                        raise UnsupportedError(nxe__tytsi)
                    if isinstance(dwn__pwck.value, ir.Expr
                        ) and dwn__pwck.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(dwn__pwck
                            .value, new_body, jww__dgja)
                    else:
                        args = _call_function_ex_replace_args_large(dwn__pwck,
                            wyox__vyyrp.body, new_body, jww__dgja)
                gluc__jvgiy = ir.Expr.call(plnue__dozer.func, args,
                    ohuq__dbrr, plnue__dozer.loc, target=plnue__dozer.target)
                if cjqv__rws.target.name in func_ir._definitions and len(
                    func_ir._definitions[cjqv__rws.target.name]) == 1:
                    func_ir._definitions[cjqv__rws.target.name].clear()
                func_ir._definitions[cjqv__rws.target.name].append(gluc__jvgiy)
                cjqv__rws = ir.Assign(gluc__jvgiy, cjqv__rws.target,
                    cjqv__rws.loc)
            new_body.append(cjqv__rws)
        if uhn__hwhvn:
            wyox__vyyrp.body = [mnw__qty for mnw__qty in new_body if 
                mnw__qty is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for wyox__vyyrp in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        uhn__hwhvn = False
        for vzvh__wunb, cjqv__rws in enumerate(wyox__vyyrp.body):
            rtnr__jgce = True
            crzjr__zuk = None
            if isinstance(cjqv__rws, ir.Assign) and isinstance(cjqv__rws.
                value, ir.Expr):
                if cjqv__rws.value.op == 'build_map':
                    crzjr__zuk = cjqv__rws.target.name
                    lit_old_idx[cjqv__rws.target.name] = vzvh__wunb
                    lit_new_idx[cjqv__rws.target.name] = vzvh__wunb
                    map_updates[cjqv__rws.target.name
                        ] = cjqv__rws.value.items.copy()
                    rtnr__jgce = False
                elif cjqv__rws.value.op == 'call' and vzvh__wunb > 0:
                    nza__kmyzu = cjqv__rws.value.func.name
                    rdcuc__rrmc = wyox__vyyrp.body[vzvh__wunb - 1]
                    args = cjqv__rws.value.args
                    if (isinstance(rdcuc__rrmc, ir.Assign) and rdcuc__rrmc.
                        target.name == nza__kmyzu and isinstance(
                        rdcuc__rrmc.value, ir.Expr) and rdcuc__rrmc.value.
                        op == 'getattr' and rdcuc__rrmc.value.value.name in
                        lit_old_idx):
                        ksr__quuv = rdcuc__rrmc.value.value.name
                        dcs__xui = rdcuc__rrmc.value.attr
                        if dcs__xui == '__setitem__':
                            rtnr__jgce = False
                            map_updates[ksr__quuv].append(args)
                            new_body[-1] = None
                        elif dcs__xui == 'update' and args[0
                            ].name in lit_old_idx:
                            rtnr__jgce = False
                            map_updates[ksr__quuv].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not rtnr__jgce:
                            lit_new_idx[ksr__quuv] = vzvh__wunb
                            func_ir._definitions[rdcuc__rrmc.target.name
                                ].remove(rdcuc__rrmc.value)
            if not (isinstance(cjqv__rws, ir.Assign) and isinstance(
                cjqv__rws.value, ir.Expr) and cjqv__rws.value.op ==
                'getattr' and cjqv__rws.value.value.name in lit_old_idx and
                cjqv__rws.value.attr in ('__setitem__', 'update')):
                for ueydv__dajo in cjqv__rws.list_vars():
                    if (ueydv__dajo.name in lit_old_idx and ueydv__dajo.
                        name != crzjr__zuk):
                        _insert_build_map(func_ir, ueydv__dajo.name,
                            wyox__vyyrp.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if rtnr__jgce:
                new_body.append(cjqv__rws)
            else:
                func_ir._definitions[cjqv__rws.target.name].remove(cjqv__rws
                    .value)
                uhn__hwhvn = True
                new_body.append(None)
        epy__han = list(lit_old_idx.keys())
        for ayc__cky in epy__han:
            _insert_build_map(func_ir, ayc__cky, wyox__vyyrp.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if uhn__hwhvn:
            wyox__vyyrp.body = [mnw__qty for mnw__qty in new_body if 
                mnw__qty is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    qen__lvbut = lit_old_idx[name]
    corq__rvxw = lit_new_idx[name]
    yqzj__vje = map_updates[name]
    new_body[corq__rvxw] = _build_new_build_map(func_ir, name, old_body,
        qen__lvbut, yqzj__vje)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    vxi__frs = old_body[old_lineno]
    tqc__zjec = vxi__frs.target
    pyhx__acc = vxi__frs.value
    htgem__yxnv = []
    gnw__xwctw = []
    for zylco__esb in new_items:
        rdab__owp, vrmn__dzf = zylco__esb
        gwi__kkjki = guard(get_definition, func_ir, rdab__owp)
        if isinstance(gwi__kkjki, (ir.Const, ir.Global, ir.FreeVar)):
            htgem__yxnv.append(gwi__kkjki.value)
        nuj__nxmns = guard(get_definition, func_ir, vrmn__dzf)
        if isinstance(nuj__nxmns, (ir.Const, ir.Global, ir.FreeVar)):
            gnw__xwctw.append(nuj__nxmns.value)
        else:
            gnw__xwctw.append(numba.core.interpreter._UNKNOWN_VALUE(
                vrmn__dzf.name))
    jnzrz__lgbni = {}
    if len(htgem__yxnv) == len(new_items):
        zkcjs__vlnl = {mnw__qty: fiokb__duuoe for mnw__qty, fiokb__duuoe in
            zip(htgem__yxnv, gnw__xwctw)}
        for vzvh__wunb, rdab__owp in enumerate(htgem__yxnv):
            jnzrz__lgbni[rdab__owp] = vzvh__wunb
    else:
        zkcjs__vlnl = None
    dty__sinca = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=zkcjs__vlnl, value_indexes=jnzrz__lgbni, loc=
        pyhx__acc.loc)
    func_ir._definitions[name].append(dty__sinca)
    return ir.Assign(dty__sinca, ir.Var(tqc__zjec.scope, name, tqc__zjec.
        loc), dty__sinca.loc)
