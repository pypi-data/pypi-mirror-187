"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    opc__xbo = tuple(val.columns.to_list())
    xapqr__knf = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        wtigf__elm = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        wtigf__elm = numba.typeof(val.index)
    mmcrd__fnmp = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    fdhxh__qyzn = len(xapqr__knf) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(xapqr__knf, wtigf__elm, opc__xbo, mmcrd__fnmp,
        is_table_format=fdhxh__qyzn)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    mmcrd__fnmp = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        wjmqa__efbz = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        wjmqa__efbz = numba.typeof(val.index)
    yoy__nce = _infer_series_arr_type(val)
    if _use_dict_str_type and yoy__nce == string_array_type:
        yoy__nce = bodo.dict_str_arr_type
    return SeriesType(yoy__nce.dtype, data=yoy__nce, index=wjmqa__efbz,
        name_typ=numba.typeof(val.name), dist=mmcrd__fnmp)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    niin__smgn = c.pyapi.object_getattr_string(val, 'index')
    cegxl__jaei = c.pyapi.to_native_value(typ.index, niin__smgn).value
    c.pyapi.decref(niin__smgn)
    if typ.is_table_format:
        yle__flz = cgutils.create_struct_proxy(typ.table_type)(c.context, c
            .builder)
        yle__flz.parent = val
        for xdwdd__yks, iswvc__xmfh in typ.table_type.type_to_blk.items():
            fnj__aqs = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[iswvc__xmfh]))
            ibxda__ksc, wnmbd__ikpop = ListInstance.allocate_ex(c.context,
                c.builder, types.List(xdwdd__yks), fnj__aqs)
            wnmbd__ikpop.size = fnj__aqs
            setattr(yle__flz, f'block_{iswvc__xmfh}', wnmbd__ikpop.value)
        saq__wxlo = c.pyapi.call_method(val, '__len__', ())
        hjzx__hpwwd = c.pyapi.long_as_longlong(saq__wxlo)
        c.pyapi.decref(saq__wxlo)
        yle__flz.len = hjzx__hpwwd
        rlumf__tdas = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [yle__flz._getvalue()])
    else:
        ikn__wzanf = [c.context.get_constant_null(xdwdd__yks) for
            xdwdd__yks in typ.data]
        rlumf__tdas = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            ikn__wzanf)
    ofhi__puylv = construct_dataframe(c.context, c.builder, typ,
        rlumf__tdas, cegxl__jaei, val, None)
    return NativeValue(ofhi__puylv)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        wtf__yyiso = df._bodo_meta['type_metadata'][1]
    else:
        wtf__yyiso = [None] * len(df.columns)
    wulps__feqt = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        wtf__yyiso[i]) for i in range(len(df.columns))]
    wulps__feqt = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        xdwdd__yks == string_array_type else xdwdd__yks) for xdwdd__yks in
        wulps__feqt]
    return tuple(wulps__feqt)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45
    PD_nullable_Float32 = 46
    PD_nullable_Float64 = 47
    FloatingArray = 48


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, FloatDtype(types.float32):
    SeriesDtypeEnum.PD_nullable_Float32.value, FloatDtype(types.float64):
    SeriesDtypeEnum.PD_nullable_Float64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.PD_nullable_Float32.value: FloatDtype(types.float32),
    SeriesDtypeEnum.PD_nullable_Float64.value: FloatDtype(types.float64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    mbjm__iekui, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(mbjm__iekui) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {mbjm__iekui}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        hrtbp__hvi, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return hrtbp__hvi, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        hrtbp__hvi, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return hrtbp__hvi, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        hrtbp__hvi, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return hrtbp__hvi, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        drv__rvzpr = typ_enum_list[1]
        get__ezfg = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(drv__rvzpr, get__ezfg)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        ttf__teg = typ_enum_list[1]
        annp__atd = tuple(typ_enum_list[2:2 + ttf__teg])
        hymm__ianhy = typ_enum_list[2 + ttf__teg:]
        pirpd__sestk = []
        for i in range(ttf__teg):
            hymm__ianhy, ldvdy__aqe = _dtype_from_type_enum_list_recursor(
                hymm__ianhy)
            pirpd__sestk.append(ldvdy__aqe)
        return hymm__ianhy, StructType(tuple(pirpd__sestk), annp__atd)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        rfzvv__zuiq = typ_enum_list[1]
        hymm__ianhy = typ_enum_list[2:]
        return hymm__ianhy, rfzvv__zuiq
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        rfzvv__zuiq = typ_enum_list[1]
        hymm__ianhy = typ_enum_list[2:]
        return hymm__ianhy, numba.types.literal(rfzvv__zuiq)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        hymm__ianhy, lznm__trqz = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        hymm__ianhy, rgxyw__twjg = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        hymm__ianhy, gmykw__etfq = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        hymm__ianhy, ankvz__cbdd = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        hymm__ianhy, mxht__gbvg = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        return hymm__ianhy, PDCategoricalDtype(lznm__trqz, rgxyw__twjg,
            gmykw__etfq, ankvz__cbdd, mxht__gbvg)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return hymm__ianhy, DatetimeIndexType(zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        hymm__ianhy, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        hymm__ianhy, ankvz__cbdd = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        return hymm__ianhy, NumericIndexType(dtype, zjl__hyog, ankvz__cbdd)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        hymm__ianhy, jys__oystc = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        return hymm__ianhy, PeriodIndexType(jys__oystc, zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        hymm__ianhy, ankvz__cbdd = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            hymm__ianhy)
        return hymm__ianhy, CategoricalIndexType(ankvz__cbdd, zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return hymm__ianhy, RangeIndexType(zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return hymm__ianhy, StringIndexType(zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return hymm__ianhy, BinaryIndexType(zjl__hyog)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        hymm__ianhy, zjl__hyog = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return hymm__ianhy, TimedeltaIndexType(zjl__hyog)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        qbfy__usyb = get_overload_const_int(typ)
        if numba.types.maybe_literal(qbfy__usyb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qbfy__usyb]
    elif is_overload_constant_str(typ):
        qbfy__usyb = get_overload_const_str(typ)
        if numba.types.maybe_literal(qbfy__usyb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qbfy__usyb]
    elif is_overload_constant_bool(typ):
        qbfy__usyb = get_overload_const_bool(typ)
        if numba.types.maybe_literal(qbfy__usyb) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qbfy__usyb]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, FloatingArrayType):
        return [SeriesDtypeEnum.FloatingArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        byo__yjv = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for hubpm__ltx in typ.names:
            byo__yjv.append(hubpm__ltx)
        for hkbq__oeajo in typ.data:
            byo__yjv += _dtype_to_type_enum_list_recursor(hkbq__oeajo)
        return byo__yjv
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        gidgk__pvf = _dtype_to_type_enum_list_recursor(typ.categories)
        sayl__bnhhz = _dtype_to_type_enum_list_recursor(typ.elem_type)
        uhf__yrp = _dtype_to_type_enum_list_recursor(typ.ordered)
        ofx__kuvk = _dtype_to_type_enum_list_recursor(typ.data)
        pgx__hoeba = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + gidgk__pvf + sayl__bnhhz + uhf__yrp + ofx__kuvk + pgx__hoeba
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                ykwq__iam = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    kqxw__qgy = FloatingArrayType(ykwq__iam)
                else:
                    kqxw__qgy = types.Array(ykwq__iam, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                ykwq__iam = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    kqxw__qgy = IntegerArrayType(ykwq__iam)
                else:
                    kqxw__qgy = types.Array(ykwq__iam, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                ykwq__iam = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    kqxw__qgy = IntegerArrayType(ykwq__iam)
                else:
                    kqxw__qgy = types.Array(ykwq__iam, 1, 'C')
            elif typ.dtype == types.bool_:
                ykwq__iam = typ.dtype
                kqxw__qgy = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(ykwq__iam
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(kqxw__qgy)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _is_wrapper_pd_arr(arr):
    if isinstance(arr, pd.arrays.StringArray):
        return False
    return isinstance(arr, (pd.arrays.PandasArray, pd.arrays.TimedeltaArray)
        ) or isinstance(arr, pd.arrays.DatetimeArray) and arr.tz is None


def unwrap_pd_arr(arr):
    if _is_wrapper_pd_arr(arr):
        return np.ascontiguousarray(arr._ndarray)
    return arr


def _fix_series_arr_type(pd_arr):
    if _is_wrapper_pd_arr(pd_arr):
        return pd_arr._ndarray
    return pd_arr


def _infer_series_arr_type(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.array) == 0 or S.isna().sum() == len(S):
            if array_metadata is not None:
                return _dtype_from_type_enum_list(array_metadata)
            elif hasattr(S, '_bodo_meta'
                ) and S._bodo_meta is not None and 'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None:
                ojnba__fmxul = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    ojnba__fmxul))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        hpy__wyxkj = bodo.typeof(_fix_series_arr_type(S.array))
        if hpy__wyxkj == types.Array(types.bool_, 1, 'C'):
            hpy__wyxkj = bodo.boolean_array
        if isinstance(hpy__wyxkj, types.Array):
            assert hpy__wyxkj.ndim == 1, 'invalid numpy array type in Series'
            hpy__wyxkj = types.Array(hpy__wyxkj.dtype, 1, 'C')
        return hpy__wyxkj
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    hek__dlgae = cgutils.is_not_null(builder, parent_obj)
    acm__bxcil = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(hek__dlgae):
        paft__xaff = pyapi.object_getattr_string(parent_obj, 'columns')
        saq__wxlo = pyapi.call_method(paft__xaff, '__len__', ())
        builder.store(pyapi.long_as_longlong(saq__wxlo), acm__bxcil)
        pyapi.decref(saq__wxlo)
        pyapi.decref(paft__xaff)
    use_parent_obj = builder.and_(hek__dlgae, builder.icmp_unsigned('==',
        builder.load(acm__bxcil), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        wvy__nigl = df_typ.runtime_colname_typ
        context.nrt.incref(builder, wvy__nigl, dataframe_payload.columns)
        return pyapi.from_native_value(wvy__nigl, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        eljl__qpdak = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        eljl__qpdak = np.array(df_typ.columns, 'int64')
    else:
        eljl__qpdak = df_typ.columns
    efsik__ivc = numba.typeof(eljl__qpdak)
    wgi__ineod = context.get_constant_generic(builder, efsik__ivc, eljl__qpdak)
    wyky__crwpr = pyapi.from_native_value(efsik__ivc, wgi__ineod, c.env_manager
        )
    if (efsik__ivc == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        bcwgx__ypyv = wyky__crwpr
        wyky__crwpr = pyapi.call_method(wyky__crwpr, 'to_numpy', ())
        pyapi.decref(bcwgx__ypyv)
    return wyky__crwpr


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (fqnt__ewu, pocd__bazlb):
        with fqnt__ewu:
            pyapi.incref(obj)
            vnuz__pxt = context.insert_const_string(c.builder.module, 'numpy')
            lao__unx = pyapi.import_module_noblock(vnuz__pxt)
            if df_typ.has_runtime_cols:
                mmd__ozjpm = 0
            else:
                mmd__ozjpm = len(df_typ.columns)
            ahw__qgdoc = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), mmd__ozjpm))
            ngew__woi = pyapi.call_method(lao__unx, 'arange', (ahw__qgdoc,))
            pyapi.object_setattr_string(obj, 'columns', ngew__woi)
            pyapi.decref(lao__unx)
            pyapi.decref(ngew__woi)
            pyapi.decref(ahw__qgdoc)
        with pocd__bazlb:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            ourks__ipg = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            vnuz__pxt = context.insert_const_string(c.builder.module, 'pandas')
            lao__unx = pyapi.import_module_noblock(vnuz__pxt)
            df_obj = pyapi.call_method(lao__unx, 'DataFrame', (pyapi.
                borrow_none(), ourks__ipg))
            pyapi.decref(lao__unx)
            pyapi.decref(ourks__ipg)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    jtl__zwzqd = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = jtl__zwzqd.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        qcth__ctc = typ.table_type
        yle__flz = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, qcth__ctc, yle__flz)
        klw__ymfy = box_table(qcth__ctc, yle__flz, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (qxni__xvfhp, llrl__awiv):
            with qxni__xvfhp:
                tquq__vwshm = pyapi.object_getattr_string(klw__ymfy, 'arrays')
                bjyv__qrfep = c.pyapi.make_none()
                if n_cols is None:
                    saq__wxlo = pyapi.call_method(tquq__vwshm, '__len__', ())
                    fnj__aqs = pyapi.long_as_longlong(saq__wxlo)
                    pyapi.decref(saq__wxlo)
                else:
                    fnj__aqs = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, fnj__aqs) as tcez__evrvr:
                    i = tcez__evrvr.index
                    niawa__yjv = pyapi.list_getitem(tquq__vwshm, i)
                    jkbg__ihseg = c.builder.icmp_unsigned('!=', niawa__yjv,
                        bjyv__qrfep)
                    with builder.if_then(jkbg__ihseg):
                        djwkl__whzm = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, djwkl__whzm, niawa__yjv)
                        pyapi.decref(djwkl__whzm)
                pyapi.decref(tquq__vwshm)
                pyapi.decref(bjyv__qrfep)
            with llrl__awiv:
                df_obj = builder.load(res)
                ourks__ipg = pyapi.object_getattr_string(df_obj, 'index')
                sji__vrizk = c.pyapi.call_method(klw__ymfy, 'to_pandas', (
                    ourks__ipg,))
                builder.store(sji__vrizk, res)
                pyapi.decref(df_obj)
                pyapi.decref(ourks__ipg)
        pyapi.decref(klw__ymfy)
    else:
        vcyv__fdhgf = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        ajm__xsvx = typ.data
        for i, arr, yoy__nce in zip(range(n_cols), vcyv__fdhgf, ajm__xsvx):
            vsm__mmdi = cgutils.alloca_once_value(builder, arr)
            ebbh__wey = cgutils.alloca_once_value(builder, context.
                get_constant_null(yoy__nce))
            jkbg__ihseg = builder.not_(is_ll_eq(builder, vsm__mmdi, ebbh__wey))
            wvx__ojmnu = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, jkbg__ihseg))
            with builder.if_then(wvx__ojmnu):
                djwkl__whzm = pyapi.long_from_longlong(context.get_constant
                    (types.int64, i))
                context.nrt.incref(builder, yoy__nce, arr)
                arr_obj = pyapi.from_native_value(yoy__nce, arr, c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, djwkl__whzm, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(djwkl__whzm)
    df_obj = builder.load(res)
    wyky__crwpr = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', wyky__crwpr)
    pyapi.decref(wyky__crwpr)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    bjyv__qrfep = pyapi.borrow_none()
    fmoyj__xxx = pyapi.unserialize(pyapi.serialize_object(slice))
    tao__kbeo = pyapi.call_function_objargs(fmoyj__xxx, [bjyv__qrfep])
    ycnm__pxj = pyapi.long_from_longlong(col_ind)
    kww__yssbf = pyapi.tuple_pack([tao__kbeo, ycnm__pxj])
    ahiyw__zmyim = pyapi.object_getattr_string(df_obj, 'iloc')
    rob__mdhxx = pyapi.object_getitem(ahiyw__zmyim, kww__yssbf)
    mhbra__akd = pyapi.object_getattr_string(rob__mdhxx, 'array')
    wvfe__qao = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(wvfe__qao, [mhbra__akd])
    pyapi.decref(mhbra__akd)
    pyapi.decref(wvfe__qao)
    pyapi.decref(fmoyj__xxx)
    pyapi.decref(tao__kbeo)
    pyapi.decref(ycnm__pxj)
    pyapi.decref(kww__yssbf)
    pyapi.decref(ahiyw__zmyim)
    pyapi.decref(rob__mdhxx)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        jtl__zwzqd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            jtl__zwzqd.parent, args[1], data_typ)
        tbcl__gbrf = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            yle__flz = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            iswvc__xmfh = df_typ.table_type.type_to_blk[data_typ]
            ozavu__papg = getattr(yle__flz, f'block_{iswvc__xmfh}')
            rcz__olgna = ListInstance(c.context, c.builder, types.List(
                data_typ), ozavu__papg)
            kiqk__oyrj = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            rcz__olgna.inititem(kiqk__oyrj, tbcl__gbrf.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, tbcl__gbrf.value, col_ind)
        pldt__akym = DataFramePayloadType(df_typ)
        llkkg__vfcsh = context.nrt.meminfo_data(builder, jtl__zwzqd.meminfo)
        anscn__uqt = context.get_value_type(pldt__akym).as_pointer()
        llkkg__vfcsh = builder.bitcast(llkkg__vfcsh, anscn__uqt)
        builder.store(dataframe_payload._getvalue(), llkkg__vfcsh)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    mhbra__akd = c.pyapi.object_getattr_string(val, 'array')
    wvfe__qao = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(wvfe__qao, [mhbra__akd])
    bnck__cfbkd = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    ourks__ipg = c.pyapi.object_getattr_string(val, 'index')
    cegxl__jaei = c.pyapi.to_native_value(typ.index, ourks__ipg).value
    axtn__opcn = c.pyapi.object_getattr_string(val, 'name')
    ubfc__lkm = c.pyapi.to_native_value(typ.name_typ, axtn__opcn).value
    pwjzc__skw = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, bnck__cfbkd, cegxl__jaei, ubfc__lkm)
    c.pyapi.decref(wvfe__qao)
    c.pyapi.decref(mhbra__akd)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(ourks__ipg)
    c.pyapi.decref(axtn__opcn)
    return NativeValue(pwjzc__skw)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ersgr__ppw = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ersgr__ppw._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    vnuz__pxt = c.context.insert_const_string(c.builder.module, 'pandas')
    trzr__gfn = c.pyapi.import_module_noblock(vnuz__pxt)
    auf__aoel = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, auf__aoel.data)
    c.context.nrt.incref(c.builder, typ.index, auf__aoel.index)
    c.context.nrt.incref(c.builder, typ.name_typ, auf__aoel.name)
    arr_obj = c.pyapi.from_native_value(typ.data, auf__aoel.data, c.env_manager
        )
    ourks__ipg = c.pyapi.from_native_value(typ.index, auf__aoel.index, c.
        env_manager)
    axtn__opcn = c.pyapi.from_native_value(typ.name_typ, auf__aoel.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(trzr__gfn, 'Series', (arr_obj, ourks__ipg,
        dtype, axtn__opcn))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(ourks__ipg)
    c.pyapi.decref(axtn__opcn)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(trzr__gfn)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    uht__wcmsm = []
    for tmha__bmycy in typ_list:
        if isinstance(tmha__bmycy, int) and not isinstance(tmha__bmycy, bool):
            xmy__wsgk = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), tmha__bmycy))
        else:
            xpmgv__cryy = numba.typeof(tmha__bmycy)
            jpfe__rnij = context.get_constant_generic(builder, xpmgv__cryy,
                tmha__bmycy)
            xmy__wsgk = pyapi.from_native_value(xpmgv__cryy, jpfe__rnij,
                env_manager)
        uht__wcmsm.append(xmy__wsgk)
    wqolv__ahrkp = pyapi.list_pack(uht__wcmsm)
    for val in uht__wcmsm:
        pyapi.decref(val)
    return wqolv__ahrkp


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    hcy__hcf = not typ.has_runtime_cols
    optnm__wfs = 2 if hcy__hcf else 1
    psjy__qyl = pyapi.dict_new(optnm__wfs)
    sftr__hjf = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(psjy__qyl, 'dist', sftr__hjf)
    pyapi.decref(sftr__hjf)
    if hcy__hcf:
        pwvkq__zaexm = _dtype_to_type_enum_list(typ.index)
        if pwvkq__zaexm != None:
            kund__aftbh = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, pwvkq__zaexm)
        else:
            kund__aftbh = pyapi.make_none()
        if typ.is_table_format:
            xdwdd__yks = typ.table_type
            iot__htdi = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for iswvc__xmfh, dtype in xdwdd__yks.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                fnj__aqs = c.context.get_constant(types.int64, len(
                    xdwdd__yks.block_to_arr_ind[iswvc__xmfh]))
                wjuzm__ykh = c.context.make_constant_array(c.builder, types
                    .Array(types.int64, 1, 'C'), np.array(xdwdd__yks.
                    block_to_arr_ind[iswvc__xmfh], dtype=np.int64))
                fmpp__ogw = c.context.make_array(types.Array(types.int64, 1,
                    'C'))(c.context, c.builder, wjuzm__ykh)
                with cgutils.for_range(c.builder, fnj__aqs) as tcez__evrvr:
                    i = tcez__evrvr.index
                    yqmj__enp = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), fmpp__ogw, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(iot__htdi, yqmj__enp, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            vmywd__agzgu = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    wqolv__ahrkp = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    wqolv__ahrkp = pyapi.make_none()
                vmywd__agzgu.append(wqolv__ahrkp)
            iot__htdi = pyapi.list_pack(vmywd__agzgu)
            for val in vmywd__agzgu:
                pyapi.decref(val)
        yps__cgmt = pyapi.list_pack([kund__aftbh, iot__htdi])
        pyapi.dict_setitem_string(psjy__qyl, 'type_metadata', yps__cgmt)
    pyapi.object_setattr_string(obj, '_bodo_meta', psjy__qyl)
    pyapi.decref(psjy__qyl)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    if isinstance(series_typ.dtype, types.Float) and isinstance(series_typ.
        data, FloatingArrayType):
        return FloatDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    psjy__qyl = pyapi.dict_new(2)
    sftr__hjf = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pwvkq__zaexm = _dtype_to_type_enum_list(typ.index)
    if pwvkq__zaexm != None:
        kund__aftbh = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, pwvkq__zaexm)
    else:
        kund__aftbh = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            cwkv__wru = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            cwkv__wru = pyapi.make_none()
    else:
        cwkv__wru = pyapi.make_none()
    sro__xtdw = pyapi.list_pack([kund__aftbh, cwkv__wru])
    pyapi.dict_setitem_string(psjy__qyl, 'type_metadata', sro__xtdw)
    pyapi.decref(sro__xtdw)
    pyapi.dict_setitem_string(psjy__qyl, 'dist', sftr__hjf)
    pyapi.object_setattr_string(obj, '_bodo_meta', psjy__qyl)
    pyapi.decref(psjy__qyl)
    pyapi.decref(sftr__hjf)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as hmmw__ovur:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    cdr__axal = numba.np.numpy_support.map_layout(val)
    rdoa__almzq = not val.flags.writeable
    return types.Array(dtype, val.ndim, cdr__axal, readonly=rdoa__almzq)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    pfzne__mrjab = val[i]
    qcm__brooj = 100
    if isinstance(pfzne__mrjab, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(pfzne__mrjab, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(pfzne__mrjab, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(pfzne__mrjab, (int, np.int8, np.int16, np.int32, np.
        int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(
            pfzne__mrjab))
    elif isinstance(pfzne__mrjab, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(
            pfzne__mrjab))
    elif isinstance(pfzne__mrjab, (dict, Dict)) and len(pfzne__mrjab.keys()
        ) <= qcm__brooj and all(isinstance(dlcm__brkav, str) for
        dlcm__brkav in pfzne__mrjab.keys()):
        annp__atd = tuple(pfzne__mrjab.keys())
        qmnzj__jsic = tuple(_get_struct_value_arr_type(v) for v in
            pfzne__mrjab.values())
        return StructArrayType(qmnzj__jsic, annp__atd)
    elif isinstance(pfzne__mrjab, (dict, Dict)):
        inkgz__ugve = numba.typeof(_value_to_array(list(pfzne__mrjab.keys())))
        himky__xhrd = numba.typeof(_value_to_array(list(pfzne__mrjab.values()))
            )
        inkgz__ugve = to_str_arr_if_dict_array(inkgz__ugve)
        himky__xhrd = to_str_arr_if_dict_array(himky__xhrd)
        return MapArrayType(inkgz__ugve, himky__xhrd)
    elif isinstance(pfzne__mrjab, tuple):
        qmnzj__jsic = tuple(_get_struct_value_arr_type(v) for v in pfzne__mrjab
            )
        return TupleArrayType(qmnzj__jsic)
    if isinstance(pfzne__mrjab, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.
        StringArray, pd.arrays.ArrowStringArray)):
        if isinstance(pfzne__mrjab, list):
            pfzne__mrjab = _value_to_array(pfzne__mrjab)
        too__xfiav = numba.typeof(pfzne__mrjab)
        too__xfiav = to_str_arr_if_dict_array(too__xfiav)
        return ArrayItemArrayType(too__xfiav)
    if isinstance(pfzne__mrjab, datetime.date):
        return datetime_date_array_type
    if isinstance(pfzne__mrjab, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(pfzne__mrjab, bodo.Time):
        return TimeArrayType(pfzne__mrjab.precision)
    if isinstance(pfzne__mrjab, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(pfzne__mrjab, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(
        f'Unsupported object array with first value: {pfzne__mrjab}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    ivq__txew = val.copy()
    ivq__txew.append(None)
    arr = np.array(ivq__txew, np.object_)
    if len(val) and isinstance(val[0], float):
        arr = np.array(val, np.float64)
    return arr


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    yoy__nce = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        yoy__nce = to_nullable_type(yoy__nce)
    return yoy__nce
