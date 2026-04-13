# THIS WILL HOUSE MULTI-MODULE VARS 


# IMPORTS
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import threading




class Variables():
    """This will house multi module vars"""

    
    # CONSTANTS
    console = Console()
    LOCK = threading.RLock()


    # RICH VARS
    console = Console()
    panel = Panel(renderable="Developed by NSM Barii", style="bold yellow", border_style="bold red", expand=False)
    table = Table(title="Developed by NSM Barii", style="bold purple", border_style="bold red", title_style="bold purple", header_style="bold purple")
    refresh_per_second = 1


    # ===============
    #  METHOD TO USE
    # ===============
    
    # BLE
    ble_wardrive        = False
    ble_sniffer         = False
    ble_enumeration     = False
    ble_fuzzer          = False
    ble_connection_spam = False

    # WiFi
    wifi_ssid_sniffer   = False
    wifi_client_sniffer = False
    wifi_deauth_attack  = False
    wifi_beacon_flood   = False
    wifi_evil_twin      = False
    wifi_war_driving    = False

    
    # ==============
    #  BLE METHODS
    # ==============

    # WAR DRIVING
    war    = False

    # SCANNING
    scan   = False
    time   = False 
    vendor = False
    mac    = False
    
    # DUMP GATT
    dump   = False
    
    # FUZZ FEATURES
    fuzz     = False
    fuzz_u   = False
    send     = "write"
    response = False
    f_type   = 1

    # CONNECTION SPAM
    conn     = False
    pair     = False
    



    # TELNET
    telnet   = False

    # ===============
    #  WiFi METHODS
    # ===============
    
    iface     = "wlan1"  # FOR MONITOR MODE
    subnet    = "192.168.1.0/24"
    ip_router = "192.168.1.1"
    ip_local  = None
    verbose   = False

    # =====================
    # MONITOR MODE ATTACKS
    # =====================


    # DEFAULT
    timeout = 15
    channel = 6 # OR 6

    # WAR DRIVING
    mode = 1 # AP's ONLY == 1 else 2 == FOR CLIENTS AND NON BEACON FRAMES

    # EVIL TWIN // BEACON FLOOOOD
    portal_num = 1    

    # DEAUTH // CLIENT SNIFFER
    mac_src    = None
    mac_dst    = None
    mac_client = None  # SINGLE CLIENT DEAUTH

    inter    = None
    loop     = None
    count    = None
    realtime = None

    reasons = [4,5,7,15]

