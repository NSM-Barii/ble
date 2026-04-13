# TESTING OUT CONTROL FOR LAN TUYA DEVICES



# ETC IMPORTS
import requests
import tinytuya
import tinytuya.Cloud




class Find_Tuya_Devices():
    """This will be responsible for finding wifi based Tuya devices"""


    @classmethod
    def _find_devices(cls):
        """This will poll/scan for tuya devices"""


        devices = tinytuya.deviceScan(maxretry=2, poll=True, forcescan=False)


        for ip in devices:

            id = devices[ip]['gwId']
            key = devices[ip]['productKey']
            vers = devices[ip]['version']
            #dps = devices[ip]['dps']


            data = (ip, id, key, vers)
            print(
                f"==================="
                f"\nIP: {ip}"
                f"\nDevice ID: {id}"
                f"\nProduct Key: {key}"
                f"\nVersion: {vers}"
                f"\n==================="
            )

            cls.devices.append(data)
        

    
    @classmethod
    def main(cls):
        """This will control this class"""

        cls.devices = []


        Find_Tuya_Devices._find_devices()

        print(cls.devices)


if __name__ == "__main__":
    Find_Tuya_Devices.main()