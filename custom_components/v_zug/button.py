"""Platform for sensor integration."""
import logging

_LOGGER = logging.getLogger(__name__)


from homeassistant.const import Platform


from homeassistant.components.button import (
    ButtonEntity,
)


from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyUpdateCoordinator
from .api import Api

from .const import (
    DOMAIN,
)

from .base_sensors import BaseEntity

# SCAN_INTERVAL = datetime.timedelta(seconds=10)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up entry."""
    _LOGGER.warning("Hello from sensor, async_setup_entry")

    # coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    coordinator: MyUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    if not coordinator.data:
        return None
    data: Api = coordinator.data

    device_model = data.device_model
    device_uuid = data.device_uuid

    new_entities = []
    new_entities.append(
        TurnOffButton(
            device_model=device_model, device_uuid=device_uuid, coordinator=coordinator
        )
    )
    async_add_entities(new_entities)


class TurnOffButton(BaseEntity, ButtonEntity):
    """Turn Off Button"""

    def __init__(self, device_model, device_uuid, coordinator: MyUpdateCoordinator):
        """Initialize the sensor. Pass coordinator to CoordinatorEntity."""
        super().__init__(
            device_model=device_model, device_uuid=device_uuid, coordinator=coordinator
        )

        # if not self.coordinator.data:
        #     return None
        # data: Api = self.coordinator.data

        self._state = None
        self._attr_unique_id = f"{Platform.BUTTON}.{DOMAIN}_{device_uuid}_turn_off"
        self._attr_has_entity_name = True
        self._attr_name = "Turn Off"

    async def async_press(self) -> None:
        """Handle the button press."""
        # if self.coordinator.data is not None:
        if not self.coordinator.data:
            return None
        data: Api = self.coordinator.data
        await data.turn_off()
        await self.coordinator.async_refresh()
        _LOGGER.warning("Appliance turned off")
