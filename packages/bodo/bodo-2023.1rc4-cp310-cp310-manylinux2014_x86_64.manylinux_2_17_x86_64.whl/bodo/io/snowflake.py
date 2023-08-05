import os
import sys
import traceback
import warnings
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, Optional, Tuple
from urllib.parse import parse_qsl, urlparse
from uuid import uuid4
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.io.helpers import ExceptionPropagatingThread, _get_numba_typ_from_pa_typ, update_env_vars, update_file_contents
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning, is_str_arr_type
if TYPE_CHECKING:
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.cursor import ResultMetadata, SnowflakeCursor
    from snowflake.connector.result_batch import JSONResultBatch, ResultBatch
SF_READ_SCHEMA_PROBE_TIMEOUT = 5
SF_READ_AUTO_DICT_ENCODE_ENABLED = True
SF_READ_DICT_ENCODE_CRITERION = 0.5
SF_READ_DICT_ENCODING_PROBE_TIMEOUT = 5
SF_READ_DICT_ENCODING_IF_TIMEOUT = False
SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT = 100000000
SCALE_TO_UNIT_PRECISION: Dict[int, Literal['s', 'ms', 'us', 'ns']] = {(0):
    's', (3): 'ms', (6): 'us', (9): 'ns'}
TYPE_CODE_TO_ARROW_TYPE: List[Callable[['ResultMetadata', str], pa.DataType]
    ] = [lambda m, _: pa.int64() if m.scale == 0 else pa.float64() if m.
    scale < 18 else pa.decimal128(m.precision, m.scale), lambda _, __: pa.
    float64(), lambda _, __: pa.string(), lambda _, __: pa.date32(), lambda
    _, __: pa.time64('ns'), lambda _, __: pa.string(), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, _: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale]), lambda _, __: pa.string(),
    lambda _, __: pa.string(), lambda _, __: pa.binary(), lambda m, _: {(0):
    pa.time32('s'), (3): pa.time32('ms'), (6): pa.time64('us'), (9): pa.
    time64('ns')}[m.scale], lambda _, __: pa.bool_(), lambda _, __: pa.string()
    ]
INT_BITSIZE_TO_ARROW_DATATYPE = {(1): pa.int8(), (2): pa.int16(), (4): pa.
    int32(), (8): pa.int64()}


