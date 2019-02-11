from bs4 import BeautifulSoup as BS
import lxml.html

class XfinityGateway:

    def __init__(self, host):
        self.host = host

        self.last_results = {}

        self._update_info()

    def scan_devices(self):
        self._update_info()
        return self.last_results.keys()

    def get_device_name(self, device):
        return self.last_results.get(device)

    def _update_info(self):
        f = open("xfinityTestPage.html", "r")
        test_page = f.read()
        self._get_bs4(test_page)
        # self._get_lxml(test_page)

    def _get_bs4(self, html):
        soup = BS(html, 'html.parser')
        headers = soup.find(id='internet-usage').table.tr

        entries = [x for x in headers.next_siblings if x != '\n']

        self.last_results = dict([(e.find(headers='mac-address').text, e.find(headers='host-name').text) for e in entries])

    def _get_lxml(self, html):
        parsed_doc = lxml.html.document_fromstring(html)
        
        rows = parsed_doc.get_element_by_id("internet-usage").find_class("form-row")

        self.last_results = dict([(row.find_class("readonlyLabel")[2].text_content(), row.find_class("readonlyLabel")[1].text_content()) for row in rows])

if __name__ == '__main__':
    device = XfinityGateway('10.0.0.1')    
    print(device.scan_devices())
    print(device.get_device_name('18:65:90:00:00:00'))