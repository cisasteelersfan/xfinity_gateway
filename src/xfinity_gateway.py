import lxml.html
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
        self._get_lxml(raw_html)

    def _get_lxml(self, html):
        try:
            parsed_doc = lxml.html.document_fromstring(html)
            
            rows = parsed_doc.get_element_by_id('internet-usage').find_class('form-row')

            self.last_results = dict([(row.find_class('readonlyLabel')[2].text_content(), row.find_class('readonlyLabel')[1].text_content()) for row in rows])
        except:
            raise(ValueError())


if __name__ == '__main__':
    device = XfinityGateway('10.0.0.1')
    print(device.scan_devices())
    print(device.get_device_name('18:65:90:00:00:00'))