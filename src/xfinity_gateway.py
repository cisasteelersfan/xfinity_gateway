from bs4 import BeautifulSoup as BS
import requests

TIMEOUT = 10

class XfinityGateway:

    def __init__(self, host):
        self.host = 'http://' + host
        self.last_results = {}

    def scan_devices(self):
        self._update_info()
        return self.last_results.keys()

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        raw_html = requests.get(self.host, timeout=TIMEOUT).text
        self._get_connected_devices(raw_html)

    def _get_connected_devices(self, html):
        try:
            soup = BS(html, 'html.parser')
            headers = soup.find(id='internet-usage').table.tr

            entries = [x for x in headers.next_siblings if x != '\n']

            self.last_results = dict([(e.find(headers='mac-address').text, e.find(headers='host-name').text) for e in entries])
        except:
            raise(ValueError())
