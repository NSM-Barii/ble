# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# UI IMPORTS
from rich.console import Console
console = Console()


# ETC IMPORTS
import argparse, sys


# NSM MODULES
from nsm_ble import BLE_Enumerater, BLE_Sniffer, BLE_Fuzzer, BLE_Connection_Spam
from nsm_telnet import Telnet_Brute_Forcer




class Main_Menu():
    """This class will gatekeep program wide logic"""



    banner = """
[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]

           [bold white]IoT & Wireless Security Framework[/bold white]
        [bold yellow]BLE • WiFi • Fuzzing • Recon • CVE Research[/bold yellow]

              [bold magenta]Offensive Security & Vuln Hunting[/bold magenta]
                    [bold white]Made by NSM-Barii[/bold white]

[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]
"""
    
    

    # I wil be calling this project/Framework NodeX


    parser = argparse.ArgumentParser(
        description="IOT Framework for Wireless Recon, Fuzzing & Hacking"
    )


   # parser.add_argument("-h", help="Display help, usage info, and project banner")
    parser.add_argument("-w", action="store_true", help="BLE Wardriving along with automatic data saving")
    parser.add_argument("-wv", action="store_true", help="BLE Wardriivng with command output")


    parser.add_argument("-s", action="store_true", help="Perform a local ble scan")
    parser.add_argument("-sv", action="store_true", help="Lookup info on MAC Addr, such as vendor")

    parser.add_argument("-t", default=10, help="Set timeout for how long ble scan may persist")
    parser.add_argument("-m", help="Set mac address for targeted control")

    parser.add_argument("-d", action="store_true", help="Connect to MAC Addr, enumerate and dump gatt services.")

    parser.add_argument("-c", action="store_true", help="Perform a connection spam on targe MAC Addr")
    parser.add_argument("-cp", action="store_true", help="Perform a connection/Pairing spam on targe MAC Addr")

    parser.add_argument("-f",action="store_true", help="Fuzz a target MAC Addr and all its characteristics automatically with random bits of data")
    parser.add_argument("-ft", help="Fuzz a target MAC Addr and the inputted characteristic with random bytes of data")
    parser.add_argument("--type", help="The type of fuzzing you want to be done")
    parser.add_argument("--send", help="Properties to write to: write, write-without-response, read, notify, all")
    parser.add_argument("--response", help="Set write-response from client to True or False - 0 or 1")


    parser.add_argument("--telnet", action="store_true", help="This will start a common dictionary attack on a given IP with a open telnet service using a preset list of credentials")


    args = parser.parse_args()
    

    # WAR DRIVING
    war   = args.w

    # SCANNING
    scan = args.s 
    time = args.t 
    vendor = args.sv
    mac = args.m
    
    # DUMP GATT
    dump = args.d 
    
    # FUZZ FEATURES
    fuzz     = args.f 
    fuzz_u   = args.ft       or False
    send     = args.send     or "write"
    response = args.response or False
    f_type   = args.type     or 1

    # CONNECTION SPAM
    conn     = args.c
    pair     = args.cp or False

    # TELNET
    telnet   = args.telnet


    if len(sys.argv) == 1:
        console.print(banner)
        parser.print_help(); exit()

    
    if scan or vendor or war: 
        BLE_Sniffer.main(scan=True if vendor else scan, timeout=int(time), vendor_lookup=vendor); exit()


    if not mac and not telnet: console.print(f"[bold red]use -m to pass a MAC Addr silly goose..."); exit()

    elif fuzz or fuzz_u: BLE_Fuzzer.main(target=mac, uuid=fuzz if fuzz else fuzz_u, send=send, response=response, f_type=int(f_type))
    
    elif conn or pair: BLE_Connection_Spam.main(target=mac, pair=pair)
    
    elif dump: BLE_Enumerater.main(target=mac)

    elif telnet: Telnet_Brute_Forcer.main()

        
        


        






