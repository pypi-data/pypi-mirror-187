"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.ArrayCompatible):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        myare__ltxbb = [('data', types.Tuple(fe_type.array_types)), (
            'names', types.Tuple(fe_type.names_typ)), ('name', fe_type.
            name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, myare__ltxbb)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[dvlox__dtbl].values) for
        dvlox__dtbl in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (xedwy__nyze) for xedwy__nyze in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    nnnbv__axxaq = c.context.insert_const_string(c.builder.module, 'pandas')
    kks__xmkee = c.pyapi.import_module_noblock(nnnbv__axxaq)
    twwef__sot = c.pyapi.object_getattr_string(kks__xmkee, 'MultiIndex')
    jrv__ncp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), jrv__ncp.data
        )
    uddll__vaxhe = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        jrv__ncp.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), jrv__ncp.names)
    hpwr__hir = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        jrv__ncp.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, jrv__ncp.name)
    dotuw__chs = c.pyapi.from_native_value(typ.name_typ, jrv__ncp.name, c.
        env_manager)
    pgpq__ijcc = c.pyapi.borrow_none()
    vdbt__ltfnh = c.pyapi.call_method(twwef__sot, 'from_arrays', (
        uddll__vaxhe, pgpq__ijcc, hpwr__hir))
    c.pyapi.object_setattr_string(vdbt__ltfnh, 'name', dotuw__chs)
    c.pyapi.decref(uddll__vaxhe)
    c.pyapi.decref(hpwr__hir)
    c.pyapi.decref(dotuw__chs)
    c.pyapi.decref(kks__xmkee)
    c.pyapi.decref(twwef__sot)
    c.context.nrt.decref(c.builder, typ, val)
    return vdbt__ltfnh


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    lnkdl__zujw = []
    vnjh__zephe = []
    for dvlox__dtbl in range(typ.nlevels):
        yppl__esonp = c.pyapi.unserialize(c.pyapi.serialize_object(dvlox__dtbl)
            )
        bblwx__rot = c.pyapi.call_method(val, 'get_level_values', (
            yppl__esonp,))
        mflpz__cdc = c.pyapi.object_getattr_string(bblwx__rot, 'values')
        c.pyapi.decref(bblwx__rot)
        c.pyapi.decref(yppl__esonp)
        lpwl__zkc = c.pyapi.to_native_value(typ.array_types[dvlox__dtbl],
            mflpz__cdc).value
        lnkdl__zujw.append(lpwl__zkc)
        vnjh__zephe.append(mflpz__cdc)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, lnkdl__zujw)
    else:
        data = cgutils.pack_struct(c.builder, lnkdl__zujw)
    hpwr__hir = c.pyapi.object_getattr_string(val, 'names')
    tqavl__iml = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    uxb__cabbe = c.pyapi.call_function_objargs(tqavl__iml, (hpwr__hir,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), uxb__cabbe
        ).value
    dotuw__chs = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, dotuw__chs).value
    jrv__ncp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jrv__ncp.data = data
    jrv__ncp.names = names
    jrv__ncp.name = name
    for mflpz__cdc in vnjh__zephe:
        c.pyapi.decref(mflpz__cdc)
    c.pyapi.decref(hpwr__hir)
    c.pyapi.decref(tqavl__iml)
    c.pyapi.decref(uxb__cabbe)
    c.pyapi.decref(dotuw__chs)
    return NativeValue(jrv__ncp._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    cvduq__qdm = 'pandas.MultiIndex.from_product'
    knlq__dwm = dict(sortorder=sortorder)
    dqoeo__ifyf = dict(sortorder=None)
    check_unsupported_args(cvduq__qdm, knlq__dwm, dqoeo__ifyf, package_name
        ='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{cvduq__qdm}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{cvduq__qdm}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{cvduq__qdm}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    bqro__kdn = MultiIndexType(array_types, names_typ)
    mwfgu__gvlvq = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, mwfgu__gvlvq, bqro__kdn)
    onb__omzn = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{mwfgu__gvlvq}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    sqs__rpi = {}
    exec(onb__omzn, globals(), sqs__rpi)
    whc__wqbto = sqs__rpi['impl']
    return whc__wqbto


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        ihpv__fwnhp, hlxi__pkh, zvq__igln = args
        bsqaa__izqir = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        bsqaa__izqir.data = ihpv__fwnhp
        bsqaa__izqir.names = hlxi__pkh
        bsqaa__izqir.name = zvq__igln
        context.nrt.incref(builder, signature.args[0], ihpv__fwnhp)
        context.nrt.incref(builder, signature.args[1], hlxi__pkh)
        context.nrt.incref(builder, signature.args[2], zvq__igln)
        return bsqaa__izqir._getvalue()
    hbz__rth = MultiIndexType(data.types, names.types, name)
    return hbz__rth(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        ros__pgrjg = len(I.array_types)
        onb__omzn = 'def impl(I, ind):\n'
        onb__omzn += '  data = I._data\n'
        onb__omzn += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{dvlox__dtbl}][ind])' for
            dvlox__dtbl in range(ros__pgrjg))))
        sqs__rpi = {}
        exec(onb__omzn, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, sqs__rpi)
        whc__wqbto = sqs__rpi['impl']
        return whc__wqbto


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    ahjxf__njeps, qvcm__curt = sig.args
    if ahjxf__njeps != qvcm__curt:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
