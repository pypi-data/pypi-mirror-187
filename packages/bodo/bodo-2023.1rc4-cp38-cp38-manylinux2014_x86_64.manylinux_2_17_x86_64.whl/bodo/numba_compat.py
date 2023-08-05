"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, get_definition, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates, peep_hole_fuse_tuple_adds
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    vrg__dox = numba.core.bytecode.FunctionIdentity.from_function(func)
    hrdzc__nurjr = numba.core.interpreter.Interpreter(vrg__dox)
    yet__ebs = numba.core.bytecode.ByteCode(func_id=vrg__dox)
    func_ir = hrdzc__nurjr.interpret(yet__ebs)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
        func_ir = peep_hole_fuse_tuple_adds(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        zkz__dum = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        zkz__dum.run()
    she__ivuru = numba.core.postproc.PostProcessor(func_ir)
    she__ivuru.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, irk__kiq in visit_vars_extensions.items():
        if isinstance(stmt, t):
            irk__kiq(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    hfpl__jin = ['ravel', 'transpose', 'reshape']
    for tomm__gxiih in blocks.values():
        for dpk__qlzph in tomm__gxiih.body:
            if type(dpk__qlzph) in alias_analysis_extensions:
                irk__kiq = alias_analysis_extensions[type(dpk__qlzph)]
                irk__kiq(dpk__qlzph, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(dpk__qlzph, ir.Assign):
                wtws__kngz = dpk__qlzph.value
                wte__fqbz = dpk__qlzph.target.name
                if is_immutable_type(wte__fqbz, typemap):
                    continue
                if isinstance(wtws__kngz, ir.Var
                    ) and wte__fqbz != wtws__kngz.name:
                    _add_alias(wte__fqbz, wtws__kngz.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr) and (wtws__kngz.op ==
                    'cast' or wtws__kngz.op in ['getitem', 'static_getitem']):
                    _add_alias(wte__fqbz, wtws__kngz.value.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr
                    ) and wtws__kngz.op == 'inplace_binop':
                    _add_alias(wte__fqbz, wtws__kngz.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr
                    ) and wtws__kngz.op == 'getattr' and wtws__kngz.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(wte__fqbz, wtws__kngz.value.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr
                    ) and wtws__kngz.op == 'getattr' and wtws__kngz.attr not in [
                    'shape'] and wtws__kngz.value.name in arg_aliases:
                    _add_alias(wte__fqbz, wtws__kngz.value.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr
                    ) and wtws__kngz.op == 'getattr' and wtws__kngz.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(wte__fqbz, wtws__kngz.value.name, alias_map,
                        arg_aliases)
                if isinstance(wtws__kngz, ir.Expr) and wtws__kngz.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(wte__fqbz, typemap):
                    for yjq__ijhy in wtws__kngz.items:
                        _add_alias(wte__fqbz, yjq__ijhy.name, alias_map,
                            arg_aliases)
                if isinstance(wtws__kngz, ir.Expr) and wtws__kngz.op == 'call':
                    ymyek__pmy = guard(find_callname, func_ir, wtws__kngz,
                        typemap)
                    if ymyek__pmy is None:
                        continue
                    svjxc__wwmsi, gxp__dyciz = ymyek__pmy
                    if ymyek__pmy in alias_func_extensions:
                        xkl__ufzvx = alias_func_extensions[ymyek__pmy]
                        xkl__ufzvx(wte__fqbz, wtws__kngz.args, alias_map,
                            arg_aliases)
                    if gxp__dyciz == 'numpy' and svjxc__wwmsi in hfpl__jin:
                        _add_alias(wte__fqbz, wtws__kngz.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(gxp__dyciz, ir.Var
                        ) and svjxc__wwmsi in hfpl__jin:
                        _add_alias(wte__fqbz, gxp__dyciz.name, alias_map,
                            arg_aliases)
    dgpt__xtcv = copy.deepcopy(alias_map)
    for yjq__ijhy in dgpt__xtcv:
        for bck__opg in dgpt__xtcv[yjq__ijhy]:
            alias_map[yjq__ijhy] |= alias_map[bck__opg]
        for bck__opg in dgpt__xtcv[yjq__ijhy]:
            alias_map[bck__opg] = alias_map[yjq__ijhy]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    jfi__tqnw = compute_cfg_from_blocks(func_ir.blocks)
    ham__dnemk = compute_use_defs(func_ir.blocks)
    jzy__eaqv = compute_live_map(jfi__tqnw, func_ir.blocks, ham__dnemk.
        usemap, ham__dnemk.defmap)
    ezvns__ddnvi = True
    while ezvns__ddnvi:
        ezvns__ddnvi = False
        for label, block in func_ir.blocks.items():
            lives = {yjq__ijhy.name for yjq__ijhy in block.terminator.
                list_vars()}
            for ntyzj__xsa, zjdo__cjltd in jfi__tqnw.successors(label):
                lives |= jzy__eaqv[ntyzj__xsa]
            riaiu__kur = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    wte__fqbz = stmt.target
                    gop__pgu = stmt.value
                    if wte__fqbz.name not in lives:
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'make_function':
                            continue
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'getattr':
                            continue
                        if isinstance(gop__pgu, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(wte__fqbz,
                            None), types.Function):
                            continue
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'build_map':
                            continue
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'build_tuple':
                            continue
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'binop':
                            continue
                        if isinstance(gop__pgu, ir.Expr
                            ) and gop__pgu.op == 'unary':
                            continue
                        if isinstance(gop__pgu, ir.Expr) and gop__pgu.op in (
                            'static_getitem', 'getitem'):
                            continue
                    if isinstance(gop__pgu, ir.Var
                        ) and wte__fqbz.name == gop__pgu.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    ydxk__hmll = analysis.ir_extension_usedefs[type(stmt)]
                    laxg__rwfvt, zbxve__cxt = ydxk__hmll(stmt)
                    lives -= zbxve__cxt
                    lives |= laxg__rwfvt
                else:
                    lives |= {yjq__ijhy.name for yjq__ijhy in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        auq__huxhg = set()
                        if isinstance(gop__pgu, ir.Expr):
                            auq__huxhg = {yjq__ijhy.name for yjq__ijhy in
                                gop__pgu.list_vars()}
                        if wte__fqbz.name not in auq__huxhg:
                            lives.remove(wte__fqbz.name)
                riaiu__kur.append(stmt)
            riaiu__kur.reverse()
            if len(block.body) != len(riaiu__kur):
                ezvns__ddnvi = True
            block.body = riaiu__kur


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    mweoq__dyn = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (mweoq__dyn,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    jozv__yhht = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), jozv__yhht)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for bem__zhj in fnty.templates:
                self._inline_overloads.update(bem__zhj._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    jozv__yhht = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), jozv__yhht)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    oukq__axflo, opfio__yki = self._get_impl(args, kws)
    if oukq__axflo is None:
        return
    pzmb__hwizp = types.Dispatcher(oukq__axflo)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        wxaf__wvrho = oukq__axflo._compiler
        flags = compiler.Flags()
        gau__zzvpc = wxaf__wvrho.targetdescr.typing_context
        pbjb__cvs = wxaf__wvrho.targetdescr.target_context
        vth__kjg = wxaf__wvrho.pipeline_class(gau__zzvpc, pbjb__cvs, None,
            None, None, flags, None)
        ufpr__zic = InlineWorker(gau__zzvpc, pbjb__cvs, wxaf__wvrho.locals,
            vth__kjg, flags, None)
        diixm__dkwdd = pzmb__hwizp.dispatcher.get_call_template
        bem__zhj, ezof__qlhfw, dduf__qbvdx, kws = diixm__dkwdd(opfio__yki, kws)
        if dduf__qbvdx in self._inline_overloads:
            return self._inline_overloads[dduf__qbvdx]['iinfo'].signature
        ir = ufpr__zic.run_untyped_passes(pzmb__hwizp.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, pbjb__cvs, ir, dduf__qbvdx, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, dduf__qbvdx, None)
        self._inline_overloads[sig.args] = {'folded_args': dduf__qbvdx}
        bnd__xub = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = bnd__xub
        if not self._inline.is_always_inline:
            sig = pzmb__hwizp.get_call_type(self.context, opfio__yki, kws)
            self._compiled_overloads[sig.args] = pzmb__hwizp.get_overload(sig)
        ncni__pjytn = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': dduf__qbvdx,
            'iinfo': ncni__pjytn}
    else:
        sig = pzmb__hwizp.get_call_type(self.context, opfio__yki, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = pzmb__hwizp.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    fpnvh__uqky = [True, False]
    kmng__iykp = [False, True]
    uurki__xonp = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    iuahh__wodt = get_local_target(context)
    cnnsf__rqyz = utils.order_by_target_specificity(iuahh__wodt, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for ptwv__uci in cnnsf__rqyz:
        psyy__zbl = ptwv__uci(context)
        tucj__vze = fpnvh__uqky if psyy__zbl.prefer_literal else kmng__iykp
        tucj__vze = [True] if getattr(psyy__zbl, '_no_unliteral', False
            ) else tucj__vze
        for uerg__jsb in tucj__vze:
            try:
                if uerg__jsb:
                    sig = psyy__zbl.apply(args, kws)
                else:
                    vqztq__hmk = tuple([_unlit_non_poison(a) for a in args])
                    dvier__duv = {bykga__pfe: _unlit_non_poison(yjq__ijhy) for
                        bykga__pfe, yjq__ijhy in kws.items()}
                    sig = psyy__zbl.apply(vqztq__hmk, dvier__duv)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    uurki__xonp.add_error(psyy__zbl, False, e, uerg__jsb)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = psyy__zbl.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    otup__iabuz = getattr(psyy__zbl, 'cases', None)
                    if otup__iabuz is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            otup__iabuz)
                    else:
                        msg = 'No match.'
                    uurki__xonp.add_error(psyy__zbl, True, msg, uerg__jsb)
    uurki__xonp.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    bem__zhj = self.template(context)
    nrcd__xmfr = None
    ewfd__rif = None
    bdf__joox = None
    tucj__vze = [True, False] if bem__zhj.prefer_literal else [False, True]
    tucj__vze = [True] if getattr(bem__zhj, '_no_unliteral', False
        ) else tucj__vze
    for uerg__jsb in tucj__vze:
        if uerg__jsb:
            try:
                bdf__joox = bem__zhj.apply(args, kws)
            except Exception as itgea__sltg:
                if isinstance(itgea__sltg, errors.ForceLiteralArg):
                    raise itgea__sltg
                nrcd__xmfr = itgea__sltg
                bdf__joox = None
            else:
                break
        else:
            exp__wbwi = tuple([_unlit_non_poison(a) for a in args])
            yzql__osb = {bykga__pfe: _unlit_non_poison(yjq__ijhy) for 
                bykga__pfe, yjq__ijhy in kws.items()}
            kfav__cdoq = exp__wbwi == args and kws == yzql__osb
            if not kfav__cdoq and bdf__joox is None:
                try:
                    bdf__joox = bem__zhj.apply(exp__wbwi, yzql__osb)
                except Exception as itgea__sltg:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        itgea__sltg, errors.NumbaError):
                        raise itgea__sltg
                    if isinstance(itgea__sltg, errors.ForceLiteralArg):
                        if bem__zhj.prefer_literal:
                            raise itgea__sltg
                    ewfd__rif = itgea__sltg
                else:
                    break
    if bdf__joox is None and (ewfd__rif is not None or nrcd__xmfr is not None):
        fme__xfwa = '- Resolution failure for {} arguments:\n{}\n'
        hukir__opm = _termcolor.highlight(fme__xfwa)
        if numba.core.config.DEVELOPER_MODE:
            wzg__dpy = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    txl__fwia = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    txl__fwia = ['']
                xbq__twmz = '\n{}'.format(2 * wzg__dpy)
                dmus__bmc = _termcolor.reset(xbq__twmz + xbq__twmz.join(
                    _bt_as_lines(txl__fwia)))
                return _termcolor.reset(dmus__bmc)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            hrqfz__sxf = str(e)
            hrqfz__sxf = hrqfz__sxf if hrqfz__sxf else str(repr(e)) + add_bt(e)
            vlpl__fsgl = errors.TypingError(textwrap.dedent(hrqfz__sxf))
            return hukir__opm.format(literalness, str(vlpl__fsgl))
        import bodo
        if isinstance(nrcd__xmfr, bodo.utils.typing.BodoError):
            raise nrcd__xmfr
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', nrcd__xmfr) +
                nested_msg('non-literal', ewfd__rif))
        else:
            if 'missing a required argument' in nrcd__xmfr.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=nrcd__xmfr.loc)
    return bdf__joox


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    svjxc__wwmsi = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=svjxc__wwmsi)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            dbp__edfxq = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), dbp__edfxq)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    ipqb__ujihf = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            ipqb__ujihf.append(types.Omitted(a.value))
        else:
            ipqb__ujihf.append(self.typeof_pyval(a))
    zqkir__yuop = None
    try:
        error = None
        zqkir__yuop = self.compile(tuple(ipqb__ujihf))
    except errors.ForceLiteralArg as e:
        heq__givr = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if heq__givr:
            dkf__edfx = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            nmptw__pmm = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(heq__givr))
            raise errors.CompilerError(dkf__edfx.format(nmptw__pmm))
        opfio__yki = []
        try:
            for i, yjq__ijhy in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        opfio__yki.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        opfio__yki.append(types.literal(args[i]))
                else:
                    opfio__yki.append(args[i])
            args = opfio__yki
        except (OSError, FileNotFoundError) as jzp__dlva:
            error = FileNotFoundError(str(jzp__dlva) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                zqkir__yuop = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        jtih__dzeyn = []
        for i, dlvxd__fgyh in enumerate(args):
            val = dlvxd__fgyh.value if isinstance(dlvxd__fgyh, numba.core.
                dispatcher.OmittedArg) else dlvxd__fgyh
            try:
                evwu__ykj = typeof(val, Purpose.argument)
            except ValueError as prm__kmsa:
                jtih__dzeyn.append((i, str(prm__kmsa)))
            else:
                if evwu__ykj is None:
                    jtih__dzeyn.append((i,
                        f'cannot determine Numba type of value {val}'))
        if jtih__dzeyn:
            cfrao__wgy = '\n'.join(f'- argument {i}: {crupq__isa}' for i,
                crupq__isa in jtih__dzeyn)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{cfrao__wgy}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                vidts__xwaw = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                ejr__mkcbn = False
                for ong__nafao in vidts__xwaw:
                    if ong__nafao in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        ejr__mkcbn = True
                        break
                if not ejr__mkcbn:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                dbp__edfxq = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), dbp__edfxq)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return zqkir__yuop


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for hub__bvo in cres.library._codegen._engine._defined_symbols:
        if hub__bvo.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in hub__bvo and (
            'bodo_gb_udf_update_local' in hub__bvo or 'bodo_gb_udf_combine' in
            hub__bvo or 'bodo_gb_udf_eval' in hub__bvo or 
            'bodo_gb_apply_general_udfs' in hub__bvo):
            gb_agg_cfunc_addr[hub__bvo] = cres.library.get_pointer_to_function(
                hub__bvo)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for hub__bvo in cres.library._codegen._engine._defined_symbols:
        if hub__bvo.startswith('cfunc') and ('get_join_cond_addr' not in
            hub__bvo or 'bodo_join_gen_cond' in hub__bvo):
            join_gen_cond_cfunc_addr[hub__bvo
                ] = cres.library.get_pointer_to_function(hub__bvo)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    oukq__axflo = self._get_dispatcher_for_current_target()
    if oukq__axflo is not self:
        return oukq__axflo.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            ewngm__aubvj = self.overloads.get(tuple(args))
            if ewngm__aubvj is not None:
                return ewngm__aubvj.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            riup__lio = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=riup__lio):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
                if bodo.get_rank() == 0:
                    self._cache.save_overload(sig, cres)
            else:
                nomf__wjd = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in nomf__wjd:
                    self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    itwdf__hobcz = self._final_module
    tgkrg__srj = []
    zgad__xbpy = 0
    for fn in itwdf__hobcz.functions:
        zgad__xbpy += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            tgkrg__srj.append(fn.name)
    if zgad__xbpy == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if tgkrg__srj:
        itwdf__hobcz = itwdf__hobcz.clone()
        for name in tgkrg__srj:
            itwdf__hobcz.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = itwdf__hobcz
    return itwdf__hobcz


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for owc__rnbog in self.constraints:
        loc = owc__rnbog.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                owc__rnbog(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                hru__ewg = numba.core.errors.TypingError(str(e), loc=
                    owc__rnbog.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(hru__ewg, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    hru__ewg = numba.core.errors.TypingError(msg.format(con
                        =owc__rnbog, err=str(e)), loc=owc__rnbog.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(hru__ewg, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for jxrs__sehni in self._failures.values():
        for srans__nlrru in jxrs__sehni:
            if isinstance(srans__nlrru.error, ForceLiteralArg):
                raise srans__nlrru.error
            if isinstance(srans__nlrru.error, bodo.utils.typing.BodoError):
                raise srans__nlrru.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    inv__mad = False
    riaiu__kur = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        upvra__jlx = set()
        griib__cbcqe = lives & alias_set
        for yjq__ijhy in griib__cbcqe:
            upvra__jlx |= alias_map[yjq__ijhy]
        lives_n_aliases = lives | upvra__jlx | arg_aliases
        if type(stmt) in remove_dead_extensions:
            irk__kiq = remove_dead_extensions[type(stmt)]
            stmt = irk__kiq(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                inv__mad = True
                continue
        if isinstance(stmt, ir.Assign):
            wte__fqbz = stmt.target
            gop__pgu = stmt.value
            if wte__fqbz.name not in lives:
                if has_no_side_effect(gop__pgu, lives_n_aliases, call_table):
                    inv__mad = True
                    continue
                if isinstance(gop__pgu, ir.Expr
                    ) and gop__pgu.op == 'call' and call_table[gop__pgu.
                    func.name] == ['astype']:
                    vqulq__tpqjc = guard(get_definition, func_ir, gop__pgu.func
                        )
                    if (vqulq__tpqjc is not None and vqulq__tpqjc.op ==
                        'getattr' and isinstance(typemap[vqulq__tpqjc.value
                        .name], types.Array) and vqulq__tpqjc.attr == 'astype'
                        ):
                        inv__mad = True
                        continue
            if saved_array_analysis and wte__fqbz.name in lives and is_expr(
                gop__pgu, 'getattr'
                ) and gop__pgu.attr == 'shape' and is_array_typ(typemap[
                gop__pgu.value.name]) and gop__pgu.value.name not in lives:
                pqzqp__dpq = {yjq__ijhy: bykga__pfe for bykga__pfe,
                    yjq__ijhy in func_ir.blocks.items()}
                if block in pqzqp__dpq:
                    label = pqzqp__dpq[block]
                    sebj__kchz = saved_array_analysis.get_equiv_set(label)
                    ensk__taqut = sebj__kchz.get_equiv_set(gop__pgu.value)
                    if ensk__taqut is not None:
                        for yjq__ijhy in ensk__taqut:
                            if yjq__ijhy.endswith('#0'):
                                yjq__ijhy = yjq__ijhy[:-2]
                            if yjq__ijhy in typemap and is_array_typ(typemap
                                [yjq__ijhy]) and yjq__ijhy in lives:
                                gop__pgu.value = ir.Var(gop__pgu.value.
                                    scope, yjq__ijhy, gop__pgu.value.loc)
                                inv__mad = True
                                break
            if isinstance(gop__pgu, ir.Var
                ) and wte__fqbz.name == gop__pgu.name:
                inv__mad = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                inv__mad = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            ydxk__hmll = analysis.ir_extension_usedefs[type(stmt)]
            laxg__rwfvt, zbxve__cxt = ydxk__hmll(stmt)
            lives -= zbxve__cxt
            lives |= laxg__rwfvt
        else:
            lives |= {yjq__ijhy.name for yjq__ijhy in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                auq__huxhg = set()
                if isinstance(gop__pgu, ir.Expr):
                    auq__huxhg = {yjq__ijhy.name for yjq__ijhy in gop__pgu.
                        list_vars()}
                if wte__fqbz.name not in auq__huxhg:
                    lives.remove(wte__fqbz.name)
        riaiu__kur.append(stmt)
    riaiu__kur.reverse()
    block.body = riaiu__kur
    return inv__mad


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            lbhc__gktbg, = args
            if isinstance(lbhc__gktbg, types.IterableType):
                dtype = lbhc__gktbg.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), lbhc__gktbg)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    qsi__dav = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (qsi__dav, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as ddce__kgv:
            return
    try:
        return literal(value)
    except LiteralTypingError as ddce__kgv:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        ysbcy__qkj = py_func.__qualname__
    except AttributeError as ddce__kgv:
        ysbcy__qkj = py_func.__name__
    hnrz__gitwz = inspect.getfile(py_func)
    for cls in self._locator_classes:
        jqwx__ccy = cls.from_function(py_func, hnrz__gitwz)
        if jqwx__ccy is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (ysbcy__qkj, hnrz__gitwz))
    self._locator = jqwx__ccy
    jxdcu__cnak = inspect.getfile(py_func)
    zjznf__oknsd = os.path.splitext(os.path.basename(jxdcu__cnak))[0]
    if hnrz__gitwz.startswith('<ipython-'):
        uwbwh__kbih = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', zjznf__oknsd, count=1)
        if uwbwh__kbih == zjznf__oknsd:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        zjznf__oknsd = uwbwh__kbih
    kxun__baw = '%s.%s' % (zjznf__oknsd, ysbcy__qkj)
    xvekn__wfzkg = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(kxun__baw, xvekn__wfzkg
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    kmd__moor = list(filter(lambda a: self._istuple(a.name), args))
    if len(kmd__moor) == 2 and fn.__name__ == 'add':
        xmzos__jmmlu = self.typemap[kmd__moor[0].name]
        kezst__yfz = self.typemap[kmd__moor[1].name]
        if xmzos__jmmlu.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                kmd__moor[1]))
        if kezst__yfz.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                kmd__moor[0]))
        try:
            vrp__qmvbu = [equiv_set.get_shape(x) for x in kmd__moor]
            if None in vrp__qmvbu:
                return None
            agel__uefy = sum(vrp__qmvbu, ())
            return ArrayAnalysis.AnalyzeResult(shape=agel__uefy)
        except GuardException as ddce__kgv:
            return None
    cgndc__kinnw = list(filter(lambda a: self._isarray(a.name), args))
    require(len(cgndc__kinnw) > 0)
    zpf__rrj = [x.name for x in cgndc__kinnw]
    lfr__nacfy = [self.typemap[x.name].ndim for x in cgndc__kinnw]
    myphx__oqi = max(lfr__nacfy)
    require(myphx__oqi > 0)
    vrp__qmvbu = [equiv_set.get_shape(x) for x in cgndc__kinnw]
    if any(a is None for a in vrp__qmvbu):
        return ArrayAnalysis.AnalyzeResult(shape=cgndc__kinnw[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, cgndc__kinnw))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, vrp__qmvbu,
        zpf__rrj)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    csa__hrkm = code_obj.code
    zlk__daill = len(csa__hrkm.co_freevars)
    wdhsg__llsy = csa__hrkm.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        brfe__hrme, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        wdhsg__llsy = [yjq__ijhy.name for yjq__ijhy in brfe__hrme]
    guh__ibgog = caller_ir.func_id.func.__globals__
    try:
        guh__ibgog = getattr(code_obj, 'globals', guh__ibgog)
    except KeyError as ddce__kgv:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    pono__ttznq = []
    for x in wdhsg__llsy:
        try:
            mrb__wwsk = caller_ir.get_definition(x)
        except KeyError as ddce__kgv:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(mrb__wwsk, (ir.Const, ir.Global, ir.FreeVar)):
            val = mrb__wwsk.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                mweoq__dyn = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                guh__ibgog[mweoq__dyn] = bodo.jit(distributed=False)(val)
                guh__ibgog[mweoq__dyn].is_nested_func = True
                val = mweoq__dyn
            if isinstance(val, CPUDispatcher):
                mweoq__dyn = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                guh__ibgog[mweoq__dyn] = val
                val = mweoq__dyn
            pono__ttznq.append(val)
        elif isinstance(mrb__wwsk, ir.Expr
            ) and mrb__wwsk.op == 'make_function':
            qqugh__strtj = convert_code_obj_to_function(mrb__wwsk, caller_ir)
            mweoq__dyn = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            guh__ibgog[mweoq__dyn] = bodo.jit(distributed=False)(qqugh__strtj)
            guh__ibgog[mweoq__dyn].is_nested_func = True
            pono__ttznq.append(mweoq__dyn)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    ndywg__vgvrx = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in
        enumerate(pono__ttznq)])
    vnzz__hcltm = ','.join([('c_%d' % i) for i in range(zlk__daill)])
    gbyo__hqji = list(csa__hrkm.co_varnames)
    kti__ypvnt = 0
    xga__aet = csa__hrkm.co_argcount
    dwki__mogx = caller_ir.get_definition(code_obj.defaults)
    if dwki__mogx is not None:
        if isinstance(dwki__mogx, tuple):
            d = [caller_ir.get_definition(x).value for x in dwki__mogx]
            rxtl__yjbdk = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in dwki__mogx.items]
            rxtl__yjbdk = tuple(d)
        kti__ypvnt = len(rxtl__yjbdk)
    qnwu__hyyd = xga__aet - kti__ypvnt
    rcjgx__ethxg = ','.join([('%s' % gbyo__hqji[i]) for i in range(qnwu__hyyd)]
        )
    if kti__ypvnt:
        vxao__kez = [('%s = %s' % (gbyo__hqji[i + qnwu__hyyd], rxtl__yjbdk[
            i])) for i in range(kti__ypvnt)]
        rcjgx__ethxg += ', '
        rcjgx__ethxg += ', '.join(vxao__kez)
    return _create_function_from_code_obj(csa__hrkm, ndywg__vgvrx,
        rcjgx__ethxg, vnzz__hcltm, guh__ibgog)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for xtsp__gsho, (gufgx__ohve, icbwi__qvoe) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % icbwi__qvoe)
            ozfgw__ivlro = _pass_registry.get(gufgx__ohve).pass_inst
            if isinstance(ozfgw__ivlro, CompilerPass):
                self._runPass(xtsp__gsho, ozfgw__ivlro, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, icbwi__qvoe)
                dxke__ofmha = self._patch_error(msg, e)
                raise dxke__ofmha
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    btha__zqg = None
    zbxve__cxt = {}

    def lookup(var, already_seen, varonly=True):
        val = zbxve__cxt.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    dug__cdi = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        wte__fqbz = stmt.target
        gop__pgu = stmt.value
        zbxve__cxt[wte__fqbz.name] = gop__pgu
        if isinstance(gop__pgu, ir.Var) and gop__pgu.name in zbxve__cxt:
            gop__pgu = lookup(gop__pgu, set())
        if isinstance(gop__pgu, ir.Expr):
            pvlhv__tyife = set(lookup(yjq__ijhy, set(), True).name for
                yjq__ijhy in gop__pgu.list_vars())
            if name in pvlhv__tyife:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(gop__pgu)]
                ismzq__sovnh = [x for x, psdv__ocx in args if psdv__ocx.
                    name != name]
                args = [(x, psdv__ocx) for x, psdv__ocx in args if x !=
                    psdv__ocx.name]
                auq__wqp = dict(args)
                if len(ismzq__sovnh) == 1:
                    auq__wqp[ismzq__sovnh[0]] = ir.Var(wte__fqbz.scope, 
                        name + '#init', wte__fqbz.loc)
                replace_vars_inner(gop__pgu, auq__wqp)
                btha__zqg = nodes[i:]
                break
    return btha__zqg


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        mkxfx__cloo = expand_aliases({yjq__ijhy.name for yjq__ijhy in stmt.
            list_vars()}, alias_map, arg_aliases)
        olra__uzvbz = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        bert__gck = expand_aliases({yjq__ijhy.name for yjq__ijhy in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        ynwlu__ldc = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(olra__uzvbz & bert__gck | ynwlu__ldc & mkxfx__cloo) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    elbnw__hjtx = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            elbnw__hjtx.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                elbnw__hjtx.update(get_parfor_writes(stmt, func_ir))
    return elbnw__hjtx


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    elbnw__hjtx = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        elbnw__hjtx.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        elbnw__hjtx = {yjq__ijhy.name for yjq__ijhy in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        elbnw__hjtx = {yjq__ijhy.name for yjq__ijhy in stmt.get_live_out_vars()
            }
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            elbnw__hjtx.update({yjq__ijhy.name for yjq__ijhy in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        ymyek__pmy = guard(find_callname, func_ir, stmt.value)
        if ymyek__pmy in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            elbnw__hjtx.add(stmt.value.args[0].name)
        if ymyek__pmy == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            elbnw__hjtx.add(stmt.value.args[1].name)
    return elbnw__hjtx


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        irk__kiq = _termcolor.errmsg('{0}') + _termcolor.filename('During: {1}'
            )
        jyj__uqal = irk__kiq.format(self, msg)
        self.args = jyj__uqal,
    else:
        irk__kiq = _termcolor.errmsg('{0}')
        jyj__uqal = irk__kiq.format(self)
        self.args = jyj__uqal,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for eiqez__byjft in options['distributed']:
            dist_spec[eiqez__byjft] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for eiqez__byjft in options['distributed_block']:
            dist_spec[eiqez__byjft] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    lko__ffk = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, qedk__ugyuu in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(qedk__ugyuu)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    oguge__gus = {}
    for hxu__nqsbv in reversed(inspect.getmro(cls)):
        oguge__gus.update(hxu__nqsbv.__dict__)
    xvr__let, dddib__vxvbj, kppma__qvar, nldou__zazx = {}, {}, {}, {}
    for bykga__pfe, yjq__ijhy in oguge__gus.items():
        if isinstance(yjq__ijhy, pytypes.FunctionType):
            xvr__let[bykga__pfe] = yjq__ijhy
        elif isinstance(yjq__ijhy, property):
            dddib__vxvbj[bykga__pfe] = yjq__ijhy
        elif isinstance(yjq__ijhy, staticmethod):
            kppma__qvar[bykga__pfe] = yjq__ijhy
        else:
            nldou__zazx[bykga__pfe] = yjq__ijhy
    yvpdj__xjuq = (set(xvr__let) | set(dddib__vxvbj) | set(kppma__qvar)) & set(
        spec)
    if yvpdj__xjuq:
        raise NameError('name shadowing: {0}'.format(', '.join(yvpdj__xjuq)))
    yqpi__skb = nldou__zazx.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(nldou__zazx)
    if nldou__zazx:
        msg = 'class members are not yet supported: {0}'
        pxr__aob = ', '.join(nldou__zazx.keys())
        raise TypeError(msg.format(pxr__aob))
    for bykga__pfe, yjq__ijhy in dddib__vxvbj.items():
        if yjq__ijhy.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(bykga__pfe))
    jit_methods = {bykga__pfe: bodo.jit(returns_maybe_distributed=lko__ffk)
        (yjq__ijhy) for bykga__pfe, yjq__ijhy in xvr__let.items()}
    jit_props = {}
    for bykga__pfe, yjq__ijhy in dddib__vxvbj.items():
        jozv__yhht = {}
        if yjq__ijhy.fget:
            jozv__yhht['get'] = bodo.jit(yjq__ijhy.fget)
        if yjq__ijhy.fset:
            jozv__yhht['set'] = bodo.jit(yjq__ijhy.fset)
        jit_props[bykga__pfe] = jozv__yhht
    jit_static_methods = {bykga__pfe: bodo.jit(yjq__ijhy.__func__) for 
        bykga__pfe, yjq__ijhy in kppma__qvar.items()}
    ulzlq__ryjm = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    fgkv__xqu = dict(class_type=ulzlq__ryjm, __doc__=yqpi__skb)
    fgkv__xqu.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), fgkv__xqu)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, ulzlq__ryjm)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(ulzlq__ryjm, typingctx, targetctx).register()
    as_numba_type.register(cls, ulzlq__ryjm.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    pwz__nekxr = ','.join('{0}:{1}'.format(bykga__pfe, yjq__ijhy) for 
        bykga__pfe, yjq__ijhy in struct.items())
    yhvei__fansk = ','.join('{0}:{1}'.format(bykga__pfe, yjq__ijhy) for 
        bykga__pfe, yjq__ijhy in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), pwz__nekxr, yhvei__fansk)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    pzna__fxh = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if pzna__fxh is None:
        return
    kcza__pvi, vqs__bcuu = pzna__fxh
    for a in itertools.chain(kcza__pvi, vqs__bcuu.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, kcza__pvi, vqs__bcuu)
    except ForceLiteralArg as e:
        pnj__vfh = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(pnj__vfh, self.kws)
        pik__szg = set()
        mmuvi__nwjqm = set()
        zdb__wdfqe = {}
        for xtsp__gsho in e.requested_args:
            mbpts__xjbp = typeinfer.func_ir.get_definition(folded[xtsp__gsho])
            if isinstance(mbpts__xjbp, ir.Arg):
                pik__szg.add(mbpts__xjbp.index)
                if mbpts__xjbp.index in e.file_infos:
                    zdb__wdfqe[mbpts__xjbp.index] = e.file_infos[mbpts__xjbp
                        .index]
            else:
                mmuvi__nwjqm.add(xtsp__gsho)
        if mmuvi__nwjqm:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif pik__szg:
            raise ForceLiteralArg(pik__szg, loc=self.loc, file_infos=zdb__wdfqe
                )
    if sig is None:
        ilk__ilzv = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in kcza__pvi]
        args += [('%s=%s' % (bykga__pfe, yjq__ijhy)) for bykga__pfe,
            yjq__ijhy in sorted(vqs__bcuu.items())]
        giw__puqw = ilk__ilzv.format(fnty, ', '.join(map(str, args)))
        unfzj__unjog = context.explain_function_type(fnty)
        msg = '\n'.join([giw__puqw, unfzj__unjog])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        mboy__watzt = context.unify_pairs(sig.recvr, fnty.this)
        if mboy__watzt is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if mboy__watzt is not None and mboy__watzt.is_precise():
            yhwrc__rmj = fnty.copy(this=mboy__watzt)
            typeinfer.propagate_refined_type(self.func, yhwrc__rmj)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            aaxgn__whce = target.getone()
            if context.unify_pairs(aaxgn__whce, sig.return_type
                ) == aaxgn__whce:
                sig = sig.replace(return_type=aaxgn__whce)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        dkf__edfx = '*other* must be a {} but got a {} instead'
        raise TypeError(dkf__edfx.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    bnqvy__wfu = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for bykga__pfe, yjq__ijhy in kwargs.items():
        smn__hbgv = None
        try:
            tzlwp__wpzp = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[tzlwp__wpzp.name] = [yjq__ijhy]
            smn__hbgv = get_const_value_inner(func_ir, tzlwp__wpzp)
            func_ir._definitions.pop(tzlwp__wpzp.name)
            if isinstance(smn__hbgv, str):
                smn__hbgv = sigutils._parse_signature_string(smn__hbgv)
            if isinstance(smn__hbgv, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {bykga__pfe} is annotated as type class {smn__hbgv}."""
                    )
            assert isinstance(smn__hbgv, types.Type)
            if isinstance(smn__hbgv, (types.List, types.Set)):
                smn__hbgv = smn__hbgv.copy(reflected=False)
            bnqvy__wfu[bykga__pfe] = smn__hbgv
        except BodoError as ddce__kgv:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(smn__hbgv, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(yjq__ijhy, ir.Global):
                    msg = f'Global {yjq__ijhy.name!r} is not defined.'
                if isinstance(yjq__ijhy, ir.FreeVar):
                    msg = f'Freevar {yjq__ijhy.name!r} is not defined.'
            if isinstance(yjq__ijhy, ir.Expr) and yjq__ijhy.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=bykga__pfe, msg=msg, loc=loc)
    for name, typ in bnqvy__wfu.items():
        self._legalize_arg_type(name, typ, loc)
    return bnqvy__wfu


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    nnm__qrj = inst.arg
    assert nnm__qrj > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(nnm__qrj)]))
    tmps = [state.make_temp() for _ in range(nnm__qrj - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    ylfw__czz = ir.Global('format', format, loc=self.loc)
    self.store(value=ylfw__czz, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    glj__pcam = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=glj__pcam, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    nnm__qrj = inst.arg
    assert nnm__qrj > 0, 'invalid BUILD_STRING count'
    fgb__zbait = self.get(strings[0])
    for other, jkgcs__vnpwz in zip(strings[1:], tmps):
        other = self.get(other)
        wtws__kngz = ir.Expr.binop(operator.add, lhs=fgb__zbait, rhs=other,
            loc=self.loc)
        self.store(wtws__kngz, jkgcs__vnpwz)
        fgb__zbait = self.get(jkgcs__vnpwz)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    unen__zye = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, unen__zye])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    ipx__ucj = mk_unique_var(f'{var_name}')
    ipks__klud = ipx__ucj.replace('<', '_').replace('>', '_')
    ipks__klud = ipks__klud.replace('.', '_').replace('$', '_v')
    return ipks__klud


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if (val1 == bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type):
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                aziq__cwln = get_overload_const_str(val2)
                if aziq__cwln != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        ufwfv__pkg = states['defmap']
        if len(ufwfv__pkg) == 0:
            jtgif__zdos = assign.target
            numba.core.ssa._logger.debug('first assign: %s', jtgif__zdos)
            if jtgif__zdos.name not in scope.localvars:
                jtgif__zdos = scope.define(assign.target.name, loc=assign.loc)
        else:
            jtgif__zdos = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=jtgif__zdos, value=assign.value, loc=
            assign.loc)
        ufwfv__pkg[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    scmsg__uyw = []
    for bykga__pfe, yjq__ijhy in typing.npydecl.registry.globals:
        if bykga__pfe == func:
            scmsg__uyw.append(yjq__ijhy)
    for bykga__pfe, yjq__ijhy in typing.templates.builtin_registry.globals:
        if bykga__pfe == func:
            scmsg__uyw.append(yjq__ijhy)
    if len(scmsg__uyw) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return scmsg__uyw


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    vnkx__trq = {}
    nxik__fepd = find_topo_order(blocks)
    oiur__prx = {}
    for label in nxik__fepd:
        block = blocks[label]
        riaiu__kur = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                wte__fqbz = stmt.target.name
                gop__pgu = stmt.value
                if (gop__pgu.op == 'getattr' and gop__pgu.attr in arr_math and
                    isinstance(typemap[gop__pgu.value.name], types.npytypes
                    .Array)):
                    gop__pgu = stmt.value
                    ejcw__lqjw = gop__pgu.value
                    vnkx__trq[wte__fqbz] = ejcw__lqjw
                    scope = ejcw__lqjw.scope
                    loc = ejcw__lqjw.loc
                    djrfz__bgv = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[djrfz__bgv.name] = types.misc.Module(numpy)
                    yqrm__rar = ir.Global('np', numpy, loc)
                    riute__dxcap = ir.Assign(yqrm__rar, djrfz__bgv, loc)
                    gop__pgu.value = djrfz__bgv
                    riaiu__kur.append(riute__dxcap)
                    func_ir._definitions[djrfz__bgv.name] = [yqrm__rar]
                    func = getattr(numpy, gop__pgu.attr)
                    xgk__chrh = get_np_ufunc_typ_lst(func)
                    oiur__prx[wte__fqbz] = xgk__chrh
                if gop__pgu.op == 'call' and gop__pgu.func.name in vnkx__trq:
                    ejcw__lqjw = vnkx__trq[gop__pgu.func.name]
                    cjga__wnth = calltypes.pop(gop__pgu)
                    xbfd__xbgrq = cjga__wnth.args[:len(gop__pgu.args)]
                    xaj__yiv = {name: typemap[yjq__ijhy.name] for name,
                        yjq__ijhy in gop__pgu.kws}
                    uzlfl__pqhjo = oiur__prx[gop__pgu.func.name]
                    ovau__bjbf = None
                    for cehwe__bnper in uzlfl__pqhjo:
                        try:
                            ovau__bjbf = cehwe__bnper.get_call_type(typingctx,
                                [typemap[ejcw__lqjw.name]] + list(
                                xbfd__xbgrq), xaj__yiv)
                            typemap.pop(gop__pgu.func.name)
                            typemap[gop__pgu.func.name] = cehwe__bnper
                            calltypes[gop__pgu] = ovau__bjbf
                            break
                        except Exception as ddce__kgv:
                            pass
                    if ovau__bjbf is None:
                        raise TypeError(
                            f'No valid template found for {gop__pgu.func.name}'
                            )
                    gop__pgu.args = [ejcw__lqjw] + gop__pgu.args
            riaiu__kur.append(stmt)
        block.body = riaiu__kur


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    irtpu__qpl = ufunc.nin
    ekjl__tuys = ufunc.nout
    qnwu__hyyd = ufunc.nargs
    assert qnwu__hyyd == irtpu__qpl + ekjl__tuys
    if len(args) < irtpu__qpl:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), irtpu__qpl)
            )
    if len(args) > qnwu__hyyd:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), qnwu__hyyd)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    qeh__mynbp = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    vui__bexd = max(qeh__mynbp)
    grknb__wvijl = args[irtpu__qpl:]
    if not all(d == vui__bexd for d in qeh__mynbp[irtpu__qpl:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(vfx__ioeox, types.ArrayCompatible) and not
        isinstance(vfx__ioeox, types.Bytes) for vfx__ioeox in grknb__wvijl):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(vfx__ioeox.mutable for vfx__ioeox in grknb__wvijl):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ndcta__scob = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    uun__ahg = None
    if vui__bexd > 0 and len(grknb__wvijl) < ufunc.nout:
        uun__ahg = 'C'
        wpn__lhqzp = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in wpn__lhqzp and 'F' in wpn__lhqzp:
            uun__ahg = 'F'
    return ndcta__scob, grknb__wvijl, vui__bexd, uun__ahg


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        bbl__mjgh = 'Dict.key_type cannot be of type {}'
        raise TypingError(bbl__mjgh.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        bbl__mjgh = 'Dict.value_type cannot be of type {}'
        raise TypingError(bbl__mjgh.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    vtx__tbkav = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[vtx__tbkav]
        return impl, args
    except KeyError as ddce__kgv:
        pass
    impl, args = self._build_impl(vtx__tbkav, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def trim_empty_parfor_branches(parfor):
    ezvns__ddnvi = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            xos__wsdut = block.body[-1]
            if isinstance(xos__wsdut, ir.Branch):
                if len(blocks[xos__wsdut.truebr].body) == 1 and len(blocks[
                    xos__wsdut.falsebr].body) == 1:
                    ncu__dua = blocks[xos__wsdut.truebr].body[0]
                    kqm__yyfg = blocks[xos__wsdut.falsebr].body[0]
                    if isinstance(ncu__dua, ir.Jump) and isinstance(kqm__yyfg,
                        ir.Jump) and ncu__dua.target == kqm__yyfg.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(ncu__dua
                            .target, xos__wsdut.loc)
                        ezvns__ddnvi = True
                elif len(blocks[xos__wsdut.truebr].body) == 1:
                    ncu__dua = blocks[xos__wsdut.truebr].body[0]
                    if isinstance(ncu__dua, ir.Jump
                        ) and ncu__dua.target == xos__wsdut.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(ncu__dua
                            .target, xos__wsdut.loc)
                        ezvns__ddnvi = True
                elif len(blocks[xos__wsdut.falsebr].body) == 1:
                    kqm__yyfg = blocks[xos__wsdut.falsebr].body[0]
                    if isinstance(kqm__yyfg, ir.Jump
                        ) and kqm__yyfg.target == xos__wsdut.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(kqm__yyfg
                            .target, xos__wsdut.loc)
                        ezvns__ddnvi = True
    return ezvns__ddnvi


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        myn__uqsp = find_topo_order(parfor.loop_body)
    zqg__wdnv = myn__uqsp[0]
    midrx__rlds = {}
    _update_parfor_get_setitems(parfor.loop_body[zqg__wdnv].body, parfor.
        index_var, alias_map, midrx__rlds, lives_n_aliases)
    zix__susi = set(midrx__rlds.keys())
    for vzrue__rqal in myn__uqsp:
        if vzrue__rqal == zqg__wdnv:
            continue
        for stmt in parfor.loop_body[vzrue__rqal].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            koyxf__pyby = set(yjq__ijhy.name for yjq__ijhy in stmt.list_vars())
            nxa__esjzl = koyxf__pyby & zix__susi
            for a in nxa__esjzl:
                midrx__rlds.pop(a, None)
    for vzrue__rqal in myn__uqsp:
        if vzrue__rqal == zqg__wdnv:
            continue
        block = parfor.loop_body[vzrue__rqal]
        bpre__hwrcm = midrx__rlds.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            bpre__hwrcm, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    nkodf__jvee = max(blocks.keys())
    abfiy__snxj, vpwme__crw = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    zxkj__teup = ir.Jump(abfiy__snxj, ir.Loc('parfors_dummy', -1))
    blocks[nkodf__jvee].body.append(zxkj__teup)
    jfi__tqnw = compute_cfg_from_blocks(blocks)
    ham__dnemk = compute_use_defs(blocks)
    jzy__eaqv = compute_live_map(jfi__tqnw, blocks, ham__dnemk.usemap,
        ham__dnemk.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        riaiu__kur = []
        kkk__qdvq = {yjq__ijhy.name for yjq__ijhy in block.terminator.
            list_vars()}
        for ntyzj__xsa, zjdo__cjltd in jfi__tqnw.successors(label):
            kkk__qdvq |= jzy__eaqv[ntyzj__xsa]
        for stmt in reversed(block.body):
            upvra__jlx = kkk__qdvq & alias_set
            for yjq__ijhy in upvra__jlx:
                kkk__qdvq |= alias_map[yjq__ijhy]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in kkk__qdvq and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                ymyek__pmy = guard(find_callname, func_ir, stmt.value)
                if ymyek__pmy == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in kkk__qdvq and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            kkk__qdvq |= {yjq__ijhy.name for yjq__ijhy in stmt.list_vars()}
            riaiu__kur.append(stmt)
        riaiu__kur.reverse()
        block.body = riaiu__kur
    typemap.pop(vpwme__crw.name)
    blocks[nkodf__jvee].body.pop()
    ezvns__ddnvi = True
    while ezvns__ddnvi:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        ezvns__ddnvi = trim_empty_parfor_branches(parfor)
    ktlsy__usah = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        ktlsy__usah &= len(block.body) == 0
    if ktlsy__usah:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.parfors.parfor import Parfor
    olhoq__elnr = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                olhoq__elnr += 1
                parfor = stmt
                yazx__fugs = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = yazx__fugs.scope
                loc = ir.Loc('parfors_dummy', -1)
                yrniy__pnk = ir.Var(scope, mk_unique_var('$const'), loc)
                yazx__fugs.body.append(ir.Assign(ir.Const(0, loc),
                    yrniy__pnk, loc))
                yazx__fugs.body.append(ir.Return(yrniy__pnk, loc))
                jfi__tqnw = compute_cfg_from_blocks(parfor.loop_body)
                for yxe__mlg in jfi__tqnw.dead_nodes():
                    del parfor.loop_body[yxe__mlg]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                yazx__fugs = parfor.loop_body[max(parfor.loop_body.keys())]
                yazx__fugs.body.pop()
                yazx__fugs.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return olhoq__elnr


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    jfi__tqnw = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != jfi__tqnw.entry_point()
    koja__chjb = list(filter(find_single_branch, blocks.keys()))
    sccaq__qkou = set()
    for label in koja__chjb:
        inst = blocks[label].body[0]
        nsp__tngr = jfi__tqnw.predecessors(label)
        txh__kdq = True
        for hekg__gva, hbmdc__xvny in nsp__tngr:
            block = blocks[hekg__gva]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                txh__kdq = False
        if txh__kdq:
            sccaq__qkou.add(label)
    for label in sccaq__qkou:
        del blocks[label]
    merge_adjacent_blocks(blocks)
    return rename_labels(blocks)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.simplify_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0b3f2add05e5691155f08fc5945956d5cca5e068247d52cff8efb161b76388b7':
        warnings.warn('numba.core.ir_utils.simplify_CFG has changed')
numba.core.ir_utils.simplify_CFG = simplify_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            ewngm__aubvj = self.overloads.get(tuple(args))
            if ewngm__aubvj is not None:
                return ewngm__aubvj.entry_point
            self._pre_compile(args, return_type, flags)
            fvra__nwuhe = self.func_ir
            riup__lio = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=riup__lio):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=fvra__nwuhe, args=
                    args, return_type=return_type, flags=flags, locals=self
                    .locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        ienoe__dlv = copy.deepcopy(flags)
        ienoe__dlv.no_rewrites = True

        def compile_local(the_ir, the_flags):
            jpmss__vdzx = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return jpmss__vdzx.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        ohmx__bpid = compile_local(func_ir, ienoe__dlv)
        tfa__uqlz = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    tfa__uqlz = compile_local(func_ir, flags)
                except Exception as ddce__kgv:
                    pass
        if tfa__uqlz is not None:
            cres = tfa__uqlz
        else:
            cres = ohmx__bpid
        return cres
    else:
        jpmss__vdzx = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return jpmss__vdzx.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    nbvlu__qsbpw = self.get_data_type(typ.dtype)
    tao__batfn = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        tao__batfn):
        uqx__wbcmi = ary.ctypes.data
        trge__jet = self.add_dynamic_addr(builder, uqx__wbcmi, info=str(
            type(uqx__wbcmi)))
        uvck__lszt = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        lczt__vqy = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            lczt__vqy = lczt__vqy.view('int64')
        val = bytearray(lczt__vqy.data)
        ojg__lcfd = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        trge__jet = cgutils.global_constant(builder, '.const.array.data',
            ojg__lcfd)
        trge__jet.align = self.get_abi_alignment(nbvlu__qsbpw)
        uvck__lszt = None
    hrsp__godpo = self.get_value_type(types.intp)
    uks__cigti = [self.get_constant(types.intp, eadrp__bqug) for
        eadrp__bqug in ary.shape]
    wdoo__xeoop = lir.Constant(lir.ArrayType(hrsp__godpo, len(uks__cigti)),
        uks__cigti)
    dor__nhqn = [self.get_constant(types.intp, eadrp__bqug) for eadrp__bqug in
        ary.strides]
    tgeiy__ldokv = lir.Constant(lir.ArrayType(hrsp__godpo, len(dor__nhqn)),
        dor__nhqn)
    wjpx__fzeww = self.get_constant(types.intp, ary.dtype.itemsize)
    dfpr__xxo = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        dfpr__xxo, wjpx__fzeww, trge__jet.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), wdoo__xeoop, tgeiy__ldokv])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    wbjj__mjoh = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    sbeq__vhxjm = lir.Function(module, wbjj__mjoh, name='nrt_atomic_{0}'.
        format(op))
    [zxasl__exa] = sbeq__vhxjm.args
    rvsh__jly = sbeq__vhxjm.append_basic_block()
    builder = lir.IRBuilder(rvsh__jly)
    lrswm__omp = lir.Constant(_word_type, 1)
    if False:
        tgbq__cojk = builder.atomic_rmw(op, zxasl__exa, lrswm__omp,
            ordering=ordering)
        res = getattr(builder, op)(tgbq__cojk, lrswm__omp)
        builder.ret(res)
    else:
        tgbq__cojk = builder.load(zxasl__exa)
        jxsh__xsm = getattr(builder, op)(tgbq__cojk, lrswm__omp)
        pkma__ygro = builder.icmp_signed('!=', tgbq__cojk, lir.Constant(
            tgbq__cojk.type, -1))
        with cgutils.if_likely(builder, pkma__ygro):
            builder.store(jxsh__xsm, zxasl__exa)
        builder.ret(jxsh__xsm)
    return sbeq__vhxjm


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        ajkri__ewb = state.targetctx.codegen()
        state.library = ajkri__ewb.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    hrdzc__nurjr = state.func_ir
    typemap = state.typemap
    soqb__fhq = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    hbzb__vgpx = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            hrdzc__nurjr, typemap, soqb__fhq, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            lzs__bgfo = lowering.Lower(targetctx, library, fndesc,
                hrdzc__nurjr, metadata=metadata)
            lzs__bgfo.lower()
            if not flags.no_cpython_wrapper:
                lzs__bgfo.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(soqb__fhq, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        lzs__bgfo.create_cfunc_wrapper()
            env = lzs__bgfo.env
            sqxo__xutrw = lzs__bgfo.call_helper
            del lzs__bgfo
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, sqxo__xutrw, cfunc=None, env=env
                )
        else:
            sjhk__xsgd = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(sjhk__xsgd, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, sqxo__xutrw, cfunc=
                sjhk__xsgd, env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        dmw__sldm = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = dmw__sldm - hbzb__vgpx
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        lwvmj__mprap = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, lwvmj__mprap),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            qmipb__oyd.do_break()
        sshn__lxais = c.builder.icmp_signed('!=', lwvmj__mprap, expected_typobj
            )
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(sshn__lxais, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, lwvmj__mprap)
                c.pyapi.decref(lwvmj__mprap)
                qmipb__oyd.do_break()
        c.pyapi.decref(lwvmj__mprap)
    xakdh__cpns, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(xakdh__cpns, likely=True) as (nvn__ikf, iio__xmn):
        with nvn__ikf:
            list.size = size
            firda__bssb = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                firda__bssb), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        firda__bssb))
                    with cgutils.for_range(c.builder, size) as qmipb__oyd:
                        itemobj = c.pyapi.list_getitem(obj, qmipb__oyd.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        gyi__uped = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(gyi__uped.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            qmipb__oyd.do_break()
                        list.setitem(qmipb__oyd.index, gyi__uped.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with iio__xmn:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    vixnm__mvvgu, nleo__iqu, zyoo__imbts, bbs__oqtn, qpwlv__owq = (
        compile_time_get_string_data(literal_string))
    itwdf__hobcz = builder.module
    gv = context.insert_const_bytes(itwdf__hobcz, vixnm__mvvgu)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        nleo__iqu), context.get_constant(types.int32, zyoo__imbts), context
        .get_constant(types.uint32, bbs__oqtn), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    wmlg__ixafy = None
    if isinstance(shape, types.Integer):
        wmlg__ixafy = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(eadrp__bqug, (types.Integer, types.IntEnumMember)
            ) for eadrp__bqug in shape):
            wmlg__ixafy = len(shape)
    return wmlg__ixafy


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            wmlg__ixafy = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if wmlg__ixafy == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    wmlg__ixafy))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            zpf__rrj = self._get_names(x)
            if len(zpf__rrj) != 0:
                return zpf__rrj[0]
            return zpf__rrj
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    zpf__rrj = self._get_names(obj)
    if len(zpf__rrj) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(zpf__rrj[0])


def get_equiv_set(self, obj):
    zpf__rrj = self._get_names(obj)
    if len(zpf__rrj) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(zpf__rrj[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    nec__ygcyf = []
    for ccp__bhlat in func_ir.arg_names:
        if ccp__bhlat in typemap and isinstance(typemap[ccp__bhlat], types.
            containers.UniTuple) and typemap[ccp__bhlat].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(ccp__bhlat))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for jbsz__iww in func_ir.blocks.values():
        for stmt in jbsz__iww.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    aghm__pqoph = getattr(val, 'code', None)
                    if aghm__pqoph is not None:
                        if getattr(val, 'closure', None) is not None:
                            qkpz__gcyd = '<creating a function from a closure>'
                            wtws__kngz = ''
                        else:
                            qkpz__gcyd = aghm__pqoph.co_name
                            wtws__kngz = '(%s) ' % qkpz__gcyd
                    else:
                        qkpz__gcyd = '<could not ascertain use case>'
                        wtws__kngz = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (qkpz__gcyd, wtws__kngz))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                ecnd__iwv = False
                if isinstance(val, pytypes.FunctionType):
                    ecnd__iwv = val in {numba.gdb, numba.gdb_init}
                if not ecnd__iwv:
                    ecnd__iwv = getattr(val, '_name', '') == 'gdb_internal'
                if ecnd__iwv:
                    nec__ygcyf.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    xszcc__hjgs = func_ir.get_definition(var)
                    izop__slent = guard(find_callname, func_ir, xszcc__hjgs)
                    if izop__slent and izop__slent[1] == 'numpy':
                        ty = getattr(numpy, izop__slent[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    ptq__msf = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(ptq__msf), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(nec__ygcyf) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        zvu__kie = '\n'.join([x.strformat() for x in nec__ygcyf])
        raise errors.UnsupportedError(msg % zvu__kie)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    bykga__pfe, yjq__ijhy = next(iter(val.items()))
    olk__inefn = typeof_impl(bykga__pfe, c)
    mxpl__aap = typeof_impl(yjq__ijhy, c)
    if olk__inefn is None or mxpl__aap is None:
        raise ValueError(
            f'Cannot type dict element type {type(bykga__pfe)}, {type(yjq__ijhy)}'
            )
    return types.DictType(olk__inefn, mxpl__aap)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    yin__zmx = cgutils.alloca_once_value(c.builder, val)
    dcia__wos = c.pyapi.object_hasattr_string(val, '_opaque')
    vgn__kpnbq = c.builder.icmp_unsigned('==', dcia__wos, lir.Constant(
        dcia__wos.type, 0))
    koonx__qaig = typ.key_type
    mun__zks = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(koonx__qaig, mun__zks)

    def copy_dict(out_dict, in_dict):
        for bykga__pfe, yjq__ijhy in in_dict.items():
            out_dict[bykga__pfe] = yjq__ijhy
    with c.builder.if_then(vgn__kpnbq):
        aki__uskp = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        hih__reubw = c.pyapi.call_function_objargs(aki__uskp, [])
        gtx__kdqo = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(gtx__kdqo, [hih__reubw, val])
        c.builder.store(hih__reubw, yin__zmx)
    val = c.builder.load(yin__zmx)
    ejl__jhfi = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    tubj__wpzos = c.pyapi.object_type(val)
    mgoy__ybo = c.builder.icmp_unsigned('==', tubj__wpzos, ejl__jhfi)
    with c.builder.if_else(mgoy__ybo) as (ces__afgx, oap__osrpc):
        with ces__afgx:
            qqj__yasve = c.pyapi.object_getattr_string(val, '_opaque')
            ltcdn__jpf = types.MemInfoPointer(types.voidptr)
            gyi__uped = c.unbox(ltcdn__jpf, qqj__yasve)
            mi = gyi__uped.value
            ipqb__ujihf = ltcdn__jpf, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *ipqb__ujihf)
            fsdb__ear = context.get_constant_null(ipqb__ujihf[1])
            args = mi, fsdb__ear
            xhxy__wcwa, wyrhm__jokpo = c.pyapi.call_jit_code(convert, sig, args
                )
            c.context.nrt.decref(c.builder, typ, wyrhm__jokpo)
            c.pyapi.decref(qqj__yasve)
            gvkpm__dlrn = c.builder.basic_block
        with oap__osrpc:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", tubj__wpzos, ejl__jhfi)
            fkusu__ccpw = c.builder.basic_block
    mxbql__coj = c.builder.phi(wyrhm__jokpo.type)
    tqzz__lxyj = c.builder.phi(xhxy__wcwa.type)
    mxbql__coj.add_incoming(wyrhm__jokpo, gvkpm__dlrn)
    mxbql__coj.add_incoming(wyrhm__jokpo.type(None), fkusu__ccpw)
    tqzz__lxyj.add_incoming(xhxy__wcwa, gvkpm__dlrn)
    tqzz__lxyj.add_incoming(cgutils.true_bit, fkusu__ccpw)
    c.pyapi.decref(ejl__jhfi)
    c.pyapi.decref(tubj__wpzos)
    with c.builder.if_then(vgn__kpnbq):
        c.pyapi.decref(val)
    return NativeValue(mxbql__coj, is_error=tqzz__lxyj)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    zgtik__okx = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=zgtik__okx, name=updatevar)
    addt__exx = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=addt__exx, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for bykga__pfe, yjq__ijhy in other.items():
            d[bykga__pfe] = yjq__ijhy
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    wtws__kngz = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(wtws__kngz, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    aiod__ozcf = PassManager(name)
    if state.func_ir is None:
        aiod__ozcf.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            aiod__ozcf.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        aiod__ozcf.add_pass(FixupArgs, 'fix up args')
    aiod__ozcf.add_pass(IRProcessing, 'processing IR')
    aiod__ozcf.add_pass(WithLifting, 'Handle with contexts')
    aiod__ozcf.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        aiod__ozcf.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        aiod__ozcf.add_pass(DeadBranchPrune, 'dead branch pruning')
        aiod__ozcf.add_pass(GenericRewrites, 'nopython rewrites')
    aiod__ozcf.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    aiod__ozcf.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        aiod__ozcf.add_pass(DeadBranchPrune, 'dead branch pruning')
    aiod__ozcf.add_pass(FindLiterallyCalls, 'find literally calls')
    aiod__ozcf.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        aiod__ozcf.add_pass(ReconstructSSA, 'ssa')
    aiod__ozcf.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    aiod__ozcf.finalize()
    return aiod__ozcf


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, bnft__omcwe = args
    if isinstance(a, types.List) and isinstance(bnft__omcwe, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(bnft__omcwe, types.List):
        return signature(bnft__omcwe, types.intp, bnft__omcwe)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        qfvge__guln, hvsr__vzgk = 0, 1
    else:
        qfvge__guln, hvsr__vzgk = 1, 0
    fjum__gfjka = ListInstance(context, builder, sig.args[qfvge__guln],
        args[qfvge__guln])
    rpggk__hdx = fjum__gfjka.size
    sergq__cxm = args[hvsr__vzgk]
    firda__bssb = lir.Constant(sergq__cxm.type, 0)
    sergq__cxm = builder.select(cgutils.is_neg_int(builder, sergq__cxm),
        firda__bssb, sergq__cxm)
    dfpr__xxo = builder.mul(sergq__cxm, rpggk__hdx)
    sqvy__hzeu = ListInstance.allocate(context, builder, sig.return_type,
        dfpr__xxo)
    sqvy__hzeu.size = dfpr__xxo
    with cgutils.for_range_slice(builder, firda__bssb, dfpr__xxo,
        rpggk__hdx, inc=True) as (xbmp__cnllr, _):
        with cgutils.for_range(builder, rpggk__hdx) as qmipb__oyd:
            value = fjum__gfjka.getitem(qmipb__oyd.index)
            sqvy__hzeu.setitem(builder.add(qmipb__oyd.index, xbmp__cnllr),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, sqvy__hzeu.value
        )


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    pheyg__imh = first.unify(self, second)
    if pheyg__imh is not None:
        return pheyg__imh
    pheyg__imh = second.unify(self, first)
    if pheyg__imh is not None:
        return pheyg__imh
    chi__ymwjo = self.can_convert(fromty=first, toty=second)
    if chi__ymwjo is not None and chi__ymwjo <= Conversion.safe:
        return second
    chi__ymwjo = self.can_convert(fromty=second, toty=first)
    if chi__ymwjo is not None and chi__ymwjo <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    dfpr__xxo = payload.used
    listobj = c.pyapi.list_new(dfpr__xxo)
    xakdh__cpns = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(xakdh__cpns, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(dfpr__xxo.
            type, 0))
        with payload._iterate() as qmipb__oyd:
            i = c.builder.load(index)
            item = qmipb__oyd.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return xakdh__cpns, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    pebne__juepj = h.type
    ezt__dca = self.mask
    dtype = self._ty.dtype
    gau__zzvpc = context.typing_context
    fnty = gau__zzvpc.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(gau__zzvpc, (dtype, dtype), {})
    pyfq__nev = context.get_function(fnty, sig)
    qmzb__pdito = ir.Constant(pebne__juepj, 1)
    jwmm__ovnb = ir.Constant(pebne__juepj, 5)
    oyh__cubp = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, ezt__dca))
    if for_insert:
        unhr__mvmti = ezt__dca.type(-1)
        ias__pxr = cgutils.alloca_once_value(builder, unhr__mvmti)
    cbexm__jat = builder.append_basic_block('lookup.body')
    zdq__fyls = builder.append_basic_block('lookup.found')
    axs__pzi = builder.append_basic_block('lookup.not_found')
    easwx__xvztg = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        okzt__rsm = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, okzt__rsm)):
            mbt__klbee = pyfq__nev(builder, (item, entry.key))
            with builder.if_then(mbt__klbee):
                builder.branch(zdq__fyls)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, okzt__rsm)):
            builder.branch(axs__pzi)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, okzt__rsm)):
                cvzwm__xmi = builder.load(ias__pxr)
                cvzwm__xmi = builder.select(builder.icmp_unsigned('==',
                    cvzwm__xmi, unhr__mvmti), i, cvzwm__xmi)
                builder.store(cvzwm__xmi, ias__pxr)
    with cgutils.for_range(builder, ir.Constant(pebne__juepj, numba.cpython
        .setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, qmzb__pdito)
        i = builder.and_(i, ezt__dca)
        builder.store(i, index)
    builder.branch(cbexm__jat)
    with builder.goto_block(cbexm__jat):
        i = builder.load(index)
        check_entry(i)
        hekg__gva = builder.load(oyh__cubp)
        hekg__gva = builder.lshr(hekg__gva, jwmm__ovnb)
        i = builder.add(qmzb__pdito, builder.mul(i, jwmm__ovnb))
        i = builder.and_(ezt__dca, builder.add(i, hekg__gva))
        builder.store(i, index)
        builder.store(hekg__gva, oyh__cubp)
        builder.branch(cbexm__jat)
    with builder.goto_block(axs__pzi):
        if for_insert:
            i = builder.load(index)
            cvzwm__xmi = builder.load(ias__pxr)
            i = builder.select(builder.icmp_unsigned('==', cvzwm__xmi,
                unhr__mvmti), i, cvzwm__xmi)
            builder.store(i, index)
        builder.branch(easwx__xvztg)
    with builder.goto_block(zdq__fyls):
        builder.branch(easwx__xvztg)
    builder.position_at_end(easwx__xvztg)
    ecnd__iwv = builder.phi(ir.IntType(1), 'found')
    ecnd__iwv.add_incoming(cgutils.true_bit, zdq__fyls)
    ecnd__iwv.add_incoming(cgutils.false_bit, axs__pzi)
    return ecnd__iwv, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    pejd__nkvbp = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    usz__tjcwc = payload.used
    qmzb__pdito = ir.Constant(usz__tjcwc.type, 1)
    usz__tjcwc = payload.used = builder.add(usz__tjcwc, qmzb__pdito)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, pejd__nkvbp), likely=True):
        payload.fill = builder.add(payload.fill, qmzb__pdito)
    if do_resize:
        self.upsize(usz__tjcwc)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    ecnd__iwv, i = payload._lookup(item, h, for_insert=True)
    xlf__muotj = builder.not_(ecnd__iwv)
    with builder.if_then(xlf__muotj):
        entry = payload.get_entry(i)
        pejd__nkvbp = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        usz__tjcwc = payload.used
        qmzb__pdito = ir.Constant(usz__tjcwc.type, 1)
        usz__tjcwc = payload.used = builder.add(usz__tjcwc, qmzb__pdito)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, pejd__nkvbp), likely=True):
            payload.fill = builder.add(payload.fill, qmzb__pdito)
        if do_resize:
            self.upsize(usz__tjcwc)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    usz__tjcwc = payload.used
    qmzb__pdito = ir.Constant(usz__tjcwc.type, 1)
    usz__tjcwc = payload.used = self._builder.sub(usz__tjcwc, qmzb__pdito)
    if do_resize:
        self.downsize(usz__tjcwc)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    kwh__gwywg = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, kwh__gwywg)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    euzo__ndyls = payload
    xakdh__cpns = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(xakdh__cpns), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with euzo__ndyls._iterate() as qmipb__oyd:
        entry = qmipb__oyd.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(euzo__ndyls.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as qmipb__oyd:
        entry = qmipb__oyd.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    xakdh__cpns = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(xakdh__cpns), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    xakdh__cpns = cgutils.alloca_once_value(builder, cgutils.true_bit)
    pebne__juepj = context.get_value_type(types.intp)
    firda__bssb = ir.Constant(pebne__juepj, 0)
    qmzb__pdito = ir.Constant(pebne__juepj, 1)
    ubktx__jiir = context.get_data_type(types.SetPayload(self._ty))
    mnsax__dlx = context.get_abi_sizeof(ubktx__jiir)
    fqw__kcjp = self._entrysize
    mnsax__dlx -= fqw__kcjp
    txx__yqyyi, knrit__tfhy = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(pebne__juepj, fqw__kcjp), ir.Constant(
        pebne__juepj, mnsax__dlx))
    with builder.if_then(knrit__tfhy, likely=False):
        builder.store(cgutils.false_bit, xakdh__cpns)
    with builder.if_then(builder.load(xakdh__cpns), likely=True):
        if realloc:
            bgfx__zlgn = self._set.meminfo
            zxasl__exa = context.nrt.meminfo_varsize_alloc(builder,
                bgfx__zlgn, size=txx__yqyyi)
            pnfu__cxpib = cgutils.is_null(builder, zxasl__exa)
        else:
            nvxle__ulld = _imp_dtor(context, builder.module, self._ty)
            bgfx__zlgn = context.nrt.meminfo_new_varsize_dtor(builder,
                txx__yqyyi, builder.bitcast(nvxle__ulld, cgutils.voidptr_t))
            pnfu__cxpib = cgutils.is_null(builder, bgfx__zlgn)
        with builder.if_else(pnfu__cxpib, likely=False) as (ehldd__ikyp,
            nvn__ikf):
            with ehldd__ikyp:
                builder.store(cgutils.false_bit, xakdh__cpns)
            with nvn__ikf:
                if not realloc:
                    self._set.meminfo = bgfx__zlgn
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, txx__yqyyi, 255)
                payload.used = firda__bssb
                payload.fill = firda__bssb
                payload.finger = firda__bssb
                icdcn__igj = builder.sub(nentries, qmzb__pdito)
                payload.mask = icdcn__igj
    return builder.load(xakdh__cpns)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    xakdh__cpns = cgutils.alloca_once_value(builder, cgutils.true_bit)
    pebne__juepj = context.get_value_type(types.intp)
    firda__bssb = ir.Constant(pebne__juepj, 0)
    qmzb__pdito = ir.Constant(pebne__juepj, 1)
    ubktx__jiir = context.get_data_type(types.SetPayload(self._ty))
    mnsax__dlx = context.get_abi_sizeof(ubktx__jiir)
    fqw__kcjp = self._entrysize
    mnsax__dlx -= fqw__kcjp
    ezt__dca = src_payload.mask
    nentries = builder.add(qmzb__pdito, ezt__dca)
    txx__yqyyi = builder.add(ir.Constant(pebne__juepj, mnsax__dlx), builder
        .mul(ir.Constant(pebne__juepj, fqw__kcjp), nentries))
    with builder.if_then(builder.load(xakdh__cpns), likely=True):
        nvxle__ulld = _imp_dtor(context, builder.module, self._ty)
        bgfx__zlgn = context.nrt.meminfo_new_varsize_dtor(builder,
            txx__yqyyi, builder.bitcast(nvxle__ulld, cgutils.voidptr_t))
        pnfu__cxpib = cgutils.is_null(builder, bgfx__zlgn)
        with builder.if_else(pnfu__cxpib, likely=False) as (ehldd__ikyp,
            nvn__ikf):
            with ehldd__ikyp:
                builder.store(cgutils.false_bit, xakdh__cpns)
            with nvn__ikf:
                self._set.meminfo = bgfx__zlgn
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = firda__bssb
                payload.mask = ezt__dca
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, fqw__kcjp)
                with src_payload._iterate() as qmipb__oyd:
                    context.nrt.incref(builder, self._ty.dtype, qmipb__oyd.
                        entry.key)
    return builder.load(xakdh__cpns)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    uwzk__vyvk = context.get_value_type(types.voidptr)
    jcwml__euu = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [uwzk__vyvk, jcwml__euu, uwzk__vyvk])
    svjxc__wwmsi = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=svjxc__wwmsi)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ywg__jakj = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ywg__jakj)
        with payload._iterate() as qmipb__oyd:
            entry = qmipb__oyd.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    nytgf__wvok, = sig.args
    brfe__hrme, = args
    gvl__vgkd = numba.core.imputils.call_len(context, builder, nytgf__wvok,
        brfe__hrme)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, gvl__vgkd)
    with numba.core.imputils.for_iter(context, builder, nytgf__wvok, brfe__hrme
        ) as qmipb__oyd:
        inst.add(qmipb__oyd.value)
        context.nrt.decref(builder, set_type.dtype, qmipb__oyd.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    nytgf__wvok = sig.args[1]
    brfe__hrme = args[1]
    gvl__vgkd = numba.core.imputils.call_len(context, builder, nytgf__wvok,
        brfe__hrme)
    if gvl__vgkd is not None:
        xksm__icak = builder.add(inst.payload.used, gvl__vgkd)
        inst.upsize(xksm__icak)
    with numba.core.imputils.for_iter(context, builder, nytgf__wvok, brfe__hrme
        ) as qmipb__oyd:
        nrvor__avuph = context.cast(builder, qmipb__oyd.value, nytgf__wvok.
            dtype, inst.dtype)
        inst.add(nrvor__avuph)
        context.nrt.decref(builder, nytgf__wvok.dtype, qmipb__oyd.value)
    if gvl__vgkd is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    egx__symj = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, egx__symj, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    sjhk__xsgd = target_context.get_executable(library, fndesc, env)
    auz__ctpl = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=sjhk__xsgd, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return auz__ctpl


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._IPythonCacheLocator.
        get_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'eb33b7198697b8ef78edddcf69e58973c44744ff2cb2f54d4015611ad43baed0':
        warnings.warn(
            'numba.core.caching._IPythonCacheLocator.get_cache_path has changed'
            )
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:

    def _get_cache_path(self):
        return numba.config.CACHE_DIR
    numba.core.caching._IPythonCacheLocator.get_cache_path = _get_cache_path
if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.Bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '977423d833eeb4b8fd0c87f55dce7251c107d8d10793fe5723de6e5452da32e2':
        warnings.warn('numba.core.types.containers.Bytes has changed')
numba.core.types.containers.Bytes.slice_is_copy = True
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheLocator.
        ensure_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '906b6f516f76927dfbe69602c335fa151b9f33d40dfe171a9190c0d11627bc03':
        warnings.warn(
            'numba.core.caching._CacheLocator.ensure_cache_path has changed')
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
    import tempfile

    def _ensure_cache_path(self):
        from mpi4py import MPI
        lseni__kwpy = MPI.COMM_WORLD
        if lseni__kwpy.Get_rank() == 0:
            ble__bnus = self.get_cache_path()
            os.makedirs(ble__bnus, exist_ok=True)
            tempfile.TemporaryFile(dir=ble__bnus).close()
    numba.core.caching._CacheLocator.ensure_cache_path = _ensure_cache_path


def _analyze_op_call_builtins_len(self, scope, equiv_set, loc, args, kws):
    from numba.parfors.array_analysis import ArrayAnalysis
    require(len(args) == 1)
    var = args[0]
    typ = self.typemap[var.name]
    require(isinstance(typ, types.ArrayCompatible))
    require(not isinstance(typ, types.Bytes))
    shape = equiv_set._get_shape(var)
    return ArrayAnalysis.AnalyzeResult(shape=shape[0], rhs=shape[0])


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_op_call_builtins_len)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '612cbc67e8e462f25f348b2a5dd55595f4201a6af826cffcd38b16cd85fc70f7':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len has changed'
            )
(numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len
    ) = _analyze_op_call_builtins_len


def generic(self, args, kws):
    assert not kws
    val, = args
    if isinstance(val, (types.Buffer, types.BaseTuple)) and not isinstance(val,
        types.Bytes):
        return signature(types.intp, val)
    elif isinstance(val, types.RangeType):
        return signature(val.dtype, val)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.Len.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '88d54238ebe0896f4s69b7347105a6a68dec443036a61f9e494c1630c62b0fa76':
        warnings.warn('numba.core.typing.builtins.Len.generic has changed')
numba.core.typing.builtins.Len.generic = generic
from numba.cpython import charseq


def _make_constant_bytes(context, builder, nbytes):
    from llvmlite import ir
    qyizz__eqth = cgutils.create_struct_proxy(charseq.bytes_type)
    eacp__vkffi = qyizz__eqth(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(eacp__vkffi.nitems.type, nbytes)
    eacp__vkffi.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    eacp__vkffi.nitems = nbytes
    eacp__vkffi.itemsize = ir.Constant(eacp__vkffi.itemsize.type, 1)
    eacp__vkffi.data = context.nrt.meminfo_data(builder, eacp__vkffi.meminfo)
    eacp__vkffi.parent = cgutils.get_null_value(eacp__vkffi.parent.type)
    eacp__vkffi.shape = cgutils.pack_array(builder, [eacp__vkffi.nitems],
        context.get_value_type(types.intp))
    eacp__vkffi.strides = cgutils.pack_array(builder, [ir.Constant(
        eacp__vkffi.strides.type.element, 1)], context.get_value_type(types
        .intp))
    return eacp__vkffi


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
