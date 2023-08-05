"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import time
from functools import cached_property
from typing import Optional, Sequence
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.hiframes.time_ext import TimeArrayType
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr, types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data: Optional[Sequence['types.Array']]=None, index=
        None, columns: Optional[Sequence[str]]=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format}, {self.has_runtime_cols})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            maedg__viar = f'{len(self.data)} columns of types {set(self.data)}'
            rld__dnx = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            hkdxr__bxvk = str(hash(super().__str__()))
            return (
                f'dataframe({maedg__viar}, {self.index}, {rld__dnx}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={hkdxr__bxvk})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @cached_property
    def column_index(self):
        return {smype__zrchv: i for i, smype__zrchv in enumerate(self.columns)}

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            jrs__yxap = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(vhff__zwg.unify(typingctx, kfaig__xzv) if 
                vhff__zwg != kfaig__xzv else vhff__zwg for vhff__zwg,
                kfaig__xzv in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if jrs__yxap is not None and None not in data:
                return DataFrameType(data, jrs__yxap, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(vhff__zwg.is_precise() for vhff__zwg in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        cpi__drz = self.columns.index(col_name)
        blzlq__kdkz = tuple(list(self.data[:cpi__drz]) + [new_type] + list(
            self.data[cpi__drz + 1:]))
        return DataFrameType(blzlq__kdkz, self.index, self.columns, self.
            dist, self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        yzp__fcy = [('data', data_typ), ('index', fe_type.df_type.index), (
            'parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            yzp__fcy.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, yzp__fcy)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        yzp__fcy = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, yzp__fcy)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        vixk__buys = 'n',
        gxd__mjjsv = {'n': 5}
        lfkyn__ash, zkcgm__pnua = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, vixk__buys, gxd__mjjsv)
        tdi__pzmdx = zkcgm__pnua[0]
        if not is_overload_int(tdi__pzmdx):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        xvllf__fak = df.copy()
        return xvllf__fak(*zkcgm__pnua).replace(pysig=lfkyn__ash)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        boguw__xffvl = (df,) + args
        vixk__buys = 'df', 'method', 'min_periods'
        gxd__mjjsv = {'method': 'pearson', 'min_periods': 1}
        vrtxe__radd = 'method',
        lfkyn__ash, zkcgm__pnua = bodo.utils.typing.fold_typing_args(func_name,
            boguw__xffvl, kws, vixk__buys, gxd__mjjsv, vrtxe__radd)
        fnan__txtu = zkcgm__pnua[2]
        if not is_overload_int(fnan__txtu):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        vfmzq__vko = []
        dnunp__zqrne = []
        for smype__zrchv, xrd__azbvl in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(xrd__azbvl.dtype):
                vfmzq__vko.append(smype__zrchv)
                dnunp__zqrne.append(types.Array(types.float64, 1, 'A'))
        if len(vfmzq__vko) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        dnunp__zqrne = tuple(dnunp__zqrne)
        vfmzq__vko = tuple(vfmzq__vko)
        index_typ = bodo.utils.typing.type_col_to_index(vfmzq__vko)
        xvllf__fak = DataFrameType(dnunp__zqrne, index_typ, vfmzq__vko)
        return xvllf__fak(*zkcgm__pnua).replace(pysig=lfkyn__ash)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        mgde__bmh = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        lksv__mzyij = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        amr__iih = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        rzqro__josc = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        vuaby__dbn = dict(raw=lksv__mzyij, result_type=amr__iih)
        knhqm__aymlt = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', vuaby__dbn, knhqm__aymlt,
            package_name='pandas', module_name='DataFrame')
        drbuc__dvxg = True
        if types.unliteral(mgde__bmh) == types.unicode_type:
            if not is_overload_constant_str(mgde__bmh):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            drbuc__dvxg = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        psex__xpdnz = get_overload_const_int(axis)
        if drbuc__dvxg and psex__xpdnz != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif psex__xpdnz not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        qoykt__pkbv = []
        for arr_typ in df.data:
            undg__dob = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            vvmc__jvv = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(undg__dob), types.int64), {}).return_type
            qoykt__pkbv.append(vvmc__jvv)
        ybm__ofevp = types.none
        qgbyo__vto = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(smype__zrchv) for smype__zrchv in df.
            columns)), None)
        dtqa__jxw = types.BaseTuple.from_types(qoykt__pkbv)
        keec__hqes = types.Tuple([types.bool_] * len(dtqa__jxw))
        gdru__tpqgl = bodo.NullableTupleType(dtqa__jxw, keec__hqes)
        pmz__tqyn = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if pmz__tqyn == types.NPDatetime('ns'):
            pmz__tqyn = bodo.pd_timestamp_tz_naive_type
        if pmz__tqyn == types.NPTimedelta('ns'):
            pmz__tqyn = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(dtqa__jxw):
            cpvw__ixu = HeterogeneousSeriesType(gdru__tpqgl, qgbyo__vto,
                pmz__tqyn)
        else:
            cpvw__ixu = SeriesType(dtqa__jxw.dtype, gdru__tpqgl, qgbyo__vto,
                pmz__tqyn)
        gwvp__mxh = cpvw__ixu,
        if rzqro__josc is not None:
            gwvp__mxh += tuple(rzqro__josc.types)
        try:
            if not drbuc__dvxg:
                czo__pdoql = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(mgde__bmh), self.context,
                    'DataFrame.apply', axis if psex__xpdnz == 1 else None)
            else:
                czo__pdoql = get_const_func_output_type(mgde__bmh,
                    gwvp__mxh, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as yhfik__akmrd:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                yhfik__akmrd))
        if drbuc__dvxg:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(czo__pdoql, (SeriesType, HeterogeneousSeriesType)
                ) and czo__pdoql.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(czo__pdoql, HeterogeneousSeriesType):
                nugi__stn, fcys__cta = czo__pdoql.const_info
                if isinstance(czo__pdoql.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    nenvj__ehcf = czo__pdoql.data.tuple_typ.types
                elif isinstance(czo__pdoql.data, types.Tuple):
                    nenvj__ehcf = czo__pdoql.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                wjbo__vnjy = tuple(to_nullable_type(dtype_to_array_type(
                    lxcx__xnub)) for lxcx__xnub in nenvj__ehcf)
                icf__lht = DataFrameType(wjbo__vnjy, df.index, fcys__cta)
            elif isinstance(czo__pdoql, SeriesType):
                ooa__vcqt, fcys__cta = czo__pdoql.const_info
                wjbo__vnjy = tuple(to_nullable_type(dtype_to_array_type(
                    czo__pdoql.dtype)) for nugi__stn in range(ooa__vcqt))
                icf__lht = DataFrameType(wjbo__vnjy, df.index, fcys__cta)
            else:
                zkx__xdfq = get_udf_out_arr_type(czo__pdoql)
                icf__lht = SeriesType(zkx__xdfq.dtype, zkx__xdfq, df.index,
                    None)
        else:
            icf__lht = czo__pdoql
        tlkn__wmga = ', '.join("{} = ''".format(vhff__zwg) for vhff__zwg in
            kws.keys())
        zwjww__ptvs = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {tlkn__wmga}):
