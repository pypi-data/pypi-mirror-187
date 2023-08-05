"""
Module for entities implemented using the
number platform (https://www.home-assistant.io/integrations/number/).
"""
from __future__ import annotations

import logging

from hahomematic.const import HM_VALUE, HmPlatform
from hahomematic.entity import GenericEntity, GenericSystemVariable, ParameterT

_LOGGER = logging.getLogger(__name__)


class BaseNumber(GenericEntity[ParameterT]):
    """
    Implementation of a number.
    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.NUMBER


class HmFloat(BaseNumber[float]):
    """
    Implementation of a Float.
    This is a default platform that gets automatically generated.
    """

    async def send_value(self, value: float, do_validate: bool = True) -> None:
        """Set the value of the entity."""
        if value is not None and (
            (self._attr_min <= float(value) <= self._attr_max) or do_validate is False
        ):
            await super().send_value(value)
        elif self._attr_special:
            if [sv for sv in self._attr_special.values() if value == sv[HM_VALUE]]:
                await super().send_value(value)
        else:
            _LOGGER.warning(
                "number.float failed: Invalid value: %s (min: %s, max: %s, special: %s)",
                value,
                self._attr_min,
                self._attr_max,
                self._attr_special,
            )


class HmInteger(BaseNumber[int]):
    """
    Implementation of an Integer.
    This is a default platform that gets automatically generated.
    """

    async def send_value(self, value: int, do_validate: bool = True) -> None:
        """Set the value of the entity."""
        if value is not None and (
            (self._attr_min <= int(value) <= self._attr_max) or do_validate is False
        ):
            await super().send_value(value)
        elif self._attr_special:
            if [sv for sv in self._attr_special.values() if value == sv[HM_VALUE]]:
                await super().send_value(value)
        else:
            _LOGGER.warning(
                "number.int failed: Invalid value: %s (min: %s, max: %s, special: %s)",
                value,
                self._attr_min,
                self._attr_max,
                self._attr_special,
            )


class HmSysvarNumber(GenericSystemVariable):
    """
    Implementation of a sysvar number.
    """

    _attr_platform = HmPlatform.HUB_NUMBER
    _attr_is_extended = True

    async def send_variable(self, value: float) -> None:
        """Set the value of the entity."""
        if value is not None and self.max is not None and self.min is not None:
            if self.min <= float(value) <= self.max:
                await super().send_variable(value)
            else:
                _LOGGER.warning(
                    "sysvar.number failed: Invalid value: %s (min: %s, max: %s)",
                    value,
                    self.min,
                    self.max,
                )
            return
        if value is not None:
            await super().send_variable(value)
