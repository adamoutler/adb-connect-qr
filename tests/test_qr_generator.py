import unittest
from src.qr_generator import generate_pairing_string

class TestQRGenerator(unittest.TestCase):
    def test_generate_pairing_string(self):
        payload = generate_pairing_string("adb-cli-test", "123456")
        self.assertEqual(payload, "WIFI:T:ADB;S:adb-cli-test;P:123456;;")

if __name__ == '__main__':
    unittest.main()