"""
        zwjww__ptvs += '    pass\n'
        wcjtl__qimh = {}
        exec(zwjww__ptvs, {}, wcjtl__qimh)
        shx__bjndd = wcjtl__qimh['apply_stub']
        lfkyn__ash = numba.core.utils.pysignature(shx__bjndd)
        jkm__zulf = (mgde__bmh, axis, lksv__mzyij, amr__iih, rzqro__josc
            ) + tuple(kws.values())
        return signature(icf__lht, *jkm__zulf).replace(pysig=lfkyn__ash)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        vixk__buys = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        gxd__mjjsv = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        vrtxe__radd = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        lfkyn__ash, zkcgm__pnua = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, vixk__buys, gxd__mjjsv, vrtxe__radd)
        savd__pcfg = zkcgm__pnua[2]
        if not is_overload_constant_str(savd__pcfg):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        kwia__vwjju = zkcgm__pnua[0]
        if not is_overload_none(kwia__vwjju) and not (is_overload_int(
            kwia__vwjju) or is_overload_constant_str(kwia__vwjju)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(kwia__vwjju):
            hzgdd__fkgaz = get_overload_const_str(kwia__vwjju)
            if hzgdd__fkgaz not in df.columns:
                raise BodoError(
                    f'{func_name}: {hzgdd__fkgaz} column not found.')
        elif is_overload_int(kwia__vwjju):
            akzy__jmc = get_overload_const_int(kwia__vwjju)
            if akzy__jmc > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {akzy__jmc} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            kwia__vwjju = df.columns[kwia__vwjju]
        fariy__uau = zkcgm__pnua[1]
        if not is_overload_none(fariy__uau) and not (is_overload_int(
            fariy__uau) or is_overload_constant_str(fariy__uau)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(fariy__uau):
            apwvv__tligd = get_overload_const_str(fariy__uau)
            if apwvv__tligd not in df.columns:
                raise BodoError(
                    f'{func_name}: {apwvv__tligd} column not found.')
        elif is_overload_int(fariy__uau):
            rbi__ngeln = get_overload_const_int(fariy__uau)
            if rbi__ngeln > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {rbi__ngeln} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            fariy__uau = df.columns[fariy__uau]
        uccib__vwfio = zkcgm__pnua[3]
        if not is_overload_none(uccib__vwfio) and not is_tuple_like_type(
            uccib__vwfio):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        fgtq__llswm = zkcgm__pnua[10]
        if not is_overload_none(fgtq__llswm) and not is_overload_constant_str(
            fgtq__llswm):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        vkjqm__lip = zkcgm__pnua[12]
        if not is_overload_bool(vkjqm__lip):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        wjj__akgpk = zkcgm__pnua[17]
        if not is_overload_none(wjj__akgpk) and not is_tuple_like_type(
            wjj__akgpk):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        gus__hnnti = zkcgm__pnua[18]
        if not is_overload_none(gus__hnnti) and not is_tuple_like_type(
            gus__hnnti):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        kxg__nzpsi = zkcgm__pnua[22]
        if not is_overload_none(kxg__nzpsi) and not is_overload_int(kxg__nzpsi
            ):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        bbg__wdnig = zkcgm__pnua[29]
        if not is_overload_none(bbg__wdnig) and not is_overload_constant_str(
            bbg__wdnig):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        ukzuf__weoeg = zkcgm__pnua[30]
        if not is_overload_none(ukzuf__weoeg) and not is_overload_constant_str(
            ukzuf__weoeg):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        faqor__xox = types.List(types.mpl_line_2d_type)
        savd__pcfg = get_overload_const_str(savd__pcfg)
        if savd__pcfg == 'scatter':
            if is_overload_none(kwia__vwjju) and is_overload_none(fariy__uau):
                raise BodoError(
                    f'{func_name}: {savd__pcfg} requires an x and y column.')
            elif is_overload_none(kwia__vwjju):
                raise BodoError(
                    f'{func_name}: {savd__pcfg} x column is missing.')
            elif is_overload_none(fariy__uau):
                raise BodoError(
                    f'{func_name}: {savd__pcfg} y column is missing.')
            faqor__xox = types.mpl_path_collection_type
        elif savd__pcfg != 'line':
            raise BodoError(f'{func_name}: {savd__pcfg} plot is not supported.'
                )
        return signature(faqor__xox, *zkcgm__pnua).replace(pysig=lfkyn__ash)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            sepcx__fdt = df.columns.index(attr)
            arr_typ = df.data[sepcx__fdt]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            gsmci__inv = []
            blzlq__kdkz = []
            flxas__ncu = False
            for i, oywuk__pmqy in enumerate(df.columns):
                if oywuk__pmqy[0] != attr:
                    continue
                flxas__ncu = True
                gsmci__inv.append(oywuk__pmqy[1] if len(oywuk__pmqy) == 2 else
                    oywuk__pmqy[1:])
                blzlq__kdkz.append(df.data[i])
            if flxas__ncu:
                return DataFrameType(tuple(blzlq__kdkz), df.index, tuple(
                    gsmci__inv))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        xqqsb__fipr = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(xqqsb__fipr)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        yudg__lnogm = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], yudg__lnogm)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    qiv__uvhnu = builder.module
    ftne__lne = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    tgte__ipfr = cgutils.get_or_insert_function(qiv__uvhnu, ftne__lne, name
        ='.dtor.df.{}'.format(df_type))
    if not tgte__ipfr.is_declaration:
        return tgte__ipfr
    tgte__ipfr.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(tgte__ipfr.append_basic_block())
    qpedh__mlt = tgte__ipfr.args[0]
    yyro__hnbd = context.get_value_type(payload_type).as_pointer()
    yqj__juvnw = builder.bitcast(qpedh__mlt, yyro__hnbd)
    payload = context.make_helper(builder, payload_type, ref=yqj__juvnw)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        lwwtz__djmj = context.get_python_api(builder)
        vfe__son = lwwtz__djmj.gil_ensure()
        lwwtz__djmj.decref(payload.parent)
        lwwtz__djmj.gil_release(vfe__son)
    builder.ret_void()
    return tgte__ipfr


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    zcby__jsoj = cgutils.create_struct_proxy(payload_type)(context, builder)
    zcby__jsoj.data = data_tup
    zcby__jsoj.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        zcby__jsoj.columns = colnames
    tyy__pac = context.get_value_type(payload_type)
    iykd__nkgo = context.get_abi_sizeof(tyy__pac)
    ygi__jcy = define_df_dtor(context, builder, df_type, payload_type)
    lyg__tfg = context.nrt.meminfo_alloc_dtor(builder, context.get_constant
        (types.uintp, iykd__nkgo), ygi__jcy)
    dis__usp = context.nrt.meminfo_data(builder, lyg__tfg)
    jezd__dyzd = builder.bitcast(dis__usp, tyy__pac.as_pointer())
    pzok__ufzky = cgutils.create_struct_proxy(df_type)(context, builder)
    pzok__ufzky.meminfo = lyg__tfg
    if parent is None:
        pzok__ufzky.parent = cgutils.get_null_value(pzok__ufzky.parent.type)
    else:
        pzok__ufzky.parent = parent
        zcby__jsoj.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            lwwtz__djmj = context.get_python_api(builder)
            vfe__son = lwwtz__djmj.gil_ensure()
            lwwtz__djmj.incref(parent)
            lwwtz__djmj.gil_release(vfe__son)
    builder.store(zcby__jsoj._getvalue(), jezd__dyzd)
    return pzok__ufzky._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        dwx__pror = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        dwx__pror = [lxcx__xnub for lxcx__xnub in data_typ.dtype.arr_types]
    rikii__iyucf = DataFrameType(tuple(dwx__pror + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        yapj__lfu = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return yapj__lfu
    sig = signature(rikii__iyucf, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    ooa__vcqt = len(data_tup_typ.types)
    if ooa__vcqt == 0:
        column_names = ()
    qvv__zzj = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(qvv__zzj, ColNamesMetaType) and isinstance(qvv__zzj.
        meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = qvv__zzj.meta
    if ooa__vcqt == 1 and isinstance(data_tup_typ.types[0], TableType):
        ooa__vcqt = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == ooa__vcqt, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    rnpo__rkjv = data_tup_typ.types
    if ooa__vcqt != 0 and isinstance(data_tup_typ.types[0], TableType):
        rnpo__rkjv = data_tup_typ.types[0].arr_types
        is_table_format = True
    rikii__iyucf = DataFrameType(rnpo__rkjv, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            mtv__rpxq = cgutils.create_struct_proxy(rikii__iyucf.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = mtv__rpxq.parent
        yapj__lfu = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return yapj__lfu
    sig = signature(rikii__iyucf, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        pzok__ufzky = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, pzok__ufzky.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        zcby__jsoj = get_dataframe_payload(context, builder, df_typ, args[0])
        pyg__lfnbw = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[pyg__lfnbw]
        if df_typ.is_table_format:
            mtv__rpxq = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(zcby__jsoj.data, 0))
            ylul__alrmk = df_typ.table_type.type_to_blk[arr_typ]
            qldu__vgqp = getattr(mtv__rpxq, f'block_{ylul__alrmk}')
            nuvt__aha = ListInstance(context, builder, types.List(arr_typ),
                qldu__vgqp)
            wsbor__pvst = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[pyg__lfnbw])
            yudg__lnogm = nuvt__aha.getitem(wsbor__pvst)
        else:
            yudg__lnogm = builder.extract_value(zcby__jsoj.data, pyg__lfnbw)
        oosb__afr = cgutils.alloca_once_value(builder, yudg__lnogm)
        xkos__iikrx = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, oosb__afr, xkos__iikrx)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    lyg__tfg = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, lyg__tfg)
    yyro__hnbd = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, yyro__hnbd)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    rikii__iyucf = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        rikii__iyucf = types.Tuple([TableType(df_typ.data)])
    sig = signature(rikii__iyucf, df_typ)

    def codegen(context, builder, signature, args):
        zcby__jsoj = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            zcby__jsoj.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        zcby__jsoj = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, zcby__jsoj
            .index)
    rikii__iyucf = df_typ.index
    sig = signature(rikii__iyucf, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        xvllf__fak = df.data[i]
        return xvllf__fak(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        zcby__jsoj = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(zcby__jsoj.data, 0))
    return df_typ.table_type(df_typ), codegen


def get_dataframe_all_data(df):
    return df.data


def get_dataframe_all_data_impl(df):
    if df.is_table_format:

        def _impl(df):
            return get_dataframe_table(df)
        return _impl
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for i in
        range(len(df.columns)))
    kliaw__mmi = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{kliaw__mmi})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        xvllf__fak = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return xvllf__fak(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        zcby__jsoj = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, zcby__jsoj.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_all_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    dtqa__jxw = self.typemap[data_tup.name]
    if any(is_tuple_like_type(lxcx__xnub) for lxcx__xnub in dtqa__jxw.types):
        return None
    if equiv_set.has_shape(data_tup):
        zmzde__eyiqa = equiv_set.get_shape(data_tup)
        if len(zmzde__eyiqa) > 1:
            equiv_set.insert_equiv(*zmzde__eyiqa)
        if len(zmzde__eyiqa) > 0:
            qgbyo__vto = self.typemap[index.name]
            if not isinstance(qgbyo__vto, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(zmzde__eyiqa[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(zmzde__eyiqa[0], len(
                zmzde__eyiqa)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vsmjj__ofmxa = args[0]
    data_types = self.typemap[vsmjj__ofmxa.name].data
    if any(is_tuple_like_type(lxcx__xnub) for lxcx__xnub in data_types):
        return None
    if equiv_set.has_shape(vsmjj__ofmxa):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            vsmjj__ofmxa)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    vsmjj__ofmxa = args[0]
    qgbyo__vto = self.typemap[vsmjj__ofmxa.name].index
    if isinstance(qgbyo__vto, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(vsmjj__ofmxa):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            vsmjj__ofmxa)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    vsmjj__ofmxa = args[0]
    if equiv_set.has_shape(vsmjj__ofmxa):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            vsmjj__ofmxa), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    vsmjj__ofmxa = args[0]
    if equiv_set.has_shape(vsmjj__ofmxa):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            vsmjj__ofmxa)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    pyg__lfnbw = get_overload_const_int(c_ind_typ)
    if df_typ.data[pyg__lfnbw] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        eqjud__dnfvi, nugi__stn, nzqh__uzaqe = args
        zcby__jsoj = get_dataframe_payload(context, builder, df_typ,
            eqjud__dnfvi)
        if df_typ.is_table_format:
            mtv__rpxq = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(zcby__jsoj.data, 0))
            ylul__alrmk = df_typ.table_type.type_to_blk[arr_typ]
            qldu__vgqp = getattr(mtv__rpxq, f'block_{ylul__alrmk}')
            nuvt__aha = ListInstance(context, builder, types.List(arr_typ),
                qldu__vgqp)
            wsbor__pvst = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[pyg__lfnbw])
            nuvt__aha.setitem(wsbor__pvst, nzqh__uzaqe, True)
        else:
            yudg__lnogm = builder.extract_value(zcby__jsoj.data, pyg__lfnbw)
            context.nrt.decref(builder, df_typ.data[pyg__lfnbw], yudg__lnogm)
            zcby__jsoj.data = builder.insert_value(zcby__jsoj.data,
                nzqh__uzaqe, pyg__lfnbw)
            context.nrt.incref(builder, arr_typ, nzqh__uzaqe)
        pzok__ufzky = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=eqjud__dnfvi)
        payload_type = DataFramePayloadType(df_typ)
        yqj__juvnw = context.nrt.meminfo_data(builder, pzok__ufzky.meminfo)
        yyro__hnbd = context.get_value_type(payload_type).as_pointer()
        yqj__juvnw = builder.bitcast(yqj__juvnw, yyro__hnbd)
        builder.store(zcby__jsoj._getvalue(), yqj__juvnw)
        return impl_ret_borrowed(context, builder, df_typ, eqjud__dnfvi)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        tjqgz__jkl = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        dwu__ozblj = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=tjqgz__jkl)
        jgqew__sfbhs = get_dataframe_payload(context, builder, df_typ,
            tjqgz__jkl)
        pzok__ufzky = construct_dataframe(context, builder, signature.
            return_type, jgqew__sfbhs.data, index_val, dwu__ozblj.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), jgqew__sfbhs.data)
        return pzok__ufzky
    rikii__iyucf = DataFrameType(df_t.data, index_t, df_t.columns, df_t.
        dist, df_t.is_table_format)
    sig = signature(rikii__iyucf, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    ooa__vcqt = len(df_type.columns)
    ijjps__zsqz = ooa__vcqt
    cqta__btzfl = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    djrlf__jjjj = col_name not in df_type.columns
    pyg__lfnbw = ooa__vcqt
    if djrlf__jjjj:
        cqta__btzfl += arr_type,
        column_names += col_name,
        ijjps__zsqz += 1
    else:
        pyg__lfnbw = df_type.columns.index(col_name)
        cqta__btzfl = tuple(arr_type if i == pyg__lfnbw else cqta__btzfl[i] for
            i in range(ooa__vcqt))

    def codegen(context, builder, signature, args):
        eqjud__dnfvi, nugi__stn, nzqh__uzaqe = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, eqjud__dnfvi)
        uurqm__wfgqp = cgutils.create_struct_proxy(df_type)(context,
            builder, value=eqjud__dnfvi)
        if df_type.is_table_format:
            voonn__pkml = df_type.table_type
            sxlbk__eyyb = builder.extract_value(in_dataframe_payload.data, 0)
            nwkt__fhg = TableType(cqta__btzfl)
            wcqu__ijbz = set_table_data_codegen(context, builder,
                voonn__pkml, sxlbk__eyyb, nwkt__fhg, arr_type, nzqh__uzaqe,
                pyg__lfnbw, djrlf__jjjj)
            data_tup = context.make_tuple(builder, types.Tuple([nwkt__fhg]),
                [wcqu__ijbz])
        else:
            rnpo__rkjv = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != pyg__lfnbw else nzqh__uzaqe) for i in range(
                ooa__vcqt)]
            if djrlf__jjjj:
                rnpo__rkjv.append(nzqh__uzaqe)
            for vsmjj__ofmxa, zgkbh__klf in zip(rnpo__rkjv, cqta__btzfl):
                context.nrt.incref(builder, zgkbh__klf, vsmjj__ofmxa)
            data_tup = context.make_tuple(builder, types.Tuple(cqta__btzfl),
                rnpo__rkjv)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        atht__bccdc = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, uurqm__wfgqp.parent, None)
        if not djrlf__jjjj and arr_type == df_type.data[pyg__lfnbw]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            yqj__juvnw = context.nrt.meminfo_data(builder, uurqm__wfgqp.meminfo
                )
            yyro__hnbd = context.get_value_type(payload_type).as_pointer()
            yqj__juvnw = builder.bitcast(yqj__juvnw, yyro__hnbd)
            dve__lbye = get_dataframe_payload(context, builder, df_type,
                atht__bccdc)
            builder.store(dve__lbye._getvalue(), yqj__juvnw)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, nwkt__fhg, builder.
                    extract_value(data_tup, 0))
            else:
                for vsmjj__ofmxa, zgkbh__klf in zip(rnpo__rkjv, cqta__btzfl):
                    context.nrt.incref(builder, zgkbh__klf, vsmjj__ofmxa)
        has_parent = cgutils.is_not_null(builder, uurqm__wfgqp.parent)
        with builder.if_then(has_parent):
            lwwtz__djmj = context.get_python_api(builder)
            vfe__son = lwwtz__djmj.gil_ensure()
            mil__gcul = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, nzqh__uzaqe)
            smype__zrchv = numba.core.pythonapi._BoxContext(context,
                builder, lwwtz__djmj, mil__gcul)
            qgcn__wfeh = smype__zrchv.pyapi.from_native_value(arr_type,
                nzqh__uzaqe, smype__zrchv.env_manager)
            if isinstance(col_name, str):
                csgmi__wloj = context.insert_const_string(builder.module,
                    col_name)
                kzpz__jqmi = lwwtz__djmj.string_from_string(csgmi__wloj)
            else:
                assert isinstance(col_name, int)
                kzpz__jqmi = lwwtz__djmj.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            lwwtz__djmj.object_setitem(uurqm__wfgqp.parent, kzpz__jqmi,
                qgcn__wfeh)
            lwwtz__djmj.decref(qgcn__wfeh)
            lwwtz__djmj.decref(kzpz__jqmi)
            lwwtz__djmj.gil_release(vfe__son)
        return atht__bccdc
    rikii__iyucf = DataFrameType(cqta__btzfl, index_typ, column_names,
        df_type.dist, df_type.is_table_format)
    sig = signature(rikii__iyucf, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    ooa__vcqt = len(pyval.columns)
    rnpo__rkjv = []
    for i in range(ooa__vcqt):
        vpdjl__cva = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            qgcn__wfeh = vpdjl__cva.array
        else:
            qgcn__wfeh = vpdjl__cva.values
        rnpo__rkjv.append(qgcn__wfeh)
    rnpo__rkjv = tuple(rnpo__rkjv)
    if df_type.is_table_format:
        mtv__rpxq = context.get_constant_generic(builder, df_type.
            table_type, Table(rnpo__rkjv))
        data_tup = lir.Constant.literal_struct([mtv__rpxq])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], oywuk__pmqy) for
            i, oywuk__pmqy in enumerate(rnpo__rkjv)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    qtt__lcmj = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, qtt__lcmj])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    hom__bjv = context.get_constant(types.int64, -1)
    feayq__pzmor = context.get_constant_null(types.voidptr)
    lyg__tfg = lir.Constant.literal_struct([hom__bjv, feayq__pzmor,
        feayq__pzmor, payload, hom__bjv])
    lyg__tfg = cgutils.global_constant(builder, '.const.meminfo', lyg__tfg
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([lyg__tfg, qtt__lcmj])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        jrs__yxap = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        jrs__yxap = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, jrs__yxap)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        blzlq__kdkz = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                blzlq__kdkz)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), blzlq__kdkz)
    elif not fromty.is_table_format and toty.is_table_format:
        blzlq__kdkz = _cast_df_data_to_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        blzlq__kdkz = _cast_df_data_to_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        blzlq__kdkz = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        blzlq__kdkz = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, blzlq__kdkz,
        jrs__yxap, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    gkbdk__wbn = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        znhx__oewn = get_index_data_arr_types(toty.index)[0]
        hluag__blz = bodo.utils.transform.get_type_alloc_counts(znhx__oewn) - 1
        vvsqn__vgd = ', '.join('0' for nugi__stn in range(hluag__blz))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(vvsqn__vgd, ', ' if hluag__blz == 1 else ''))
        gkbdk__wbn['index_arr_type'] = znhx__oewn
    ozb__hcv = []
    for i, arr_typ in enumerate(toty.data):
        hluag__blz = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        vvsqn__vgd = ', '.join('0' for nugi__stn in range(hluag__blz))
        qkzdr__zxwh = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, vvsqn__vgd, ', ' if hluag__blz == 1 else ''))
        ozb__hcv.append(qkzdr__zxwh)
        gkbdk__wbn[f'arr_type{i}'] = arr_typ
    ozb__hcv = ', '.join(ozb__hcv)
    zwjww__ptvs = 'def impl():\n'
    rqg__nieqt = bodo.hiframes.dataframe_impl._gen_init_df(zwjww__ptvs,
        toty.columns, ozb__hcv, index, gkbdk__wbn)
    df = context.compile_internal(builder, rqg__nieqt, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    foume__hhgd = toty.table_type
    mtv__rpxq = cgutils.create_struct_proxy(foume__hhgd)(context, builder)
    mtv__rpxq.parent = in_dataframe_payload.parent
    for lxcx__xnub, ylul__alrmk in foume__hhgd.type_to_blk.items():
        zlz__vav = context.get_constant(types.int64, len(foume__hhgd.
            block_to_arr_ind[ylul__alrmk]))
        nugi__stn, dfl__khks = ListInstance.allocate_ex(context, builder,
            types.List(lxcx__xnub), zlz__vav)
        dfl__khks.size = zlz__vav
        setattr(mtv__rpxq, f'block_{ylul__alrmk}', dfl__khks.value)
    for i, lxcx__xnub in enumerate(fromty.data):
        nhxvv__bppuc = toty.data[i]
        if lxcx__xnub != nhxvv__bppuc:
            nbmw__rcque = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*nbmw__rcque)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        yudg__lnogm = builder.extract_value(in_dataframe_payload.data, i)
        if lxcx__xnub != nhxvv__bppuc:
            pmsds__gajh = context.cast(builder, yudg__lnogm, lxcx__xnub,
                nhxvv__bppuc)
            sjol__gqz = False
        else:
            pmsds__gajh = yudg__lnogm
            sjol__gqz = True
        ylul__alrmk = foume__hhgd.type_to_blk[lxcx__xnub]
        qldu__vgqp = getattr(mtv__rpxq, f'block_{ylul__alrmk}')
        nuvt__aha = ListInstance(context, builder, types.List(lxcx__xnub),
            qldu__vgqp)
        wsbor__pvst = context.get_constant(types.int64, foume__hhgd.
            block_offsets[i])
        nuvt__aha.setitem(wsbor__pvst, pmsds__gajh, sjol__gqz)
    data_tup = context.make_tuple(builder, types.Tuple([foume__hhgd]), [
        mtv__rpxq._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    rnpo__rkjv = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            nbmw__rcque = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*nbmw__rcque)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            yudg__lnogm = builder.extract_value(in_dataframe_payload.data, i)
            pmsds__gajh = context.cast(builder, yudg__lnogm, fromty.data[i],
                toty.data[i])
            sjol__gqz = False
        else:
            pmsds__gajh = builder.extract_value(in_dataframe_payload.data, i)
            sjol__gqz = True
        if sjol__gqz:
            context.nrt.incref(builder, toty.data[i], pmsds__gajh)
        rnpo__rkjv.append(pmsds__gajh)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), rnpo__rkjv)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    voonn__pkml = fromty.table_type
    sxlbk__eyyb = cgutils.create_struct_proxy(voonn__pkml)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    nwkt__fhg = toty.table_type
    wcqu__ijbz = cgutils.create_struct_proxy(nwkt__fhg)(context, builder)
    wcqu__ijbz.parent = in_dataframe_payload.parent
    for lxcx__xnub, ylul__alrmk in nwkt__fhg.type_to_blk.items():
        zlz__vav = context.get_constant(types.int64, len(nwkt__fhg.
            block_to_arr_ind[ylul__alrmk]))
        nugi__stn, dfl__khks = ListInstance.allocate_ex(context, builder,
            types.List(lxcx__xnub), zlz__vav)
        dfl__khks.size = zlz__vav
        setattr(wcqu__ijbz, f'block_{ylul__alrmk}', dfl__khks.value)
    for i in range(len(fromty.data)):
        qdij__ekgoy = fromty.data[i]
        nhxvv__bppuc = toty.data[i]
        if qdij__ekgoy != nhxvv__bppuc:
            nbmw__rcque = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*nbmw__rcque)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        kpn__ljekb = voonn__pkml.type_to_blk[qdij__ekgoy]
        yac__sntc = getattr(sxlbk__eyyb, f'block_{kpn__ljekb}')
        wlqmi__ujp = ListInstance(context, builder, types.List(qdij__ekgoy),
            yac__sntc)
        sqzy__hcd = context.get_constant(types.int64, voonn__pkml.
            block_offsets[i])
        yudg__lnogm = wlqmi__ujp.getitem(sqzy__hcd)
        if qdij__ekgoy != nhxvv__bppuc:
            pmsds__gajh = context.cast(builder, yudg__lnogm, qdij__ekgoy,
                nhxvv__bppuc)
            sjol__gqz = False
        else:
            pmsds__gajh = yudg__lnogm
            sjol__gqz = True
        vxj__prph = nwkt__fhg.type_to_blk[lxcx__xnub]
        dfl__khks = getattr(wcqu__ijbz, f'block_{vxj__prph}')
        ecso__odcks = ListInstance(context, builder, types.List(
            nhxvv__bppuc), dfl__khks)
        tae__oota = context.get_constant(types.int64, nwkt__fhg.
            block_offsets[i])
        ecso__odcks.setitem(tae__oota, pmsds__gajh, sjol__gqz)
    data_tup = context.make_tuple(builder, types.Tuple([nwkt__fhg]), [
        wcqu__ijbz._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    foume__hhgd = fromty.table_type
    mtv__rpxq = cgutils.create_struct_proxy(foume__hhgd)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    rnpo__rkjv = []
    for i, lxcx__xnub in enumerate(toty.data):
        qdij__ekgoy = fromty.data[i]
        if lxcx__xnub != qdij__ekgoy:
            nbmw__rcque = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*nbmw__rcque)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ylul__alrmk = foume__hhgd.type_to_blk[qdij__ekgoy]
        qldu__vgqp = getattr(mtv__rpxq, f'block_{ylul__alrmk}')
        nuvt__aha = ListInstance(context, builder, types.List(qdij__ekgoy),
            qldu__vgqp)
        wsbor__pvst = context.get_constant(types.int64, foume__hhgd.
            block_offsets[i])
        yudg__lnogm = nuvt__aha.getitem(wsbor__pvst)
        if lxcx__xnub != qdij__ekgoy:
            pmsds__gajh = context.cast(builder, yudg__lnogm, qdij__ekgoy,
                lxcx__xnub)
        else:
            pmsds__gajh = yudg__lnogm
            context.nrt.incref(builder, lxcx__xnub, pmsds__gajh)
        rnpo__rkjv.append(pmsds__gajh)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), rnpo__rkjv)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    tmrpk__scez, ozb__hcv, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    kaq__nexfp = ColNamesMetaType(tuple(tmrpk__scez))
    zwjww__ptvs = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    zwjww__ptvs += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(ozb__hcv, index_arg))
    wcjtl__qimh = {}
    exec(zwjww__ptvs, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': kaq__nexfp}, wcjtl__qimh)
    reh__aun = wcjtl__qimh['_init_df']
    return reh__aun


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rikii__iyucf = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(rikii__iyucf, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rikii__iyucf = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(rikii__iyucf, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    rls__ypq = ''
    if not is_overload_none(dtype):
        rls__ypq = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        ooa__vcqt = (len(data.types) - 1) // 2
        osz__nykv = [lxcx__xnub.literal_value for lxcx__xnub in data.types[
            1:ooa__vcqt + 1]]
        data_val_types = dict(zip(osz__nykv, data.types[ooa__vcqt + 1:]))
        rnpo__rkjv = ['data[{}]'.format(i) for i in range(ooa__vcqt + 1, 2 *
            ooa__vcqt + 1)]
        data_dict = dict(zip(osz__nykv, rnpo__rkjv))
        if is_overload_none(index):
            for i, lxcx__xnub in enumerate(data.types[ooa__vcqt + 1:]):
                if isinstance(lxcx__xnub, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(ooa__vcqt + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        furvv__iwt = '.copy()' if copy else ''
        dfaya__raxp = get_overload_const_list(columns)
        ooa__vcqt = len(dfaya__raxp)
        data_val_types = {smype__zrchv: data.copy(ndim=1) for smype__zrchv in
            dfaya__raxp}
        rnpo__rkjv = ['data[:,{}]{}'.format(i, furvv__iwt) for i in range(
            ooa__vcqt)]
        data_dict = dict(zip(dfaya__raxp, rnpo__rkjv))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    ozb__hcv = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[smype__zrchv], df_len, rls__ypq) for smype__zrchv in
        col_names))
    if len(col_names) == 0:
        ozb__hcv = '()'
    return col_names, ozb__hcv, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for smype__zrchv in col_names:
        if smype__zrchv in data_dict and is_iterable_type(data_val_types[
            smype__zrchv]):
            df_len = 'len({})'.format(data_dict[smype__zrchv])
            break
    if df_len == '0':
        if not index_is_none:
            df_len = f'len({index_arg})'
        elif data_dict:
            raise BodoError(
                'Internal Error: Unable to determine length of DataFrame Index. If this is unexpected, please try passing an index value.'
                )
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(smype__zrchv in data_dict for smype__zrchv in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    zrr__afl = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for smype__zrchv in col_names:
        if smype__zrchv not in data_dict:
            data_dict[smype__zrchv] = zrr__afl


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            lxcx__xnub = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(lxcx__xnub)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        zsm__yyoig = idx.literal_value
        if isinstance(zsm__yyoig, int):
            xvllf__fak = tup.types[zsm__yyoig]
        elif isinstance(zsm__yyoig, slice):
            xvllf__fak = types.BaseTuple.from_types(tup.types[zsm__yyoig])
        return signature(xvllf__fak, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    own__vzw, idx = sig.args
    idx = idx.literal_value
    tup, nugi__stn = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(own__vzw)
        if not 0 <= idx < len(own__vzw):
            raise IndexError('cannot index at %d in %s' % (idx, own__vzw))
        csq__zoj = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        fmet__zaov = cgutils.unpack_tuple(builder, tup)[idx]
        csq__zoj = context.make_tuple(builder, sig.return_type, fmet__zaov)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, csq__zoj)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, uub__nuo, suffix_x, suffix_y,
            is_join, indicator, nugi__stn, nugi__stn) = args
        how = get_overload_const_str(uub__nuo)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            rsc__zxg = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(rsc__zxg, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        dlbla__zic = {smype__zrchv: i for i, smype__zrchv in enumerate(left_on)
            }
        avg__oknn = {smype__zrchv: i for i, smype__zrchv in enumerate(right_on)
            }
        xymmf__hhrug = set(left_on) & set(right_on)
        ufyt__kyt = set(left_df.columns) & set(right_df.columns)
        gvbm__mgo = ufyt__kyt - xymmf__hhrug
        loja__nmial = '$_bodo_index_' in left_on
        gpl__uzsut = '$_bodo_index_' in right_on
        bir__dtzmt = how in {'left', 'outer'}
        bagwc__tyu = how in {'right', 'outer'}
        columns = []
        data = []
        if loja__nmial or gpl__uzsut:
            if loja__nmial:
                oxe__adn = bodo.utils.typing.get_index_data_arr_types(left_df
                    .index)[0]
            else:
                oxe__adn = left_df.data[left_df.column_index[left_on[0]]]
            if gpl__uzsut:
                fahuz__dqcaf = bodo.utils.typing.get_index_data_arr_types(
                    right_df.index)[0]
            else:
                fahuz__dqcaf = right_df.data[right_df.column_index[right_on[0]]
                    ]
        if loja__nmial and not gpl__uzsut and not is_join.literal_value:
            ewvp__iee = right_on[0]
            if ewvp__iee in left_df.column_index:
                columns.append(ewvp__iee)
                if (fahuz__dqcaf == bodo.dict_str_arr_type and oxe__adn ==
                    bodo.string_array_type):
                    pzb__hux = bodo.string_array_type
                else:
                    pzb__hux = fahuz__dqcaf
                data.append(pzb__hux)
        if gpl__uzsut and not loja__nmial and not is_join.literal_value:
            uidmf__eyq = left_on[0]
            if uidmf__eyq in right_df.column_index:
                columns.append(uidmf__eyq)
                if (oxe__adn == bodo.dict_str_arr_type and fahuz__dqcaf ==
                    bodo.string_array_type):
                    pzb__hux = bodo.string_array_type
                else:
                    pzb__hux = oxe__adn
                data.append(pzb__hux)
        for qdij__ekgoy, vpdjl__cva in zip(left_df.data, left_df.columns):
            columns.append(str(vpdjl__cva) + suffix_x.literal_value if 
                vpdjl__cva in gvbm__mgo else vpdjl__cva)
            if vpdjl__cva in xymmf__hhrug:
                if qdij__ekgoy == bodo.dict_str_arr_type:
                    qdij__ekgoy = right_df.data[right_df.column_index[
                        vpdjl__cva]]
                data.append(qdij__ekgoy)
            else:
                if (qdij__ekgoy == bodo.dict_str_arr_type and vpdjl__cva in
                    dlbla__zic):
                    if gpl__uzsut:
                        qdij__ekgoy = fahuz__dqcaf
                    else:
                        xiu__pjm = dlbla__zic[vpdjl__cva]
                        deru__ppp = right_on[xiu__pjm]
                        qdij__ekgoy = right_df.data[right_df.column_index[
                            deru__ppp]]
                if bagwc__tyu:
                    qdij__ekgoy = to_nullable_type(qdij__ekgoy)
                data.append(qdij__ekgoy)
        for qdij__ekgoy, vpdjl__cva in zip(right_df.data, right_df.columns):
            if vpdjl__cva not in xymmf__hhrug:
                columns.append(str(vpdjl__cva) + suffix_y.literal_value if 
                    vpdjl__cva in gvbm__mgo else vpdjl__cva)
                if (qdij__ekgoy == bodo.dict_str_arr_type and vpdjl__cva in
                    avg__oknn):
                    if loja__nmial:
                        qdij__ekgoy = oxe__adn
                    else:
                        xiu__pjm = avg__oknn[vpdjl__cva]
                        vtje__uuy = left_on[xiu__pjm]
                        qdij__ekgoy = left_df.data[left_df.column_index[
                            vtje__uuy]]
                if bir__dtzmt:
                    qdij__ekgoy = to_nullable_type(qdij__ekgoy)
                data.append(qdij__ekgoy)
        igpww__cva = get_overload_const_bool(indicator)
        if igpww__cva:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        xzul__ibkdq = False
        if loja__nmial and gpl__uzsut and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            xzul__ibkdq = True
        elif loja__nmial and not gpl__uzsut:
            index_typ = right_df.index
            xzul__ibkdq = True
        elif gpl__uzsut and not loja__nmial:
            index_typ = left_df.index
            xzul__ibkdq = True
        if xzul__ibkdq and isinstance(index_typ, bodo.hiframes.pd_index_ext
            .RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        rsc__zxg = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(rsc__zxg, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    pzok__ufzky = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return pzok__ufzky._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    vuaby__dbn = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    gxd__mjjsv = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', vuaby__dbn, gxd__mjjsv,
        package_name='pandas', module_name='General')
    zwjww__ptvs = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        trxq__aeslr = 0
        ozb__hcv = []
        names = []
        for i, nha__ljpm in enumerate(objs.types):
            assert isinstance(nha__ljpm, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(nha__ljpm, 'pandas.concat()')
            if isinstance(nha__ljpm, SeriesType):
                names.append(str(trxq__aeslr))
                trxq__aeslr += 1
                ozb__hcv.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(nha__ljpm.columns)
                for mbb__qnbt in range(len(nha__ljpm.data)):
                    ozb__hcv.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, mbb__qnbt))
        return bodo.hiframes.dataframe_impl._gen_init_df(zwjww__ptvs, names,
            ', '.join(ozb__hcv), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(lxcx__xnub, DataFrameType) for lxcx__xnub in
            objs.types)
        wjyef__bxir = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            wjyef__bxir.extend(df.columns)
        wjyef__bxir = list(dict.fromkeys(wjyef__bxir).keys())
        dwx__pror = {}
        for trxq__aeslr, smype__zrchv in enumerate(wjyef__bxir):
            for i, df in enumerate(objs.types):
                if smype__zrchv in df.column_index:
                    dwx__pror[f'arr_typ{trxq__aeslr}'] = df.data[df.
                        column_index[smype__zrchv]]
                    break
        assert len(dwx__pror) == len(wjyef__bxir)
        sqele__pmqnr = []
        for trxq__aeslr, smype__zrchv in enumerate(wjyef__bxir):
            args = []
            for i, df in enumerate(objs.types):
                if smype__zrchv in df.column_index:
                    pyg__lfnbw = df.column_index[smype__zrchv]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, pyg__lfnbw))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, trxq__aeslr))
            zwjww__ptvs += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(trxq__aeslr, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(zwjww__ptvs,
            wjyef__bxir, ', '.join('A{}'.format(i) for i in range(len(
            wjyef__bxir))), index, dwx__pror)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(lxcx__xnub, SeriesType) for lxcx__xnub in
            objs.types)
        zwjww__ptvs += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            zwjww__ptvs += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zwjww__ptvs += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        zwjww__ptvs += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        wcjtl__qimh = {}
        exec(zwjww__ptvs, {'bodo': bodo, 'np': np, 'numba': numba}, wcjtl__qimh
            )
        return wcjtl__qimh['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for trxq__aeslr, smype__zrchv in enumerate(df_type.columns):
            zwjww__ptvs += '  arrs{} = []\n'.format(trxq__aeslr)
            zwjww__ptvs += '  for i in range(len(objs)):\n'
            zwjww__ptvs += '    df = objs[i]\n'
            zwjww__ptvs += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(trxq__aeslr))
            zwjww__ptvs += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(trxq__aeslr))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            zwjww__ptvs += '  arrs_index = []\n'
            zwjww__ptvs += '  for i in range(len(objs)):\n'
            zwjww__ptvs += '    df = objs[i]\n'
            zwjww__ptvs += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(zwjww__ptvs,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        zwjww__ptvs += '  arrs = []\n'
        zwjww__ptvs += '  for i in range(len(objs)):\n'
        zwjww__ptvs += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        zwjww__ptvs += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            zwjww__ptvs += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zwjww__ptvs += '  arrs_index = []\n'
            zwjww__ptvs += '  for i in range(len(objs)):\n'
            zwjww__ptvs += '    S = objs[i]\n'
            zwjww__ptvs += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            zwjww__ptvs += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        zwjww__ptvs += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        wcjtl__qimh = {}
        exec(zwjww__ptvs, {'bodo': bodo, 'np': np, 'numba': numba}, wcjtl__qimh
            )
        return wcjtl__qimh['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position,
    _bodo_chunk_bounds):
    pass


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df = args[0]
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        rikii__iyucf = df.copy(index=index)
        return signature(rikii__iyucf, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    ssqol__vhu = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ssqol__vhu._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    vuaby__dbn = dict(index=index, name=name)
    gxd__mjjsv = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', vuaby__dbn, gxd__mjjsv,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        dwx__pror = (types.Array(types.int64, 1, 'C'),) + df.data
        hnrn__hbofz = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, dwx__pror)
        return signature(hnrn__hbofz, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    ssqol__vhu = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ssqol__vhu._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    ssqol__vhu = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ssqol__vhu._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    ssqol__vhu = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return ssqol__vhu._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    ejdeg__jbum = get_overload_const_bool(check_duplicates)
    rcr__jxekq = not get_overload_const_bool(is_already_shuffled)
    yecew__zoqm = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    lkmo__bghw = len(value_names) > 1
    ywsax__pme = None
    gjwud__dnhb = None
    rntb__tocgm = None
    kzc__otrl = None
    prfq__qts = isinstance(values_tup, types.UniTuple)
    if prfq__qts:
        kdd__tabi = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        kdd__tabi = [to_str_arr_if_dict_array(to_nullable_type(zgkbh__klf)) for
            zgkbh__klf in values_tup]
    zwjww__ptvs = 'def impl(\n'
    zwjww__ptvs += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    zwjww__ptvs += '):\n'
    zwjww__ptvs += (
        "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n")
    if rcr__jxekq:
        zwjww__ptvs += '    if parallel:\n'
        zwjww__ptvs += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        crzu__fsbu = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        zwjww__ptvs += f'        info_list = [{crzu__fsbu}]\n'
        zwjww__ptvs += (
            '        cpp_table = arr_info_list_to_table(info_list)\n')
        zwjww__ptvs += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        ahsad__tfab = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        jpmui__ndgcz = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        uiimt__fbrf = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        zwjww__ptvs += f'        index_tup = ({ahsad__tfab},)\n'
        zwjww__ptvs += f'        columns_tup = ({jpmui__ndgcz},)\n'
        zwjww__ptvs += f'        values_tup = ({uiimt__fbrf},)\n'
        zwjww__ptvs += '        delete_table(cpp_table)\n'
        zwjww__ptvs += '        delete_table(out_cpp_table)\n'
        zwjww__ptvs += '        ev_shuffle.finalize()\n'
    zwjww__ptvs += '    columns_arr = columns_tup[0]\n'
    if prfq__qts:
        zwjww__ptvs += '    values_arrs = [arr for arr in values_tup]\n'
    zwjww__ptvs += """    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)
