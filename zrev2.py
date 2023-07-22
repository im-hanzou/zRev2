import requests
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def print_banner():
    banner = r"""
    GITHUB : IM-Hanzou
        _______                   _____   
       |_   __ \                 / ___ `. 
 ____    | |__) |  .---.  _   __|_/___) | 
[_   ]   |  __ /  / /__\\[ \ [  ].'____.' 
 .' /_  _| |  \ \_| \__., \ \/ // /_____  
[_____]|____| |___|'.__.'  \__/ |_______| 
                                          
   zRev2 - Reverse IP Lookup using API
    """
    print(banner)

def reverse_ip(ip):
    url = f"https://api.rostovabrothers.biz.id/api.php?ip={ip}"
    user_agent = UserAgent().random
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == 200:
                domains = data["result"]
                with open('results.txt', 'a') as f:
                    for domain in domains:
                        f.write(domain + '\n')
                count = len(domains)
                print(ip + ': ' + str(count) + ' domains')
            else:
                print(ip + ': API returned an error - ' + data["message"])
        else:
            print(ip + ': Failed to fetch data, Your IP blocked from API Host')
    except:
        print(ip + ': Failed to connect to the API, API Host down!')

def scan_ips(ips, threads):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = []
        for ip in ips:
            tasks.append(executor.submit(reverse_ip, ip.strip()))
        for task in tasks:
            task.result()

def count_total_domains():
    with open('results.txt', 'r') as f:
        lines = f.readlines()
        return len(lines)

def main():
    print_banner()
    file_name = input("File list of IPs: ")
    threads = int(input("Number threads to use: "))

    with open(file_name, 'r') as f:
        ips = f.readlines()

    scan_ips(ips, threads)

    total_domains = count_total_domains()
    print(f"\n\nReverse IP lookup done. Result saved to results.txt [{total_domains} Domains]")
    print("If you only got 1 domain, try to change your IP, or use VPN")

if __name__ == "__main__":
    main()
