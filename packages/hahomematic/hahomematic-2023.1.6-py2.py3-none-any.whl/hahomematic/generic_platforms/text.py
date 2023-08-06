"""Module for entities implemented using text."""
from __future__ import annotations

from hahomematic.const import HmPlatform
from hahomematic.entity import GenericEntity, GenericSystemVariable


class HmText(GenericEntity[str]):
    """
    Implementation of a text.
    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.TEXT

    async def send_value(self, value: str | None) -> bool:
        """Set the value of the entity."""
        return await super().send_value(value)


class HmSysvarText(GenericSystemVariable):
    """
    Implementation of a sysvar text entity.
    """

    _attr_platform = HmPlatform.HUB_TEXT
    _attr_is_extended = True

    async def send_variable(self, value: str | None) -> bool:
        """Set the value of the entity."""
        return await super().send_variable(value)
