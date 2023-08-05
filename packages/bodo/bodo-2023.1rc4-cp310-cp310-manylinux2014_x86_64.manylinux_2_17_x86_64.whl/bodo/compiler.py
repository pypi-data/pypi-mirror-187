"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        srat__pldr = 'bodo' if distributed else 'bodo_seq'
        srat__pldr = (srat__pldr + '_inline' if inline_calls_pass else
            srat__pldr)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, srat__pldr
            )
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for jyi__csxh, (icfs__sjzbk, kkr__lfmuo) in enumerate(pm.passes):
        if icfs__sjzbk == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(jyi__csxh, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for jyi__csxh, (icfs__sjzbk, kkr__lfmuo) in enumerate(pm.passes):
        if icfs__sjzbk == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[jyi__csxh] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for jyi__csxh, (icfs__sjzbk, kkr__lfmuo) in enumerate(pm.passes):
        if icfs__sjzbk == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(jyi__csxh)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    tqeag__ojs = guard(get_definition, func_ir, rhs.func)
    if isinstance(tqeag__ojs, (ir.Global, ir.FreeVar, ir.Const)):
        ajifs__kthxf = tqeag__ojs.value
    else:
        yzfkz__lfsf = guard(find_callname, func_ir, rhs)
        if not (yzfkz__lfsf and isinstance(yzfkz__lfsf[0], str) and
            isinstance(yzfkz__lfsf[1], str)):
            return
        func_name, func_mod = yzfkz__lfsf
        try:
            import importlib
            pbqfn__oepks = importlib.import_module(func_mod)
            ajifs__kthxf = getattr(pbqfn__oepks, func_name)
        except:
            return
    if isinstance(ajifs__kthxf, CPUDispatcher) and issubclass(ajifs__kthxf.
        _compiler.pipeline_class, BodoCompiler
        ) and ajifs__kthxf._compiler.pipeline_class != BodoCompilerUDF:
        ajifs__kthxf._compiler.pipeline_class = BodoCompilerUDF
        ajifs__kthxf.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kwwd__tnk in block.body:
                if is_call_assign(kwwd__tnk):
                    _convert_bodo_dispatcher_to_udf(kwwd__tnk.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        ldixq__xtb = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags, isinstance(state.
            pipeline, BodoCompilerSeq))
        ldixq__xtb.run()
        return True


def _update_definitions(func_ir, node_list):
    gftm__qitrv = ir.Loc('', 0)
    vxt__wbrbr = ir.Block(ir.Scope(None, gftm__qitrv), gftm__qitrv)
    vxt__wbrbr.body = node_list
    build_definitions({(0): vxt__wbrbr}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        kkkku__iqkbo = 'overload_series_' + rhs.attr
        vduep__ekm = getattr(bodo.hiframes.series_impl, kkkku__iqkbo)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        kkkku__iqkbo = 'overload_dataframe_' + rhs.attr
        vduep__ekm = getattr(bodo.hiframes.dataframe_impl, kkkku__iqkbo)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    qlbqn__pok = vduep__ekm(rhs_type)
    nouhh__znji = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc
        )
    dibt__luq = compile_func_single_block(qlbqn__pok, (rhs.value,), stmt.
        target, nouhh__znji)
    _update_definitions(func_ir, dibt__luq)
    new_body += dibt__luq
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        tknjf__hhc = tuple(typemap[vnyqt__vnhs.name] for vnyqt__vnhs in rhs
            .args)
        ftdk__jjni = {srat__pldr: typemap[vnyqt__vnhs.name] for srat__pldr,
            vnyqt__vnhs in dict(rhs.kws).items()}
        qlbqn__pok = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*tknjf__hhc, **ftdk__jjni)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        tknjf__hhc = tuple(typemap[vnyqt__vnhs.name] for vnyqt__vnhs in rhs
            .args)
        ftdk__jjni = {srat__pldr: typemap[vnyqt__vnhs.name] for srat__pldr,
            vnyqt__vnhs in dict(rhs.kws).items()}
        qlbqn__pok = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*tknjf__hhc, **ftdk__jjni)
    else:
        return False
    aogxg__hgdza = replace_func(pass_info, qlbqn__pok, rhs.args, pysig=
        numba.core.utils.pysignature(qlbqn__pok), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    acnxr__wrh, kkr__lfmuo = inline_closure_call(func_ir, aogxg__hgdza.
        glbls, block, len(new_body), aogxg__hgdza.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=aogxg__hgdza.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for apmr__gvy in acnxr__wrh.values():
        apmr__gvy.loc = rhs.loc
        update_locs(apmr__gvy.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    mqsbb__fye = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = mqsbb__fye(func_ir, typemap)
    ghfva__xrdus = func_ir.blocks
    work_list = list((wbcv__dbp, ghfva__xrdus[wbcv__dbp]) for wbcv__dbp in
        reversed(ghfva__xrdus.keys()))
    while work_list:
        svrpt__vohi, block = work_list.pop()
        new_body = []
        txklx__dfs = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                yzfkz__lfsf = guard(find_callname, func_ir, rhs, typemap)
                if yzfkz__lfsf is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = yzfkz__lfsf
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    txklx__dfs = True
                    break
            new_body.append(stmt)
        if not txklx__dfs:
            ghfva__xrdus[svrpt__vohi].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        trts__gqdpt = DistributedPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = trts__gqdpt.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        ang__vdfbb = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        ghwf__xyqc = ang__vdfbb.run()
        kdyi__ekwy = ghwf__xyqc
        if kdyi__ekwy:
            kdyi__ekwy = ang__vdfbb.run()
        if kdyi__ekwy:
            ang__vdfbb.run()
        return ghwf__xyqc


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        www__mdb = 0
        moc__pjmvk = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            www__mdb = int(os.environ[moc__pjmvk])
        except:
            pass
        if www__mdb > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(www__mdb, state.
                metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        nouhh__znji = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, nouhh__znji)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kwwd__tnk in block.body:
                if type(kwwd__tnk) in distributed_run_extensions:
                    upm__pofx = distributed_run_extensions[type(kwwd__tnk)]
                    if isinstance(kwwd__tnk, bodo.ir.parquet_ext.ParquetReader
                        ) or isinstance(kwwd__tnk, bodo.ir.sql_ext.SqlReader
                        ) and kwwd__tnk.db_type in ('iceberg', 'snowflake'):
                        tbjzf__dsaf = upm__pofx(kwwd__tnk, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        tbjzf__dsaf = upm__pofx(kwwd__tnk, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += tbjzf__dsaf
                elif is_call_assign(kwwd__tnk):
                    rhs = kwwd__tnk.value
                    yzfkz__lfsf = guard(find_callname, state.func_ir, rhs)
                    if yzfkz__lfsf == ('gatherv', 'bodo') or yzfkz__lfsf == (
                        'allgatherv', 'bodo'):
                        kjus__amvs = state.typemap[kwwd__tnk.target.name]
                        iwo__lvgpk = state.typemap[rhs.args[0].name]
                        if isinstance(iwo__lvgpk, types.Array) and isinstance(
                            kjus__amvs, types.Array):
                            rus__rew = iwo__lvgpk.copy(readonly=False)
                            onyng__fry = kjus__amvs.copy(readonly=False)
                            if rus__rew == onyng__fry:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kwwd__tnk.target, nouhh__znji)
                                continue
                        if (kjus__amvs != iwo__lvgpk and 
                            to_str_arr_if_dict_array(kjus__amvs) ==
                            to_str_arr_if_dict_array(iwo__lvgpk)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kwwd__tnk.target,
                                nouhh__znji, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kwwd__tnk.value = rhs.args[0]
                    new_body.append(kwwd__tnk)
                else:
                    new_body.append(kwwd__tnk)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bkvt__ouwuo = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return bkvt__ouwuo.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    qmv__pjidk = set()
    while work_list:
        svrpt__vohi, block = work_list.pop()
        qmv__pjidk.add(svrpt__vohi)
        for i, qyl__rnzx in enumerate(block.body):
            if isinstance(qyl__rnzx, ir.Assign):
                vbgk__pdzqu = qyl__rnzx.value
                if isinstance(vbgk__pdzqu, ir.Expr
                    ) and vbgk__pdzqu.op == 'call':
                    tqeag__ojs = guard(get_definition, func_ir, vbgk__pdzqu
                        .func)
                    if isinstance(tqeag__ojs, (ir.Global, ir.FreeVar)
                        ) and isinstance(tqeag__ojs.value, CPUDispatcher
                        ) and issubclass(tqeag__ojs.value._compiler.
                        pipeline_class, BodoCompiler):
                        zrijt__yurpf = tqeag__ojs.value.py_func
                        arg_types = None
                        if typingctx:
                            xszo__ozhk = dict(vbgk__pdzqu.kws)
                            hubpl__ymse = tuple(typemap[vnyqt__vnhs.name] for
                                vnyqt__vnhs in vbgk__pdzqu.args)
                            hfzs__audn = {eegt__knbze: typemap[vnyqt__vnhs.
                                name] for eegt__knbze, vnyqt__vnhs in
                                xszo__ozhk.items()}
                            kkr__lfmuo, arg_types = (tqeag__ojs.value.
                                fold_argument_types(hubpl__ymse, hfzs__audn))
                        kkr__lfmuo, dusn__tzd = inline_closure_call(func_ir,
                            zrijt__yurpf.__globals__, block, i,
                            zrijt__yurpf, typingctx=typingctx, targetctx=
                            targetctx, arg_typs=arg_types, typemap=typemap,
                            calltypes=calltypes, work_list=work_list)
                        _locals.update((dusn__tzd[eegt__knbze].name,
                            vnyqt__vnhs) for eegt__knbze, vnyqt__vnhs in
                            tqeag__ojs.value.locals.items() if eegt__knbze in
                            dusn__tzd)
                        break
    return qmv__pjidk


def udf_jit(signature_or_function=None, **options):
    qggtf__izgs = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=qggtf__izgs,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for jyi__csxh, (icfs__sjzbk, kkr__lfmuo) in enumerate(pm.passes):
        if icfs__sjzbk == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:jyi__csxh + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    pmbo__ecj = None
    acq__bkdjr = None
    _locals = {}
    squnb__jrr = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(squnb__jrr, arg_types,
        kw_types)
    qls__vnyab = numba.core.compiler.Flags()
    mgw__cdn = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    lgx__lyig = {'nopython': True, 'boundscheck': False, 'parallel': mgw__cdn}
    numba.core.registry.cpu_target.options.parse_as_flags(qls__vnyab, lgx__lyig
        )
    cjk__mbnsa = TyperCompiler(typingctx, targetctx, pmbo__ecj, args,
        acq__bkdjr, qls__vnyab, _locals)
    return cjk__mbnsa.compile_extra(func)
