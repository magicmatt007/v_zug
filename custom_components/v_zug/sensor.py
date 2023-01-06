"""Platform for sensor integration."""
import logging

from homeassistant.components.sensor import SensorEntity
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
            sensor_type=EntityType.DEVICE_NAME,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.PROGRAM,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.ACTIVE,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.STATUS_ACTION,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.STATUS_END_TIME,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.PROGRAM_END,
            coordinator=coordinator,
        ),
        MySensor(
            device_model=device_model,
            device_uuid=device_uuid,
            sensor_type=EntityType.MESSAGES,
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


class MySensor(BaseSensor, SensorEntity):
    """Representation of a Sensor."""

    @property
    def native_value(self):
        """Return the state of the sensor."""

        if not self.coordinator.data:
            return None
        data: Api = self.coordinator.data

        if self._sensor_type == EntityType.DEVICE_NAME:
            return data.device_name
        if self._sensor_type == EntityType.PROGRAM:
            return data.program
        if self._sensor_type == EntityType.ACTIVE:
            return data.active
        if self._sensor_type == EntityType.STATUS_ACTION:
            return data.status_action
        if self._sensor_type == EntityType.STATUS_END_TIME:
            return data.status_end_time
        if self._sensor_type == EntityType.PROGRAM_END:
            return data.program_end
        if self._sensor_type == EntityType.MESSAGES:
            return data.messages_txt
        return None

    async def turn_off(self):
        """Turn off appliance."""
        if not self.coordinator.data:
            return None
        data: Api = self.coordinator.data
        await data.turn_off()
