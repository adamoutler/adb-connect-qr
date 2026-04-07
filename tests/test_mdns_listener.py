import unittest
from src.mdns_listener import AdbPairingListener

class DummyServiceInfo:
    def __init__(self, addresses, port):
        self._addresses = addresses
        self.port = port
    def parsed_addresses(self):
        return self._addresses

class TestMdnsListener(unittest.TestCase):
    def test_listener_stores_info(self):
        listener = AdbPairingListener("adb-cli-test")
        info = DummyServiceInfo(["192.168.1.10"], 44444)
        # Simulate zeroconf callback
        listener.on_service_found(info, "adb-cli-test")
        self.assertEqual(listener.ip_address, "192.168.1.10")
        self.assertEqual(listener.port, 44444)

if __name__ == '__main__':
    unittest.main()
