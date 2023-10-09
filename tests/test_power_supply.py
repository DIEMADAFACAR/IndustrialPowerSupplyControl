import asynctest
from unittest.mock import patch, MagicMock
from app.power_supply import PowerSupply


class TestPowerSupply(asynctest.TestCase):
    @patch('app.power_supply.PowerSupply.connect')
    async def test_set_channel_current(self, mock_connect):
        mock_connect.return_value = None
        await self.power_supply.set_channel_current(1, 5)
        self.mock_connection.send.assert_called_with(":MEASure1:CURRent 5\n")

    async def setUp(self):
        self.mock_connection = MagicMock()
        self.power_supply = PowerSupply(host="mock_host", port=12345)
        self.power_supply.connection = self.mock_connection

    async def test_set_channel_voltage(self):
        await self.power_supply.set_channel_voltage(2, 10)
        self.mock_connection.send.assert_called_with(":MEASure2:VOLTage 10\n")

    async def test_enable_channel_output(self):
        await self.power_supply.enable_channel_output(3)
        self.mock_connection.send.assert_called_with(":OUTPut3:STATe 1\n")

    async def test_disable_channel_output(self):
        await self.power_supply.disable_channel_output(4)
        self.mock_connection.send.assert_called_with(":OUTPut4:STATe 0\n")

    async def test_query_channel_status(self):
        self.mock_connection.query.return_value = "ON"
        status = await self.power_supply.query_channel_status()
        self.assertEqual(status, "ON")
        self.mock_connection.query.assert_called_with(":OUTPut1:STATe?")

    async def test_query_voltage(self):
        self.mock_connection.recv.return_value = "5.0"
        voltage = await self.power_supply.query_voltage(1)
        self.assertEqual(voltage, 5.0)

    async def test_query_current(self):
        self.mock_connection.recv.return_value = "2.5"
        current = await self.power_supply.query_current(2)
        self.assertEqual(current, 2.5)

    async def test_query_power(self):
        self.mock_connection.recv.return_value = "10.0"
        power = await self.power_supply.query_power(3)
        self.assertEqual(power, 10.0)

    async def test_connect_exception(self):
        self.mock_connection.connect.side_effect = Exception("Connection error")
        with self.assertRaises(Exception):
            await self.power_supply.connect()

    async def test_query_all_channel_status(self):
        expected_status = {'channel_1': {'status': 'ON', 'current': 0.0}}
        self.mock_connection.query.return_value = "ON"
        status = await self.power_supply.query_all_channel_status()
        self.assertEqual(status, expected_status)

    async def test_send_command_exception(self):
        self.mock_connection.send.side_effect = Exception("Send error")
        with self.assertRaises(Exception):
            await self.power_supply.send_command(":MEASure1:CURRent 5\n")

    async def test_receive_response_exception(self):
        self.mock_connection.recv.side_effect = Exception("Receive error")
        with self.assertRaises(Exception):
            await self.power_supply.receive_response()


if __name__ == '__main__':
    asynctest.main()
