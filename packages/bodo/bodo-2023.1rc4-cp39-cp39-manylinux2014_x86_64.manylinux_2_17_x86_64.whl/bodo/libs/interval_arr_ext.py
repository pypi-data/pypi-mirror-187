"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vqh__jfx = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, vqh__jfx)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        rmhk__rne, awhco__nvc = args
        sfzzm__loyp = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        sfzzm__loyp.left = rmhk__rne
        sfzzm__loyp.right = awhco__nvc
        context.nrt.incref(builder, signature.args[0], rmhk__rne)
        context.nrt.incref(builder, signature.args[1], awhco__nvc)
        return sfzzm__loyp._getvalue()
    mzj__elnn = IntervalArrayType(left)
    gfdh__nrbs = mzj__elnn(left, right)
    return gfdh__nrbs, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    jwkx__vntev = []
    for awqcm__voo in args:
        httt__rruz = equiv_set.get_shape(awqcm__voo)
        if httt__rruz is not None:
            jwkx__vntev.append(httt__rruz[0])
    if len(jwkx__vntev) > 1:
        equiv_set.insert_equiv(*jwkx__vntev)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    sfzzm__loyp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, sfzzm__loyp.left)
    bya__ytj = c.pyapi.from_native_value(typ.arr_type, sfzzm__loyp.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, sfzzm__loyp.right)
    zgsnb__vdjoe = c.pyapi.from_native_value(typ.arr_type, sfzzm__loyp.
        right, c.env_manager)
    xgdm__uuxna = c.context.insert_const_string(c.builder.module, 'pandas')
    kdw__kgtwk = c.pyapi.import_module_noblock(xgdm__uuxna)
    gph__tbgir = c.pyapi.object_getattr_string(kdw__kgtwk, 'arrays')
    vjzq__nywm = c.pyapi.object_getattr_string(gph__tbgir, 'IntervalArray')
    qfdxu__sgz = c.pyapi.call_method(vjzq__nywm, 'from_arrays', (bya__ytj,
        zgsnb__vdjoe))
    c.pyapi.decref(bya__ytj)
    c.pyapi.decref(zgsnb__vdjoe)
    c.pyapi.decref(kdw__kgtwk)
    c.pyapi.decref(gph__tbgir)
    c.pyapi.decref(vjzq__nywm)
    c.context.nrt.decref(c.builder, typ, val)
    return qfdxu__sgz


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    bya__ytj = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, bya__ytj).value
    c.pyapi.decref(bya__ytj)
    zgsnb__vdjoe = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, zgsnb__vdjoe).value
    c.pyapi.decref(zgsnb__vdjoe)
    sfzzm__loyp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    sfzzm__loyp.left = left
    sfzzm__loyp.right = right
    vbpb__xxfda = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sfzzm__loyp._getvalue(), is_error=vbpb__xxfda)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
