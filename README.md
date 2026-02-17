# NSM-Barii

**IoT Exploitation Framework**

A comprehensive toolkit for security testing and vulnerability research on IoT devices through BLE, WiFi, and UART attack surfaces.

> ⚠️ **This project is actively in development.** New features and modules are being added regularly. Expect frequent updates and improvements.

---

## Features

- **BLE Exploitation**
  - Wardriving with automatic data logging
  - Device enumeration and GATT service dumping
  - Connection spam attacks
  - Fuzzing with customizable payloads

- **WiFi Analysis**
  - Wireless reconnaissance
  - Packet analysis

- **Hardware Protocols**
  - UART interface testing

- **Mobile Security**
  - Rooted Android integration (Magisk)
  - Frida runtime instrumentation

---

## Installation

### Quick Setup

```bash
# Clone the repository
git clone <repo-url>
cd ble/py_modules

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install BlueZ driver (Linux/macOS)
# On Ubuntu/Debian:
sudo apt-get install bluez libbluetooth-dev

# On macOS:
brew install bluez

# Install Python dependencies
pip install -r requirements.txt
```

### Running the Framework

```bash
# Must run with sudo for BLE access
sudo venv/bin/python3 main.py
```

---

## Usage

Run the framework without arguments to see the help menu:

```bash
sudo venv/bin/python3 main.py
```

### Common Commands

**BLE Scanning:**
```bash
sudo venv/bin/python3 main.py -s              # Basic BLE scan
sudo venv/bin/python3 main.py -sv             # Scan with vendor lookup
sudo venv/bin/python3 main.py -t 20           # Set scan timeout (seconds)
```

**BLE Wardriving:**
```bash
sudo venv/bin/python3 main.py -w              # Wardriving mode
sudo venv/bin/python3 main.py -wv             # Wardriving with verbose output
```

**BLE Exploitation:**
```bash
sudo venv/bin/python3 main.py -m <MAC> -d     # Dump GATT services
sudo venv/bin/python3 main.py -m <MAC> -c     # Connection spam
sudo venv/bin/python3 main.py -m <MAC> -cp    # Connection + pairing spam
sudo venv/bin/python3 main.py -m <MAC> -f     # Fuzz all characteristics
```

**Advanced Fuzzing:**
```bash
sudo venv/bin/python3 main.py -m <MAC> -ft <UUID> --send write --response 1
```

**Telnet Bruteforce:**
```bash
sudo venv/bin/python3 main.py --telnet
```

---

## Project Structure

```
ble/
├── py_modules/
│   ├── main.py              # Main entry point
│   ├── nsm_ble.py           # BLE modules
│   └── nsm_telnet.py        # Telnet bruteforce
├── root_pixel7a/            # Android rooting guides
└── README.md
```

---

## Requirements

- Python 3.x
- Bluetooth adapter (for BLE testing)
- Root access on Android device (for mobile features)

---

## Disclaimer

This tool is intended for **authorized security research and testing only**. Unauthorized access to devices or networks is illegal. The author is not responsible for misuse of this framework.

---

## Author

**NSM-Barii**

---

## License

[Specify your license here]
