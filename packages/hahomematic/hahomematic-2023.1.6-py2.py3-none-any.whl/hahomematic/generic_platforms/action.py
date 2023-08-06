"""Module for entities implemented actions."""
from __future__ import annotations

from typing import Any

from hahomematic.const import HmPlatform
from hahomematic.entity import GenericEntity


class HmAction(GenericEntity[None]):
    """
    Implementation of an action.
    This is an internal default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.ACTION

    async def send_value(self, value: Any) -> bool:
        """Set the value of the entity."""
        # We allow setting the value via index as well, just in case.
        if value is not None and self._attr_value_list and isinstance(value, str):
            return await super().send_value(self._attr_value_list.index(value))
        return await super().send_value(value)
