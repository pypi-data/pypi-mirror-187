"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.ir_utils import guard
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_none, is_overload_true, raise_bodo_error, to_str_arr_if_dict_array, unwrap_typeref
from bodo.utils.utils import is_whole_slice


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            kfcx__joja = 0
            fru__rmyb = []
            for i in range(usecols[-1] + 1):
                if i == usecols[kfcx__joja]:
                    fru__rmyb.append(arrs[kfcx__joja])
                    kfcx__joja += 1
                else:
                    fru__rmyb.append(None)
            for rhasm__uyqgz in range(usecols[-1] + 1, num_arrs):
                fru__rmyb.append(None)
            self.arrays = fru__rmyb
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((jqoyd__rrbf == kjyre__lwi).all() for 
            jqoyd__rrbf, kjyre__lwi in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        pzaya__baixx = len(self.arrays)
        sqx__vwbe = dict(zip(range(pzaya__baixx), self.arrays))
        df = pd.DataFrame(sqx__vwbe, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        baxfe__itgwd = []
        cuqwt__iplg = []
        xcfz__sfsw = {}
        gfuk__ryq = {}
        yopgs__shdzh = defaultdict(int)
        eqxg__bawgp = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in xcfz__sfsw:
                    ixcpy__thdi = len(xcfz__sfsw)
                    xcfz__sfsw[t] = ixcpy__thdi
                    gfuk__ryq[ixcpy__thdi] = t
                ekzc__obxtf = xcfz__sfsw[t]
                baxfe__itgwd.append(ekzc__obxtf)
                cuqwt__iplg.append(yopgs__shdzh[ekzc__obxtf])
                yopgs__shdzh[ekzc__obxtf] += 1
                eqxg__bawgp[ekzc__obxtf].append(i)
        self.block_nums = baxfe__itgwd
        self.block_offsets = cuqwt__iplg
        self.type_to_blk = xcfz__sfsw
        self.blk_to_type = gfuk__ryq
        self.block_to_arr_ind = eqxg__bawgp
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(arr) for arr in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            qaly__ykkgo = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            qaly__ykkgo = [(f'block_{ekzc__obxtf}', types.List(t)) for t,
                ekzc__obxtf in fe_type.type_to_blk.items()]
        qaly__ykkgo.append(('parent', types.pyobject))
        qaly__ykkgo.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, qaly__ykkgo)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    spuz__dxhav = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    rrp__ekakc = c.pyapi.make_none()
    vjorn__pvcjl = c.context.get_constant(types.int64, 0)
    ealtv__bfwp = cgutils.alloca_once_value(c.builder, vjorn__pvcjl)
    for t, ekzc__obxtf in typ.type_to_blk.items():
        zod__xzi = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[ekzc__obxtf]))
        rhasm__uyqgz, dxwl__owm = ListInstance.allocate_ex(c.context, c.
            builder, types.List(t), zod__xzi)
        dxwl__owm.size = zod__xzi
        qwkde__vmtf = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[ekzc__obxtf
            ], dtype=np.int64))
        efum__mlga = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, qwkde__vmtf)
        with cgutils.for_range(c.builder, zod__xzi) as hvfnt__yps:
            i = hvfnt__yps.index
            kqkq__vqg = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), efum__mlga, i)
            dltl__wxzyb = c.pyapi.long_from_longlong(kqkq__vqg)
            lbgzi__xppjf = c.pyapi.object_getitem(spuz__dxhav, dltl__wxzyb)
            czihu__gzbp = c.builder.icmp_unsigned('==', lbgzi__xppjf,
                rrp__ekakc)
            with c.builder.if_else(czihu__gzbp) as (qowoh__crss, atsp__snabz):
                with qowoh__crss:
                    opjw__ieu = c.context.get_constant_null(t)
                    dxwl__owm.inititem(i, opjw__ieu, incref=False)
                with atsp__snabz:
                    ltpt__fcv = c.pyapi.call_method(lbgzi__xppjf, '__len__', ()
                        )
                    qwfie__aukw = c.pyapi.long_as_longlong(ltpt__fcv)
                    c.builder.store(qwfie__aukw, ealtv__bfwp)
                    c.pyapi.decref(ltpt__fcv)
                    arr = c.pyapi.to_native_value(t, lbgzi__xppjf).value
                    dxwl__owm.inititem(i, arr, incref=False)
            c.pyapi.decref(lbgzi__xppjf)
            c.pyapi.decref(dltl__wxzyb)
        setattr(table, f'block_{ekzc__obxtf}', dxwl__owm.value)
    table.len = c.builder.load(ealtv__bfwp)
    c.pyapi.decref(spuz__dxhav)
    c.pyapi.decref(rrp__ekakc)
    mmcz__chjpm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=mmcz__chjpm)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        shgs__mcgo = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            fru__rmyb = getattr(table, f'block_{i}')
            ubea__lfk = ListInstance(c.context, c.builder, types.List(t),
                fru__rmyb)
            shgs__mcgo = c.builder.add(shgs__mcgo, ubea__lfk.size)
        getf__jem = c.pyapi.list_new(shgs__mcgo)
        dpx__rndx = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            fru__rmyb = getattr(table, f'block_{i}')
            ubea__lfk = ListInstance(c.context, c.builder, types.List(t),
                fru__rmyb)
            with cgutils.for_range(c.builder, ubea__lfk.size) as hvfnt__yps:
                i = hvfnt__yps.index
                arr = ubea__lfk.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(dpx__rndx, i)
                c.pyapi.list_setitem(getf__jem, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            dpx__rndx = c.builder.add(dpx__rndx, ubea__lfk.size)
        zvqhk__bpbab = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        wyxjq__kdrde = c.pyapi.call_function_objargs(zvqhk__bpbab, (getf__jem,)
            )
        c.pyapi.decref(zvqhk__bpbab)
        c.pyapi.decref(getf__jem)
        c.context.nrt.decref(c.builder, typ, val)
        return wyxjq__kdrde
    getf__jem = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    dikh__mnpe = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, ekzc__obxtf in typ.type_to_blk.items():
        fru__rmyb = getattr(table, f'block_{ekzc__obxtf}')
        ubea__lfk = ListInstance(c.context, c.builder, types.List(t), fru__rmyb
            )
        qwkde__vmtf = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[ekzc__obxtf
            ], dtype=np.int64))
        efum__mlga = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, qwkde__vmtf)
        with cgutils.for_range(c.builder, ubea__lfk.size) as hvfnt__yps:
            i = hvfnt__yps.index
            kqkq__vqg = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), efum__mlga, i)
            arr = ubea__lfk.getitem(i)
            ntjpn__xjgcv = cgutils.alloca_once_value(c.builder, arr)
            dab__trit = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, ntjpn__xjgcv, dab__trit)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (qowoh__crss, atsp__snabz):
                with qowoh__crss:
                    rrp__ekakc = c.pyapi.make_none()
                    c.pyapi.list_setitem(getf__jem, kqkq__vqg, rrp__ekakc)
                with atsp__snabz:
                    lbgzi__xppjf = cgutils.alloca_once(c.builder, c.context
                        .get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, dikh__mnpe)
                        ) as (bpw__xfjam, zhi__gmo):
                        with bpw__xfjam:
                            lyre__ygz = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, table.parent, kqkq__vqg, t)
                            c.builder.store(lyre__ygz, lbgzi__xppjf)
                        with zhi__gmo:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), lbgzi__xppjf)
                    c.pyapi.list_setitem(getf__jem, kqkq__vqg, c.builder.
                        load(lbgzi__xppjf))
    zvqhk__bpbab = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    wyxjq__kdrde = c.pyapi.call_function_objargs(zvqhk__bpbab, (getf__jem,))
    c.pyapi.decref(zvqhk__bpbab)
    c.pyapi.decref(getf__jem)
    c.context.nrt.decref(c.builder, typ, val)
    return wyxjq__kdrde


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        kxtor__bwd = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            fru__rmyb = getattr(table, f'block_{i}')
            ubea__lfk = ListInstance(context, builder, types.List(t), fru__rmyb
                )
            kxtor__bwd = builder.add(kxtor__bwd, ubea__lfk.size)
        return kxtor__bwd
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    ekzc__obxtf = table_type.block_nums[col_ind]
    iflr__qrkgq = table_type.block_offsets[col_ind]
    fru__rmyb = getattr(table, f'block_{ekzc__obxtf}')
    vaf__rax = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    cbuk__kggm = context.get_constant(types.int64, col_ind)
    xysp__mys = context.get_constant(types.int64, iflr__qrkgq)
    oxad__uvot = table_arg, fru__rmyb, xysp__mys, cbuk__kggm
    ensure_column_unboxed_codegen(context, builder, vaf__rax, oxad__uvot)
    ubea__lfk = ListInstance(context, builder, types.List(arr_type), fru__rmyb)
    arr = ubea__lfk.getitem(iflr__qrkgq)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, rhasm__uyqgz = args
        arr = get_table_data_codegen(context, builder, table_arg, col_ind,
            table_type)
        return impl_ret_borrowed(context, builder, arr_type, arr)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType
        ), 'Can only delete columns from a table'
    assert isinstance(ind_typ, types.TypeRef) and isinstance(ind_typ.
        instance_type, MetaType), 'ind_typ must be a typeref for a meta type'
    npskk__hrh = list(ind_typ.instance_type.meta)
    fcrcn__hutil = defaultdict(list)
    for ind in npskk__hrh:
        fcrcn__hutil[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, rhasm__uyqgz = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for ekzc__obxtf, nynjn__nnya in fcrcn__hutil.items():
            arr_type = table_type.blk_to_type[ekzc__obxtf]
            fru__rmyb = getattr(table, f'block_{ekzc__obxtf}')
            ubea__lfk = ListInstance(context, builder, types.List(arr_type),
                fru__rmyb)
            opjw__ieu = context.get_constant_null(arr_type)
            if len(nynjn__nnya) == 1:
                iflr__qrkgq = nynjn__nnya[0]
                arr = ubea__lfk.getitem(iflr__qrkgq)
                context.nrt.decref(builder, arr_type, arr)
                ubea__lfk.inititem(iflr__qrkgq, opjw__ieu, incref=False)
            else:
                zod__xzi = context.get_constant(types.int64, len(nynjn__nnya))
                kxer__fkcz = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(nynjn__nnya, dtype
                    =np.int64))
                ytx__gie = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, kxer__fkcz)
                with cgutils.for_range(builder, zod__xzi) as hvfnt__yps:
                    i = hvfnt__yps.index
                    iflr__qrkgq = _getitem_array_single_int(context,
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), ytx__gie, i)
                    arr = ubea__lfk.getitem(iflr__qrkgq)
                    context.nrt.decref(builder, arr_type, arr)
                    ubea__lfk.inititem(iflr__qrkgq, opjw__ieu, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    vjorn__pvcjl = context.get_constant(types.int64, 0)
    lkq__rem = context.get_constant(types.int64, 1)
    fusv__xhlzs = arr_type not in in_table_type.type_to_blk
    for t, ekzc__obxtf in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            pbb__uki = in_table_type.type_to_blk[t]
            dxwl__owm = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{pbb__uki}'))
            context.nrt.incref(builder, types.List(t), dxwl__owm.value)
            setattr(out_table, f'block_{ekzc__obxtf}', dxwl__owm.value)
    if fusv__xhlzs:
        rhasm__uyqgz, dxwl__owm = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), lkq__rem)
        dxwl__owm.size = lkq__rem
        dxwl__owm.inititem(vjorn__pvcjl, arr_arg, incref=True)
        ekzc__obxtf = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{ekzc__obxtf}', dxwl__owm.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        ekzc__obxtf = out_table_type.type_to_blk[arr_type]
        dxwl__owm = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{ekzc__obxtf}'))
        if is_new_col:
            n = dxwl__owm.size
            hwtxt__vdfy = builder.add(n, lkq__rem)
            dxwl__owm.resize(hwtxt__vdfy)
            dxwl__owm.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            rtkhb__llfrp = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            dxwl__owm.setitem(rtkhb__llfrp, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            rtkhb__llfrp = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            n = dxwl__owm.size
            hwtxt__vdfy = builder.add(n, lkq__rem)
            dxwl__owm.resize(hwtxt__vdfy)
            context.nrt.incref(builder, arr_type, dxwl__owm.getitem(
                rtkhb__llfrp))
            dxwl__owm.move(builder.add(rtkhb__llfrp, lkq__rem),
                rtkhb__llfrp, builder.sub(n, rtkhb__llfrp))
            dxwl__owm.setitem(rtkhb__llfrp, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    jmins__aoe = in_table_type.arr_types[col_ind]
    if jmins__aoe in out_table_type.type_to_blk:
        ekzc__obxtf = out_table_type.type_to_blk[jmins__aoe]
        cuoi__duuia = getattr(out_table, f'block_{ekzc__obxtf}')
        dcmjc__llyx = types.List(jmins__aoe)
        rtkhb__llfrp = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        losfz__kwx = dcmjc__llyx.dtype(dcmjc__llyx, types.intp)
        szs__yos = context.compile_internal(builder, lambda lst, i: lst.pop
            (i), losfz__kwx, (cuoi__duuia, rtkhb__llfrp))
        context.nrt.decref(builder, jmins__aoe, szs__yos)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    xzw__dqj = list(table.arr_types)
    if ind == len(xzw__dqj):
        wjsg__kktq = None
        xzw__dqj.append(arr_type)
    else:
        wjsg__kktq = table.arr_types[ind]
        xzw__dqj[ind] = arr_type
    oyl__aqxm = TableType(tuple(xzw__dqj))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': oyl__aqxm}
    oqh__uvisg = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    oqh__uvisg += f'  T2 = init_table(out_table_typ, False)\n'
    oqh__uvisg += f'  T2 = set_table_len(T2, len(table))\n'
    oqh__uvisg += f'  T2 = set_table_parent(T2, table)\n'
    for typ, ekzc__obxtf in oyl__aqxm.type_to_blk.items():
        if typ in table.type_to_blk:
            knz__qrj = table.type_to_blk[typ]
            oqh__uvisg += (
                f'  arr_list_{ekzc__obxtf} = get_table_block(table, {knz__qrj})\n'
                )
            oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_{ekzc__obxtf}, {len(oyl__aqxm.block_to_arr_ind[ekzc__obxtf])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[knz__qrj]
                ) & used_cols:
                oqh__uvisg += (
                    f'  for i in range(len(arr_list_{ekzc__obxtf})):\n')
                if typ not in (wjsg__kktq, arr_type):
                    oqh__uvisg += (
                        f'    out_arr_list_{ekzc__obxtf}[i] = arr_list_{ekzc__obxtf}[i]\n'
                        )
                else:
                    dhj__qphpy = table.block_to_arr_ind[knz__qrj]
                    msrp__yox = np.empty(len(dhj__qphpy), np.int64)
                    yua__uwodq = False
                    for nutvp__wls, kqkq__vqg in enumerate(dhj__qphpy):
                        if kqkq__vqg != ind:
                            suwkl__lzzxs = oyl__aqxm.block_offsets[kqkq__vqg]
                        else:
                            suwkl__lzzxs = -1
                            yua__uwodq = True
                        msrp__yox[nutvp__wls] = suwkl__lzzxs
                    glbls[f'out_idxs_{ekzc__obxtf}'] = np.array(msrp__yox,
                        np.int64)
                    oqh__uvisg += f'    out_idx = out_idxs_{ekzc__obxtf}[i]\n'
                    if yua__uwodq:
                        oqh__uvisg += f'    if out_idx == -1:\n'
                        oqh__uvisg += f'      continue\n'
                    oqh__uvisg += f"""    out_arr_list_{ekzc__obxtf}[out_idx] = arr_list_{ekzc__obxtf}[i]
"""
            if typ == arr_type and not is_null:
                oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf}[{oyl__aqxm.block_offsets[ind]}] = arr
"""
        else:
            glbls[f'arr_list_typ_{ekzc__obxtf}'] = types.List(arr_type)
            oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_typ_{ekzc__obxtf}, 1, False)
"""
            if not is_null:
                oqh__uvisg += f'  out_arr_list_{ekzc__obxtf}[0] = arr\n'
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{ekzc__obxtf}, {ekzc__obxtf})\n'
            )
    oqh__uvisg += f'  return T2\n'
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        eub__vfr = None
    else:
        eub__vfr = set(used_cols.instance_type.meta)
    rxbjm__quq = get_overload_const_int(ind)
    return generate_set_table_data_code(table, rxbjm__quq, arr, eub__vfr)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    rxbjm__quq = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        eub__vfr = None
    else:
        eub__vfr = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, rxbjm__quq, arr_type,
        eub__vfr, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    bcxyy__gxiln = args[0]
    if equiv_set.has_shape(bcxyy__gxiln):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            bcxyy__gxiln)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    jqnw__rxrk = []
    for t, ekzc__obxtf in table_type.type_to_blk.items():
        toq__ncxoj = len(table_type.block_to_arr_ind[ekzc__obxtf])
        jeo__utpt = []
        for i in range(toq__ncxoj):
            kqkq__vqg = table_type.block_to_arr_ind[ekzc__obxtf][i]
            jeo__utpt.append(pyval.arrays[kqkq__vqg])
        jqnw__rxrk.append(context.get_constant_generic(builder, types.List(
            t), jeo__utpt))
    gqmq__injna = context.get_constant_null(types.pyobject)
    lsug__hmc = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(jqnw__rxrk + [gqmq__injna, lsug__hmc])


