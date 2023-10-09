import unittest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


class TestAPI(unittest.TestCase):
    async def test_enable_channel(self):
        response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Channel 1 is enabled."})

    async def test_disable_channel(self):
        response = await client.post("/disable_channel/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Channel 1 is disabled."})

    async def test_get_status(self):
        response = await client.get("/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("status" in data)

    async def test_get_all_channels_status(self):
        response = await client.get("/all_channels_status")
        self.assertEqual(response.status_code, 200)
        data = response.json()

    async def test_enable_channel_connection_error(self):
        with patch('app.main.PowerSupply.is_connected', return_value=False):
            response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 500)

    async def test_enable_channel_error(self):
        with patch('app.main.PowerSupply.is_connected', return_value=True):
            with patch('app.main.PowerSupply.set_channel_voltage', side_effect=Exception("Test error")):
                response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 500)

    async def test_get_status_error(self):
        with patch('app.main.PowerSupply.query_all_channel_status', side_effect=Exception("Test error")):
            response = await client.get("/status")
        self.assertEqual(response.status_code, 500)

    async def test_get_all_channels_status_error(self):
        with patch('app.main.PowerSupply.query_all_channel_status', side_effect=Exception("Test error")):
            response = await client.get("/all_channels_status")
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()