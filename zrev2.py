import os
import requests
import random
import urllib3
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def print_banner():
    banner_text = "zRev2 - Reverse IP Lookup using API"
    banner_github = "Github: IM-Hanzou"
    text_color = Fore.YELLOW
    banner_color = Fore.CYAN
    github_color = Fore.MAGENTA

    banner = f"""
  {text_color}{banner_text}{Fore.RESET}{banner_color}
        _______                   _____   
       |_   __ \                 / ___ `. 
 ____    | |__) |  .---.  _   __|_/___) | 
[_   ]   |  __ /  / /__\\[ \ [  ].'____.' 
 .' /_  _| |  \ \_| \__., \ \/ // /_____  
[_____]|____| |___|'.__.'  \__/ |_______| 
                                          
   {Fore.RESET}{github_color}{banner_github}{Fore.RESET}
    """
    print(banner)

def reverse_ip(ip):
    url = f"https://api.rostovabrothers.com/api?ip={ip}"
    user_agent = UserAgent().random
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == 200:
                domains = data["result"]
                if domains:
                    with open('results.txt', 'a') as f:
                        for domain in domains:
                            f.write(domain + '\n')
                    count = len(domains)
                    print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.GREEN}{ip.strip()}{Fore.RESET} ] Got [{Fore.GREEN}{str(count)}{Fore.RESET}] domains')
                else:
                    print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Doesn\'t have domains')
            else:
                print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] API returned an error - {Fore.RED}{data["message"]}{Fore.RESET}')
        else:
            print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Failed to fetch data, Your IP maybe blocked from API Host')
    except:
        print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Failed to connect to the API, API Host down!')


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

def create_results_file():
    if not os.path.exists('results.txt'):
        with open('results.txt', 'w'):
            pass

def main():
    print_banner()
    file_name = input("File list of IPs: ")
    threads = int(input("Number threads to use: "))

    create_results_file()

    with open(file_name, 'r') as f:
        ips = f.readlines()

    scan_ips(ips, threads)

    total_domains = count_total_domains()
    print(f"\n{Fore.GREEN}Reverse IP Lookup Done{Fore.RESET}\n")
    print(f"=> Result saved to results.txt")
    print(f"=> You got {Fore.GREEN}{total_domains}{Fore.RESET} Domains")

if __name__ == "__main__":
    main()
