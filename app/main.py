from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import asyncio
import os
from app.power_supply import PowerSupply
from app.api import power_supply_router

load_dotenv()

power_supply_host = os.getenv("POWER_SUPPLY_HOST")
power_supply_port = os.getenv("POWER_SUPPLY_PORT")
power_supply = PowerSupply(host=power_supply_host, port=power_supply_port)
app = FastAPI()

# Подключение роутера
app.include_router(power_supply_router)


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

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

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
