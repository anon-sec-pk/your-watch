import requests
import socket
import subprocess
from ipwhois import IPWhois
import os
import ipaddress
import whois

def get_ip_info(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    return data

def get_my_ip():
    return requests.get("https://api.ipify.org").text

def domain_to_ip(domain):
    return socket.gethostbyname(domain)

def ip_to_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname[0]
    except socket.herror:
        return None

def get_asn_info(ip_address):
    try:
        obj = IPWhois(ip_address)
        results = obj.lookup_rdap()
        return results
    except Exception as e:
        print("\033[31mError fetching ASN information:", e)
        return None

def perform_traceroute(ip_address):
    try:
        result = subprocess.run(['traceroute', ip_address], capture_output=True, text=True)
        print("\033[31mTraceroute Results:")
        print(result.stdout)
    except FileNotFoundError:
        print("\033[31mTraceroute command not found. Please install traceroute.")

def perform_port_scan(ip_address):
    try:
        result = subprocess.run(['nmap', '-Pn', '-p-', ip_address], capture_output=True, text=True)
        print("\033[31mPort Scan Results:")
        print(result.stdout)
    except FileNotFoundError:
        print("\033[31mNmap command not found. Please install nmap.")

def reverse_dns_lookup(ip_address):
    try:
        result = socket.gethostbyaddr(ip_address)
        return result[0]
    except socket.herror:
        return None

def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        print("\033[31mError performing WHOIS lookup:", e)
        return None

def validate_ip(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def ping_ip(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], capture_output=True, text=True)
        print("\033[31mPing Results:")
        print(result.stdout)
    except Exception as e:
        print("\033[31mError performing ping:", e)

def print_banner():
    print("\033[32m")
    print("""
    __   __                  __          __        _       _     
    \ \ / /___   ___   _ __  \ \        / /  __ _| |_ ___| |__  
     \ V // _ \ / _ \ | '__|  \ \  /\  / /  / _` | __/ __| '_ \ 
      | | (_) | (_) || |      \ \/  \/ /  | (_| | || (__| | | |
      |_|\___/ \___/ |_|       \  /\  /    \__,_|\__\___|_| |_|
                               \/  \/                             
    """)

def main():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_banner()
    print("\033[31mWelcome to SCF_PK IP Tools!\033[0m")
    print("\033[31m1. Get information about a specific IP address\033[0m")
    print("\033[31m2. Get information about your own IP address\033[0m")
    print("\033[31m3. Convert domain to IP address\033[0m")
    print("\033[31m4. Find hostname from IP address\033[0m")
    print("\033[31m5. Get ASN information for an IP address\033[0m")
    print("\033[31m6. Perform traceroute to an IP address\033[0m")
    print("\033[31m7. Perform port scan on an IP address\033[0m")
    print("\033[31m8. Get information for multiple IP addresses\033[0m")
    print("\033[31m9. Perform reverse DNS lookup\033[0m")
    print("\033[31m10. Perform WHOIS lookup\033[0m")
    print("\033[31m11. Validate IP address format\033[0m")
    print("\033[31m12. Perform ping to IP address\033[0m")
    choice = input("\033[31mChoose an option (1-12): \033[0m")

    if choice == '1':
        ip_address = input("Enter the IP address: ")
        ip_info = get_ip_info(ip_address)
        if ip_info['status'] == 'fail':
            print("Failed to retrieve IP information. Please check the IP address.")
        else:
            print(f"\033[31m\nIP Information for {ip_address}:\033[0m")
            print(f"IP Address: {ip_info['query']}")
            print(f"Country: {ip_info['country']}")
            print(f"Region: {ip_info['regionName']}")
            print(f"City: {ip_info['city']}")
            print(f"ZIP: {ip_info['zip']}")
            print(f"Latitude: {ip_info['lat']}")
            print(f"Longitude: {ip_info['lon']}")
            print(f"ISP: {ip_info['isp']}")
            print(f"Organization: {ip_info['org']}")
            print(f"AS: {ip_info['as']}")
    elif choice == '2':
        ip_address = get_my_ip()
        print(f"Your IP address is: {ip_address}")
    elif choice == '3':
        domain = input("Enter the domain name: ")
        ip_address = domain_to_ip(domain)
        print(f"The IP address for {domain} is {ip_address}")
    elif choice == '4':
        ip_address = input("Enter the IP address: ")
        hostname = ip_to_hostname(ip_address)
        if hostname:
            print(f"The hostname for {ip_address} is {hostname}")
        else:
            print("Hostname could not be found.")
    elif choice == '5':
        ip_address = input("Enter the IP address: ")
        asn_info = get_asn_info(ip_address)
        if asn_info:
            print("\033[31m\nASN Information:\033[0m")
            print(f"ASN: {asn_info['asn']}")
            print(f"ASN Registry: {asn_info['asn_registry']}")
            print(f"ASN CIDR: {asn_info['asn_cidr']}")
            print(f"ASN Country Code: {asn_info['asn_country_code']}")
            print(f"ASN Description: {asn_info['asn_description']}")
    elif choice == '6':
        ip_address = input("Enter the IP address: ")
        print(f"Performing traceroute to {ip_address}...")
        perform_traceroute(ip_address)
    elif choice == '7':
        ip_address = input("Enter the IP address: ")
        print(f"Performing port scan on {ip_address}...")
        perform_port_scan(ip_address)
    elif choice == '8':
        ip_addresses = input("Enter the IP addresses (comma-separated): ").split(',')
        for ip in ip_addresses:
            ip = ip.strip()
            ip_info = get_ip_info(ip)
            if ip_info['status'] == 'fail':
                print(f"Failed to retrieve information for {ip}.")
                continue
            print(f"\033[31m\nIP Information for {ip}:\033[0m")
            print(f"IP Address: {ip_info['query']}")
            print(f"Country: {ip_info['country']}")
            print(f"Region: {ip_info['regionName']}")
            print(f"City: {ip_info['city']}")
            print(f"ZIP: {ip_info['zip']}")
            print(f"Latitude: {ip_info['lat']}")
            print(f"Longitude: {ip_info['lon']}")
            print(f"ISP: {ip_info['isp']}")
            print(f"Organization: {ip_info['org']}")
            print(f"AS: {ip_info['as']}")
    elif choice == '9':
        ip_address = input("Enter the IP address: ")
        hostname = reverse_dns_lookup(ip_address)
        if hostname:
            print(f"The reverse DNS lookup result for {ip_address} is {hostname}")
        else:
            print("Reverse DNS lookup failed.")
    elif choice == '10':
        domain = input("Enter the domain name: ")
        domain_info = whois_lookup(domain)
        if domain_info:
            print(f"\033[31m\nWHOIS Information for {domain}:\033[0m")
            print(domain_info)
    elif choice == '11':
        ip_address = input("Enter the IP address: ")
        if validate_ip(ip_address):
            print(f"{ip_address} is a valid IP address.")
        else:
            print(f"{ip_address} is not a valid IP address.")
    elif choice == '12':
        ip_address = input("Enter the IP address: ")
        print(f"Pinging {ip_address}...")
        ping_ip(ip_address)

if __name__ == "__main__":
    main()
