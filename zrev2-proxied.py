import os
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
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

def is_valid_proxy(proxy):
    parts = proxy.split(':')
    if len(parts) == 2:
        try:
            int(parts[1])
            return True
        except ValueError:
            pass
    return False

def reverse_ip(ip, proxies=None):
    url = f"https://api.rostovabrothers.com/api?ip={ip.strip()}"
    try:
        if proxies:
            proxy = random.choice(proxies)
            response = requests.get(url, proxies={'http': proxy, 'https': proxy}, verify=False)
        else:
            response = requests.get(url, verify=False)

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
            print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Failed to fetch data, Your IP maybe doesn\'t have domains')
    except requests.exceptions.ProxyError:
        print(f'{Fore.RED}Proxy dead! Using another proxy{Fore.RESET}')
        if proxies:
            proxies.remove(proxy)
            if proxies:
                reverse_ip(ip, proxies)
            else:
                print(f'{Fore.RED}No proxies left to try. Skipping IP: {ip.strip()}{Fore.RESET}')
    except requests.exceptions.ConnectTimeout:
        print(f'{Fore.RED}Connection timeout! Maybe proxy dead!{Fore.RESET}')
    except requests.exceptions.ConnectionError as e:
        if "10054" in str(e):
            print(f'{Fore.RED}Connection broken: ConnectionResetError(10054, "An existing connection was forcibly closed by the remote host", None, 10054, None){Fore.RESET}')
        else:
            print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Failed to connect to the API, Exception: {Fore.RED}{e}{Fore.RESET}')
    except requests.exceptions.JSONDecodeError:
        print(f'Error')
    except Exception as e:
        print(f'{Fore.CYAN}${Fore.RESET}{Fore.YELLOW}IP{Fore.RESET} [ {Fore.RED}{ip.strip()}{Fore.RESET} ] Failed to connect to the API, Exception: {Fore.RED}{e}{Fore.RESET}')

def scan_ips(ips, threads, proxies=None):
    valid_proxies = [proxy.strip() for proxy in proxies if is_valid_proxy(proxy.strip())] if proxies else None

    with ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = [executor.submit(reverse_ip, ip.strip(), valid_proxies) for ip in ips]
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
    use_proxies = input("Do you want to use proxies? (y/n): ").lower() == 'y'

    create_results_file()

    with open(file_name, 'r') as f:
        ips = f.readlines()

    proxies = None
    if use_proxies:
        proxy_file = input("Proxy list: ")
        with open(proxy_file, 'r') as f:
            proxies = f.readlines()

    scan_ips(ips, threads, proxies)

    total_domains = count_total_domains()
    print(f"\n{Fore.GREEN}Reverse IP Lookup Done{Fore.RESET}\n")
    print(f"=> Result saved to results.txt")
    print(f"=> You got {Fore.GREEN}{total_domains}{Fore.RESET} Domains")

if __name__ == "__main__":
    main()
