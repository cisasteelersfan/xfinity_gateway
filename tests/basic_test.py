import unittest
import requests_mock
import requests
from xfinity_gateway import XfinityGateway

@requests_mock.Mocker()
class TestXfinity(unittest.TestCase):

    URL = 'http://10.0.0.1'
    CONNECTED_DEVICES = {'A0:F3:C1:00:00:00': 'TPLINK', '18:65:90:00:00:00': 'Colbys-iPhone', '48:A9:1C:00:00:00': 'Carloss-iPhone', '70:56:81:00:00:00': 'Colbys-Air', 'CC:9E:A2:00:00:00': 'amazon-4d73d5f06', '20:EE:28:00:00:00': 'Amandas-iPhone', '80:E6:50:00:00:00': 'Amandas-MBP-2'}

    @classmethod
    def setUpClass(cls):
        with open('./tests/xfinityTestPage.html', 'r') as fh:
            cls.test_xfinity_page = fh.read()


    def setup_matcher(self, m):
        m.get(self.URL, text=self.test_xfinity_page)
        m.get('http://10.0.0.2', exc=requests.exceptions.ConnectTimeout)
        m.get('http://10.0.0.3', text='<html></html>')

    def test_scan_devices(self, m):
        self.setup_matcher(m)

        gateway = XfinityGateway('10.0.0.1')
        
        self.assertEqual(gateway.scan_devices(), self.CONNECTED_DEVICES.keys())

    def test_get_device_name_valid(self, m):
        self.setup_matcher(m)

        gateway = XfinityGateway('10.0.0.1')
        gateway.scan_devices()

        self.assertEqual(gateway.get_device_name('18:65:90:00:00:00'), 'Colbys-iPhone')

    def test_invalid_host(self, m):
        self.setup_matcher(m)

        gateway = XfinityGateway('10.0.0.2')

        with self.assertRaises(requests.exceptions.RequestException):
            gateway.scan_devices()

    def test_wrong_host(self, m):
        self.setup_matcher(m)

        gateway = XfinityGateway('10.0.0.3')

        with self.assertRaises(ValueError):
            gateway.scan_devices()


if __name__ == '__main__':
    unittest.main()