def get_init_table_output_type(table_type, to_str_if_dict_t):
    out_table_type = table_type.instance_type if isinstance(table_type,
        types.TypeRef) else table_type
    assert isinstance(out_table_type, TableType
        ), 'table type or typeref expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(out_table_type)
    return out_table_type


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    out_table_type = get_init_table_output_type(table_type, to_str_if_dict_t)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(out_table_type)(context, builder)
        for t, ekzc__obxtf in out_table_type.type_to_blk.items():
            rmo__nneug = context.get_constant_null(types.List(t))
            setattr(table, f'block_{ekzc__obxtf}', rmo__nneug)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    qvgzd__cjodg = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        qvgzd__cjodg[typ.dtype] = i
    ujya__pnaor = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(ujya__pnaor, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        vexb__pbqm, rhasm__uyqgz = args
        table = cgutils.create_struct_proxy(ujya__pnaor)(context, builder)
        for t, ekzc__obxtf in ujya__pnaor.type_to_blk.items():
            idx = qvgzd__cjodg[t]
            nhf__aylqq = signature(types.List(t), tuple_of_lists_type,
                types.literal(idx))
            ibny__oud = vexb__pbqm, idx
            toy__vszg = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, nhf__aylqq, ibny__oud)
            setattr(table, f'block_{ekzc__obxtf}', toy__vszg)
        return table._getvalue()
    sig = ujya__pnaor(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    ekzc__obxtf = get_overload_const_int(blk_type)
    arr_type = None
    for t, kjyre__lwi in table_type.type_to_blk.items():
        if kjyre__lwi == ekzc__obxtf:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    xrl__pkzr = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        fru__rmyb = getattr(table, f'block_{ekzc__obxtf}')
        return impl_ret_borrowed(context, builder, xrl__pkzr, fru__rmyb)
    sig = xrl__pkzr(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, hgtr__wpk = args
        ahuy__bpb = context.get_python_api(builder)
        tct__nizp = used_cols_typ == types.none
        if not tct__nizp:
            geg__lfdc = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), hgtr__wpk)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, ekzc__obxtf in table_type.type_to_blk.items():
            zod__xzi = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[ekzc__obxtf]))
            qwkde__vmtf = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                ekzc__obxtf], dtype=np.int64))
            efum__mlga = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, qwkde__vmtf)
            fru__rmyb = getattr(table, f'block_{ekzc__obxtf}')
            with cgutils.for_range(builder, zod__xzi) as hvfnt__yps:
                i = hvfnt__yps.index
                kqkq__vqg = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    efum__mlga, i)
                vaf__rax = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                oxad__uvot = table_arg, fru__rmyb, i, kqkq__vqg
                if tct__nizp:
                    ensure_column_unboxed_codegen(context, builder,
                        vaf__rax, oxad__uvot)
                else:
                    kben__qelr = geg__lfdc.contains(kqkq__vqg)
                    with builder.if_then(kben__qelr):
                        ensure_column_unboxed_codegen(context, builder,
                            vaf__rax, oxad__uvot)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, bmf__effz, jmw__aym, qlcuh__ukmqr = args
    ahuy__bpb = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    dikh__mnpe = cgutils.is_not_null(builder, table.parent)
    ubea__lfk = ListInstance(context, builder, sig.args[1], bmf__effz)
    mib__fvgw = ubea__lfk.getitem(jmw__aym)
    ntjpn__xjgcv = cgutils.alloca_once_value(builder, mib__fvgw)
    dab__trit = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, ntjpn__xjgcv, dab__trit)
    with builder.if_then(is_null):
        with builder.if_else(dikh__mnpe) as (qowoh__crss, atsp__snabz):
            with qowoh__crss:
                lbgzi__xppjf = get_df_obj_column_codegen(context, builder,
                    ahuy__bpb, table.parent, qlcuh__ukmqr, sig.args[1].dtype)
                arr = ahuy__bpb.to_native_value(sig.args[1].dtype, lbgzi__xppjf
                    ).value
                ubea__lfk.inititem(jmw__aym, arr, incref=False)
                ahuy__bpb.decref(lbgzi__xppjf)
            with atsp__snabz:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    ekzc__obxtf = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, pil__kohkw, rhasm__uyqgz = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{ekzc__obxtf}', pil__kohkw)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, dnxv__tazuj = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = dnxv__tazuj
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        gwbd__tlv, rury__tvlw = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, rury__tvlw)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, gwbd__tlv)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    xrl__pkzr = list_type.instance_type if isinstance(list_type, types.TypeRef
        ) else list_type
    assert isinstance(xrl__pkzr, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        xrl__pkzr = types.List(to_str_arr_if_dict_array(xrl__pkzr.dtype))

    def codegen(context, builder, sig, args):
        wyr__wjdh = args[1]
        rhasm__uyqgz, dxwl__owm = ListInstance.allocate_ex(context, builder,
            xrl__pkzr, wyr__wjdh)
        dxwl__owm.size = wyr__wjdh
        return dxwl__owm.value
    sig = xrl__pkzr(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    sbcav__iolu = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(sbcav__iolu)

    def codegen(context, builder, sig, args):
        wyr__wjdh, rhasm__uyqgz = args
        rhasm__uyqgz, dxwl__owm = ListInstance.allocate_ex(context, builder,
            list_type, wyr__wjdh)
        dxwl__owm.size = wyr__wjdh
        return dxwl__owm.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        sxywi__bgew = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(sxywi__bgew)
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_filter(T, idx, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, '_get_idx_length': _get_idx_length,
        'ensure_contig_if_np': ensure_contig_if_np}
    if not is_overload_none(used_cols):
        nonv__rmh = used_cols.instance_type
        itc__yjeb = np.array(nonv__rmh.meta, dtype=np.int64)
        glbls['used_cols_vals'] = itc__yjeb
        ecflm__pyu = set([T.block_nums[i] for i in itc__yjeb])
    else:
        itc__yjeb = None
    oqh__uvisg = 'def table_filter_func(T, idx, used_cols=None):\n'
    oqh__uvisg += f'  T2 = init_table(T, False)\n'
    oqh__uvisg += f'  l = 0\n'
    if itc__yjeb is not None and len(itc__yjeb) == 0:
        oqh__uvisg += f'  l = _get_idx_length(idx, len(T))\n'
        oqh__uvisg += f'  T2 = set_table_len(T2, l)\n'
        oqh__uvisg += f'  return T2\n'
        yxy__jker = {}
        exec(oqh__uvisg, glbls, yxy__jker)
        return yxy__jker['table_filter_func']
    if itc__yjeb is not None:
        oqh__uvisg += f'  used_set = set(used_cols_vals)\n'
    for ekzc__obxtf in T.type_to_blk.values():
        oqh__uvisg += (
            f'  arr_list_{ekzc__obxtf} = get_table_block(T, {ekzc__obxtf})\n')
        oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_{ekzc__obxtf}, len(arr_list_{ekzc__obxtf}), False)
"""
        if itc__yjeb is None or ekzc__obxtf in ecflm__pyu:
            glbls[f'arr_inds_{ekzc__obxtf}'] = np.array(T.block_to_arr_ind[
                ekzc__obxtf], dtype=np.int64)
            oqh__uvisg += f'  for i in range(len(arr_list_{ekzc__obxtf})):\n'
            oqh__uvisg += (
                f'    arr_ind_{ekzc__obxtf} = arr_inds_{ekzc__obxtf}[i]\n')
            if itc__yjeb is not None:
                oqh__uvisg += (
                    f'    if arr_ind_{ekzc__obxtf} not in used_set: continue\n'
                    )
            oqh__uvisg += f"""    ensure_column_unboxed(T, arr_list_{ekzc__obxtf}, i, arr_ind_{ekzc__obxtf})
"""
            oqh__uvisg += f"""    out_arr_{ekzc__obxtf} = ensure_contig_if_np(arr_list_{ekzc__obxtf}[i][idx])
"""
            oqh__uvisg += f'    l = len(out_arr_{ekzc__obxtf})\n'
            oqh__uvisg += (
                f'    out_arr_list_{ekzc__obxtf}[i] = out_arr_{ekzc__obxtf}\n')
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{ekzc__obxtf}, {ekzc__obxtf})\n'
            )
    oqh__uvisg += f'  T2 = set_table_len(T2, l)\n'
    oqh__uvisg += f'  return T2\n'
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    kfhd__jnwwg = list(idx.instance_type.meta)
    xzw__dqj = tuple(np.array(T.arr_types, dtype=object)[kfhd__jnwwg])
    oyl__aqxm = TableType(xzw__dqj)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    eckhf__usiid = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': oyl__aqxm}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        tsqut__gtyu = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        uzpup__rsn = True
    else:
        uzpup__rsn = False
    qstem__uemgl = {i: c for i, c in enumerate(kfhd__jnwwg)}
    oqh__uvisg = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    oqh__uvisg += f'  T2 = init_table(out_table_typ, False)\n'
    oqh__uvisg += f'  T2 = set_table_len(T2, len(T))\n'
    if uzpup__rsn and len(tsqut__gtyu) == 0:
        oqh__uvisg += f'  return T2\n'
        yxy__jker = {}
        exec(oqh__uvisg, glbls, yxy__jker)
        return yxy__jker['table_subset']
    if uzpup__rsn:
        oqh__uvisg += f'  kept_cols_set = set(kept_cols)\n'
    for typ, ekzc__obxtf in oyl__aqxm.type_to_blk.items():
        knz__qrj = T.type_to_blk[typ]
        oqh__uvisg += (
            f'  arr_list_{ekzc__obxtf} = get_table_block(T, {knz__qrj})\n')
        oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_{ekzc__obxtf}, {len(oyl__aqxm.block_to_arr_ind[ekzc__obxtf])}, False)
"""
        zoa__avy = True
        if uzpup__rsn:
            ezftr__demp = set(oyl__aqxm.block_to_arr_ind[ekzc__obxtf])
            iauph__vzlxm = ezftr__demp & tsqut__gtyu
            zoa__avy = len(iauph__vzlxm) > 0
        if zoa__avy:
            glbls[f'out_arr_inds_{ekzc__obxtf}'] = np.array(oyl__aqxm.
                block_to_arr_ind[ekzc__obxtf], dtype=np.int64)
            oqh__uvisg += (
                f'  for i in range(len(out_arr_list_{ekzc__obxtf})):\n')
            oqh__uvisg += (
                f'    out_arr_ind_{ekzc__obxtf} = out_arr_inds_{ekzc__obxtf}[i]\n'
                )
            if uzpup__rsn:
                oqh__uvisg += (
                    f'    if out_arr_ind_{ekzc__obxtf} not in kept_cols_set: continue\n'
                    )
            mbazq__jnhd = []
            rgsh__aahm = []
            for adwu__ebw in oyl__aqxm.block_to_arr_ind[ekzc__obxtf]:
                tjr__tlrpc = qstem__uemgl[adwu__ebw]
                mbazq__jnhd.append(tjr__tlrpc)
                vwer__eqcu = T.block_offsets[tjr__tlrpc]
                rgsh__aahm.append(vwer__eqcu)
            glbls[f'in_logical_idx_{ekzc__obxtf}'] = np.array(mbazq__jnhd,
                dtype=np.int64)
            glbls[f'in_physical_idx_{ekzc__obxtf}'] = np.array(rgsh__aahm,
                dtype=np.int64)
            oqh__uvisg += (
                f'    logical_idx_{ekzc__obxtf} = in_logical_idx_{ekzc__obxtf}[i]\n'
                )
            oqh__uvisg += (
                f'    physical_idx_{ekzc__obxtf} = in_physical_idx_{ekzc__obxtf}[i]\n'
                )
            oqh__uvisg += f"""    ensure_column_unboxed(T, arr_list_{ekzc__obxtf}, physical_idx_{ekzc__obxtf}, logical_idx_{ekzc__obxtf})
"""
            czyk__zgg = '.copy()' if eckhf__usiid else ''
            oqh__uvisg += f"""    out_arr_list_{ekzc__obxtf}[i] = arr_list_{ekzc__obxtf}[physical_idx_{ekzc__obxtf}]{czyk__zgg}
"""
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{ekzc__obxtf}, {ekzc__obxtf})\n'
            )
    oqh__uvisg += f'  return T2\n'
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    bcxyy__gxiln = args[0]
    if equiv_set.has_shape(bcxyy__gxiln):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=bcxyy__gxiln, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (bcxyy__gxiln)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    bcxyy__gxiln = args[0]
    if equiv_set.has_shape(bcxyy__gxiln):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            bcxyy__gxiln)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    ezobp__jbn = in_table_type.type_to_blk[bodo.string_array_type]
    ieti__yty = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    kvpg__vpsos = in_table_type.block_to_arr_ind.get(ezobp__jbn)
    nkjbl__cducl = in_table_type.block_to_arr_ind.get(ieti__yty)
    ltlwm__utqn = []
    xvx__ntu = []
    eoni__ocf = 0
    opsy__jzuef = 0
    for czr__axls in range(len(kvpg__vpsos) + len(nkjbl__cducl)):
        if eoni__ocf == len(kvpg__vpsos):
            xvx__ntu.append(czr__axls)
            continue
        elif opsy__jzuef == len(nkjbl__cducl):
            ltlwm__utqn.append(czr__axls)
            continue
        wshq__snkz = kvpg__vpsos[eoni__ocf]
        txijf__beia = nkjbl__cducl[opsy__jzuef]
        if wshq__snkz < txijf__beia:
            ltlwm__utqn.append(czr__axls)
            eoni__ocf += 1
        else:
            xvx__ntu.append(czr__axls)
            opsy__jzuef += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        ltlwm__utqn)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(xvx__ntu)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    ueqp__euesz = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{ezobp__jbn}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{ezobp__jbn} already present in global variables'
    glbls[f'arr_inds_{ezobp__jbn}'] = np.array(in_table_type.
        block_to_arr_ind[ezobp__jbn], dtype=np.int64)
    assert f'arr_inds_{ieti__yty}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{ieti__yty} already present in global variables'
    glbls[f'arr_inds_{ieti__yty}'] = np.array(in_table_type.
        block_to_arr_ind[ieti__yty], dtype=np.int64)
    oqh__uvisg = f'  input_str_arr_list = get_table_block(T, {ezobp__jbn})\n'
    oqh__uvisg += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {ieti__yty})\n')
    oqh__uvisg += f"""  out_arr_list_{ueqp__euesz} = alloc_list_like(input_str_arr_list, {len(ltlwm__utqn) + len(xvx__ntu)}, True)
"""
    oqh__uvisg += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    oqh__uvisg += (
        f'    arr_ind_str = arr_inds_{ezobp__jbn}[input_str_ary_idx]\n')
    oqh__uvisg += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    oqh__uvisg += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        oqh__uvisg += (
            f'    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)\n'
            )
    oqh__uvisg += (
        f'    out_arr_list_{ueqp__euesz}[output_str_arr_offset] = out_arr_str\n'
        )
    oqh__uvisg += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    oqh__uvisg += (
        f'    arr_ind_dict_enc_str = arr_inds_{ieti__yty}[input_dict_enc_str_ary_idx]\n'
        )
    oqh__uvisg += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    oqh__uvisg += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        oqh__uvisg += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    oqh__uvisg += f"""    out_arr_list_{ueqp__euesz}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    oqh__uvisg += (
        f'  T2 = set_table_block(T2, out_arr_list_{ueqp__euesz}, {ueqp__euesz})\n'
        )
    return oqh__uvisg


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    oqh__uvisg = 'def impl(T):\n'
    oqh__uvisg += f'  T2 = init_table(T, True)\n'
    oqh__uvisg += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    vnan__jhbt = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if vnan__jhbt:
        oqh__uvisg += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, qqgy__nzfwt in T.type_to_blk.items():
        if vnan__jhbt and typ in (bodo.string_array_type, bodo.
            dict_str_arr_type):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            aphwp__jxnm = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            aphwp__jxnm = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{qqgy__nzfwt}'] = np.array(T.block_to_arr_ind[
            qqgy__nzfwt], dtype=np.int64)
        oqh__uvisg += (
            f'  arr_list_{qqgy__nzfwt} = get_table_block(T, {qqgy__nzfwt})\n')
        oqh__uvisg += f"""  out_arr_list_{qqgy__nzfwt} = alloc_list_like(arr_list_{qqgy__nzfwt}, len(arr_list_{qqgy__nzfwt}), True)
