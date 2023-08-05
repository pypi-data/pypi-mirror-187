"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        tsa__fitdh = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, tsa__fitdh)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        isdc__axnbb = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        isdc__axnbb.data = data_tuple
        isdc__axnbb.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return isdc__axnbb._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    rewot__vjtds = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, rewot__vjtds.data)
    c.context.nrt.incref(c.builder, typ.null_typ, rewot__vjtds.null_values)
    kxp__vdwh = c.pyapi.from_native_value(typ.tuple_typ, rewot__vjtds.data,
        c.env_manager)
    xdi__yjl = c.pyapi.from_native_value(typ.null_typ, rewot__vjtds.
        null_values, c.env_manager)
    njp__imdn = c.context.get_constant(types.int64, len(typ.tuple_typ))
    jipc__crd = c.pyapi.list_new(njp__imdn)
    with cgutils.for_range(c.builder, njp__imdn) as gsha__ukp:
        i = gsha__ukp.index
        wojw__lyh = c.pyapi.long_from_longlong(i)
        iiu__oqj = c.pyapi.object_getitem(xdi__yjl, wojw__lyh)
        ievkw__hyepq = c.pyapi.to_native_value(types.bool_, iiu__oqj).value
        with c.builder.if_else(ievkw__hyepq) as (sdkkp__bxal, ktz__yoes):
            with sdkkp__bxal:
                c.pyapi.list_setitem(jipc__crd, i, c.pyapi.make_none())
            with ktz__yoes:
                rlyf__ewi = c.pyapi.object_getitem(kxp__vdwh, wojw__lyh)
                c.pyapi.list_setitem(jipc__crd, i, rlyf__ewi)
        c.pyapi.decref(wojw__lyh)
        c.pyapi.decref(iiu__oqj)
    mpbi__hpyr = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    rfuh__aruye = c.pyapi.call_function_objargs(mpbi__hpyr, (jipc__crd,))
    c.pyapi.decref(kxp__vdwh)
    c.pyapi.decref(xdi__yjl)
    c.pyapi.decref(mpbi__hpyr)
    c.pyapi.decref(jipc__crd)
    c.context.nrt.decref(c.builder, typ, val)
    return rfuh__aruye


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    isdc__axnbb = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (isdc__axnbb.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    oldw__gcxdm = 'def impl(val1, val2):\n'
    oldw__gcxdm += '    data_tup1 = val1._data\n'
    oldw__gcxdm += '    null_tup1 = val1._null_values\n'
    oldw__gcxdm += '    data_tup2 = val2._data\n'
    oldw__gcxdm += '    null_tup2 = val2._null_values\n'
    qzx__msotm = val1._tuple_typ
    for i in range(len(qzx__msotm)):
        oldw__gcxdm += f'    null1_{i} = null_tup1[{i}]\n'
        oldw__gcxdm += f'    null2_{i} = null_tup2[{i}]\n'
        oldw__gcxdm += f'    data1_{i} = data_tup1[{i}]\n'
        oldw__gcxdm += f'    data2_{i} = data_tup2[{i}]\n'
        oldw__gcxdm += f'    if null1_{i} != null2_{i}:\n'
        oldw__gcxdm += '        return False\n'
        oldw__gcxdm += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        oldw__gcxdm += f'        return False\n'
    oldw__gcxdm += f'    return True\n'
    mvuu__cas = {}
    exec(oldw__gcxdm, {}, mvuu__cas)
    impl = mvuu__cas['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    oldw__gcxdm = 'def impl(nullable_tup):\n'
    oldw__gcxdm += '    data_tup = nullable_tup._data\n'
    oldw__gcxdm += '    null_tup = nullable_tup._null_values\n'
    oldw__gcxdm += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    oldw__gcxdm += '    acc = _PyHASH_XXPRIME_5\n'
    qzx__msotm = nullable_tup._tuple_typ
    for i in range(len(qzx__msotm)):
        oldw__gcxdm += f'    null_val_{i} = null_tup[{i}]\n'
        oldw__gcxdm += f'    null_lane_{i} = hash(null_val_{i})\n'
        oldw__gcxdm += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        oldw__gcxdm += '        return -1\n'
        oldw__gcxdm += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        oldw__gcxdm += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        oldw__gcxdm += '    acc *= _PyHASH_XXPRIME_1\n'
        oldw__gcxdm += f'    if not null_val_{i}:\n'
        oldw__gcxdm += f'        lane_{i} = hash(data_tup[{i}])\n'
        oldw__gcxdm += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        oldw__gcxdm += f'            return -1\n'
        oldw__gcxdm += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        oldw__gcxdm += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        oldw__gcxdm += '        acc *= _PyHASH_XXPRIME_1\n'
    oldw__gcxdm += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    oldw__gcxdm += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    oldw__gcxdm += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    oldw__gcxdm += '    return numba.cpython.hashing.process_return(acc)\n'
    mvuu__cas = {}
    exec(oldw__gcxdm, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, mvuu__cas)
    impl = mvuu__cas['impl']
    return impl
