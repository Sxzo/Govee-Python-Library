import requests
import subprocess


device_url = "https://developer-api.govee.com/v1/devices"
control_url = "https://developer-api.govee.com/v1/devices/control"
state_url = "https://developer-api.govee.com/v1/devices/state?"

class Device:
    def __init__(self, name, model, id, key):
        self.name = name
        self.model = model
        self.id = id
        self.key = key

        # JSON to be used in request bodies
        self.control_json = {"device": id,
                             "model": model,
                             "cmd": {
                                "name": "x",
                                "value": "x"
                            }}

    # Change the object representation to the name of the device
    def __repr__(self):
        return self.name
    
    # @mode = "on", "off", or None
    def toggle(self, mode=None):
        # Preset JSON body 
        cmd_json = self.control_json

        # Handle general toggle
        if mode == None:
            # Get current powerstate:
            try:
                powerState = requests.get(f"{state_url}device={self.id}&model={self.model}", headers={"Govee-API-Key": self.key}).json()["data"]["properties"][1]["powerState"]
            except Exception as e:
                print(f"Something went wrong. {e}")

            if powerState == "off":
              cmd_json["cmd"]["name"] = "turn"
              cmd_json["cmd"]["value"] = "on"
            else: 
              cmd_json["cmd"]["name"] = "turn"
              cmd_json["cmd"]["value"] = "off"

        # Handle specified toggle
        elif mode == "on" or mode == "off":
              cmd_json["cmd"]["name"] = "turn"
              cmd_json["cmd"]["value"] = mode
        
        # Send request to govee devices
        try:
            ctrl_request = requests.put(control_url, headers={"Govee-API-Key": self.key}, json = cmd_json)
        except Exception as e:
            print(f"Something went wrong. {e}")

        # Ensure proper response from the network
        if ctrl_request.status_code != 200:
            raise Exception(f"An error occured. Error code: {ctrl_request.status_code}")

        
    # @brightness is a float 0-100.
    def set_brightness(self, brightness):
        # Preset JSON body 
        cmd_json = self.control_json
        
        # Ensure valid params
        brightness = int(brightness)
        if brightness > 100:
            brightness = 100
        if brightness < 0:
            brightness = 0
        
        cmd_json["cmd"]["name"] = "brightness"
        cmd_json["cmd"]["value"] = brightness

        # Send request to govee devices
        try:
            ctrl_request = requests.put(control_url, headers={"Govee-API-Key": self.key}, json = cmd_json)
        except Exception as e:
            print(f"Something went wrong. {e}")
        
        # Ensure proper response from the network
        if ctrl_request.status_code != 200:
            raise Exception(f"An error occured. Error code: {ctrl_request.status_code}")

    # @colors is a tuple of colors (R, G, B) where R,G,B are all integers 0-255
    def set_color(self, colors):
        R = float(colors[0])
        G = float(colors[1])
        B = float(colors[2])
        
        # Ensure valid params
        if R > 255:
            R = 225
        elif R < 0: 
            R = 0
        
        if G > 255:
            G = 225
        elif G < 0: 
            G = 0
        
        if B > 255:
            B = 225
        elif B < 0: 
            B = 0

        # Preset JSON body 
        cmd_json = self.control_json
        
        cmd_json["cmd"]["name"] = "color"
        cmd_json["cmd"]["value"] = {"r": R, "g": G, "b": B}

        # Send request to govee devices
        try:
            ctrl_request = requests.put(control_url, headers={"Govee-API-Key": self.key}, json = cmd_json)
        except Exception as e:
            print(f"Something went wrong. {e}")
        
        # Ensure proper response from the network
        if ctrl_request.status_code != 200:
            raise Exception(f"An error occured. Error code: {ctrl_request.status_code}")



# Client class representing the control center for all Govee lights on the network. 
class GoveeClient:
    # Construct the user client by discovering all devices on the network using their API key
    def __init__(self, api_key):
        self.key = api_key
        self.devices = []

        # Try the device discovery request
        try:
            discovery_req = requests.get(device_url, headers = {"Govee-API-Key": api_key})
        except Exception as e:
            print(f"Something went wrong. {e}")

        # Ensure proper response from the network
        if discovery_req.status_code != 200:
            raise Exception("An error occured when trying to initialize the client. Try checking your API key.")

        discovered_device_list = discovery_req.json()["data"]["devices"]
        for device in discovered_device_list:
            self.devices.append(Device(device["deviceName"], device["model"], device["device"], api_key))

        # Get Wifi SSID:
        try:
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            output = result.stdout
            lines = output.split('\n')
            for line in lines:
                if "SSID" in line:
                    wifi_name = line.split(":")[1].strip()
                    self.ssid = wifi_name
                    break
        except:
            print("Using default SSID.")
            self.ssid = "Admin"
    
    def __repr__(self):
        return f"{self.ssid}'s Govee Client"
