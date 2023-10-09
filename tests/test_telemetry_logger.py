import unittest
from unittest.mock import MagicMock, patch
from app.telemetry_logger import log_telemetry, logger

class TestTelemetryLogger(unittest.TestCase):
    @patch('app.telemetry_logger.logging.FileHandler')
    @patch('app.telemetry_logger.logging.getLogger')
    async def test_logging(self, mock_get_logger, mock_file_handler):
        # Testing logging
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        log_message = "Test log message"
        await log_telemetry(log_message)  # Await the asynchronous function
        mock_get_logger.assert_called_with(__name__)  # Check if getLogger was called with __name__
        mock_get_logger.assert_called_with('tests.test_telemetry_logger')
        mock_logger.addHandler.assert_called_with(mock_file_handler.return_value)
        mock_logger.info.assert_called_with(log_message)

if __name__ == '__main__':
    unittest.main()
