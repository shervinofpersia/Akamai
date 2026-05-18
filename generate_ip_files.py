import os
import ipaddress

# نگاشت هر رنج به اطلاعات کشور + شرکت (بر اساس نتیجه‌ی قبلی)
# از کد کشور انگلیسی و نام شرکت استفاده می‌کنیم تا اسم فایل امن باشد.
ranges_info = {
    "104.64.0.0/10": ("US", "Akamai"),
    "23.192.0.0/11": ("US", "Akamai"),
    "23.32.0.0/11": ("US", "Akamai"),
    "172.224.0.0/12": ("US", "Akamai"),
    "23.0.0.0/12": ("US", "Akamai"),
    "184.24.0.0/13": ("US", "Akamai"),
    "2.16.0.0/13": ("NL", "Akamai"),
    "23.72.0.0/13": ("US", "Akamai"),
    "184.84.0.0/14": ("US", "Akamai"),
    "23.64.0.0/14": ("US", "Akamai"),
    "173.222.0.0/15": ("US", "Akamai"),
    "184.50.0.0/15": ("US", "Akamai"),
    "72.246.0.0/15": ("US", "Akamai"),
    "92.122.0.0/15": ("EU", "Akamai"),
    "96.16.0.0/15": ("US", "Akamai"),
    "96.6.0.0/15": ("US", "Akamai"),
    "69.192.0.0/16": ("US", "Akamai"),
    "88.221.0.0/16": ("EU", "Akamai"),
    "125.56.128.0/17": ("SG", "Akamai"),
    "209.200.128.0/18": ("US", "Akamai"),
    "59.151.128.0/18": ("US", "Akamai"),
    "60.254.128.0/18": ("US", "Akamai"),
    "72.52.0.0/18": ("US", "Akamai"),
    "122.252.32.0/19": ("US", "Akamai"),
    "122.252.128.0/20": ("PH", "Akamai"),
    "37.26.112.0/20": ("IL", "Akamai"),
    "95.100.144.0/20": ("BR", "Akamai"),
    "109.69.136.0/21": ("NL", "Akamai"),
    "193.108.88.0/21": ("EU", "Akamai"),
    "80.67.64.0/21": ("US", "Akamai"),
    "80.67.88.0/21": ("NL", "Akamai"),
    "93.191.168.0/21": ("US", "Akamai"),
    "94.127.72.0/21": ("BE", "Akamai"),
    "173.205.68.0/22": ("US", "PacketExchange"),
    "193.108.152.0/22": ("DE", "Akamai"),
    "204.10.28.0/22": ("US", "Akamai"),
    "204.237.212.0/22": ("US", "PrivateCustomer"),
    "204.8.48.0/22": ("US", "Akamai"),
    "64.145.68.0/22": ("US", "ScottResidential"),
    "80.67.84.0/22": ("NL", "Akamai"),
    "84.53.148.0/22": ("NL", "Akamai"),
    "84.53.164.0/22": ("NL", "Akamai"),
    "84.53.168.0/22": ("US", "Akamai"),
    "173.205.30.0/23": ("US", "ArcticFoxNetworks"),
    "173.245.192.0/23": ("US", "Amazon"),
    "195.245.124.0/23": ("NL", "Akamai"),
    "195.245.126.0/23": ("GB", "Akamai"),
    "195.59.188.0/23": ("EU", "Vodafone"),
    "195.95.192.0/23": ("EU", "Akamai"),
    "195.95.194.0/23": ("EU", "Akamai"),
    "204.93.62.0/23": ("DE", "NorthernCable"),
    "204.95.24.0/23": ("US", "Cogent"),
    "205.185.204.0/23": ("US", "Amazon"),
    "208.185.44.0/23": ("US", "SouthwestAirlines"),
    "209.66.126.0/23": ("US", "Zayo"),
    "61.19.12.0/23": ("TH", "CambridgeCenter"),
    "63.148.206.0/23": ("US", "CenturyLink"),
    "63.151.28.0/23": ("US", "CenturyLink"),
    "63.151.44.0/23": ("US", "CenturyLink"),
    "63.243.206.0/23": ("US", "Akamai"),
    "65.116.164.0/23": ("US", "CenturyLink"),
    "65.120.60.0/23": ("US", "CenturyLink"),
    "65.121.158.0/23": ("US", "CenturyLink"),
    "65.121.208.0/23": ("US", "CenturyLink"),
    "66.171.224.0/23": ("US", "GTT"),
    "69.22.162.0/23": ("US", "Akamai"),
    "69.31.106.0/23": ("US", "GTT"),
    "70.39.178.0/23": ("US", "GTT"),
    "70.39.182.0/23": ("US", "GTT"),
    "72.164.252.0/23": ("US", "CenturyLink"),
    "72.37.154.0/23": ("US", "IPNetZone"),
    "72.37.164.0/23": ("US", "IPNetZone"),
    "77.67.96.0/23": ("US", "Akamai"),
    "80.12.96.0/23": ("FR", "Orange"),
    "80.239.244.0/23": ("FI", "WallacOy"),
    "80.67.72.0/23": ("US", "Akamai"),
    "80.67.76.0/23": ("US", "BostonColo"),
    "84.53.134.0/23": ("US", "Akamai"),
    "84.53.136.0/23": ("US", "Akamai"),
    "93.186.138.0/23": ("IT", "Akamai_TI"),
    "104.254.123.0/24": ("US", "GTT"),
    "149.3.179.0/24": ("IT", "Akamai_TI"),
    "173.245.198.0/24": ("US", "Amazon"),
    "190.210.32.0/24": ("AR", "NSS"),
    "190.90.203.0/24": ("CO", "Internexa"),
    "193.45.15.0/24": ("SE", "Telia"),
    "194.221.64.0/24": ("EU", "Akamai"),
    "195.10.27.0/24": ("IT", "Vodafone"),
    "195.12.233.0/24": ("FI", "UniversalSatcom"),
    "195.59.122.0/24": ("EU", "Vodafone"),
    "195.59.150.0/24": ("EU", "Akamai"),
    "195.59.190.0/24": ("GB", "Vodafone"),
    "195.59.44.0/24": ("US", "TSIInstruments"),
    "198.144.100.0/24": ("US", "GTT"),
    "198.144.112.0/24": ("US", "BITE"),
    "198.144.115.0/24": ("US", "BITE"),
    "198.144.96.0/24": ("US", "GTT"),
    "198.47.108.0/24": ("US", "GTT"),
    "199.2.204.0/24": ("US", "Cogent"),
    "203.126.70.0/24": ("SG", "Unknown"),
}

def safe_filename(cc, company, cidr):
    # حذف کاراکترهای غیرمجاز از نام فایل
    safe_cidr = cidr.replace('/', '_')
    filename = f"{cc}_{company}_{safe_cidr}.txt"
    # حذف هر کاراکتری جز حروف، اعداد، خط زیر و خط تیره
    import re
    filename = re.sub(r'[^\w\-.]', '', filename)
    return filename

def generate_files():
    output_dir = "ip_lists"
    os.makedirs(output_dir, exist_ok=True)
    
    for cidr, (cc, company) in ranges_info.items():
        print(f"Processing {cidr} ({cc}_{company}) ...")
        network = ipaddress.ip_network(cidr)
        filename = safe_filename(cc, company, cidr)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            for ip in network:
                f.write(str(ip) + '\n')
        print(f" -> {filename} ({network.num_addresses} IPs) written.")
    
    print("Done!")

if __name__ == "__main__":
    generate_files()
