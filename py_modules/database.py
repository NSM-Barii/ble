# THIS MODULE WILL HOLD UTILITIES FOR ETC



# UI IMPORTS
from rich.console import Console
console = Console()


# IMPORTS
import manuf, json
from pathlib import Path
from mac_vendor_lookup import MacLookup #vendors = MacLookup().load_vendors()



class DataBase():
    """This will be a database for service uuids"""


    database = Path(__file__).parent.parent / "database" / "bluetooth_sig" / "assigned_numbers" / "company_identifiers"
    company_ids_path = database / "company_ids.json"



    @staticmethod
    def _importer(file_path: str, type="json", verbose=True) -> any:
        """This method will be responsble for returning all file paths"""

        
        if type == "json":
            with open(file_path, "r") as file:
                
                data = json.load(file)

                if verbose: console.print(f"[bold green][+] Successfully pulled: {file_path}")

                return data 
        
       

    @staticmethod
    def _services():
        """This will house the database for service uuids"""

        
        services = [
            {
                "name": "Tuya",
                "uuid": "fd50",
                "notes": "Used in cheap BLE smart locks, plugs, bulbs, and scales sold under dozens of brands.",
                "likelihood": "Very High"
            },
            {
                "name": "Xiaomi",
                "uuid": "fd21",
                "notes": "Used in BLE sensors and fitness trackers. Common in Mijia/Mi Band devices.",
                "likelihood": "High"
            },
            {
                "name": "Xiaomi (MiBeacon)",
                "uuid": "fe95",
                "notes": "BLE advertisement extension. Seen in multiple Xiaomi ecosystem devices.",
                "likelihood": "High"
            },
            {
                "name": "Fitbit",
                "uuid": "fd6f",
                "notes": "Used in fitness trackers for sync and telemetry.",
                "likelihood": "Medium"
            },
            {
                "name": "Tile",
                "uuid": "fe9f",
                "notes": "Custom protocol for encrypted BLE location beacons.",
                "likelihood": "Medium"
            },
            {
                "name": "Oura Ring",
                "uuid": "fd88",
                "notes": "Used for health data sync over BLE from biometric rings.",
                "likelihood": "Medium"
            },
            {
                "name": "Amazon Echo Buds",
                "uuid": "fdcf",
                "notes": "Custom telemetry + control services for earbuds.",
                "likelihood": "Low"
            },
            {
                "name": "Garmin",
                "uuid": "fd19",
                "notes": "Used in fitness watches and sensors with proprietary ANT+/BLE profiles.",
                "likelihood": "Medium"
            },
            {
                "name": "Apple (Find My)",
                "uuid": "fdc0",
                "notes": "Used in AirTags and Find My-enabled BLE devices.",
                "likelihood": "Low"
            },
            {
                "name": "Samsung",
                "uuid": "fee0",
                "notes": "Health device sync and BLE watch pairing.",
                "likelihood": "Medium"
            },
            {
                "name": "Nordic Semiconductor",
                "uuid": "fd3d",
                "notes": "Often shows up in DIY firmware. Some devices use it for OTA or control.",
                "likelihood": "High"
            },
            {
                "name": "Withings",
                "uuid": "fdc1",
                "notes": "Used in smart scales, BP monitors, and watches.",
                "likelihood": "Medium"
            },
            {
                "name": "Anker Soundcore",
                "uuid": "fd12",
                "notes": "Controls BLE headphone settings, EQ, and firmware.",
                "likelihood": "Medium"
            },
            {
                "name": "Google (Fast Pair)",
                "uuid": "fdaf",
                "notes": "Used in Android Fast Pair BLE handshake.",
                "likelihood": "Low"
            }
        ]
        
   
    @classmethod
    def _get_service_uuids(cls, uuid: any) -> str:
        """this will take given services and parse them through known database"""


        pass


    @classmethod
    def _get_manufacturers(cls, manufacturer_hex, verbose=True) -> str:
        """Manufacturer ID --> Manufacturer / Vendor"""

        id = 0

        if not manufacturer_hex: return "N/A"
        #elif isinstance(id, int): id = manufacturer_hex


        if not id:
            data = {}
            for key, value in manufacturer_hex.items():
                id = key
                data[key] = value.hex()
            

        company_ids = DataBase._importer(file_path=cls.company_ids_path, verbose=False)


        for key, value in company_ids.items():

            if int(key) == int(id):

                manufacturer = value["company"]

                if verbose: console.print(f"[bold green][+] {id} --> {manufacturer}")
                
                return manufacturer
        
        return False



        pass


    @classmethod
    def _get_vendor(cls, mac: str, verbose=True) -> str:
        """MAC --> Vendor | lookup"""
        
        try:

            manuf_path = str(Path(__file__).parent / "old_manuf.txt")

            vendor = manuf.MacParser(manuf_path).get_manuf_long(mac=mac)
            
            if verbose:
                console.print(f"Manuf.txt pulled -> {manuf_path}")            
                console.print(f"[bold green][+] Vendor Lookup:[/bold green] {vendor} -> {mac}")
            

            return vendor
                
        

        except FileNotFoundError:
            console.print(f"[bold red][-] Failed to pull manuf.txt:[bold yellow] File not Found!"); exit()
      
        
        except Exception as e:
            console.print(f"[bold red][-]Exception Error:[bold yellow] {e}"); exit()
    

    @staticmethod
    def _get_vendor_new(mac: str, verbose=True) -> str:
        """MAC Prefixes --> Vendor"""
        

        try:

            manuf_path = str(Path(__file__).parent / "manuf.txt")

            mac_prefix = mac.split(':'); prefix = mac_prefix[0] + mac_prefix[1] + mac_prefix[2]


            with open(manuf_path, "r") as file:

                #if  verbose: console.print(f"[bold green][+] Successfully pulled: {manuf_path}")


                for line in file:
                    parts = line.strip().split('\t')
                    
                    if parts[0] == prefix:

                        vendor = parts[1]

                        if verbose: console.print(f"[bold green][+] {parts[0]} --> {vendor}" )
                        return vendor


        except FileNotFoundError:
            console.print(f"[bold red][-] Failed to pull manuf.txt:[bold yellow] File not Found!"); exit()
      

        except Exception as e:
            console.print(f"[bold red][-] Exception Error:[bold yellow] {e}")
    
     




if __name__ == "__main__":
    DataBase._new_get_vendor(mac="")
  #  DataBase._get_manufacturers(manufacturer_hex=2000, verbose=True)