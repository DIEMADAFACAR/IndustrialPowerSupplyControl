![PyPI - Python Version](https://img.shields.io/pypi/pyversions/:packageName)
# Источник питания API

API для управления и мониторинга источника питания

## Структура проекта

- app/ - пакет с основной логикой
  - api.py
  - main.py
  - power_supply.py
  - telemetry_logger.py
- tests/ - тесты
  - test_api.py
  - test_main.py
  - test_power_supply.py
  - test_telemetry_logger.py
- logs/ - логи
  - telemetry.log
  - power_supply.log
- requirements.txt
- README.md

## Запуск тестов

Для запуска тестов:
bash
python -m unittest discover tests

## Установка

1. Склонируйте репозиторий на свой компьютер:
git clone https://github.com/yourusername/power-supply-api.git

   
2. Перейдите в каталог проекта:
cd power-supply-api

3. Установите зависимости с помощью pip:
pip install -r requirements.txt

## Запуск
1. Запустите сервер API:
python main.py


2. Сервер будет доступен по адресу http://localhost:8000

## Использование API
1. Установка тока для канала
- Метод: POST
- URL: /enable_channel/{channel}
- Параметры запроса:
  - channel (int): Номер канала
  - voltage (float): Заданное напряжение
  - current (float): Заданный ток
- Пример запроса:
  ```
  POST /enable_channel/1
  {
    "voltage": 5.0,
    "current": 2.0
  }
  ```

2. Включение канала
- Метод: POST
- URL: /enable_channel/{channel}
- Параметры запроса:
  - channel (int): Номер канала
- Пример запроса:
  ```
  POST /enable_channel/1
  ```

3. Запрос состояния канала
- Метод: GET
- URL: /channel_status/{channel}
- Параметры запроса:
  - channel (int): Номер канала
- Пример запроса:
  ```
  GET /channel_status/1
  ```

4. Получение данных о всех каналах
- Метод: GET
- URL: /all_channels_status
- Пример запроса:
  ```
  GET /all_channels_status
  ```

## Документация на источник питания
https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/14242/1737


