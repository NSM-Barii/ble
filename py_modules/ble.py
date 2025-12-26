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


# NSM IMPORTS
from utilities import Utilities

console = Console()



class BLE_Sniffer(): 
    """This will be a ble hacking framework"""



    @classmethod
    async def _ble_discover(cls):
        """This will sniff traffic"""


        devices =  await BleakScanner.discover(timeout=2, return_adv=True)

        return devices
    
    

    @staticmethod
    def _get_manuf(manuf):
        """This will parse and get manuf"""


        data = {}

        for key, value in manuf.items():
            data[key] = value.hex()

        return data



    @classmethod
    def _ble_printer(cls, timeout, vendor_lookup):
        """Lets enumerate"""


        c1 = "bold red"
        c2 = "bold yellow"
        c3 = "bold green"
        c4 = "bold red"
        c5 = "bold blue"
        table = Table(title="BLE Sniffer", title_style="bold red", border_style="bold purple", style="bold purple", header_style="bold red")
        if vendor_lookup: table.add_column("RSSI", style=c2); table.add_column("Mac", style=c3); table.add_column("Vendor"); table.add_column("Local_name", style=c5); table.add_column("Manufacturer"); table.add_column("UUID", style=c3)
        else: table.add_column("RSSI", style=c2); table.add_column("Mac", style=c3); table.add_column("Local_name", style=c5); table.add_column("Manufacturer"); table.add_column("UUID", style=c3)


        try:

            with Live(table, console=console, refresh_per_second=4):
                while 0 < timeout:

                    devices = asyncio.run(BLE_Sniffer._ble_discover()); timeout -= 2
                    
                    if not devices: return

                    
                    
                    for mac, (device, adv) in devices.items():

                        if mac not in cls.devices:


                            name  = adv.local_name or False
                            rssi  = adv.rssi
                            uuid  = adv.service_uuids or False
                            manuf = BLE_Sniffer._get_manuf(manuf=adv.manufacturer_data) or False
                            if vendor_lookup: vendor = Utilities.get_vendor(mac=mac, verbose=False) or False


                            data = {
                                "addr": mac,
                                "rssi": rssi,
                                "name": name,
                                "manuf": manuf,
                                "uuid": uuid
                            }

                            cls.devices.append(mac)


                            p1 = c3; p2 = "white" 
                             
                            if vendor_lookup: table.add_row(f"{rssi}",f"{mac}", f"{vendor}", f"{name}", f"{manuf}",  f"{uuid}")
                            else:             table.add_row(f"{rssi}", f"{mac}", f"{name}", f"{manuf}", f"{uuid}")
                            #if vendor_lookup:  console.print(f"[{c2}][+][/{c2}] [{p1}]Addr:[{p2}] {mac} - [{p1}]RSSI:[{p2}] {rssi} - [{p1}]Local_name:[{p2}] {name} - [{p1}]Manufacturer:[{p2}] {manuf} - [{p1}]UUID:[{p2}] {uuid}") 
                            #else: console.print(f"[{c2}][+][/{c2}] [{p1}]Addr:[{p2}] {mac} - [{p1}]RSSI:[{p2}] {rssi} - [{p1}]Local_name:[{p2}] {name} - [{p1}]Manufacturer:[{p2}] {manuf} - [{p1}]UUID:[{p2}] {uuid}")
    
                
        except KeyboardInterrupt:
            return KeyboardInterrupt


        except Exception as e:
            return Exception



        
    @classmethod
    def main(cls, timeout, vendor_lookup):
        """Run from here"""

        cls.devices = []


        try:

            BLE_Sniffer._ble_printer(timeout=timeout, vendor_lookup=vendor_lookup)
        

        
        except KeyboardInterrupt:
            console.print("\n[bold red]Stopping....")
        
        except Exception as e:
            console.print(f"[bold red]Sniffer Exception Error:[bold yellow] {e}")
            

