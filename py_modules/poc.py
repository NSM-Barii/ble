import asyncio
from bleak import BleakClient
from rich.console import Console

console = Console()

# === CONFIG ===
TARGET_ADDR = "CC:38:35:30:6F:83"
TIMEOUT = 3.0

async def main():
    console.print(f"[yellow][*] Connecting to {TARGET_ADDR}...")
    client = BleakClient(TARGET_ADDR, timeout=TIMEOUT)

    try:
        await client.connect()
        if client.is_connected:
            console.print("[green][+] Connected.")
            input("[cyan]>>> Unlock the lock now, then press [Enter] to disconnect...")

    except Exception as e:
        console.print(f"[red]Connection failed: {e}")
    finally:
        try:
            await client.disconnect()
            console.print("[bold red][!] Disconnected.")
        except Exception as e:
            console.print(f"[red]Disconnection failed: {e}")


print("fsf")
if __name__ == "__main__":
    print("dfds")
    asyncio.run(main())
