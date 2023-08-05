"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            bzrib__xnm = 'Series'
        else:
            bzrib__xnm = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{bzrib__xnm}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pzpxi__olpp = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, pzpxi__olpp)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    fdzrk__mpjfu = dict(win_type=win_type, axis=axis, closed=closed)
    jvi__ixkfp = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', fdzrk__mpjfu, jvi__ixkfp,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    fdzrk__mpjfu = dict(win_type=win_type, axis=axis, closed=closed)
    jvi__ixkfp = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', fdzrk__mpjfu, jvi__ixkfp,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        rdg__zyrm, zkpc__wtuo, ixuvc__cijqi, tkm__zypru, wzxfp__ned = args
        tof__jdzi = signature.return_type
        yzgem__szedo = cgutils.create_struct_proxy(tof__jdzi)(context, builder)
        yzgem__szedo.obj = rdg__zyrm
        yzgem__szedo.window = zkpc__wtuo
        yzgem__szedo.min_periods = ixuvc__cijqi
        yzgem__szedo.center = tkm__zypru
        context.nrt.incref(builder, signature.args[0], rdg__zyrm)
        context.nrt.incref(builder, signature.args[1], zkpc__wtuo)
        context.nrt.incref(builder, signature.args[2], ixuvc__cijqi)
        context.nrt.incref(builder, signature.args[3], tkm__zypru)
        return yzgem__szedo._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    tof__jdzi = RollingType(obj_type, window_type, on, selection, False)
    return tof__jdzi(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    degj__qfygh = not isinstance(rolling.window_type, types.Integer)
    obdw__vwi = 'variable' if degj__qfygh else 'fixed'
    byfb__gaqx = 'None'
    if degj__qfygh:
        byfb__gaqx = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    tvcd__oxcz = []
    derh__mqng = 'on_arr, ' if degj__qfygh else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{obdw__vwi}(bodo.hiframes.pd_series_ext.get_series_data(df), {derh__mqng}index_arr, window, minp, center, func, raw)'
            , byfb__gaqx, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    woe__zonld = rolling.obj_type.data
    out_cols = []
    for pzaki__smi in rolling.selection:
        vabq__vwtok = rolling.obj_type.columns.index(pzaki__smi)
        if pzaki__smi == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            slv__ovq = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {vabq__vwtok})'
                )
            out_cols.append(pzaki__smi)
        else:
            if not isinstance(woe__zonld[vabq__vwtok].dtype, (types.Boolean,
                types.Number)):
                continue
            slv__ovq = (
                f'bodo.hiframes.rolling.rolling_{obdw__vwi}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {vabq__vwtok}), {derh__mqng}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(pzaki__smi)
        tvcd__oxcz.append(slv__ovq)
    return ', '.join(tvcd__oxcz), byfb__gaqx, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    fdzrk__mpjfu = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    jvi__ixkfp = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', fdzrk__mpjfu, jvi__ixkfp,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    fdzrk__mpjfu = dict(win_type=win_type, axis=axis, closed=closed, method
        =method)
    jvi__ixkfp = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', fdzrk__mpjfu, jvi__ixkfp,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        acn__hpxz = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        rvrht__ewah = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{essz__cagav}'" if
                isinstance(essz__cagav, str) else f'{essz__cagav}' for
                essz__cagav in rolling.selection if essz__cagav != rolling.on))
        axthe__mhq = bnhq__mfq = ''
        if fname == 'apply':
            axthe__mhq = 'func, raw, args, kwargs'
            bnhq__mfq = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            axthe__mhq = bnhq__mfq = 'other, pairwise'
        if fname == 'cov':
            axthe__mhq = bnhq__mfq = 'other, pairwise, ddof'
        haczm__foml = (
            f'lambda df, window, minp, center, {axthe__mhq}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {rvrht__ewah}){selection}.{fname}({bnhq__mfq})'
            )
        acn__hpxz += f"""  return rolling.obj.apply({haczm__foml}, rolling.window, rolling.min_periods, rolling.center, {axthe__mhq})
"""
        gea__cvp = {}
        exec(acn__hpxz, {'bodo': bodo}, gea__cvp)
        impl = gea__cvp['impl']
        return impl
    lwa__vdglt = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if lwa__vdglt else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if lwa__vdglt else rolling.obj_type.columns
        other_cols = None if lwa__vdglt else other.columns
        tvcd__oxcz, byfb__gaqx = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        tvcd__oxcz, byfb__gaqx, out_cols = _gen_df_rolling_out_data(rolling)
    uev__uft = lwa__vdglt or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    xua__rzjt = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    xua__rzjt += '  df = rolling.obj\n'
    xua__rzjt += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if lwa__vdglt else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    bzrib__xnm = 'None'
    if lwa__vdglt:
        bzrib__xnm = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif uev__uft:
        pzaki__smi = (set(out_cols) - set([rolling.on])).pop()
        bzrib__xnm = f"'{pzaki__smi}'" if isinstance(pzaki__smi, str) else str(
            pzaki__smi)
    xua__rzjt += f'  name = {bzrib__xnm}\n'
    xua__rzjt += '  window = rolling.window\n'
    xua__rzjt += '  center = rolling.center\n'
    xua__rzjt += '  minp = rolling.min_periods\n'
    xua__rzjt += f'  on_arr = {byfb__gaqx}\n'
    if fname == 'apply':
        xua__rzjt += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        xua__rzjt += f"  func = '{fname}'\n"
        xua__rzjt += f'  index_arr = None\n'
        xua__rzjt += f'  raw = False\n'
    if uev__uft:
        xua__rzjt += (
            f'  return bodo.hiframes.pd_series_ext.init_series({tvcd__oxcz}, index, name)'
            )
        gea__cvp = {}
        reen__bhxmv = {'bodo': bodo}
        exec(xua__rzjt, reen__bhxmv, gea__cvp)
        impl = gea__cvp['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(xua__rzjt, out_cols,
        tvcd__oxcz)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        ouryx__ssnu = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(ouryx__ssnu)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    sedt__escuo = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(sedt__escuo) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    degj__qfygh = not isinstance(window_type, types.Integer)
    byfb__gaqx = 'None'
    if degj__qfygh:
        byfb__gaqx = 'bodo.utils.conversion.index_to_array(index)'
    derh__mqng = 'on_arr, ' if degj__qfygh else ''
    tvcd__oxcz = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {derh__mqng}window, minp, center)'
            , byfb__gaqx)
    for pzaki__smi in out_cols:
        if pzaki__smi in df_cols and pzaki__smi in other_cols:
            acps__esmy = df_cols.index(pzaki__smi)
            hbp__clp = other_cols.index(pzaki__smi)
            slv__ovq = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {acps__esmy}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {hbp__clp}), {derh__mqng}window, minp, center)'
                )
        else:
            slv__ovq = 'np.full(len(df), np.nan)'
        tvcd__oxcz.append(slv__ovq)
    return ', '.join(tvcd__oxcz), byfb__gaqx


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    rjvq__dvbi = {'pairwise': pairwise, 'ddof': ddof}
    rykqy__hws = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        rjvq__dvbi, rykqy__hws, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    rjvq__dvbi = {'ddof': ddof, 'pairwise': pairwise}
    rykqy__hws = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        rjvq__dvbi, rykqy__hws, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, eng__kunpw = args
        if isinstance(rolling, RollingType):
            sedt__escuo = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(eng__kunpw, (tuple, list)):
                if len(set(eng__kunpw).difference(set(sedt__escuo))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(eng__kunpw).difference(set(sedt__escuo))))
                selection = list(eng__kunpw)
            else:
                if eng__kunpw not in sedt__escuo:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(eng__kunpw))
                selection = [eng__kunpw]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            atylx__yux = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(atylx__yux, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        sedt__escuo = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            sedt__escuo = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            sedt__escuo = rolling.obj_type.columns
        if attr in sedt__escuo:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    soo__kjt = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    woe__zonld = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in soo__kjt):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        jgvc__zru = woe__zonld[soo__kjt.index(get_literal_value(on))]
        if not isinstance(jgvc__zru, types.Array
            ) or jgvc__zru.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(rfgr__lano.dtype, (types.Boolean, types.Number)) for
        rfgr__lano in woe__zonld):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
