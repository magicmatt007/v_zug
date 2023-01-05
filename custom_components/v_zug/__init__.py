"""The example sensor integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, UPDATE_INTERVAL
from .api import Api

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BUTTON,
    # Platform.BINARY_SENSOR,
]

ATTR_NAME = "entity_id"
DEFAULT_NAME = "<enter course id>"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up is called when Home Assistant is loading our component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""
    ip_address = entry.data["ip_address"]
    coordinator = MyUpdateCoordinator(hass, entry, ip_address=ip_address)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok


class MyUpdateCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, entry: ConfigEntry, ip_address):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="V-Zug",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.entry = entry
        self.ip_address = ip_address
        session = aiohttp_client.async_get_clientsession(hass)
        self._api = Api(session=session, ip_address=ip_address)

    async def _async_update_data(self) -> Api | None:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.warning("Hello from _async_update_data")
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            # selected_centers= [54] # 54 = Schlieren, 96 = Olten
            # selected_course_names = ["BODYPUMP® 55'"]

            async with async_timeout.timeout(15):
                await self._api.get_device_status()
                await self._api.get_last_push_notifications()
                await self._api.get_command_spinning()
                await self._api.get_command_aquaplus()
                await self._api.get_command_soiling()
                await self._api.get_model_description()
                return self._api

        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Error %s in MyCoordinator _async_update_data", exception)

        return self._api
