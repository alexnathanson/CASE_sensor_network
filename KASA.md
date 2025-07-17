# Kasa

There are 4 Kasa smart plugs in use.

Model: KP125M<br>
Max Load: 15A 1800W

## Setup
You must use the Kasa app to set up the devices and connect them to the network. This requires an account, which is tied to the Kasa username and password. These can be found in the Login & Credentials doc.

In the unlikely event that you need to make changes to the device, you can perform a factory reset and complete the setup instructions on the app. <bold>If you do this, you must update the .env file (and the L&C Google Doc) with the updated credentials.</bold> This file is located in the rpi_zero_sensor directory of each device. You must update all of them.

When setting up a Kasa plug:
* Be sure to use the correct unique name. Devices are named kasa1 to kasa4.
* Make sure they are on the correct wifi network.
* Once set up, in the Kasa app, make sure the default state is set to on.