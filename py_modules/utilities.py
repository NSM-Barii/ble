# THIS MODULE WILL HOLD UTILITIES FOR ETC



# UI IMPORTS
from rich.console import Console
console = Console()


# IMPORTS
import manuf
from pathlib import Path
from mac_vendor_lookup import MacLookup
vendors = MacLookup().load_vendors()




class Utilities():
    """Responsible for etc tasks"""



    @classmethod
    def get_vendor(cls, mac: str) -> str:
        """MAC --> Vendor | lookup"""
        
        try:

            manuf_path = str(Path(__file__).parent / "manuf.txt")

            vendor = manuf.MacParser(manuf_path).get_manuf_long(mac=mac)

            console.print(f"Manuf.txt pulled -> {manuf_path}")            
            console.print(f"[bold green][+] Vendor Lookup:[/bold green] {vendor} -> {mac}"); return vendor
            
        

        except FileNotFoundError:
            console.print(f"[bold red][-] Failed to pull manuf.txt:[bold yellow] File not Found!"); exit()
      
        
        except Exception as e:
            console.print(f"[bold red][-]Exception Error:[bold yellow] {e}"); exit()