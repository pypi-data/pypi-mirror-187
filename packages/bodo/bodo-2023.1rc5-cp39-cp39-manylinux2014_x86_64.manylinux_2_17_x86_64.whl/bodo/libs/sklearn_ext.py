"""Support scikit-learn using object mode of Numba """
import itertools
import numbers
import sys
import types as pytypes
import warnings
from itertools import combinations
import numba
import numpy as np
import pandas as pd
import sklearn.cluster
import sklearn.ensemble
import sklearn.feature_extraction
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.svm
import sklearn.utils
from mpi4py import MPI
from numba.core import types
from numba.extending import overload, overload_attribute, overload_method, register_jitable
from scipy import stats
from scipy.special import comb
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import hinge_loss, log_loss, mean_squared_error
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing._data import _handle_zeros_in_scale as sklearn_handle_zeros_in_scale
from sklearn.utils._encode import _unique
from sklearn.utils.extmath import _safe_accumulator_op as sklearn_safe_accumulator_op
from sklearn.utils.validation import _check_sample_weight, column_or_1d
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.csr_matrix_ext import CSRMatrixType
from bodo.libs.distributed_api import Reduce_Type, create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks, get_num_nodes
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, get_overload_const, get_overload_const_int, get_overload_const_str, is_overload_constant_number, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true
this_module = sys.modules[__name__]
_is_sklearn_supported_version = False
_min_sklearn_version = 1, 1, 0
_min_sklearn_ver_str = '.'.join(str(x) for x in _min_sklearn_version)
_max_sklearn_version_exclusive = 1, 2, 0
_max_sklearn_ver_str = '.'.join(str(x) for x in _max_sklearn_version_exclusive)
try:
    import re
    import sklearn
    regex = re.compile('(\\d+)\\.(\\d+)\\..*(\\d+)')
    sklearn_version = sklearn.__version__
    m = regex.match(sklearn_version)
    if m:
        ver = tuple(map(int, m.groups()))
        if (ver >= _min_sklearn_version and ver <
            _max_sklearn_version_exclusive):
            _is_sklearn_supported_version = True
except ImportError as jobg__wdsr:
    pass


def check_sklearn_version():
    if not _is_sklearn_supported_version:
        ddkf__huuu = f""" Bodo supports scikit-learn version >= {_min_sklearn_ver_str} and < {_max_sklearn_ver_str}.
             Installed version is {sklearn.__version__}.
"""
        raise BodoError(ddkf__huuu)


def random_forest_model_fit(m, X, y):
    jttx__wkeal = m.n_estimators
    cocn__hdd = MPI.Get_processor_name()
    ipzzs__gxe = get_host_ranks()
    ireh__xkh = len(ipzzs__gxe)
    tkl__xpe = bodo.get_rank()
    m.n_estimators = bodo.libs.distributed_api.get_node_portion(jttx__wkeal,
        ireh__xkh, tkl__xpe)
    if tkl__xpe == ipzzs__gxe[cocn__hdd][0]:
        m.n_jobs = len(ipzzs__gxe[cocn__hdd])
        if m.random_state is None:
            m.random_state = np.random.RandomState()
        from sklearn.utils import parallel_backend
        with parallel_backend('threading'):
            m.fit(X, y)
        m.n_jobs = 1
    with numba.objmode(first_rank_node='int32[:]'):
        first_rank_node = get_nodes_first_ranks()
    xxlun__fou = create_subcomm_mpi4py(first_rank_node)
    if xxlun__fou != MPI.COMM_NULL:
        qdi__jdrm = 10
        feau__shwcm = bodo.libs.distributed_api.get_node_portion(jttx__wkeal,
            ireh__xkh, 0)
        whndj__sdy = feau__shwcm // qdi__jdrm
        if feau__shwcm % qdi__jdrm != 0:
            whndj__sdy += 1
        ciiyq__cdp = []
        for sox__hscf in range(whndj__sdy):
            qctzn__bqmbb = xxlun__fou.gather(m.estimators_[sox__hscf *
                qdi__jdrm:sox__hscf * qdi__jdrm + qdi__jdrm])
            if tkl__xpe == 0:
                ciiyq__cdp += list(itertools.chain.from_iterable(qctzn__bqmbb))
        if tkl__xpe == 0:
            m.estimators_ = ciiyq__cdp
    dmbdm__fdzd = MPI.COMM_WORLD
    if tkl__xpe == 0:
        for sox__hscf in range(0, jttx__wkeal, 10):
            dmbdm__fdzd.bcast(m.estimators_[sox__hscf:sox__hscf + 10])
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            dmbdm__fdzd.bcast(m.n_classes_)
            dmbdm__fdzd.bcast(m.classes_)
        dmbdm__fdzd.bcast(m.n_outputs_)
    else:
        ehq__tpf = []
        for sox__hscf in range(0, jttx__wkeal, 10):
            ehq__tpf += dmbdm__fdzd.bcast(None)
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            m.n_classes_ = dmbdm__fdzd.bcast(None)
            m.classes_ = dmbdm__fdzd.bcast(None)
        m.n_outputs_ = dmbdm__fdzd.bcast(None)
        m.estimators_ = ehq__tpf
    assert len(m.estimators_) == jttx__wkeal
    m.n_estimators = jttx__wkeal
    m.n_features_in_ = X.shape[1]


BodoRandomForestClassifierType = install_py_obj_class(types_name=
    'random_forest_classifier_type', python_type=sklearn.ensemble.
    RandomForestClassifier, module=this_module, class_name=
    'BodoRandomForestClassifierType', model_name=
    'BodoRandomForestClassifierModel')


