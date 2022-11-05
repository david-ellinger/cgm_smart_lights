import requests
import os

hue_bridge_ip = os.getenv("HUE_BRIDGE_IP")
hue_bridge_username = os.getenv("HUE_BRIDGE_USERNAME")

class Hue():
    def change_color(self, x, y):
        headers = {
            "Accept": "application/json",
        }
        light = 3
        data = '{"on":true,"xy":[%.4f,%.4f]}' % (x, y)
        result = requests.put(
            f"http://{hue_bridge_ip}/api/{hue_bridge_username}/lights/{light}/state",
            headers=headers,
            data=data,
        )
        return result.json()
