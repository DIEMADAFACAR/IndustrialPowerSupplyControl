from fastapi import APIRouter
from pydantic import BaseModel
from app.power_supply import PowerSupply
from dotenv import load_dotenv
import os

load_dotenv()

power_supply_host = os.getenv("POWER_SUPPLY_HOST")
power_supply_port = os.getenv("POWER_SUPPLY_PORT")
ps = PowerSupply(host=power_supply_host, port=power_supply_port)

power_supply_router = APIRouter()  # Создание роутера


class ChannelParams(BaseModel):
    voltage: float
    current: float


@power_supply_router.get("/status")
async def get_status():
    status = await ps.query_all_channel_status()
    return {"status": status}


@power_supply_router.post("/enable_channel/{channel}")
async def enable_channel(channel: int, params: ChannelParams):
    if not await ps.is_connected():
        await ps.connect()
    await ps.set_channel_voltage(channel, params.voltage)
    await ps.set_channel_current(channel, params.current)
    await ps.enable_channel_output(channel)
    return {"message": f"Channel {channel} is enabled."}


@power_supply_router.post("/disable_channel/{channel}")
async def disable_channel(channel: int):
    await ps.connect()
    await ps.disable_channel_output(channel)
    return {"message": f"Channel {channel} is disabled."}
