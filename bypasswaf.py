import socket
import sys
import ssl
import os
import requests
import urllib.request
import random
import argparse


from cryptography import x509
from cryptography.hazmat.backends import default_backend
from colorama import *
import threading
import time
from bs4 import BeautifulSoup
import configparser
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

###############BANNER###############
class INFO:
    
    version = "2.1.1"
    """Update 
    1. fix bug save file
    """
    dev_by = "BabyH@ck"
    facebook = "https://www.facebook.com/thanawee321"
    youtube = "https://www.youtube.com/@BabyHackSenior"
    default_path_install_file = "/usr/local/share/bypasswaf"
    namefile = os.path.join(default_path_install_file,"config.ini")
    
    wordlist_url = "https://raw.githubusercontent.com/reewardius/bbDomains.txt/refs/heads/main/bug-bounty-program-subdomains-trickest-inventory.txt"
    default_wordlists = os.path.join(default_path_install_file,"wordlists.txt")
    updated_wordlists = os.path.join(default_path_install_file,"wordlists.txt")
    
    

    
def banner():
    
    info = INFO()
    version = info.version
    logo_lines = [
        
        " ██████╗    █████╗   ██████╗  ██╗   ██╗ ██╗  ██╗  ██████╗   ██████╗  ██╗  ██╗",
        " ██╔══██╗  ██╔══██╗  ██╔══██╗ ╚██╗ ██╔╝ ██║  ██║ ██╔═══██╗ ██╔═══██╗ ██║ ██╔╝",
        " ██████╔╝  ███████║  ██████╔╝  ╚████╔╝  ███████║ ██║   ██║ ██║   ╚═╝ █████═╝ ",
        " ██╔══██╗  ██╔══██║  ██╔══██╗   ╚██╔╝   ██╔══██║ ██║ █ ██║ ██║       ██╔ ██╗ ",
        " ██████╔╝  ██║  ██║  ██████╔╝    ██║    ██║  ██║ ██║ ████║ ██║   ██╗ ██╔══██╗",
        " ╚═════╝   ╚═╝  ╚═╝  ╚═════╝     ╚═╝    ╚═╝  ╚═╝  ╚══╝╚══╝ ╚██████╔╝ ╚═╝  ╚═╝",
       f"                                                (BYPASS_WAF_APPLICATION_V{version})"
       
    ]
    
    foreground_colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE
]
    rand_color = random.choice(foreground_colors)
    return "\n".join([rand_color + line + Style.RESET_ALL for line in logo_lines])+"\n"
    
    
def information():
    
    width = 60
    info = INFO()
    version = info.version
    dev_by = info.dev_by
    facebook = info.facebook
    youtube = info.youtube
    

    # สร้างกรอบและเก็บในตัวแปร
    result = []
    
    edge = "=" + Fore.WHITE
    
    # ขอบบน
    result.append(edge * width)
    result.append(edge + " " * (width - 2) + edge)  # บรรทัดว่าง
    
    
    # ข้อความชิดซ้าย
    title_text = f"\tTool bypass WAF application and more other".ljust(width - 8)
    version_text = f" Version       : {version}".ljust(width - 2)
    dev_by_text = f" DevBy         : {dev_by}".ljust(width - 2)
    aboutme = f" Facebook      : {facebook}".ljust(width - 2)
    youtube = f" Youtube  : {youtube}".ljust(width - 2)
    
    result.append(edge + title_text + edge)
    result.append(edge + version_text + edge)
    result.append(edge + dev_by_text + edge)
    result.append(edge + aboutme + edge)
    result.append(edge + youtube + edge)
    result.append(edge + " " * (width - 2) + edge)  # บรรทัดว่าง
    result.append(edge + " " * (width - 2) + edge)  # บรรทัดว่าง
    result.append(edge * width + Fore.RESET)  # ขอบล่าง

    # รวมข้อความทั้งหมดเป็นสตริงเดียว
    border_content = "\n".join(result)

    # ผลลัพธ์ที่ประกอบกันเป็น ASCII Art และกรอบ
    return banner() + "\n" + border_content + "\n"
    
##########################################################

