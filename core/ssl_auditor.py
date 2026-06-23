import os
import sys
import time
import re
import shutil
import subprocess
from urllib.parse import urlparse

# Terminal ANSI Color Escape Constants (Crimson DedSec Theme)
C_RESET = "\033[0m"
C_RED   = "\033[31m"
C_GREEN = "\033[92m"
C_YEL   = "\033[93m"
C_CYAN  = "\033[96m"
C_WHITE = "\033[97m"

class SslAuditorEngine:
    def __init__(self, target_url: str):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            self.target_url = f"https://{target_url}"
        else:
            self.target_url = target_url
            
        self.domain = self.extract_clean_domain(self.target_url)
        self.log_file = f"{self.domain}_ssl_report.txt"
        self.transport_findings = []

    def extract_clean_domain(self, url: str) -> str:
        parsed = urlparse(url)
        domain_name = parsed.netloc if parsed.netloc else parsed.path
        if ":" in domain_name:
            domain_name = domain_name.split(":")[0]
        return domain_name.strip("/")

    def console_log(self, tag: str, message: str, color=C_RESET):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}{C_RESET}")

    def write_report_section(self, section_title: str, items_list: list):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n- {section_title.upper()}:\n")
            if not items_list:
                f.write("    None identified. Transport layer configurations match secure baselines.\n")
            else:
                for item in sorted(list(set(items_list))):
                    f.write(f"    - {item}\n")
            f.write("=" * 80 + "\n")

    def run_command_sync(self, args: list) -> str:
        # FIXED: Extracting the first element string from args to prevent shutil TypeErrors
        binary_name = args[0]
        if not shutil.which(binary_name):
            return ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=45)
            return res.stdout.strip()
        except Exception as e:
            self.console_log("ERROR", f"Subprocess exception failure on {binary_name}: {str(e)}", C_RED)
            return ""

    def run_ssl_pipeline(self):
        print(f"{C_RED}{C_WHITE}[*] INITIALIZING TRANSPORT LAYER ENCRYPTION AUDIT FOR: {self.domain}{C_RESET}")
        print(f"{C_RED}[*] Report Output Location File Hook: {self.log_file}{C_RESET}\n" + "-"*80)
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"☠️ DEDSEC SSL/TLS ENCRYPTION STACK & CIPHER FORENSIC REPORT: {self.domain.upper()}\n")
            f.write(f"🎯 TARGET DOMAIN: {self.domain}\n")
            f.write(f"🎯 TIMESTAMP GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        self.console_log("TESTSSL", "Evaluating target socket for broken protocols and cipher vulnerabilities...", C_WHITE)
        testssl_out = self.run_command_sync(["testssl.sh", "--quiet", "--color", "0", "-p", "-p", self.domain])
        
        if testssl_out:
            for line in testssl_out.splitlines():
                line_lower = line.lower()
                if any(x in line_lower for x in ["vulnerable", "offered", "not ok"]) and any(p in line_lower for p in ["sslv2", "sslv3", "tls1.0", "tls1.1"]):
                    clean_line = re.sub(r'\s+', ' ', line).strip()
                    self.transport_findings.append(f"[Protocol Exposure] {clean_line}")
                    self.console_log("PROTOCOL_ALERT", clean_line, C_RED)
                elif "rc4" in line_lower or "null cipher" in line_lower or "sweet32" in line_lower:
                    clean_line = re.sub(r'\s+', ' ', line).strip()
                    self.transport_findings.append(f"[Cipher Exposure] {clean_line}")
                    self.console_log("CIPHER_ALERT", clean_line, C_YEL)

        if not self.transport_findings:
            self.console_log("SSLYZE", "Deploying sslyze scanner fallback task modules...", C_WHITE)
            sslyze_out = self.run_command_sync(["sslyze", self.domain])
            if sslyze_out:
                for line in sslyze_out.splitlines():
                    if "VULNERABLE" in line or "ACCEPTED" in line and any(p in line for p in ["SSLv2", "SSLv3", "TLS 1.0", "TLS 1.1"]):
                        clean_line = line.strip()
                        self.transport_findings.append(f"[Fallback Threat] {clean_line}")
                        self.console_log("PROTOCOL_ALERT", clean_line, C_RED)

        if not self.transport_findings and self.target_url.startswith("https://"):
            self.console_log("SOCKET_CHECK", "Running native SSL context probes...", C_YEL)
            try:
                import ssl
                import socket
                context = ssl.create_default_context()
                context.minimum_version = ssl.TLSVersion.TLSv1
                with socket.create_connection((self.domain, 443), timeout=3) as sock:
                    with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                        self.console_log("INFO", f"Negotiated Connection Protocol: {ssock.version()}", C_GREEN)
            except Exception:
                pass

        self.write_report_section("TRANSPORT LAYER SECURITY (SSL/TLS) AUDIT FINDINGS", self.transport_findings)
        print(f"\n{C_GREEN}[✅] SSL/TLS evaluation complete. Transport configuration logs archived: {self.log_file}{C_RESET}\n")
