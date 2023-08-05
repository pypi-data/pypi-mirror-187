"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            kwd__flcdd = idx
            zlwn__ncugy = df.data
            nknx__ufp = df.columns
            nsu__pco = self.replace_range_with_numeric_idx_if_needed(df,
                kwd__flcdd)
            rgvol__dusf = DataFrameType(zlwn__ncugy, nsu__pco, nknx__ufp,
                is_table_format=df.is_table_format)
            return rgvol__dusf(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            adz__nbeb = idx.types[0]
            chlxw__kodcx = idx.types[1]
            if isinstance(adz__nbeb, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(chlxw__kodcx):
                    sagm__kzs = get_overload_const_str(chlxw__kodcx)
                    if sagm__kzs not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, sagm__kzs))
                    zxzzj__mtvo = df.columns.index(sagm__kzs)
                    return df.data[zxzzj__mtvo].dtype(*args)
                if isinstance(chlxw__kodcx, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(adz__nbeb
                ) and adz__nbeb.dtype == types.bool_ or isinstance(adz__nbeb,
                types.SliceType):
                nsu__pco = self.replace_range_with_numeric_idx_if_needed(df,
                    adz__nbeb)
                if is_overload_constant_str(chlxw__kodcx):
                    tpss__tlu = get_overload_const_str(chlxw__kodcx)
                    if tpss__tlu not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {tpss__tlu}'
                            )
                    zxzzj__mtvo = df.columns.index(tpss__tlu)
                    kjbls__hzeyg = df.data[zxzzj__mtvo]
                    xkjlz__ffwq = kjbls__hzeyg.dtype
                    jffi__lnwjc = types.literal(df.columns[zxzzj__mtvo])
                    rgvol__dusf = bodo.SeriesType(xkjlz__ffwq, kjbls__hzeyg,
                        nsu__pco, jffi__lnwjc)
                    return rgvol__dusf(*args)
                if isinstance(chlxw__kodcx, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(chlxw__kodcx):
                    qti__xpom = get_overload_const_list(chlxw__kodcx)
                    bcln__sfk = types.unliteral(chlxw__kodcx)
                    if bcln__sfk.dtype == types.bool_:
                        if len(df.columns) != len(qti__xpom):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {qti__xpom} has {len(qti__xpom)} values'
                                )
                        ywu__gbey = []
                        ratpw__adi = []
                        for zzrsa__nyg in range(len(qti__xpom)):
                            if qti__xpom[zzrsa__nyg]:
                                ywu__gbey.append(df.columns[zzrsa__nyg])
                                ratpw__adi.append(df.data[zzrsa__nyg])
                        wflja__wkfn = tuple()
                        umlrr__szwf = df.is_table_format and len(ywu__gbey
                            ) > 0 and len(ywu__gbey
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        rgvol__dusf = DataFrameType(tuple(ratpw__adi),
                            nsu__pco, tuple(ywu__gbey), is_table_format=
                            umlrr__szwf)
                        return rgvol__dusf(*args)
                    elif bcln__sfk.dtype == bodo.string_type:
                        wflja__wkfn, ratpw__adi = (
                            get_df_getitem_kept_cols_and_data(df, qti__xpom))
                        umlrr__szwf = df.is_table_format and len(qti__xpom
                            ) > 0 and len(qti__xpom
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        rgvol__dusf = DataFrameType(ratpw__adi, nsu__pco,
                            wflja__wkfn, is_table_format=umlrr__szwf)
                        return rgvol__dusf(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                ywu__gbey = []
                ratpw__adi = []
                for zzrsa__nyg, dmxcm__ylyf in enumerate(df.columns):
                    if dmxcm__ylyf[0] != ind_val:
                        continue
                    ywu__gbey.append(dmxcm__ylyf[1] if len(dmxcm__ylyf) == 
                        2 else dmxcm__ylyf[1:])
                    ratpw__adi.append(df.data[zzrsa__nyg])
                kjbls__hzeyg = tuple(ratpw__adi)
                gyf__edhos = df.index
                kpi__cwo = tuple(ywu__gbey)
                rgvol__dusf = DataFrameType(kjbls__hzeyg, gyf__edhos, kpi__cwo)
                return rgvol__dusf(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                zxzzj__mtvo = df.columns.index(ind_val)
                kjbls__hzeyg = df.data[zxzzj__mtvo]
                xkjlz__ffwq = kjbls__hzeyg.dtype
                gyf__edhos = df.index
                jffi__lnwjc = types.literal(df.columns[zxzzj__mtvo])
                rgvol__dusf = bodo.SeriesType(xkjlz__ffwq, kjbls__hzeyg,
                    gyf__edhos, jffi__lnwjc)
                return rgvol__dusf(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            kjbls__hzeyg = df.data
            gyf__edhos = self.replace_range_with_numeric_idx_if_needed(df, ind)
            kpi__cwo = df.columns
            rgvol__dusf = DataFrameType(kjbls__hzeyg, gyf__edhos, kpi__cwo,
                is_table_format=df.is_table_format)
            return rgvol__dusf(*args)
        elif is_overload_constant_list(ind):
            lzbz__vef = get_overload_const_list(ind)
            kpi__cwo, kjbls__hzeyg = get_df_getitem_kept_cols_and_data(df,
                lzbz__vef)
            gyf__edhos = df.index
            umlrr__szwf = df.is_table_format and len(lzbz__vef) > 0 and len(
                lzbz__vef) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            rgvol__dusf = DataFrameType(kjbls__hzeyg, gyf__edhos, kpi__cwo,
                is_table_format=umlrr__szwf)
            return rgvol__dusf(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        nsu__pco = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return nsu__pco


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for bggmz__jutwf in cols_to_keep_list:
        if bggmz__jutwf not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(bggmz__jutwf, df.columns))
    kpi__cwo = tuple(cols_to_keep_list)
    kjbls__hzeyg = tuple(df.data[df.column_index[zyrsm__lupnu]] for
        zyrsm__lupnu in kpi__cwo)
    return kpi__cwo, kjbls__hzeyg


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            ywu__gbey = []
            ratpw__adi = []
            for zzrsa__nyg, dmxcm__ylyf in enumerate(df.columns):
                if dmxcm__ylyf[0] != ind_val:
                    continue
                ywu__gbey.append(dmxcm__ylyf[1] if len(dmxcm__ylyf) == 2 else
                    dmxcm__ylyf[1:])
                ratpw__adi.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(zzrsa__nyg))
            vraj__viqz = 'def impl(df, ind):\n'
            oxdm__fnd = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz,
                ywu__gbey, ', '.join(ratpw__adi), oxdm__fnd)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        lzbz__vef = get_overload_const_list(ind)
        for bggmz__jutwf in lzbz__vef:
            if bggmz__jutwf not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(bggmz__jutwf, df.columns))
        mpc__wkx = None
        if df.is_table_format and len(lzbz__vef) > 0 and len(lzbz__vef
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            lfgpg__khrn = [df.column_index[bggmz__jutwf] for bggmz__jutwf in
                lzbz__vef]
            mpc__wkx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
                lfgpg__khrn))}
            ratpw__adi = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            ratpw__adi = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bggmz__jutwf]}).copy()'
                 for bggmz__jutwf in lzbz__vef)
        vraj__viqz = 'def impl(df, ind):\n'
        oxdm__fnd = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz,
            lzbz__vef, ratpw__adi, oxdm__fnd, extra_globals=mpc__wkx)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        vraj__viqz = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            vraj__viqz += (
                '  ind = bodo.utils.conversion.coerce_to_array(ind)\n')
        oxdm__fnd = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            ratpw__adi = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            ratpw__adi = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bggmz__jutwf]})[ind]'
                 for bggmz__jutwf in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz, df.
            columns, ratpw__adi, oxdm__fnd)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        zyrsm__lupnu = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(zyrsm__lupnu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        njmzf__dgrj = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, njmzf__dgrj)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dmq__svan, = args
        ejmu__fugm = signature.return_type
        bmymw__pur = cgutils.create_struct_proxy(ejmu__fugm)(context, builder)
        bmymw__pur.obj = dmq__svan
        context.nrt.incref(builder, signature.args[0], dmq__svan)
        return bmymw__pur._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        iota__wvue = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            listg__fesc = get_overload_const_int(idx.types[1])
            if listg__fesc < 0 or listg__fesc >= iota__wvue:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            ecab__qcu = [listg__fesc]
        else:
            is_out_series = False
            ecab__qcu = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= iota__wvue for
                ind in ecab__qcu):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[ecab__qcu])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                listg__fesc = ecab__qcu[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, listg__fesc
                        )[idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    vraj__viqz = 'def impl(I, idx):\n'
    vraj__viqz += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        vraj__viqz += f'  idx_t = {idx}\n'
    else:
        vraj__viqz += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    oxdm__fnd = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    mpc__wkx = None
    if df.is_table_format and not is_out_series:
        lfgpg__khrn = [df.column_index[bggmz__jutwf] for bggmz__jutwf in
            col_names]
        mpc__wkx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            lfgpg__khrn))}
        ratpw__adi = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        ratpw__adi = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bggmz__jutwf]})[idx_t]'
             for bggmz__jutwf in col_names)
    if is_out_series:
        rkn__vvkwx = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        vraj__viqz += f"""  return bodo.hiframes.pd_series_ext.init_series({ratpw__adi}, {oxdm__fnd}, {rkn__vvkwx})
"""
        gvn__gzsc = {}
        exec(vraj__viqz, {'bodo': bodo}, gvn__gzsc)
        return gvn__gzsc['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz, col_names,
        ratpw__adi, oxdm__fnd, extra_globals=mpc__wkx)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    vraj__viqz = 'def impl(I, idx):\n'
    vraj__viqz += '  df = I._obj\n'
    euky__dvgo = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bggmz__jutwf]})[{idx}]'
         for bggmz__jutwf in col_names)
    vraj__viqz += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    vraj__viqz += f"""  return bodo.hiframes.pd_series_ext.init_series(({euky__dvgo},), row_idx, None)
"""
    gvn__gzsc = {}
    exec(vraj__viqz, {'bodo': bodo}, gvn__gzsc)
    impl = gvn__gzsc['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        zyrsm__lupnu = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(zyrsm__lupnu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        njmzf__dgrj = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, njmzf__dgrj)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dmq__svan, = args
        ohvp__flnd = signature.return_type
        yxe__dckl = cgutils.create_struct_proxy(ohvp__flnd)(context, builder)
        yxe__dckl.obj = dmq__svan
        context.nrt.incref(builder, signature.args[0], dmq__svan)
        return yxe__dckl._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        vraj__viqz = 'def impl(I, idx):\n'
        vraj__viqz += '  df = I._obj\n'
        vraj__viqz += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        oxdm__fnd = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            ratpw__adi = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            ratpw__adi = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[bggmz__jutwf]})[idx_t]'
                 for bggmz__jutwf in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz, df.
            columns, ratpw__adi, oxdm__fnd)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        wzyic__odh = idx.types[1]
        if is_overload_constant_str(wzyic__odh):
            nlqx__vakbf = get_overload_const_str(wzyic__odh)
            listg__fesc = df.columns.index(nlqx__vakbf)

            def impl_col_name(I, idx):
                df = I._obj
                oxdm__fnd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                das__fso = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                    , listg__fesc)
                return bodo.hiframes.pd_series_ext.init_series(das__fso,
                    oxdm__fnd, nlqx__vakbf).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(wzyic__odh):
            col_idx_list = get_overload_const_list(wzyic__odh)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(bggmz__jutwf in df.
                column_index for bggmz__jutwf in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    ecab__qcu = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for zzrsa__nyg, yufjw__cqe in enumerate(col_idx_list):
            if yufjw__cqe:
                ecab__qcu.append(zzrsa__nyg)
                col_names.append(df.columns[zzrsa__nyg])
    else:
        col_names = col_idx_list
        ecab__qcu = [df.column_index[bggmz__jutwf] for bggmz__jutwf in
            col_idx_list]
    mpc__wkx = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        mpc__wkx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            ecab__qcu))}
        ratpw__adi = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        ratpw__adi = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in ecab__qcu)
    oxdm__fnd = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    vraj__viqz = 'def impl(I, idx):\n'
    vraj__viqz += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(vraj__viqz, col_names,
        ratpw__adi, oxdm__fnd, extra_globals=mpc__wkx)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        zyrsm__lupnu = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(zyrsm__lupnu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        njmzf__dgrj = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, njmzf__dgrj)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dmq__svan, = args
        hrxbq__aao = signature.return_type
        ttnc__gpdz = cgutils.create_struct_proxy(hrxbq__aao)(context, builder)
        ttnc__gpdz.obj = dmq__svan
        context.nrt.incref(builder, signature.args[0], dmq__svan)
        return ttnc__gpdz._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        listg__fesc = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            das__fso = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                listg__fesc)
            return bodo.utils.conversion.box_if_dt64(das__fso[idx[0]])
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        listg__fesc = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[listg__fesc]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            das__fso = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                listg__fesc)
            das__fso[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    ttnc__gpdz = cgutils.create_struct_proxy(fromty)(context, builder, val)
    lpx__jyzv = context.cast(builder, ttnc__gpdz.obj, fromty.df_type, toty.
        df_type)
    hibnp__ohayp = cgutils.create_struct_proxy(toty)(context, builder)
    hibnp__ohayp.obj = lpx__jyzv
    return hibnp__ohayp._getvalue()