###############PARSER###############
def get_parser():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",help="IP Address or Domain name")
    parser.add_argument("-s","--securitytrailsAPI",help="Setting API Key -s <Your API Key> (Ex. -s t4uwUDrv5mIe0aR19KIGThhhVrCAE86u)")
    parser.add_argument("-w","--wordlists",help="Setting custom wordlists file -w <Your file location> (Ex. -w wordlists.txt)")
    parser.add_argument("-T","--Thread",help="Setting Threading -T <NUM THREAD>(Ex. -T 50",default=50)
    return parser
##########################################################


###############GETDOMAIN###############
def get_real_ip(domain):
    try:
        
        ip_address = socket.gethostbyname(domain)
        
    except Exception as e:
        
        print(f"{Fore.RED}[-] ERROR Get real IP Address : {Fore.RESET}{e}")
        
    return ip_address
###########################################################



#############GETWAFINFOMATION##########
def is_use_WAF(domain):
    WAF_SIGNATURES = {
    "Cloudflare": ["cf-ray", "cf-cache-status", "cloudflare", "__cfduid", "__cf_bm"],
    "Akamai": ["akamai", "akamai-ghost", "akamaighost", "ak_bmsc"],
    "Sucuri": ["x-sucuri-id", "x-sucuri-cache"],
    "Imperva / Incapsula": ["incapsula", "x-iinfo", "x-cdn"],
    #"F5 BIG-IP": ["bigipserver", "f5", "x-waf-status"],
    "AWS WAF": ["awswaf", "x-amz-cf-id", "x-amzn-requestid"],
    "ModSecurity": ["mod_security", "modsecurity", "x-mod-security", "x-powered-by-modsecurity"],
    "Barracuda": ["barra", "barracuda", "barra-counter"],
    "Citrix Netscaler": ["citrix", "ns_af"],
    "Fortinet FortiWeb": ["fortiwafsid", "fortinet", "fortiweb"],
    "Palo Alto Networks": ["paloalto", "x-paloalto"],
    "Azure WAF": ["azure", "x-azure-ref", "x-azure-socketip"],
    "Google Cloud Armor": ["x-cloud-armor"],
    "StackPath": ["stackpath", "sp-request-id"],
    "Fastly": ["fastly", "x-fastly-request-id"],
    "SiteGround": ["siteground", "sg-optimizer"],
    "Radware": ["radware", "x-rdwr"],
    "Check Point AppWall": ["appwall", "x-cp-appwall-action"],
    "Wallarm": ["wallarm", "x-wallarm-mode"],
    "Reblaze": ["reblaze", "rbzid"],
    "Cloudbric": ["cloudbric", "x-cloudbric-id"],
    "BlazingFast": ["blazingfast", "bf-cdn"],
    "NSFocus": ["nsfocus"],
    "Trustwave": ["trustwave", "tswaf"],
    "Alibaba Cloud WAF": ["aliwaf", "x-aliwaf-id"],
    "Generic WAF": ["x-waf", "x-firewall", "x-protected-by"]
    }
    
    urls = [f"http://{domain}",f"https://{domain}"]
    headers= {}
    detected_waf=[]
    waf_tech = {"waf_list":[]}
    for url in urls :
        try:
            response = requests.get(url,timeout=5)
            headers = {k.lower():v.lower() for k,v in response.headers.items()}
            if headers:
                for waf_name,signature in WAF_SIGNATURES.items():
                    for sig in signature:
                        if any(sig in v for k,v in headers.items()):
                            detected_waf.append(waf_name)

                if detected_waf:
                    waf_tech["waf_list"] = detected_waf
                    return True,waf_tech
        except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
            continue

    if not waf_tech["waf_list"]:
        waf_tech["waf_list"] = ["Not Detected"]
    return False,waf_tech
###############################################################



############DETECTED_WEB_SERVER############
def detected_web_server(domain):
    urls = [f"http://{domain}",f"https://{domain}"]
    for url in urls:
        try:
        
            response = requests.head(url,timeout=5)
            server_headers = response.headers.get("Server")
            if server_headers:
                return server_headers
        except (requests.exceptions.RequestException, requests.exceptions.ConnectionError): 
            continue
        
    return "UNKNOWN"
##################################################################        
       
