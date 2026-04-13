# DOCUMENATION FOR REFERENCE // LETS MAKE IT BETTER LOL


import asyncio
import sys
import argparse
from bleak import BleakClient
from bleak.exc import BleakError
from datetime import datetime

async def explore_device_services(client, show_descriptors=True):
    """
    Explore all services and characteristics of a connected BLE device.

    Args:
        client (BleakClient): Connected BLE client
    """
    try:
        # Get all services as a list
        services = list(client.services)
        if not services:
            print("No services found on this device.")
            return

        print(f"Found {len(services)} service(s):")
        print("=" * 80)

        for service in services:
            print(f"\nService: {service.uuid}")
            print(f"Description: {service.description}")
            print(f"Handle: {service.handle}")

            # Get characteristics for this service
            characteristics = service.characteristics

            if characteristics:
                print(f"  Characteristics ({len(characteristics)}):")
                print("  " + "-" * 76)

                for char in characteristics:
                    print(f"    UUID: {char.uuid}")
                    print(f"    Description: {char.description}")
                    print(f"    Handle: {char.handle}")
                    print(f"    Properties: {', '.join(char.properties)}")

                    # Try to read the characteristic if it's readable
                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            # Try to decode as string, otherwise show as hex
                            try:
                                decoded_value = value.decode('utf-8')
                                print(f"    Value (string): {decoded_value}")
                            except UnicodeDecodeError:
                                hex_value = ' '.join(f'{b:02x}' for b in value)
                                print(f"    Value (hex): {hex_value}")
                                print(f"    Value (raw bytes): {value}")
                        except Exception as e:
                            print(f"    Value: <Could not read - {e}>")

                    # Show descriptors only if requested
                    if show_descriptors:
                        descriptors = char.descriptors
                        if descriptors:
                            print(f"\n    Descriptors ({len(descriptors)}):")
                            for desc in descriptors:
                                print(f"      UUID: {desc.uuid}")
                                print(f"      Description: {desc.description}")
                                print(f"      Handle: {desc.handle}")
                                # Try to read descriptor if possible
                                try:
                                    desc_value = await client.read_gatt_descriptor(desc.handle)
                                    try:
                                        decoded_desc = desc_value.decode('utf-8')
                                        print(f"      Value (string): {decoded_desc}")
                                    except UnicodeDecodeError:
                                        hex_desc = ' '.join(f'{b:02x}' for b in desc_value)
                                        print(f"      Value (hex): {hex_desc}")
                                except Exception as e:
                                    print(f"      Value: <Could not read - {e}>")
                            print()  # Empty line between characteristics
                    else:
                        print()
            else:
                print("    No characteristics found for this service.")

            print("-" * 80)

    except Exception as e:
        print(f"Error exploring services: {e}")


async def connect_and_explore(mac_address, show_descriptors=False):
    """
    Connect to a BLE device and explore its services.

    Args:
        mac_address (str): MAC address of the device to connect to
        scan_time (int): Duration to scan for the device
    """
    print(f"\nAttempting to connect to {mac_address} ...")
    try:
        async with BleakClient(mac_address) as client:
            if client.is_connected:
                print(f"Successfully connected to {mac_address}")
                print(f"Connected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                # Explore all services and characteristics
                await explore_device_services(client, show_descriptors=show_descriptors)
                print(f"\nDisconnected from {mac_address}")
                return True
            else:
                print(f"Failed to connect to {mac_address}")
                return False
    except BleakError as e:
        print(f"Bluetooth error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


async def main():
    """
    Main function to run the BLE device connector and explorer.
    """
    print("BLE Device Connection and Service Explorer")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    parser = argparse.ArgumentParser(description="Connect to a BLE device and list all services and attributes.")
    parser.add_argument("-m", nargs="?", default="24:EC:4A:76:00:32", help="MAC address of the BLE device (default: 24:EC:4A:76:00:32)")
    parser.add_argument("-d", "--descriptors", action="store_true", help="Show individual descriptors for each characteristic")
    args = parser.parse_args()

    mac_address = args.m
    show_descriptors = args.descriptors

    print(f"Using MAC address: {mac_address}")
    if show_descriptors:
        print("Descriptor display enabled.")

    # Validate MAC address format (basic check)
    if len(mac_address.replace(":", "").replace("-", "")) != 12:
        print(f"Invalid MAC address format: {mac_address}")
        print("Expected format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX")
        return

    print()

    # Connect and explore the device
    success = await connect_and_explore(mac_address, show_descriptors=show_descriptors)

    if success:
        print("\nDevice exploration completed successfully.")
    else:
        print("\nDevice exploration failed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)