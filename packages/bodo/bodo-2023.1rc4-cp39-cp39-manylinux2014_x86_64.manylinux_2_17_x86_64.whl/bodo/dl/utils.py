"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    cohss__ykm = MPI.COMM_WORLD
    osyki__gaq = cohss__ykm.Get_rank()
    mbijm__ygel = get_host_ranks()
    gys__onx = get_nodes_first_ranks()
    if osyki__gaq in gys__onx:
        try:
            vtbvu__oaqzr = get_num_gpus(framework)
        except Exception as zlf__hqml:
            vtbvu__oaqzr = zlf__hqml
        gzb__pquqj = create_subcomm_mpi4py(gys__onx)
        tyd__ukdv = gzb__pquqj.gather(vtbvu__oaqzr)
        if osyki__gaq == 0:
            gpu_ranks = []
            wan__pyqon = None
            for bgw__idxjm, ylm__koxaq in enumerate(mbijm__ygel.values()):
                vho__mzdl = tyd__ukdv[bgw__idxjm]
                if isinstance(vho__mzdl, Exception):
                    wan__pyqon = vho__mzdl
                    break
                if vho__mzdl == 0:
                    continue
                byhh__vacn = len(ylm__koxaq) // vho__mzdl
                for hfc__mqojr, rotv__xks in enumerate(ylm__koxaq):
                    if hfc__mqojr % byhh__vacn == 0:
                        tob__wsvx = hfc__mqojr / byhh__vacn
                        if tob__wsvx < vho__mzdl:
                            gpu_ranks.append(rotv__xks)
            if wan__pyqon:
                cohss__ykm.bcast(wan__pyqon)
                raise wan__pyqon
            else:
                cohss__ykm.bcast(gpu_ranks)
    if osyki__gaq != 0:
        gpu_ranks = cohss__ykm.bcast(None)
        if isinstance(gpu_ranks, Exception):
            zlf__hqml = gpu_ranks
            raise zlf__hqml
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    eapfb__jluq = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        gzb__pquqj = MPI.COMM_WORLD.Split(color=0 if eapfb__jluq in
            gpu_ranks else MPI.UNDEFINED, key=eapfb__jluq)
        if gzb__pquqj != MPI.COMM_NULL:
            hvd.init(comm=gzb__pquqj)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                axm__cjj = tf.config.experimental.list_physical_devices('GPU')
                for myk__gycf in axm__cjj:
                    tf.config.experimental.set_memory_growth(myk__gycf, True)
                tf.config.experimental.set_visible_devices(axm__cjj[hvd.
                    local_rank()], 'GPU')
    else:
        if eapfb__jluq == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        sqefk__hjy = 17
        cohss__ykm = MPI.COMM_WORLD
        obgg__szju = MPI.Get_processor_name()
        bglau__fqysb = get_host_ranks()[obgg__szju]
        assert_dl_initialized()
        if bodo.get_rank() == bglau__fqysb[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for osyki__gaq in bglau__fqysb[1:]:
                cohss__ykm.isend(1, dest=osyki__gaq, tag=sqefk__hjy)
        else:
            while True:
                igexl__jqan = MPI.Status()
                naeo__yeua = cohss__ykm.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    igexl__jqan)
                if naeo__yeua:
                    assert igexl__jqan.source == bglau__fqysb[0]
                    assert igexl__jqan.tag == sqefk__hjy
                    cohss__ykm.recv(source=0, tag=sqefk__hjy)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
