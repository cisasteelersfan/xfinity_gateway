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


def get_scanner(hass, config):
    info = config[DOMAIN]
    host = info.get(CONF_HOST)

    scanner = XfinityDeviceScanner(host)

    return scanner if scanner.success_init else None

class XfinityDeviceScanner(DeviceScanner):

    def __init__(self, address):
        self.address = address

        self.last_results = {}

        self._update_info()

        self.success_init = True


    def scan_devices(self):
        self._update_info()

        return self.last_results.keys()

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        from bs4 import BeautifulSoup as BS
        request = self._make_request()
        _LOGGER.info("Scanning")

        try:
            soup = BS(request.content, 'html.parser')

            headers = soup.find(id='internet-usage').table.tr

            entries = [x for x in headers.next_siblings if x != '\n']

            self.last_results = dict([(e.find(headers='mac-address').text, e.find(headers='host-name').text) for e in entries])
        except:
            self.last_results = {}
            _LOGGER.warn("failed to scan xfinity device")

    def _make_request(self):
        return requests.get('http://'+self.address)

# device = XfinityDeviceScanner('10.0.0.1')

# print(device.scan_devices())