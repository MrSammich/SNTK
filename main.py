import os
import shutil
from portScanner import run_port_scanner
from hostDiscovery import run_host_discovery

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

#brace yourself for the shittiest tui oat

os.system('clear')
width = shutil.get_terminal_size().columns

while True:
    
    try:

        print("Welcome".center(width,"-") + "\n")
        print(f"\t{BRIGHT_YELLOW}===>[i]For Host Discovery, type 1")
        print(f"\t===>[i]For Port Scanning, type 2")
        print(f"\t===>[i]To quit, press 3 or Ctrl + C")
        print(f"\t===>[!] All of the results are stored inside 'inventory.json'{RESET}")
        desicion = str(input(" > "))
        print("-".center(width, "-"))

        if desicion == "1":
            run_host_discovery()
        
        elif desicion == "2":
            run_port_scanner()
        
        elif desicion == "3" or desicion == "exit":
            raise KeyboardInterrupt
        
        else:
            os.system('clear')
            print(f"{RED}[!]Invalid option{RESET}")
            continue

    
    except KeyboardInterrupt:
        print("\n\texiting...")
        break
   

