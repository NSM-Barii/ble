import asyncio
from bleak import BleakClient

DEVICE_MAC = "99:B9:05:1E:35:BC"  # <- Your device MAC here
WRITE_UUID = "00000001-0000-1001-8001-00805f9b07d0"

# OFF payload (boolean false)
off_payload = bytes.fromhex("02012E05000100040000")


async def toggle_plug():
    print("[*] Connecting to Tuya Plug...")
    client = BleakClient(DEVICE_MAC)

    await client.connect()
    if not client.is_connected:
        print("[-] Failed to connect.")
        return
    print("[+] Connected. Sending payload...")

    try:
        
        for crc in range(256):
            payload = bytes.fromhex("02012E0500010004") + bytes([crc])
            await client.write_gatt_char(WRITE_UUID, payload, response=True)
    except Exception as e:
        print(f"[-] Failed to write: {e}")

asyncio.run(toggle_plug())
