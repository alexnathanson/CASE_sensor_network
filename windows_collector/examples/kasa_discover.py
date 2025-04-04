#source: https://python-kasa.readthedocs.io/en/latest/tutorial.html

import asyncio
from kasa import Discover, Credentials

async def discoverSingle():
    #discover a single specific device
    device = await Discover.discover_single(
        "127.0.0.1",
        credentials=Credentials("myusername", "mypassword"),
        discovery_timeout=10
    )

    await device.update()  # Request the update
    print(device.alias)  # Print out the alias

async def discoverAll():
    #discover all available devices
    devices = await Discover.discover(
        credentials=Credentials("myusername", "mypassword"),
        discovery_timeout=10
    )
    for ip, device in devices.items():
        await device.update()
        print(device.alias + " at " + device.host)
        print(type(device))

    return devices

async def main():
    await discoverAll()

    # dev = await Discover.discover_single("127.0.0.1",username="un@example.com",password="pw")
    # await dev.turn_on()
    # await dev.update()

if __name__ == "__main__":
    asyncio.run(main())