import unittest
from aioresponses import aioresponses
import asyncio
import sys
sys.path.append('/home/colby/development/xfinity_scanner/src/xfinity_gateway')
from xfinity_gateway import XfinityGateway

class TestXfinity(unittest.TestCase):

    def test_something(self):
        assert(1==1)

    @aioresponses()
    def test_helloworld(self, m):
        f = open('./xfinityTestPage.html', 'r')
        text = f.read()
        f.close()
        m.get('http://10.0.0.1', status=200, body=text, repeat=True)

        gateway = XfinityGateway('10.0.0.1')

        async def run():
            await gateway._connect()
            print(await gateway.scan_devices())
            print(gateway.get_device_name('18:65:90:00:00:00'))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(run()))

if __name__ == '__main__':
    unittest.main()