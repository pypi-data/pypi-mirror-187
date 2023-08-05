from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    gqqu__xxpdq = f'class {class_name}(types.Opaque):\n'
    gqqu__xxpdq += f'    def __init__(self):\n'
    gqqu__xxpdq += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    gqqu__xxpdq += f'    def __reduce__(self):\n'
    gqqu__xxpdq += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    jklu__art = {}
    exec(gqqu__xxpdq, {'types': types, 'models': models}, jklu__art)
    vqq__kexi = jklu__art[class_name]
    setattr(module, class_name, vqq__kexi)
    class_instance = vqq__kexi()
    setattr(types, types_name, class_instance)
    gqqu__xxpdq = f'class {model_name}(models.StructModel):\n'
    gqqu__xxpdq += f'    def __init__(self, dmm, fe_type):\n'
    gqqu__xxpdq += f'        members = [\n'
    gqqu__xxpdq += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    gqqu__xxpdq += f"            ('pyobj', types.voidptr),\n"
    gqqu__xxpdq += f'        ]\n'
    gqqu__xxpdq += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(gqqu__xxpdq, {'types': types, 'models': models, types_name:
        class_instance}, jklu__art)
    xxem__tkx = jklu__art[model_name]
    setattr(module, model_name, xxem__tkx)
    register_model(vqq__kexi)(xxem__tkx)
    make_attribute_wrapper(vqq__kexi, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(vqq__kexi)(unbox_py_obj)
    box(vqq__kexi)(box_py_obj)
    return vqq__kexi


def box_py_obj(typ, val, c):
    ztvsu__ebri = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = ztvsu__ebri.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    ztvsu__ebri = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ztvsu__ebri.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    ztvsu__ebri.pyobj = obj
    return NativeValue(ztvsu__ebri._getvalue())
