"""Api."""
from __future__ import annotations

import asyncio
import datetime

import aiohttp


class Api:
    """Api."""

    def __init__(self, session: aiohttp.ClientSession, ip_address, attempts=2):
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
        self.program_end: datetime.time | None = None
        self.device_uuid: str = ""

        # Updated in api call get_last_push_notifications
        self.messages: list = []
        self.messages_txt = ""

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
            if content == {"error": {"code": 503.01}}:
                await asyncio.sleep(0.1)
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
        self.status_action = self.status.split("\n")[0]
        self.status_end_time = self.status.split("\n")[1]
        # self.program_end = c["ProgramEnd"]["End"]
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
        for message_dict in content:
            date = message_dict["date"]
            message = message_dict["message"]
            date_obj = datetime.datetime.fromisoformat(date[:-1])
            time_str = date_obj.strftime("%a @ %H:%M")
            messages_txt += f"**{time_str}** {message}\n"
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
