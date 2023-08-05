"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    jfvco__kul = context.get_python_api(builder)
    return jfvco__kul.unserialize(jfvco__kul.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        ufb__uaw = ', '.join('e{}'.format(jyqe__xvz) for jyqe__xvz in range
            (len(args)))
        if ufb__uaw:
            ufb__uaw += ', '
        ahmsn__cow = ', '.join("{} = ''".format(fhe__oznvl) for fhe__oznvl in
            kws.keys())
        qbmaj__mayth = f'def format_stub(string, {ufb__uaw} {ahmsn__cow}):\n'
        qbmaj__mayth += '    pass\n'
        scr__uso = {}
        exec(qbmaj__mayth, {}, scr__uso)
        qkkm__kqis = scr__uso['format_stub']
        mqo__nbz = numba.core.utils.pysignature(qkkm__kqis)
        pyobn__pec = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, pyobn__pec).replace(pysig=mqo__nbz)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for vvcib__uiv in ('logging.Logger', 'logging.RootLogger'):
        for xbe__tgbgf in func_names:
            btakg__svwd = f'@bound_function("{vvcib__uiv}.{xbe__tgbgf}")\n'
            btakg__svwd += (
                f'def resolve_{xbe__tgbgf}(self, logger_typ, args, kws):\n')
            btakg__svwd += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(btakg__svwd)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for ttahw__nptl in logging_logger_unsupported_attrs:
        vqeaz__vuao = 'logging.Logger.' + ttahw__nptl
        overload_attribute(LoggingLoggerType, ttahw__nptl)(
            create_unsupported_overload(vqeaz__vuao))
    for ehdt__col in logging_logger_unsupported_methods:
        vqeaz__vuao = 'logging.Logger.' + ehdt__col
        overload_method(LoggingLoggerType, ehdt__col)(
            create_unsupported_overload(vqeaz__vuao))


_install_logging_logger_unsupported_objects()
