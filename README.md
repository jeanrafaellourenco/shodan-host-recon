# shodan-host-recon

**Shodan host Recon** é um script em Python para coleta rápida e estruturada de informações públicas sobre um host utilizando scraping da página de detalhes do [Shodan](https://www.shodan.io/host/37.59.174.225) (não utiliza API).

O script extrai automaticamente:
- Informações gerais (ISP, localização, sistema operacional, etc.)
- Domínios associados
- Tecnologias web detectadas
- Vulnerabilidades (com detalhes como CVSS, portas e resumo)

O output é salvo em um arquivo `.txt` organizado e também exibido de forma bonita no terminal com cores.

---

## 🚀 Instalação

Clone este repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

**Requisitos:**
- Python 3.x
- requests
- beautifulsoup4
- rich

Ou instale direto:

```bash
pip install requests beautifulsoup4 rich
```

---

## ⚙️ Uso

Você pode passar o IP diretamente como argumento:

```bash
python3 shodan_recon.py 37.59.174.225
```

Ou, se não passar, ele perguntará:

```bash
$ python3 shodan_recon.py
Digite o IP: 37.59.174.225
```

---

## 📄 Exemplo de Saída

No terminal:

```
========================================
[General Info]
Organization: OVH SAS
Operating System: Linux 4.x
Location: Gravelines, France

[Domains]
ip-37-59-174.eu

[Web Technologies]
jQuery
Modernizr
Backstretch

[Vulnerabilities]
CVE-2024-40898
  CVSS: 7.5
  Ports: 80
  Summary: SSRF in Apache HTTP Server on Windows with mod_rewrite...

CVE-2023-31122
  CVSS: 7.5
  Ports: 80
  Summary: Out-of-bounds Read vulnerability in mod_macro...

========================================
[+] Recon salvo em: 37.59.174.225_shodan_recon.txt
```

---

## 🟢 O que este script faz (por baixo dos panos)
- Acessa a página pública do Shodan de um host.
- Faz scraping com **BeautifulSoup**.
- Busca campos relevantes no HTML e no JavaScript embutido (`const VULNS`).
- Organiza e salva a saída de forma legível.

---

## ⚠️ Avisos
- Este script faz scraping da página pública, então pode ser afetado por mudanças na estrutura do Shodan.
- Respeite o rate-limit do Shodan. Não abuse.

---
