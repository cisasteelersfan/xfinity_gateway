import unittest
import requests_mock
import sys
sys.path.append('/home/colby/development/xfinity_scanner/src/xfinity_gateway')
from xfinity_gateway import XfinityGateway

@requests_mock.Mocker()
class TestXfinity(unittest.TestCase):

    URL = 'http://10.0.0.1'

    @classmethod
    def setUpClass(cls):
        with open('./xfinityTestPage.html', 'r') as fh:
            cls.test_xfinity_page = fh.read()


    def setup_matcher_valid(self, m):
        m.get(self.URL, text=self.test_xfinity_page)


    def test_get_device_name_valid(self, m):
        self.setup_matcher_valid(m)

        gateway = XfinityGateway('10.0.0.1')
        gateway.scan_devices()

        self.assertEqual(gateway.get_device_name('18:65:90:00:00:00'), 'Colbys-iPhone')


if __name__ == '__main__':
    unittest.main()