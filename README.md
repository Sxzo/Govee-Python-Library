# Govee API 2.0 Python Library (2023)
This is a super simple interface for interacting with Govee smart lights via Python. 

There are three primary functions to control the lights:
- Toggle power
- Set brightness
- Set color

## Initializing a Client
To interact with Govee devices on your network, you'll need a Govee API key. You can request one from in-app or browser on the Govee platform. 
```
from govee import GoveeClient

client = GoveeClient("API KEY")
```
A client is initialized with 3 key values:
```
from govee import GoveeClient

client = GoveeClient("API KEY")

# Access the client device list:
client.devices

# Access the client network SSID
client.ssid

# Access the client API key
client.key
```

All device interaction revolves around actual device objects. All available devices at the time of client initialization are stored in `GoveeClient.devices`

## Toggle Power
`@param mode = "on", "off", or None`

```
from govee import GoveeClient

client = GoveeClient("API KEY")

# Get the first device object
wall_lights = client.devices[0]

# Toggle Power (if on -> off | if off -> on)
wall_lights.toggle()

# Turn on 
wall_lights.toggle(mode="on")

# Turn off
wall_lights.toggle(mode="off")

```

## Set Brightness
`@param int brightness = 0-100`

Note that setting the brightness to 0 will power off the device. 
```
from govee import GoveeClient

client = GoveeClient("API KEY")

# Get the first device object
wall_lights = client.devices[0]

# Set the brightness to 50%
wall_lights.set_brightness(50)

```

## Set Color
`@param tuple colors = ((0-255), (0-255), (0-255))`

@colors is in the format: (R, G, B)
```
from govee import GoveeClient

client = GoveeClient("API KEY")

# Get the first device object
wall_lights = client.devices[0]

# Set the lights red
wall_lights.set_color(255, 0, 0)

# Set the lights green
wall_lights.set_color(0, 255, 0)

# Set the lights blue
wall_lights.set_color(0, 0, 255)

```





<sub> *This functionality is dependent upon Govee's API which is not my creation. All rights and credit reserved to Govee 2023 ©.* </sub>
