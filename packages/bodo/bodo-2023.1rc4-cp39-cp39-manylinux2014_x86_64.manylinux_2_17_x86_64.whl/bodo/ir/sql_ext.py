"""
Implementation of pd.read_sql in Bodo.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from typing import Any, List, Optional
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.io.helpers import PyArrowTableSchemaType, is_nullable
from bodo.io.parquet_pio import ParquetPredicateType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
if bodo.utils.utils.has_pyarrow():
    import llvmlite.binding as ll
    from bodo.io import arrow_cpp
    ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
    ll.add_symbol('iceberg_pq_read', arrow_cpp.iceberg_pq_read)
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request: str, connection: str, df_out,
        df_colnames, out_vars, out_types, converted_colnames: List[str],
        db_type: str, loc, unsupported_columns: List[str],
        unsupported_arrow_types: List[pa.DataType], is_select_query: bool,
        has_side_effects: bool, index_column_name: str, index_column_type,
        database_schema: Optional[str], pyarrow_schema: Optional[pa.Schema],
        is_merge_into: bool, file_list_type, snapshot_id_type):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.has_side_effects = has_side_effects
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(df_colnames)))
        self.database_schema = database_schema
        self.pyarrow_schema = pyarrow_schema
        self.is_merge_into = is_merge_into
        self.is_live_table = True
        self.file_list_live = is_merge_into
        self.snapshot_id_live = is_merge_into
        if is_merge_into:
            self.file_list_type = file_list_type
            self.snapshot_id_type = snapshot_id_type
        else:
            self.file_list_type = types.none
            self.snapshot_id_type = types.none

    def __repr__(self):
        obgbm__qtphr = tuple(ndzzm__bugk.name for ndzzm__bugk in self.out_vars)
        return (
            f'{obgbm__qtphr} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    txitu__ohlgn = urlparse(con_str)
    db_type = txitu__ohlgn.scheme
    efbwh__vik = txitu__ohlgn.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', efbwh__vik
    if db_type == 'mysql+pymysql':
        return 'mysql', efbwh__vik
    if con_str.startswith('iceberg+glue') or txitu__ohlgn.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', efbwh__vik
    return db_type, efbwh__vik


def remove_iceberg_prefix(con):
    import sys
    if sys.version_info.minor < 9:
        if con.startswith('iceberg+'):
            con = con[len('iceberg+'):]
        if con.startswith('iceberg://'):
            con = con[len('iceberg://'):]
    else:
        con = con.removeprefix('iceberg+').removeprefix('iceberg://')
    return con


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    xhzmv__azysm = sql_node.out_vars[0].name
    mcfgg__xppbw = sql_node.out_vars[1].name
    zqjf__ydsd = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    pfp__zcd = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and xhzmv__azysm not in lives and 
        mcfgg__xppbw not in lives and zqjf__ydsd not in lives and pfp__zcd
         not in lives):
        return None
    if xhzmv__azysm not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if mcfgg__xppbw not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if zqjf__ydsd not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if pfp__zcd not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        ogpm__rgj = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        ybo__ubxxo = []
        dict_encoded_cols = []
        for xwzt__jwa in sql_node.out_used_cols:
            jntv__jca = sql_node.df_colnames[xwzt__jwa]
            ybo__ubxxo.append(jntv__jca)
            if isinstance(sql_node.out_types[xwzt__jwa], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(jntv__jca)
        if sql_node.index_column_name:
            ybo__ubxxo.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        qpn__djifj = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', ogpm__rgj,
            qpn__djifj, ybo__ubxxo)
        if dict_encoded_cols:
            bhyj__irtw = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', bhyj__irtw,
                qpn__djifj, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        axos__afvrv = set(sql_node.unsupported_columns)
        ecb__utnok = set(sql_node.out_used_cols)
        osh__uvdbf = ecb__utnok & axos__afvrv
        if osh__uvdbf:
            esjvb__eaplu = sorted(osh__uvdbf)
            glqpp__uqn = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            euss__gfh = 0
            for fna__bfd in esjvb__eaplu:
                while sql_node.unsupported_columns[euss__gfh] != fna__bfd:
                    euss__gfh += 1
                glqpp__uqn.append(
                    f"Column '{sql_node.original_df_colnames[fna__bfd]}' with unsupported arrow type {sql_node.unsupported_arrow_types[euss__gfh]}"
                    )
                euss__gfh += 1
            kpnr__ruxlc = '\n'.join(glqpp__uqn)
            raise BodoError(kpnr__ruxlc, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    nidni__scovm, nxk__ivtw = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    nonky__dixkd = ', '.join(nidni__scovm.values())
    hrix__mtv = (
        f'def sql_impl(sql_request, conn, database_schema, {nonky__dixkd}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            kdoqr__luq = []
            for msaiz__evq in sql_node.filters:
                kyg__hjpjw = []
                for xzu__vfd in msaiz__evq:
                    tjukw__codn, noq__crak = xzu__vfd[0], xzu__vfd[2]
                    tjukw__codn = convert_col_name(tjukw__codn, sql_node.
                        converted_colnames)
                    tjukw__codn = '\\"' + tjukw__codn + '\\"'
                    dtpxe__dpqo = '{' + nidni__scovm[xzu__vfd[2].name
                        ] + '}' if isinstance(xzu__vfd[2], ir.Var
                        ) else noq__crak
                    if xzu__vfd[1] in ('startswith', 'endswith'):
                        ksylb__lvixu = ['(', xzu__vfd[1], '(', tjukw__codn,
                            ',', dtpxe__dpqo, ')', ')']
                    else:
                        ksylb__lvixu = ['(', tjukw__codn, xzu__vfd[1],
                            dtpxe__dpqo, ')']
                    kyg__hjpjw.append(' '.join(ksylb__lvixu))
                kdoqr__luq.append(' ( ' + ' AND '.join(kyg__hjpjw) + ' ) ')
            jcdc__azcqg = ' WHERE ' + ' OR '.join(kdoqr__luq)
            for xwzt__jwa, mgi__nwtm in enumerate(nidni__scovm.values()):
                hrix__mtv += (
                    f'    {mgi__nwtm} = get_sql_literal({mgi__nwtm})\n')
            hrix__mtv += (
                f'    sql_request = f"{{sql_request}} {jcdc__azcqg}"\n')
        if sql_node.limit != limit:
            hrix__mtv += (
                f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n')
    aayve__moym = ''
    if sql_node.db_type == 'iceberg':
        aayve__moym = nonky__dixkd
    hrix__mtv += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {aayve__moym})
"""
    vouuz__rwaew = {}
    exec(hrix__mtv, {}, vouuz__rwaew)
    llzxl__vmun = vouuz__rwaew['sql_impl']
    kfvsd__mgdf = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.out_used_cols, sql_node.converted_colnames, typingctx,
        targetctx, sql_node.db_type, limit, parallel, typemap, sql_node.
        filters, sql_node.pyarrow_schema, not sql_node.is_live_table,
        sql_node.is_select_query, sql_node.is_merge_into, is_independent)
    kgtw__aooss = (types.none if sql_node.database_schema is None else
        string_type)
    gta__whynn = compile_to_numba_ir(llzxl__vmun, {'_sql_reader_py':
        kfvsd__mgdf, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        kgtw__aooss) + tuple(typemap[ndzzm__bugk.name] for ndzzm__bugk in
        nxk__ivtw), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        vvrjo__cvxwk = [sql_node.df_colnames[xwzt__jwa] for xwzt__jwa in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            vvrjo__cvxwk.append(sql_node.index_column_name)
        if len(vvrjo__cvxwk) == 0:
            gkwm__zoeu = 'COUNT(*)'
        else:
            gkwm__zoeu = escape_column_names(vvrjo__cvxwk, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            hutvu__yovt = ('SELECT ' + gkwm__zoeu + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            hutvu__yovt = ('SELECT ' + gkwm__zoeu + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        hutvu__yovt = sql_node.sql_request
    replace_arg_nodes(gta__whynn, [ir.Const(hutvu__yovt, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + nxk__ivtw)
    gzs__hmxb = gta__whynn.body[:-3]
    if meta_head_only_info:
        gzs__hmxb[-5].target = meta_head_only_info[1]
    gzs__hmxb[-4].target = sql_node.out_vars[0]
    gzs__hmxb[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        gzs__hmxb.pop(-3)
    elif not sql_node.is_live_table:
        gzs__hmxb.pop(-4)
    if sql_node.file_list_live:
        gzs__hmxb[-2].target = sql_node.out_vars[2]
    else:
        gzs__hmxb.pop(-2)
    if sql_node.snapshot_id_live:
        gzs__hmxb[-1].target = sql_node.out_vars[3]
    else:
        gzs__hmxb.pop(-1)
    return gzs__hmxb


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        gkwm__zoeu = ', '.join(escape_col_name(convert_col_name(yctc__uwmbp,
            converted_colnames)) for yctc__uwmbp in col_names)
    elif db_type == 'oracle':
        vvrjo__cvxwk = []
        for yctc__uwmbp in col_names:
            vvrjo__cvxwk.append(convert_col_name(yctc__uwmbp,
                converted_colnames))
        gkwm__zoeu = ', '.join([f'"{yctc__uwmbp}"' for yctc__uwmbp in
            vvrjo__cvxwk])
    elif db_type == 'mysql':
        gkwm__zoeu = ', '.join([f'`{yctc__uwmbp}`' for yctc__uwmbp in
            col_names])
    else:
        gkwm__zoeu = ', '.join([f'"{yctc__uwmbp}"' for yctc__uwmbp in
            col_names])
    return gkwm__zoeu


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    czb__maj = types.unliteral(filter_value)
    if czb__maj == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(czb__maj, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(czb__maj, bodo.PandasTimestampType):
        if czb__maj.tz is None:
            hrf__jtwp = 'TIMESTAMP_NTZ'
        else:
            hrf__jtwp = 'TIMESTAMP_TZ'

        def impl(filter_value):
            yzfi__hjsvb = filter_value.nanosecond
            gbqjm__ysd = ''
            if yzfi__hjsvb < 10:
                gbqjm__ysd = '00'
            elif yzfi__hjsvb < 100:
                gbqjm__ysd = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{gbqjm__ysd}{yzfi__hjsvb}'::{hrf__jtwp}"
                )
        return impl
    elif czb__maj == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {czb__maj} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    ddh__ubj = bodo.datetime_date_type, types.unicode_type, types.bool_
    czb__maj = types.unliteral(filter_value)
    if (isinstance(czb__maj, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        czb__maj in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        boolean_array, bodo.datetime_date_array_type)) and (isinstance(
        czb__maj.dtype, scalar_isinstance) or czb__maj.dtype in ddh__ubj):

        def impl(filter_value):
            mcyre__ijmo = ', '.join([_get_snowflake_sql_literal_scalar(
                yctc__uwmbp) for yctc__uwmbp in filter_value])
            return f'({mcyre__ijmo})'
        return impl
    elif isinstance(czb__maj, scalar_isinstance) or czb__maj in ddh__ubj:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {czb__maj} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.
        df_colnames, require_one_column=sql_node.db_type not in ('iceberg',
        'snowflake'))


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as gljd__kzmb:
        bst__mghs = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(bst__mghs)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as gljd__kzmb:
        bst__mghs = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(bst__mghs)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as gljd__kzmb:
        bst__mghs = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(bst__mghs)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as gljd__kzmb:
        bst__mghs = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(bst__mghs)


def req_limit(sql_request):
    import re
    kbecy__std = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    kzkuz__fkaga = kbecy__std.search(sql_request)
    if kzkuz__fkaga:
        return int(kzkuz__fkaga.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    npvb__qxmpa = next_label()
    vvrjo__cvxwk = [col_names[xwzt__jwa] for xwzt__jwa in out_used_cols]
    exqr__guzsw = [col_typs[xwzt__jwa] for xwzt__jwa in out_used_cols]
    if index_column_name:
        vvrjo__cvxwk.append(index_column_name)
        exqr__guzsw.append(index_column_type)
    qwqap__vosz = None
    jghi__kjs = None
    qtof__hld = types.none if is_dead_table else TableType(tuple(col_typs))
    aayve__moym = ''
    nidni__scovm = {}
    nxk__ivtw = []
    if filters and db_type == 'iceberg':
        nidni__scovm, nxk__ivtw = bodo.ir.connector.generate_filter_map(filters
            )
        aayve__moym = ', '.join(nidni__scovm.values())
    hrix__mtv = (
        f'def sql_reader_py(sql_request, conn, database_schema, {aayve__moym}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        epzr__tng, nwp__rqvhv = bodo.ir.connector.generate_arrow_filters(
            filters, nidni__scovm, nxk__ivtw, col_names, col_names,
            col_typs, typemap, 'iceberg')
        mfxbg__zrks = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            mfxbg__zrks = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[xwzt__jwa]) for xwzt__jwa in out_used_cols if 
            xwzt__jwa != mfxbg__zrks]
        lmema__easq = {gecz__ygelu: xwzt__jwa for xwzt__jwa, gecz__ygelu in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[xwzt__jwa])) for
            xwzt__jwa in selected_cols]
        kmb__jwkiz = [xwzt__jwa for xwzt__jwa in selected_cols if col_typs[
            xwzt__jwa] == bodo.dict_str_arr_type]
        aeuhx__ics = (
            f'dict_str_cols_arr_{npvb__qxmpa}.ctypes, np.int32({len(kmb__jwkiz)})'
             if kmb__jwkiz else '0, 0')
        uyk__eqeye = ',' if aayve__moym else ''
        hrix__mtv += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{epzr__tng}", "{nwp__rqvhv}", ({aayve__moym}{uyk__eqeye}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{npvb__qxmpa}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{npvb__qxmpa}.ctypes,
    pyarrow_schema_{npvb__qxmpa},
    {aeuhx__ics},
    {is_merge_into},
  )
"""
        if parallel:
            hrix__mtv += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            hrix__mtv += f'  local_rows = total_rows\n'
        qwqap__vosz = None
        if not is_dead_table:
            qwqap__vosz = []
            ces__pkci = 0
            for xwzt__jwa in range(len(col_names)):
                if ces__pkci < len(out_used_cols
                    ) and xwzt__jwa == out_used_cols[ces__pkci]:
                    if xwzt__jwa == mfxbg__zrks:
                        qwqap__vosz.append(len(selected_cols))
                    else:
                        qwqap__vosz.append(lmema__easq[xwzt__jwa])
                    ces__pkci += 1
                else:
                    qwqap__vosz.append(-1)
            qwqap__vosz = np.array(qwqap__vosz, dtype=np.int64)
        if is_dead_table:
            hrix__mtv += '  table_var = None\n'
        else:
            hrix__mtv += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{npvb__qxmpa}, py_table_type_{npvb__qxmpa})
"""
            if len(out_used_cols) == 0:
                hrix__mtv += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        mcfgg__xppbw = 'None'
        if index_column_name is not None:
            ylpfd__wkww = len(out_used_cols) + 1 if not is_dead_table else 0
            mcfgg__xppbw = (
                f'info_to_array(info_from_table(out_table, {ylpfd__wkww}), index_col_typ)'
                )
        hrix__mtv += f'  index_var = {mcfgg__xppbw}\n'
        hrix__mtv += f'  delete_table(out_table)\n'
        hrix__mtv += f'  ev.finalize()\n'
        hrix__mtv += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            dcv__qirqi = []
            for col_name in vvrjo__cvxwk:
                yfiu__ywk = convert_col_name(col_name, converted_colnames)
                euss__gfh = pyarrow_schema.get_field_index(yfiu__ywk)
                if euss__gfh < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {yfiu__ywk} is not in source schema'
                        )
                dcv__qirqi.append(pyarrow_schema.field(euss__gfh))
            pyarrow_schema = pa.schema(dcv__qirqi)
        umb__hldxx = {gecz__ygelu: xwzt__jwa for xwzt__jwa, gecz__ygelu in
            enumerate(out_used_cols)}
        gvu__xlvz = [umb__hldxx[xwzt__jwa] for xwzt__jwa in out_used_cols if
            col_typs[xwzt__jwa] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[xwzt__jwa])) for
            xwzt__jwa in out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        fchic__zoe = np.array(gvu__xlvz, dtype=np.int32)
        xkpk__jmxdt = np.array(nullable_cols, dtype=np.int32)
        hrix__mtv += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{npvb__qxmpa},
    {len(xkpk__jmxdt)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(fchic__zoe)},
    total_rows_np.ctypes,
    {is_select_query and len(vvrjo__cvxwk) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        hrix__mtv += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            hrix__mtv += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            hrix__mtv += f'  local_rows = total_rows\n'
        if index_column_name:
            hrix__mtv += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            hrix__mtv += '  index_var = None\n'
        if not is_dead_table:
            euss__gfh = []
            ces__pkci = 0
            for xwzt__jwa in range(len(col_names)):
                if ces__pkci < len(out_used_cols
                    ) and xwzt__jwa == out_used_cols[ces__pkci]:
                    euss__gfh.append(ces__pkci)
                    ces__pkci += 1
                else:
                    euss__gfh.append(-1)
            qwqap__vosz = np.array(euss__gfh, dtype=np.int64)
            hrix__mtv += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{npvb__qxmpa}, py_table_type_{npvb__qxmpa})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    hrix__mtv += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    hrix__mtv += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            hrix__mtv += '  table_var = None\n'
        hrix__mtv += '  delete_table(out_table)\n'
        hrix__mtv += '  ev.finalize()\n'
        hrix__mtv += (
            '  return (total_rows, table_var, index_var, None, None)\n')
    else:
        if not is_dead_table:
            hrix__mtv += f"""  type_usecols_offsets_arr_{npvb__qxmpa}_2 = type_usecols_offsets_arr_{npvb__qxmpa}
"""
            jghi__kjs = np.array(out_used_cols, dtype=np.int64)
        hrix__mtv += '  df_typeref_2 = df_typeref\n'
        hrix__mtv += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            hrix__mtv += '  pymysql_check()\n'
        elif db_type == 'oracle':
            hrix__mtv += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            hrix__mtv += '  psycopg2_check()\n'
        if parallel:
            hrix__mtv += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                hrix__mtv += f'  nb_row = {limit}\n'
            else:
                hrix__mtv += '  with objmode(nb_row="int64"):\n'
                hrix__mtv += f'     if rank == {MPI_ROOT}:\n'
                hrix__mtv += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                hrix__mtv += '         frame = pd.read_sql(sql_cons, conn)\n'
                hrix__mtv += '         nb_row = frame.iat[0,0]\n'
                hrix__mtv += '     else:\n'
                hrix__mtv += '         nb_row = 0\n'
                hrix__mtv += '  nb_row = bcast_scalar(nb_row)\n'
            hrix__mtv += f"""  with objmode(table_var=py_table_type_{npvb__qxmpa}, index_var=index_col_typ):
"""
            hrix__mtv += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                hrix__mtv += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                hrix__mtv += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            hrix__mtv += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            hrix__mtv += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            hrix__mtv += f"""  with objmode(table_var=py_table_type_{npvb__qxmpa}, index_var=index_col_typ):
"""
            hrix__mtv += '    df_ret = pd.read_sql(sql_request, conn)\n'
            hrix__mtv += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            hrix__mtv += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            hrix__mtv += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            hrix__mtv += '    index_var = None\n'
        if not is_dead_table:
            hrix__mtv += f'    arrs = []\n'
            hrix__mtv += f'    for i in range(df_ret.shape[1]):\n'
            hrix__mtv += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            hrix__mtv += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{npvb__qxmpa}_2, {len(col_names)})
