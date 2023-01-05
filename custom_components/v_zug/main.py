"""Main as playground."""

import asyncio

import aiohttp

# from .api import Api
from api import Api

IP_ADDRESS ="192.168.0.186"

async def main():
    """Run main program."""
    session = aiohttp.ClientSession()
    api = Api(session=session, ip_address=IP_ADDRESS)
    await api.get_device_status()
    await api.get_last_push_notifications()
    await api.get_command_spinning()
    await api.get_command_soiling()
    await api.get_command_aquaplus()
    await api.get_model_description()

    await session.close()

    attrs = vars(api)
    print(f"\n {attrs}")
    # await api.turn_off()

    await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