def gen_snowflake_schema(column_names, column_datatypes):
    sf_schema = {}
    for col_name, msitk__dxj in zip(column_names, column_datatypes):
        if isinstance(msitk__dxj, bodo.DatetimeArrayType
            ) or msitk__dxj == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif msitk__dxj == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(msitk__dxj, bodo.TimeArrayType):
            if msitk__dxj.precision in [0, 3, 6]:
                heack__ytxn = msitk__dxj.precision
            elif msitk__dxj.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                heack__ytxn = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({heack__ytxn})'
        elif isinstance(msitk__dxj, types.Array):
            tog__imfy = msitk__dxj.dtype.name
            if tog__imfy.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if tog__imfy.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif tog__imfy.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif tog__imfy.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(msitk__dxj):
            sf_schema[col_name] = 'TEXT'
        elif msitk__dxj == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif msitk__dxj == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(msitk__dxj, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(msitk__dxj, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(msitk__dxj, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(msitk__dxj, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {msitk__dxj} to snowflake type for {col_name} not supported yet.'
                )
    return sf_schema


SF_WRITE_COPY_INTO_ON_ERROR = 'abort_statement'
SF_WRITE_OVERLAP_UPLOAD = True
SF_WRITE_PARQUET_CHUNK_SIZE = int(256000000.0)
SF_WRITE_PARQUET_COMPRESSION = 'snappy'
SF_WRITE_UPLOAD_USING_PUT = False
SF_AZURE_WRITE_HDFS_CORE_SITE = """<configuration>
  <property>
    <name>fs.azure.account.auth.type</name>
    <value>SAS</value>
  </property>
  <property>
    <name>fs.azure.sas.token.provider.type</name>
    <value>org.bodo.azurefs.sas.BodoSASTokenProvider</value>
  </property>
  <property>
    <name>fs.abfs.impl</name>
    <value>org.apache.hadoop.fs.azurebfs.AzureBlobFileSystem</value>
  </property>
</configuration>
"""
SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION = os.path.join(bodo.
    HDFS_CORE_SITE_LOC_DIR.name, 'sas_token.txt')


def execute_query(cursor: 'SnowflakeCursor', query: str, timeout: Optional[int]
    ) ->Optional['SnowflakeCursor']:
    try:
        return cursor.execute(query, timeout=timeout)
    except snowflake.connector.errors.ProgrammingError as lwg__plr:
        if 'SQL execution canceled' in str(lwg__plr):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    niq__pph = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    rql__qubm = urlparse(conn_str)
    josoe__bgos = {}
    if rql__qubm.username:
        josoe__bgos['user'] = rql__qubm.username
    if rql__qubm.password:
        josoe__bgos['password'] = rql__qubm.password
    if rql__qubm.hostname:
        josoe__bgos['account'] = rql__qubm.hostname
    if rql__qubm.port:
        josoe__bgos['port'] = rql__qubm.port
    if rql__qubm.path:
        kdazq__qnr = rql__qubm.path
        if kdazq__qnr.startswith('/'):
            kdazq__qnr = kdazq__qnr[1:]
        guxq__hte = kdazq__qnr.split('/')
        if len(guxq__hte) == 2:
            izgti__yhwd, schema = guxq__hte
        elif len(guxq__hte) == 1:
            izgti__yhwd = guxq__hte[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        josoe__bgos['database'] = izgti__yhwd
        if schema:
            josoe__bgos['schema'] = schema
    if rql__qubm.query:
        for kec__tlz, vsus__cksft in parse_qsl(rql__qubm.query):
            josoe__bgos[kec__tlz] = vsus__cksft
            if kec__tlz == 'session_parameters':
                import json
                josoe__bgos[kec__tlz] = json.loads(vsus__cksft)
    josoe__bgos['application'] = 'bodo'
    josoe__bgos['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as rpsc__dkp:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**josoe__bgos)
    chao__vfb = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if chao__vfb and bodo.get_rank() == 0:
        chao__vfb = chao__vfb.lower()
        tzxg__amp = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if tzxg__amp is not None:
            tzxg__amp = tzxg__amp.lower()
        jug__eyvs = conn.cursor()
        jug__eyvs.execute('select current_region()')
        qfb__ocq: pa.Table = jug__eyvs.fetch_arrow_all()
        islc__zimm = qfb__ocq[0][0].as_py()
        jug__eyvs.close()
        gjc__yfj = islc__zimm.split('_')
        fai__rrs = gjc__yfj[0].lower()
        jsp__mqo = '-'.join(gjc__yfj[1:]).lower()
        if tzxg__amp and tzxg__amp != fai__rrs:
            ikuql__gsnby = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {fai__rrs}, but the Bodo cluster is located on {tzxg__amp}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(ikuql__gsnby)
        elif chao__vfb != jsp__mqo:
            ikuql__gsnby = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {jsp__mqo}, but the Bodo cluster is located in {chao__vfb}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(ikuql__gsnby)
    niq__pph.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    dhgfi__sygfk = cursor.describe(sql_query)
    tz: str = cursor._timezone
    abloe__xnmug: List[pa.Field] = []
    zzoht__xusu: List[str] = []
    mwdd__xyg: List[int] = []
    for ozi__mjtmf, hownq__mcby in enumerate(dhgfi__sygfk):
        occl__nqsco = TYPE_CODE_TO_ARROW_TYPE[hownq__mcby.type_code](
            hownq__mcby, tz)
        abloe__xnmug.append(pa.field(hownq__mcby.name, occl__nqsco,
            hownq__mcby.is_nullable))
        if pa.types.is_int64(occl__nqsco):
            zzoht__xusu.append(hownq__mcby.name)
            mwdd__xyg.append(ozi__mjtmf)
    if is_select_query and len(zzoht__xusu) != 0:
        jhmb__fqdtq = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in zzoht__xusu
            ) + f' FROM ({sql_query}) LIMIT 1'
        vif__cluo = execute_query(cursor, jhmb__fqdtq, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if vif__cluo is not None and (xikq__owl := vif__cluo.fetch_arrow_all()
            ) is not None:
            for ozi__mjtmf, (dlc__pwrn, uqcq__alijn) in enumerate(xikq__owl
                .to_pylist()[0].items()):
                lyyg__rzo = zzoht__xusu[ozi__mjtmf]
                xko__amu = (f'SYSTEM$TYPEOF({escape_col_name(lyyg__rzo)})',
                    f'SYSTEM$TYPEOF({escape_col_name(lyyg__rzo.upper())})')
                assert dlc__pwrn in xko__amu, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                qbddt__cxjg = mwdd__xyg[ozi__mjtmf]
                poqc__icpqx = int(uqcq__alijn[-2])
                lzkfk__yist = INT_BITSIZE_TO_ARROW_DATATYPE[poqc__icpqx]
                abloe__xnmug[qbddt__cxjg] = abloe__xnmug[qbddt__cxjg
                    ].with_type(lzkfk__yist)
    dnu__nljf = []
    ckxv__vgz = []
    heiub__ufra = []
    for ozi__mjtmf, dlfm__eieso in enumerate(abloe__xnmug):
        occl__nqsco, rzizf__egm = _get_numba_typ_from_pa_typ(dlfm__eieso, 
            False, dlfm__eieso.nullable, None)
        dnu__nljf.append(occl__nqsco)
        if not rzizf__egm:
            ckxv__vgz.append(ozi__mjtmf)
            heiub__ufra.append(dlfm__eieso.type)
    return abloe__xnmug, dnu__nljf, ckxv__vgz, heiub__ufra


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    qnply__mgih, dnu__nljf, ckxv__vgz, heiub__ufra = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    avriw__cdu = _bodo_read_as_dict if _bodo_read_as_dict else []
    xgg__rmkhd = {}
    for ozi__mjtmf, gteca__ugcxr in enumerate(dnu__nljf):
        if gteca__ugcxr == string_array_type:
            xgg__rmkhd[qnply__mgih[ozi__mjtmf].name] = ozi__mjtmf
    nis__pxxe = {(btao__lmqla.lower() if btao__lmqla.isupper() else
        btao__lmqla): btao__lmqla for btao__lmqla in xgg__rmkhd.keys()}
    agjtv__mtkrv = avriw__cdu - nis__pxxe.keys()
    if len(agjtv__mtkrv) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {agjtv__mtkrv}'
                ))
    gkgk__zrkc = nis__pxxe.keys() & avriw__cdu
    for btao__lmqla in gkgk__zrkc:
        dnu__nljf[xgg__rmkhd[nis__pxxe[btao__lmqla]]] = dict_str_arr_type
    caos__xfbrj, jtu__vhbej = [], []
    eqmc__gyu = nis__pxxe.keys() - avriw__cdu
    for btao__lmqla in eqmc__gyu:
        caos__xfbrj.append(f'count (distinct "{nis__pxxe[btao__lmqla]}")')
        jtu__vhbej.append(xgg__rmkhd[nis__pxxe[btao__lmqla]])
    mrdna__zhs: Optional[Tuple[int, List[str]]] = None
    if len(caos__xfbrj) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        fda__itn = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            caos__xfbrj), 1)
        vhar__zhnw = (
            f"select count(*),{', '.join(caos__xfbrj)}from ( select * from ({sql_query}) limit {fda__itn} ) SAMPLE (1)"
            )
        mjv__hemx = execute_query(cursor, vhar__zhnw, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if mjv__hemx is None:
            mrdna__zhs = fda__itn, caos__xfbrj
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for ozi__mjtmf in jtu__vhbej:
                    dnu__nljf[ozi__mjtmf] = dict_str_arr_type
        else:
            gxrwt__exfrp: pa.Table = mjv__hemx.fetch_arrow_all()
            rii__rbyel = gxrwt__exfrp[0][0].as_py()
            uyvcn__jofu = [(gxrwt__exfrp[ozi__mjtmf][0].as_py() / max(
                rii__rbyel, 1)) for ozi__mjtmf in range(1, len(caos__xfbrj) +
                1)]
            vujjx__nxafp = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(uyvcn__jofu, jtu__vhbej))
            for _, mgr__mccgj in vujjx__nxafp:
                dnu__nljf[mgr__mccgj] = dict_str_arr_type
    coeo__rhv: List[str] = []
    hcp__cfn = set()
    for x in qnply__mgih:
        if x.name.isupper():
            hcp__cfn.add(x.name.lower())
            coeo__rhv.append(x.name.lower())
        else:
            coeo__rhv.append(x.name)
    vegdv__xqux = DataFrameType(data=tuple(dnu__nljf), columns=tuple(coeo__rhv)
        )
    return vegdv__xqux, hcp__cfn, ckxv__vgz, heiub__ufra, pa.schema(qnply__mgih
        ), mrdna__zhs


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for uhlkj__behqj in batches:
            uhlkj__behqj._bodo_num_rows = uhlkj__behqj.rowcount
            self._bodo_total_rows += uhlkj__behqj._bodo_num_rows
        self.schema = schema
        self.conn = conn


class FakeArrowJSONResultBatch:

    def __init__(self, json_batch: 'JSONResultBatch', schema: pa.Schema
        ) ->None:
        self._json_batch = json_batch
        self._schema = schema

    @property
    def rowcount(self):
        return self._json_batch.rowcount

    def to_arrow(self, _: Optional['SnowflakeConnection']=None) ->pa.Table:
        ztucm__dlzm = []
        for wtmkc__vcnt in self._json_batch.create_iter():
            ztucm__dlzm.append({self._schema.names[ozi__mjtmf]: mrl__sco for
                ozi__mjtmf, mrl__sco in enumerate(wtmkc__vcnt)})
        dba__fvep = pa.Table.from_pylist(ztucm__dlzm, schema=self._schema)
        return dba__fvep


def get_dataset(query: str, conn_str: str, schema: pa.Schema,
    only_fetch_length: bool=False, is_select_query: bool=True, is_parallel:
    bool=True, is_independent: bool=False) ->Tuple[SnowflakeDataset, int]:
    assert not (only_fetch_length and not is_select_query
        ), 'The only length optimization can only be run with select queries'
    assert not (is_parallel and is_independent
        ), 'Snowflake get_dataset: is_parallel and is_independent cannot be True at the same time'
    try:
        import snowflake.connector
        from snowflake.connector.result_batch import ArrowResultBatch, JSONResultBatch
    except ImportError as rpsc__dkp:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    niq__pph = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel)
    spm__hsnmu = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    nnlj__tes = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            jug__eyvs = conn.cursor()
            gile__rji = tracing.Event('execute_length_query', is_parallel=False
                )
            jug__eyvs.execute(query)
            qfb__ocq = jug__eyvs.fetch_arrow_all()
            nnlj__tes = qfb__ocq[0][0].as_py()
            jug__eyvs.close()
            gile__rji.finalize()
        if not is_independent:
            nnlj__tes = spm__hsnmu.bcast(nnlj__tes)
    else:
        if bodo.get_rank() == 0 or is_independent:
            jug__eyvs = conn.cursor()
            gile__rji = tracing.Event('execute_query', is_parallel=False)
            jug__eyvs = conn.cursor()
            jug__eyvs.execute(query)
            gile__rji.finalize()
            nnlj__tes: int = jug__eyvs.rowcount
            batches: 'List[ResultBatch]' = jug__eyvs.get_result_batches()
            if len(batches) > 0 and not isinstance(batches[0], ArrowResultBatch
                ):
                if not is_select_query and len(batches) == 1 and isinstance(
                    batches[0], JSONResultBatch):
                    batches = [FakeArrowJSONResultBatch(x, schema) for x in
                        batches]
                else:
                    raise BodoError(
                        f"Batches returns from Snowflake don't match the expected format. Expected Arrow batches but got {type(batches[0])}"
                        )
            jug__eyvs.close()
        if not is_independent:
            nnlj__tes, batches, schema = spm__hsnmu.bcast((nnlj__tes,
                batches, schema))
    oww__nim = SnowflakeDataset(batches, schema, conn)
    niq__pph.finalize()
    return oww__nim, nnlj__tes


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    niq__pph = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as rpsc__dkp:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    adn__zfdsh = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                kfsnm__sslmr = 'CREATE TEMPORARY STAGE'
            else:
                kfsnm__sslmr = 'CREATE STAGE'
            txha__yke = (
                f'{kfsnm__sslmr} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(txha__yke, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as ezjpi__sls:
            if ezjpi__sls.msg is not None and ezjpi__sls.msg.endswith(
                'already exists.'):
                continue
            adn__zfdsh = ezjpi__sls.msg
            break
    niq__pph.finalize()
    if adn__zfdsh is not None:
        raise snowflake.connector.ProgrammingError(adn__zfdsh)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    niq__pph = tracing.Event('drop_internal_stage', is_parallel=False)
    asgkq__hitk = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(asgkq__hitk, _is_internal=True)
    niq__pph.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        xnn__qtbe = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        eaf__thfn = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(eaf__thfn, _is_internal=True).fetchall()
        xnn__qtbe.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        ocys__bjyiv = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        ocys__bjyiv.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        ocys__bjyiv = None
    return ocys__bjyiv


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    niq__pph = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as rpsc__dkp:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        jbqs__yhx = 'CREATE TABLE'
    elif if_exists == 'replace':
        jbqs__yhx = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        jbqs__yhx = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    meynz__foun = tracing.Event('create_table', is_parallel=False)
    efhpz__yjfy = ', '.join([f'"{uvwd__vexi}" {sf_schema[uvwd__vexi]}' for
        uvwd__vexi in sf_schema.keys()])
    uqpjd__xkw = (
        f'{jbqs__yhx} {location} ({efhpz__yjfy}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(uqpjd__xkw, _is_internal=True)
    meynz__foun.finalize()
    niq__pph.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    niq__pph = tracing.Event('execute_copy_into', is_parallel=False)
    nood__clgxm = ','.join([f'"{uvwd__vexi}"' for uvwd__vexi in sf_schema.
        keys()])
    hcqwv__aivs = {uvwd__vexi: ('::binary' if sf_schema[uvwd__vexi] ==
        'BINARY' else '::string' if sf_schema[uvwd__vexi].startswith('TIME'
        ) else '') for uvwd__vexi in sf_schema.keys()}
    fmavf__ptzt = ','.join([f'$1:"{uvwd__vexi}"{hcqwv__aivs[uvwd__vexi]}' for
        uvwd__vexi in sf_schema.keys()])
    uti__oxl = (
        f'COPY INTO {location} ({nood__clgxm}) FROM (SELECT {fmavf__ptzt} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    yagz__ewd = cursor.execute(uti__oxl, _is_internal=True).fetchall()
    mxp__auhz = sum(1 if lwg__plr[1] == 'LOADED' else 0 for lwg__plr in
        yagz__ewd)
    occx__rmpp = len(yagz__ewd)
    ieg__ldrqa = sum(int(lwg__plr[3]) for lwg__plr in yagz__ewd)
    nkcb__jjejy = mxp__auhz, occx__rmpp, ieg__ldrqa, yagz__ewd
    niq__pph.add_attribute('copy_into_nsuccess', mxp__auhz)
    niq__pph.add_attribute('copy_into_nchunks', occx__rmpp)
    niq__pph.add_attribute('copy_into_nrows', ieg__ldrqa)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(yagz__ewd)}')
    niq__pph.finalize()
    return nkcb__jjejy


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as rpsc__dkp:
    snowflake_connector_cursor_python_type = None
SnowflakeConnectorCursorType = install_py_obj_class(types_name=
    'snowflake_connector_cursor_type', python_type=
    snowflake_connector_cursor_python_type, module=sys.modules[__name__],
    class_name='SnowflakeConnectorCursorType', model_name=
    'SnowflakeConnectorCursorModel')
TemporaryDirectoryType = install_py_obj_class(types_name=
    'temporary_directory_type', python_type=TemporaryDirectory, module=sys.
    modules[__name__], class_name='TemporaryDirectoryType', model_name=
    'TemporaryDirectoryModel')


def get_snowflake_stage_info(cursor: 'SnowflakeCursor', stage_name: str,
    tmp_folder: TemporaryDirectory) ->Dict:
    niq__pph = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    hxzd__asm = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    hxzd__asm = hxzd__asm.replace('\\', '\\\\').replace("'", "\\'")
    eaf__thfn = (
        f'PUT \'file://{hxzd__asm}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    japb__zit = cursor._execute_helper(eaf__thfn, is_internal=True)
    niq__pph.finalize()
    return japb__zit


def connect_and_get_upload_info(conn_str: str):
    niq__pph = tracing.Event('connect_and_get_upload_info')
    spm__hsnmu = MPI.COMM_WORLD
    hicxd__zmcww = spm__hsnmu.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    etf__wow = ''
    mvjp__top = {}
    old_creds = {}
    old_core_site = ''
    vupb__plns = ''
    old_sas_token = ''
    bms__fnuoh = None
    if hicxd__zmcww == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                etf__wow = ''
            else:
                japb__zit = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                jkqu__sydyx = japb__zit['data']['uploadInfo']
                vewbb__pmva = jkqu__sydyx.get('locationType', 'UNKNOWN')
                udm__mkroi = False
                if vewbb__pmva == 'S3':
                    tel__nxibk, _, kdazq__qnr = jkqu__sydyx['location'
                        ].partition('/')
                    kdazq__qnr = kdazq__qnr.rstrip('/')
                    etf__wow = f's3://{tel__nxibk}/{kdazq__qnr}/'
                    mvjp__top = {'AWS_ACCESS_KEY_ID': jkqu__sydyx['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': jkqu__sydyx
                        ['creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        jkqu__sydyx['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': jkqu__sydyx['region']}
                elif vewbb__pmva == 'AZURE':
                    huf__udzr = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        huf__udzr = True
                    except ImportError as rpsc__dkp:
                        pass
                    hmhv__mfy = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if huf__udzr and hmhv__mfy:
                        nqs__rsfd, _, kdazq__qnr = jkqu__sydyx['location'
                            ].partition('/')
                        kdazq__qnr = kdazq__qnr.rstrip('/')
                        jpsu__rpj = jkqu__sydyx['storageAccount']
                        vupb__plns = jkqu__sydyx['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(kdazq__qnr) == 0:
                            etf__wow = (
                                f'abfs://{nqs__rsfd}@{jpsu__rpj}.dfs.core.windows.net/'
                                )
                        else:
                            etf__wow = (
                                f'abfs://{nqs__rsfd}@{jpsu__rpj}.dfs.core.windows.net/{kdazq__qnr}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        udm__mkroi = True
                        mnxuu__bzev = 'Detected Azure Stage. '
                        if not huf__udzr:
                            mnxuu__bzev += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not hmhv__mfy:
                            mnxuu__bzev += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        mnxuu__bzev += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(mnxuu__bzev))
                else:
                    udm__mkroi = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{vewbb__pmva}'. Falling back to PUT command for upload."
                        ))
                if udm__mkroi:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as lwg__plr:
            bms__fnuoh = RuntimeError(str(lwg__plr))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, lwg__plr,
                    lwg__plr.__traceback__)))
    bms__fnuoh = spm__hsnmu.bcast(bms__fnuoh)
    if isinstance(bms__fnuoh, Exception):
        raise bms__fnuoh
    etf__wow = spm__hsnmu.bcast(etf__wow)
    azure_stage_direct_upload = etf__wow.startswith('abfs://')
    if etf__wow == '':
        ejgs__kaf = True
        etf__wow = tmp_folder.name + '/'
        if hicxd__zmcww != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        ejgs__kaf = False
        mvjp__top = spm__hsnmu.bcast(mvjp__top)
        old_creds = update_env_vars(mvjp__top)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            vupb__plns = spm__hsnmu.bcast(vupb__plns)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, vupb__plns)
    stage_name = spm__hsnmu.bcast(stage_name)
    niq__pph.finalize()
    return (cursor, tmp_folder, stage_name, etf__wow, ejgs__kaf, old_creds,
        azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    niq__pph = tracing.Event('create_table_copy_into', is_parallel=False)
    spm__hsnmu = MPI.COMM_WORLD
    hicxd__zmcww = spm__hsnmu.Get_rank()
    bms__fnuoh = None
    if hicxd__zmcww == 0:
        try:
            ssw__unaef = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(ssw__unaef)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            mxp__auhz, occx__rmpp, ieg__ldrqa, aqo__gnjm = execute_copy_into(
                cursor, stage_name, location, sf_schema)
            if mxp__auhz != occx__rmpp:
                raise BodoError(
                    f'Snowflake write copy_into failed: {aqo__gnjm}')
            nfyub__fhrc = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(nfyub__fhrc)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as lwg__plr:
            bms__fnuoh = RuntimeError(str(lwg__plr))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, lwg__plr,
                    lwg__plr.__traceback__)))
    bms__fnuoh = spm__hsnmu.bcast(bms__fnuoh)
    if isinstance(bms__fnuoh, Exception):
        raise bms__fnuoh
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    niq__pph.finalize()