"""
        else:
            hrix__mtv += '    table_var = None\n'
        hrix__mtv += '  return (-1, table_var, index_var, None, None)\n'
    emgar__arwpq = globals()
    emgar__arwpq.update({'bodo': bodo, f'py_table_type_{npvb__qxmpa}':
        qtof__hld, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        emgar__arwpq.update({f'table_idx_{npvb__qxmpa}': qwqap__vosz,
            f'pyarrow_schema_{npvb__qxmpa}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        emgar__arwpq.update({f'selected_cols_arr_{npvb__qxmpa}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{npvb__qxmpa}':
            np.array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{npvb__qxmpa}': np.array(kmb__jwkiz, np.
            int32), f'py_table_type_{npvb__qxmpa}': qtof__hld,
            'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        emgar__arwpq.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': xkpk__jmxdt, 'snowflake_dict_cols_array':
            fchic__zoe})
    else:
        emgar__arwpq.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(exqr__guzsw), bodo.RangeIndexType(None
            ), tuple(vvrjo__cvxwk)), 'Table': Table,
            f'type_usecols_offsets_arr_{npvb__qxmpa}': jghi__kjs})
    vouuz__rwaew = {}
    exec(hrix__mtv, emgar__arwpq, vouuz__rwaew)
    kfvsd__mgdf = vouuz__rwaew['sql_reader_py']
    dat__ebva = numba.njit(kfvsd__mgdf)
    compiled_funcs.append(dat__ebva)
    return dat__ebva


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        qzqf__jfs = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        wkiap__tbvxi = cgutils.get_or_insert_function(builder.module,
            qzqf__jfs, name='iceberg_pq_read')
        xlfq__rwzks = cgutils.alloca_once(builder, lir.IntType(64))
        theep__ebs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        tiey__cdt = cgutils.alloca_once(builder, lir.IntType(64))
        opz__qnit = args + (xlfq__rwzks, theep__ebs, tiey__cdt)
        tra__nseg = builder.call(wkiap__tbvxi, opz__qnit)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        qwe__bws = builder.load(theep__ebs)
        yywj__cbdln = cgutils.create_struct_proxy(types.pyobject_of_list_type)(
            context, builder)
        gaqdf__pnj = context.get_python_api(builder)
        yywj__cbdln.meminfo = gaqdf__pnj.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), qwe__bws)
        yywj__cbdln.pyobj = qwe__bws
        gaqdf__pnj.decref(qwe__bws)
        vkmde__vwv = [tra__nseg, builder.load(xlfq__rwzks), yywj__cbdln.
            _getvalue(), builder.load(tiey__cdt)]
        return context.make_tuple(builder, put__fwjz, vkmde__vwv)
    put__fwjz = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    nar__inyso = put__fwjz(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return nar__inyso, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