def config_APIKEY(api_key):
    config = configparser.ConfigParser()
    info = INFO()
    namefile = info.namefile
    
    #Create file config.ini
    if not os.path.exists(namefile):
        config["DEFAULT"] = {
            "securitytrails_api_key": "your_api_key"
        }
        with open(namefile,'w') as file:
            config.write(file)
            
        print(f"{Fore.GREEN}[+] Create file config.ini Successfully.{Fore.RESET}")
        
        
    config.read(namefile)
    if api_key:
        config.set("DEFAULT","securitytrails_api_key",api_key)
        with open(namefile,'w') as file:
            config.write(file)
            print(f"{Fore.CYAN}[+] API Key has been updated to: {Fore.RESET}{api_key}")
    else:
        current_key = config.get("DEFAULT", "securitytrails_api_key", fallback="your_api_key")
        print(f"{Fore.YELLOW}[!] Current API Key: {Fore.RESET}{current_key}")
            
        
##########GET_DOMAIN_HISTORICAL##########  
def get_domain_historical_ip_address(domain):

    try:
        
        
        driver = webdriver.Chrome()
        driver.get(f"https://viewdns.info/iphistory/?domain={domain}")
        
        print(f"{Fore.GREEN}[+] Fetching historical IP data for {Fore.RESET}{domain} ...")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        table = soup.find('table')
        if not table:
            print(f"{Fore.RED}[-] No table found. You might be blocked or page structure changed.{Fore.RESET}")
            return
        
        rows = table.find_all('tr')[2:]  # ข้าม header 2 แถวแรก
        
        print(f"\n{Fore.GREEN}[+] {Fore.CYAN}Historical IP Address Info from {Fore.RESET} ViewDNS.com {Fore.GREEN}IP data for {Fore.RESET}{domain}")
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4:
                continue  # skip row ที่ไม่ครบ columns
            
            ip_address = cols[0].text.strip()
            location = cols[1].text.strip()
            owner = cols[2].text.strip()
            last_seen = cols[3].text.strip()
            
            print(f"\n{Fore.GREEN} [+] IP Address: {Fore.RESET}{ip_address}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Last Seen : {Fore.RESET}{last_seen}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Organizations : {Fore.RESET}{owner}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Location : {Fore.RESET}{location}")
            
            
            
    except Exception as e:
        print(f"{Fore.RED}[-] Exception : {e}{Fore.RESET}")
########################################################################################


############GET_DOMAIN_HISTORICAL_BY_SECURITYTRAILS########################
def get_domain_historical_securitytrails_ip_address(domain):
    info = INFO()
    namefile = info.namefile
    config = configparser.ConfigParser()
    config.read(namefile)
    
    api_key = config.get("DEFAULT","securitytrails_api_key",fallback=None)
    try:
        if api_key is None or api_key.strip().lower() == "your_api_key":
            print(f"{Fore.RED}[!] Not setting API Key...{Fore.RESET}")
            if input(f"{Fore.BLUE}[!] Do you want to Setup API KEY? {Fore.YELLOW}(Y/n) : {Fore.RESET}").lower() == 'y':
                api_key_update = input(f"{Fore.BLUE}[+] Your API KEY : {Fore.RESET}").strip() 
                config_APIKEY(api_key_update)
                pass
            else:
                return
    
        url = f"https://api.securitytrails.com/v1/history/{domain}/dns/a"
        headers = {
                    "accept": "application/json",
                    "APIKEY": str(api_key)}
                   
    
        response = requests.get(url,headers=headers)
        data = response.json()
        print(f"{Fore.GREEN}[+] Fetching historical by {Fore.RESET}securitytrails.com {Fore.GREEN}IP data for {Fore.RESET}{domain} ...")
        for record in data['records']:
            ip_address = record["values"][0]["ip"]
            first_seen = record["first_seen"]
            last_seen = record["last_seen"]
            organizations = record["organizations"][0]
            
            try:
                response_location = requests.get(f"http://ip-api.com/json/{ip_address}",timeout=5)
                data = response_location.json()
            except:
                pass
            
            print(f"\n{Fore.GREEN} [+] IP Address: {Fore.RESET}{ip_address}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} First Seen : {Fore.RESET}{first_seen}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Last Seen : {Fore.RESET}{last_seen}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Organizations : {Fore.RESET}{organizations}")
            print(f"{Fore.CYAN}  \u2514\u27A4 {Fore.RESET}{Fore.GREEN} Location : {Fore.RESET}{str(data['country'])}")
            
    except Exception as e:

        print(f"{Fore.RED}[-] ERROR API_KEY Exception : {e}{Fore.RESET}")
        print(f"{Fore.YELLOW}[!] If you update API_KEY {Fore.CYAN}Please run command again!!{Fore.RESET}")

        