class BLE_Enumerater():
    """This class will be responsible for performing connections --> BLE"""



    async def _connect(target):
        """This method will be responsible for device connection"""

        while True:
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
                console.print(f"[bold red]Enumerator Exception Error:[bold yellow] {e}")

 

    @classmethod
    async def _enumeration(cls, client: str) -> list:
        """Service Enumeration"""



        try:

            services = list(client.services)
            if not services: console.print("[bold red][-] No services found on this device!"); return

            console.print(f"[bold green][*][bold yellow] Found {len(services)} service(s).\n")


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
    async def _connector(cls, target: str, uuid, send, response, f_type):
        """This method will connect and create client"""


        while True:
            try:

                console.print(f"[bold yellow][*] Attempting Connection...")


                async with BleakClient(target) as client:

                    if client.is_connected:

                        console.print(f"[bold green][+] Successfully Connected to: {target}")


                        # GET UUIDS if uuid == False
                        if uuid == True: uuid = await BLE_Fuzzer._get_uuids(client=client)
                        
                        # FUZZ SERVICES
                        await BLE_Fuzzer._fuzzer(client=client, uuid=uuid, send=send, response=response, f_type=f_type)

                        console.print(f"\n\n[bold red][-] Disconnected from:[bold yellow] {target}"); return True
                    
                    
                    console.print(f"\n\n[bold red][-] Failed to connect to:[bold yellow] {target}"); return False

            


            except Exception as e:
                console.print(f"[bold red]Fuzzer Exception Error:[bold yellow] {e}")
        

    
    @classmethod
    async def _get_uuids(cls, client):
        """This method will be responsible for automatically pulling uuids and chars to then pass them to --> _fuzzer"""

        
        services_characteristics_data = {}
        c_count = 0
        services = list(client.services) or False


        if not services: console.print("[bold red][!] No services were found!"); return False
        

       
        for service in services:

            
            try:

                service_uuid = service.uuid; description = service.description; handle = service.handle; characteristics = service.characteristics or False 

                services_characteristics_data[str(service_uuid)] = {
                    "uuid": service_uuid,
                    "description": description,
                    "handle": handle,
                    "character_#": len(characteristics),
                    "characteristics": {}
                }


                if not characteristics: continue
                chars = []


                for character in characteristics:

                    uuid = character.uuid; description = character.description; handle = character.handle; properties = character.properties
                    hi = (uuid, properties); chars.append(hi); c_count+= 1

        
            except Exception as e:
                console.print(f"[bold red]Exception Error:[bold yellow] {e}")
            

            finally: 
                console.print(f"[bold green][*][bold yellow] Found {len(services)} service(s) & {c_count} Characteristic(s)).\n"); return chars

                    

    @classmethod
    async def _fuzzer(cls, client, uuid: any, send, response, f_type: int):
        """Lets get to fuzzing"""


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


        def noty(uuid, char):
            """This will be a callback for notifications"""

            console.print(f"[bold green][*] UUID:[/bold green] {uuid} -> {char}")
            
            #await client.pair()
            #await client.start_notify(char_specifier="00000002-0000-1001-8001-00805f9b07d0", callback=noty)
        

        valid_uuids = []; raw = send.split(','); send = [s.strip() for s in raw if s.strip()] 
        
        if "all" not in send:

            for s in send:
                for id in uuid:
                    identify = id[0]; properties = id[1]
                    if s in properties: 
                        console.print(f"[bold yellow][!][/bold yellow] {s} --> {properties} --> {identify}")
                        valid_uuids.append(identify)
            

        
        else: 
            
            for id in uuid:
                identify = id[0]; properties = id[1] 
                console.print(f"[bold yellow][!][/bold yellow] all --> {properties} --> {identify}")
                valid_uuids.append(identify) 

         

        console.print(f"[bold red][+] Fuzzing[/bold red][bold yellow] -->[/bold yellow] {valid_uuids}\n")
        


        try:

            if f_type == 1:

                for p in payloads:
                    for id in valid_uuids:
                        
                        await client.write_gatt_char(char_specifier=str(id).strip(), data=p, response=response); t -= 1
                        console.print(f"[bold red][*] Fuzzing:[cyan] {p.hex()}")
            
            elif f_type == 2:

                while t > 0:
                    for id in valid_uuids:
                        for payload in payloads:
                        
                            payload = os.urandom(5)
                            await client.write_gatt_char(char_specifier=str(id).strip(), data=payload, response=response); t -= 1
                            console.print(f"[bold red][*] Fuzzing:[cyan] {payload.hex()}")
                
                        await asyncio.sleep(1)

        except Exception as e:
            console.print(f"[bold red]Fuzzer Exception Error:[bold yellow] {e}")



    @classmethod
    def main(cls, target: str, uuid: any, send, response, f_type:int=1):
        """Class starts from here"""


        print("")
        asyncio.run(BLE_Fuzzer._connector(target=target, uuid=uuid, send=send, response=response, f_type=f_type))
        

class BLE_Connection_Spam():
    """This kik"""        


    
    @classmethod
    async def _connection_spam(cls, target):
        """Rapidly connect and disconnect from target"""


        active = True
        connections = 0
        client = BleakClient(address_or_ble_device=target, timeout=10)

        console.print(f"[bold yellow][*] Attempting Connection...")


        while active:
            try:
                    

              
                await client.connect()
                await client.pair()
                console.print("tried to pair")
                await asyncio.sleep(0.3)
                await client.disconnect()
                print("f")
                console.print(f"[bold red][!][bold yellow] Connection #{connections}"); connections += 1
                await client.pair()
                client.write_gatt_char(char_specifier="00000001-0000-1001-8001-00805f9b07d0", data=os.urandom(5), response=True)
                
                #await client.unpair()
                #if client.is_connected: await client.disconnect()
            


                #await client.connect(); connections += 1; await asyncio.sleep(0.01)
                #await client.pair(); await asyncio.sleep(0.1); await client.unpair()
                #await client.disconnect()
            

            
            except Exception as e:
                console.print(f"[bold red]Connection_Spam Exception Error:[bold yellow] {e}")
                await client.disconnect(); await asyncio.sleep(0.1)
    


    @classmethod
    def main(cls, target: str):
        """This method will control class logic"""


        print("")
        asyncio.run(BLE_Connection_Spam._connection_spam(target=target))

                




if __name__ == "__main__":
    target = BLE_Sniffer.main()
    BLE_Enumerater.main(target=target)