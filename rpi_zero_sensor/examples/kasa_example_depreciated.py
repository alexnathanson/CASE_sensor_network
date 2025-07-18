# TP Link Kasa Smart Plug with Energy Monitoring
# This script no longer works for python-kasa V7
'''
documentation:
https://python-kasa.readthedocs.io/en/latest/index.html
https://python-kasa.readthedocs.io/en/latest/smartdevice.html
'''

import asyncio
# kasa.SmartPlug is not kasa.iot.IotPlug
from kasa import SmartPlug, Discover, Credentials

async def initialize():
	#discover a single specific device
    # device = await Discover.discover_single(
    #     "127.0.0.1",
    #     credentials=Credentials("myusername", "mypassword"),
    #     discovery_timeout=10
    # )

    # await device.update()  # Request the update
    # print(device.alias)  # Print out the alias

    #discover all available devices
    devices = await Discover.discover(
        credentials=Credentials("myusername", "mypassword"),
        discovery_timeout=10
    )
    for ip, device in devices.items():
        await device.update()
        print(device.alias + " ip: " + device.host)

    return devices

# get power and energy data
async def getData(ip):
	p = SmartPlug(ip)

	await p.update()

	# emerter_realtime still works but prints a depreciation error
	#print(p.emeter_realtime)
	print(str(p.emeter_realtime.power) + "W")
	print(str(p.emeter_realtime.current) + "A")
	print(str(p.emeter_realtime.voltage) + "V")
	print(str(p.emeter_today) + "Wh today")

# flip state of outlet 
async def flipState(ip):

	p = SmartPlug(ip)
	await p.update()

	if p.is_on:
		print(p.alias + ' is on. Turning off now...')
		await p.turn_off()
	else:
		print(p.alias + ' is off. Turning on now...')
		await p.turn_on()

async def main():
	deviceList = await initialize()

	for ip, device in deviceList.items():
		#flip = await flipState(ip)
		await getData(ip)

if __name__ == "__main__":
    asyncio.run(main())