"""
        oqh__uvisg += f'  for i in range(len(arr_list_{qqgy__nzfwt})):\n'
        oqh__uvisg += (
            f'    arr_ind_{qqgy__nzfwt} = arr_inds_{qqgy__nzfwt}[i]\n')
        oqh__uvisg += f"""    ensure_column_unboxed(T, arr_list_{qqgy__nzfwt}, i, arr_ind_{qqgy__nzfwt})
"""
        oqh__uvisg += f"""    out_arr_{qqgy__nzfwt} = decode_if_dict_array(arr_list_{qqgy__nzfwt}[i])
"""
        oqh__uvisg += (
            f'    out_arr_list_{qqgy__nzfwt}[i] = out_arr_{qqgy__nzfwt}\n')
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{qqgy__nzfwt}, {aphwp__jxnm})\n'
            )
    oqh__uvisg += f'  T2 = set_table_len(T2, l)\n'
    oqh__uvisg += f'  return T2\n'
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['impl']


@overload(operator.getitem, no_unliteral=True, inline='always')
def overload_table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return lambda T, idx: table_filter(T, idx)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        ehk__tlq = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        ehk__tlq = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            ehk__tlq.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ppe__vprae, gkymt__nairz = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = gkymt__nairz
        jqnw__rxrk = cgutils.unpack_tuple(builder, ppe__vprae)
        for i, fru__rmyb in enumerate(jqnw__rxrk):
            setattr(table, f'block_{i}', fru__rmyb)
            context.nrt.incref(builder, types.List(ehk__tlq[i]), fru__rmyb)
        return table._getvalue()
    table_type = TableType(tuple(ehk__tlq), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen


def _to_arr_if_series(t):
    return t.data if isinstance(t, SeriesType) else t


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def logical_table_to_table(in_table_t, extra_arrs_t, in_col_inds_t,
    n_table_cols_t, out_table_type_t=None, used_cols=None):
    in_col_inds = in_col_inds_t.instance_type.meta
    assert isinstance(in_table_t, (TableType, types.BaseTuple, types.NoneType)
        ), 'logical_table_to_table: input table must be a TableType or tuple of arrays or None (for dead table)'
    glbls = {}
    if not is_overload_none(used_cols):
        kept_cols = set(used_cols.instance_type.meta)
        glbls['kept_cols'] = np.array(list(kept_cols), np.int64)
        uzpup__rsn = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        uzpup__rsn = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    uhl__jpufp = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        uhl__jpufp else _to_arr_if_series(extra_arrs_t.types[i - uhl__jpufp
        ]) for i in in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    oqh__uvisg = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        oqh__uvisg += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    oqh__uvisg += f'  T1 = in_table_t\n'
    oqh__uvisg += f'  T2 = init_table(out_table_type, False)\n'
    oqh__uvisg += f'  T2 = set_table_len(T2, len(T1))\n'
    if uzpup__rsn and len(kept_cols) == 0:
        oqh__uvisg += f'  return T2\n'
        yxy__jker = {}
        exec(oqh__uvisg, glbls, yxy__jker)
        return yxy__jker['impl']
    if uzpup__rsn:
        oqh__uvisg += f'  kept_cols_set = set(kept_cols)\n'
    for typ, ekzc__obxtf in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{ekzc__obxtf}'] = types.List(typ)
        zod__xzi = len(out_table_type.block_to_arr_ind[ekzc__obxtf])
        oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_typ_{ekzc__obxtf}, {zod__xzi}, False)
"""
        if typ in in_table_t.type_to_blk:
            vhr__vjoe = in_table_t.type_to_blk[typ]
            jtnuj__pdfhp = []
            osnu__anu = []
            for yqqt__ltr in out_table_type.block_to_arr_ind[ekzc__obxtf]:
                lxel__btz = in_col_inds[yqqt__ltr]
                if lxel__btz < uhl__jpufp:
                    jtnuj__pdfhp.append(in_table_t.block_offsets[lxel__btz])
                    osnu__anu.append(lxel__btz)
                else:
                    jtnuj__pdfhp.append(-1)
                    osnu__anu.append(-1)
            glbls[f'in_idxs_{ekzc__obxtf}'] = np.array(jtnuj__pdfhp, np.int64)
            glbls[f'in_arr_inds_{ekzc__obxtf}'] = np.array(osnu__anu, np.int64)
            if uzpup__rsn:
                glbls[f'out_arr_inds_{ekzc__obxtf}'] = np.array(out_table_type
                    .block_to_arr_ind[ekzc__obxtf], dtype=np.int64)
            oqh__uvisg += (
                f'  in_arr_list_{ekzc__obxtf} = get_table_block(T1, {vhr__vjoe})\n'
                )
            oqh__uvisg += (
                f'  for i in range(len(out_arr_list_{ekzc__obxtf})):\n')
            oqh__uvisg += (
                f'    in_offset_{ekzc__obxtf} = in_idxs_{ekzc__obxtf}[i]\n')
            oqh__uvisg += f'    if in_offset_{ekzc__obxtf} == -1:\n'
            oqh__uvisg += f'      continue\n'
            oqh__uvisg += (
                f'    in_arr_ind_{ekzc__obxtf} = in_arr_inds_{ekzc__obxtf}[i]\n'
                )
            if uzpup__rsn:
                oqh__uvisg += f"""    if out_arr_inds_{ekzc__obxtf}[i] not in kept_cols_set: continue
"""
            oqh__uvisg += f"""    ensure_column_unboxed(T1, in_arr_list_{ekzc__obxtf}, in_offset_{ekzc__obxtf}, in_arr_ind_{ekzc__obxtf})
"""
            oqh__uvisg += f"""    out_arr_list_{ekzc__obxtf}[i] = in_arr_list_{ekzc__obxtf}[in_offset_{ekzc__obxtf}]
"""
        for i, yqqt__ltr in enumerate(out_table_type.block_to_arr_ind[
            ekzc__obxtf]):
            if yqqt__ltr not in kept_cols:
                continue
            lxel__btz = in_col_inds[yqqt__ltr]
            if lxel__btz >= uhl__jpufp:
                oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf}[{i}] = extra_arrs_t[{lxel__btz - uhl__jpufp}]
