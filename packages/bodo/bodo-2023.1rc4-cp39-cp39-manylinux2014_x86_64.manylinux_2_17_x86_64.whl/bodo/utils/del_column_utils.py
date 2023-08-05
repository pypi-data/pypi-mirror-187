"""Helper information to keep table column deletion
pass organized. This contains information about all
table operations for optimizations.
"""
from typing import Dict, Tuple
from numba.core import ir, types
from bodo.hiframes.table import TableType
table_usecol_funcs = {('get_table_data', 'bodo.hiframes.table'), (
    'table_filter', 'bodo.hiframes.table'), ('table_subset',
    'bodo.hiframes.table'), ('set_table_data', 'bodo.hiframes.table'), (
    'set_table_data_null', 'bodo.hiframes.table'), (
    'generate_mappable_table_func', 'bodo.utils.table_utils'), (
    'table_astype', 'bodo.utils.table_utils'), ('generate_table_nbytes',
    'bodo.utils.table_utils'), ('table_concat', 'bodo.utils.table_utils'),
    ('py_data_to_cpp_table', 'bodo.libs.array'), ('logical_table_to_table',
    'bodo.hiframes.table')}


def is_table_use_column_ops(fdef: Tuple[str, str], args, typemap):
    return fdef in table_usecol_funcs and len(args) > 0 and isinstance(typemap
        [args[0].name], TableType)


def get_table_used_columns(fdef: Tuple[str, str], call_expr: ir.Expr,
    typemap: Dict[str, types.Type]):
    if fdef == ('get_table_data', 'bodo.hiframes.table'):
        pec__nrn = typemap[call_expr.args[1].name].literal_value
        return {pec__nrn}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        xyav__bknpo = dict(call_expr.kws)
        if 'used_cols' in xyav__bknpo:
            zsjfb__jldc = xyav__bknpo['used_cols']
            cpl__gzi = typemap[zsjfb__jldc.name]
            cpl__gzi = cpl__gzi.instance_type
            return set(cpl__gzi.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        zsjfb__jldc = call_expr.args[1]
        cpl__gzi = typemap[zsjfb__jldc.name]
        cpl__gzi = cpl__gzi.instance_type
        return set(cpl__gzi.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        mkmbh__noht = call_expr.args[1]
        byzyo__zhbz = typemap[mkmbh__noht.name]
        byzyo__zhbz = byzyo__zhbz.instance_type
        eiy__gkftl = byzyo__zhbz.meta
        xyav__bknpo = dict(call_expr.kws)
        if 'used_cols' in xyav__bknpo:
            zsjfb__jldc = xyav__bknpo['used_cols']
            cpl__gzi = typemap[zsjfb__jldc.name]
            cpl__gzi = cpl__gzi.instance_type
            trrsx__znqzn = set(cpl__gzi.meta)
            mxf__hys = set()
            for pyrmd__byaxz, phpaz__kvq in enumerate(eiy__gkftl):
                if pyrmd__byaxz in trrsx__znqzn:
                    mxf__hys.add(phpaz__kvq)
            return mxf__hys
        else:
            return set(eiy__gkftl)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        ivexx__yep = typemap[call_expr.args[2].name].instance_type.meta
        wpv__zssm = len(typemap[call_expr.args[0].name].arr_types)
        return set(pyrmd__byaxz for pyrmd__byaxz in ivexx__yep if 
            pyrmd__byaxz < wpv__zssm)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        qad__jcpp = typemap[call_expr.args[2].name].instance_type.meta
        lkm__urnxl = len(typemap[call_expr.args[0].name].arr_types)
        xyav__bknpo = dict(call_expr.kws)
        if 'used_cols' in xyav__bknpo:
            trrsx__znqzn = set(typemap[xyav__bknpo['used_cols'].name].
                instance_type.meta)
            jul__aanqm = set()
            for mkqh__ngt, zvog__gtw in enumerate(qad__jcpp):
                if mkqh__ngt in trrsx__znqzn and zvog__gtw < lkm__urnxl:
                    jul__aanqm.add(zvog__gtw)
            return jul__aanqm
        else:
            return set(pyrmd__byaxz for pyrmd__byaxz in qad__jcpp if 
                pyrmd__byaxz < lkm__urnxl)
    return None
