from src.xfinity_gateway.xfinity_gateway import XfinityGateway
import asyncio
import logging

import voluptuous as vol

import requests
import json

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_PORT)

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = '10.0.0.1'
DEFAULT_PORT = 80

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string
})


async def async_get_scanner(hass, config):
    info = config[DOMAIN]
    host = info.get(CONF_HOST)

    scanner = XfinityDeviceScanner(host)
    await scanner._connect()

    return scanner if scanner.success_init else None

class XfinityDeviceScanner(DeviceScanner):

    def __init__(self, address):
        self.success_init = False
        try:
            self.xfinity_gateway = XfinityGateway(address)
            self.success_init = True
        except:
            print("!!!!!! Error setting up gateway")
            pass

    async def async_scan_devices(self):
        return await self.xfinity_gateway.scan_devices()

    async def async_get_device_name(self, device):
        return self.xfinity_gateway.get_device_name(device)



if __name__ == '__main__':
    async def run():
        device = XfinityDeviceScanner('10.0.0.1')

        print(await device.async_scan_devices())
        print(await device.async_get_device_name('18:65:90:00:00:00'))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(run()))