"""Constants for the V-Zug integration."""

from homeassistant.backports.enum import StrEnum

DOMAIN = "v_zug"
UPDATE_INTERVAL = 30  # in seconds

DEVICE_MODEL = "Adora Wash V2000"
MANUFACTURER = "V-Zug"
SUGGESTED_AREA = "V-Zug"


class SensorType(StrEnum):
    """SensorType Class."""

    DEVICE_NAME = "device_name"
    PROGRAM = "program"
    ACTIVE = "active"
    STATUS_ACTION = "status_action"
    PROGRAM_END = "program_end"
    MESSAGES = "messages"


SENSOR_NAMES = {
    SensorType.DEVICE_NAME: "Name",
    SensorType.PROGRAM: "Program",
    SensorType.ACTIVE: "Active",
    SensorType.STATUS_ACTION: "Status Action",
    SensorType.PROGRAM_END: "Program End",
    SensorType.MESSAGES: "Messages",
}
