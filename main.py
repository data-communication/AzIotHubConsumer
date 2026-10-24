import asyncio
import sys
import os

from dotenv import load_dotenv
from azure.eventhub.aio import EventHubConsumerClient

from dashboard.dashboard import Dashboard


async def main():
    load_dotenv()

    azure_client = EventHubConsumerClient.from_connection_string(
        conn_str=os.getenv("AZURE_IOT_CONNECTION_STRING"),
        consumer_group="$Default"
    )

    dashboard = Dashboard()

    print("Connected. Listening for snapshot batches...\n")

    try:
        while True:
            async with azure_client:
                    await azure_client.receive(dashboard.handle_message)

    except asyncio.CancelledError:
        print("Shutting down.")
    finally:
        await azure_client.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(main())