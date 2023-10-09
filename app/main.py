from app.power_supply import PowerSupply
from fastapi import FastAPI

import asyncio

app = FastAPI()
power_supply = PowerSupply(host="your_power_supply_ip", port="")


async def poll_telemetry():
    try:
        while True:
            await power_supply.poll_telemetry()
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        # Обработка отмены задачи (например, при завершении приложения)
        pass
    except Exception as e:
        # Обработка других ошибок и логирование
        print(f"Error in telemetry polling: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    telemetry_task = loop.create_task(poll_telemetry())
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        # Обработка сигнала Ctrl+C для корректного завершения
        print("Received KeyboardInterrupt. Stopping...")
        telemetry_task.cancel()
        loop.run_until_complete(telemetry_task)