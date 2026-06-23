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

class PassiveReconEngine:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.domain = self.extract_clean_domain(target_url)
        self.log_file = f"{self.domain}_passive_report.txt"
        
        # Data storage arrays
        self.discovered_subdomains = []
        self.historic_dns_records = []
        self.leaked_credentials = []

    def extract_clean_domain(self, url: str) -> str:
        """Strips protocol schemes and paths to isolate a clean root domain string."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        parsed = urlparse(url)
        domain_name = parsed.netloc if parsed.netloc else parsed.path
        return domain_name.split(":")[0].strip("/")

    def console_log(self, tag: str, message: str, color=C_RESET):
        """Prints live status tracks on your screen window."""
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}{C_RESET}")

    def write_report_section(self, section_title: str, items_list: list):
        """Appends structured, high-value data logs directly to your targeted report text file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[✦] {section_title.upper()}:\n")
            if not items_list:
                f.write("    No passive intelligence data discovered in public logs.\n")
            else:
                for item in sorted(list(set(items_list))):
                    f.write(f"    - {item}\n")
            f.write("=" * 80 + "\n")

    def run_command_sync(self, args: list) -> str:
        """Safely executes native binaries using array arguments to protect against command injection."""
        binary_name = args[0]
        if not shutil.which(binary_name):
            self.console_log("MISSING_TOOL", f"Kali binary '{binary_name}' is not available in system PATH.", C_YEL)
            return ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=180)
            return res.stdout.strip()
        except subprocess.TimeoutExpired:
            self.console_log("TIMEOUT", f"Subprocess loop expired for tool: {binary_name}", C_RED)
            return ""
        except Exception as e:
            self.console_log("ERROR", f"Subprocess failure on {binary_name}: {str(e)}", C_RED)
            return ""

    def run_passive_pipeline(self):
        """Main driver driving your passive background reconnaissance task loops."""
        print(f"{C_RED}{C_WHITE}[*] INITIALIZING PASSIVE AUDIT PIPELINE FOR TARGET: {self.domain}{C_RESET}")
        print(f"{C_RED}[*] Report Output Location File Hook: {self.log_file}{C_RESET}\n" + "-"*80)
        
        # Establish or clear the target file report
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"☠️ DEDSEC PASSIVE INTELLIGENCE FORENSIC RECONNAISSANCE REPORT: {self.domain.upper()}\n")
            f.write(f"🎯 TIMESTAMP GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        # 🚀 STEP 1: SUBDOMAINS HARVESTING VIA SUBFINDER
        self.console_log("SUBFINDER", "Harvesting passive subdomain records from public API caches...", C_WHITE)
        subfinder_out = self.run_command_sync(["subfinder", "-d", self.domain, "-silent"])
        for line in subfinder_out.splitlines():
            host = line.strip()
            if host:
                self.discovered_subdomains.append(host)
                self.console_log("SUB_HIT", f"Discovered passive node: {host}", C_GREEN)

        # 🚀 STEP 2: SURFACE MAPPING VIA AMASS PASSIVE ENUMERATION
        self.console_log("AMASS", "Running passive surface mapping layer against open index registries...", C_WHITE)
        amass_out = self.run_command_sync(["amass", "enum", "-passive", "-d", self.domain])
        for line in amass_out.splitlines():
            host = line.strip()
            if host and host not in self.discovered_subdomains:
                self.discovered_subdomains.append(host)
                self.console_log("SUB_HIT", f"Discovered passive node: {host}", C_GREEN)

        # 🚀 STEP 3: HISTORIC DNS RECORDS RETRIEVAL VIA DNSRECON
        self.console_log("DNSRECON", "Extracting historic zone details and name server layouts...", C_WHITE)
        dnsrecon_out = self.run_command_sync(["dnsrecon", "-d", self.domain, "-t", "std"])
        for line in dnsrecon_out.splitlines():
            if any(x in line.lower() for x in ["txt", "mx", "ns", "soa"]):
                clean_line = re.sub(r'\s+', ' ', line).strip()
                self.historic_dns_records.append(clean_line)
                self.console_log("DNS_HIT", clean_line, C_CYAN)

        # 🚀 STEP 4: DATA LEAK AND EMAIL SNOOPING VIA THEHARVESTER
        self.console_log("THEHARVESTER", "Searching leak repositories for associated user emails and keys...", C_WHITE)
        harvester_out = self.run_command_sync(["theHarvester", "-d", self.domain, "-b", "anonymouse,bing,duckduckgo", "-l", "200"])
        
        email_regex = re.compile(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9.\-_]+\.[a-zA-Z]{2,4}')
        for line in harvester_out.splitlines():
            found_emails = email_regex.findall(line)
            for email in found_emails:
                self.leaked_credentials.append(email)
                self.console_log("LEAK_HIT", f"Leaked identity target uncovered: {email}", C_YEL)

        # Package data structures cleanly into your report text file
        self.write_report_section("PASSIVELY HARVESTED SUBDOMAINS INFRASTRUCTURE", self.discovered_subdomains)
        self.write_report_section("HISTORIC ZONE DNS INTERCEPT RECORDS", self.historic_dns_records)
        self.write_report_section("PUBLICLY EXPOSED USER IDENTITIES & CREDENTIALS", self.leaked_credentials)
        
        print(f"\n{C_GREEN}[✅] Passive phase complete. Target intelligence archived cleanly into: {self.log_file}{C_RESET}\n")

if __name__ == "__main__":
    test_target = "vulnweb.com"
    if len(sys.argv) > 1:
        test_target = sys.argv[1]
    engine = PassiveReconEngine(test_target)
    engine.run_passive_pipeline()
