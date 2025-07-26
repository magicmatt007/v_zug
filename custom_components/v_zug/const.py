"""Constants for the V-Zug integration."""

# from homeassistant.backports.enum import StrEnum   # 26.7.25: Depreciated. Replaced by next line
from enum import StrEnum


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
    MESSAGE_1 = "message_1"
    MESSAGE_2 = "message_2"
    MESSAGE_3 = "message_3"
    TURN_OFF_BUTTON = "button"
    PROGRAM_COMPLETED_COUNTER = "program_completed_counter"


ENTITY_NAMES = {
    EntityType.DEVICE_NAME: "Name",
    EntityType.PROGRAM: "Program",
    EntityType.ACTIVE: "Active",
    EntityType.STATUS_ACTION: "Action",
    EntityType.STATUS_END_TIME: "End Time",
    EntityType.PROGRAM_END: "Program End",
    EntityType.MESSAGES: "Messages",
    EntityType.MESSAGE_1: "Message 1",
    EntityType.MESSAGE_2: "Message 2",
    EntityType.MESSAGE_3: "Message 3",
    EntityType.TURN_OFF_BUTTON: "Turn Off",
    EntityType.PROGRAM_COMPLETED_COUNTER: "Counter",
}

ENTITY_ICONS = {
    EntityType.DEVICE_NAME: "mdi:account",
    EntityType.PROGRAM: "mdi:application-outline",
    EntityType.ACTIVE: "mdi:washing-machine",
    EntityType.STATUS_ACTION: "mdi:information-outline",
    EntityType.STATUS_END_TIME: "mdi:clock-outline",
    EntityType.PROGRAM_END: "mdi:timer-outline",
    EntityType.MESSAGES: "mdi:message-outline",
    EntityType.MESSAGE_1: "mdi:message-outline",
    EntityType.MESSAGE_2: "mdi:message-outline",
    EntityType.MESSAGE_3: "mdi:message-outline",
    EntityType.TURN_OFF_BUTTON: "mdi:pause",
    EntityType.PROGRAM_COMPLETED_COUNTER: "mdi:counter",
}
