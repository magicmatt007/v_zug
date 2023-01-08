"""Platform for sensor integration."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyUpdateCoordinator
from .api import Api
from .base_sensors import BaseSensor
from .const import DOMAIN, EntityType

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry."""

    coordinator: MyUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    if not coordinator.data:
        return None
    data: Api = coordinator.data

    device_model = data.device_model
    device_uuid = data.device_uuid

    new_entities = [
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.ACTIVE,
            coordinator=coordinator,
        ),
    ]

    async_add_entities(new_entities)

    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        "turn_off",
        {},
        "turn_off",
    )


class MySensor(BaseSensor, BinarySensorEntity):
    """Representation of a Sensor."""

    # @property
    # def native_value(self):
    #     """Return the state of the sensor."""

    #     if not self.coordinator.data:
    #         return None
    #     data: Api = self.coordinator.data

    #     if self._sensor_type == EntityType.ACTIVE:
    #         return data.active
    #     return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
        data: Api = self.coordinator.data

        if self._sensor_type == EntityType.ACTIVE:
            return data.active
        return None
        # return self._attr_is_on

    async def turn_off(self):
        """Turn off appliance."""
        if not self.coordinator.data:
            return None
        data: Api = self.coordinator.data
        await data.turn_off()
