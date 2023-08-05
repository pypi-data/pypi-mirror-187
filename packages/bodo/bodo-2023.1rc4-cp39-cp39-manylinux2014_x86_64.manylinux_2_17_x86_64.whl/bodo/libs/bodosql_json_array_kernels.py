"""
Implements BodoSQL array kernels related to JSON utilities
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def parse_json(arg):
    if isinstance(arg, types.optional):
        return bodo.libs.bodosql_array_kernel_utils.unopt_argument(
            'bodo.libs.bodosql_array_kernels.parse_json', ['arg'], 0)

    def impl(arg):
        return parse_json_util(arg)
    return impl


@numba.generated_jit(nopython=True)
def parse_single_json_map(s):

    def impl(s):
        wowti__xjqop = 1
        tedse__qiwv = {}
        waip__vwrxh = ['{']
        tkcb__atcu = ''
        tczhu__yoccs = ''
        tro__tkr = False
        for wwl__uav in s:
            if wowti__xjqop == 1:
                if wwl__uav.isspace():
                    continue
                elif wwl__uav == '{':
                    wowti__xjqop = 2
                else:
                    return None
            elif wowti__xjqop == 2:
                if wwl__uav.isspace():
                    continue
                elif wwl__uav == '"':
                    wowti__xjqop = 3
                elif wwl__uav == '}':
                    wowti__xjqop = 9
                else:
                    return None
            elif wowti__xjqop == 3:
                if tro__tkr:
                    tkcb__atcu += wwl__uav
                    tro__tkr = False
                elif wwl__uav == '"':
                    wowti__xjqop = 4
                elif wwl__uav == '\\':
                    tro__tkr = True
                else:
                    tkcb__atcu += wwl__uav
            elif wowti__xjqop == 4:
                if wwl__uav.isspace():
                    continue
                elif wwl__uav == ':':
                    wowti__xjqop = 5
                else:
                    return None
            elif wowti__xjqop == 5:
                if wwl__uav.isspace():
                    continue
                if wwl__uav in '},]':
                    return None
                else:
                    wowti__xjqop = 7 if wwl__uav == '"' else 6
                    tczhu__yoccs += wwl__uav
                    if wwl__uav in '{[':
                        waip__vwrxh.append(wwl__uav)
            elif wowti__xjqop == 6:
                if wwl__uav.isspace():
                    continue
                if wwl__uav in '{[':
                    tczhu__yoccs += wwl__uav
                    waip__vwrxh.append(wwl__uav)
                elif wwl__uav in '}]':
                    ktxl__wvtqb = '{' if wwl__uav == '}' else '['
                    if len(waip__vwrxh) == 0 or waip__vwrxh[-1] != ktxl__wvtqb:
                        return None
                    elif len(waip__vwrxh) == 1:
                        tedse__qiwv[tkcb__atcu] = tczhu__yoccs
                        tkcb__atcu = ''
                        tczhu__yoccs = ''
                        waip__vwrxh.pop()
                        wowti__xjqop = 9
                    elif len(waip__vwrxh) == 2:
                        tczhu__yoccs += wwl__uav
                        tedse__qiwv[tkcb__atcu] = tczhu__yoccs
                        tkcb__atcu = ''
                        tczhu__yoccs = ''
                        waip__vwrxh.pop()
                        wowti__xjqop = 8
                    else:
                        tczhu__yoccs += wwl__uav
                        waip__vwrxh.pop()
                elif wwl__uav == '"':
                    tczhu__yoccs += wwl__uav
                    wowti__xjqop = 7
                elif wwl__uav == ',':
                    if len(waip__vwrxh) == 1:
                        tedse__qiwv[tkcb__atcu] = tczhu__yoccs
                        tkcb__atcu = ''
                        tczhu__yoccs = ''
                        wowti__xjqop = 2
                    else:
                        tczhu__yoccs += wwl__uav
                else:
                    tczhu__yoccs += wwl__uav
            elif wowti__xjqop == 7:
                if tro__tkr:
                    tczhu__yoccs += wwl__uav
                    tro__tkr = False
                elif wwl__uav == '\\':
                    tro__tkr = True
                elif wwl__uav == '"':
                    tczhu__yoccs += wwl__uav
                    wowti__xjqop = 6
                else:
                    tczhu__yoccs += wwl__uav
            elif wowti__xjqop == 8:
                if wwl__uav.isspace():
                    continue
                elif wwl__uav == ',':
                    wowti__xjqop = 2
                elif wwl__uav == '}':
                    wowti__xjqop = 9
                else:
                    return None
            elif wowti__xjqop == 9:
                if not wwl__uav.isspace():
                    return None
        return tedse__qiwv if wowti__xjqop == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    tsyv__jkd = ['arr']
    lfwr__knk = [arr]
    rhaf__jlz = [False]
    azlk__lxc = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        xzo__qja = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        azlk__lxc += 'res.append(jmap)\n'
        azlk__lxc += 'if jmap is None:\n'
        azlk__lxc += '   lengths[i] = 0\n'
        azlk__lxc += 'else:\n'
        azlk__lxc += '   lengths[i] = len(jmap)\n'
    else:
        xzo__qja = None
        azlk__lxc += 'return jmap'
    ukff__incjn = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    ukff__incjn += 'numba.parfors.parfor.init_prange()\n'
    ukff__incjn += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    ukff__incjn += '   if res[i] is None:\n'
    ukff__incjn += '     bodo.libs.array_kernels.setna(res2, i)\n'
    ukff__incjn += '   else:\n'
    ukff__incjn += '     res2[i] = res[i]\n'
    ukff__incjn += 'res = res2\n'
    cbyfh__qdfyh = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    tacay__sgpr = bodo.utils.typing.to_nullable_type(cbyfh__qdfyh)
    return gen_vectorized(tsyv__jkd, lfwr__knk, rhaf__jlz, azlk__lxc,
        tacay__sgpr, prefix_code=xzo__qja, suffix_code=ukff__incjn,
        res_list=True, support_dict_encoding=False)
