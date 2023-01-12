"""Api."""
from __future__ import annotations

import asyncio
import datetime
import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)


class Api:
    """Api."""

    def __init__(self, session: aiohttp.ClientSession, ip_address, attempts=5):
        """Init."""
        # Session data:
        self.session = session
        self.ip_address = ip_address
        self.attempts = attempts

        # Updated in api call get_device_status:
        self.device_name: str = ""
        self.program: str = ""
        self.inactive: bool = False
        self.active: bool = not self.inactive
        self.status: str = ""
        self.status_action: str = ""
        self.status_end_time: str = ""
        self.program_end: datetime.time | None = None
        self.device_uuid: str = ""

        # Updated in api call get_last_push_notifications
        self.messages: list = []
        self.messages_txt = ""
        self.message_1_txt = ""
        self.message_2_txt = ""
        self.message_3_txt = ""
        self.program_completed_counter = 0

        # Updated in api call get_command_spinning
        self.default_spinning: str = ""

        # Updated in api call get_command_soiling
        self.default_soiling: str = ""

        # Updated in api call get_command_aquaplus
        self.default_aquaplus: str = ""

        # Updated in api call get_device_model
        self.device_model: str = ""

    async def _get(self, url):
        """Help to manage dodgy Api."""

        for _ in range(self.attempts):
            resp = await self.session.get(url)
            content = await resp.json(content_type=None)

            if "error" in content:
                _LOGGER.debug(
                    "error: %s attempts: %s / %s",
                    content["error"],
                    _ + 1,
                    self.attempts,
                )
                await asyncio.sleep(0.2)
            else:
                return content

    async def get_device_status(self):
        """Get device status."""
        url = f"http://{self.ip_address}/ai?command=getDeviceStatus"
        content = await self._get(url)

        self.device_name = content["DeviceName"]
        self.program = content["Program"]
        self.inactive = not (content["Inactive"] == "false")
        self.active = not self.inactive
        self.status = content["Status"]
        status_lst = self.status.split("\n")
        self.status_action = status_lst[0] if len(status_lst) == 2 else ""
        self.status_end_time = status_lst[1] if len(status_lst) == 2 else ""
        self.program_end = (
            ""
            if content["ProgramEnd"]["End"] == ""
            else datetime.datetime.strptime(
                content["ProgramEnd"]["End"], "%Hh%M"
            ).time()
        )
        self.device_uuid = content["deviceUuid"]

        return content

    async def get_last_push_notifications(self):
        """Get last push notifications."""

        url = f"http://{self.ip_address}/ai?command=getLastPUSHNotifications"
        content = await self._get(url)

        messages_txt = ""
        message_dict: dict
        for index, message_dict in enumerate(content):
            date = message_dict["date"]
            message = message_dict["message"]
            date_obj = datetime.datetime.fromisoformat(
                date[:-1]
            )  # api provides time  in UTC
            time_str = date_obj.strftime("%a @ %H:%M")
            messages_txt += f"**{time_str}** {message}\n"

            message_x_txt = f"{time_str}: {message}"
            if index == 0:
                self.message_1_txt = message_x_txt
                # print(date_obj)
                if "finished" in message_x_txt:
                    now = datetime.datetime.now()
                    delta = now - date_obj
                    print(delta)
                    print(delta.total_seconds())
                    if (
                        delta.total_seconds() < 60 * 5
                    ):  # After the program has finished, show 1 for 5 minutes
                        self.program_completed_counter = 1
                    else:
                        self.program_completed_counter = 0
                else:
                    self.program_completed_counter = 0
            elif index == 1:
                self.message_2_txt = message_x_txt
            elif index == 2:
                self.message_3_txt = message_x_txt

        if messages_txt:
            messages_txt = messages_txt[:-1]

        self.messages = content
        self.messages_txt = messages_txt

        return content

    async def get_command_spinning(self):
        """Get spinning default setting."""
        url = f"http://{self.ip_address}/hh?command=getCommand&value=spinningXat"
        content = await self._get(url)
        content: dict
        value = content["value"]
        self.default_spinning = value
        return value

    async def get_command_soiling(self):
        """Get soiling default setting."""
        url = f"http://{self.ip_address}/hh?command=getCommand&value=soiling"
        content = await self._get(url)
        content: dict
        self.default_soiling = content["value"]
        value = content["value"]
        self.default_soiling = value
        return value

    async def get_command_aquaplus(self):
        """Get aquaplus default setting."""
        url = f"http://{self.ip_address}/hh?command=getCommand&value=aquaplus"
        content = await self._get(url)
        content: dict
        value = content["value"]
        self.default_aquaplus = value
        return value

    async def get_model_description(self):
        """Get aquaplus default setting."""
        url = f"http://{self.ip_address}/ai?command=getModelDescription"
        resp = await self.session.get(url)
        content = await resp.text()
        value = content
        self.device_model = value
        return value

    async def turn_off(self):
        """Turn off appliance."""
        url = f"http://{self.ip_address}/hh?command=doTurnOff"
        content = await self._get(url)