"""
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{ekzc__obxtf}, {ekzc__obxtf})\n'
            )
    oqh__uvisg += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    uhl__jpufp = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < uhl__jpufp else
        _to_arr_if_series(extra_arrs_t.types[i - uhl__jpufp]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    negq__top = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                negq__top = f'in_table_t[{i}]'
                break
    if negq__top is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                negq__top = f'extra_arrs_t[{i}]'
                break
    assert negq__top is not None, 'no array found in input data'
    oqh__uvisg = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        oqh__uvisg += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    oqh__uvisg += f'  T1 = in_table_t\n'
    oqh__uvisg += f'  T2 = init_table(out_table_type, False)\n'
    oqh__uvisg += f'  T2 = set_table_len(T2, len({negq__top}))\n'
    glbls = {}
    for typ, ekzc__obxtf in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{ekzc__obxtf}'] = types.List(typ)
        zod__xzi = len(out_table_type.block_to_arr_ind[ekzc__obxtf])
        oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf} = alloc_list_like(arr_list_typ_{ekzc__obxtf}, {zod__xzi}, False)
"""
        for i, yqqt__ltr in enumerate(out_table_type.block_to_arr_ind[
            ekzc__obxtf]):
            if yqqt__ltr not in kept_cols:
                continue
            lxel__btz = in_col_inds[yqqt__ltr]
            if lxel__btz < uhl__jpufp:
                oqh__uvisg += (
                    f'  out_arr_list_{ekzc__obxtf}[{i}] = T1[{lxel__btz}]\n')
            else:
                oqh__uvisg += f"""  out_arr_list_{ekzc__obxtf}[{i}] = extra_arrs_t[{lxel__btz - uhl__jpufp}]
"""
        oqh__uvisg += (
            f'  T2 = set_table_block(T2, out_arr_list_{ekzc__obxtf}, {ekzc__obxtf})\n'
            )
    oqh__uvisg += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    yxy__jker = {}
    exec(oqh__uvisg, glbls, yxy__jker)
    return yxy__jker['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    xjekh__ofvr = args[0]
    ubfq__jvaz = args[1]
    if equiv_set.has_shape(xjekh__ofvr):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            xjekh__ofvr)[0], None), pre=[])
    if equiv_set.has_shape(ubfq__jvaz):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            ubfq__jvaz)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
