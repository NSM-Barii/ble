# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# UI IMPORTS
from rich.console import Console
console = Console()


# ETC IMPORTS
import argparse


# NSM MODULES
from ble import BLE_Enumerater, BLE_Sniffer, BLE_Fuzzer, BLE_Connection_Spam
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
    parser.add_argument("-f" , action="store_true", help="Fuzz a target MAC Addr with random bytes of data")
    parser.add_argument("-c", action="store_true", help="Perform a connection spam on targe MAC Addr")
    parser.add_argument("-sv", action="store_true", help="Lookup info on MAC Addr, such as vendor")
    parser.add_argument("--type", help="The type of fuzzing you want to be done")
    parser.add_argument("--send", help="Properties to write to: write, write-without-response, read, notify, all")
    parser.add_argument("--response", help="Set write-response from client to True or False - 0 or 1")


    args = parser.parse_args()

   # help = args.h 
    scan = args.s 
    time = args.t 
    vendor = args.sv
    mac = args.m
    
    # DUMP GATT
    dump = args.d
    
    # FUZZ FEATURES
    fuzz     = args.f
    send     = args.send     or "write"
    response = args.response or False
    f_type   = args.type     or 1


    # CONNECTION SPAM
    conn     = args.c




    if scan or vendor:
        BLE_Sniffer.main(timeout=int(time), vendor_lookup=vendor)
    

    elif fuzz:

        if send  not in ["notify", "read", "write", "all"]: console.print("--send inputs not valid, try: write, read, notify, all")
        #if response.strip().lower() not in ["true"]: console.print("--response inputs not valid, try: True or False")
        
        
        BLE_Fuzzer.main(target=mac, uuid=fuzz, send=send, response=response, f_type=int(f_type))
    

    elif conn:

        BLE_Connection_Spam.main(target=mac)


    
    elif dump:

        if not mac: console.print(f"[bold red]use -m to pass a MAC Addr silly goose..."); exit()

        mac = mac.strip()

        if dump: BLE_Enumerater.main(target=mac)
        
        


        