##########MENU HISTORICAL###########
def select_historical_memu(domain):
    while True:
        print(f"{Fore.CYAN}\n[!] Select historical view info{Fore.RESET}")
        print(f"{Fore.MAGENTA}[1] 'viewdns.info' ")
        print("[2] 'securitytrails.com' ")
        print(f"[0]  Back...{Fore.RESET}")
    
        select = input(f"\n{Fore.BLUE}[!] Select menu : {Fore.RESET}")
        if select == '1':
            get_domain_historical_ip_address(domain)
        if select == '2':
            get_domain_historical_securitytrails_ip_address(domain)
            
        elif select == '0':
            break
###################################################

###########DOWNLOAD_WORDLISTS#############
def download_wordlists(wordlists_path):
    wordlists_url = INFO().wordlist_url
    updated_wordlists = INFO().updated_wordlists
    default_wordlists = INFO().default_wordlists
    try:
        if not os.path.exists(default_wordlists):
            print(f"\n{Fore.GREEN}[+] Downloading an updated wordlist from {Fore.WHITE}reewardius{Fore.RESET}")
        
            urllib.request.urlretrieve(wordlists_url,wordlists_path)
            print(f"{Fore.GREEN}[+] Wordlist downloaded successfully as {Fore.WHITE}{wordlists_path}{Fore.RESET}")
            
            return updated_wordlists
        else:
            if input(f"{Fore.BLUE}[!] Do you want update Wordlists from {Fore.WHITE}reewardius{Fore.RESET}? {Fore.YELLOW}(Y/n) : {Fore.RESET}").lower() == 'y':
                urllib.request.urlretrieve(wordlists_url,wordlists_path)
                print(f"{Fore.GREEN}[+] Wordlist downloaded successfully as {Fore.WHITE}{wordlists_path}{Fore.RESET}")
                
                
                
            
            if input(f"{Fore.BLUE}[!] Do you want select custom wordlists?{Fore.YELLOW} (Y/n) : {Fore.RESET}").lower() == 'y':
                custom_path_wordlists = input(f"{Fore.GREEN}[+] {Fore.BLUE}Custom wordlists file : {Fore.RESET}")
                if not os.path.exists(custom_path_wordlists):
                    print(f"{Fore.RED}[-] Custom wordlists file not found...{Fore.RESET}")
                    print(f"{Fore.CYAN}[!] Default wordlists file as : {Fore.RESET}{default_wordlists}") 
                    return default_wordlists
                else:
                    print(f"{Fore.GREEN}[+] File wordlists : {Fore.RESET}{custom_path_wordlists}")
                    return custom_path_wordlists
            
            return default_wordlists
            
    except Exception as e:
        
        print(f"{Fore.RED}[-] Error downloading wordlist: {Fore.RESET}{e}")
        print(f"{Fore.CYAN}[!] Using the existing wordlist {Fore.GREEN}{custom_path_wordlists}{Fore.RESET}")
        
           
        
        return custom_path_wordlists
####################################################################

def get_ssl_certificate_info(host):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=host) as sock:
            sock.connect((host, 443))
            certificate_der = sock.getpeercert(True)

        certificate = x509.load_der_x509_certificate(certificate_der, default_backend())

        common_name = certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        issuer = certificate.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        serial_number = certificate.serial_number
        sig_algo = certificate.signature_hash_algorithm.name


        validity_start = certificate.not_valid_before_utc
        validity_end = certificate.not_valid_after_utc

        return {
            "Common Name": common_name,
            "Issuer": issuer,
            "Serial Number":serial_number,
            "Signature Algorithm":sig_algo,
            "Validity Start": validity_start,
            "Validity End": validity_end,
            
        }
    except Exception as e:
        print(f"{Fore.RED}[-] Error extracting SSL certificate information : {Fore.RESET}{e}")
        return None



