from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.power_supply import PowerSupply

app = FastAPI()
ps = PowerSupply(host="your_host", port="")


class ChannelParams(BaseModel):
    voltage: float
    current: float


async def connect_power_supply():
    try:
        await ps.connect()
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the power supply: {str(e)}")


@app.on_event("startup")
async def startup_event():
    await connect_power_supply()


@app.get("/status")
async def get_status():
    try:
        status = await ps.query_all_channel_status()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query status: {str(e)}")


@app.post("/enable_channel/{channel}")
async def enable_channel(channel: int, params: ChannelParams):
    try:
        if not await ps.is_connected():
            await connect_power_supply()
        await ps.set_channel_voltage(channel, params.voltage)
        await ps.set_channel_current(channel, params.current)
        await ps.enable_channel_output(channel)
        return {"message": f"Channel {channel} is enabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enable channel {channel}: {str(e)}")


@app.post("/disable_channel/{channel}")
async def disable_channel(channel: int):
    try:
        await connect_power_supply()
        await ps.disable_channel_output(channel)
        return {"message": f"Channel {channel} is disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to disable channel {channel}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
