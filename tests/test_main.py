import unittest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestMain(unittest.TestCase):
    async def test_status_route(self):
        # Проверяем маршрут /status
        response = await client.get("/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        data = response.json()
        self.assertTrue("status" in data)
        self.assertIsInstance(data["status"], dict)

        # Проверяем наличие ожидаемых ключей в данных статуса
        expected_keys = ["channel_1", "channel_2", "channel_3", "channel_4"]
        for key in expected_keys:
            self.assertIn(key, data["status"])
            self.assertIsInstance(data["status"][key], dict)
            self.assertIn("status", data["status"][key])
            self.assertIn("current", data["status"][key])

    async def test_enable_channel_route(self):
        # Проверяем маршрут /enable_channel/{channel}
        response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"message": "Channel 1 is enabled."})

    async def test_disable_channel_route(self):
        # Проверяем маршрут /disable_channel/{channel}
        response = await client.post("/disable_channel/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"message": "Channel 1 is disabled."})

    async def test_enable_channel_invalid_data(self):
        # Проверяем маршрут /enable_channel/{channel} с недопустимыми данными
        response = await client.post("/enable_channel/1", json={"voltage": -5.0, "current": 2.0})
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("voltage", data["detail"][0]["ctx"]["field_errors"])
        self.assertIn("current", data["detail"][0]["ctx"]["field_errors"])

    async def test_enable_channel_connection_error(self):
        # Проверяем маршрут /enable_channel/{channel} при ошибке соединения
        with unittest.mock.patch('app.main.PowerSupply.is_connected', return_value=False):
            response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 500)

    async def test_enable_channel_error(self):
        # Проверяем маршрут /enable_channel/{channel} при ошибке настройки канала
        with unittest.mock.patch('app.main.PowerSupply.is_connected', return_value=True):
            with unittest.mock.patch('app.main.PowerSupply.set_channel_voltage', side_effect=Exception("Test error")):
                response = await client.post("/enable_channel/1", json={"voltage": 5.0, "current": 2.0})
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()