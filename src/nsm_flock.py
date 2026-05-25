# THIS MODULE WILL HOUSE FLOCK CAMERA SPOOFING


# UI IMPORTS
from rich.panel import Panel


# NETWORK IMPORTS
from scapy.all import RadioTap, sendp
from scapy.layers.dot11 import Dot11, Dot11ProbeReq, Dot11Elt


# ETC IMPORTS
import time, random


# NSM IMPORTS
from nsm_vars import Variables


# CONSTANTS
console = Variables.console


# FLOCK SIGNATURES
MAC_PREFIXES = [
    "58:8e:81", "cc:cc:cc", "ec:1b:bd", "90:35:ea", "04:0d:84",
    "f0:82:c0", "1c:34:f1", "38:5b:44", "94:34:69", "b4:e3:f9",
    "70:c9:4e", "3c:91:80", "d8:f3:bc", "80:30:49", "14:5a:fc",
    "74:4c:a1", "08:3a:88", "9c:2f:9d", "94:08:53", "e4:aa:ea"
]

SSIDS = [
    "flock",
    "Flock",
    "FLOCK",
    "FS Ext Battery",
    "Penguin",
    "Pigvision"
]




class Flock_Spoofer():
    """This class will spoof Flock camera probe requests"""


    @classmethod
    def _get_mac(cls):
        """Build a full MAC from a random Flock prefix"""

        prefix = random.choice(MAC_PREFIXES)
        suffix = ":".join("%02x" % random.randint(0, 255) for _ in range(3))
        return f"{prefix}:{suffix}"


    @classmethod
    def _get_ssid(cls):
        """Pick a random Flock SSID"""

        return random.choice(SSIDS)


    @classmethod
    def _build_frame(cls, mac, ssid):
        """Build a probe request frame spoofing a Flock camera"""

        return (
            RadioTap() /
            Dot11(type=0, subtype=4,
                  addr1="ff:ff:ff:ff:ff:ff",
                  addr2=mac,
                  addr3="ff:ff:ff:ff:ff:ff") /
            Dot11ProbeReq() /
            Dot11Elt(ID="SSID", info=ssid.encode())
        )


    @classmethod
    def _spoof(cls, iface, count, inter):
        """Send spoofed Flock probe requests"""

        c1 = "bold green"
        c2 = "bold red"
        c3 = "bold yellow"
        c4 = "bold purple"

        sent = 0

        try:

            while True:

                mac  = cls._get_mac()
                ssid = cls._get_ssid()
                frame = cls._build_frame(mac=mac, ssid=ssid)

                sendp(frame, iface=iface, count=count, inter=inter, verbose=False)

                sent += count

                console.print(
                    f"[{c1}][[/{c1}][{c2}]FLOCK SPOOF[/{c2}][{c1}]][/{c1}]"
                    f"  [{c3}]mac:[/{c3}] [{c4}]{mac}[/{c4}]"
                    f"  [{c3}]ssid:[/{c3}] [{c4}]{ssid}[/{c4}]"
                    f"  [{c3}]sent:[/{c3}] [{c2}]{sent}[/{c2}]"
                )

                time.sleep(inter)

        except KeyboardInterrupt: console.print(f"\n[bold red][-] Flock_Spoofer stopped — {sent} frames sent")
        except Exception as e:    console.print(f"[bold red]Exception Error:[bold yellow] {e}")


    @classmethod
    def main(cls):
        """Run from here"""

        if not Variables.flock_spoof: return

        console.print(Panel("Flock Spoofer", style="bold red", border_style="bold purple"))

        iface = Variables.iface
        count = Variables.count
        inter = Variables.timeout or 0.1

        console.print(f"[bold green][+] Spoofing Flock cameras on [bold yellow]{iface}  [bold green]delay:[bold yellow] {inter}s")

        cls._spoof(iface=iface, count=count, inter=inter)
