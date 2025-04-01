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
HEADERS = {"User-Agent": "Mozilla/5.0 (ReconBot)"}

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
general_table = soup.select("h1#general + table tr")

for row in general_table:
    cols = row.find_all("td")
    if len(cols) == 2:
        key = cols[0].get_text(strip=True)
        value = cols[1].get_text(strip=True)
        general_info[key] = value

output += "[General Info]\n"
for k, v in general_info.items():
    output += f"{k}: {v}\n"
output += "\n"

# --- Domains ---
domains = []
for a in soup.select("td a.button"):
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

# --- Vulnerabilities (detalhado) ---
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
