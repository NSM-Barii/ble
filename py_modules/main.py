# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# ETC IMPORTS
import argparse


# NSM MODULES
from ble import BLE_Enumerater, BLE_Sniffer



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
    parser.add_argument("-f", action="store_true", help="Fuzz a target MAC Addr with random bytes of data")


    args = parser.parse_args()

   # help = args.h 
    scan = args.s 
    time = args.t 
    mac = args.m 
    dump = args.d
    fuzz = args.f 




    if scan:
        BLE_Sniffer.main(timeout=int(time))
    

    elif dump:
        BLE_Enumerater.main(target=mac)
    







