"""Base Sensors."""

import logging

from homeassistant.const import Platform
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import MyUpdateCoordinator
from .const import DEVICE_MODEL, DOMAIN, MANUFACTURER, SENSOR_NAMES, SUGGESTED_AREA

_LOGGER = logging.getLogger(__name__)


class BaseEntity(CoordinatorEntity, Entity):
    """Representation of a Base Entity related to Devices."""

    def __init__(self, device_model, device_uuid, coordinator: MyUpdateCoordinator):
        """Initialize the sensor. Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        # Shared attributes of device entities:
        self.device_model = device_model
        self._device_uuid = device_uuid  # used as device identifier.

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Use course_no as unique identifier to group sensors as a Course Device:
                (DOMAIN, self._device_uuid)
            },
            name=f"{self.device_model}",
            manufacturer=MANUFACTURER,
            suggested_area=SUGGESTED_AREA,
        )


class BaseSensor(BaseEntity):
    """Representation of a Base Sensor related to the Device."""

    def __init__(
        self, device_model, device_uuid, sensor_type, coordinator: MyUpdateCoordinator
    ):
        """Initialize the sensor. Pass coordinator to CoordinatorEntity."""
        super().__init__(
            device_model=device_model, device_uuid=device_uuid, coordinator=coordinator
        )

        # Shared attributes of course sensor types:
        self._sensor_type = sensor_type
        self._attr_has_entity_name = True
        self._state = None
        self._attr_unique_id = f"{Platform.SENSOR}.{DOMAIN}_{DEVICE_MODEL.lower()}_{device_uuid}_{sensor_type}"
        self._attr_name = f"{SENSOR_NAMES[sensor_type]}"
