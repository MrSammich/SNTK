<h1>SNTK/Simple Network ToolKit</h1>

This is a tiny script for port scanning and host discovery that saves its results to a json

<h1>About This Project</h1>

Main.py is just a simple text user interface for running the actual scrips which can be called as functions in your project easily.
Both port scanning and host discovery save to the same json by default in a way that file wont be confusing to read you may also point the output
in to file of your choice

<h1>Host Discovery</h1>

Host discovery simply takes the ip address you provided and pings all possible ip addresses relative to subnet mask (CIDR) you provide to it.
Default value for subnet mask is 24 but you can chose any subnet mask you like

```json
    "192.168.1.1": {
        "status": "up",
        "last_seen": "2026-07-11 16:32:48",
        "open_ports": {},
        "credentials": {}
```

In the example of a default gateway scan, you can see that Host discovery only fills the "status" and "last_seen" feilds, hence its nature

To use the funciton in your own code;

```py
from hostDiscovery import run_host_discovery

run_host_discovery(user_ip="", user_subnet=24, user_scan_type="", user_filename="")
```
firstly, the "user_ip", this is the ip that will get scanned. you can assign it with an varibale or hard code it dont forget to put it inside this => " "

for the "user_subnet", its best if you leaved it at 24. Same as before you can assign a baribale to it

for the scan type, there are 2 options either the "d" which is default/aggrasive scan or "s" for slow/stealth scan

finally, for the "user_filename" point it to a .json or .txt file. Fair warning i never tested anything other than json files

<h1>Port Scanner</h1>

This script works by trying to connect to a spesific port on provided host, if it fails it assumes port requires HTTP request which the script sends and listens again 
to identify what is running there and if its even active/open and writes it down to the json

```json
{
    "192.168.1.1": {
        "status": "up",
        "last_seen": "2026-07-11 16:52:05",
        "open_ports": {
            "53": {
                "last_seen": "2026-07-11 16:11:14",
                "banner": "Unknown"
            },
            "80": {
                "last_seen": "2026-07-11 16:11:14",
                "banner": "Server: ##### web server 1.0 ##### corp 2015."
            },
            "443": {
                "last_seen": "2026-07-11 16:11:14",
                "banner": "Server: #### web server 1.0 #### corp 2015."
            }
        },
        "credentials": {}
```
Yea this script isnt as advanced as nmap so it cannot identify most of the services but it can identify ssh, web servers etc nicely

To use this in your own scripts;

```py
from portScanner import run_port_scanner

run_port_scanner(host, start_port=1, end_port=1025)
```

this one is easier to use, for host you can hardcode or assign the ip to a variable enclosed in " "

for start_port and end_port its just the range of the ports the script will scan.
yes it does not asks for the file like in host discovery becouse i kinada focused on banner grabbing way too much, will be updated PROBABLY
