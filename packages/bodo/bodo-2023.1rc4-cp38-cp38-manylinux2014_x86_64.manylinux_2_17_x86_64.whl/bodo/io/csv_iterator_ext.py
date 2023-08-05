"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.typing import ColNamesMetaType
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        pknam__rue = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(pknam__rue)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ykb__ivyq = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, ykb__ivyq)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    ubq__cltvs = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    dyam__kclpk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer()])
    ftz__kknen = cgutils.get_or_insert_function(builder.module, dyam__kclpk,
        name='initialize_csv_reader')
    iutdt__tpswy = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=ubq__cltvs.csv_reader)
    builder.call(ftz__kknen, [iutdt__tpswy.pyobj])
    builder.store(context.get_constant(types.uint64, 0), ubq__cltvs.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [bgyob__ljm] = sig.args
    [ulww__lozkx] = args
    ubq__cltvs = cgutils.create_struct_proxy(bgyob__ljm)(context, builder,
        value=ulww__lozkx)
    dyam__kclpk = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer()])
    ftz__kknen = cgutils.get_or_insert_function(builder.module, dyam__kclpk,
        name='update_csv_reader')
    iutdt__tpswy = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=ubq__cltvs.csv_reader)
    apgxq__dbucp = builder.call(ftz__kknen, [iutdt__tpswy.pyobj])
    result.set_valid(apgxq__dbucp)
    with builder.if_then(apgxq__dbucp):
        oix__ecaz = builder.load(ubq__cltvs.index)
        ouei__aexox = types.Tuple([sig.return_type.first_type, types.int64])
        tzbo__tvlze = gen_read_csv_objmode(sig.args[0])
        yqpc__qlacm = signature(ouei__aexox, types.stream_reader_type,
            types.int64)
        ewaid__lqcq = context.compile_internal(builder, tzbo__tvlze,
            yqpc__qlacm, [ubq__cltvs.csv_reader, oix__ecaz])
        zzd__absio, dsbu__faf = cgutils.unpack_tuple(builder, ewaid__lqcq)
        asoqo__wkdfh = builder.add(oix__ecaz, dsbu__faf, flags=['nsw'])
        builder.store(asoqo__wkdfh, ubq__cltvs.index)
        result.yield_(zzd__absio)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        hgnrm__fqzq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        hgnrm__fqzq.csv_reader = args[0]
        mjq__vvm = context.get_constant(types.uintp, 0)
        hgnrm__fqzq.index = cgutils.alloca_once_value(builder, mjq__vvm)
        return hgnrm__fqzq._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    oky__xjx = csv_iterator_typeref.instance_type
    sig = signature(oky__xjx, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    hyox__kfq = 'def read_csv_objmode(f_reader):\n'
    xotg__mhlh = [sanitize_varname(eft__elryf) for eft__elryf in
        csv_iterator_type._out_colnames]
    hpxso__bysu = ir_utils.next_label()
    gpaxz__poacj = globals()
    out_types = csv_iterator_type._out_types
    gpaxz__poacj[f'table_type_{hpxso__bysu}'] = TableType(tuple(out_types))
    gpaxz__poacj[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    yatu__nlifj = list(range(len(csv_iterator_type._usecols)))
    hyox__kfq += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        xotg__mhlh, out_types, csv_iterator_type._usecols, yatu__nlifj,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, hpxso__bysu, gpaxz__poacj,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    caegg__cycrw = bodo.ir.csv_ext._gen_parallel_flag_name(xotg__mhlh)
    cml__zlwj = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [caegg__cycrw]
    hyox__kfq += f"  return {', '.join(cml__zlwj)}"
    gpaxz__poacj = globals()
    gyiro__epi = {}
    exec(hyox__kfq, gpaxz__poacj, gyiro__epi)
    mipit__posyi = gyiro__epi['read_csv_objmode']
    mqmvq__tfe = numba.njit(mipit__posyi)
    bodo.ir.csv_ext.compiled_funcs.append(mqmvq__tfe)
    ftmeo__ckdb = 'def read_func(reader, local_start):\n'
    ftmeo__ckdb += f"  {', '.join(cml__zlwj)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        ftmeo__ckdb += f'  local_len = len(T)\n'
        ftmeo__ckdb += '  total_size = local_len\n'
        ftmeo__ckdb += f'  if ({caegg__cycrw}):\n'
        ftmeo__ckdb += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        ftmeo__ckdb += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        xov__vqza = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        ftmeo__ckdb += '  total_size = 0\n'
        xov__vqza = (
            f'bodo.utils.conversion.convert_to_index({cml__zlwj[1]}, {csv_iterator_type._index_name!r})'
            )
    ftmeo__ckdb += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({cml__zlwj[0]},), {xov__vqza}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(ftmeo__ckdb, {'bodo': bodo, 'objmode_func': mqmvq__tfe, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, gyiro__epi)
    return gyiro__epi['read_func']
