# Azure IoT Hub Consumer

A lightweight Python consumer that connects to an Azure IoT Hub/Event Hub and reads incoming device snapshot batches from the stream. Each batch is decoded and printed in the terminal as a readable dashboard.

## What this project does

This project listens for messages published by Azure IoT devices and prints the received telemetry in a simple console view. The app currently expects payloads with device and snapshot metadata, then displays each timestamp and its measurement values.

## Requirements

- Python 3.10 or later

## Setup

Create and activate a virtual environment, then install the required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root with your Azure IoT connection string:

```dotenv
AZURE_IOT_CONNECTION_STRING=
```

## Run

With the virtual environment active:

```powershell
python main.py
```

The application connects to the configured Event Hub and begins listening for incoming message batches. Stop it with `Ctrl+C`.

## Message format

The consumer expects JSON payloads that contain a list of devices and their snapshots. A typical payload looks like this:

```json
[
  {
    "deviceId": "device-01",
    "snapshot": [
      {
        "timestamp": "2026-10-25T12:00:00Z",
        "measurements": [
          {
            "type": "temperature",
            "value": 21.4,
            "unit": "C"
          },
          {
            "type": "humidity",
            "value": 42,
            "unit": "%"
          }
        ]
      }
    ]
  }
]
```

## Project structure

```text
AzIotHubConsumer/
├── main.py
├── dashboard/
│   ├── __init__.py
│   └── dashboard.py
├── .env
├── .gitignore
├── README.md
└── .venv/                     # local virtual environment
```

## How it works

- `main.py` loads the connection string from `.env`
- creates an `EventHubConsumerClient`
- listens continuously for incoming event batches
- passes each event payload to `Dashboard.handle_message()`
- `dashboard.py` parses the JSON and prints the data in the terminal
