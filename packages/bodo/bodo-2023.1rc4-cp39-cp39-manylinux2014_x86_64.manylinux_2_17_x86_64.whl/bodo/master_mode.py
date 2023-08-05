import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        zml__muyv = state
        uoys__ufwd = inspect.getsourcelines(zml__muyv)[0][0]
        assert uoys__ufwd.startswith('@bodo.jit') or uoys__ufwd.startswith(
            '@jit')
        fjzkf__sxpd = eval(uoys__ufwd[1:])
        self.dispatcher = fjzkf__sxpd(zml__muyv)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    bss__ildge = MPI.COMM_WORLD
    while True:
        ybeaq__sqlz = bss__ildge.bcast(None, root=MASTER_RANK)
        if ybeaq__sqlz[0] == 'exec':
            zml__muyv = pickle.loads(ybeaq__sqlz[1])
            for bomc__mnj, epm__mil in list(zml__muyv.__globals__.items()):
                if isinstance(epm__mil, MasterModeDispatcher):
                    zml__muyv.__globals__[bomc__mnj] = epm__mil.dispatcher
            if zml__muyv.__module__ not in sys.modules:
                sys.modules[zml__muyv.__module__] = pytypes.ModuleType(
                    zml__muyv.__module__)
            uoys__ufwd = inspect.getsourcelines(zml__muyv)[0][0]
            assert uoys__ufwd.startswith('@bodo.jit') or uoys__ufwd.startswith(
                '@jit')
            fjzkf__sxpd = eval(uoys__ufwd[1:])
            func = fjzkf__sxpd(zml__muyv)
            lhhpm__iiyi = ybeaq__sqlz[2]
            vthjy__adeg = ybeaq__sqlz[3]
            ylk__btjf = []
            for hahwr__uqz in lhhpm__iiyi:
                if hahwr__uqz == 'scatter':
                    ylk__btjf.append(bodo.scatterv(None))
                elif hahwr__uqz == 'bcast':
                    ylk__btjf.append(bss__ildge.bcast(None, root=MASTER_RANK))
            gscx__zvcp = {}
            for argname, hahwr__uqz in vthjy__adeg.items():
                if hahwr__uqz == 'scatter':
                    gscx__zvcp[argname] = bodo.scatterv(None)
                elif hahwr__uqz == 'bcast':
                    gscx__zvcp[argname] = bss__ildge.bcast(None, root=
                        MASTER_RANK)
            chzm__kqc = func(*ylk__btjf, **gscx__zvcp)
            if chzm__kqc is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(chzm__kqc)
            del (ybeaq__sqlz, zml__muyv, func, fjzkf__sxpd, lhhpm__iiyi,
                vthjy__adeg, ylk__btjf, gscx__zvcp, chzm__kqc)
            gc.collect()
        elif ybeaq__sqlz[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    bss__ildge = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        lhhpm__iiyi = ['scatter' for gswzv__najp in range(len(args))]
        vthjy__adeg = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        ctyi__nuauo = func.py_func.__code__.co_varnames
        mhwi__mgzx = func.targetoptions

        def get_distribution(argname):
            if argname in mhwi__mgzx.get('distributed', []
                ) or argname in mhwi__mgzx.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        lhhpm__iiyi = [get_distribution(argname) for argname in ctyi__nuauo
            [:len(args)]]
        vthjy__adeg = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    iea__cmymf = pickle.dumps(func.py_func)
    bss__ildge.bcast(['exec', iea__cmymf, lhhpm__iiyi, vthjy__adeg])
    ylk__btjf = []
    for dets__mlnx, hahwr__uqz in zip(args, lhhpm__iiyi):
        if hahwr__uqz == 'scatter':
            ylk__btjf.append(bodo.scatterv(dets__mlnx))
        elif hahwr__uqz == 'bcast':
            bss__ildge.bcast(dets__mlnx)
            ylk__btjf.append(dets__mlnx)
    gscx__zvcp = {}
    for argname, dets__mlnx in kwargs.items():
        hahwr__uqz = vthjy__adeg[argname]
        if hahwr__uqz == 'scatter':
            gscx__zvcp[argname] = bodo.scatterv(dets__mlnx)
        elif hahwr__uqz == 'bcast':
            bss__ildge.bcast(dets__mlnx)
            gscx__zvcp[argname] = dets__mlnx
    toolz__hynk = []
    for bomc__mnj, epm__mil in list(func.py_func.__globals__.items()):
        if isinstance(epm__mil, MasterModeDispatcher):
            toolz__hynk.append((func.py_func.__globals__, bomc__mnj, func.
                py_func.__globals__[bomc__mnj]))
            func.py_func.__globals__[bomc__mnj] = epm__mil.dispatcher
    chzm__kqc = func(*ylk__btjf, **gscx__zvcp)
    for daeet__ufld, bomc__mnj, epm__mil in toolz__hynk:
        daeet__ufld[bomc__mnj] = epm__mil
    if chzm__kqc is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        chzm__kqc = bodo.gatherv(chzm__kqc)
    return chzm__kqc


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
