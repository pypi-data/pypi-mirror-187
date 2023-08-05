"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
import sys
from collections import defaultdict
from typing import Literal, Set, Tuple
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError
from bodo.utils.utils import debug_prints, is_array_typ


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    dawpb__ifgs = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    wrs__hec = []
    for mmyz__gtik, rqqze__agd in enumerate(node.out_vars):
        esq__jqcnx = typemap[rqqze__agd.name]
        if esq__jqcnx == types.none:
            continue
        uorj__ylzsd = mmyz__gtik == 0 and node.connector_typ in ('parquet',
            'sql') and not node.is_live_table
        qrhg__fsvx = node.connector_typ == 'sql' and mmyz__gtik > 1
        if not (uorj__ylzsd or qrhg__fsvx):
            voraa__yhsxi = array_analysis._gen_shape_call(equiv_set,
                rqqze__agd, esq__jqcnx.ndim, None, dawpb__ifgs)
            equiv_set.insert_equiv(rqqze__agd, voraa__yhsxi)
            wrs__hec.append(voraa__yhsxi[0])
            equiv_set.define(rqqze__agd, set())
    if len(wrs__hec) > 1:
        equiv_set.insert_equiv(*wrs__hec)
    return [], dawpb__ifgs


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        khzoq__gahi = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        khzoq__gahi = Distribution.OneD_Var
    else:
        khzoq__gahi = Distribution.OneD
    for ayyec__dodpt in node.out_vars:
        if ayyec__dodpt.name in array_dists:
            khzoq__gahi = Distribution(min(khzoq__gahi.value, array_dists[
                ayyec__dodpt.name].value))
    for ayyec__dodpt in node.out_vars:
        array_dists[ayyec__dodpt.name] = khzoq__gahi


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        if node.connector_typ == 'sql':
            if len(node.out_vars) > 2:
                typeinferer.lock_type(node.out_vars[2].name, node.
                    file_list_type, loc=node.loc)
            if len(node.out_vars) > 3:
                typeinferer.lock_type(node.out_vars[3].name, node.
                    snapshot_id_type, loc=node.loc)
        return
    for rqqze__agd, esq__jqcnx in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(rqqze__agd.name, esq__jqcnx, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    rpw__neep = []
    for rqqze__agd in node.out_vars:
        uvsrf__kft = visit_vars_inner(rqqze__agd, callback, cbdata)
        rpw__neep.append(uvsrf__kft)
    node.out_vars = rpw__neep
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for blz__mqkm in node.filters:
            for mmyz__gtik in range(len(blz__mqkm)):
                nkk__ollld = blz__mqkm[mmyz__gtik]
                blz__mqkm[mmyz__gtik] = nkk__ollld[0], nkk__ollld[1
                    ], visit_vars_inner(nkk__ollld[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({ayyec__dodpt.name for ayyec__dodpt in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for xxen__xnaa in node.filters:
            for ayyec__dodpt in xxen__xnaa:
                if isinstance(ayyec__dodpt[2], ir.Var):
                    use_set.add(ayyec__dodpt[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    rzsa__pwxrd = set(ayyec__dodpt.name for ayyec__dodpt in node.out_vars)
    return set(), rzsa__pwxrd


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    rpw__neep = []
    for rqqze__agd in node.out_vars:
        uvsrf__kft = replace_vars_inner(rqqze__agd, var_dict)
        rpw__neep.append(uvsrf__kft)
    node.out_vars = rpw__neep
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for blz__mqkm in node.filters:
            for mmyz__gtik in range(len(blz__mqkm)):
                nkk__ollld = blz__mqkm[mmyz__gtik]
                blz__mqkm[mmyz__gtik] = nkk__ollld[0], nkk__ollld[1
                    ], replace_vars_inner(nkk__ollld[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for rqqze__agd in node.out_vars:
        hohro__qlisu = definitions[rqqze__agd.name]
        if node not in hohro__qlisu:
            hohro__qlisu.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        ngwqf__lsk = [ayyec__dodpt[2] for xxen__xnaa in filters for
            ayyec__dodpt in xxen__xnaa]
        fxc__rqagv = set()
        for vlw__ykr in ngwqf__lsk:
            if isinstance(vlw__ykr, ir.Var):
                if vlw__ykr.name not in fxc__rqagv:
                    filter_vars.append(vlw__ykr)
                fxc__rqagv.add(vlw__ykr.name)
        return {ayyec__dodpt.name: f'f{mmyz__gtik}' for mmyz__gtik,
            ayyec__dodpt in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {mmyz__gtik for mmyz__gtik in used_columns if mmyz__gtik <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    ejgpq__smki = {}
    for mmyz__gtik, enig__yjef in enumerate(df_type.data):
        if isinstance(enig__yjef, bodo.IntegerArrayType):
            ulmb__yeg = enig__yjef.get_pandas_scalar_type_instance
            if ulmb__yeg not in ejgpq__smki:
                ejgpq__smki[ulmb__yeg] = []
            ejgpq__smki[ulmb__yeg].append(df.columns[mmyz__gtik])
    for esq__jqcnx, zfshl__alvw in ejgpq__smki.items():
        df[zfshl__alvw] = df[zfshl__alvw].astype(esq__jqcnx)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    yusnw__fyr = node.out_vars[0].name
    assert isinstance(typemap[yusnw__fyr], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, moiw__niaf, rbdp__pdc = get_live_column_nums_block(
            column_live_map, equiv_vars, yusnw__fyr)
        if not (moiw__niaf or rbdp__pdc):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    yhft__mqc = False
    if array_dists is not None:
        whhur__cgy = node.out_vars[0].name
        yhft__mqc = array_dists[whhur__cgy] in (Distribution.OneD,
            Distribution.OneD_Var)
        nhwl__fujd = node.out_vars[1].name
        assert typemap[nhwl__fujd
            ] == types.none or not yhft__mqc or array_dists[nhwl__fujd] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return yhft__mqc


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    euts__ufu = 'None'
    uix__rwfjz = 'None'
    if filters:
        zkns__lye = []
        jgo__xdezr = []
        kmicp__byv = False
        orig_colname_map = {pkd__xpkc: mmyz__gtik for mmyz__gtik, pkd__xpkc in
            enumerate(col_names)}
        for blz__mqkm in filters:
            ept__wdk = []
            nwf__ifpoj = []
            for ayyec__dodpt in blz__mqkm:
                if isinstance(ayyec__dodpt[2], ir.Var):
                    bdnb__cwcm, wzu__rhah = determine_filter_cast(
                        original_out_types, typemap, ayyec__dodpt,
                        orig_colname_map, partition_names, source)
                    if ayyec__dodpt[1] == 'in':
                        znfzf__qovg = (
                            f"(ds.field('{ayyec__dodpt[0]}').isin({filter_map[ayyec__dodpt[2].name]}))"
                            )
                    else:
                        znfzf__qovg = (
                            f"(ds.field('{ayyec__dodpt[0]}'){bdnb__cwcm} {ayyec__dodpt[1]} ds.scalar({filter_map[ayyec__dodpt[2].name]}){wzu__rhah})"
                            )
                else:
                    assert ayyec__dodpt[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if ayyec__dodpt[1] == 'is not':
                        wawe__vag = '~'
                    else:
                        wawe__vag = ''
                    znfzf__qovg = (
                        f"({wawe__vag}ds.field('{ayyec__dodpt[0]}').is_null())"
                        )
                nwf__ifpoj.append(znfzf__qovg)
                if not kmicp__byv:
                    if ayyec__dodpt[0] in partition_names and isinstance(
                        ayyec__dodpt[2], ir.Var):
                        if output_dnf:
                            nsiox__sgpau = (
                                f"('{ayyec__dodpt[0]}', '{ayyec__dodpt[1]}', {filter_map[ayyec__dodpt[2].name]})"
                                )
                        else:
                            nsiox__sgpau = znfzf__qovg
                        ept__wdk.append(nsiox__sgpau)
                    elif ayyec__dodpt[0] in partition_names and not isinstance(
                        ayyec__dodpt[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            nsiox__sgpau = (
                                f"('{ayyec__dodpt[0]}', '{ayyec__dodpt[1]}', '{ayyec__dodpt[2]}')"
                                )
                        else:
                            nsiox__sgpau = znfzf__qovg
                        ept__wdk.append(nsiox__sgpau)
            lwdhf__drqj = ''
            if ept__wdk:
                if output_dnf:
                    lwdhf__drqj = ', '.join(ept__wdk)
                else:
                    lwdhf__drqj = ' & '.join(ept__wdk)
            else:
                kmicp__byv = True
            wwvby__trba = ' & '.join(nwf__ifpoj)
            if lwdhf__drqj:
                if output_dnf:
                    zkns__lye.append(f'[{lwdhf__drqj}]')
                else:
                    zkns__lye.append(f'({lwdhf__drqj})')
            jgo__xdezr.append(f'({wwvby__trba})')
        if output_dnf:
            vxy__sfvr = ', '.join(zkns__lye)
        else:
            vxy__sfvr = ' | '.join(zkns__lye)
        ssh__smnda = ' | '.join(jgo__xdezr)
        if vxy__sfvr and not kmicp__byv:
            if output_dnf:
                euts__ufu = f'[{vxy__sfvr}]'
            else:
                euts__ufu = f'({vxy__sfvr})'
        uix__rwfjz = f'({ssh__smnda})'
    return euts__ufu, uix__rwfjz


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    ebp__hehde = filter_val[0]
    rlp__ztorp = col_types[orig_colname_map[ebp__hehde]]
    mtna__nwib = bodo.utils.typing.element_type(rlp__ztorp)
    if source == 'parquet' and ebp__hehde in partition_names:
        if mtna__nwib == types.unicode_type:
            twza__uwmaq = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(mtna__nwib, types.Integer):
            twza__uwmaq = f'.cast(pyarrow.{mtna__nwib.name}(), safe=False)'
        else:
            twza__uwmaq = ''
    else:
        twza__uwmaq = ''
    suq__fkwxb = typemap[filter_val[2].name]
    if isinstance(suq__fkwxb, (types.List, types.Set)):
        xjr__axve = suq__fkwxb.dtype
    elif is_array_typ(suq__fkwxb):
        xjr__axve = suq__fkwxb.dtype
    else:
        xjr__axve = suq__fkwxb
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mtna__nwib,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(xjr__axve,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([mtna__nwib, xjr__axve]):
        if not bodo.utils.typing.is_safe_arrow_cast(mtna__nwib, xjr__axve):
            raise BodoError(
                f'Unsupported Arrow cast from {mtna__nwib} to {xjr__axve} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if mtna__nwib == types.unicode_type and xjr__axve in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif xjr__axve == types.unicode_type and mtna__nwib in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(suq__fkwxb, (types.List, types.Set)):
                gypy__fsj = 'list' if isinstance(suq__fkwxb, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {gypy__fsj} values with isin filter pushdown.'
                    )
            return twza__uwmaq, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif mtna__nwib == bodo.datetime_date_type and xjr__axve in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif xjr__axve == bodo.datetime_date_type and mtna__nwib in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return twza__uwmaq, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return twza__uwmaq, ''
