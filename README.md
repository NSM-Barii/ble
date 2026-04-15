# IoT Exploitation Framework

A comprehensive toolkit for security testing and vulnerability research on IoT devices through BLE, WiFi, and UART attack surfaces.

> ⚠️ **This project is actively in development.** New features and modules are being added regularly. Expect frequent updates and improvements.

---

## Features

- **BLE Exploitation**
  - Wardriving with automatic data logging
  - Device enumeration and GATT service dumping
  - Connection spam attacks
  - Fuzzing with customizable payloads

- **WiFi Attacks**
  - SSID scanning and enumeration
  - Client discovery from specific SSIDs
  - Deauthentication attacks
  - Beacon flooding with fake APs
  - Evil twin / captive portal attacks
  - WiFi wardriving mode

- **Network Security**
  - Telnet bruteforce attacks

- **Hardware Protocols** *(Coming Soon)*
  - UART interface testing

---

## Installation

### Quick Setup

```bash
# Clone the repository
git clone github.com/NSM-Barii/framework
cd framework/py_modules

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Running the Framework

```bash
# Must run with sudo for BLE/WiFi access
sudo venv/bin/python3 main.py

# View help menu
sudo venv/bin/python3 main.py -h
```

---

## Dependencies

### BLE Modules

The BLE modules require BlueZ drivers for Bluetooth Low Energy support.

**Debian/Ubuntu:**
```bash
sudo apt-get install bluez bluez-tools libbluetooth-dev
```

**Arch Linux:**
```bash
sudo pacman -S bluez bluez-utils
```

### Evil Twin Attack

The Evil Twin module requires `hostapd` and `dnsmasq` for creating fake access points and captive portals.

**Debian/Ubuntu:**
```bash
sudo apt update && sudo apt install hostapd dnsmasq -y
```

**Arch Linux:**
```bash
sudo pacman -Syu && sudo pacman -S hostapd dnsmasq
```

---

## Usage

Run the framework without arguments to see the help menu:

```bash
sudo venv/bin/python3 main.py -h
```

### Command Structure

All commands use a **prefix system** to organize modules:
- **`-b*`** = BLE operations
- **`-w*`** = WiFi operations
- **Generic flags**: `-t`, `-m`, `-i`, `--channel`

---

### BLE Commands

**BLE Scanning:**
```bash
sudo venv/bin/python3 main.py -bs              # Basic BLE scan
sudo venv/bin/python3 main.py -bsv -t 20      # Scan with vendor lookup, 20s timeout
```

**BLE Wardriving:**
```bash
sudo venv/bin/python3 main.py -bw             # Wardriving mode
sudo venv/bin/python3 main.py -bwv            # Wardriving with verbose output
```

**BLE Exploitation:**
```bash
sudo venv/bin/python3 main.py -bd -m <MAC>    # Dump GATT services
sudo venv/bin/python3 main.py -bc -m <MAC>    # Connection spam
sudo venv/bin/python3 main.py -bcp -m <MAC>   # Connection + pairing spam
sudo venv/bin/python3 main.py -bf -m <MAC>    # Fuzz all characteristics
```

**Advanced BLE Fuzzing:**
```bash
sudo venv/bin/python3 main.py -bft <UUID> -m <MAC> --send write --response 1
```

---

### WiFi Commands

**WiFi Scanning:**
```bash
sudo venv/bin/python3 main.py -ws -i wlan0    # SSID scan on wlan0
sudo venv/bin/python3 main.py -ws --channel 11 # SSID scan on channel 11
```

**WiFi Client Discovery:**
```bash
sudo venv/bin/python3 main.py -wc <BSSID> -i wlan0  # Sniff clients from specific AP
```

**WiFi Deauth Attack:**
```bash
sudo venv/bin/python3 main.py -wd <BSSID> --channel 6  # Deauth all clients
sudo venv/bin/python3 main.py -wd <BSSID> --dst <CLIENT_MAC>  # Deauth specific client
sudo venv/bin/python3 main.py -wd <BSSID> --reasons 1,6,7  # Custom reason codes
```

**WiFi Beacon Flood:**
```bash
sudo venv/bin/python3 main.py -wb 1 --channel 6  # Beacon flood (portal choice 1-3)
```

**WiFi Evil Twin:**
```bash
sudo venv/bin/python3 main.py -we 5 --channel 6  # Evil twin (portal 1-20)
```

**WiFi Wardriving:**
```bash
sudo venv/bin/python3 main.py -ww -i wlan0      # Wardrive mode (APs only)
sudo venv/bin/python3 main.py -ww --mode 2      # Wardrive mode (clients + non-beacon)
```

---

### Other Commands

**Telnet Bruteforce:**
```bash
sudo venv/bin/python3 main.py --telnet
```

---

### Generic Options

```bash
-t <seconds>      # Scan timeout (default: 10)
-m <MAC>          # Target MAC address
-i, --iface       # Network interface (default: wlan1)
--channel <n>     # WiFi channel (default: 6)
--mode <1|2>      # Wardrive mode: 1=APs only, 2=clients+non-beacon
--dst <MAC>       # Deauth destination MAC (default: broadcast)
--inter <float>   # Packet send interval
--loop <n>        # Packet send loop count
--count <n>       # Number of packets to send
--realtime        # Enable realtime packet sending
--reasons <codes> # Deauth reason codes (comma-separated, default: 4,5,7,15)
```

---

## Project Structure

```
framework/
├── py_modules/
│   ├── main.py              # Main entry point
│   ├── nsm_vars.py          # Centralized configuration
│   ├── nsm_ble.py           # BLE exploitation modules
│   ├── nsm_wifi.py          # WiFi attack modules
│   ├── nsm_telnet.py        # Telnet bruteforce
│   ├── nsm_database.py      # Database operations
│   └── requirements.txt     # Python dependencies
└── README.md
```

---

## Requirements

### Hardware
- Linux (Ubuntu/Debian/Arch recommended)
- Bluetooth adapter (for BLE testing)
- WiFi adapter with monitor mode support (for WiFi attacks)

### Software
- Python 3.8+
- BlueZ drivers (for BLE - see Dependencies)
- hostapd & dnsmasq (for Evil Twin - see Dependencies)
- Root/sudo access (required for low-level network operations)

---

## Disclaimer

This tool is intended for **authorized security research and testing only**. Unauthorized access to devices or networks is illegal. The author is not responsible for misuse of this framework.

---

## Author

**NSM-Barii**

---

## License

[Specify your license here]
