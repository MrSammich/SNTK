import socket
import json
import threading
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

#Colors!

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"   # this turns it off for next text
BRIGHT_RED    = "\033[91m"
BRIGHT_GREEN  = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE   = "\033[94m"
BRIGHT_CYAN   = "\033[96m"
BOLD      = "\033[1m"
UNDERLINE = "\033[4m"


open_ports = 0
lock = threading.Lock()

inventory_file = "inventory.json"
inventory = {} 


def scan_port(host, port: int) -> bool:     #tbh i barely know this function, stackoverflow is a macigal place
    global open_ports 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            banner = ""

            if result == 0:

                try:
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except socket.timeout:
                    pass

                if not banner:
                    try:
                        s.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                        banner = s.recv(1024).decode(errors="ignore").strip()
                        banner_split = banner.split("\r\n")
                        
                        for line in banner_split:
                            if line.startswith("Server:"):
                                banner = line
                                break
                            
                    except socket.timeout:
                        pass

                print(f'{BRIGHT_YELLOW}[!] Port {port} is open with banner {banner if banner else "Unknown"}{RESET}')
                
                with lock:
                    open_ports += 1
                return (str(port),banner if banner else "Unknown")

            return None

    except Exception as e: 
        print(e)
    
        

def run_port_scanner(host=None, start_port=1, end_port=1025):
    try:
        user_host = host if host else input("[?] Enter the ip address you want to scan\n\t > ")

        if host is None:                #turns out we can do this macigal stuff so if ip is already given it wont ask for the port
            user_port = input("[?] Please enter a port number to scan (Default/eg: 1, 1025):\n\t\t > ").strip()

            if user_port:
                try:
                    start_port, end_port = (int(p.strip()) for p in user_port.split(","))
                
                except ValueError:
                    print(f"{RED}[!]Invalid port range, falling back to default range of 1, 1025{RESET}")
                    start_port, end_port = 1, 1025

            else:
                start_port, end_port = 1, 1025
        


        found_ports = []
        

        try:
            with ThreadPoolExecutor(max_workers=200) as exec:
                futures = [exec.submit(scan_port, user_host, port) for port in range(start_port, end_port + 1)]
                for future in futures:
                    result = future.result()
                    if result is not None:
                        found_ports.append(result)
        
        except ConnectionRefusedError:
            print("Connection refused. host is not reachable. Please check the host name and try again.")
        except TimeoutError:
            print("Timeout error occurred. Please check your connection and try again.")
        except BrokenPipeError:
            print("Broken pipe error occurred. Please check your connection and try again.")
        except OSError as e:
            print(f"An OS error occurred: {e}. Please check your connection and try again.")
        except Exception as e:
            print(f"Something went wrong: {e}.")
        
        if not found_ports:
            print("No open ports found in the specified range.")

        inventory_file = "inventory.json"
        inventory = {}

        if os.path.exists(inventory_file):
            try:
                with open(inventory_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        inventory = json.loads(content)
            except (json.JSONDecodeError, PermissionError):
                print(f"{BRIGHT_RED}[!] Warning: Could not read {inventory_file} cleanly. Starting fresh.{RESET}")
                inventory = {}

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user_host not in inventory:
            inventory[user_host] = {
                "status": "up",
                "last_seen": timestamp,
                "open_ports": {},
                "credentials": {},
            }

        for port, banner in found_ports:
            inventory[user_host]["open_ports"][port] = {"last_seen": timestamp, "banner": banner}

        with open(inventory_file, "w") as f:
            json.dump(inventory, f, indent=4)

        print(f"[!] Results saved to {inventory_file}")    

    except KeyboardInterrupt:
        os.system('clear')
        print(f"\n{BRIGHT_YELLOW}[!] Action interrupted by user. Exiting.{RESET}")
        return
    
if __name__ == "__main__":
    run_port_scanner()