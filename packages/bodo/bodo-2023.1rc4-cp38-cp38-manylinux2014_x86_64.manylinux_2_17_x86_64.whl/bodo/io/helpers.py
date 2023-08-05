"""
File that contains some IO related helpers.
"""
import os
import threading
import uuid
import numba
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, models, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError, raise_bodo_error


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PyArrowTableSchemaType)
def box_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(pa.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    hxm__abnl = context.get_python_api(builder)
    return hxm__abnl.unserialize(hxm__abnl.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pa.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
use_nullable_pd_arr = True
_pyarrow_numba_type_map = {pa.bool_(): types.bool_, pa.int8(): types.int8,
    pa.int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.
    int64, pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
    types.uint32, pa.uint64(): types.uint64, pa.float32(): types.float32,
    pa.float64(): types.float64, pa.string(): string_type, pa.large_string(
    ): string_type, pa.binary(): bytes_type, pa.date32():
    datetime_date_type, pa.date64(): types.NPDatetime('ns'), pa.time32('s'):
    TimeType(0), pa.time32('ms'): TimeType(3), pa.time64('us'): TimeType(6),
    pa.time64('ns'): TimeType(9), pa.null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    mrvb__zqzqr = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in mrvb__zqzqr:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        amym__eecz = pa_ts_typ.to_pandas_dtype().tz
        lzl__plcnx = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            amym__eecz)
        return bodo.DatetimeArrayType(lzl__plcnx), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        eyspz__hhki, nli__qkr = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(eyspz__hhki), nli__qkr
    if isinstance(pa_typ.type, pa.StructType):
        jotlu__xcynt = []
        dgq__xnvw = []
        nli__qkr = True
        for bwt__surg in pa_typ.flatten():
            dgq__xnvw.append(bwt__surg.name.split('.')[-1])
            emo__utbb, bayqh__ddu = _get_numba_typ_from_pa_typ(bwt__surg,
                is_index, nullable_from_metadata, category_info)
            jotlu__xcynt.append(emo__utbb)
            nli__qkr = nli__qkr and bayqh__ddu
        return StructArrayType(tuple(jotlu__xcynt), tuple(dgq__xnvw)), nli__qkr
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        nndz__raqvy = _pyarrow_numba_type_map[pa_typ.type.index_type]
        hdl__mehqi = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=nndz__raqvy)
        return CategoricalArrayType(hdl__mehqi), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        sidl__ebm = _pyarrow_numba_type_map[pa_typ.type]
        nli__qkr = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if sidl__ebm == datetime_date_type:
        return datetime_date_array_type, nli__qkr
    if isinstance(sidl__ebm, TimeType):
        return TimeArrayType(sidl__ebm.precision), nli__qkr
    if sidl__ebm == bytes_type:
        return binary_array_type, nli__qkr
    eyspz__hhki = (string_array_type if sidl__ebm == string_type else types
        .Array(sidl__ebm, 1, 'C'))
    if sidl__ebm == types.bool_:
        eyspz__hhki = boolean_array
    ybh__rhxf = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if ybh__rhxf and not is_index and isinstance(sidl__ebm, types.Integer
        ) and pa_typ.nullable:
        eyspz__hhki = IntegerArrayType(sidl__ebm)
    if (ybh__rhxf and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(sidl__ebm, types.Float) and pa_typ.nullable):
        eyspz__hhki = FloatingArrayType(sidl__ebm)
    return eyspz__hhki, nli__qkr


_numba_pyarrow_type_map = {types.bool_: pa.bool_(), types.int8: pa.int8(),
    types.int16: pa.int16(), types.int32: pa.int32(), types.int64: pa.int64
    (), types.uint8: pa.uint8(), types.uint16: pa.uint16(), types.uint32:
    pa.uint32(), types.uint64: pa.uint64(), types.float32: pa.float32(),
    types.float64: pa.float64(), types.NPDatetime('ns'): pa.date64()}


def is_nullable_arrow_out(numba_type: types.ArrayCompatible) ->bool:
    return is_nullable(numba_type) or isinstance(numba_type, bodo.
        DatetimeArrayType) or isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.datetime64ns


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible, is_iceberg:
    bool=False):
    if isinstance(numba_type, ArrayItemArrayType):
        kwy__qrzlx = pa.field('element', _numba_to_pyarrow_type(numba_type.
            dtype, is_iceberg)[0])
        sidl__ebm = pa.list_(kwy__qrzlx)
    elif isinstance(numba_type, StructArrayType):
        ull__fhde = []
        for yays__epx, xwog__hmh in zip(numba_type.names, numba_type.data):
            cuhkv__ctk, xqcv__slrh = _numba_to_pyarrow_type(xwog__hmh,
                is_iceberg)
            ull__fhde.append(pa.field(yays__epx, cuhkv__ctk, True))
        sidl__ebm = pa.struct(ull__fhde)
    elif isinstance(numba_type, DecimalArrayType):
        sidl__ebm = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        hdl__mehqi: PDCategoricalDtype = numba_type.dtype
        sidl__ebm = pa.dictionary(_numba_to_pyarrow_type(hdl__mehqi.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(hdl__mehqi.
            elem_type, is_iceberg)[0], ordered=False if hdl__mehqi.ordered is
            None else hdl__mehqi.ordered)
    elif numba_type == boolean_array:
        sidl__ebm = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        sidl__ebm = pa.string()
    elif numba_type == binary_array_type:
        sidl__ebm = pa.binary()
    elif numba_type == datetime_date_array_type:
        sidl__ebm = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        sidl__ebm = pa.timestamp('us', 'UTC') if is_iceberg else pa.timestamp(
            'ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        sidl__ebm = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        sidl__ebm = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            sidl__ebm = pa.time32('s')
        elif numba_type.precision == 3:
            sidl__ebm = pa.time32('ms')
        elif numba_type.precision == 6:
            sidl__ebm = pa.time64('us')
        elif numba_type.precision == 9:
            sidl__ebm = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return sidl__ebm, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    ull__fhde = []
    for yays__epx, uwjp__niqq in zip(df.columns, df.data):
        try:
            avkxj__slrv, cyrn__irgs = _numba_to_pyarrow_type(uwjp__niqq,
                is_iceberg)
        except BodoError as ojfv__bza:
            raise_bodo_error(ojfv__bza.msg, ojfv__bza.loc)
        ull__fhde.append(pa.field(yays__epx, avkxj__slrv, cyrn__irgs))
    return pa.schema(ull__fhde)


def update_env_vars(env_vars):
    vwudo__jmlv = {}
    for eluc__fzsdw, immnc__oimeh in env_vars.items():
        if eluc__fzsdw in os.environ:
            vwudo__jmlv[eluc__fzsdw] = os.environ[eluc__fzsdw]
        else:
            vwudo__jmlv[eluc__fzsdw] = '__none__'
        if immnc__oimeh == '__none__':
            del os.environ[eluc__fzsdw]
        else:
            os.environ[eluc__fzsdw] = immnc__oimeh
    return vwudo__jmlv


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    iaa__zilfp = MPI.COMM_WORLD
    crlia__jcac = None
    if not is_parallel or iaa__zilfp.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as xwg__vez:
                crlia__jcac = xwg__vez.read()
    if is_parallel:
        crlia__jcac = iaa__zilfp.bcast(crlia__jcac)
    if crlia__jcac is None:
        crlia__jcac = '__none__'
    ozfup__vbg = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if ozfup__vbg and os.path.exists(fname):
            os.remove(fname)
    elif ozfup__vbg:
        with open(fname, 'w') as xwg__vez:
            xwg__vez.write(contents)
    if is_parallel:
        iaa__zilfp.Barrier()
    return crlia__jcac


@numba.njit
def uuid4_helper():
    with numba.objmode(out='unicode_type'):
        out = str(uuid.uuid4())
    return out


class ExceptionPropagatingThread(threading.Thread):

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as ojfv__bza:
            self.exc = ojfv__bza

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class ExceptionPropagatingThreadType(types.Opaque):

    def __init__(self):
        super(ExceptionPropagatingThreadType, self).__init__(name=
            'ExceptionPropagatingThreadType')


exception_propagating_thread_type = ExceptionPropagatingThreadType()
types.exception_propagating_thread_type = exception_propagating_thread_type
register_model(ExceptionPropagatingThreadType)(models.OpaqueModel)


@unbox(ExceptionPropagatingThreadType)
def unbox_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ExceptionPropagatingThreadType)
def box_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(ExceptionPropagatingThread)
def typeof_exception_propagating_thread(val, c):
    return exception_propagating_thread_type


def join_all_threads(thread_list):
    uqpd__rzvwa = tracing.Event('join_all_threads', is_parallel=True)
    iaa__zilfp = MPI.COMM_WORLD
    ytlli__hgny = None
    try:
        for nfm__kmdno in thread_list:
            if isinstance(nfm__kmdno, threading.Thread):
                nfm__kmdno.join()
    except Exception as ojfv__bza:
        ytlli__hgny = ojfv__bza
    fvqpi__pkhgn = int(ytlli__hgny is not None)
    nlsv__irjiy, tsbs__aeide = iaa__zilfp.allreduce((fvqpi__pkhgn,
        iaa__zilfp.Get_rank()), op=MPI.MAXLOC)
    if nlsv__irjiy:
        if iaa__zilfp.Get_rank() == tsbs__aeide:
            lysxi__jdkj = ytlli__hgny
        else:
            lysxi__jdkj = None
        lysxi__jdkj = iaa__zilfp.bcast(lysxi__jdkj, root=tsbs__aeide)
        if fvqpi__pkhgn:
            raise ytlli__hgny
        else:
            raise lysxi__jdkj
    uqpd__rzvwa.finalize()
