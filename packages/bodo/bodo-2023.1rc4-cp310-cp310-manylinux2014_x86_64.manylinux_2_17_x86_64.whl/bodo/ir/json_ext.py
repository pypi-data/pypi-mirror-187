import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_and_propagate_cpp_exception, check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)


@intrinsic
def json_file_chunk_reader(typingctx, fname_t, lines_t, is_parallel_t,
    nrows_t, compression_t, bucket_region_t, storage_options_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        jee__dvbv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        zyrkj__jxuob = cgutils.get_or_insert_function(builder.module,
            jee__dvbv, name='json_file_chunk_reader')
        qmgkh__ltsj = builder.call(zyrkj__jxuob, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        szih__tlz = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        tpw__rmuvx = context.get_python_api(builder)
        szih__tlz.meminfo = tpw__rmuvx.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), qmgkh__ltsj)
        szih__tlz.pyobj = qmgkh__ltsj
        tpw__rmuvx.decref(qmgkh__ltsj)
        return szih__tlz._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    gdkqt__iuzca = []
    qudlx__rfxq = []
    lhsx__bimbe = []
    for tfgq__pcg, slguh__cjag in enumerate(json_node.out_vars):
        if slguh__cjag.name in lives:
            gdkqt__iuzca.append(json_node.df_colnames[tfgq__pcg])
            qudlx__rfxq.append(json_node.out_vars[tfgq__pcg])
            lhsx__bimbe.append(json_node.out_types[tfgq__pcg])
    json_node.df_colnames = gdkqt__iuzca
    json_node.out_vars = qudlx__rfxq
    json_node.out_types = lhsx__bimbe
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        kee__rmwo = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        yzcve__rder = json_node.loc.strformat()
        bedyl__eqa = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', kee__rmwo,
            yzcve__rder, bedyl__eqa)
        qsj__mpk = [jnw__tnp for tfgq__pcg, jnw__tnp in enumerate(json_node
            .df_colnames) if isinstance(json_node.out_types[tfgq__pcg],
            bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if qsj__mpk:
            hlq__hyav = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', hlq__hyav,
                yzcve__rder, qsj__mpk)
    parallel = False
    if array_dists is not None:
        parallel = True
        for gnnyg__jgme in json_node.out_vars:
            if array_dists[gnnyg__jgme.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                gnnyg__jgme.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    jwess__ivzoo = len(json_node.out_vars)
    mfkx__fpz = ', '.join('arr' + str(tfgq__pcg) for tfgq__pcg in range(
        jwess__ivzoo))
    fia__wobjj = 'def json_impl(fname):\n'
    fia__wobjj += '    ({},) = _json_reader_py(fname)\n'.format(mfkx__fpz)
    rkv__ynu = {}
    exec(fia__wobjj, {}, rkv__ynu)
    yjtpt__hwv = rkv__ynu['json_impl']
    rzsg__zcx = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    bylse__velm = compile_to_numba_ir(yjtpt__hwv, {'_json_reader_py':
        rzsg__zcx}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(bylse__velm, [json_node.file_name])
    qulq__qasf = bylse__velm.body[:-3]
    for tfgq__pcg in range(len(json_node.out_vars)):
        qulq__qasf[-len(json_node.out_vars) + tfgq__pcg
            ].target = json_node.out_vars[tfgq__pcg]
    return qulq__qasf


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    zjivv__axy = [sanitize_varname(jnw__tnp) for jnw__tnp in col_names]
    bzpj__wvxh = ', '.join(str(tfgq__pcg) for tfgq__pcg, izj__jiwgl in
        enumerate(col_typs) if izj__jiwgl.dtype == types.NPDatetime('ns'))
    vew__umbpy = ', '.join(["{}='{}'".format(rjgf__vuxk, bodo.ir.csv_ext.
        _get_dtype_str(izj__jiwgl)) for rjgf__vuxk, izj__jiwgl in zip(
        zjivv__axy, col_typs)])
    vky__npm = ', '.join(["'{}':{}".format(tfhl__xzlj, bodo.ir.csv_ext.
        _get_pd_dtype_str(izj__jiwgl)) for tfhl__xzlj, izj__jiwgl in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    fia__wobjj = 'def json_reader_py(fname):\n'
    fia__wobjj += '  df_typeref_2 = df_typeref\n'
    fia__wobjj += '  check_java_installation(fname)\n'
    fia__wobjj += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    fia__wobjj += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    fia__wobjj += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    fia__wobjj += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    fia__wobjj += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    fia__wobjj += "      raise FileNotFoundError('File does not exist')\n"
    fia__wobjj += f'  with objmode({vew__umbpy}):\n'
    fia__wobjj += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    fia__wobjj += f'       convert_dates = {convert_dates}, \n'
    fia__wobjj += f'       precise_float={precise_float}, \n'
    fia__wobjj += f'       lines={lines}, \n'
    fia__wobjj += '       dtype={{{}}},\n'.format(vky__npm)
    fia__wobjj += '       )\n'
    fia__wobjj += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for rjgf__vuxk, tfhl__xzlj in zip(zjivv__axy, col_names):
        fia__wobjj += '    if len(df) > 0:\n'
        fia__wobjj += "        {} = df['{}'].values\n".format(rjgf__vuxk,
            tfhl__xzlj)
        fia__wobjj += '    else:\n'
        fia__wobjj += '        {} = np.array([])\n'.format(rjgf__vuxk)
    fia__wobjj += '  return ({},)\n'.format(', '.join(nty__icjb for
        nty__icjb in zjivv__axy))
    igt__nfcyp = globals()
    igt__nfcyp.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    rkv__ynu = {}
    exec(fia__wobjj, igt__nfcyp, rkv__ynu)
    rzsg__zcx = rkv__ynu['json_reader_py']
    ujbx__buc = numba.njit(rzsg__zcx)
    compiled_funcs.append(ujbx__buc)
    return ujbx__buc