@overload(sklearn.ensemble.RandomForestClassifier, no_unliteral=True)
def sklearn_ensemble_RandomForestClassifier_overload(n_estimators=100,
    criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf
    =1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False,
    class_weight=None, ccp_alpha=0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestClassifier_impl(n_estimators=100,
        criterion='gini', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_classifier_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestClassifier(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, class_weight=class_weight,
                ccp_alpha=ccp_alpha, max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestClassifier_impl


def parallel_predict_regression(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='float64[:]'):
            m.n_jobs = 1
            if len(X) == 0:
                result = np.empty(0, dtype=np.float64)
            else:
                result = m.predict(X).astype(np.float64).flatten()
        return result
    return _model_predict_impl


def parallel_predict(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='int64[:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty(0, dtype=np.int64)
            else:
                result = m.predict(X).astype(np.int64).flatten()
        return result
    return _model_predict_impl


def parallel_predict_proba(m, X):
    check_sklearn_version()

    def _model_predict_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_proba(X).astype(np.float64)
        return result
    return _model_predict_proba_impl


def parallel_predict_log_proba(m, X):
    check_sklearn_version()

    def _model_predict_log_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_log_proba(X).astype(np.float64)
        return result
    return _model_predict_log_proba_impl


def parallel_score(m, X, y, sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()

    def _model_score_impl(m, X, y, sample_weight=None, _is_data_distributed
        =False):
        with numba.objmode(result='float64[:]'):
            result = m.score(X, y, sample_weight=sample_weight)
            if _is_data_distributed:
                result = np.full(len(y), result)
            else:
                result = np.array([result])
        if _is_data_distributed:
            result = bodo.allgatherv(result)
        return result.mean()
    return _model_score_impl


@overload_method(BodoRandomForestClassifierType, 'predict', no_unliteral=True)
def overload_model_predict(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict. (Data parallelization)"""
    return parallel_predict(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_proba',
    no_unliteral=True)
def overload_rf_predict_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_proba. (Data parallelization)"""
    return parallel_predict_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_log_proba',
    no_unliteral=True)
def overload_rf_predict_log_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_log_proba. (Data parallelization)"""
    return parallel_predict_log_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'score', no_unliteral=True)
def overload_model_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


def precision_recall_fscore_support_helper(MCM, average):

    def multilabel_confusion_matrix(y_true, y_pred, *, sample_weight=None,
        labels=None, samplewise=False):
        return MCM
    ybi__byfo = sklearn.metrics._classification.multilabel_confusion_matrix
    result = -1.0
    try:
        sklearn.metrics._classification.multilabel_confusion_matrix = (
            multilabel_confusion_matrix)
        result = (sklearn.metrics._classification.
            precision_recall_fscore_support([], [], average=average))
    finally:
        sklearn.metrics._classification.multilabel_confusion_matrix = ybi__byfo
    return result


@numba.njit
def precision_recall_fscore_parallel(y_true, y_pred, operation, average=
    'binary'):
    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)
    labels = bodo.allgatherv(labels, False)
    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False
        )
    ter__fren = len(labels)
    zqynt__ptj = np.zeros(ter__fren, np.int64)
    jfp__lzm = np.zeros(ter__fren, np.int64)
    djtcr__uak = np.zeros(ter__fren, np.int64)
    lptu__zrd = (bodo.hiframes.pd_categorical_ext.
        get_label_dict_from_categories(labels))
    for sox__hscf in range(len(y_true)):
        jfp__lzm[lptu__zrd[y_true[sox__hscf]]] += 1
        if y_pred[sox__hscf] not in lptu__zrd:
            continue
        vmwa__jec = lptu__zrd[y_pred[sox__hscf]]
        djtcr__uak[vmwa__jec] += 1
        if y_true[sox__hscf] == y_pred[sox__hscf]:
            zqynt__ptj[vmwa__jec] += 1
    zqynt__ptj = bodo.libs.distributed_api.dist_reduce(zqynt__ptj, np.int32
        (Reduce_Type.Sum.value))
    jfp__lzm = bodo.libs.distributed_api.dist_reduce(jfp__lzm, np.int32(
        Reduce_Type.Sum.value))
    djtcr__uak = bodo.libs.distributed_api.dist_reduce(djtcr__uak, np.int32
        (Reduce_Type.Sum.value))
    cfaaj__eaavx = djtcr__uak - zqynt__ptj
    shacj__rva = jfp__lzm - zqynt__ptj
    omnq__mxb = zqynt__ptj
    flabh__syaou = y_true.shape[0] - omnq__mxb - cfaaj__eaavx - shacj__rva
    with numba.objmode(result='float64[:]'):
        MCM = np.array([flabh__syaou, cfaaj__eaavx, shacj__rva, omnq__mxb]
            ).T.reshape(-1, 2, 2)
        if operation == 'precision':
            result = precision_recall_fscore_support_helper(MCM, average)[0]
        elif operation == 'recall':
            result = precision_recall_fscore_support_helper(MCM, average)[1]
        elif operation == 'f1':
            result = precision_recall_fscore_support_helper(MCM, average)[2]
        if average is not None:
            result = np.array([result])
    return result


@overload(sklearn.metrics.precision_score, no_unliteral=True)
def overload_precision_score(y_true, y_pred, labels=None, pos_label=1,
    average='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.precision_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _precision_score_impl
        else:

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'precision', average=average)
            return _precision_score_impl
    elif is_overload_false(_is_data_distributed):

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.precision_score(y_true, y_pred,
                    labels=labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _precision_score_impl
    else:

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'precision', average=average)
            return score[0]
        return _precision_score_impl


@overload(sklearn.metrics.recall_score, no_unliteral=True)
def overload_recall_score(y_true, y_pred, labels=None, pos_label=1, average
    ='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.recall_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _recall_score_impl
        else:

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'recall', average=average)
            return _recall_score_impl
    elif is_overload_false(_is_data_distributed):

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.recall_score(y_true, y_pred, labels
                    =labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _recall_score_impl
    else:

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'recall', average=average)
            return score[0]
        return _recall_score_impl


@overload(sklearn.metrics.f1_score, no_unliteral=True)
def overload_f1_score(y_true, y_pred, labels=None, pos_label=1, average=
    'binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.f1_score(y_true, y_pred, labels
                        =labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _f1_score_impl
        else:

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'f1', average=average)
            return _f1_score_impl
    elif is_overload_false(_is_data_distributed):

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.f1_score(y_true, y_pred, labels=
                    labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _f1_score_impl
    else:

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred, 'f1',
                average=average)
            return score[0]
        return _f1_score_impl


def mse_mae_dist_helper(y_true, y_pred, sample_weight, multioutput, squared,
    metric):
    if metric == 'mse':
        mvfxt__tbebm = sklearn.metrics.mean_squared_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values', squared=True
            )
    elif metric == 'mae':
        mvfxt__tbebm = sklearn.metrics.mean_absolute_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values')
    else:
        raise RuntimeError(
            f"Unrecognized metric {metric}. Must be one of 'mae' and 'mse'")
    dmbdm__fdzd = MPI.COMM_WORLD
    yohh__jjf = dmbdm__fdzd.Get_size()
    if sample_weight is not None:
        dbkea__qfpf = np.sum(sample_weight)
    else:
        dbkea__qfpf = np.float64(y_true.shape[0])
    zbfkv__zccz = np.zeros(yohh__jjf, dtype=type(dbkea__qfpf))
    dmbdm__fdzd.Allgather(dbkea__qfpf, zbfkv__zccz)
    unj__ffmk = np.zeros((yohh__jjf, *mvfxt__tbebm.shape), dtype=
        mvfxt__tbebm.dtype)
    dmbdm__fdzd.Allgather(mvfxt__tbebm, unj__ffmk)
    cogz__zwtof = np.average(unj__ffmk, weights=zbfkv__zccz, axis=0)
    if metric == 'mse' and not squared:
        cogz__zwtof = np.sqrt(cogz__zwtof)
    if isinstance(multioutput, str) and multioutput == 'raw_values':
        return cogz__zwtof
    elif isinstance(multioutput, str) and multioutput == 'uniform_average':
        return np.average(cogz__zwtof)
    else:
        return np.average(cogz__zwtof, weights=multioutput)


@overload(sklearn.metrics.mean_squared_error, no_unliteral=True)
def overload_mean_squared_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', squared=True, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
        else:

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
    elif is_overload_none(sample_weight):

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl
    else:

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl


@overload(sklearn.metrics.mean_absolute_error, no_unliteral=True)
def overload_mean_absolute_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
        else:

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
    elif is_overload_none(sample_weight):

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl
    else:

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl


def log_loss_dist_helper(y_true, y_pred, eps, normalize, sample_weight, labels
    ):
    loss = sklearn.metrics.log_loss(y_true, y_pred, eps=eps, normalize=
        False, sample_weight=sample_weight, labels=labels)
    dmbdm__fdzd = MPI.COMM_WORLD
    loss = dmbdm__fdzd.allreduce(loss, op=MPI.SUM)
    if normalize:
        rdwn__ffppw = np.sum(sample_weight
            ) if sample_weight is not None else len(y_true)
        rdwn__ffppw = dmbdm__fdzd.allreduce(rdwn__ffppw, op=MPI.SUM)
        loss = loss / rdwn__ffppw
    return loss


@overload(sklearn.metrics.log_loss, no_unliteral=True)
def overload_log_loss(y_true, y_pred, eps=1e-15, normalize=True,
    sample_weight=None, labels=None, _is_data_distributed=False):
    check_sklearn_version()
    sbj__nfv = 'def _log_loss_impl(\n'
    sbj__nfv += '    y_true,\n'
    sbj__nfv += '    y_pred,\n'
    sbj__nfv += '    eps=1e-15,\n'
    sbj__nfv += '    normalize=True,\n'
    sbj__nfv += '    sample_weight=None,\n'
    sbj__nfv += '    labels=None,\n'
    sbj__nfv += '    _is_data_distributed=False,\n'
    sbj__nfv += '):\n'
    sbj__nfv += '    y_true = bodo.utils.conversion.coerce_to_array(y_true)\n'
    sbj__nfv += '    y_pred = bodo.utils.conversion.coerce_to_array(y_pred)\n'
    if not is_overload_none(sample_weight):
        sbj__nfv += (
            '    sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight)\n'
            )
    if not is_overload_none(labels):
        sbj__nfv += (
            '    labels = bodo.utils.conversion.coerce_to_array(labels)\n')
    if is_overload_true(_is_data_distributed) and is_overload_none(labels):
        sbj__nfv += (
            '    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)\n'
            )
        sbj__nfv += '    labels = bodo.allgatherv(labels, False)\n'
    sbj__nfv += "    with numba.objmode(loss='float64'):\n"
    if is_overload_false(_is_data_distributed):
        sbj__nfv += '        loss = sklearn.metrics.log_loss(\n'
    else:
        sbj__nfv += '        loss = log_loss_dist_helper(\n'
    sbj__nfv += '            y_true, y_pred, eps=eps, normalize=normalize,\n'
    sbj__nfv += '            sample_weight=sample_weight, labels=labels\n'
    sbj__nfv += '        )\n'
    sbj__nfv += '        return loss\n'
    vsdj__wqc = {}
    exec(sbj__nfv, globals(), vsdj__wqc)
    vlclp__xgooh = vsdj__wqc['_log_loss_impl']
    return vlclp__xgooh


@overload(sklearn.metrics.pairwise.cosine_similarity, no_unliteral=True)
def overload_metrics_cosine_similarity(X, Y=None, dense_output=True,
    _is_Y_distributed=False, _is_X_distributed=False):
    check_sklearn_version()
    goy__fyi = {'dense_output': dense_output}
    swcl__syzb = {'dense_output': True}
    check_unsupported_args('cosine_similarity', goy__fyi, swcl__syzb, 'ml')
    if is_overload_false(_is_X_distributed):
        lyn__isi = (
            f'metrics_cosine_similarity_type_{numba.core.ir_utils.next_label()}'
            )
        setattr(types, lyn__isi, X)
        sbj__nfv = 'def _metrics_cosine_similarity_impl(\n'
        sbj__nfv += """    X, Y=None, dense_output=True, _is_Y_distributed=False, _is_X_distributed=False
"""
        sbj__nfv += '):\n'
        if not is_overload_none(Y) and is_overload_true(_is_Y_distributed):
            sbj__nfv += '    Y = bodo.allgatherv(Y)\n'
        sbj__nfv += "    with numba.objmode(out='float64[:,::1]'):\n"
        sbj__nfv += (
            '        out = sklearn.metrics.pairwise.cosine_similarity(\n')
        sbj__nfv += '            X, Y, dense_output=dense_output\n'
        sbj__nfv += '        )\n'
        sbj__nfv += '    return out\n'
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        _metrics_cosine_similarity_impl = vsdj__wqc[
            '_metrics_cosine_similarity_impl']
    elif is_overload_none(Y):

        def _metrics_cosine_similarity_impl(X, Y=None, dense_output=True,
            _is_Y_distributed=False, _is_X_distributed=False):
            skua__yonu = np.sqrt((X * X).sum(axis=1)).reshape(-1, 1)
            dgb__vny = X / skua__yonu
            tvvzl__hov = bodo.allgatherv(dgb__vny).T
            akq__eijhw = np.dot(dgb__vny, tvvzl__hov)
            return akq__eijhw
    else:
        sbj__nfv = 'def _metrics_cosine_similarity_impl(\n'
        sbj__nfv += """    X, Y=None, dense_output=True, _is_Y_distributed=False, _is_X_distributed=False
"""
        sbj__nfv += '):\n'
        sbj__nfv += (
            '    X_norms = np.sqrt((X * X).sum(axis=1)).reshape(-1, 1)\n')
        sbj__nfv += '    X_normalized = X / X_norms\n'
        sbj__nfv += (
            '    Y_norms = np.sqrt((Y * Y).sum(axis=1)).reshape(-1, 1)\n')
        sbj__nfv += '    Y_normalized = Y / Y_norms\n'
        if is_overload_true(_is_Y_distributed):
            sbj__nfv += '    Y_normalized = bodo.allgatherv(Y_normalized)\n'
        sbj__nfv += '    Y_normalized_T = Y_normalized.T\n'
        sbj__nfv += (
            '    kernel_matrix = np.dot(X_normalized, Y_normalized_T)\n')
        sbj__nfv += '    return kernel_matrix\n'
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        _metrics_cosine_similarity_impl = vsdj__wqc[
            '_metrics_cosine_similarity_impl']
    return _metrics_cosine_similarity_impl


def accuracy_score_dist_helper(y_true, y_pred, normalize, sample_weight):
    score = sklearn.metrics.accuracy_score(y_true, y_pred, normalize=False,
        sample_weight=sample_weight)
    dmbdm__fdzd = MPI.COMM_WORLD
    score = dmbdm__fdzd.allreduce(score, op=MPI.SUM)
    if normalize:
        rdwn__ffppw = np.sum(sample_weight
            ) if sample_weight is not None else len(y_true)
        rdwn__ffppw = dmbdm__fdzd.allreduce(rdwn__ffppw, op=MPI.SUM)
        score = score / rdwn__ffppw
    return score


@overload(sklearn.metrics.accuracy_score, no_unliteral=True)
def overload_accuracy_score(y_true, y_pred, normalize=True, sample_weight=
    None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_false(_is_data_distributed):
        if is_overload_none(sample_weight):

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
        else:

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
    elif is_overload_none(sample_weight):

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl
    else:

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl


def check_consistent_length_parallel(*arrays):
    dmbdm__fdzd = MPI.COMM_WORLD
    prt__pihaq = True
    brmga__kyxb = [len(ewnvk__cblc) for ewnvk__cblc in arrays if 
        ewnvk__cblc is not None]
    if len(np.unique(brmga__kyxb)) > 1:
        prt__pihaq = False
    prt__pihaq = dmbdm__fdzd.allreduce(prt__pihaq, op=MPI.LAND)
    return prt__pihaq


def r2_score_dist_helper(y_true, y_pred, sample_weight, multioutput):
    dmbdm__fdzd = MPI.COMM_WORLD
    if y_true.ndim == 1:
        y_true = y_true.reshape((-1, 1))
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape((-1, 1))
    if not check_consistent_length_parallel(y_true, y_pred, sample_weight):
        raise ValueError(
            'y_true, y_pred and sample_weight (if not None) have inconsistent number of samples'
            )
    coywi__uwaz = y_true.shape[0]
    rjg__bvv = dmbdm__fdzd.allreduce(coywi__uwaz, op=MPI.SUM)
    if rjg__bvv < 2:
        warnings.warn(
            'R^2 score is not well-defined with less than two samples.',
            UndefinedMetricWarning)
        return np.array([float('nan')])
    if sample_weight is not None:
        sample_weight = column_or_1d(sample_weight)
        uhtk__loz = sample_weight[:, np.newaxis]
    else:
        sample_weight = np.float64(y_true.shape[0])
        uhtk__loz = 1.0
    fpozz__pjld = (uhtk__loz * (y_true - y_pred) ** 2).sum(axis=0, dtype=np
        .float64)
    qlny__xksab = np.zeros(fpozz__pjld.shape, dtype=fpozz__pjld.dtype)
    dmbdm__fdzd.Allreduce(fpozz__pjld, qlny__xksab, op=MPI.SUM)
    fskm__qzwp = np.nansum(y_true * uhtk__loz, axis=0, dtype=np.float64)
    axxv__ktf = np.zeros_like(fskm__qzwp)
    dmbdm__fdzd.Allreduce(fskm__qzwp, axxv__ktf, op=MPI.SUM)
    gto__ing = np.nansum(sample_weight, dtype=np.float64)
    dirm__mqf = dmbdm__fdzd.allreduce(gto__ing, op=MPI.SUM)
    nknr__vhrg = axxv__ktf / dirm__mqf
    qzo__idyvh = (uhtk__loz * (y_true - nknr__vhrg) ** 2).sum(axis=0, dtype
        =np.float64)
    zqoj__fet = np.zeros(qzo__idyvh.shape, dtype=qzo__idyvh.dtype)
    dmbdm__fdzd.Allreduce(qzo__idyvh, zqoj__fet, op=MPI.SUM)
    ijuo__ylw = zqoj__fet != 0
    czw__ktdq = qlny__xksab != 0
    yph__iiviw = ijuo__ylw & czw__ktdq
    yywnf__ndsat = np.ones([y_true.shape[1] if len(y_true.shape) > 1 else 1])
    yywnf__ndsat[yph__iiviw] = 1 - qlny__xksab[yph__iiviw] / zqoj__fet[
        yph__iiviw]
    yywnf__ndsat[czw__ktdq & ~ijuo__ylw] = 0.0
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            return yywnf__ndsat
        elif multioutput == 'uniform_average':
            sjpsy__dapla = None
        elif multioutput == 'variance_weighted':
            sjpsy__dapla = zqoj__fet
            if not np.any(ijuo__ylw):
                if not np.any(czw__ktdq):
                    return np.array([1.0])
                else:
                    return np.array([0.0])
    else:
        sjpsy__dapla = multioutput
    return np.array([np.average(yywnf__ndsat, weights=sjpsy__dapla)])


@overload(sklearn.metrics.r2_score, no_unliteral=True)
def overload_r2_score(y_true, y_pred, sample_weight=None, multioutput=
    'uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) not in ['raw_values', 'uniform_average',
        'variance_weighted']:
        raise BodoError(
            f"Unsupported argument {get_overload_const_str(multioutput)} specified for 'multioutput'"
            )
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
        else:

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
    elif is_overload_none(sample_weight):

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl
    else:

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl


def confusion_matrix_dist_helper(y_true, y_pred, labels=None, sample_weight
    =None, normalize=None):
    if normalize not in ['true', 'pred', 'all', None]:
        raise ValueError(
            "normalize must be one of {'true', 'pred', 'all', None}")
    dmbdm__fdzd = MPI.COMM_WORLD
    try:
        jsua__wqppn = sklearn.metrics.confusion_matrix(y_true, y_pred,
            labels=labels, sample_weight=sample_weight, normalize=None)
    except ValueError as qqv__vle:
        jsua__wqppn = qqv__vle
    dgqtr__tsg = isinstance(jsua__wqppn, ValueError
        ) and 'At least one label specified must be in y_true' in jsua__wqppn.args[
        0]
    oldx__rgbrn = dmbdm__fdzd.allreduce(dgqtr__tsg, op=MPI.LAND)
    if oldx__rgbrn:
        raise jsua__wqppn
    elif dgqtr__tsg:
        dtype = np.int64
        if sample_weight is not None and sample_weight.dtype.kind not in {'i',
            'u', 'b'}:
            dtype = np.float64
        ybjeg__air = np.zeros((labels.size, labels.size), dtype=dtype)
    else:
        ybjeg__air = jsua__wqppn
    amkl__ylpl = np.zeros_like(ybjeg__air)
    dmbdm__fdzd.Allreduce(ybjeg__air, amkl__ylpl)
    with np.errstate(all='ignore'):
        if normalize == 'true':
            amkl__ylpl = amkl__ylpl / amkl__ylpl.sum(axis=1, keepdims=True)
        elif normalize == 'pred':
            amkl__ylpl = amkl__ylpl / amkl__ylpl.sum(axis=0, keepdims=True)
        elif normalize == 'all':
            amkl__ylpl = amkl__ylpl / amkl__ylpl.sum()
        amkl__ylpl = np.nan_to_num(amkl__ylpl)
    return amkl__ylpl


@overload(sklearn.metrics.confusion_matrix, no_unliteral=True)
def overload_confusion_matrix(y_true, y_pred, labels=None, sample_weight=
    None, normalize=None, _is_data_distributed=False):
    check_sklearn_version()
    sbj__nfv = 'def _confusion_matrix_impl(\n'
    sbj__nfv += '    y_true, y_pred, labels=None,\n'
    sbj__nfv += '    sample_weight=None, normalize=None,\n'
    sbj__nfv += '    _is_data_distributed=False,\n'
    sbj__nfv += '):\n'
    sbj__nfv += '    y_true = bodo.utils.conversion.coerce_to_array(y_true)\n'
    sbj__nfv += '    y_pred = bodo.utils.conversion.coerce_to_array(y_pred)\n'
    sbj__nfv += '    y_true = bodo.utils.typing.decode_if_dict_array(y_true)\n'
    sbj__nfv += '    y_pred = bodo.utils.typing.decode_if_dict_array(y_pred)\n'
    weg__oiiay = 'int64[:,:]', 'np.int64'
    if not is_overload_none(normalize):
        weg__oiiay = 'float64[:,:]', 'np.float64'
    if not is_overload_none(sample_weight):
        sbj__nfv += (
            '    sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight)\n'
            )
        if numba.np.numpy_support.as_dtype(sample_weight.dtype).kind not in {
            'i', 'u', 'b'}:
            weg__oiiay = 'float64[:,:]', 'np.float64'
    if not is_overload_none(labels):
        sbj__nfv += (
            '    labels = bodo.utils.conversion.coerce_to_array(labels)\n')
    elif is_overload_true(_is_data_distributed):
        sbj__nfv += (
            '    labels = bodo.libs.array_kernels.concat([y_true, y_pred])\n')
        sbj__nfv += (
            '    labels = bodo.libs.array_kernels.unique(labels, parallel=True)\n'
            )
        sbj__nfv += '    labels = bodo.allgatherv(labels, False)\n'
        sbj__nfv += """    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False)
"""
    sbj__nfv += f"    with numba.objmode(cm='{weg__oiiay[0]}'):\n"
    if is_overload_false(_is_data_distributed):
        sbj__nfv += '      cm = sklearn.metrics.confusion_matrix(\n'
    else:
        sbj__nfv += '      cm = confusion_matrix_dist_helper(\n'
    sbj__nfv += '        y_true, y_pred, labels=labels,\n'
    sbj__nfv += '        sample_weight=sample_weight, normalize=normalize,\n'
    sbj__nfv += f'      ).astype({weg__oiiay[1]})\n'
    sbj__nfv += '    return cm\n'
    vsdj__wqc = {}
    exec(sbj__nfv, globals(), vsdj__wqc)
    sklgs__zkps = vsdj__wqc['_confusion_matrix_impl']
    return sklgs__zkps


BodoSGDRegressorType = install_py_obj_class(types_name='sgd_regressor_type',
    python_type=sklearn.linear_model.SGDRegressor, module=this_module,
    class_name='BodoSGDRegressorType', model_name='BodoSGDRegressorModel')


@overload(sklearn.linear_model.SGDRegressor, no_unliteral=True)
def sklearn_linear_model_SGDRegressor_overload(loss='squared_error',
    penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter
    =1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1, random_state=
    None, learning_rate='invscaling', eta0=0.01, power_t=0.25,
    early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDRegressor_impl(loss='squared_error',
        penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True,
        max_iter=1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1,
        random_state=None, learning_rate='invscaling', eta0=0.01, power_t=
        0.25, early_stopping=False, validation_fraction=0.1,
        n_iter_no_change=5, warm_start=False, average=False):
        with numba.objmode(m='sgd_regressor_type'):
            m = sklearn.linear_model.SGDRegressor(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, random_state=random_state,
                learning_rate=learning_rate, eta0=eta0, power_t=power_t,
                early_stopping=early_stopping, validation_fraction=
                validation_fraction, n_iter_no_change=n_iter_no_change,
                warm_start=warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDRegressor_impl


@overload_method(BodoSGDRegressorType, 'fit', no_unliteral=True)
def overload_sgdr_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = fit_sgd(m, X, y, _is_data_distributed)
            bodo.barrier()
            return m
        return _model_sgdr_fit_impl
    else:

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdr_fit_impl


@overload_method(BodoSGDRegressorType, 'predict', no_unliteral=True)
def overload_sgdr_model_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoSGDRegressorType, 'score', no_unliteral=True)
def overload_sgdr_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoSGDClassifierType = install_py_obj_class(types_name=
    'sgd_classifier_type', python_type=sklearn.linear_model.SGDClassifier,
    module=this_module, class_name='BodoSGDClassifierType', model_name=
    'BodoSGDClassifierModel')


@overload(sklearn.linear_model.SGDClassifier, no_unliteral=True)
def sklearn_linear_model_SGDClassifier_overload(loss='hinge', penalty='l2',
    alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol=
    0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None, random_state=
    None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=
    False, validation_fraction=0.1, n_iter_no_change=5, class_weight=None,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDClassifier_impl(loss='hinge', penalty='l2',
        alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol
        =0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None,
        random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5,
        early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
        class_weight=None, warm_start=False, average=False):
        with numba.objmode(m='sgd_classifier_type'):
            m = sklearn.linear_model.SGDClassifier(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, n_jobs=n_jobs,
                random_state=random_state, learning_rate=learning_rate,
                eta0=eta0, power_t=power_t, early_stopping=early_stopping,
                validation_fraction=validation_fraction, n_iter_no_change=
                n_iter_no_change, class_weight=class_weight, warm_start=
                warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDClassifier_impl


def fit_sgd(m, X, y, y_classes=None, _is_data_distributed=False):
    dmbdm__fdzd = MPI.COMM_WORLD
    rlyb__lpg = dmbdm__fdzd.allreduce(len(X), op=MPI.SUM)
    stiw__bhs = len(X) / rlyb__lpg
    jnacm__uaqjm = dmbdm__fdzd.Get_size()
    m.n_jobs = 1
    m.early_stopping = False
    lfpy__zanbv = np.inf
    qcsv__ydlog = 0
    if m.loss == 'hinge':
        zmaz__twmsh = hinge_loss
    elif m.loss == 'log':
        zmaz__twmsh = log_loss
    elif m.loss == 'squared_error':
        zmaz__twmsh = mean_squared_error
    else:
        raise ValueError('loss {} not supported'.format(m.loss))
    rif__uuk = False
    if isinstance(m, sklearn.linear_model.SGDRegressor):
        rif__uuk = True
    for eoq__lvzxl in range(m.max_iter):
        if rif__uuk:
            m.partial_fit(X, y)
        else:
            m.partial_fit(X, y, classes=y_classes)
        m.coef_ = m.coef_ * stiw__bhs
        m.coef_ = dmbdm__fdzd.allreduce(m.coef_, op=MPI.SUM)
        m.intercept_ = m.intercept_ * stiw__bhs
        m.intercept_ = dmbdm__fdzd.allreduce(m.intercept_, op=MPI.SUM)
        if rif__uuk:
            y_pred = m.predict(X)
            vwpkx__waz = zmaz__twmsh(y, y_pred)
        else:
            y_pred = m.decision_function(X)
            vwpkx__waz = zmaz__twmsh(y, y_pred, labels=y_classes)
        rzj__plgrn = dmbdm__fdzd.allreduce(vwpkx__waz, op=MPI.SUM)
        vwpkx__waz = rzj__plgrn / jnacm__uaqjm
        if m.tol > np.NINF and vwpkx__waz > lfpy__zanbv - m.tol * rlyb__lpg:
            qcsv__ydlog += 1
        else:
            qcsv__ydlog = 0
        if vwpkx__waz < lfpy__zanbv:
            lfpy__zanbv = vwpkx__waz
        if qcsv__ydlog >= m.n_iter_no_change:
            break
    return m


@overload_method(BodoSGDClassifierType, 'fit', no_unliteral=True)
def overload_sgdc_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    """
    Provide implementations for the fit function.
    In case input is replicated, we simply call sklearn,
    else we use partial_fit on each rank then use we re-compute the attributes using MPI operations.
    """
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            with numba.objmode(m='sgd_classifier_type'):
                m = fit_sgd(m, X, y, y_classes, _is_data_distributed)
            return m
        return _model_sgdc_fit_impl
    else:

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_classifier_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdc_fit_impl


@overload_method(BodoSGDClassifierType, 'predict', no_unliteral=True)
def overload_sgdc_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoSGDClassifierType, 'predict_proba', no_unliteral=True)
def overload_sgdc_model_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoSGDClassifierType, 'predict_log_proba', no_unliteral=True)
def overload_sgdc_model_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoSGDClassifierType, 'score', no_unliteral=True)
def overload_sgdc_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoSGDClassifierType, 'coef_')
def get_sgdc_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


BodoKMeansClusteringType = install_py_obj_class(types_name=
    'kmeans_clustering_type', python_type=sklearn.cluster.KMeans, module=
    this_module, class_name='BodoKMeansClusteringType', model_name=
    'BodoKMeansClusteringModel')


@overload(sklearn.cluster.KMeans, no_unliteral=True)
def sklearn_cluster_kmeans_overload(n_clusters=8, init='k-means++', n_init=
    10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True,
    algorithm='auto'):
    check_sklearn_version()

    def _sklearn_cluster_kmeans_impl(n_clusters=8, init='k-means++', n_init
        =10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x
        =True, algorithm='auto'):
        with numba.objmode(m='kmeans_clustering_type'):
            m = sklearn.cluster.KMeans(n_clusters=n_clusters, init=init,
                n_init=n_init, max_iter=max_iter, tol=tol, verbose=verbose,
                random_state=random_state, copy_x=copy_x, algorithm=algorithm)
        return m
    return _sklearn_cluster_kmeans_impl


def kmeans_fit_helper(m, len_X, all_X, all_sample_weight, _is_data_distributed
    ):
    dmbdm__fdzd = MPI.COMM_WORLD
    tkl__xpe = dmbdm__fdzd.Get_rank()
    cocn__hdd = MPI.Get_processor_name()
    ipzzs__gxe = get_host_ranks()
    dalti__xzj = m.n_jobs if hasattr(m, 'n_jobs') else None
    tlnkg__yrb = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = len(ipzzs__gxe[cocn__hdd])
    if tkl__xpe == 0:
        m.fit(X=all_X, y=None, sample_weight=all_sample_weight)
    if tkl__xpe == 0:
        dmbdm__fdzd.bcast(m.cluster_centers_)
        dmbdm__fdzd.bcast(m.inertia_)
        dmbdm__fdzd.bcast(m.n_iter_)
    else:
        m.cluster_centers_ = dmbdm__fdzd.bcast(None)
        m.inertia_ = dmbdm__fdzd.bcast(None)
        m.n_iter_ = dmbdm__fdzd.bcast(None)
    if _is_data_distributed:
        oiq__dege = dmbdm__fdzd.allgather(len_X)
        if tkl__xpe == 0:
            hrmz__ckbnw = np.empty(len(oiq__dege) + 1, dtype=int)
            np.cumsum(oiq__dege, out=hrmz__ckbnw[1:])
            hrmz__ckbnw[0] = 0
            wgysi__kynwl = [m.labels_[hrmz__ckbnw[dzxt__uhjfo]:hrmz__ckbnw[
                dzxt__uhjfo + 1]] for dzxt__uhjfo in range(len(oiq__dege))]
            vydx__nzcav = dmbdm__fdzd.scatter(wgysi__kynwl)
        else:
            vydx__nzcav = dmbdm__fdzd.scatter(None)
        m.labels_ = vydx__nzcav
    elif tkl__xpe == 0:
        dmbdm__fdzd.bcast(m.labels_)
    else:
        m.labels_ = dmbdm__fdzd.bcast(None)
    m._n_threads = tlnkg__yrb
    return m


@overload_method(BodoKMeansClusteringType, 'fit', no_unliteral=True)
def overload_kmeans_clustering_fit(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_fit_impl(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        if _is_data_distributed:
            all_X = bodo.gatherv(X)
            if sample_weight is not None:
                all_sample_weight = bodo.gatherv(sample_weight)
            else:
                all_sample_weight = None
        else:
            all_X = X
            all_sample_weight = sample_weight
        with numba.objmode(m='kmeans_clustering_type'):
            m = kmeans_fit_helper(m, len(X), all_X, all_sample_weight,
                _is_data_distributed)
        return m
    return _cluster_kmeans_fit_impl


def kmeans_predict_helper(m, X, sample_weight):
    tlnkg__yrb = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = 1
    if len(X) == 0:
        preds = np.empty(0, dtype=np.int64)
    else:
        preds = m.predict(X, sample_weight).astype(np.int64).flatten()
    m._n_threads = tlnkg__yrb
    return preds


@overload_method(BodoKMeansClusteringType, 'predict', no_unliteral=True)
def overload_kmeans_clustering_predict(m, X, sample_weight=None):

    def _cluster_kmeans_predict(m, X, sample_weight=None):
        with numba.objmode(preds='int64[:]'):
            preds = kmeans_predict_helper(m, X, sample_weight)
        return preds
    return _cluster_kmeans_predict


@overload_method(BodoKMeansClusteringType, 'score', no_unliteral=True)
def overload_kmeans_clustering_score(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_score(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        with numba.objmode(result='float64'):
            tlnkg__yrb = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                result = 0
            else:
                result = m.score(X, y=y, sample_weight=sample_weight)
            if _is_data_distributed:
                dmbdm__fdzd = MPI.COMM_WORLD
                result = dmbdm__fdzd.allreduce(result, op=MPI.SUM)
            m._n_threads = tlnkg__yrb
        return result
    return _cluster_kmeans_score


@overload_method(BodoKMeansClusteringType, 'transform', no_unliteral=True)
def overload_kmeans_clustering_transform(m, X):

    def _cluster_kmeans_transform(m, X):
        with numba.objmode(X_new='float64[:,:]'):
            tlnkg__yrb = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                X_new = np.empty((0, m.n_clusters), dtype=np.int64)
            else:
                X_new = m.transform(X).astype(np.float64)
            m._n_threads = tlnkg__yrb
        return X_new
    return _cluster_kmeans_transform


BodoMultinomialNBType = install_py_obj_class(types_name=
    'multinomial_nb_type', python_type=sklearn.naive_bayes.MultinomialNB,
    module=this_module, class_name='BodoMultinomialNBType', model_name=
    'BodoMultinomialNBModel')


@overload(sklearn.naive_bayes.MultinomialNB, no_unliteral=True)
def sklearn_naive_bayes_multinomialnb_overload(alpha=1.0, fit_prior=True,
    class_prior=None):
    check_sklearn_version()

    def _sklearn_naive_bayes_multinomialnb_impl(alpha=1.0, fit_prior=True,
        class_prior=None):
        with numba.objmode(m='multinomial_nb_type'):
            m = sklearn.naive_bayes.MultinomialNB(alpha=alpha, fit_prior=
                fit_prior, class_prior=class_prior)
        return m
    return _sklearn_naive_bayes_multinomialnb_impl


@overload_method(BodoMultinomialNBType, 'fit', no_unliteral=True)
def overload_multinomial_nb_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _naive_bayes_multinomial_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _naive_bayes_multinomial_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.naive_bayes.MultinomialNB.fit() : 'sample_weight' not supported."
                )
        sbj__nfv = 'def _model_multinomial_nb_fit_impl(\n'
        sbj__nfv += (
            '    m, X, y, sample_weight=None, _is_data_distributed=False\n')
        sbj__nfv += '):  # pragma: no cover\n'
        sbj__nfv += '    y = bodo.utils.conversion.coerce_to_ndarray(y)\n'
        if isinstance(X, DataFrameType):
            sbj__nfv += '    X = X.to_numpy()\n'
        else:
            sbj__nfv += '    X = bodo.utils.conversion.coerce_to_ndarray(X)\n'
        sbj__nfv += '    my_rank = bodo.get_rank()\n'
        sbj__nfv += '    nranks = bodo.get_size()\n'
        sbj__nfv += '    total_cols = X.shape[1]\n'
        sbj__nfv += '    for i in range(nranks):\n'
        sbj__nfv += (
            '        start = bodo.libs.distributed_api.get_start(total_cols, nranks, i)\n'
            )
        sbj__nfv += (
            '        end = bodo.libs.distributed_api.get_end(total_cols, nranks, i)\n'
            )
        sbj__nfv += '        if i == my_rank:\n'
        sbj__nfv += (
            '            X_train = bodo.gatherv(X[:, start:end:1], root=i)\n')
        sbj__nfv += '        else:\n'
        sbj__nfv += '            bodo.gatherv(X[:, start:end:1], root=i)\n'
        sbj__nfv += '    y_train = bodo.allgatherv(y, False)\n'
        sbj__nfv += '    with numba.objmode(m="multinomial_nb_type"):\n'
        sbj__nfv += '        m = fit_multinomial_nb(\n'
        sbj__nfv += """            m, X_train, y_train, sample_weight, total_cols, _is_data_distributed
"""
        sbj__nfv += '        )\n'
        sbj__nfv += '    bodo.barrier()\n'
        sbj__nfv += '    return m\n'
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        bufhg__jzdvf = vsdj__wqc['_model_multinomial_nb_fit_impl']
        return bufhg__jzdvf


def fit_multinomial_nb(m, X_train, y_train, sample_weight=None, total_cols=
    0, _is_data_distributed=False):
    m._check_X_y(X_train, y_train)
    eoq__lvzxl, n_features = X_train.shape
    m.n_features_in_ = n_features
    wkjld__hpgs = LabelBinarizer()
    Y = wkjld__hpgs.fit_transform(y_train)
    m.classes_ = wkjld__hpgs.classes_
    if Y.shape[1] == 1:
        Y = np.concatenate((1 - Y, Y), axis=1)
    if sample_weight is not None:
        Y = Y.astype(np.float64, copy=False)
        sample_weight = _check_sample_weight(sample_weight, X_train)
        sample_weight = np.atleast_2d(sample_weight)
        Y *= sample_weight.T
    class_prior = m.class_prior
    xgzr__zwthg = Y.shape[1]
    m._init_counters(xgzr__zwthg, n_features)
    m._count(X_train.astype('float64'), Y)
    alpha = m._check_alpha()
    m._update_class_log_prior(class_prior=class_prior)
    kdw__abt = m.feature_count_ + alpha
    btghf__frt = kdw__abt.sum(axis=1)
    dmbdm__fdzd = MPI.COMM_WORLD
    jnacm__uaqjm = dmbdm__fdzd.Get_size()
    yswv__jgeo = np.zeros(xgzr__zwthg)
    dmbdm__fdzd.Allreduce(btghf__frt, yswv__jgeo, op=MPI.SUM)
    zjxy__kta = np.log(kdw__abt) - np.log(yswv__jgeo.reshape(-1, 1))
    alz__fevf = zjxy__kta.T.reshape(n_features * xgzr__zwthg)
    zhf__ovwi = np.ones(jnacm__uaqjm) * (total_cols // jnacm__uaqjm)
    mcuw__wia = total_cols % jnacm__uaqjm
    for ibtd__rdb in range(mcuw__wia):
        zhf__ovwi[ibtd__rdb] += 1
    zhf__ovwi *= xgzr__zwthg
    kdf__xksq = np.zeros(jnacm__uaqjm, dtype=np.int32)
    kdf__xksq[1:] = np.cumsum(zhf__ovwi)[:-1]
    jkm__grl = np.zeros((total_cols, xgzr__zwthg), dtype=np.float64)
    dmbdm__fdzd.Allgatherv(alz__fevf, [jkm__grl, zhf__ovwi, kdf__xksq, MPI.
        DOUBLE_PRECISION])
    m.feature_log_prob_ = jkm__grl.T
    m.n_features_in_ = m.feature_log_prob_.shape[1]
    return m


@overload_method(BodoMultinomialNBType, 'predict', no_unliteral=True)
def overload_multinomial_nb_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoMultinomialNBType, 'score', no_unliteral=True)
def overload_multinomial_nb_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoLogisticRegressionType = install_py_obj_class(types_name=
    'logistic_regression_type', python_type=sklearn.linear_model.
    LogisticRegression, module=this_module, class_name=
    'BodoLogisticRegressionType', model_name='BodoLogisticRegressionModel')


@overload(sklearn.linear_model.LogisticRegression, no_unliteral=True)
def sklearn_linear_model_logistic_regression_overload(penalty='l2', dual=
    False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
    class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
    multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None
    ):
    check_sklearn_version()

    def _sklearn_linear_model_logistic_regression_impl(penalty='l2', dual=
        False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
        class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
        multi_class='auto', verbose=0, warm_start=False, n_jobs=None,
        l1_ratio=None):
        with numba.objmode(m='logistic_regression_type'):
            m = sklearn.linear_model.LogisticRegression(penalty=penalty,
                dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                intercept_scaling=intercept_scaling, class_weight=
                class_weight, random_state=random_state, solver=solver,
                max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
        return m
    return _sklearn_linear_model_logistic_regression_impl


@register_jitable
def _raise_SGD_warning(sgd_name):
    with numba.objmode:
        warnings.warn(
            f'Data is distributed so Bodo will fit model with SGD solver optimization ({sgd_name})'
            , BodoWarning)


@overload_method(BodoLogisticRegressionType, 'fit', no_unliteral=True)
def overload_logistic_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _logistic_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LogisticRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                if m.l1_ratio is None:
                    l1_ratio = 0.15
                else:
                    l1_ratio = m.l1_ratio
                clf = sklearn.linear_model.SGDClassifier(loss='log',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose, warm_start=m.warm_start, n_jobs=m.
                    n_jobs, l1_ratio=l1_ratio)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _sgdc_logistic_regression_fit_impl


@overload_method(BodoLogisticRegressionType, 'predict', no_unliteral=True)
def overload_logistic_regression_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_proba', no_unliteral=True
    )
def overload_logistic_regression_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_log_proba',
    no_unliteral=True)
def overload_logistic_regression_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'score', no_unliteral=True)
def overload_logistic_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLogisticRegressionType, 'coef_')
def get_logisticR_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


BodoLinearRegressionType = install_py_obj_class(types_name=
    'linear_regression_type', python_type=sklearn.linear_model.
    LinearRegression, module=this_module, class_name=
    'BodoLinearRegressionType', model_name='BodoLinearRegressionModel')


@overload(sklearn.linear_model.LinearRegression, no_unliteral=True)
def sklearn_linear_model_linear_regression_overload(fit_intercept=True,
    copy_X=True, n_jobs=None, positive=False):
    check_sklearn_version()

    def _sklearn_linear_model_linear_regression_impl(fit_intercept=True,
        copy_X=True, n_jobs=None, positive=False):
        with numba.objmode(m='linear_regression_type'):
            m = sklearn.linear_model.LinearRegression(fit_intercept=
                fit_intercept, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        return m
    return _sklearn_linear_model_linear_regression_impl


@overload_method(BodoLinearRegressionType, 'fit', no_unliteral=True)
def overload_linear_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _linear_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LinearRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty=None, fit_intercept=m.
                    fit_intercept)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
            return m
        return _sgdc_linear_regression_fit_impl


@overload_method(BodoLinearRegressionType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLinearRegressionType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLinearRegressionType, 'coef_')
def get_lr_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


BodoLassoType = install_py_obj_class(types_name='lasso_type', python_type=
    sklearn.linear_model.Lasso, module=this_module, class_name=
    'BodoLassoType', model_name='BodoLassoModel')


@overload(sklearn.linear_model.Lasso, no_unliteral=True)
def sklearn_linear_model_lasso_overload(alpha=1.0, fit_intercept=True,
    precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=
    False, positive=False, random_state=None, selection='cyclic'):
    check_sklearn_version()

    def _sklearn_linear_model_lasso_impl(alpha=1.0, fit_intercept=True,
        precompute=False, copy_X=True, max_iter=1000, tol=0.0001,
        warm_start=False, positive=False, random_state=None, selection='cyclic'
        ):
        with numba.objmode(m='lasso_type'):
            m = sklearn.linear_model.Lasso(alpha=alpha, fit_intercept=
                fit_intercept, precompute=precompute, copy_X=copy_X,
                max_iter=max_iter, tol=tol, warm_start=warm_start, positive
                =positive, random_state=random_state, selection=selection)
        return m
    return _sklearn_linear_model_lasso_impl


@overload_method(BodoLassoType, 'fit', no_unliteral=True)
def overload_lasso_fit(m, X, y, sample_weight=None, check_input=True,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _lasso_fit_impl(m, X, y, sample_weight=None, check_input=True,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight, check_input)
            return m
        return _lasso_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_true(check_input):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'check_input' is not supported for distributed data."
                )

        def _sgdc_lasso_fit_impl(m, X, y, sample_weight=None, check_input=
            True, _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l1', alpha=m.alpha,
                    fit_intercept=m.fit_intercept, max_iter=m.max_iter, tol
                    =m.tol, warm_start=m.warm_start, random_state=m.
                    random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _sgdc_lasso_fit_impl


@overload_method(BodoLassoType, 'predict', no_unliteral=True)
def overload_lass_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLassoType, 'score', no_unliteral=True)
def overload_lasso_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoRidgeType = install_py_obj_class(types_name='ridge_type', python_type=
    sklearn.linear_model.Ridge, module=this_module, class_name=
    'BodoRidgeType', model_name='BodoRidgeModel')


@overload(sklearn.linear_model.Ridge, no_unliteral=True)
def sklearn_linear_model_ridge_overload(alpha=1.0, fit_intercept=True,
    copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=False,
    random_state=None):
    check_sklearn_version()

    def _sklearn_linear_model_ridge_impl(alpha=1.0, fit_intercept=True,
        copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=
        False, random_state=None):
        with numba.objmode(m='ridge_type'):
            m = sklearn.linear_model.Ridge(alpha=alpha, fit_intercept=
                fit_intercept, copy_X=copy_X, max_iter=max_iter, tol=tol,
                solver=solver, positive=positive, random_state=random_state)
        return m
    return _sklearn_linear_model_ridge_impl


@overload_method(BodoRidgeType, 'fit', no_unliteral=True)
def overload_ridge_fit(m, X, y, sample_weight=None, _is_data_distributed=False
    ):
    if is_overload_false(_is_data_distributed):

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _ridge_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Ridge.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                if m.max_iter is None:
                    max_iter = 1000
                else:
                    max_iter = m.max_iter
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l2', alpha=0.001,
                    fit_intercept=m.fit_intercept, max_iter=max_iter, tol=m
                    .tol, random_state=m.random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _ridge_fit_impl


@overload_method(BodoRidgeType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRidgeType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoRidgeType, 'coef_')
def get_ridge_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


BodoLinearSVCType = install_py_obj_class(types_name='linear_svc_type',
    python_type=sklearn.svm.LinearSVC, module=this_module, class_name=
    'BodoLinearSVCType', model_name='BodoLinearSVCModel')


@overload(sklearn.svm.LinearSVC, no_unliteral=True)
def sklearn_svm_linear_svc_overload(penalty='l2', loss='squared_hinge',
    dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
    intercept_scaling=1, class_weight=None, verbose=0, random_state=None,
    max_iter=1000):
    check_sklearn_version()

    def _sklearn_svm_linear_svc_impl(penalty='l2', loss='squared_hinge',
        dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
        intercept_scaling=1, class_weight=None, verbose=0, random_state=
        None, max_iter=1000):
        with numba.objmode(m='linear_svc_type'):
            m = sklearn.svm.LinearSVC(penalty=penalty, loss=loss, dual=dual,
                tol=tol, C=C, multi_class=multi_class, fit_intercept=
                fit_intercept, intercept_scaling=intercept_scaling,
                class_weight=class_weight, verbose=verbose, random_state=
                random_state, max_iter=max_iter)
        return m
    return _sklearn_svm_linear_svc_impl


@overload_method(BodoLinearSVCType, 'fit', no_unliteral=True)
def overload_linear_svc_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _svm_linear_svc_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.svm.LinearSVC.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                clf = sklearn.linear_model.SGDClassifier(loss='hinge',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _svm_linear_svc_fit_impl


@overload_method(BodoLinearSVCType, 'predict', no_unliteral=True)
def overload_svm_linear_svc_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLinearSVCType, 'score', no_unliteral=True)
def overload_svm_linear_svc_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


BodoPreprocessingOneHotEncoderType = install_py_obj_class(types_name=
    'preprocessing_one_hot_encoder_type', python_type=sklearn.preprocessing
    .OneHotEncoder, module=this_module, class_name=
    'BodoPreprocessingOneHotEncoderType', model_name=
    'BodoPreprocessingOneHotEncoderModel')
BodoPreprocessingOneHotEncoderCategoriesType = install_py_obj_class(types_name
    ='preprocessing_one_hot_encoder_categories_type', module=this_module,
    class_name='BodoPreprocessingOneHotEncoderCategoriesType', model_name=
    'BodoPreprocessingOneHotEncoderCategoriesModel')
BodoPreprocessingOneHotEncoderDropIdxType = install_py_obj_class(types_name
    ='preprocessing_one_hot_encoder_drop_idx_type', module=this_module,
    class_name='BodoPreprocessingOneHotEncoderDropIdxType', model_name=
    'BodoPreprocessingOneHotEncoderDropIdxModel')


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'categories_')
def get_one_hot_encoder_categories_(m):

    def impl(m):
        with numba.objmode(result=
            'preprocessing_one_hot_encoder_categories_type'):
            result = m.categories_
        return result
    return impl


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'drop_idx_')
def get_one_hot_encoder_drop_idx_(m):

    def impl(m):
        with numba.objmode(result='preprocessing_one_hot_encoder_drop_idx_type'
            ):
            result = m.drop_idx_
        return result
    return impl


@overload_attribute(BodoPreprocessingOneHotEncoderType, 'n_features_in_')
def get_one_hot_encoder_n_features_in_(m):

    def impl(m):
        with numba.objmode(result='int64'):
            result = m.n_features_in_
        return result
    return impl


@overload(sklearn.preprocessing.OneHotEncoder, no_unliteral=True)
def sklearn_preprocessing_one_hot_encoder_overload(categories='auto', drop=
    None, sparse=True, dtype=np.float64, handle_unknown='error',
    min_frequency=None, max_categories=None):
    check_sklearn_version()
    goy__fyi = {'sparse': sparse, 'dtype': 'float64' if 'float64' in repr(
        dtype) else repr(dtype), 'min_frequency': min_frequency,
        'max_categories': max_categories}
    swcl__syzb = {'sparse': False, 'dtype': 'float64', 'min_frequency':
        None, 'max_categories': None}
    check_unsupported_args('OneHotEncoder', goy__fyi, swcl__syzb, 'ml')

    def _sklearn_preprocessing_one_hot_encoder_impl(categories='auto', drop
        =None, sparse=True, dtype=np.float64, handle_unknown='error',
        min_frequency=None, max_categories=None):
        with numba.objmode(m='preprocessing_one_hot_encoder_type'):
            m = sklearn.preprocessing.OneHotEncoder(categories=categories,
                drop=drop, sparse=sparse, dtype=dtype, handle_unknown=
                handle_unknown, min_frequency=min_frequency, max_categories
                =max_categories)
        return m
    return _sklearn_preprocessing_one_hot_encoder_impl


def sklearn_preprocessing_one_hot_encoder_fit_dist_helper(m, X):
    dmbdm__fdzd = MPI.COMM_WORLD
    try:
        m._validate_keywords()
        yze__kwvpa = m._fit(X, handle_unknown=m.handle_unknown,
            force_all_finite='allow-nan', return_counts=m._infrequent_enabled)
    except ValueError as qqv__vle:
        if 'Found unknown categories' in qqv__vle.args[0]:
            yze__kwvpa = qqv__vle
        else:
            raise qqv__vle
    qith__iamsh = int(isinstance(yze__kwvpa, ValueError))
    fkw__ijxak, zzam__utxm = dmbdm__fdzd.allreduce((qith__iamsh,
        dmbdm__fdzd.Get_rank()), op=MPI.MAXLOC)
    if fkw__ijxak:
        if dmbdm__fdzd.Get_rank() == zzam__utxm:
            nue__hfcmn = yze__kwvpa.args[0]
        else:
            nue__hfcmn = None
        nue__hfcmn = dmbdm__fdzd.bcast(nue__hfcmn, root=zzam__utxm)
        if qith__iamsh:
            raise yze__kwvpa
        else:
            raise ValueError(nue__hfcmn)
    if m.categories == 'auto':
        fjebw__cwd = m.categories_
        esyo__cqhqz = []
        for gmh__lfz in fjebw__cwd:
            dnjg__vpzv = bodo.allgatherv(gmh__lfz)
            pwarh__ckr = _unique(dnjg__vpzv)
            esyo__cqhqz.append(pwarh__ckr)
        m.categories_ = esyo__cqhqz
    if m._infrequent_enabled:
        m._fit_infrequent_category_mapping(yze__kwvpa['n_samples'],
            yze__kwvpa['category_counts'])
    m.drop_idx_ = m._compute_drop_idx()
    m._n_features_outs = m._compute_n_features_outs()
    return m


@overload_method(BodoPreprocessingOneHotEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_one_hot_encoder_fit(m, X, y=None,
    _is_data_distributed=False):
    sbj__nfv = 'def _preprocessing_one_hot_encoder_fit_impl(\n'
    sbj__nfv += '    m, X, y=None, _is_data_distributed=False\n'
    sbj__nfv += '):\n'
    sbj__nfv += (
        "    with numba.objmode(m='preprocessing_one_hot_encoder_type'):\n")
    sbj__nfv += """        if X.ndim == 1 and isinstance(X[0], (np.ndarray, pd.arrays.ArrowStringArray)):
"""
    sbj__nfv += '            X = np.vstack(X)\n'
    if is_overload_true(_is_data_distributed):
        sbj__nfv += (
            '        m = sklearn_preprocessing_one_hot_encoder_fit_dist_helper(m, X)\n'
            )
    else:
        sbj__nfv += '        m = m.fit(X, y)\n'
    sbj__nfv += '    return m\n'
    vsdj__wqc = {}
    exec(sbj__nfv, globals(), vsdj__wqc)
    hsoiq__ejehe = vsdj__wqc['_preprocessing_one_hot_encoder_fit_impl']
    return hsoiq__ejehe


@overload_method(BodoPreprocessingOneHotEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_one_hot_encoder_transform(m, X):

    def _preprocessing_one_hot_encoder_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            if X.ndim == 1 and isinstance(X[0], (np.ndarray, pd.arrays.
                ArrowStringArray)):
                X = np.vstack(X)
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_one_hot_encoder_transform_impl


@overload_method(BodoPreprocessingOneHotEncoderType,
    'get_feature_names_out', no_unliteral=True)
def overload_preprocessing_one_hot_encoder_get_feature_names_out(m,
    input_features=None):

    def _preprocessing_one_hot_encoder_get_feature_names_out_impl(m,
        input_features=None):
        with numba.objmode(out_features='string[:]'):
            out_features = get_feature_names_out(input_features)
        return out_features
    return _preprocessing_one_hot_encoder_get_feature_names_out_impl


BodoPreprocessingStandardScalerType = install_py_obj_class(types_name=
    'preprocessing_standard_scaler_type', python_type=sklearn.preprocessing
    .StandardScaler, module=this_module, class_name=
    'BodoPreprocessingStandardScalerType', model_name=
    'BodoPreprocessingStandardScalerModel')


@overload(sklearn.preprocessing.StandardScaler, no_unliteral=True)
def sklearn_preprocessing_standard_scaler_overload(copy=True, with_mean=
    True, with_std=True):
    check_sklearn_version()

    def _sklearn_preprocessing_standard_scaler_impl(copy=True, with_mean=
        True, with_std=True):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            m = sklearn.preprocessing.StandardScaler(copy=copy, with_mean=
                with_mean, with_std=with_std)
        return m
    return _sklearn_preprocessing_standard_scaler_impl


def sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X):
    dmbdm__fdzd = MPI.COMM_WORLD
    yohh__jjf = dmbdm__fdzd.Get_size()
    jqe__lsqp = m.with_std
    fou__uqa = m.with_mean
    m.with_std = False
    if jqe__lsqp:
        m.with_mean = True
    m = m.fit(X)
    m.with_std = jqe__lsqp
    m.with_mean = fou__uqa
    if not isinstance(m.n_samples_seen_, numbers.Integral):
        husue__zvex = False
    else:
        husue__zvex = True
        m.n_samples_seen_ = np.repeat(m.n_samples_seen_, X.shape[1]).astype(np
            .int64, copy=False)
    jezj__pwn = np.zeros((yohh__jjf, *m.n_samples_seen_.shape), dtype=m.
        n_samples_seen_.dtype)
    dmbdm__fdzd.Allgather(m.n_samples_seen_, jezj__pwn)
    zjryz__tmt = np.sum(jezj__pwn, axis=0)
    m.n_samples_seen_ = zjryz__tmt
    if m.with_mean or m.with_std:
        ytwkx__qxpow = np.zeros((yohh__jjf, *m.mean_.shape), dtype=m.mean_.
            dtype)
        dmbdm__fdzd.Allgather(m.mean_, ytwkx__qxpow)
        ytwkx__qxpow[np.isnan(ytwkx__qxpow)] = 0
        sqfp__qnoka = np.average(ytwkx__qxpow, axis=0, weights=jezj__pwn)
        m.mean_ = sqfp__qnoka
    if m.with_std:
        van__mpbz = sklearn_safe_accumulator_op(np.nansum, (X - sqfp__qnoka
            ) ** 2, axis=0) / zjryz__tmt
        poaqy__yhxwh = np.zeros_like(van__mpbz)
        dmbdm__fdzd.Allreduce(van__mpbz, poaqy__yhxwh, op=MPI.SUM)
        m.var_ = poaqy__yhxwh
        m.scale_ = sklearn_handle_zeros_in_scale(np.sqrt(m.var_))
    husue__zvex = dmbdm__fdzd.allreduce(husue__zvex, op=MPI.LAND)
    if husue__zvex:
        m.n_samples_seen_ = m.n_samples_seen_[0]
    return m


@overload_method(BodoPreprocessingStandardScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_standard_scaler_fit(m, X, y=None, sample_weight=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.preprocessing.StandardScaler.fit(): 'sample_weight' is not supported for distributed data."
                )

        def _preprocessing_standard_scaler_fit_impl(m, X, y=None,
            sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='preprocessing_standard_scaler_type'):
                m = sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X)
            return m
    else:

        def _preprocessing_standard_scaler_fit_impl(m, X, y=None,
            sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='preprocessing_standard_scaler_type'):
                m = m.fit(X, y, sample_weight)
            return m
    return _preprocessing_standard_scaler_fit_impl


@overload_method(BodoPreprocessingStandardScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_transform(m, X, copy=None):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
            with numba.objmode(transformed_X='csr_matrix_float64_int64'):
                transformed_X = m.transform(X, copy=copy)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
    else:

        def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
            with numba.objmode(transformed_X='float64[:,:]'):
                transformed_X = m.transform(X, copy=copy)
            return transformed_X
    return _preprocessing_standard_scaler_transform_impl


@overload_method(BodoPreprocessingStandardScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_inverse_transform(m, X, copy=None):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_standard_scaler_inverse_transform_impl(m, X,
            copy=None):
            with numba.objmode(inverse_transformed_X='csr_matrix_float64_int64'
                ):
                inverse_transformed_X = m.inverse_transform(X, copy=copy)
                inverse_transformed_X.indices = (inverse_transformed_X.
                    indices.astype(np.int64))
                inverse_transformed_X.indptr = (inverse_transformed_X.
                    indptr.astype(np.int64))
            return inverse_transformed_X
    else:

        def _preprocessing_standard_scaler_inverse_transform_impl(m, X,
            copy=None):
            with numba.objmode(inverse_transformed_X='float64[:,:]'):
                inverse_transformed_X = m.inverse_transform(X, copy=copy)
            return inverse_transformed_X
    return _preprocessing_standard_scaler_inverse_transform_impl


BodoPreprocessingMaxAbsScalerType = install_py_obj_class(types_name=
    'preprocessing_max_abs_scaler_type', python_type=sklearn.preprocessing.
    MaxAbsScaler, module=this_module, class_name=
    'BodoPreprocessingMaxAbsScalerType', model_name=
    'BodoPreprocessingMaxAbsScalerModel')


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'scale_')
def get_max_abs_scaler_scale_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.scale_
        return result
    return impl


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'max_abs_')
def get_max_abs_scaler_max_abs_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.max_abs_
        return result
    return impl


@overload_attribute(BodoPreprocessingMaxAbsScalerType, 'n_samples_seen_')
def get_max_abs_scaler_n_samples_seen_(m):

    def impl(m):
        with numba.objmode(result='int64'):
            result = m.n_samples_seen_
        return result
    return impl


@overload(sklearn.preprocessing.MaxAbsScaler, no_unliteral=True)
def sklearn_preprocessing_max_abs_scaler_overload(copy=True):
    check_sklearn_version()

    def _sklearn_preprocessing_max_abs_scaler_impl(copy=True):
        with numba.objmode(m='preprocessing_max_abs_scaler_type'):
            m = sklearn.preprocessing.MaxAbsScaler(copy=copy)
        return m
    return _sklearn_preprocessing_max_abs_scaler_impl


def sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m, X, partial=False):
    dmbdm__fdzd = MPI.COMM_WORLD
    yohh__jjf = dmbdm__fdzd.Get_size()
    if hasattr(m, 'n_samples_seen_'):
        aejnz__phuf = m.n_samples_seen_
    else:
        aejnz__phuf = 0
    if partial:
        m = m.partial_fit(X)
    else:
        m = m.fit(X)
    zjryz__tmt = dmbdm__fdzd.allreduce(m.n_samples_seen_ - aejnz__phuf, op=
        MPI.SUM)
    m.n_samples_seen_ = zjryz__tmt + aejnz__phuf
    baohz__gkitc = np.zeros((yohh__jjf, *m.max_abs_.shape), dtype=m.
        max_abs_.dtype)
    dmbdm__fdzd.Allgather(m.max_abs_, baohz__gkitc)
    qtj__yas = np.nanmax(baohz__gkitc, axis=0)
    m.scale_ = sklearn_handle_zeros_in_scale(qtj__yas)
    m.max_abs_ = qtj__yas
    return m


@overload_method(BodoPreprocessingMaxAbsScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_max_abs_scaler_fit(m, X, y=None,
    _is_data_distributed=False):
    if _is_data_distributed:

        def _preprocessing_max_abs_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m,
                    X, partial=False)
            return m
    else:

        def _preprocessing_max_abs_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = m.fit(X, y)
            return m
    return _preprocessing_max_abs_scaler_fit_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'partial_fit',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_partial_fit(m, X, y=None,
    _is_data_distributed=False):
    if _is_data_distributed:

        def _preprocessing_max_abs_scaler_partial_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = sklearn_preprocessing_max_abs_scaler_fit_dist_helper(m,
                    X, partial=True)
            return m
    else:

        def _preprocessing_max_abs_scaler_partial_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_max_abs_scaler_type'):
                m = m.partial_fit(X, y)
            return m
    return _preprocessing_max_abs_scaler_partial_fit_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_transform(m, X):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_max_abs_scaler_transform_impl(m, X):
            with numba.objmode(transformed_X='csr_matrix_float64_int64'):
                transformed_X = m.transform(X)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
    else:

        def _preprocessing_max_abs_scaler_transform_impl(m, X):
            with numba.objmode(transformed_X='float64[:,:]'):
                transformed_X = m.transform(X)
            return transformed_X
    return _preprocessing_max_abs_scaler_transform_impl


@overload_method(BodoPreprocessingMaxAbsScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_max_abs_scaler_inverse_transform(m, X):
    if isinstance(X, CSRMatrixType):
        types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types
            .int64)

        def _preprocessing_max_abs_scaler_inverse_transform_impl(m, X):
            with numba.objmode(inverse_transformed_X='csr_matrix_float64_int64'
                ):
                inverse_transformed_X = m.inverse_transform(X)
                inverse_transformed_X.indices = (inverse_transformed_X.
                    indices.astype(np.int64))
                inverse_transformed_X.indptr = (inverse_transformed_X.
                    indptr.astype(np.int64))
            return inverse_transformed_X
    else:

        def _preprocessing_max_abs_scaler_inverse_transform_impl(m, X):
            with numba.objmode(inverse_transformed_X='float64[:,:]'):
                inverse_transformed_X = m.inverse_transform(X)
            return inverse_transformed_X
    return _preprocessing_max_abs_scaler_inverse_transform_impl


BodoModelSelectionLeavePOutType = install_py_obj_class(types_name=
    'model_selection_leave_p_out_type', python_type=sklearn.model_selection
    .LeavePOut, module=this_module, class_name=
    'BodoModelSelectionLeavePOutType', model_name=
    'BodoModelSelectionLeavePOutModel')
BodoModelSelectionLeavePOutGeneratorType = install_py_obj_class(types_name=
    'model_selection_leave_p_out_generator_type', module=this_module,
    class_name='BodoModelSelectionLeavePOutGeneratorType', model_name=
    'BodoModelSelectionLeavePOutGeneratorModel')


@overload(sklearn.model_selection.LeavePOut, no_unliteral=True)
def sklearn_model_selection_leave_p_out_overload(p):
    check_sklearn_version()

    def _sklearn_model_selection_leave_p_out_impl(p):
        with numba.objmode(m='model_selection_leave_p_out_type'):
            m = sklearn.model_selection.LeavePOut(p=p)
        return m
    return _sklearn_model_selection_leave_p_out_impl


def sklearn_model_selection_leave_p_out_generator_dist_helper(m, X):
    tkl__xpe = bodo.get_rank()
    jnacm__uaqjm = bodo.get_size()
    fmk__crqa = np.empty(jnacm__uaqjm, np.int64)
    bodo.libs.distributed_api.allgather(fmk__crqa, len(X))
    if tkl__xpe > 0:
        sajv__aufja = np.sum(fmk__crqa[:tkl__xpe])
    else:
        sajv__aufja = 0
    muor__ywqn = sajv__aufja + fmk__crqa[tkl__xpe]
    uspvo__orbum = np.sum(fmk__crqa)
    if uspvo__orbum <= m.p:
        raise ValueError(
            f'p={m.p} must be strictly less than the number of samples={uspvo__orbum}'
            )
    xghyi__iep = np.arange(sajv__aufja, muor__ywqn)
    for btrz__kdtk in combinations(range(uspvo__orbum), m.p):
        mske__gfd = np.array(btrz__kdtk)
        mske__gfd = mske__gfd[mske__gfd >= sajv__aufja]
        mske__gfd = mske__gfd[mske__gfd < muor__ywqn]
        xezq__dhxtl = np.zeros(len(X), dtype=bool)
        xezq__dhxtl[mske__gfd - sajv__aufja] = True
        fgpd__snh = xghyi__iep[np.logical_not(xezq__dhxtl)]
        yield fgpd__snh, mske__gfd


@overload_method(BodoModelSelectionLeavePOutType, 'split', no_unliteral=True)
def overload_model_selection_leave_p_out_generator(m, X, y=None, groups=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_leave_p_out_generator_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(gen='model_selection_leave_p_out_generator_type'
                ):
                gen = (
                    sklearn_model_selection_leave_p_out_generator_dist_helper
                    (m, X))
            return gen
    else:

        def _model_selection_leave_p_out_generator_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(gen='model_selection_leave_p_out_generator_type'
                ):
                gen = m.split(X, y=y, groups=groups)
            return gen
    return _model_selection_leave_p_out_generator_impl


@overload_method(BodoModelSelectionLeavePOutType, 'get_n_splits',
    no_unliteral=True)
def overload_model_selection_leave_p_out_get_n_splits(m, X, y=None, groups=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_leave_p_out_get_n_splits_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(out='int64'):
                uspvo__orbum = bodo.libs.distributed_api.dist_reduce(len(X),
                    np.int32(Reduce_Type.Sum.value))
                out = int(comb(uspvo__orbum, m.p, exact=True))
            return out
    else:

        def _model_selection_leave_p_out_get_n_splits_impl(m, X, y=None,
            groups=None, _is_data_distributed=False):
            with numba.objmode(out='int64'):
                out = m.get_n_splits(X)
            return out
    return _model_selection_leave_p_out_get_n_splits_impl


BodoModelSelectionKFoldType = install_py_obj_class(types_name=
    'model_selection_kfold_type', python_type=sklearn.model_selection.KFold,
    module=this_module, class_name='BodoModelSelectionKFoldType',
    model_name='BodoModelSelectionKFoldModel')


@overload(sklearn.model_selection.KFold, no_unliteral=True)
def sklearn_model_selection_kfold_overload(n_splits=5, shuffle=False,
    random_state=None):
    check_sklearn_version()

    def _sklearn_model_selection_kfold_impl(n_splits=5, shuffle=False,
        random_state=None):
        with numba.objmode(m='model_selection_kfold_type'):
            m = sklearn.model_selection.KFold(n_splits=n_splits, shuffle=
                shuffle, random_state=random_state)
        return m
    return _sklearn_model_selection_kfold_impl


def sklearn_model_selection_kfold_generator_dist_helper(m, X, y=None,
    groups=None):
    tkl__xpe = bodo.get_rank()
    jnacm__uaqjm = bodo.get_size()
    fmk__crqa = np.empty(jnacm__uaqjm, np.int64)
    bodo.libs.distributed_api.allgather(fmk__crqa, len(X))
    if tkl__xpe > 0:
        sajv__aufja = np.sum(fmk__crqa[:tkl__xpe])
    else:
        sajv__aufja = 0
    muor__ywqn = sajv__aufja + len(X)
    uspvo__orbum = np.sum(fmk__crqa)
    if uspvo__orbum < m.n_splits:
        raise ValueError(
            f'number of splits n_splits={m.n_splits} greater than the number of samples {uspvo__orbum}'
            )
    pybg__igozo = np.arange(uspvo__orbum)
    if m.shuffle:
        if m.random_state is None:
            wzqi__fxxlm = bodo.libs.distributed_api.bcast_scalar(np.random.
                randint(0, 2 ** 31))
            np.random.seed(wzqi__fxxlm)
        else:
            np.random.seed(m.random_state)
        np.random.shuffle(pybg__igozo)
    xghyi__iep = pybg__igozo[sajv__aufja:muor__ywqn]
    iptlp__fsubw = np.full(m.n_splits, uspvo__orbum // (jnacm__uaqjm * m.
        n_splits), dtype=np.int32)
    gpj__uczr = uspvo__orbum % (jnacm__uaqjm * m.n_splits)
    upn__qmlrs = np.full(m.n_splits, gpj__uczr // m.n_splits, dtype=int)
    upn__qmlrs[:gpj__uczr % m.n_splits] += 1
    ysg__nkkbi = np.repeat(np.arange(m.n_splits), upn__qmlrs)
    mtmoi__nru = ysg__nkkbi[tkl__xpe::jnacm__uaqjm]
    iptlp__fsubw[mtmoi__nru] += 1
    szqfw__gur = 0
    for cqi__qbzpp in iptlp__fsubw:
        wevv__lma = szqfw__gur + cqi__qbzpp
        mske__gfd = xghyi__iep[szqfw__gur:wevv__lma]
        fgpd__snh = np.concatenate((xghyi__iep[:szqfw__gur], xghyi__iep[
            wevv__lma:]), axis=0)
        yield fgpd__snh, mske__gfd
        szqfw__gur = wevv__lma


@overload_method(BodoModelSelectionKFoldType, 'split', no_unliteral=True)
def overload_model_selection_kfold_generator(m, X, y=None, groups=None,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _model_selection_kfold_generator_impl(m, X, y=None, groups=None,
            _is_data_distributed=False):
            with numba.objmode(gen='List(UniTuple(int64[:], 2))'):
                gen = list(sklearn_model_selection_kfold_generator_dist_helper
                    (m, X, y=None, groups=None))
            return gen
    else:

        def _model_selection_kfold_generator_impl(m, X, y=None, groups=None,
            _is_data_distributed=False):
            with numba.objmode(gen='List(UniTuple(int64[:], 2))'):
                gen = list(m.split(X, y=y, groups=groups))
            return gen
    return _model_selection_kfold_generator_impl


@overload_method(BodoModelSelectionKFoldType, 'get_n_splits', no_unliteral=True
    )
def overload_model_selection_kfold_get_n_splits(m, X=None, y=None, groups=
    None, _is_data_distributed=False):

    def _model_selection_kfold_get_n_splits_impl(m, X=None, y=None, groups=
        None, _is_data_distributed=False):
        with numba.objmode(out='int64'):
            out = m.n_splits
        return out
    return _model_selection_kfold_get_n_splits_impl


def get_data_slice_parallel(data, labels, len_train):
    ekfhb__bnx = data[:len_train]
    rbo__dutmn = data[len_train:]
    ekfhb__bnx = bodo.rebalance(ekfhb__bnx)
    rbo__dutmn = bodo.rebalance(rbo__dutmn)
    haj__kxway = labels[:len_train]
    voz__igsb = labels[len_train:]
    haj__kxway = bodo.rebalance(haj__kxway)
    voz__igsb = bodo.rebalance(voz__igsb)
    return ekfhb__bnx, rbo__dutmn, haj__kxway, voz__igsb


@numba.njit
def get_train_test_size(train_size, test_size):
    if train_size is None:
        train_size = -1.0
    if test_size is None:
        test_size = -1.0
    if train_size == -1.0 and test_size == -1.0:
        return 0.75, 0.25
    elif test_size == -1.0:
        return train_size, 1.0 - train_size
    elif train_size == -1.0:
        return 1.0 - test_size, test_size
    elif train_size + test_size > 1:
        raise ValueError(
            'The sum of test_size and train_size, should be in the (0, 1) range. Reduce test_size and/or train_size.'
            )
    else:
        return train_size, test_size


def set_labels_type(labels, label_type):
    return labels


@overload(set_labels_type, no_unliteral=True)
def overload_set_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _set_labels(labels, label_type):
            return pd.Series(labels)
        return _set_labels
    elif get_overload_const_int(label_type) == 2:

        def _set_labels(labels, label_type):
            return labels.values
        return _set_labels
    else:

        def _set_labels(labels, label_type):
            return labels
        return _set_labels


def reset_labels_type(labels, label_type):
    return labels


@overload(reset_labels_type, no_unliteral=True)
def overload_reset_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _reset_labels(labels, label_type):
            return labels.values
        return _reset_labels
    elif get_overload_const_int(label_type) == 2:

        def _reset_labels(labels, label_type):
            return pd.Series(labels, index=np.arange(len(labels)))
        return _reset_labels
    else:

        def _reset_labels(labels, label_type):
            return labels
        return _reset_labels


@overload(sklearn.model_selection.train_test_split, no_unliteral=True)
def overload_train_test_split(data, labels=None, train_size=None, test_size
    =None, random_state=None, shuffle=True, stratify=None,
    _is_data_distributed=False):
    check_sklearn_version()
    goy__fyi = {'stratify': stratify}
    swcl__syzb = {'stratify': None}
    check_unsupported_args('train_test_split', goy__fyi, swcl__syzb, 'ml')
    if is_overload_false(_is_data_distributed):
        uzyu__hjm = f'data_split_type_{numba.core.ir_utils.next_label()}'
        bclke__rxu = f'labels_split_type_{numba.core.ir_utils.next_label()}'
        for twt__ylhg, ifo__gmf in ((data, uzyu__hjm), (labels, bclke__rxu)):
            if isinstance(twt__ylhg, (DataFrameType, SeriesType)):
                eybei__eqpa = twt__ylhg.copy(index=NumericIndexType(types.
                    int64))
                setattr(types, ifo__gmf, eybei__eqpa)
            else:
                setattr(types, ifo__gmf, twt__ylhg)
        sbj__nfv = 'def _train_test_split_impl(\n'
        sbj__nfv += '    data,\n'
        sbj__nfv += '    labels=None,\n'
        sbj__nfv += '    train_size=None,\n'
        sbj__nfv += '    test_size=None,\n'
        sbj__nfv += '    random_state=None,\n'
        sbj__nfv += '    shuffle=True,\n'
        sbj__nfv += '    stratify=None,\n'
        sbj__nfv += '    _is_data_distributed=False,\n'
        sbj__nfv += '):  # pragma: no cover\n'
        sbj__nfv += (
            """    with numba.objmode(data_train='{}', data_test='{}', labels_train='{}', labels_test='{}'):
"""
            .format(uzyu__hjm, uzyu__hjm, bclke__rxu, bclke__rxu))
        sbj__nfv += """        data_train, data_test, labels_train, labels_test = sklearn.model_selection.train_test_split(
"""
        sbj__nfv += '            data,\n'
        sbj__nfv += '            labels,\n'
        sbj__nfv += '            train_size=train_size,\n'
        sbj__nfv += '            test_size=test_size,\n'
        sbj__nfv += '            random_state=random_state,\n'
        sbj__nfv += '            shuffle=shuffle,\n'
        sbj__nfv += '            stratify=stratify,\n'
        sbj__nfv += '        )\n'
        sbj__nfv += (
            '    return data_train, data_test, labels_train, labels_test\n')
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        _train_test_split_impl = vsdj__wqc['_train_test_split_impl']
        return _train_test_split_impl
    else:
        global get_data_slice_parallel
        if isinstance(get_data_slice_parallel, pytypes.FunctionType):
            get_data_slice_parallel = bodo.jit(get_data_slice_parallel,
                all_args_distributed_varlength=True,
                all_returns_distributed=True)
        label_type = 0
        if isinstance(data, DataFrameType) and isinstance(labels, types.Array):
            label_type = 1
        elif isinstance(data, types.Array) and isinstance(labels, SeriesType):
            label_type = 2
        if is_overload_none(random_state):
            random_state = 42

        def _train_test_split_impl(data, labels=None, train_size=None,
            test_size=None, random_state=None, shuffle=True, stratify=None,
            _is_data_distributed=False):
            if data.shape[0] != labels.shape[0]:
                raise ValueError(
                    'Found input variables with inconsistent number of samples\n'
                    )
            train_size, test_size = get_train_test_size(train_size, test_size)
            uspvo__orbum = bodo.libs.distributed_api.dist_reduce(len(data),
                np.int32(Reduce_Type.Sum.value))
            len_train = int(uspvo__orbum * train_size)
            llj__ckzll = uspvo__orbum - len_train
            if shuffle:
                labels = set_labels_type(labels, label_type)
                tkl__xpe = bodo.get_rank()
                jnacm__uaqjm = bodo.get_size()
                fmk__crqa = np.empty(jnacm__uaqjm, np.int64)
                bodo.libs.distributed_api.allgather(fmk__crqa, len(data))
                mbepo__ooggh = np.cumsum(fmk__crqa[0:tkl__xpe + 1])
                twwii__urcsh = np.full(uspvo__orbum, True)
                twwii__urcsh[:llj__ckzll] = False
                np.random.seed(42)
                np.random.permutation(twwii__urcsh)
                if tkl__xpe:
                    szqfw__gur = mbepo__ooggh[tkl__xpe - 1]
                else:
                    szqfw__gur = 0
                wilu__tcs = mbepo__ooggh[tkl__xpe]
                wrso__iudv = twwii__urcsh[szqfw__gur:wilu__tcs]
                ekfhb__bnx = data[wrso__iudv]
                rbo__dutmn = data[~wrso__iudv]
                haj__kxway = labels[wrso__iudv]
                voz__igsb = labels[~wrso__iudv]
                ekfhb__bnx = bodo.random_shuffle(ekfhb__bnx, seed=
                    random_state, parallel=True)
                rbo__dutmn = bodo.random_shuffle(rbo__dutmn, seed=
                    random_state, parallel=True)
                haj__kxway = bodo.random_shuffle(haj__kxway, seed=
                    random_state, parallel=True)
                voz__igsb = bodo.random_shuffle(voz__igsb, seed=
                    random_state, parallel=True)
                haj__kxway = reset_labels_type(haj__kxway, label_type)
                voz__igsb = reset_labels_type(voz__igsb, label_type)
            else:
                ekfhb__bnx, rbo__dutmn, haj__kxway, voz__igsb = (
                    get_data_slice_parallel(data, labels, len_train))
            return ekfhb__bnx, rbo__dutmn, haj__kxway, voz__igsb
        return _train_test_split_impl


@overload(sklearn.utils.shuffle, no_unliteral=True)
def sklearn_utils_shuffle_overload(data, random_state=None, n_samples=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):
        uzyu__hjm = f'utils_shuffle_type_{numba.core.ir_utils.next_label()}'
        if isinstance(data, (DataFrameType, SeriesType)):
            hnfx__ughw = data.copy(index=NumericIndexType(types.int64))
            setattr(types, uzyu__hjm, hnfx__ughw)
        else:
            setattr(types, uzyu__hjm, data)
        sbj__nfv = 'def _utils_shuffle_impl(\n'
        sbj__nfv += (
            '    data, random_state=None, n_samples=None, _is_data_distributed=False\n'
            )
        sbj__nfv += '):\n'
        sbj__nfv += f"    with numba.objmode(out='{uzyu__hjm}'):\n"
        sbj__nfv += '        out = sklearn.utils.shuffle(\n'
        sbj__nfv += (
            '            data, random_state=random_state, n_samples=n_samples\n'
            )
        sbj__nfv += '        )\n'
        sbj__nfv += '    return out\n'
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        _utils_shuffle_impl = vsdj__wqc['_utils_shuffle_impl']
    else:

        def _utils_shuffle_impl(data, random_state=None, n_samples=None,
            _is_data_distributed=False):
            m = bodo.random_shuffle(data, seed=random_state, n_samples=
                n_samples, parallel=True)
            return m
    return _utils_shuffle_impl


BodoPreprocessingMinMaxScalerType = install_py_obj_class(types_name=
    'preprocessing_minmax_scaler_type', python_type=sklearn.preprocessing.
    MinMaxScaler, module=this_module, class_name=
    'BodoPreprocessingMinMaxScalerType', model_name=
    'BodoPreprocessingMinMaxScalerModel')


@overload(sklearn.preprocessing.MinMaxScaler, no_unliteral=True)
def sklearn_preprocessing_minmax_scaler_overload(feature_range=(0, 1), copy
    =True, clip=False):
    check_sklearn_version()

    def _sklearn_preprocessing_minmax_scaler_impl(feature_range=(0, 1),
        copy=True, clip=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            m = sklearn.preprocessing.MinMaxScaler(feature_range=
                feature_range, copy=copy, clip=clip)
        return m
    return _sklearn_preprocessing_minmax_scaler_impl


def sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X):
    dmbdm__fdzd = MPI.COMM_WORLD
    yohh__jjf = dmbdm__fdzd.Get_size()
    m = m.fit(X)
    zjryz__tmt = dmbdm__fdzd.allreduce(m.n_samples_seen_, op=MPI.SUM)
    m.n_samples_seen_ = zjryz__tmt
    aakvs__elaut = np.zeros((yohh__jjf, *m.data_min_.shape), dtype=m.
        data_min_.dtype)
    dmbdm__fdzd.Allgather(m.data_min_, aakvs__elaut)
    tqf__mhf = np.nanmin(aakvs__elaut, axis=0)
    klxeb__rwrr = np.zeros((yohh__jjf, *m.data_max_.shape), dtype=m.
        data_max_.dtype)
    dmbdm__fdzd.Allgather(m.data_max_, klxeb__rwrr)
    thb__lsbr = np.nanmax(klxeb__rwrr, axis=0)
    wwkn__ybc = thb__lsbr - tqf__mhf
    m.scale_ = (m.feature_range[1] - m.feature_range[0]
        ) / sklearn_handle_zeros_in_scale(wwkn__ybc)
    m.min_ = m.feature_range[0] - tqf__mhf * m.scale_
    m.data_min_ = tqf__mhf
    m.data_max_ = thb__lsbr
    m.data_range_ = wwkn__ybc
    return m


@overload_method(BodoPreprocessingMinMaxScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_minmax_scaler_fit(m, X, y=None,
    _is_data_distributed=False):

    def _preprocessing_minmax_scaler_fit_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y)
        return m
    return _preprocessing_minmax_scaler_fit_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_transform(m, X):

    def _preprocessing_minmax_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_minmax_scaler_transform_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_inverse_transform(m, X):

    def _preprocessing_minmax_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_minmax_scaler_inverse_transform_impl


BodoPreprocessingRobustScalerType = install_py_obj_class(types_name=
    'preprocessing_robust_scaler_type', python_type=sklearn.preprocessing.
    RobustScaler, module=this_module, class_name=
    'BodoPreprocessingRobustScalerType', model_name=
    'BodoPreprocessingRobustScalerModel')


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_centering')
def get_robust_scaler_with_centering(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_centering
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_scaling')
def get_robust_scaler_with_scaling(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_scaling
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'quantile_range')
def get_robust_scaler_quantile_range(m):
    piu__xjo = numba.typeof((25.0, 75.0))

    def impl(m):
        with numba.objmode(result=piu__xjo):
            result = m.quantile_range
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'unit_variance')
def get_robust_scaler_unit_variance(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.unit_variance
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'copy')
def get_robust_scaler_copy(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.copy
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'center_')
def get_robust_scaler_center_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.center_
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'scale_')
def get_robust_scaler_scale_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.scale_
        return result
    return impl


@overload(sklearn.preprocessing.RobustScaler, no_unliteral=True)
def sklearn_preprocessing_robust_scaler_overload(with_centering=True,
    with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
    unit_variance=False):
    check_sklearn_version()

    def _sklearn_preprocessing_robust_scaler_impl(with_centering=True,
        with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
        unit_variance=False):
        with numba.objmode(m='preprocessing_robust_scaler_type'):
            m = sklearn.preprocessing.RobustScaler(with_centering=
                with_centering, with_scaling=with_scaling, quantile_range=
                quantile_range, copy=copy, unit_variance=unit_variance)
        return m
    return _sklearn_preprocessing_robust_scaler_impl


@overload_method(BodoPreprocessingRobustScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_robust_scaler_fit(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        sbj__nfv = f'def preprocessing_robust_scaler_fit_impl(\n'
        sbj__nfv += f'  m, X, y=None, _is_data_distributed=False\n'
        sbj__nfv += f'):\n'
        if isinstance(X, DataFrameType):
            sbj__nfv += f'  X = X.to_numpy()\n'
        sbj__nfv += (
            f"  with numba.objmode(qrange_l='float64', qrange_r='float64'):\n")
        sbj__nfv += f'    (qrange_l, qrange_r) = m.quantile_range\n'
        sbj__nfv += f'  if not 0 <= qrange_l <= qrange_r <= 100:\n'
        sbj__nfv += f'    raise ValueError(\n'
        sbj__nfv += f"""      'Invalid quantile range provided. Ensure that 0 <= quantile_range[0] <= quantile_range[1] <= 100.'
"""
        sbj__nfv += f'    )\n'
        sbj__nfv += (
            f'  qrange_l, qrange_r = qrange_l / 100.0, qrange_r / 100.0\n')
        sbj__nfv += f'  X = bodo.utils.conversion.coerce_to_array(X)\n'
        sbj__nfv += f'  num_features = X.shape[1]\n'
        sbj__nfv += f'  if m.with_scaling:\n'
        sbj__nfv += f'    scales = np.zeros(num_features)\n'
        sbj__nfv += f'  else:\n'
        sbj__nfv += f'    scales = None\n'
        sbj__nfv += f'  if m.with_centering:\n'
        sbj__nfv += f'    centers = np.zeros(num_features)\n'
        sbj__nfv += f'  else:\n'
        sbj__nfv += f'    centers = None\n'
        sbj__nfv += f'  if m.with_scaling or m.with_centering:\n'
        sbj__nfv += f'    numba.parfors.parfor.init_prange()\n'
        sbj__nfv += (
            f'    for feature_idx in numba.parfors.parfor.internal_prange(num_features):\n'
            )
        sbj__nfv += f"""      column_data = bodo.utils.conversion.ensure_contig_if_np(X[:, feature_idx])
"""
        sbj__nfv += f'      if m.with_scaling:\n'
        sbj__nfv += (
            f'        q1 = bodo.libs.array_kernels.quantile_parallel(\n')
        sbj__nfv += f'          column_data, qrange_l, 0\n'
        sbj__nfv += f'        )\n'
        sbj__nfv += (
            f'        q2 = bodo.libs.array_kernels.quantile_parallel(\n')
        sbj__nfv += f'          column_data, qrange_r, 0\n'
        sbj__nfv += f'        )\n'
        sbj__nfv += f'        scales[feature_idx] = q2 - q1\n'
        sbj__nfv += f'      if m.with_centering:\n'
        sbj__nfv += (
            f'        centers[feature_idx] = bodo.libs.array_ops.array_op_median(\n'
            )
        sbj__nfv += f'          column_data, True, True\n'
        sbj__nfv += f'        )\n'
        sbj__nfv += f'  if m.with_scaling:\n'
        sbj__nfv += (
            f'    constant_mask = scales < 10 * np.finfo(scales.dtype).eps\n')
        sbj__nfv += f'    scales[constant_mask] = 1.0\n'
        sbj__nfv += f'    if m.unit_variance:\n'
        sbj__nfv += f"      with numba.objmode(adjust='float64'):\n"
        sbj__nfv += (
            f'        adjust = stats.norm.ppf(qrange_r) - stats.norm.ppf(qrange_l)\n'
            )
        sbj__nfv += f'      scales = scales / adjust\n'
        sbj__nfv += f'  with numba.objmode():\n'
        sbj__nfv += f'    m.center_ = centers\n'
        sbj__nfv += f'    m.scale_ = scales\n'
        sbj__nfv += f'  return m\n'
        vsdj__wqc = {}
        exec(sbj__nfv, globals(), vsdj__wqc)
        _preprocessing_robust_scaler_fit_impl = vsdj__wqc[
            'preprocessing_robust_scaler_fit_impl']
        return _preprocessing_robust_scaler_fit_impl
    else:

        def _preprocessing_robust_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_robust_scaler_type'):
                m = m.fit(X, y)
            return m
        return _preprocessing_robust_scaler_fit_impl


@overload_method(BodoPreprocessingRobustScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_robust_scaler_transform_impl


@overload_method(BodoPreprocessingRobustScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_inverse_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_robust_scaler_inverse_transform_impl


BodoPreprocessingLabelEncoderType = install_py_obj_class(types_name=
    'preprocessing_label_encoder_type', python_type=sklearn.preprocessing.
    LabelEncoder, module=this_module, class_name=
    'BodoPreprocessingLabelEncoderType', model_name=
    'BodoPreprocessingLabelEncoderModel')


@overload(sklearn.preprocessing.LabelEncoder, no_unliteral=True)
def sklearn_preprocessing_label_encoder_overload():
    check_sklearn_version()

    def _sklearn_preprocessing_label_encoder_impl():
        with numba.objmode(m='preprocessing_label_encoder_type'):
            m = sklearn.preprocessing.LabelEncoder()
        return m
    return _sklearn_preprocessing_label_encoder_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_label_encoder_fit(m, y, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            y = bodo.utils.typing.decode_if_dict_array(y)
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            y_classes = bodo.libs.array_kernels.sort(y_classes, ascending=
                True, inplace=False)
            with numba.objmode:
                m.classes_ = y_classes
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl
    else:

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_label_encoder_type'):
                m = m.fit(y)
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_transform(m, y,
    _is_data_distributed=False):

    def _preprocessing_label_encoder_transform_impl(m, y,
        _is_data_distributed=False):
        with numba.objmode(transformed_y='int64[:]'):
            transformed_y = m.transform(y)
        return transformed_y
    return _preprocessing_label_encoder_transform_impl


@numba.njit
def le_fit_transform(m, y):
    m = m.fit(y, _is_data_distributed=True)
    transformed_y = m.transform(y, _is_data_distributed=True)
    return transformed_y


@overload_method(BodoPreprocessingLabelEncoderType, 'fit_transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_fit_transform(m, y,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            transformed_y = le_fit_transform(m, y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl
    else:

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(transformed_y='int64[:]'):
                transformed_y = m.fit_transform(y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl


BodoFExtractHashingVectorizerType = install_py_obj_class(types_name=
    'f_extract_hashing_vectorizer_type', python_type=sklearn.
    feature_extraction.text.HashingVectorizer, module=this_module,
    class_name='BodoFExtractHashingVectorizerType', model_name=
    'BodoFExtractHashingVectorizerModel')


@overload(sklearn.feature_extraction.text.HashingVectorizer, no_unliteral=True)
def sklearn_hashing_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', n_features=2 **
    20, binary=False, norm='l2', alternate_sign=True, dtype=np.float64):
    check_sklearn_version()

    def _sklearn_hashing_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word',
        n_features=2 ** 20, binary=False, norm='l2', alternate_sign=True,
        dtype=np.float64):
        with numba.objmode(m='f_extract_hashing_vectorizer_type'):
            m = sklearn.feature_extraction.text.HashingVectorizer(input=
                input, encoding=encoding, decode_error=decode_error,
                strip_accents=strip_accents, lowercase=lowercase,
                preprocessor=preprocessor, tokenizer=tokenizer, stop_words=
                stop_words, token_pattern=token_pattern, ngram_range=
                ngram_range, analyzer=analyzer, n_features=n_features,
                binary=binary, norm=norm, alternate_sign=alternate_sign,
                dtype=dtype)
        return m
    return _sklearn_hashing_vectorizer_impl


@overload_method(BodoFExtractHashingVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_hashing_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types.int64)

    def _hashing_vectorizer_fit_transform_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(transformed_X='csr_matrix_float64_int64'):
            transformed_X = m.fit_transform(X, y)
            transformed_X.indices = transformed_X.indices.astype(np.int64)
            transformed_X.indptr = transformed_X.indptr.astype(np.int64)
        return transformed_X
    return _hashing_vectorizer_fit_transform_impl


BodoRandomForestRegressorType = install_py_obj_class(types_name=
    'random_forest_regressor_type', python_type=sklearn.ensemble.
    RandomForestRegressor, module=this_module, class_name=
    'BodoRandomForestRegressorType', model_name=
    'BodoRandomForestRegressorModel')


@overload(sklearn.ensemble.RandomForestRegressor, no_unliteral=True)
def overload_sklearn_rf_regressor(n_estimators=100, criterion=
    'squared_error', max_depth=None, min_samples_split=2, min_samples_leaf=
    1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False, ccp_alpha=
    0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestRegressor_impl(n_estimators=100,
        criterion='squared_error', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_regressor_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestRegressor(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestRegressor_impl


@overload_method(BodoRandomForestRegressorType, 'predict', no_unliteral=True)
def overload_rf_regressor_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRandomForestRegressorType, 'score', no_unliteral=True)
def overload_rf_regressor_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_method(BodoRandomForestRegressorType, 'fit', no_unliteral=True)
@overload_method(BodoRandomForestClassifierType, 'fit', no_unliteral=True)
def overload_rf_classifier_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    zvs__bzgi = 'RandomForestClassifier'
    if isinstance(m, BodoRandomForestRegressorType):
        zvs__bzgi = 'RandomForestRegressor'
    if not is_overload_none(sample_weight):
        raise BodoError(
            f"sklearn.ensemble.{zvs__bzgi}.fit() : 'sample_weight' is not supported for distributed data."
            )

    def _model_fit_impl(m, X, y, sample_weight=None, _is_data_distributed=False
        ):
        with numba.objmode(first_rank_node='int32[:]'):
            first_rank_node = get_nodes_first_ranks()
        if _is_data_distributed:
            ireh__xkh = len(first_rank_node)
            X = bodo.gatherv(X)
            y = bodo.gatherv(y)
            if ireh__xkh > 1:
                X = bodo.libs.distributed_api.bcast_comm(X, comm_ranks=
                    first_rank_node, nranks=ireh__xkh)
                y = bodo.libs.distributed_api.bcast_comm(y, comm_ranks=
                    first_rank_node, nranks=ireh__xkh)
        with numba.objmode:
            random_forest_model_fit(m, X, y)
        bodo.barrier()
        return m
    return _model_fit_impl


BodoFExtractCountVectorizerType = install_py_obj_class(types_name=
    'f_extract_count_vectorizer_type', python_type=sklearn.
    feature_extraction.text.CountVectorizer, module=this_module, class_name
    ='BodoFExtractCountVectorizerType', model_name=
    'BodoFExtractCountVectorizerModel')


@overload(sklearn.feature_extraction.text.CountVectorizer, no_unliteral=True)
def sklearn_count_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=1.0,
    min_df=1, max_features=None, vocabulary=None, binary=False, dtype=np.int64
    ):
    check_sklearn_version()
    if not is_overload_constant_number(min_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'min_df' is not supported for distributed data.
"""
            )
    if not is_overload_constant_number(max_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'max_df' is not supported for distributed data.
"""
            )

    def _sklearn_count_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=
        1.0, min_df=1, max_features=None, vocabulary=None, binary=False,
        dtype=np.int64):
        with numba.objmode(m='f_extract_count_vectorizer_type'):
            m = sklearn.feature_extraction.text.CountVectorizer(input=input,
                encoding=encoding, decode_error=decode_error, strip_accents
                =strip_accents, lowercase=lowercase, preprocessor=
                preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                token_pattern=token_pattern, ngram_range=ngram_range,
                analyzer=analyzer, max_df=max_df, min_df=min_df,
                max_features=max_features, vocabulary=vocabulary, binary=
                binary, dtype=dtype)
        return m
    return _sklearn_count_vectorizer_impl


@overload_attribute(BodoFExtractCountVectorizerType, 'vocabulary_')
def get_cv_vocabulary_(m):
    types.dict_string_int = types.DictType(types.unicode_type, types.int64)

    def impl(m):
        with numba.objmode(result='dict_string_int'):
            result = m.vocabulary_
        return result
    return impl


def _cv_fit_transform_helper(m, X):
    nglzp__ccwsi = False
    local_vocabulary = m.vocabulary
    if m.vocabulary is None:
        m.fit(X)
        local_vocabulary = m.vocabulary_
        nglzp__ccwsi = True
    return nglzp__ccwsi, local_vocabulary


@overload_method(BodoFExtractCountVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_count_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    types.csr_matrix_int64_int64 = CSRMatrixType(types.int64, types.int64)
    if is_overload_true(_is_data_distributed):
        types.dict_str_int = types.DictType(types.unicode_type, types.int64)

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(local_vocabulary='dict_str_int', changeVoc=
                'bool_'):
                changeVoc, local_vocabulary = _cv_fit_transform_helper(m, X)
            if changeVoc:
                local_vocabulary = bodo.utils.conversion.coerce_to_array(list
                    (local_vocabulary.keys()))
                ikqo__avy = bodo.libs.array_kernels.unique(local_vocabulary,
                    parallel=True)
                ikqo__avy = bodo.allgatherv(ikqo__avy, False)
                ikqo__avy = bodo.libs.array_kernels.sort(ikqo__avy,
                    ascending=True, inplace=True)
                mcs__wwjho = {}
                for sox__hscf in range(len(ikqo__avy)):
                    mcs__wwjho[ikqo__avy[sox__hscf]] = sox__hscf
            else:
                mcs__wwjho = local_vocabulary
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                if changeVoc:
                    m.vocabulary = mcs__wwjho
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl
    else:

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl


@overload_method(BodoFExtractCountVectorizerType, 'get_feature_names_out',
    no_unliteral=True)
def overload_count_vectorizer_get_feature_names_out(m):
    check_sklearn_version()

    def impl(m):
        with numba.objmode(result=bodo.string_array_type):
            result = m.get_feature_names_out()
        return result
    return impl
