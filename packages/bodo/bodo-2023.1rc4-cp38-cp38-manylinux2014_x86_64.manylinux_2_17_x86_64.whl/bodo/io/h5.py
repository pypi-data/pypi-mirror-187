"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        fcr__ajco = self._get_h5_type(lhs, rhs)
        if fcr__ajco is not None:
            jwkh__vguma = str(fcr__ajco.dtype)
            yeszz__eynse = 'def _h5_read_impl(dset, index):\n'
            yeszz__eynse += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(fcr__ajco.ndim, jwkh__vguma))
            glpfb__edv = {}
            exec(yeszz__eynse, {}, glpfb__edv)
            ivsx__dsq = glpfb__edv['_h5_read_impl']
            ems__qfij = compile_to_numba_ir(ivsx__dsq, {'bodo': bodo}
                ).blocks.popitem()[1]
            iiak__fasvq = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(ems__qfij, [rhs.value, iiak__fasvq])
            qkx__nkxi = ems__qfij.body[:-3]
            qkx__nkxi[-1].target = assign.target
            return qkx__nkxi
        return None

    def _get_h5_type(self, lhs, rhs):
        fcr__ajco = self._get_h5_type_locals(lhs)
        if fcr__ajco is not None:
            return fcr__ajco
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        iiak__fasvq = rhs.index if rhs.op == 'getitem' else rhs.index_var
        mjkn__wfsj = guard(find_const, self.func_ir, iiak__fasvq)
        require(not isinstance(mjkn__wfsj, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            zwyso__akly = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            ylt__qrugf = get_const_value_inner(self.func_ir, zwyso__akly,
                arg_types=self.arg_types)
            obj_name_list.append(ylt__qrugf)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        yxtpr__tzecs = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        herbp__ufa = h5py.File(yxtpr__tzecs, 'r')
        ojwgv__dmno = herbp__ufa
        for ylt__qrugf in obj_name_list:
            ojwgv__dmno = ojwgv__dmno[ylt__qrugf]
        require(isinstance(ojwgv__dmno, h5py.Dataset))
        fur__tizc = len(ojwgv__dmno.shape)
        mduo__nyrpr = numba.np.numpy_support.from_dtype(ojwgv__dmno.dtype)
        herbp__ufa.close()
        return types.Array(mduo__nyrpr, fur__tizc, 'C')

    def _get_h5_type_locals(self, varname):
        aevue__lxlhl = self.locals.pop(varname, None)
        if aevue__lxlhl is None and varname is not None:
            aevue__lxlhl = self.flags.h5_types.get(varname, None)
        return aevue__lxlhl
