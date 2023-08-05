"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            jydks__swrhe = self.fs.open_input_file(path)
        except:
            jydks__swrhe = self.fs.open_input_stream(path)
    elif mode == 'wb':
        jydks__swrhe = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, jydks__swrhe, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr,
    types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    iqu__bdgbd = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    pzos__lbego = False
    jhjib__von = get_proxy_uri_from_env_vars()
    if storage_options:
        pzos__lbego = storage_options.get('anon', False)
    return S3FileSystem(anonymous=pzos__lbego, region=region,
        endpoint_override=iqu__bdgbd, proxy_options=jhjib__von)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    iqu__bdgbd = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    pzos__lbego = False
    jhjib__von = get_proxy_uri_from_env_vars()
    if storage_options:
        pzos__lbego = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=iqu__bdgbd,
        anonymous=pzos__lbego, proxy_options=jhjib__von)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    npqt__bzhmg = urlparse(path)
    if npqt__bzhmg.scheme in ('abfs', 'abfss'):
        peqr__xnpod = path
        if npqt__bzhmg.port is None:
            ipha__mncge = 0
        else:
            ipha__mncge = npqt__bzhmg.port
        pdka__kfy = None
    else:
        peqr__xnpod = npqt__bzhmg.hostname
        ipha__mncge = npqt__bzhmg.port
        pdka__kfy = npqt__bzhmg.username
    try:
        fs = HdFS(host=peqr__xnpod, port=ipha__mncge, user=pdka__kfy)
    except Exception as gpltp__doywe:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            gpltp__doywe))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        pcu__tyy = fs.isdir(path)
    except gcsfs.utils.HttpError as gpltp__doywe:
        raise BodoError(
            f'{gpltp__doywe}. Make sure your google cloud credentials are set!'
            )
    return pcu__tyy


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [mlaqo__ntzy.split('/')[-1] for mlaqo__ntzy in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        npqt__bzhmg = urlparse(path)
        poqw__voxzq = (npqt__bzhmg.netloc + npqt__bzhmg.path).rstrip('/')
        jdo__dct = fs.get_file_info(poqw__voxzq)
        if jdo__dct.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not jdo__dct.size and jdo__dct.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as gpltp__doywe:
        raise
    except BodoError as vjxfs__igrd:
        raise
    except Exception as gpltp__doywe:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gpltp__doywe).__name__}: {str(gpltp__doywe)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    tst__sgb = None
    try:
        if s3_is_directory(fs, path):
            npqt__bzhmg = urlparse(path)
            poqw__voxzq = (npqt__bzhmg.netloc + npqt__bzhmg.path).rstrip('/')
            hmgbs__hbs = pa_fs.FileSelector(poqw__voxzq, recursive=False)
            vcax__egn = fs.get_file_info(hmgbs__hbs)
            if vcax__egn and vcax__egn[0].path in [poqw__voxzq,
                f'{poqw__voxzq}/'] and int(vcax__egn[0].size or 0) == 0:
                vcax__egn = vcax__egn[1:]
            tst__sgb = [qici__bnsh.base_name for qici__bnsh in vcax__egn]
    except BodoError as vjxfs__igrd:
        raise
    except Exception as gpltp__doywe:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gpltp__doywe).__name__}: {str(gpltp__doywe)}
{bodo_error_msg}"""
            )
    return tst__sgb


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    npqt__bzhmg = urlparse(path)
    sbdxt__zhywb = npqt__bzhmg.path
    try:
        nqsmm__acun = HadoopFileSystem.from_uri(path)
    except Exception as gpltp__doywe:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            gpltp__doywe))
    bdp__woipg = nqsmm__acun.get_file_info([sbdxt__zhywb])
    if bdp__woipg[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not bdp__woipg[0].size and bdp__woipg[0].type == FileType.Directory:
        return nqsmm__acun, True
    return nqsmm__acun, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    tst__sgb = None
    nqsmm__acun, pcu__tyy = hdfs_is_directory(path)
    if pcu__tyy:
        npqt__bzhmg = urlparse(path)
        sbdxt__zhywb = npqt__bzhmg.path
        hmgbs__hbs = FileSelector(sbdxt__zhywb, recursive=True)
        try:
            vcax__egn = nqsmm__acun.get_file_info(hmgbs__hbs)
        except Exception as gpltp__doywe:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(sbdxt__zhywb, gpltp__doywe))
        tst__sgb = [qici__bnsh.base_name for qici__bnsh in vcax__egn]
    return nqsmm__acun, tst__sgb


def abfs_is_directory(path):
    nqsmm__acun = get_hdfs_fs(path)
    try:
        bdp__woipg = nqsmm__acun.info(path)
    except OSError as vjxfs__igrd:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if bdp__woipg['size'] == 0 and bdp__woipg['kind'].lower() == 'directory':
        return nqsmm__acun, True
    return nqsmm__acun, False


def abfs_list_dir_fnames(path):
    tst__sgb = None
    nqsmm__acun, pcu__tyy = abfs_is_directory(path)
    if pcu__tyy:
        npqt__bzhmg = urlparse(path)
        sbdxt__zhywb = npqt__bzhmg.path
        try:
            gedvq__doan = nqsmm__acun.ls(sbdxt__zhywb)
        except Exception as gpltp__doywe:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(sbdxt__zhywb, gpltp__doywe))
        tst__sgb = [fname[fname.rindex('/') + 1:] for fname in gedvq__doan]
    return nqsmm__acun, tst__sgb


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    wuz__dxga = urlparse(path)
    fname = path
    fs = None
    kugh__suf = 'read_json' if ftype == 'json' else 'read_csv'
    ann__nfu = (
        f'pd.{kugh__suf}(): there is no {ftype} file in directory: {fname}')
    qkdp__vrt = directory_of_files_common_filter
    if wuz__dxga.scheme == 's3':
        upeo__msutb = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        dmt__fifhi = s3_list_dir_fnames(fs, path)
        poqw__voxzq = (wuz__dxga.netloc + wuz__dxga.path).rstrip('/')
        fname = poqw__voxzq
        if dmt__fifhi:
            dmt__fifhi = [(poqw__voxzq + '/' + mlaqo__ntzy) for mlaqo__ntzy in
                sorted(filter(qkdp__vrt, dmt__fifhi))]
            pxi__cbjjy = [mlaqo__ntzy for mlaqo__ntzy in dmt__fifhi if int(
                fs.get_file_info(mlaqo__ntzy).size or 0) > 0]
            if len(pxi__cbjjy) == 0:
                raise BodoError(ann__nfu)
            fname = pxi__cbjjy[0]
        kkzq__yelx = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        hhnb__posv = fs._open(fname)
    elif wuz__dxga.scheme == 'hdfs':
        upeo__msutb = True
        fs, dmt__fifhi = hdfs_list_dir_fnames(path)
        kkzq__yelx = fs.get_file_info([wuz__dxga.path])[0].size
        if dmt__fifhi:
            path = path.rstrip('/')
            dmt__fifhi = [(path + '/' + mlaqo__ntzy) for mlaqo__ntzy in
                sorted(filter(qkdp__vrt, dmt__fifhi))]
            pxi__cbjjy = [mlaqo__ntzy for mlaqo__ntzy in dmt__fifhi if fs.
                get_file_info([urlparse(mlaqo__ntzy).path])[0].size > 0]
            if len(pxi__cbjjy) == 0:
                raise BodoError(ann__nfu)
            fname = pxi__cbjjy[0]
            fname = urlparse(fname).path
            kkzq__yelx = fs.get_file_info([fname])[0].size
        hhnb__posv = fs.open_input_file(fname)
    elif wuz__dxga.scheme in ('abfs', 'abfss'):
        upeo__msutb = True
        fs, dmt__fifhi = abfs_list_dir_fnames(path)
        kkzq__yelx = fs.info(fname)['size']
        if dmt__fifhi:
            path = path.rstrip('/')
            dmt__fifhi = [(path + '/' + mlaqo__ntzy) for mlaqo__ntzy in
                sorted(filter(qkdp__vrt, dmt__fifhi))]
            pxi__cbjjy = [mlaqo__ntzy for mlaqo__ntzy in dmt__fifhi if fs.
                info(mlaqo__ntzy)['size'] > 0]
            if len(pxi__cbjjy) == 0:
                raise BodoError(ann__nfu)
            fname = pxi__cbjjy[0]
            kkzq__yelx = fs.info(fname)['size']
            fname = urlparse(fname).path
        hhnb__posv = fs.open(fname, 'rb')
    else:
        if wuz__dxga.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {wuz__dxga.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        upeo__msutb = False
        if os.path.isdir(path):
            gedvq__doan = filter(qkdp__vrt, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            pxi__cbjjy = [mlaqo__ntzy for mlaqo__ntzy in sorted(gedvq__doan
                ) if os.path.getsize(mlaqo__ntzy) > 0]
            if len(pxi__cbjjy) == 0:
                raise BodoError(ann__nfu)
            fname = pxi__cbjjy[0]
        kkzq__yelx = os.path.getsize(fname)
        hhnb__posv = fname
    return upeo__msutb, hhnb__posv, kkzq__yelx, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    ujeiv__lzbyp = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            ewcd__fckkq, quub__chd = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = ewcd__fckkq.region
        except Exception as gpltp__doywe:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{gpltp__doywe}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = ujeiv__lzbyp.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, filename_prefix, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, filename_prefix, is_parallel=False):

    def impl(path_or_buf, D, filename_prefix, is_parallel=False):
        ffpz__hhco = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        sdsxw__gdkyw, pie__yzhyx = unicode_to_utf8_and_len(D)
        rgch__gie = 0
        if is_parallel:
            rgch__gie = bodo.libs.distributed_api.dist_exscan(pie__yzhyx,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), sdsxw__gdkyw, rgch__gie,
            pie__yzhyx, is_parallel, unicode_to_utf8(ffpz__hhco),
            unicode_to_utf8(filename_prefix))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    uzsj__zpyzs = get_overload_constant_dict(storage_options)
    fgnti__gydnn = 'def impl(storage_options):\n'
    fgnti__gydnn += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    fgnti__gydnn += f'    storage_options_py = {str(uzsj__zpyzs)}\n'
    fgnti__gydnn += '  return storage_options_py\n'
    rxz__kgzhd = {}
    exec(fgnti__gydnn, globals(), rxz__kgzhd)
    return rxz__kgzhd['impl']
