import unittest
from unittest.mock import patch, MagicMock
from src.adb_wrapper import pair_device, connect_device

class TestAdbWrapper(unittest.TestCase):
    @patch('subprocess.run')
    def test_pair_device(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Successfully paired")
        success = pair_device("192.168.1.10", 44444, "123456")
        self.assertTrue(success)
        mock_run.assert_called_with(['adb', 'pair', '192.168.1.10:44444', '123456'], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_connect_device(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="connected")
        success = connect_device("192.168.1.10", 55555)
        self.assertTrue(success)
        mock_run.assert_called_with(['adb', 'connect', '192.168.1.10:55555'], capture_output=True, text=True)

if __name__ == '__main__':
    unittest.main()
