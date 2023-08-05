"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        iiig__wvr = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(iiig__wvr)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kvw__svhr = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, kvw__svhr)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        byal__fji, = args
        moxbo__pmdbh = signature.return_type
        teyu__wgz = cgutils.create_struct_proxy(moxbo__pmdbh)(context, builder)
        teyu__wgz.obj = byal__fji
        context.nrt.incref(builder, signature.args[0], byal__fji)
        return teyu__wgz._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        mbak__bqvk = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        ofwi__vdzt = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in ofwi__vdzt:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        sqif__nbkel = 'def impl(S_dt):\n'
        sqif__nbkel += '    S = S_dt._obj\n'
        sqif__nbkel += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sqif__nbkel += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sqif__nbkel += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sqif__nbkel += '    numba.parfors.parfor.init_prange()\n'
        sqif__nbkel += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            sqif__nbkel += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            sqif__nbkel += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        sqif__nbkel += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        sqif__nbkel += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        sqif__nbkel += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        sqif__nbkel += '            continue\n'
        if not mbak__bqvk:
            sqif__nbkel += """        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])
"""
            sqif__nbkel += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                sqif__nbkel += '        out_arr[i] = ts.weekday()\n'
            else:
                sqif__nbkel += '        out_arr[i] = ts.' + field + '\n'
        else:
            sqif__nbkel += '        out_arr[i] = arr[i].{}\n'.format(field)
        sqif__nbkel += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        pnul__nnzhx = {}
        exec(sqif__nbkel, {'bodo': bodo, 'numba': numba, 'np': np}, pnul__nnzhx
            )
        impl = pnul__nnzhx['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        cckk__bffnj = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(cckk__bffnj)


_install_date_fields()


def create_date_method_overload(method):
    bgcc__cijar = method in ['day_name', 'month_name']
    if bgcc__cijar:
        sqif__nbkel = 'def overload_method(S_dt, locale=None):\n'
        sqif__nbkel += '    unsupported_args = dict(locale=locale)\n'
        sqif__nbkel += '    arg_defaults = dict(locale=None)\n'
        sqif__nbkel += '    bodo.utils.typing.check_unsupported_args(\n'
        sqif__nbkel += f"        'Series.dt.{method}',\n"
        sqif__nbkel += '        unsupported_args,\n'
        sqif__nbkel += '        arg_defaults,\n'
        sqif__nbkel += "        package_name='pandas',\n"
        sqif__nbkel += "        module_name='Series',\n"
        sqif__nbkel += '    )\n'
    else:
        sqif__nbkel = 'def overload_method(S_dt):\n'
        sqif__nbkel += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    sqif__nbkel += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    sqif__nbkel += '        return\n'
    if bgcc__cijar:
        sqif__nbkel += '    def impl(S_dt, locale=None):\n'
    else:
        sqif__nbkel += '    def impl(S_dt):\n'
    sqif__nbkel += '        S = S_dt._obj\n'
    sqif__nbkel += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    sqif__nbkel += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    sqif__nbkel += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    sqif__nbkel += '        numba.parfors.parfor.init_prange()\n'
    sqif__nbkel += '        n = len(arr)\n'
    if bgcc__cijar:
        sqif__nbkel += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        sqif__nbkel += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    sqif__nbkel += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    sqif__nbkel += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    sqif__nbkel += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    sqif__nbkel += '                continue\n'
    sqif__nbkel += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    sqif__nbkel += f'            method_val = ts.{method}()\n'
    if bgcc__cijar:
        sqif__nbkel += '            out_arr[i] = method_val\n'
    else:
        sqif__nbkel += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    sqif__nbkel += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    sqif__nbkel += '    return impl\n'
    pnul__nnzhx = {}
    exec(sqif__nbkel, {'bodo': bodo, 'numba': numba, 'np': np}, pnul__nnzhx)
    overload_method = pnul__nnzhx['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        cckk__bffnj = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cckk__bffnj)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        skvc__rarro = S_dt._obj
        zvtd__pvz = bodo.hiframes.pd_series_ext.get_series_data(skvc__rarro)
        kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(skvc__rarro)
        iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(skvc__rarro)
        numba.parfors.parfor.init_prange()
        xbue__ail = len(zvtd__pvz)
        loj__zqk = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            xbue__ail)
        for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail):
            zehk__dzxn = zvtd__pvz[ujy__oeq]
            jmow__zhbn = bodo.utils.conversion.box_if_dt64(zehk__dzxn)
            loj__zqk[ujy__oeq] = datetime.date(jmow__zhbn.year, jmow__zhbn.
                month, jmow__zhbn.day)
        return bodo.hiframes.pd_series_ext.init_series(loj__zqk, kmj__xevsu,
            iiig__wvr)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        mbak__bqvk = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            xec__muh = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            uuuh__wawx = 'convert_numpy_timedelta64_to_pd_timedelta'
            dqm__urz = 'np.empty(n, np.int64)'
            jdd__nmxw = attr
        elif attr == 'isocalendar':
            xec__muh = ['year', 'week', 'day']
            if mbak__bqvk:
                uuuh__wawx = None
            else:
                uuuh__wawx = 'convert_datetime64_to_timestamp'
            dqm__urz = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            jdd__nmxw = attr + '()'
        sqif__nbkel = 'def impl(S_dt):\n'
        sqif__nbkel += '    S = S_dt._obj\n'
        sqif__nbkel += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sqif__nbkel += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sqif__nbkel += '    numba.parfors.parfor.init_prange()\n'
        sqif__nbkel += '    n = len(arr)\n'
        for field in xec__muh:
            sqif__nbkel += '    {} = {}\n'.format(field, dqm__urz)
        sqif__nbkel += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        sqif__nbkel += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in xec__muh:
            sqif__nbkel += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        sqif__nbkel += '            continue\n'
        qlg__eclmh = '(' + '[i], '.join(xec__muh) + '[i])'
        if uuuh__wawx:
            etqlx__pzj = f'bodo.hiframes.pd_timestamp_ext.{uuuh__wawx}(arr[i])'
        else:
            etqlx__pzj = 'arr[i]'
        sqif__nbkel += f'        {qlg__eclmh} = {etqlx__pzj}.{jdd__nmxw}\n'
        ylp__jqh = '(' + ', '.join(xec__muh) + ')'
        sqif__nbkel += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(ylp__jqh))
        pnul__nnzhx = {}
        exec(sqif__nbkel, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(xec__muh))}, pnul__nnzhx)
        impl = pnul__nnzhx['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    wyg__pxjgt = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, ixa__mlws in wyg__pxjgt:
        cckk__bffnj = create_series_dt_df_output_overload(attr)
        ixa__mlws(SeriesDatetimePropertiesType, attr, inline='always')(
            cckk__bffnj)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        sqif__nbkel = 'def impl(S_dt):\n'
        sqif__nbkel += '    S = S_dt._obj\n'
        sqif__nbkel += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sqif__nbkel += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sqif__nbkel += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sqif__nbkel += '    numba.parfors.parfor.init_prange()\n'
        sqif__nbkel += '    n = len(A)\n'
        sqif__nbkel += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        sqif__nbkel += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        sqif__nbkel += '        if bodo.libs.array_kernels.isna(A, i):\n'
        sqif__nbkel += '            bodo.libs.array_kernels.setna(B, i)\n'
        sqif__nbkel += '            continue\n'
        sqif__nbkel += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            sqif__nbkel += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            sqif__nbkel += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            sqif__nbkel += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            sqif__nbkel += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        sqif__nbkel += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        pnul__nnzhx = {}
        exec(sqif__nbkel, {'numba': numba, 'np': np, 'bodo': bodo}, pnul__nnzhx
            )
        impl = pnul__nnzhx['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        sqif__nbkel = 'def impl(S_dt):\n'
        sqif__nbkel += '    S = S_dt._obj\n'
        sqif__nbkel += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sqif__nbkel += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sqif__nbkel += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sqif__nbkel += '    numba.parfors.parfor.init_prange()\n'
        sqif__nbkel += '    n = len(A)\n'
        if method == 'total_seconds':
            sqif__nbkel += '    B = np.empty(n, np.float64)\n'
        else:
            sqif__nbkel += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        sqif__nbkel += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        sqif__nbkel += '        if bodo.libs.array_kernels.isna(A, i):\n'
        sqif__nbkel += '            bodo.libs.array_kernels.setna(B, i)\n'
        sqif__nbkel += '            continue\n'
        sqif__nbkel += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            sqif__nbkel += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            sqif__nbkel += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            sqif__nbkel += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            sqif__nbkel += '    return B\n'
        pnul__nnzhx = {}
        exec(sqif__nbkel, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, pnul__nnzhx)
        impl = pnul__nnzhx['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        cckk__bffnj = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(cckk__bffnj)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        cckk__bffnj = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cckk__bffnj)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        skvc__rarro = S_dt._obj
        enl__szyga = bodo.hiframes.pd_series_ext.get_series_data(skvc__rarro)
        kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(skvc__rarro)
        iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(skvc__rarro)
        numba.parfors.parfor.init_prange()
        xbue__ail = len(enl__szyga)
        cqn__honb = bodo.libs.str_arr_ext.pre_alloc_string_array(xbue__ail, -1)
        for pqyzo__tuv in numba.parfors.parfor.internal_prange(xbue__ail):
            if bodo.libs.array_kernels.isna(enl__szyga, pqyzo__tuv):
                bodo.libs.array_kernels.setna(cqn__honb, pqyzo__tuv)
                continue
            cqn__honb[pqyzo__tuv] = bodo.utils.conversion.box_if_dt64(
                enl__szyga[pqyzo__tuv]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(cqn__honb,
            kmj__xevsu, iiig__wvr)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        skvc__rarro = S_dt._obj
        zxsz__qrw = get_series_data(skvc__rarro).tz_convert(tz)
        kmj__xevsu = get_series_index(skvc__rarro)
        iiig__wvr = get_series_name(skvc__rarro)
        return init_series(zxsz__qrw, kmj__xevsu, iiig__wvr)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        bmpn__uro = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        ncjlg__bkwf = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        ecxk__rkj = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', ncjlg__bkwf,
            ecxk__rkj, package_name='pandas', module_name='Series')
        sqif__nbkel = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        sqif__nbkel += '    S = S_dt._obj\n'
        sqif__nbkel += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        sqif__nbkel += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        sqif__nbkel += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        sqif__nbkel += '    numba.parfors.parfor.init_prange()\n'
        sqif__nbkel += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            sqif__nbkel += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif bmpn__uro:
            sqif__nbkel += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            sqif__nbkel += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        sqif__nbkel += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        sqif__nbkel += '        if bodo.libs.array_kernels.isna(A, i):\n'
        sqif__nbkel += '            bodo.libs.array_kernels.setna(B, i)\n'
        sqif__nbkel += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            olzn__pda = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            yeypq__ztizk = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            olzn__pda = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            yeypq__ztizk = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if bmpn__uro:
            sqif__nbkel += f'        B[i] = A[i].{method}(freq)\n'
        else:
            sqif__nbkel += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(yeypq__ztizk, olzn__pda, method))
        sqif__nbkel += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        pnul__nnzhx = {}
        sgt__zgrt = None
        if bmpn__uro:
            sgt__zgrt = S_dt.stype.dtype.tz
        exec(sqif__nbkel, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': sgt__zgrt}, pnul__nnzhx)
        impl = pnul__nnzhx['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    wgzw__rtxi = ['ceil', 'floor', 'round']
    for method in wgzw__rtxi:
        cckk__bffnj = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            cckk__bffnj)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                vysgl__rgsty = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                ofq__owovk = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    vysgl__rgsty)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                qnbjt__rxi = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xwd__vmfvp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qnbjt__rxi)
                xbue__ail = len(ofq__owovk)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    tcel__xftee = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ofq__owovk[ujy__oeq]))
                    aqe__kvka = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xwd__vmfvp[ujy__oeq])
                    if tcel__xftee == npa__jpai or aqe__kvka == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(tcel__xftee, aqe__kvka)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xwd__vmfvp = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, dt64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xwd__vmfvp[ujy__oeq]))
                    if dji__gbsho == npa__jpai or sxye__rylsb == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, sxye__rylsb)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xwd__vmfvp = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, dt64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xwd__vmfvp[ujy__oeq]))
                    if dji__gbsho == npa__jpai or sxye__rylsb == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, sxye__rylsb)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                frr__kec = rhs.value
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    if dji__gbsho == npa__jpai or frr__kec == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, frr__kec)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                frr__kec = lhs.value
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    if frr__kec == npa__jpai or dji__gbsho == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(frr__kec, dji__gbsho)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, dt64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                uhdzf__jav = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uhdzf__jav))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    if dji__gbsho == npa__jpai or sxye__rylsb == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, sxye__rylsb)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, dt64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                uhdzf__jav = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uhdzf__jav))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    dji__gbsho = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    if dji__gbsho == npa__jpai or sxye__rylsb == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, sxye__rylsb)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                ioku__ezkvn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                dji__gbsho = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ioku__ezkvn)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    vtkt__rqu = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zvtd__pvz[ujy__oeq])
                    if vtkt__rqu == npa__jpai or dji__gbsho == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(vtkt__rqu, dji__gbsho)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                ioku__ezkvn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                dji__gbsho = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ioku__ezkvn)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    vtkt__rqu = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zvtd__pvz[ujy__oeq])
                    if dji__gbsho == npa__jpai or vtkt__rqu == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(dji__gbsho, vtkt__rqu)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yvg__zpe = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zvtd__pvz = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yvg__zpe))
                uhdzf__jav = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uhdzf__jav))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    krfpp__gnt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zvtd__pvz[ujy__oeq]))
                    if sxye__rylsb == npa__jpai or krfpp__gnt == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(krfpp__gnt, sxye__rylsb)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yvg__zpe = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zvtd__pvz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                skvc__rarro = np.empty(xbue__ail, timedelta64_dtype)
                npa__jpai = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yvg__zpe))
                uhdzf__jav = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                sxye__rylsb = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uhdzf__jav))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    krfpp__gnt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zvtd__pvz[ujy__oeq]))
                    if sxye__rylsb == npa__jpai or krfpp__gnt == npa__jpai:
                        xute__lejqg = npa__jpai
                    else:
                        xute__lejqg = op(sxye__rylsb, krfpp__gnt)
                    skvc__rarro[ujy__oeq
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        xute__lejqg)
                return bodo.hiframes.pd_series_ext.init_series(skvc__rarro,
                    kmj__xevsu, iiig__wvr)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            cvtvz__acc = True
        else:
            cvtvz__acc = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yvg__zpe = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zvtd__pvz = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yvg__zpe))
                vdmia__bvnd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                aeew__kvx = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(vdmia__bvnd))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    mel__poga = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zvtd__pvz[ujy__oeq]))
                    if mel__poga == npa__jpai or aeew__kvx == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(mel__poga, aeew__kvx)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yvg__zpe = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zvtd__pvz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yvg__zpe))
                ajhz__ingj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                mel__poga = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ajhz__ingj))
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    aeew__kvx = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zvtd__pvz[ujy__oeq]))
                    if mel__poga == npa__jpai or aeew__kvx == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(mel__poga, aeew__kvx)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    mel__poga = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zvtd__pvz[ujy__oeq])
                    if mel__poga == npa__jpai or rhs.value == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(mel__poga, rhs.value)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    aeew__kvx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zvtd__pvz[ujy__oeq])
                    if aeew__kvx == npa__jpai or lhs.value == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(lhs.value, aeew__kvx)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                admb__wzjr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                krc__dus = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    admb__wzjr)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    mel__poga = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zvtd__pvz[ujy__oeq])
                    if mel__poga == npa__jpai or krc__dus == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(mel__poga, krc__dus)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            yvg__zpe = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                jwz__zkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zvtd__pvz = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    jwz__zkn)
                kmj__xevsu = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                iiig__wvr = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                xbue__ail = len(zvtd__pvz)
                loj__zqk = bodo.libs.bool_arr_ext.alloc_bool_array(xbue__ail)
                npa__jpai = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yvg__zpe)
                admb__wzjr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                krc__dus = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    admb__wzjr)
                for ujy__oeq in numba.parfors.parfor.internal_prange(xbue__ail
                    ):
                    ioku__ezkvn = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zvtd__pvz[ujy__oeq]))
                    if ioku__ezkvn == npa__jpai or krc__dus == npa__jpai:
                        xute__lejqg = cvtvz__acc
                    else:
                        xute__lejqg = op(krc__dus, ioku__ezkvn)
                    loj__zqk[ujy__oeq] = xute__lejqg
                return bodo.hiframes.pd_series_ext.init_series(loj__zqk,
                    kmj__xevsu, iiig__wvr)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for ild__utr in series_dt_unsupported_attrs:
        vomik__srre = 'Series.dt.' + ild__utr
        overload_attribute(SeriesDatetimePropertiesType, ild__utr)(
            create_unsupported_overload(vomik__srre))
    for mdrul__mqjqc in series_dt_unsupported_methods:
        vomik__srre = 'Series.dt.' + mdrul__mqjqc
        overload_method(SeriesDatetimePropertiesType, mdrul__mqjqc,
            no_unliteral=True)(create_unsupported_overload(vomik__srre))


_install_series_dt_unsupported()
