"""
Defines decorators of Bodo. Currently just @jit.
"""
import hashlib
import inspect
import warnings
import numba
from numba.core import cpu
from numba.core.options import _mapping
from numba.core.targetconfig import Option, TargetConfig
import bodo
from bodo import master_mode
numba.core.cpu.CPUTargetOptions.all_args_distributed_block = _mapping(
    'all_args_distributed_block')
numba.core.cpu.CPUTargetOptions.all_args_distributed_varlength = _mapping(
    'all_args_distributed_varlength')
numba.core.cpu.CPUTargetOptions.all_returns_distributed = _mapping(
    'all_returns_distributed')
numba.core.cpu.CPUTargetOptions.returns_maybe_distributed = _mapping(
    'returns_maybe_distributed')
numba.core.cpu.CPUTargetOptions.args_maybe_distributed = _mapping(
    'args_maybe_distributed')
numba.core.cpu.CPUTargetOptions.distributed = _mapping('distributed')
numba.core.cpu.CPUTargetOptions.distributed_block = _mapping(
    'distributed_block')
numba.core.cpu.CPUTargetOptions.replicated = _mapping('replicated')
numba.core.cpu.CPUTargetOptions.threaded = _mapping('threaded')
numba.core.cpu.CPUTargetOptions.pivots = _mapping('pivots')
numba.core.cpu.CPUTargetOptions.h5_types = _mapping('h5_types')


class Flags(TargetConfig):
    enable_looplift = Option(type=bool, default=False, doc=
        'Enable loop-lifting')
    enable_pyobject = Option(type=bool, default=False, doc=
        'Enable pyobject mode (in general)')
    enable_pyobject_looplift = Option(type=bool, default=False, doc=
        'Enable pyobject mode inside lifted loops')
    enable_ssa = Option(type=bool, default=True, doc='Enable SSA')
    force_pyobject = Option(type=bool, default=False, doc=
        'Force pyobject mode inside the whole function')
    release_gil = Option(type=bool, default=False, doc=
        'Release GIL inside the native function')
    no_compile = Option(type=bool, default=False, doc='TODO')
    debuginfo = Option(type=bool, default=False, doc='TODO')
    boundscheck = Option(type=bool, default=False, doc='TODO')
    forceinline = Option(type=bool, default=False, doc='TODO')
    no_cpython_wrapper = Option(type=bool, default=False, doc='TODO')
    no_cfunc_wrapper = Option(type=bool, default=False, doc='TODO')
    auto_parallel = Option(type=cpu.ParallelOptions, default=cpu.
        ParallelOptions(False), doc=
        """Enable automatic parallel optimization, can be fine-tuned by
taking a dictionary of sub-options instead of a boolean, see parfor.py for
detail"""
        )
    nrt = Option(type=bool, default=False, doc='TODO')
    no_rewrites = Option(type=bool, default=False, doc='TODO')
    error_model = Option(type=str, default='python', doc='TODO')
    fastmath = Option(type=cpu.FastMathOptions, default=cpu.FastMathOptions
        (False), doc='TODO')
    noalias = Option(type=bool, default=False, doc='TODO')
    inline = Option(type=cpu.InlineOptions, default=cpu.InlineOptions(
        'never'), doc='TODO')
    target_backend = Option(type=str, default='cpu', doc='backend')
    all_args_distributed_block = Option(type=bool, default=False, doc=
        'All args have 1D distribution')
    all_args_distributed_varlength = Option(type=bool, default=False, doc=
        'All args have 1D_Var distribution')
    all_returns_distributed = Option(type=bool, default=False, doc=
        'All returns are distributed')
    returns_maybe_distributed = Option(type=bool, default=True, doc=
        'Returns may be distributed')
    args_maybe_distributed = Option(type=bool, default=True, doc=
        'Arguments may be distributed')
    distributed = Option(type=set, default=set(), doc=
        'distributed arguments or returns')
    distributed_block = Option(type=set, default=set(), doc=
        'distributed 1D arguments or returns')
    replicated = Option(type=set, default=set(), doc=
        'replicated arguments or returns')
    threaded = Option(type=set, default=set(), doc=
        'Threaded arguments or returns')
    pivots = Option(type=dict, default=dict(), doc='pivot values')
    h5_types = Option(type=dict, default=dict(), doc='HDF5 read data types')


