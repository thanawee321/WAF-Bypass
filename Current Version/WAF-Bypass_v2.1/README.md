# WAF-Bypass

![Banner](https://img.shields.io/badge/Version-1.8-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.x-yellow)

**Developer:** [BabyH@ck](https://www.facebook.com/thanawee321)  
**YouTube:** [BabyHackSenior](https://www.youtube.com/@BabyHackSenior)

---
## 🤨 What is tool

This tool is designed to discover the real IP address hidden behind a WAF (Web Application Firewall) by using a brute-force subdomain enumeration technique to uncover hidden domains.
In addition, it can also retrieve DNS history to identify where the target web server or host was previously registered and which service providers it has been associated with. 

## 📌 Overview

**BYPASS_WAF_APPLICATION** is a tool for:

- Detecting whether a website is protected by **WAF (Web Application Firewall)**  
- Checking web server information  
- Extracting **SSL certificate** information  
- Viewing **historical IP addresses** of a domain via `viewdns.info` and `securitytrails.com`  
- Scanning and finding **subdomains** with SSL analysis  
- Supporting **wordlists** for subdomain enumeration  

This tool is suitable for Bug Bounty hunters, Pentesters, and Security Researchers.

---
## ⚡ Features

- Detect **WAF type** and status  
- Detect **web server** type  
- Extract **SSL certificate information** (CN, Issuer, Serial Number, Validity)  
- Retrieve **historical IP addresses**  
  - via `viewdns.info`  
  - via `securitytrails.com` API  
- Subdomain enumeration with **SSL analysis**  
- Supports **custom wordlists** or download the latest wordlists from GitHub  

---
## 🚀 What's New update Version 2.1

- Added multithreaded input handling
- Implemented stop event mechanism for threads
- Optimized overall performance
- Fixed bugs with color and text rendering
- Display status codes for non-200 HTTP responses
- Improved logic: subdomain scanning works even if WAF detection fails
- Fixed custom wordlist update issue

## 🛠 Installation
Run with a single command-line argument: the target domain you want to analyze.
   ```
   git clone https://thanawee321/WAF-Bypass.git
   ```
   ```
   cd WAF-Bypass
   ```
   ```
   sudo chmod +x install.sh
   ```
   ```
   ./install.sh
   ```
   ```
   bypasswaf -t domainname.com
   ```

If you have API key of Securitytrails you can setting follow up below cmd command
   ```
   bypasswaf -s <your_API_key>
   ```

If setup threading setting follow up below cmd command
   ```
   bypasswaf -T <num_thread> (Ex. bypasswaf -T 100)
   ```


