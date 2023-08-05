"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            cha__htx = set()
            nuxx__jyn = list(self.context._get_attribute_templates(self.key))
            pcvnk__suhh = nuxx__jyn.index(self) + 1
            for txmz__efbj in range(pcvnk__suhh, len(nuxx__jyn)):
                if isinstance(nuxx__jyn[txmz__efbj], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    cha__htx.add(nuxx__jyn[txmz__efbj]._attr)
            self._attr_set = cha__htx
        return attr_name in self._attr_set