#########################FIND_SUBDOMAIN_SSL#############################
def find_subdomains_with_ssl_analysis(domain,wordlists_path_updated,worker=50):
    
    subdomains_found = []
    subdomain_status_200 = []
    subdomains_lock = threading.Lock()
    stop_event = threading.Event()
    
    def check_subdomain(subdomain):
        if stop_event.is_set():
            return
        subdomain_url = f"https://{subdomain}.{domain}"
        
        
        try:
            response = requests.get(subdomain_url, timeout=(0.5,0.5),verify=True)
            if response.status_code == 200:
                with subdomains_lock:
                    subdomains_found.append(subdomain_url)
                    print(f"{Fore.GREEN}[+] Subdomain Found {Fore.CYAN}\u2514\u27A4{Fore.WHITE} {subdomain_url}{Fore.RESET}")
                    subdomain_status_200.append(f"{Fore.GREEN}[+] Subdomain Found {Fore.CYAN}\u2514\u27A4{Fore.WHITE} {subdomain_url}{Fore.RESET}")
            elif response.status_code != 200:
                print(f"{Fore.RED}[-] Subdomain {Fore.YELLOW}[{response.status_code}]{Fore.RED} request {Fore.CYAN}\u2514\u27A4{Fore.WHITE} {subdomain_url}{Fore.RESET}")
                
               
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[-] Subdomain error requests {Fore.CYAN}\u2514\u27A4{Fore.WHITE} {subdomain_url}{Fore.RESET}")
            if "Max retries exceeded with url" in str(e):
                pass
        
        
        
    print(f"{Fore.GREEN}[+] Wordlists file {Fore.RESET}{wordlists_path_updated}")
    with open(wordlists_path_updated,"r",encoding='utf-8',errors='ignore') as file:
        subdomains = [line.strip() for line in file.readlines()]
        
        
        
    MAX_WORKERS = worker    
    print(f"\n{Fore.YELLOW}[!] Starting {MAX_WORKERS} threads...{Fore.RESET}")
    
    if MAX_WORKERS >=500:
        print(f"{Fore.RED}[!] Warning Using too many threads{Fore.YELLOW}[{MAX_WORKERS}]{Fore.RED}can cause high memory usage and CPU Usage{Fore.RESET}")
    
    time.sleep(2)
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_subdomain,subdomain) for subdomain in subdomains]
        
        try:
            for future in as_completed(futures):
                if stop_event.is_set():
                    break
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Stop scanning by user (Ctrl+C)...{Fore.RESET}\n")
            stop_event.set()
            executor.shutdown(wait=False)
            time.sleep(0.5)
    
    """threads = []
    try:
        for subdomain in subdomains:
            if stop_event.is_set():
                break
        
            t1 = threading.Thread(target=check_subdomain,args=(subdomain,))
            threads.append(t1)
            t1.start()
            
        
        for thread in threads:
            thread.join()
            
    except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] {Fore.YELLOW}Stop scanning subdomain by user (Ctrl+C)...{Fore.RESET}")
            stop_event.set()
            for thread in threads:
                thread.join()"""
    
    time.sleep(3)
    print(f"{Fore.GREEN}\n[!] {Fore.CYAN}Summary found subdomain!!{Fore.RESET}")    
    for log in subdomain_status_200:
        print(log)    
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"\n{Fore.GREEN} {Fore.CYAN}\u2514\u27A4{Fore.RESET}{Fore.GREEN} [+] Total Subdomains Scanned : {Fore.RESET} {len(subdomains)}")
    print(f"{Fore.GREEN} {Fore.CYAN}\u2514\u27A4{Fore.RESET}{Fore.GREEN} [+] Total Subdomains Found :{Fore.RESET} {len(subdomains_found)}")
    print(f"{Fore.GREEN} {Fore.CYAN}\u2514\u27A4{Fore.RESET}{Fore.GREEN} [+] Time taken : {Fore.RESET} {hours:02d}:{minutes:02d}:{seconds:02d} seconds\n")


    real_ips = []
    for subdomain in subdomains_found:
        subdomain_paths = subdomain.split('//')
        if len(subdomain_paths) > 1:
            host = subdomain_paths[1]
            real_ip = get_real_ip(host)

            if real_ip:
                real_ips.append((host,real_ip))
                print(f"{Fore.GREEN}[+] Real IP Address of {Fore.RESET}{host} : {real_ip}")
                ssl_info = get_ssl_certificate_info(host)
                if ssl_info:
                    print(f"{Fore.GREEN}[+] {Fore.CYAN}SSL Certificate Information :")
                    #k=key,v=values
                    for k,v in ssl_info.items():
                        print(f"{Fore.CYAN}      \u2514\u27A4 {Fore.RESET}{k} : {v}")
    
        print("\n")            
    if not real_ips:
        print(f"{Fore.RED}[-] No real IP addresses found for subdomains.{Fore.RESET}")
        pass
    else:
        print(f"\n{Fore.GREEN}[+] Task Complete!!{Fore.RESET}\n")
        pass
            
