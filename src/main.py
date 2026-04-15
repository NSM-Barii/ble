# THIS MODULE WILL BE THE MAIN PILLAR IN THE BLE HACKING FRAMEWORK



# UI IMPORTS
from rich.panel import Panel
import pyfiglet


# ETC IMPORTS
import argparse, sys


# NSM MODULES
from nsm_vars import Variables
from nsm_ble import BLE_Enumerater, BLE_Sniffer, BLE_Fuzzer, BLE_Connection_Spam
from nsm_wifi import SSID_Sniffer, Client_Sniffer, Deauth_Attacker, Evil_Twin, Beacon_Flooder, War_Driving
from nsm_telnet import Telnet_Brute_Forcer
from nsm_database import DataBase

# CONSTANTS
console = Variables.console




class Main_Menu():
    """This class will gatekeep program wide logic"""


    @staticmethod
    def main():
        """Main entry point"""

        data = (
            "\n       [bold cyan]IoT Exploitation Framework[/bold cyan]"
            "\n\n            [bold yellow]BLE • WiFi • UART[/bold yellow]"
            "\n\n              [bold magenta]Made by NSM-Barii[/bold magenta]\n"
        )

        panel = Panel(renderable=data, expand=False, style="bold red")


        parser = argparse.ArgumentParser(
            description="IOT Framework for Wireless Recon, Fuzzing & Hacking",
            add_help=False
        )

        parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")


        # ============
        #     BLE
        # ============
        parser.add_argument("-bw", action="store_true", help="BLE wardriving with automatic data logging")
        parser.add_argument("-bwv", action="store_true", help="BLE wardriving with verbose output")

        parser.add_argument("-bs", action="store_true", help="BLE scan")
        parser.add_argument("-bsv", action="store_true", help="BLE scan with vendor lookup")

        parser.add_argument("-bd", action="store_true", help="BLE dump GATT services from target (-m required)")

        parser.add_argument("-bc", action="store_true", help="BLE connection spam attack (-m required)")
        parser.add_argument("-bcp", action="store_true", help="BLE connection + pairing spam attack (-m required)")

        parser.add_argument("-bf", action="store_true", help="BLE fuzz all characteristics (-m required)")
        parser.add_argument("-bft", help="BLE fuzz specific characteristic UUID (-m required)")
        parser.add_argument("--send", help="Write properties: write, read, notify, all (default: write)")
        parser.add_argument("--response", help="Write-response flag: 0 or 1")
        parser.add_argument("--type", help="Fuzzing type (default: 1)")


        # ============
        #    WiFi
        # ============
        parser.add_argument("-ws", action="store_true", help="WiFi SSID scan")
        parser.add_argument("-wc", help="WiFi client scan from specific SSID (provide BSSID/MAC)")
        parser.add_argument("-wd", help="WiFi deauth attack on SSID (provide BSSID/MAC)")
        parser.add_argument("-wb", help="WiFi beacon flood (provide portal choice 1-3)")
        parser.add_argument("-we", help="WiFi evil twin attack (provide portal number 1-20)")
        parser.add_argument("-ww", action="store_true", help="WiFi wardriving mode")

        parser.add_argument("-mm", help="Change iface to monitor mode")

        parser.add_argument("--channel", type=int, help="WiFi channel (default: 6)")
        parser.add_argument("--hop-delay", type=float, help="delay between hopping channels")
        parser.add_argument("--mode", type=int, help="Wardrive mode: 1=APs only, 2=clients+non-beacon (default: 1)")
        parser.add_argument("--dst", help="Deauth destination MAC (default: ff:ff:ff:ff:ff:ff)")
        parser.add_argument("--inter", type=float, help="Packet send interval")
        parser.add_argument("--loop", type=int, help="Packet send loop count")
        parser.add_argument("--count", type=int, help="Number of packets to send")
        parser.add_argument("--realtime", action="store_true", help="Enable realtime packet sending")
        parser.add_argument("--reasons", help="Deauth reason codes (comma-separated, default: 4,5,7,15)")


        # ==========================
        #   GENERIC // ALL MODULES
        # ==========================
        parser.add_argument("-t", type=int, default=10, help="Scan timeout in seconds (default: 10)")
        parser.add_argument("-m", help="Target MAC address")
        parser.add_argument("-i", "--iface", help="Network interface (default: wlan1)")
        


        # ===============
        #  OTHERS // LOL
        # ===============
        parser.add_argument("--telnet", action="store_true", help="Telnet dictionary attack")

        args = parser.parse_args()


        if args.help or len(sys.argv) == 1:
            console.print(panel)
            parser.print_help()
            exit()


        # GENERIC CONFIG
        Variables.timeout   = args.t
        Variables.mac       = args.m
        Variables.iface     = args.iface or "wlan1"
        Variables.channel   = args.channel or 6
        Variables.hop_delay = args.hop_delay
        Variables.mode      = args.mode or 1
        Variables.mac_dst   = args.dst or "ff:ff:ff:ff:ff:ff"
        Variables.inter     = args.inter
        Variables.loop      = args.loop
        Variables.count     = args.count
        Variables.realtime  = args.realtime

        if args.reasons:  Variables.reasons = [int(r.strip()) for r in args.reasons.split(',')]
        else:             Variables.reasons = [4, 5, 7, 15]


        # ============
        #  BLE FLAGS
        # ============
        if args.bw or args.bwv:
            Variables.ble_wardrive  = True
            Variables.war           = args.bw
            Variables.vendor        = args.bwv

        if args.bs or args.bsv:
            Variables.ble_sniffer = True
            Variables.scan        = args.bs
            Variables.vendor      = args.bsv

        if args.bd:
            Variables.ble_enumeration = True

        if args.bf or args.bft:
            Variables.ble_fuzzer  = True
            Variables.fuzz        = args.bf
            Variables.fuzz_u      = args.bft or False
            Variables.send        = args.send or "write"
            Variables.response    = args.response or False
            Variables.f_type      = args.type or 1

        if args.bc or args.bcp:
            Variables.ble_connection_spam = True
            Variables.conn                = args.bc
            Variables.pair                = args.bcp or False


        # ============
        #  WiFi FLAGS
        # ============
        if args.ws:
            Variables.wifi_ssid_sniffer   = True

        if args.wc:
            Variables.wifi_client_sniffer = True
            Variables.mac_client          = args.wc

        if args.wd:
            Variables.wifi_deauth_attack  = True
            Variables.mac_src             = args.wd

        if args.wb:
            Variables.wifi_beacon_flood   = True
            Variables.portal_num          = args.wb

        if args.we:
            Variables.wifi_evil_twin      = True
            Variables.portal_num          = args.we

        if args.ww:
            Variables.wifi_war_driving    = True


        # ============
        # OTHER FLAGS
        # ============
        if args.telnet: Variables.telnet = True
        
        if args.mm: DataBase.WiFi.monitor_mode(iface=args.mm)

        BLE_Sniffer.main();  BLE_Enumerater.main(); BLE_Fuzzer.main(); BLE_Connection_Spam.main()
        SSID_Sniffer.main(); Client_Sniffer.main(); Deauth_Attacker.main(); Beacon_Flooder.main(); Evil_Twin.main(); War_Driving.main()

        Telnet_Brute_Forcer.main()



if __name__ == "__main__": Main_Menu.main()
