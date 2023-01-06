"""Constants for the V-Zug integration."""

from homeassistant.backports.enum import StrEnum

DOMAIN = "v_zug"
UPDATE_INTERVAL = 30  # in seconds

DEVICE_MODEL = "Adora Wash V2000"
MANUFACTURER = "V-Zug"
SUGGESTED_AREA = "V-Zug"


class EntityType(StrEnum):
    """SensorType Class."""

    DEVICE_NAME = "device_name"
    PROGRAM = "program"
    ACTIVE = "active"
    STATUS_ACTION = "status_action"
    STATUS_END_TIME = "status_end_time"
    PROGRAM_END = "program_end"
    MESSAGES = "messages"
    TURN_OFF_BUTTON = "button"


ENTITY_NAMES = {
    EntityType.DEVICE_NAME: "Name",
    EntityType.PROGRAM: "Program",
    EntityType.ACTIVE: "Active",
    EntityType.STATUS_ACTION: "Action",
    EntityType.STATUS_END_TIME: "End Time",
    EntityType.PROGRAM_END: "Program End",
    EntityType.MESSAGES: "Messages",
    EntityType.TURN_OFF_BUTTON: "Turn Off",
}

ENTITY_ICONS = {
    EntityType.DEVICE_NAME: "mdi:account",
    EntityType.PROGRAM: "mdi:application-outline",
    EntityType.ACTIVE: "mdi:washing-machine",
    EntityType.STATUS_ACTION: "mdi:information-outline",
    EntityType.STATUS_END_TIME: "mdi:clock-outline",
    EntityType.PROGRAM_END: "mdi:timer-outline",
    EntityType.MESSAGES: "mdi:message-outline",
    EntityType.TURN_OFF_BUTTON: "mdi:pause",
}
