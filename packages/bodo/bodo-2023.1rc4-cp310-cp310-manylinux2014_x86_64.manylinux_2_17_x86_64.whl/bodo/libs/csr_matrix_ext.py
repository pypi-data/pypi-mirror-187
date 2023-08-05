"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ujk__cstt = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, ujk__cstt)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        tjih__lsu, onkyb__qdv, qgj__odgbe, obk__qinq = args
        ylx__wusk = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        ylx__wusk.data = tjih__lsu
        ylx__wusk.indices = onkyb__qdv
        ylx__wusk.indptr = qgj__odgbe
        ylx__wusk.shape = obk__qinq
        context.nrt.incref(builder, signature.args[0], tjih__lsu)
        context.nrt.incref(builder, signature.args[1], onkyb__qdv)
        context.nrt.incref(builder, signature.args[2], qgj__odgbe)
        return ylx__wusk._getvalue()
    lpp__vob = CSRMatrixType(data_t.dtype, indices_t.dtype)
    nxn__orahk = lpp__vob(data_t, indices_t, indptr_t, types.UniTuple(types
        .int64, 2))
    return nxn__orahk, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    ylx__wusk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zguit__pwi = c.pyapi.object_getattr_string(val, 'data')
    ciwq__ova = c.pyapi.object_getattr_string(val, 'indices')
    ziz__hnx = c.pyapi.object_getattr_string(val, 'indptr')
    qicc__nlhgo = c.pyapi.object_getattr_string(val, 'shape')
    ylx__wusk.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        zguit__pwi).value
    ylx__wusk.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), ciwq__ova).value
    ylx__wusk.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), ziz__hnx).value
    ylx__wusk.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), qicc__nlhgo).value
    c.pyapi.decref(zguit__pwi)
    c.pyapi.decref(ciwq__ova)
    c.pyapi.decref(ziz__hnx)
    c.pyapi.decref(qicc__nlhgo)
    nec__auna = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ylx__wusk._getvalue(), is_error=nec__auna)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    vfs__xyzg = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    ehhta__lxst = c.pyapi.import_module_noblock(vfs__xyzg)
    ylx__wusk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        ylx__wusk.data)
    zguit__pwi = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        ylx__wusk.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ylx__wusk.indices)
    ciwq__ova = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), ylx__wusk.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ylx__wusk.indptr)
    ziz__hnx = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'),
        ylx__wusk.indptr, c.env_manager)
    qicc__nlhgo = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        ylx__wusk.shape, c.env_manager)
    fjm__gfek = c.pyapi.tuple_pack([zguit__pwi, ciwq__ova, ziz__hnx])
    mzfq__driql = c.pyapi.call_method(ehhta__lxst, 'csr_matrix', (fjm__gfek,
        qicc__nlhgo))
    c.pyapi.decref(fjm__gfek)
    c.pyapi.decref(zguit__pwi)
    c.pyapi.decref(ciwq__ova)
    c.pyapi.decref(ziz__hnx)
    c.pyapi.decref(qicc__nlhgo)
    c.pyapi.decref(ehhta__lxst)
    c.context.nrt.decref(c.builder, typ, val)
    return mzfq__driql


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    fdux__lnvqf = A.dtype
    vvo__qnj = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            vjbmq__rvf, kuw__jxwg = A.shape
            uoo__dljug = numba.cpython.unicode._normalize_slice(idx[0],
                vjbmq__rvf)
            fcfp__yxmgi = numba.cpython.unicode._normalize_slice(idx[1],
                kuw__jxwg)
            if uoo__dljug.step != 1 or fcfp__yxmgi.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            ffiz__tzyk = uoo__dljug.start
            lpd__koyv = uoo__dljug.stop
            zzgk__fdqv = fcfp__yxmgi.start
            pwrt__yfbuw = fcfp__yxmgi.stop
            pyprj__pdzwo = A.indptr
            gjzt__kiwe = A.indices
            dzc__imik = A.data
            chpj__pfdc = lpd__koyv - ffiz__tzyk
            uhax__gzdp = pwrt__yfbuw - zzgk__fdqv
            ybygx__rnjed = 0
            bkj__hzme = 0
            for yyn__zkwp in range(chpj__pfdc):
                iipwj__kwt = pyprj__pdzwo[ffiz__tzyk + yyn__zkwp]
                rvw__vty = pyprj__pdzwo[ffiz__tzyk + yyn__zkwp + 1]
                for uqawc__styae in range(iipwj__kwt, rvw__vty):
                    if gjzt__kiwe[uqawc__styae] >= zzgk__fdqv and gjzt__kiwe[
                        uqawc__styae] < pwrt__yfbuw:
                        ybygx__rnjed += 1
            ygyax__ume = np.empty(chpj__pfdc + 1, vvo__qnj)
            lbzwr__paz = np.empty(ybygx__rnjed, vvo__qnj)
            hbaa__bfq = np.empty(ybygx__rnjed, fdux__lnvqf)
            ygyax__ume[0] = 0
            for yyn__zkwp in range(chpj__pfdc):
                iipwj__kwt = pyprj__pdzwo[ffiz__tzyk + yyn__zkwp]
                rvw__vty = pyprj__pdzwo[ffiz__tzyk + yyn__zkwp + 1]
                for uqawc__styae in range(iipwj__kwt, rvw__vty):
                    if gjzt__kiwe[uqawc__styae] >= zzgk__fdqv and gjzt__kiwe[
                        uqawc__styae] < pwrt__yfbuw:
                        lbzwr__paz[bkj__hzme] = gjzt__kiwe[uqawc__styae
                            ] - zzgk__fdqv
                        hbaa__bfq[bkj__hzme] = dzc__imik[uqawc__styae]
                        bkj__hzme += 1
                ygyax__ume[yyn__zkwp + 1] = bkj__hzme
            return init_csr_matrix(hbaa__bfq, lbzwr__paz, ygyax__ume, (
                chpj__pfdc, uhax__gzdp))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == vvo__qnj:

        def impl(A, idx):
            vjbmq__rvf, kuw__jxwg = A.shape
            pyprj__pdzwo = A.indptr
            gjzt__kiwe = A.indices
            dzc__imik = A.data
            chpj__pfdc = len(idx)
            ybygx__rnjed = 0
            bkj__hzme = 0
            for yyn__zkwp in range(chpj__pfdc):
                vigu__wva = idx[yyn__zkwp]
                iipwj__kwt = pyprj__pdzwo[vigu__wva]
                rvw__vty = pyprj__pdzwo[vigu__wva + 1]
                ybygx__rnjed += rvw__vty - iipwj__kwt
            ygyax__ume = np.empty(chpj__pfdc + 1, vvo__qnj)
            lbzwr__paz = np.empty(ybygx__rnjed, vvo__qnj)
            hbaa__bfq = np.empty(ybygx__rnjed, fdux__lnvqf)
            ygyax__ume[0] = 0
            for yyn__zkwp in range(chpj__pfdc):
                vigu__wva = idx[yyn__zkwp]
                iipwj__kwt = pyprj__pdzwo[vigu__wva]
                rvw__vty = pyprj__pdzwo[vigu__wva + 1]
                lbzwr__paz[bkj__hzme:bkj__hzme + rvw__vty - iipwj__kwt
                    ] = gjzt__kiwe[iipwj__kwt:rvw__vty]
                hbaa__bfq[bkj__hzme:bkj__hzme + rvw__vty - iipwj__kwt
                    ] = dzc__imik[iipwj__kwt:rvw__vty]
                bkj__hzme += rvw__vty - iipwj__kwt
                ygyax__ume[yyn__zkwp + 1] = bkj__hzme
            uilro__yfr = init_csr_matrix(hbaa__bfq, lbzwr__paz, ygyax__ume,
                (chpj__pfdc, kuw__jxwg))
            return uilro__yfr
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
