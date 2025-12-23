# TEST MODULE WILL BE STARTING BLE FRAMEWORK FROM HERE
 

# UI IMPORTS
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Console


# HACKING IMPORTS
from bleak import BleakClient, BleakScanner


# ETC IMPORTS
import asyncio, os, time

console = Console()



class BLE_Sniffer(): 
    """This will be a ble hacking framework"""



    @classmethod
    async def _ble_discover(cls):
        """This will sniff traffic"""


        devices =  await BleakScanner.discover(timeout=2, return_adv=True)

        return devices
    


    @classmethod
    def _ble_printer(cls):
        """Lets enumerate"""


        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold green"
        c4 = "bold red"
        c5 = "bold blue"


        try:

            devices = asyncio.run(BLE_Sniffer._ble_discover())
            
            if not devices: return

            
            
            for mac, (device, adv) in devices.items():

                if mac not in cls.devices:


                    name = adv.local_name or False
                    rssi = adv.rssi
                    uuid = adv.service_uuids or False
                    manuf = adv.manufacturer_data


                    data = {
                        "addr": mac,
                        "rssi": rssi,
                        "name": name,
                        "manuf": manuf,
                        "uuid": uuid
                    }

                    cls.devices.append(mac)
                    cls.data[mac] = data

                    p1 = c3
                    p2 = "white"



                    console.print(f"[{c2}][+][/{c2}] [{p1}]Addr:[{p2}] {mac} - [{p1}]RSSI:[{p2}] {rssi} - [{p1}]Local_name:[{p2}] {name} - [{p1}]Manufacturer:[{p2}] {manuf} - [{p1}]UUID:[{p2}] {uuid}")
            

        except Exception as e:
            console.print(f"[bold red]Sniffer Exception Error:[bold yellow] {e}")



        
    @classmethod
    def main(cls, timeout):
        """Run from here"""

        cls.devices = []
        cls.data = {}

        i = 0
        try:
            while i < timeout:
                BLE_Sniffer._ble_printer(); timeout -= 2
        
        except KeyboardInterrupt:
            console.print("\n[bold red]Stopping....")
        
        except Exception as e:
            console.print(f"[bold red]Sniffer Exception Error:[bold yellow] {e}")
            
        #console.print(cls.devices)

        #for mac in cls.devices:

            #if mac == "CC:38:35:30:6F:83": return mac



class BLE_Enumerater():
    """This class will be responsible for performing connections --> BLE"""



    async def _connect(target):
        """This method will be responsible for device connection"""


        try:

            console.print(f"[bold yellow][*] Attempting Connection...")


            async with BleakClient(target) as client:

                if client.is_connected:

                    console.print(f"[bold green][+] Successfully Connected to:[red] {target}")

                    
                    # ENUMARATE SERVICES
                    await BLE_Enumerater._enumeration(client=client) 

                    console.print(f"\n\n[bold red][-] Disconnected from:[bold yellow] {target}"); return True
                
                 
                console.print(f"\n\n[bold red][-] Failed to connect to:[bold yellow] {target}"); return False

        


        except Exception as e:
            console.print(f"[bold red]Connector Exception Error:[bold yellow] {e}")

 

    @classmethod
    async def _enumeration(cls, client: str) -> list:
        """Service Enumeration"""



        try:

            services = list(client.services)
            if not services: console.print("[bold red][-] No services found on this device!"); return

            console.print(f"[bold green][*][bold yellow] Found {len(services)} service(s).\n")


            # ENUMERATE SERVICES
            num = 0
            for service in services:
                
                num += 1; table = Table(title=f"Service #{num}", style="bold red",header_style="bold red", border_style="bold purple", title_style="bold green")
                table.add_column("Key", style="bold green")
                table.add_column("Value", style="bold yellow")


                uuid = service.uuid; description = service.description; handle = service.handle
                characteristics = service.characteristics or False


                
                table.add_row("UUID", f"{uuid}"); table.add_row("Description", f"{description}"); table.add_row(f"Handle", f"{handle}"); table.add_row("Char #", f"{len(characteristics)}")
                console.print(table, "")
                


                if not characteristics: continue
                c = len(characteristics)

                for char in characteristics:

                    space = " " * 8
                    c1 = "bold red"; c2 = "bold yellow"; c3 = "bold green"
                    uuid = char.uuid; description = char.description
                    handle = char.handle; properties = char.properties

                    console.print(
                        f"{space}[{c3}][+] UUID:[white] {uuid}"
                        f"\n{space}[{c3}][+] Description:[/{c3}] {description}"
                        f"\n{space}[{c3}][+] Handle:[/{c3}] {handle}"
                        f"\n{space}[{c3}][+] Properties:[/{c3}] {','.join(properties)}"                  
                        )
                    
                            
                                                                        
                    if c > 1: lines = '=' * 50; console.print(f'[yellow]{space}{lines}'); c -= 1                    
                    else: print("\n")



        except Exception as e:
            console.print(f"[bold red]Connector Exception Error:[bold yellow] {e}")

    

    @classmethod
    def main(cls, target):
        """This will run class methods"""


        print("\n\n")
        asyncio.run(BLE_Enumerater._connect(target=target))



class BLE_Fuzzer():
    """This class will be responsible for fuzzing ble chars"""


    @classmethod
    async def _connector(cls, target: str, uuid, f_type):
        """This method will connect and create client"""



        try:

            console.print(f"[bold yellow][*] Attempting Connection...")


            async with BleakClient(target) as client:

                if client.is_connected:

                    console.print(f"[bold green][+] Successfully Connected to: {target}")

                    
                    # FUZZ SERVICES
                    await BLE_Fuzzer._fuzzer(client=client, uuid=uuid, f_type=f_type) 

                    console.print(f"\n\n[bold red][-] Disconnected from:[bold yellow] {target}"); return True
                
                 
                console.print(f"\n\n[bold red][-] Failed to connect to:[bold yellow] {target}"); return False

        


        except Exception as e:
            console.print(f"[bold red]Connector Exception Error:[bold yellow] {e}")



    @classmethod
    async def _fuzzer(cls, client, uuid: any, f_type: int):
        """Lets get to fuzzing"""

        print("\n")


        t = 100000000

        payloads = [
            b'\x01\x01',
            b'\x01\xFF',
            b'\xA0\x01',
            b'\xAA\x55\x01\x00\x00',
            b'\x01\x03\x00\x00\x00',
            b'\xFF'*5,
            b'\x00'*5,
        ]

        console.print(f"[bold green][+] Fuzz Type:[/bold green] {f_type}")
        console.print(f"[bold green][+] Fuzzing --> [/bold green] {uuid} \n"); time.sleep(.5)
 
        
        if f_type == 1:

            for p in payloads:

                await client.write_gatt_char(char_specifier=uuid, data=p); t -= 1
                console.print(f"[bold red][!] Fuzzing:[cyan] {p.hex()}")
        
        elif f_type == 2:
            while t > 0:
                payload = os.urandom(40)
                await client.write_gatt_char(char_specifier=uuid, data=payload); t -= 1
                console.print(f"[bold red][!] Fuzzing:[cyan] {payload.hex()}")
    


    @classmethod
    def main(cls, target: str, uuid: any, f_type:int=1):
        """Class starts from here"""


        print("\n\n")
        asyncio.run(BLE_Fuzzer._connector(target=target, uuid=uuid, f_type=f_type))
        

        




if __name__ == "__main__":
    target = BLE_Sniffer.main()
    BLE_Enumerater.main(target=target)