"""
    zwjww__ptvs += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    zwjww__ptvs += '        index_tup\n'
    zwjww__ptvs += '    )\n'
    zwjww__ptvs += '    n_rows = len(unique_index_arr_tup[0])\n'
    zwjww__ptvs += '    num_values_arrays = len(values_tup)\n'
    zwjww__ptvs += '    n_unique_pivots = len(pivot_values)\n'
    if prfq__qts:
        zwjww__ptvs += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        zwjww__ptvs += '    n_cols = n_unique_pivots\n'
    zwjww__ptvs += '    col_map = {}\n'
    zwjww__ptvs += '    for i in range(n_unique_pivots):\n'
    zwjww__ptvs += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    zwjww__ptvs += '            raise ValueError(\n'
    zwjww__ptvs += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    zwjww__ptvs += '            )\n'
    zwjww__ptvs += '        col_map[pivot_values[i]] = i\n'
    zwjww__ptvs += '    ev_unique.finalize()\n'
    zwjww__ptvs += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    ryn__knl = False
    for i, uteoo__eutlm in enumerate(kdd__tabi):
        if is_str_arr_type(uteoo__eutlm):
            ryn__knl = True
            zwjww__ptvs += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            zwjww__ptvs += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if ryn__knl:
        if ejdeg__jbum:
            zwjww__ptvs += '    nbytes = (n_rows + 7) >> 3\n'
            zwjww__ptvs += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        zwjww__ptvs += '    for i in range(len(columns_arr)):\n'
        zwjww__ptvs += '        col_name = columns_arr[i]\n'
        zwjww__ptvs += '        pivot_idx = col_map[col_name]\n'
        zwjww__ptvs += '        row_idx = row_vector[i]\n'
        if ejdeg__jbum:
            zwjww__ptvs += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            zwjww__ptvs += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            zwjww__ptvs += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            zwjww__ptvs += '        else:\n'
            zwjww__ptvs += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if prfq__qts:
            zwjww__ptvs += '        for j in range(num_values_arrays):\n'
            zwjww__ptvs += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            zwjww__ptvs += '            len_arr = len_arrs_0[col_idx]\n'
            zwjww__ptvs += '            values_arr = values_arrs[j]\n'
            zwjww__ptvs += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            zwjww__ptvs += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            zwjww__ptvs += '                len_arr[row_idx] = str_val_len\n'
            zwjww__ptvs += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, uteoo__eutlm in enumerate(kdd__tabi):
                if is_str_arr_type(uteoo__eutlm):
                    zwjww__ptvs += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    zwjww__ptvs += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    zwjww__ptvs += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    zwjww__ptvs += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    zwjww__ptvs += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, uteoo__eutlm in enumerate(kdd__tabi):
        if is_str_arr_type(uteoo__eutlm):
            zwjww__ptvs += f'    data_arrs_{i} = [\n'
            zwjww__ptvs += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            zwjww__ptvs += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            zwjww__ptvs += '        )\n'
            zwjww__ptvs += '        for i in range(n_cols)\n'
            zwjww__ptvs += '    ]\n'
            zwjww__ptvs += f'    if tracing.is_tracing():\n'
            zwjww__ptvs += '         for i in range(n_cols):\n'
            zwjww__ptvs += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            zwjww__ptvs += f'    data_arrs_{i} = [\n'
            zwjww__ptvs += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            zwjww__ptvs += '        for _ in range(n_cols)\n'
            zwjww__ptvs += '    ]\n'
    if not ryn__knl and ejdeg__jbum:
        zwjww__ptvs += '    nbytes = (n_rows + 7) >> 3\n'
        zwjww__ptvs += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    zwjww__ptvs += '    ev_alloc.finalize()\n'
    zwjww__ptvs += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    zwjww__ptvs += '    for i in range(len(columns_arr)):\n'
    zwjww__ptvs += '        col_name = columns_arr[i]\n'
    zwjww__ptvs += '        pivot_idx = col_map[col_name]\n'
    zwjww__ptvs += '        row_idx = row_vector[i]\n'
    if not ryn__knl and ejdeg__jbum:
        zwjww__ptvs += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        zwjww__ptvs += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        zwjww__ptvs += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        zwjww__ptvs += '        else:\n'
        zwjww__ptvs += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if prfq__qts:
        zwjww__ptvs += '        for j in range(num_values_arrays):\n'
        zwjww__ptvs += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        zwjww__ptvs += '            col_arr = data_arrs_0[col_idx]\n'
        zwjww__ptvs += '            values_arr = values_arrs[j]\n'
        zwjww__ptvs += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, uteoo__eutlm in enumerate(kdd__tabi):
            zwjww__ptvs += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            zwjww__ptvs += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        zwjww__ptvs += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        ywsax__pme = index_names.meta[0]
    else:
        zwjww__ptvs += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        ywsax__pme = tuple(index_names.meta)
    zwjww__ptvs += f'    if tracing.is_tracing():\n'
    zwjww__ptvs += f'        index_nbytes = index.nbytes\n'
    zwjww__ptvs += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not yecew__zoqm:
        rntb__tocgm = columns_name.meta[0]
        if lkmo__bghw:
            zwjww__ptvs += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            gjwud__dnhb = value_names.meta
            if all(isinstance(smype__zrchv, str) for smype__zrchv in
                gjwud__dnhb):
                gjwud__dnhb = pd.array(gjwud__dnhb, 'string')
            elif all(isinstance(smype__zrchv, int) for smype__zrchv in
                gjwud__dnhb):
                gjwud__dnhb = np.array(gjwud__dnhb, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(gjwud__dnhb.dtype, pd.StringDtype):
                zwjww__ptvs += '    total_chars = 0\n'
                zwjww__ptvs += f'    for i in range({len(value_names)}):\n'
                zwjww__ptvs += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                zwjww__ptvs += '        total_chars += value_name_str_len\n'
                zwjww__ptvs += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                zwjww__ptvs += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                zwjww__ptvs += '    total_chars = 0\n'
                zwjww__ptvs += '    for i in range(len(pivot_values)):\n'
                zwjww__ptvs += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                zwjww__ptvs += '        total_chars += pivot_val_str_len\n'
                zwjww__ptvs += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                zwjww__ptvs += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            zwjww__ptvs += f'    for i in range({len(value_names)}):\n'
            zwjww__ptvs += '        for j in range(len(pivot_values)):\n'
            zwjww__ptvs += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            zwjww__ptvs += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            zwjww__ptvs += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            zwjww__ptvs += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    zwjww__ptvs += '    ev_fill.finalize()\n'
    foume__hhgd = None
    if yecew__zoqm:
        if lkmo__bghw:
            ieiq__stwr = []
            for zjzd__gpcs in _constant_pivot_values.meta:
                for cdzu__jnxbv in value_names.meta:
                    ieiq__stwr.append((zjzd__gpcs, cdzu__jnxbv))
            column_names = tuple(ieiq__stwr)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        kzc__otrl = ColNamesMetaType(column_names)
        eryxu__sgrn = []
        for zgkbh__klf in kdd__tabi:
            eryxu__sgrn.extend([zgkbh__klf] * len(_constant_pivot_values))
        zjwph__iktqa = tuple(eryxu__sgrn)
        foume__hhgd = TableType(zjwph__iktqa)
        zwjww__ptvs += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        zwjww__ptvs += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, zgkbh__klf in enumerate(kdd__tabi):
            zwjww__ptvs += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {foume__hhgd.type_to_blk[zgkbh__klf]})
"""
        zwjww__ptvs += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        zwjww__ptvs += '        (table,), index, columns_typ\n'
        zwjww__ptvs += '    )\n'
    else:
        plb__hprv = ', '.join(f'data_arrs_{i}' for i in range(len(kdd__tabi)))
        zwjww__ptvs += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({plb__hprv},), n_rows)