DEFAULT_FLAGS = Flags()
DEFAULT_FLAGS.nrt = True
if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.core.compiler.Flags)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9d5f7a93545fe783c20a9d7579c73e04d91d6b2841fb5972b391a67fff03b9c3':
        warnings.warn('numba.core.compiler.Flags has changed')
numba.core.compiler.Flags = Flags
numba.core.compiler.DEFAULT_FLAGS = DEFAULT_FLAGS


def distributed_diagnostics(self, signature=None, level=1):
    if signature is None and len(self.signatures) == 0:
        raise bodo.utils.typing.BodoError(
            'Distributed diagnostics not available for a function that is not compiled yet'
            )
    if bodo.get_rank() != 0:
        return

    def dump(sig):
        tbes__dmkvx = self.overloads[sig]
        nlu__yyuzv = tbes__dmkvx.metadata.get('distributed_diagnostics', None)
        if nlu__yyuzv is None:
            eajnl__cya = 'No distributed diagnostic available'
            raise bodo.utils.typing.BodoError(eajnl__cya)
        nlu__yyuzv.dump(level, self.get_metadata(sig))
    if signature is not None:
        dump(signature)
    else:
        [dump(sig) for sig in self.signatures]


numba.core.dispatcher.Dispatcher.distributed_diagnostics = (
    distributed_diagnostics)


def master_mode_wrapper(numba_jit_wrapper):

    def _wrapper(pyfunc):
        hrfky__iiq = numba_jit_wrapper(pyfunc)
        return master_mode.MasterModeDispatcher(hrfky__iiq)
    return _wrapper


def is_jit_execution():
    return False


@numba.extending.overload(is_jit_execution)
def is_jit_execution_overload():
    return lambda : True


def jit(signature_or_function=None, pipeline_class=None, **options):
    _init_extensions()
    if 'nopython' not in options:
        options['nopython'] = True
    options['parallel'] = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    pipeline_class = (bodo.compiler.BodoCompiler if pipeline_class is None else
        pipeline_class)
    if 'distributed' in options and isinstance(options['distributed'], bool):
        pcr__zpia = options.pop('distributed')
        pipeline_class = (pipeline_class if pcr__zpia else bodo.compiler.
            BodoCompilerSeq)
    if 'replicated' in options and isinstance(options['replicated'], bool):
        mvyrb__kot = options.pop('replicated')
        pipeline_class = (bodo.compiler.BodoCompilerSeq if mvyrb__kot else
            pipeline_class)
    aqv__nuqge = numba.jit(signature_or_function, pipeline_class=
        pipeline_class, **options)
    if master_mode.master_mode_on and bodo.get_rank(
        ) == master_mode.MASTER_RANK:
        if isinstance(aqv__nuqge, numba.dispatcher._DispatcherBase):
            return master_mode.MasterModeDispatcher(aqv__nuqge)
        else:
            return master_mode_wrapper(aqv__nuqge)
    else:
        return aqv__nuqge


def _init_extensions():
    import sys
    bvmoo__nne = False
    if 'sklearn' in sys.modules and 'bodo.libs.sklearn_ext' not in sys.modules:
        import bodo.libs.sklearn_ext
        bvmoo__nne = True
    if ('matplotlib' in sys.modules and 'bodo.libs.matplotlib_ext' not in
        sys.modules):
        import bodo.libs.matplotlib_ext
        bvmoo__nne = True
    if 'xgboost' in sys.modules and 'bodo.libs.xgb_ext' not in sys.modules:
        import bodo.libs.xgb_ext
        bvmoo__nne = True
    if 'h5py' in sys.modules and 'bodo.io.h5_api' not in sys.modules:
        import bodo.io.h5_api
        if bodo.utils.utils.has_supported_h5py():
            from bodo.io import h5
        bvmoo__nne = True
    if 'pyspark' in sys.modules and 'bodo.libs.pyspark_ext' not in sys.modules:
        import pyspark.sql.functions
        import bodo.libs.pyspark_ext
        bodo.utils.transform.no_side_effect_call_tuples.update({('col',
            pyspark.sql.functions), (pyspark.sql.functions.col,), ('sum',
            pyspark.sql.functions), (pyspark.sql.functions.sum,)})
        bvmoo__nne = True
    if bvmoo__nne:
        numba.core.registry.cpu_target.target_context.refresh()
