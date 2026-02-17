# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# UI IMPORTS
from rich.console import Console
from rich.panel import Panel
import pyfiglet
console = Console()


# ETC IMPORTS
import argparse, sys


# NSM MODULES
from nsm_ble import BLE_Enumerater, BLE_Sniffer, BLE_Fuzzer, BLE_Connection_Spam
from nsm_telnet import Telnet_Brute_Forcer




class Main_Menu():
    """This class will gatekeep program wide logic"""


    data = (
        "\n       [bold cyan]IoT Exploitation Framework[/bold cyan]"
        "\n\n            [bold yellow]BLE • WiFi • UART[/bold yellow]"
        "\n\n              [bold magenta]Made by NSM-Barii[/bold magenta]\n"
    )

    panel = Panel(renderable=data, expand=False, style="bold red")


    # I wil be calling this project/Framework NodeX


    parser = argparse.ArgumentParser(
        description="IOT Framework for Wireless Recon, Fuzzing & Hacking"
    )


   # parser.add_argument("-h", help="Display help, usage info, and project banner")
    parser.add_argument("-w", action="store_true", help="BLE wardriving with automatic data logging")
    parser.add_argument("-wv", action="store_true", help="BLE wardriving with verbose output")

    parser.add_argument("-s", action="store_true", help="Perform local BLE scan")
    parser.add_argument("-sv", action="store_true", help="BLE scan with vendor lookup")

    parser.add_argument("-t", default=10, help="Scan timeout in seconds (default: 10)")
    parser.add_argument("-m", help="Target MAC address")

    parser.add_argument("-d", action="store_true", help="Dump GATT services from target")

    parser.add_argument("-c", action="store_true", help="Connection spam attack")
    parser.add_argument("-cp", action="store_true", help="Connection + pairing spam attack")

    parser.add_argument("-f", action="store_true", help="Fuzz all characteristics on target")
    parser.add_argument("-ft", help="Fuzz specific characteristic UUID")
    parser.add_argument("--type", help="Fuzzing type")
    parser.add_argument("--send", help="Write properties: write, write-without-response, read, notify, all")
    parser.add_argument("--response", help="Write-response flag: 0 or 1")

    parser.add_argument("--telnet", action="store_true", help="Telnet dictionary attack with preset credentials")


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
        console.print(panel)
        parser.print_help(); exit()

    
    if scan or vendor or war: 
        BLE_Sniffer.main(scan=True if vendor else scan, timeout=int(time), vendor_lookup=vendor); exit()


    if not mac and not telnet: console.print(f"[bold red]use -m to pass a MAC Addr silly goose..."); exit()

    elif fuzz or fuzz_u: BLE_Fuzzer.main(target=mac, uuid=fuzz if fuzz else fuzz_u, send=send, response=response, f_type=int(f_type))
    
    elif conn or pair: BLE_Connection_Spam.main(target=mac, pair=pair)
    
    elif dump: BLE_Enumerater.main(target=mac)

    elif telnet: Telnet_Brute_Forcer.main()

        
        


        






