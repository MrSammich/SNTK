import os
import time
import ipaddress
import subprocess
import json
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from portScanner import run_port_scanner

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

#this whole function just checks if the host is alive by pinging it.
#probably a better way exists but i am not aware of it. I am open to suggestions.

def is_host_alive(ip, delay=0):
    if delay > 0:                   #place holder thingy for the "stealth" option
        time.sleep(delay)
    
    state = subprocess.run(                 #uses the built in ping command so
        ["ping", "-c", "1", str(ip)],       #i wont have to deal with permisson issues 
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL
    )

    if state.returncode == 0:                           #in plain english; "If the host is up, type it out"
        sys.stdout.write(f"    {GREEN}[✓] {ip}    is up{RESET}\n")
        sys.stdout.flush()
        return str(ip)  
    return None


#this is cursed but works, has inputs and everything. More detail below
def run_host_discovery():
    try:                        #encased everything in a try block so i can detect if you hit ctr-c. in this way you wont see python crying
        while True:
            user_ip = input ("[?] Enter the ip address you want to scan\n\t > ")
            user_subnet = input("[?] Enter the subnet mask (default is 24)\n\t > ") or 24
            
            try:
                network = ipaddress.ip_network(f"{user_ip}/{user_subnet}", strict=False)       #looks if the host you entered is dead or alive before you waste time
            
            except ValueError:
                print(f"{RED}[!] Invalid IP address or subnet mask. Please try again.{RESET}\n")
                continue


            user_scan_type = input("[?] Would you like to perform a (D)efault scan or (S)tealth scan?\n\t > ") or "d"
            user_filename = input("[?] Output filename (default is inventory.json)\n\t > ").strip() or "inventory.json"

            if user_scan_type.lower() == "d":               #Aggrasive scan works as fast as it can so you can be done with it quick
                workers = 50
                ping_delay = 0
                print(f"{BLUE}[/] Aggressive scan is underway{RESET}\n")
                break

            elif user_scan_type.lower() == "s":             #who would have guessed, its the slow one
                workers = 10
                ping_delay = 1
                print(f"{GREEN}[@] Slow scan is underway{RESET}\n")
                break

            else:
                print(f"{RED}[!] Invalid input. Please enter D or S.{RESET}")
                continue

    except KeyboardInterrupt:
        os.system('clear')                           #the keyboard check i was talking about a few lines ago
        print(f"\n{BRIGHT_YELLOW}[!] Action interrupted by user. Exiting.{RESET}")
        return                                       #Returns to "main.py" if activated from there

    if not user_filename.lower().endswith(".json"):
        user_filename = f"{user_filename}.json"

    network = ipaddress.ip_network(f"{user_ip}/{user_subnet}", strict=False)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(lambda ip: is_host_alive(ip, delay=ping_delay), network.hosts())

    alive_hosts = [ip for ip in results if ip is not None]

    print(f"\n{GREEN}[✓] Scan complete.{RESET}")
    print(f"{BLUE}[!] {len(alive_hosts)} hosts are alive.{RESET}")
    print(f"{BLUE}[!] Results saved to {user_filename}{RESET}")

    inventory = {}

    if os.path.exists(user_filename):
        try:
            with open(user_filename, "r") as f:
                file_content = f.read().strip()
                if file_content:
                    inventory = json.loads(file_content)

        except (json.JSONDecodeError, PermissionError):
            print(f"{BRIGHT_RED}[!] Warning: Could not read {user_filename} cleanly. Starting fresh.{RESET}")
            inventory = {}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    current_hosts = []

    for host in alive_hosts:
        current_hosts.append(host)

        if host in inventory:
            inventory[host]["status"] = "up"
            inventory[host]["last_seen"] = timestamp
        else:
            inventory[host] = {
                "status": "up",
                "last_seen": timestamp,
                "open_ports": {},
                "credentials": {},
            }
            
    # Write back out to the chosen file path
    with open(user_filename, "w") as f:
        json.dump(inventory, f, indent=4)

    print(current_hosts)

    countinue = input("Would you like to scan for open ports on the discovered hosts? (Y/N)")

    if countinue.lower() == "y":

        for host in current_hosts:
            print(f"\n{BRIGHT_YELLOW}[!] Scanning for open ports on {host}...{RESET}")
            run_port_scanner(host, start_port=1, end_port=1025)



if __name__ == "__main__":
    run_host_discovery()