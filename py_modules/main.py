# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# UI IMPORTS
from rich.console import Console
console = Console()


# ETC IMPORTS
import argparse


# NSM MODULES
from ble import BLE_Enumerater, BLE_Sniffer, BLE_Fuzzer
from utilities import Utilities



class Main_Menu():
    """This class will gatekeep program wide logic"""


    parser = argparse.ArgumentParser(
        description="BLE Framework for Wireless Recon, Fuzzing & Hacking"
    )


   # parser.add_argument("-h", help="Display help, usage info, and project banner")
    parser.add_argument("-s", action="store_true", help="Perform a local ble scan")
    parser.add_argument("-t", default=10, help="Set timeout for how long ble scan may persist")
    parser.add_argument("-m", help="Set mac address for targeted control")
    parser.add_argument("-d", action="store_true", help="Connect to MAC Addr, enumerate and dump gatt services.")
    parser.add_argument("-f" , help="Fuzz a target MAC Addr with random bytes of data")
    parser.add_argument("-v", action="store_true", help="Lookup info on MAC Addr, such as vendor")
    parser.add_argument("--type", help="The type of fuzzing you want to be done")


    args = parser.parse_args()

   # help = args.h 
    scan = args.s 
    time = args.t 
    mac = args.m.strip() 
    dump = args.d
    fuzz = args.f
    vendor = args.v
    f_type = args.type or 1




    if scan:
        BLE_Sniffer.main(timeout=int(time))
    
    
    elif dump or fuzz or vendor:

        if not mac: console.print(f"[bold red]use -m to pass a MAC Addr silly goose..."); exit()

        elif vendor: Utilities.get_vendor(mac=mac)

        elif dump: BLE_Enumerater.main(target=mac)
        
        elif fuzz:BLE_Fuzzer.main(target=mac, uuid=fuzz.strip() , f_type=int(f_type))
        


        