"""
        zwjww__ptvs += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        zwjww__ptvs += '        (table,), index, column_index\n'
        zwjww__ptvs += '    )\n'
    zwjww__ptvs += '    ev.finalize()\n'
    zwjww__ptvs += '    return result\n'
    wcjtl__qimh = {}
    pyhi__bqa = {f'data_arr_typ_{i}': uteoo__eutlm for i, uteoo__eutlm in
        enumerate(kdd__tabi)}
    sijz__rfht = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        foume__hhgd, 'columns_typ': kzc__otrl, 'index_names_lit':
        ywsax__pme, 'value_names_lit': gjwud__dnhb, 'columns_name_lit':
        rntb__tocgm, **pyhi__bqa, 'tracing': tracing}
    exec(zwjww__ptvs, sijz__rfht, wcjtl__qimh)
    impl = wcjtl__qimh['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    vyjt__ppeio = {}
    vyjt__ppeio['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, ftzos__hfwn in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        jena__kgc = None
        if isinstance(ftzos__hfwn, bodo.DatetimeArrayType):
            zxwbc__nqcwt = 'datetimetz'
            byb__psn = 'datetime64[ns]'
            if isinstance(ftzos__hfwn.tz, int):
                bees__uzn = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(ftzos__hfwn.tz))
            else:
                bees__uzn = pd.DatetimeTZDtype(tz=ftzos__hfwn.tz).tz
            jena__kgc = {'timezone': pa.lib.tzinfo_to_string(bees__uzn)}
        elif isinstance(ftzos__hfwn, types.Array
            ) or ftzos__hfwn == boolean_array:
            zxwbc__nqcwt = byb__psn = ftzos__hfwn.dtype.name
            if byb__psn.startswith('datetime'):
                zxwbc__nqcwt = 'datetime'
        elif is_str_arr_type(ftzos__hfwn):
            zxwbc__nqcwt = 'unicode'
            byb__psn = 'object'
        elif ftzos__hfwn == binary_array_type:
            zxwbc__nqcwt = 'bytes'
            byb__psn = 'object'
        elif isinstance(ftzos__hfwn, DecimalArrayType):
            zxwbc__nqcwt = byb__psn = 'object'
        elif isinstance(ftzos__hfwn, IntegerArrayType):
            chocd__fgjfa = ftzos__hfwn.dtype.name
            if chocd__fgjfa.startswith('int'):
                byb__psn = 'Int' + chocd__fgjfa[3:]
            elif chocd__fgjfa.startswith('uint'):
                byb__psn = 'UInt' + chocd__fgjfa[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, ftzos__hfwn))
            zxwbc__nqcwt = ftzos__hfwn.dtype.name
        elif isinstance(ftzos__hfwn, bodo.FloatingArrayType):
            chocd__fgjfa = ftzos__hfwn.dtype.name
            zxwbc__nqcwt = chocd__fgjfa
            byb__psn = chocd__fgjfa.capitalize()
        elif ftzos__hfwn == datetime_date_array_type:
            zxwbc__nqcwt = 'datetime'
            byb__psn = 'object'
        elif isinstance(ftzos__hfwn, TimeArrayType):
            zxwbc__nqcwt = 'datetime'
            byb__psn = 'object'
        elif isinstance(ftzos__hfwn, (StructArrayType, ArrayItemArrayType)):
            zxwbc__nqcwt = 'object'
            byb__psn = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, ftzos__hfwn))
        hgdnj__rmv = {'name': col_name, 'field_name': col_name,
            'pandas_type': zxwbc__nqcwt, 'numpy_type': byb__psn, 'metadata':
            jena__kgc}
        vyjt__ppeio['columns'].append(hgdnj__rmv)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            phnx__wfdu = '__index_level_0__'
            mbcfq__sig = None
        else:
            phnx__wfdu = '%s'
            mbcfq__sig = '%s'
        vyjt__ppeio['index_columns'] = [phnx__wfdu]
        vyjt__ppeio['columns'].append({'name': mbcfq__sig, 'field_name':
            phnx__wfdu, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        vyjt__ppeio['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        vyjt__ppeio['index_columns'] = []
    vyjt__ppeio['pandas_version'] = pd.__version__
    return vyjt__ppeio


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        mcp__wpsv = []
        for qwxbx__diiqs in partition_cols:
            try:
                idx = df.columns.index(qwxbx__diiqs)
            except ValueError as xrozf__cvs:
                raise BodoError(
                    f'Partition column {qwxbx__diiqs} is not in dataframe')
            mcp__wpsv.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    if not is_overload_none(_bodo_timestamp_tz) and (not
        is_overload_constant_str(_bodo_timestamp_tz) or not
        get_overload_const_str(_bodo_timestamp_tz)):
        raise BodoError(
            'to_parquet(): _bodo_timestamp_tz must be None or a constant string'
            )
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    tiwp__gba = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    evq__zvpg = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not tiwp__gba)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not tiwp__gba or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and tiwp__gba and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        lze__itse = df.runtime_data_types
        scpe__vawl = len(lze__itse)
        jena__kgc = gen_pandas_parquet_metadata([''] * scpe__vawl,
            lze__itse, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        mke__xbw = jena__kgc['columns'][:scpe__vawl]
        jena__kgc['columns'] = jena__kgc['columns'][scpe__vawl:]
        mke__xbw = [json.dumps(kwia__vwjju).replace('""', '{0}') for
            kwia__vwjju in mke__xbw]
        letr__epqv = json.dumps(jena__kgc)
        rge__ffug = '"columns": ['
        hcm__yrcz = letr__epqv.find(rge__ffug)
        if hcm__yrcz == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        zwux__hmvz = hcm__yrcz + len(rge__ffug)
        dwbva__chk = letr__epqv[:zwux__hmvz]
        letr__epqv = letr__epqv[zwux__hmvz:]
        vfgx__glg = len(jena__kgc['columns'])
    else:
        letr__epqv = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and tiwp__gba:
        letr__epqv = letr__epqv.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            letr__epqv = letr__epqv.replace('"%s"', '%s')
    if not df.is_table_format:
        ozb__hcv = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    zwjww__ptvs = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        zwjww__ptvs += '    py_table = get_dataframe_table(df)\n'
        zwjww__ptvs += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        zwjww__ptvs += '    info_list = [{}]\n'.format(ozb__hcv)
        zwjww__ptvs += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        zwjww__ptvs += '    columns_index = get_dataframe_column_names(df)\n'
        zwjww__ptvs += '    names_arr = index_to_array(columns_index)\n'
        zwjww__ptvs += '    col_names = array_to_info(names_arr)\n'
    else:
        zwjww__ptvs += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and evq__zvpg:
        zwjww__ptvs += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        xdx__avzj = True
    else:
        zwjww__ptvs += '    index_col = array_to_info(np.empty(0))\n'
        xdx__avzj = False
    if df.has_runtime_cols:
        zwjww__ptvs += '    columns_lst = []\n'
        zwjww__ptvs += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            zwjww__ptvs += f'    for _ in range(len(py_table.block_{i})):\n'
            zwjww__ptvs += f"""        columns_lst.append({mke__xbw[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            zwjww__ptvs += '        num_cols += 1\n'
        if vfgx__glg:
            zwjww__ptvs += "    columns_lst.append('')\n"
        zwjww__ptvs += '    columns_str = ", ".join(columns_lst)\n'
        zwjww__ptvs += ('    metadata = """' + dwbva__chk +
            '""" + columns_str + """' + letr__epqv + '"""\n')
    else:
        zwjww__ptvs += '    metadata = """' + letr__epqv + '"""\n'
    zwjww__ptvs += '    if compression is None:\n'
    zwjww__ptvs += "        compression = 'none'\n"
    zwjww__ptvs += '    if _bodo_timestamp_tz is None:\n'
    zwjww__ptvs += "        _bodo_timestamp_tz = ''\n"
    zwjww__ptvs += '    if df.index.name is not None:\n'
    zwjww__ptvs += '        name_ptr = df.index.name\n'
    zwjww__ptvs += '    else:\n'
    zwjww__ptvs += "        name_ptr = 'null'\n"
    zwjww__ptvs += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    sqgu__kejyy = None
    if partition_cols:
        sqgu__kejyy = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        oyr__gfvj = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in mcp__wpsv)
        if oyr__gfvj:
            zwjww__ptvs += '    cat_info_list = [{}]\n'.format(oyr__gfvj)
            zwjww__ptvs += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            zwjww__ptvs += '    cat_table = table\n'
        zwjww__ptvs += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        zwjww__ptvs += (
            f'    part_cols_idxs = np.array({mcp__wpsv}, dtype=np.int32)\n')
        zwjww__ptvs += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        zwjww__ptvs += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        zwjww__ptvs += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        zwjww__ptvs += (
            '                            unicode_to_utf8(compression),\n')
        zwjww__ptvs += '                            _is_parallel,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(bucket_region),\n')
        zwjww__ptvs += '                            row_group_size,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        zwjww__ptvs += '    delete_table_decref_arrays(table)\n'
        zwjww__ptvs += '    delete_info_decref_array(index_col)\n'
        zwjww__ptvs += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        zwjww__ptvs += '    delete_info_decref_array(col_names)\n'
        if oyr__gfvj:
            zwjww__ptvs += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        zwjww__ptvs += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zwjww__ptvs += (
            '                            table, col_names, index_col,\n')
        zwjww__ptvs += '                            ' + str(xdx__avzj) + ',\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(metadata),\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(compression),\n')
        zwjww__ptvs += (
            '                            _is_parallel, 1, df.index.start,\n')
        zwjww__ptvs += (
            '                            df.index.stop, df.index.step,\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(name_ptr),\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(bucket_region),\n')
        zwjww__ptvs += '                            row_group_size,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        zwjww__ptvs += '                              False,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        zwjww__ptvs += '                              False)\n'
        zwjww__ptvs += '    delete_table_decref_arrays(table)\n'
        zwjww__ptvs += '    delete_info_decref_array(index_col)\n'
        zwjww__ptvs += '    delete_info_decref_array(col_names)\n'
    else:
        zwjww__ptvs += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zwjww__ptvs += (
            '                            table, col_names, index_col,\n')
        zwjww__ptvs += '                            ' + str(xdx__avzj) + ',\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(metadata),\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(compression),\n')
        zwjww__ptvs += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(name_ptr),\n')
        zwjww__ptvs += (
            '                            unicode_to_utf8(bucket_region),\n')
        zwjww__ptvs += '                            row_group_size,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        zwjww__ptvs += '                              False,\n'
        zwjww__ptvs += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        zwjww__ptvs += '                              False)\n'
        zwjww__ptvs += '    delete_table_decref_arrays(table)\n'
        zwjww__ptvs += '    delete_info_decref_array(index_col)\n'
        zwjww__ptvs += '    delete_info_decref_array(col_names)\n'
    wcjtl__qimh = {}
    if df.has_runtime_cols:
        fvou__rncc = None
    else:
        for vpdjl__cva in df.columns:
            if not isinstance(vpdjl__cva, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        fvou__rncc = pd.array(df.columns)
    exec(zwjww__ptvs, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': fvou__rncc,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': sqgu__kejyy, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, wcjtl__qimh)
    dltd__oos = wcjtl__qimh['df_to_parquet']
    return dltd__oos


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    wxv__ctlhq = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    ejnh__nswqs = 'all_ok'
    hwob__yhc, ggcgt__afcpq = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        ncl__fvpuc = 100
        if chunksize is None:
            jonp__cze = ncl__fvpuc
        else:
            jonp__cze = min(chunksize, ncl__fvpuc)
        if _is_table_create:
            df = df.iloc[:jonp__cze, :]
        else:
            df = df.iloc[jonp__cze:, :]
            if len(df) == 0:
                return ejnh__nswqs
    vscow__qnza = df.columns
    try:
        if hwob__yhc == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            yssxb__cijvb = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            woia__ssmju = bodo.typeof(df)
            blc__jrhx = {}
            for smype__zrchv, ngp__qtaq in zip(woia__ssmju.columns,
                woia__ssmju.data):
                if df[smype__zrchv].dtype == 'object':
                    if ngp__qtaq == datetime_date_array_type:
                        blc__jrhx[smype__zrchv] = sa.types.Date
                    elif ngp__qtaq in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not yssxb__cijvb or 
                        yssxb__cijvb == '0'):
                        blc__jrhx[smype__zrchv] = VARCHAR2(4000)
            dtype = blc__jrhx
        try:
            qsj__ufa = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            qsj__ufa.finalize()
        except Exception as yhfik__akmrd:
            ejnh__nswqs = yhfik__akmrd.args[0]
            if hwob__yhc == 'oracle' and 'ORA-12899' in ejnh__nswqs:
                ejnh__nswqs += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return ejnh__nswqs
    finally:
        df.columns = vscow__qnza
        wxv__ctlhq.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    wxv__ctlhq = tracing.Event('to_sql_exception_guard_encaps', is_parallel
        =_is_parallel)
    with numba.objmode(out='unicode_type'):
        rvgl__ocisv = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        rvgl__ocisv.finalize()
    wxv__ctlhq.finalize()
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _bodo_allow_downcasting=False, _is_parallel=False):
    import warnings
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    df: DataFrameType = df
    assert df.columns is not None and df.data is not None
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )
    from bodo.io.helpers import exception_propagating_thread_type
    from bodo.io.parquet_pio import parquet_write_table_cpp
    from bodo.io.snowflake import snowflake_connector_cursor_python_type
    for vpdjl__cva in df.columns:
        if not isinstance(vpdjl__cva, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    fvou__rncc = pd.array(df.columns)
    zwjww__ptvs = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    zwjww__ptvs += """    if con.startswith('iceberg'):
        con_str = bodo.io.iceberg.format_iceberg_conn_njit(con)
        if schema is None:
            raise ValueError('DataFrame.to_sql(): schema must be provided when writing to an Iceberg table.')
        if chunksize is not None:
            raise ValueError('DataFrame.to_sql(): chunksize not supported for Iceberg tables.')
        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Iceberg tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Iceberg tables.')
"""
    if df.is_table_format:
        zwjww__ptvs += f'        py_table = get_dataframe_table(df)\n'
        zwjww__ptvs += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        ozb__hcv = ', '.join(f'array_to_info(get_dataframe_data(df, {i}))' for
            i in range(len(df.columns)))
        zwjww__ptvs += f'        info_list = [{ozb__hcv}]\n'
        zwjww__ptvs += f'        table = arr_info_list_to_table(info_list)\n'
    zwjww__ptvs += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    zwjww__ptvs += "    elif con.startswith('snowflake'):\n"
    zwjww__ptvs += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    zwjww__ptvs += "        location = ''\n"
    if not is_overload_none(schema):
        zwjww__ptvs += '        location += \'"\' + schema + \'".\'\n'
    zwjww__ptvs += '        location += name\n'
    zwjww__ptvs += '        my_rank = bodo.get_rank()\n'
    zwjww__ptvs += """        with bodo.objmode(
            cursor='snowflake_connector_cursor_type',
            tmp_folder='temporary_directory_type',
            stage_name='unicode_type',
            parquet_path='unicode_type',
            upload_using_snowflake_put='boolean',
            old_creds='DictType(unicode_type, unicode_type)',
            azure_stage_direct_upload='boolean',
            old_core_site='unicode_type',
            old_sas_token='unicode_type',
        ):
            (
                cursor, tmp_folder, stage_name, parquet_path, upload_using_snowflake_put, old_creds, azure_stage_direct_upload, old_core_site, old_sas_token,
            ) = bodo.io.snowflake.connect_and_get_upload_info(con)
"""
    zwjww__ptvs += '        bodo.barrier()\n'
    zwjww__ptvs += '        if azure_stage_direct_upload:\n'
    zwjww__ptvs += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    zwjww__ptvs += '        if chunksize is None:\n'
    zwjww__ptvs += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        zwjww__ptvs += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        kliaw__mmi = ',' if len(df.columns) == 1 else ''
        zwjww__ptvs += f"""            memory_usage = np.array(({data}{kliaw__mmi}), np.int64).sum()
"""
    zwjww__ptvs += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        zwjww__ptvs += (
            '        columns_index = get_dataframe_column_names(df)\n')
        zwjww__ptvs += '        names_arr = index_to_array(columns_index)\n'
        zwjww__ptvs += '        col_names = array_to_info(names_arr)\n'
    else:
        zwjww__ptvs += '        col_names = array_to_info(col_names_arr)\n'
    zwjww__ptvs += '        index_col = array_to_info(np.empty(0))\n'
    zwjww__ptvs += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    zwjww__ptvs += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    zwjww__ptvs += '        upload_threads_in_progress = []\n'
    zwjww__ptvs += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    zwjww__ptvs += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    zwjww__ptvs += '            chunk_path = parquet_path + chunk_name\n'
    zwjww__ptvs += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    zwjww__ptvs += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    zwjww__ptvs += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    zwjww__ptvs += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        zwjww__ptvs += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        zwjww__ptvs += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        limad__lxf = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        zwjww__ptvs += (
            f'            table_chunk = arr_info_list_to_table([{limad__lxf}])     \n'
            )
    zwjww__ptvs += '            ev_to_df_table.finalize()\n'
    zwjww__ptvs += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
            ev_pq_write_cpp.add_attribute('chunk_start', i)
            ev_pq_write_cpp.add_attribute('chunk_end', i + len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_size', len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_path', chunk_path)
            parquet_write_table_cpp(
                unicode_to_utf8(chunk_path),
                table_chunk, col_names, index_col,
                False,
                unicode_to_utf8('null'),
                unicode_to_utf8(bodo.io.snowflake.SF_WRITE_PARQUET_COMPRESSION),
                False,
                0,
                0, 0, 0,
                unicode_to_utf8('null'),
                unicode_to_utf8(bucket_region),
                chunksize,
                unicode_to_utf8('null'),
                True,
                unicode_to_utf8('UTC'),
                True,
            )
            ev_pq_write_cpp.finalize()
            delete_table_decref_arrays(table_chunk)
            if upload_using_snowflake_put:
                with bodo.objmode(upload_thread='types.optional(exception_propagating_thread_type)'):
                    upload_thread = bodo.io.snowflake.do_upload_and_cleanup(
                        cursor, chunk_idx, chunk_path, stage_name,
                    )
                if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
                    upload_threads_in_progress.append(upload_thread)
        delete_info_decref_array(index_col)
        delete_info_decref_array(col_names)
        if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
            with bodo.objmode():
                bodo.io.helpers.join_all_threads(upload_threads_in_progress)
        ev_upload_df.finalize()
"""
    zwjww__ptvs += '        bodo.barrier()\n'
    tspiw__kzb = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    zwjww__ptvs += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {tspiw__kzb},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    zwjww__ptvs += '        if azure_stage_direct_upload:\n'
    zwjww__ptvs += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    zwjww__ptvs += '        ev.finalize()\n'
    zwjww__ptvs += '    else:\n'
    zwjww__ptvs += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    zwjww__ptvs += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    zwjww__ptvs += '        rank = bodo.libs.distributed_api.get_rank()\n'
    zwjww__ptvs += "        err_msg = 'unset'\n"
    zwjww__ptvs += '        if rank != 0:\n'
    zwjww__ptvs += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    zwjww__ptvs += '        elif rank == 0:\n'
    zwjww__ptvs += '            err_msg = to_sql_exception_guard_encaps(\n'
    zwjww__ptvs += """                          df, name, con, schema, if_exists, index, index_label,
"""
    zwjww__ptvs += '                          chunksize, dtype, method,\n'
    zwjww__ptvs += '                          True, _is_parallel,\n'
    zwjww__ptvs += '                      )\n'
    zwjww__ptvs += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    zwjww__ptvs += "        if_exists = 'append'\n"
    zwjww__ptvs += "        if _is_parallel and err_msg == 'all_ok':\n"
    zwjww__ptvs += '            err_msg = to_sql_exception_guard_encaps(\n'
    zwjww__ptvs += """                          df, name, con, schema, if_exists, index, index_label,
"""
    zwjww__ptvs += '                          chunksize, dtype, method,\n'
    zwjww__ptvs += '                          False, _is_parallel,\n'
    zwjww__ptvs += '                      )\n'
    zwjww__ptvs += "        if err_msg != 'all_ok':\n"
    zwjww__ptvs += "            print('err_msg=', err_msg)\n"
    zwjww__ptvs += (
        "            raise ValueError('error in to_sql() operation')\n")
    wcjtl__qimh = {}
    sijz__rfht = globals().copy()
    sijz__rfht.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        fvou__rncc, 'delete_info_decref_array': delete_info_decref_array,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'get_dataframe_column_names': get_dataframe_column_names,
        'get_dataframe_data': get_dataframe_data, 'get_dataframe_table':
        get_dataframe_table, 'index_to_array': index_to_array, 'np': np,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'pyarrow_table_schema': bodo.io.helpers.
        numba_to_pyarrow_schema(df, is_iceberg=True), 'time': time,
        'to_sql_exception_guard_encaps': to_sql_exception_guard_encaps,
        'tracing': tracing, 'unicode_to_utf8': unicode_to_utf8, 'warnings':
        warnings})
    exec(zwjww__ptvs, sijz__rfht, wcjtl__qimh)
    _impl = wcjtl__qimh['df_to_sql']
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=
    None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        uctzv__kdhx = get_overload_const_str(path_or_buf)
        if uctzv__kdhx.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None, _bodo_file_prefix=
            'part-'):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D, _bodo_file_prefix)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None, _bodo_file_prefix='part-'
            ):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        jtgci__bawd = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(jtgci__bawd), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(jtgci__bawd), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    jyirx__aejb = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    lagqn__tlxth = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', jyirx__aejb, lagqn__tlxth,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    zwjww__ptvs = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        loh__uqcj = data.data.dtype.categories
        zwjww__ptvs += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        loh__uqcj = data.dtype.categories
        zwjww__ptvs += '  data_values = data\n'
    ooa__vcqt = len(loh__uqcj)
    zwjww__ptvs += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    zwjww__ptvs += '  numba.parfors.parfor.init_prange()\n'
    zwjww__ptvs += '  n = len(data_values)\n'
    for i in range(ooa__vcqt):
        zwjww__ptvs += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    zwjww__ptvs += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    zwjww__ptvs += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for mbb__qnbt in range(ooa__vcqt):
        zwjww__ptvs += '          data_arr_{}[i] = 0\n'.format(mbb__qnbt)
    zwjww__ptvs += '      else:\n'
    for mvqqt__vamcj in range(ooa__vcqt):
        zwjww__ptvs += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            mvqqt__vamcj)
    ozb__hcv = ', '.join(f'data_arr_{i}' for i in range(ooa__vcqt))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(loh__uqcj[0], np.datetime64):
        loh__uqcj = tuple(pd.Timestamp(smype__zrchv) for smype__zrchv in
            loh__uqcj)
    elif isinstance(loh__uqcj[0], np.timedelta64):
        loh__uqcj = tuple(pd.Timedelta(smype__zrchv) for smype__zrchv in
            loh__uqcj)
    return bodo.hiframes.dataframe_impl._gen_init_df(zwjww__ptvs, loh__uqcj,
        ozb__hcv, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_query, pd.read_gbq, pd.read_stata, pd.ExcelWriter, pd.
    json_normalize, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'round',
    'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix', 'align',
    'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for cybcj__senyf in pd_unsupported:
        ybyx__vjhbd = mod_name + '.' + cybcj__senyf.__name__
        overload(cybcj__senyf, no_unliteral=True)(create_unsupported_overload
            (ybyx__vjhbd))


def _install_dataframe_unsupported():
    for udmm__nqniw in dataframe_unsupported_attrs:
        xvq__iehbs = 'DataFrame.' + udmm__nqniw
        overload_attribute(DataFrameType, udmm__nqniw)(
            create_unsupported_overload(xvq__iehbs))
    for ybyx__vjhbd in dataframe_unsupported:
        xvq__iehbs = 'DataFrame.' + ybyx__vjhbd + '()'
        overload_method(DataFrameType, ybyx__vjhbd)(create_unsupported_overload
            (xvq__iehbs))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
