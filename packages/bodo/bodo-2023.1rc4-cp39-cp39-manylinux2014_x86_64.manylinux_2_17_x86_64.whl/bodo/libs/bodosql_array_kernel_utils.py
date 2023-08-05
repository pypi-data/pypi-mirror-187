"""
Common utilities for all BodoSQL array kernels
"""
import math
import re
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import types
import bodo
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType
from bodo.hiframes.pd_series_ext import is_datetime_date_series_typ, is_timedelta64_series_typ, pd_timedelta_type, pd_timestamp_tz_naive_type
from bodo.utils.typing import is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_number, is_overload_constant_str, is_overload_float, is_overload_int, is_overload_none, raise_bodo_error


def indent_block(text, indentation):
    if text is None:
        return ''
    moo__xax = text.splitlines()[0]
    i = len(moo__xax) - len(moo__xax.lstrip())
    return '\n'.join([(' ' * indentation + pou__rojg[i:]) for pou__rojg in
        text.splitlines()]) + '\n'


def gen_vectorized(arg_names, arg_types, propagate_null, scalar_text,
    out_dtype, arg_string=None, arg_sources=None, array_override=None,
    support_dict_encoding=True, may_cause_duplicate_dict_array_values=False,
    prefix_code=None, suffix_code=None, res_list=False, extra_globals=None,
    alloc_array_scalars=True, synthesize_dict_if_vector=None,
    synthesize_dict_setup_text=None, synthesize_dict_scalar_text=None,
    synthesize_dict_global=False, synthesize_dict_unique=False):
    assert not (res_list and support_dict_encoding
        ), 'Cannot use res_list with support_dict_encoding'
    lilka__jfrl = [bodo.utils.utils.is_array_typ(uti__cip, True) for
        uti__cip in arg_types]
    mwjwl__vjec = not any(lilka__jfrl)
    yxoq__vys = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    szqu__eskad = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        szqu__eskad = True
        for i in range(len(arg_types)):
            if lilka__jfrl[i] and synthesize_dict_if_vector[i] == 'S':
                szqu__eskad = False
            if not lilka__jfrl[i] and synthesize_dict_if_vector[i] == 'V':
                szqu__eskad = False
    qbnp__dcvd = 0
    emv__kgj = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            qbnp__dcvd += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                emv__kgj = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            qbnp__dcvd += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                emv__kgj = i
    jdezf__mtj = support_dict_encoding and qbnp__dcvd == 1 and emv__kgj >= 0
    oxnjm__qzzjz = jdezf__mtj and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    rcpkt__ijw = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for rcnld__xslgc, bwatx__mwm in arg_sources.items():
            rcpkt__ijw += f'   {rcnld__xslgc} = {bwatx__mwm}\n'
    if mwjwl__vjec and array_override == None:
        if yxoq__vys:
            rcpkt__ijw += '   return None'
        else:
            rcpkt__ijw += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                rcpkt__ijw += f'   arg{i} = {arg_names[i]}\n'
            whpaj__kvyhs = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            rcpkt__ijw += indent_block(whpaj__kvyhs, 3)
            rcpkt__ijw += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                rcpkt__ijw += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            nuq__gxm = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if lilka__jfrl[i]:
                    nuq__gxm = f'len({arg_names[i]})'
                    break
        if jdezf__mtj:
            if out_dtype == bodo.string_array_type:
                rcpkt__ijw += (
                    f'   indices = {arg_names[emv__kgj]}._indices.copy()\n')
                rcpkt__ijw += (
                    f'   has_global = {arg_names[emv__kgj]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    rcpkt__ijw += f'   is_dict_unique = False\n'
                else:
                    rcpkt__ijw += f"""   is_dict_unique = {arg_names[emv__kgj]}._has_deduped_local_dictionary
"""
                rcpkt__ijw += (
                    f'   {arg_names[i]} = {arg_names[emv__kgj]}._data\n')
            else:
                rcpkt__ijw += f'   indices = {arg_names[emv__kgj]}._indices\n'
                rcpkt__ijw += (
                    f'   {arg_names[i]} = {arg_names[emv__kgj]}._data\n')
        rcpkt__ijw += f'   n = {nuq__gxm}\n'
        if prefix_code is not None and not yxoq__vys:
            rcpkt__ijw += indent_block(prefix_code, 3)
        if szqu__eskad:
            rcpkt__ijw += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            rcpkt__ijw += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            rcpkt__ijw += '   numba.parfors.parfor.init_prange()\n'
            rcpkt__ijw += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif jdezf__mtj:
            sev__wbbs = 'n' if propagate_null[emv__kgj] else '(n + 1)'
            if not propagate_null[emv__kgj]:
                oosf__gfl = arg_names[emv__kgj]
                rcpkt__ijw += f"""   {oosf__gfl} = bodo.libs.array_kernels.concat([{oosf__gfl}, bodo.libs.array_kernels.gen_na_array(1, {oosf__gfl})])
"""
            if out_dtype == bodo.string_array_type:
                rcpkt__ijw += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({sev__wbbs}, -1)
"""
            else:
                rcpkt__ijw += f"""   res = bodo.utils.utils.alloc_type({sev__wbbs}, out_dtype, (-1,))
"""
            rcpkt__ijw += f'   for i in range({sev__wbbs}):\n'
        elif res_list:
            rcpkt__ijw += '   res = []\n'
            rcpkt__ijw += '   for i in range(n):\n'
        else:
            rcpkt__ijw += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            rcpkt__ijw += '   numba.parfors.parfor.init_prange()\n'
            rcpkt__ijw += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if yxoq__vys:
            rcpkt__ijw += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if lilka__jfrl[i]:
                    if propagate_null[i]:
                        rcpkt__ijw += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        if res_list:
                            rcpkt__ijw += '         res.append(None)\n'
                        else:
                            rcpkt__ijw += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        rcpkt__ijw += '         continue\n'
            for i in range(len(arg_names)):
                if lilka__jfrl[i]:
                    if alloc_array_scalars:
                        rcpkt__ijw += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    rcpkt__ijw += f'      arg{i} = {arg_names[i]}\n'
            if not szqu__eskad:
                rcpkt__ijw += indent_block(scalar_text, 6)
            else:
                rcpkt__ijw += indent_block(synthesize_dict_scalar_text, 6)
        if jdezf__mtj:
            if oxnjm__qzzjz:
                rcpkt__ijw += '   numba.parfors.parfor.init_prange()\n'
                rcpkt__ijw += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                rcpkt__ijw += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                rcpkt__ijw += '         loc = indices[i]\n'
                rcpkt__ijw += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                rcpkt__ijw += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                rcpkt__ijw += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                rcpkt__ijw += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                rcpkt__ijw += '   numba.parfors.parfor.init_prange()\n'
                rcpkt__ijw += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[emv__kgj]:
                    rcpkt__ijw += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    rcpkt__ijw += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    rcpkt__ijw += '         continue\n'
                    rcpkt__ijw += '      loc = indices[i]\n'
                else:
                    rcpkt__ijw += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                rcpkt__ijw += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                rcpkt__ijw += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                rcpkt__ijw += '      else:\n'
                rcpkt__ijw += '         res2[i] = res[loc]\n'
                rcpkt__ijw += '   res = res2\n'
        rcpkt__ijw += indent_block(suffix_code, 3)
        if szqu__eskad:
            rcpkt__ijw += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            rcpkt__ijw += '   return res'
    rvhq__jtj = {}
    eqpqs__vydm = {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        eqpqs__vydm.update(extra_globals)
    exec(rcpkt__ijw, eqpqs__vydm, rvhq__jtj)
    kfaqo__jlohi = rvhq__jtj['impl']
    return kfaqo__jlohi


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        qij__fec = [(f'{arg_names[i]}{[ifsuy__qhpq]}' if ifsuy__qhpq !=
            container_arg else 'None') for ifsuy__qhpq in range(
            container_length)]
        klrzg__vvb = ',' if container_length != 0 else ''
        fsty__zar = f"({', '.join(qij__fec)}{klrzg__vvb})"
        pwmh__opxl = [(f'{arg_names[i]}{[ifsuy__qhpq]}' if ifsuy__qhpq !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{ifsuy__qhpq}])'
            ) for ifsuy__qhpq in range(container_length)]
        nwq__fezx = f"({', '.join(pwmh__opxl)}{klrzg__vvb})"
        pyche__mqt = [(arg_names[ifsuy__qhpq] if ifsuy__qhpq != i else
            fsty__zar) for ifsuy__qhpq in range(len(arg_names))]
        whwb__dahp = [(arg_names[ifsuy__qhpq] if ifsuy__qhpq != i else
            nwq__fezx) for ifsuy__qhpq in range(len(arg_names))]
        rcpkt__ijw = f"def impl({', '.join(arg_names)}):\n"
        rcpkt__ijw += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        rcpkt__ijw += f"      return {func_name}({', '.join(pyche__mqt)})\n"
        rcpkt__ijw += f'   else:\n'
        rcpkt__ijw += f"      return {func_name}({', '.join(whwb__dahp)})\n"
    else:
        qij__fec = [(arg_names[ifsuy__qhpq] if ifsuy__qhpq != i else 'None'
            ) for ifsuy__qhpq in range(len(arg_names))]
        pwmh__opxl = [(arg_names[ifsuy__qhpq] if ifsuy__qhpq != i else
            f'bodo.utils.indexing.unoptional({arg_names[ifsuy__qhpq]})') for
            ifsuy__qhpq in range(len(arg_names))]
        rcpkt__ijw = f"def impl({', '.join(arg_names)}):\n"
        rcpkt__ijw += f'   if {arg_names[i]} is None:\n'
        rcpkt__ijw += f"      return {func_name}({', '.join(qij__fec)})\n"
        rcpkt__ijw += f'   else:\n'
        rcpkt__ijw += f"      return {func_name}({', '.join(pwmh__opxl)})\n"
    rvhq__jtj = {}
    exec(rcpkt__ijw, {'bodo': bodo, 'numba': numba}, rvhq__jtj)
    kfaqo__jlohi = rvhq__jtj['impl']
    return kfaqo__jlohi


def is_valid_int_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Integer) and
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Integer)) and not is_overload_int(arg))


def is_valid_float_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Float) and 
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Float)) and not is_overload_float(arg))


def is_valid_numeric_bool(arg):
    return not (arg != types.none and not isinstance(arg, (types.Integer,
        types.Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ
        (arg, True) and isinstance(arg.dtype, (types.Integer, types.Float,
        types.Boolean))) and not is_overload_constant_number(arg) and not
        is_overload_constant_bool(arg))


def verify_int_arg(arg, f_name, a_name):
    if not is_valid_int_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be an integer, integer column, or null'
            )


def verify_int_float_arg(arg, f_name, a_name):
    if arg != types.none and not isinstance(arg, (types.Integer, types.
        Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ(arg, 
        True) and isinstance(arg.dtype, (types.Integer, types.Float, types.
        Boolean))) and not is_overload_constant_number(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a numeric, numeric column, or null'
            )


def is_valid_string_arg(arg):
    arg = types.unliteral(arg)
    return not (arg not in (types.none, types.unicode_type) and not (bodo.
        utils.utils.is_array_typ(arg, True) and arg.dtype == types.
        unicode_type) and not is_overload_constant_str(arg))


def is_valid_binary_arg(arg):
    return not (arg != bodo.bytes_type and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == bodo.bytes_type) and not
        is_overload_constant_bytes(arg) and not isinstance(arg, types.Bytes))


def is_valid_datetime_or_date_arg(arg):
    return arg == pd_timestamp_tz_naive_type or bodo.utils.utils.is_array_typ(
        arg, True) and (is_datetime_date_series_typ(arg) or isinstance(arg,
        bodo.DatetimeArrayType) or arg.dtype == bodo.datetime64ns)


def is_valid_timedelta_arg(arg):
    return arg == pd_timedelta_type or bodo.utils.utils.is_array_typ(arg, True
        ) and (is_timedelta64_series_typ(arg) or isinstance(arg,
        PDTimeDeltaType) or arg.dtype == bodo.timedelta64ns)


def is_valid_boolean_arg(arg):
    return not (arg != types.boolean and not (bodo.utils.utils.is_array_typ
        (arg, True) and arg.dtype == types.boolean) and not
        is_overload_constant_bool(arg))


def verify_string_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, string column, or null'
            )


def verify_scalar_string_arg(arg, f_name, a_name):
    if arg not in (types.unicode_type, bodo.none) and not isinstance(arg,
        types.StringLiteral):
        raise_bodo_error(f'{f_name} {a_name} argument must be a scalar string')


def verify_binary_arg(arg, f_name, a_name):
    if not is_valid_binary_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be binary data or null')


def verify_string_binary_arg(arg, f_name, a_name):
    iaxk__utq = is_valid_string_arg(arg)
    uyhgf__fcnl = is_valid_binary_arg(arg)
    if iaxk__utq or uyhgf__fcnl:
        return iaxk__utq
    else:
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a binary data, string, string column, or null'
            )


def verify_string_numeric_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg) and not is_valid_numeric_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, integer, float, boolean, string column, integer column, float column, or boolean column'
            )


def verify_boolean_arg(arg, f_name, a_name):
    if arg not in (types.none, types.boolean) and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == types.boolean
        ) and not is_overload_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a boolean, boolean column, or null'
            )


def is_valid_date_arg(arg):
    return arg == bodo.datetime_date_type or bodo.utils.utils.is_array_typ(arg,
        True) and arg.dtype == bodo.datetime_date_type


def is_valid_tz_naive_datetime_arg(arg):
    return arg in (bodo.datetime64ns, bodo.pd_timestamp_tz_naive_type
        ) or bodo.utils.utils.is_array_typ(arg, True
        ) and arg.dtype == bodo.datetime64ns


def is_valid_tz_aware_datetime_arg(arg):
    return isinstance(arg, bodo.PandasTimestampType
        ) and arg.tz is not None or bodo.utils.utils.is_array_typ(arg, True
        ) and isinstance(arg.dtype, bodo.libs.pd_datetime_arr_ext.
        PandasDatetimeTZDtype)


def verify_datetime_arg(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null without a tz'
            )


def verify_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null'
            )


def verify_datetime_arg_require_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a tz-aware datetime, datetime column, or null'
            )


def verify_sql_interval(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_timedelta_arg(arg) or arg ==
        bodo.date_offset_type):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a Timedelta scalar/column, DateOffset, or null'
            )


def get_tz_if_exists(arg):
    if is_valid_tz_aware_datetime_arg(arg):
        if bodo.utils.utils.is_array_typ(arg, True):
            return arg.dtype.tz
        else:
            return arg.tz
    return None


def is_valid_time_arg(arg):
    return isinstance(arg, bodo.TimeType) or bodo.utils.utils.is_array_typ(arg,
        True) and isinstance(arg.dtype, bodo.bodo.TimeType)


def verify_time_or_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_time_arg(arg) or is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a time/datetime, time/datetime column, or null without a tz'
            )


def get_common_broadcasted_type(arg_types, func_name):
    kngyh__fckx = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            kngyh__fckx.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            kngyh__fckx.append(arg_types[i].data)
        else:
            kngyh__fckx.append(arg_types[i])
    if len(kngyh__fckx) == 0:
        return bodo.none
    elif len(kngyh__fckx) == 1:
        if bodo.utils.utils.is_array_typ(kngyh__fckx[0]):
            return bodo.utils.typing.to_nullable_type(kngyh__fckx[0])
        elif kngyh__fckx[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(kngyh__fckx[0]))
    else:
        yoz__dicm = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                yoz__dicm.append(kngyh__fckx[i].dtype)
            elif kngyh__fckx[i] == bodo.none:
                pass
            else:
                yoz__dicm.append(kngyh__fckx[i])
        if len(yoz__dicm) == 0:
            return bodo.none
        bxrql__yldec, lmg__vlxhb = bodo.utils.typing.get_common_scalar_dtype(
            yoz__dicm)
        if not lmg__vlxhb:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(bxrql__yldec))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    dbhzm__vrodb = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            dbhzm__vrodb = len(arg)
            break
    if dbhzm__vrodb == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    obccs__bbt = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            obccs__bbt.append(arg)
        else:
            obccs__bbt.append([arg] * dbhzm__vrodb)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*rirvq__ncem)) for rirvq__ncem in
            zip(*obccs__bbt)])
    else:
        return pd.Series([scalar_fn(*rirvq__ncem) for rirvq__ncem in zip(*
            obccs__bbt)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    anjz__vbx = calculate_block.splitlines()
    byh__kvk = len(anjz__vbx[0]) - len(anjz__vbx[0].lstrip())
    if constant_block != None:
        zqu__puvz = constant_block.splitlines()
        ndzwy__zdgcr = len(zqu__puvz[0]) - len(zqu__puvz[0].lstrip())
    if setup_block != None:
        opd__thee = setup_block.splitlines()
        lbrma__kbrq = len(opd__thee[0]) - len(opd__thee[0].lstrip())
    if enter_block != None:
        vup__irkcs = enter_block.splitlines()
        vsqk__iccp = len(vup__irkcs[0]) - len(vup__irkcs[0].lstrip())
    if exit_block != None:
        xmpea__xfh = exit_block.splitlines()
        gne__wdsw = len(xmpea__xfh[0]) - len(xmpea__xfh[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    mql__xztzt = empty_block.splitlines()
    oos__jspvc = len(mql__xztzt[0]) - len(mql__xztzt[0].lstrip())
    rcpkt__ijw = 'def impl(S, lower_bound, upper_bound):\n'
    rcpkt__ijw += '   n = len(S)\n'
    rcpkt__ijw += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    rcpkt__ijw += '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n'
    rcpkt__ijw += '   if upper_bound < lower_bound:\n'
    rcpkt__ijw += '      for i in range(n):\n'
    rcpkt__ijw += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        rcpkt__ijw += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        rcpkt__ijw += '      if S.count() == 0:\n'
        rcpkt__ijw += '         for i in range(n):\n'
        rcpkt__ijw += '\n'.join([(' ' * 12 + pou__rojg[oos__jspvc:]) for
            pou__rojg in mql__xztzt]) + '\n'
        rcpkt__ijw += '      else:\n'
        rcpkt__ijw += '\n'.join([(' ' * 9 + pou__rojg[ndzwy__zdgcr:]) for
            pou__rojg in zqu__puvz]) + '\n'
        rcpkt__ijw += '         for i in range(n):\n'
        rcpkt__ijw += '            res[i] = constant_value\n'
    rcpkt__ijw += '   else:\n'
    rcpkt__ijw += '      exiting = lower_bound\n'
    rcpkt__ijw += '      entering = upper_bound\n'
    rcpkt__ijw += '      in_window = 0\n'
    if setup_block != None:
        rcpkt__ijw += '\n'.join([(' ' * 6 + pou__rojg[lbrma__kbrq:]) for
            pou__rojg in opd__thee]) + '\n'
    rcpkt__ijw += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    rcpkt__ijw += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    rcpkt__ijw += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            rcpkt__ijw += '            elem = arr[i]\n'
        rcpkt__ijw += '\n'.join([(' ' * 12 + pou__rojg[vsqk__iccp:]) for
            pou__rojg in vup__irkcs]) + '\n'
    rcpkt__ijw += '      for i in range(n):\n'
    rcpkt__ijw += '         if in_window == 0:\n'
    rcpkt__ijw += '\n'.join([(' ' * 12 + pou__rojg[oos__jspvc:]) for
        pou__rojg in mql__xztzt]) + '\n'
    rcpkt__ijw += '         else:\n'
    rcpkt__ijw += '\n'.join([(' ' * 12 + pou__rojg[byh__kvk:]) for
        pou__rojg in anjz__vbx]) + '\n'
    rcpkt__ijw += '         if 0 <= exiting < n:\n'
    rcpkt__ijw += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    rcpkt__ijw += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            rcpkt__ijw += '               elem = arr[exiting]\n'
        rcpkt__ijw += '\n'.join([(' ' * 15 + pou__rojg[gne__wdsw:]) for
            pou__rojg in xmpea__xfh]) + '\n'
    rcpkt__ijw += '         exiting += 1\n'
    rcpkt__ijw += '         entering += 1\n'
    rcpkt__ijw += '         if 0 <= entering < n:\n'
    rcpkt__ijw += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    rcpkt__ijw += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            rcpkt__ijw += '               elem = arr[entering]\n'
        rcpkt__ijw += '\n'.join([(' ' * 15 + pou__rojg[vsqk__iccp:]) for
            pou__rojg in vup__irkcs]) + '\n'
    rcpkt__ijw += '   return res'
    rvhq__jtj = {}
    exec(rcpkt__ijw, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, rvhq__jtj)
    kfaqo__jlohi = rvhq__jtj['impl']
    return kfaqo__jlohi