###############MAIN###############
def main():
    
    logo = information()
    print(logo)
    
    parser = get_parser()
    args = parser.parse_args()
    
    if args.target:
        domain = args.target
        worker = int(args.Thread)
        ip_address = ip_address = domain if domain.replace('.', '').isdigit() else get_real_ip(domain)
        
        print(f"{Fore.GREEN}[+]{Fore.CYAN} Domain name website : {Fore.RESET}{str(domain)}")
        print(f"{Fore.GREEN}[+]{Fore.CYAN} Visible IP Address : {Fore.RESET}{str(ip_address)}\n")
        
    
        print(f"{Fore.GREEN}\n[!]{Fore.YELLOW} Checking.. website use a WAF{Fore.RESET}")
        waf_status,waf_info = is_use_WAF(domain)
        tech = detected_web_server(domain)
        
        wordlists_path = INFO().default_wordlists
        
        if waf_status:
            
            print(f"{Fore.GREEN}[+] WAF Detected : {Fore.RESET}{",".join(waf_info['waf_list'])}")
            print(f"{Fore.GREEN}[+] Website is using : {Fore.RESET}{tech}")
            
            if input(f"{Fore.BLUE}[!] Do you want to view historical? {Fore.YELLOW}(Y/n): {Fore.RESET}").lower() == 'y':
                select_historical_memu(domain)
            
            print(f"\n{Fore.GREEN}[!] {Fore.YELLOW}Scanning for subdomain...{Fore.RESET}")
            
            if args.wordlists:
                custom_path_wordlists = args.wordlists
                if not os.path.exists(custom_path_wordlists):
                    print(f"{Fore.RED}[-] Wordlists file {Fore.RESET}{custom_path_wordlists}{Fore.RED} not found!!!{Fore.RESET}\n")

                    wordlists_path_updated = download_wordlists(wordlists_path)
                    find_subdomains_with_ssl_analysis(domain,wordlists_path_updated,worker)
                
                find_subdomains_with_ssl_analysis(domain,custom_path_wordlists,worker)
                
            else:
                
                wordlists_path_updated = download_wordlists(wordlists_path)
                if input(f"{Fore.BLUE}[!] Do you want process {Fore.YELLOW}(Y/n) : {Fore.RESET}").lower() == 'y':
                    find_subdomains_with_ssl_analysis(domain,wordlists_path_updated,worker)
                    
                else:
                    print(f"{Fore.RED}[+] Exit...{Fore.RESET}")
                    return 

            
            
        else:
            
            print(f"{Fore.YELLOW}[!] WAF Detected : {Fore.RESET}{Fore.RED}{",".join(waf_info['waf_list'])}{Fore.RESET}")
            print(f"{Fore.GREEN}[+] Website is using : {Fore.RESET}{tech}")
            select_historical_memu(domain)
            wordlists_path_updated = download_wordlists(wordlists_path)
            if input(f"{Fore.BLUE}[!] Do you want process {Fore.YELLOW}(Y/n) : {Fore.RESET}").lower() == 'y':
                    find_subdomains_with_ssl_analysis(domain,wordlists_path_updated,worker)
                    
            else:
                return
    
    elif args.securitytrailsAPI:
        api_key = args.securitytrailsAPI
        config_APIKEY(api_key)
    
    
    elif not args.target and not args.securitytrailsAPI:
        parser.print_help()
        sys.exit(1)
    
    
    return None
##########################################################


if __name__ == '__main__':
    if os.getuid() !=0:
        print(f"{Fore.RED} Please run as '{Fore.YELLOW}sudo{Fore.RESET}{Fore.RED}' only")
        sys.exit(1)
        
    main()






