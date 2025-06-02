import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

# === Configurações ===
if len(sys.argv) > 1:
    IP = sys.argv[1]
else:
    IP = input("Digite o IP: ").strip()

if not IP or not re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", IP):
    console.print("[bold red]IP inválido ou não informado.")
    exit()

URL = f"https://www.shodan.io/host/{IP}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# === Requisição ===
response = requests.get(URL, headers=HEADERS)

if response.status_code != 200:
    console.print(f"[bold red]Erro ao acessar Shodan: {response.status_code}")
    exit()

html = response.text
soup = BeautifulSoup(html, "html.parser")
output = f"Recon Shodan - Host {IP}\n"
output += "=" * 40 + "\n\n"

# --- General Info ---
general_info = {}

# Hostnames
hostnames = []
host_label = soup.find("label", string="Hostnames")
if host_label:
    div = host_label.find_next_sibling("div")
    if div:
        raw = div.decode_contents().split("<br/>")
        for h in raw:
            clean = re.sub(r"<.*?>", "", h).strip()
            if clean:
                hostnames.append(clean)
if hostnames:
    general_info["Hostnames"] = hostnames

output += "[General Info]\n"
for k, v in general_info.items():
    if isinstance(v, list):
        output += f"{k}:\n"
        for item in v:
            output += f"  - {item}\n"
    else:
        output += f"{k}: {v}\n"
output += "\n"

# --- Domains ---
domains = []
for a in soup.select("div.domains a.button"):
    text = a.text.strip()
    if text and "." in text:
        domains.append(text)
output += "[Domains]\n" + "\n".join(domains) + "\n\n"

# --- Web Technologies ---
technologies = []
for tech in soup.select("#http-components .technology-name"):
    name = tech.text.strip()
    if name:
        technologies.append(name)
output += "[Web Technologies]\n" + "\n".join(set(technologies)) + "\n\n"

# --- Vulnerabilities ---
vulns = {}

m = re.search(r"const VULNS\s*=\s*(\{.*?\});", html, re.DOTALL)
if m:
    try:
        vulns = json.loads(m.group(1))
    except Exception as e:
        console.print(f"[bold red]Erro ao processar VULNS: {e}")

output += "[Vulnerabilities]\n"
if vulns:
    for cve, data in vulns.items():
        output += f"{cve}\n"
        output += f"  CVSS: {data.get('cvss')}\n"
        output += f"  Ports: {', '.join(map(str, data.get('ports', [])))}\n"
        output += f"  Summary: {data.get('summary').strip()}\n\n"
else:
    output += "Nenhuma vulnerabilidade encontrada.\n"

output += "=" * 40 + "\n"

# --- Exibição bonita no terminal ---
console.print(Panel(output, title=f"Shodan Recon - {IP}", border_style="green"))

# --- Salvar ---
with open(f"{IP}_shodan_recon.txt", "w") as f:
    f.write(output)

console.print(f"[bold green]\n[+] Recon salvo em: {IP}_shodan_recon.txt")
