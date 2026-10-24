import json

from datetime import datetime


class Dashboard:
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self):
        self.anchor_row = 2
        self.device_rows = {}
        self.last_measurements = {}

    def move_cursor(self, relative_row: int):
        print(f"\033[{self.anchor_row + relative_row};1H", end="")

    def clear_line(self):
        print("\033[2K", end="")

    async def print_snapshots(self, batch):
        print(f"{self.CYAN}Received batch with {len(batch)} devices{self.RESET}\n")

        for device in batch:
            device_id = device["deviceId"]
            snapshots = device["snapshot"]

            print(f"{self.GREEN}Device: {device_id}{self.RESET}")
            print(f"Snapshots: {len(snapshots)}")

            for snap in snapshots:
                ts = snap["timestamp"]
                ts_local = datetime.fromisoformat(ts.replace("Z", "+00:00"))

                print(f"  {self.YELLOW}{ts_local}{self.RESET}")

                for m in snap["measurements"]:
                    print(f"    - {m['type']}: {m['value']} {m['unit']}")

            print() 

    async def handle_message(self, partition_context, event):
        try:
            payload = event.body_as_str()
            data = json.loads(payload)
            
            await self.print_snapshots(data)

        except Exception as ex:
            print("Error:", ex)

