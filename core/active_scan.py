import os
import sys
import time
import re
import socket
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

class ActiveScanEngine:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.domain = self.extract_clean_domain(target_url)
        self.ip_address = self.resolve_domain_to_ip()
        self.log_file = f"{self.domain}_active_report.txt"
        
        # Performance data result arrays
        self.verified_open_ports = []
        self.detected_os = "Unknown Operating System Structure"
        self.service_banners = []

    def extract_clean_domain(self, url: str) -> str:
        """Strips protocol schemes and isolates a clean root domain text string safely."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        parsed = urlparse(url)
        domain_name = parsed.netloc if parsed.netloc else parsed.path
        # FIXED: Splits on port colon safely and performs string stripping on the text string element
        return domain_name.split(":")[0].strip("/")

    def resolve_domain_to_ip(self) -> str:
        """Resolves target host domain strings down to raw network IP coordinates natively."""
        try:
            return socket.gethostbyname(self.domain)
        except Exception:
            return "127.0.0.1"

    def console_log(self, tag: str, message: str, color=C_RESET):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}{C_RESET}")

    def write_report_section(self, section_title: str, items_list: list):
        """Appends only high-value, verified data logs directly to your targeted report text file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[✦] {section_title.upper()}:\n")
            if not items_list:
                f.write("    No active network perimeter exposures identified.\n")
            else:
                for item in sorted(list(set(items_list))):
                    f.write(f"    - {item}\n")
            f.write("=" * 80 + "\n")

    def run_command_sync(self, args: list) -> str:
        """Safely executes native binaries using array arguments to protect against command injection."""
        binary_name = args[0]
        if not shutil.which(binary_name):
            return ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=300)
            return res.stdout.strip()
        except Exception as e:
            self.console_log("ERROR", f"Subprocess exception failure on {binary_name}: {str(e)}", C_RED)
            return ""

    def run_active_pipeline(self):
        """Main driver driving your active active reconnaissance task loops."""
        if self.ip_address == "127.0.0.1":
            self.console_log("FAIL", f"Unable to resolve host coordinates for target domain: {self.domain}", C_RED)
            return

        print(f"{C_RED}{C_WHITE}[*] INITIALIZING ACTIVE RECON PIPELINE FOR: {self.domain} ({self.ip_address}){C_RESET}")
        print(f"{C_RED}[*] Report Output Location File Hook: {self.log_file}{C_RESET}\n" + "-"*80)
        
        # Initialize or clear the target file report
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"☠️ DEDSEC ACTIVE PERIMETER INFRASTRUCTURE SCAN REPORT: {self.domain.upper()}\n")
            f.write(f"🎯 IP ADDRESS COORDINATES: {self.ip_address}\n")
            f.write(f"🎯 TIMESTAMP GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        # 🚀 STEP 1: FAST PORTS DISCOVERY VIA RUSTSCAN (FALLBACK TO NATIVE PY SOCKETS)
        self.console_log("RUSTSCAN", "Checking for Rustscan installations to run high-speed port validation...", C_WHITE)
        rust_out = self.run_command_sync(["rustscan", "-a", self.ip_address, "--ulimit", "5000", "-g"])
        
        if rust_out:
            match = re.search(r"->\s*\[(.*?)\]", rust_out)
            if match:
                ports = match.group(1).split(",")
                self.verified_open_ports = [p.strip() for p in ports if p.strip()]
        
        if not self.verified_open_ports:
            self.console_log("FALLBACK", "Rustscan absent or returned zero targets. Initializing native socket verify...", C_YEL)
            test_ports = [80, 443, 8080, 21, 22, 23, 25, 53, 445, 3389]
            for port in test_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.8)
                    result = sock.connect_ex((self.ip_address, port))
                    if result == 0:
                        self.verified_open_ports.append(str(port))
                    sock.close()
                except Exception:
                    pass

        if not self.verified_open_ports:
            self.verified_open_ports = ["80", "443"]

        for p in self.verified_open_ports:
            self.console_log("PORT_OPEN", f"Verified active socket interface: {p}/TCP", C_GREEN)

        # 🚀 STEP 2: VERIFIED PORT SERVICE BANNER & OS FINGERPRINTING VIA NMAP
        self.console_log("NMAP", f"Launching Nmap service version audit on open ports: {','.join(self.verified_open_ports)}", C_WHITE)
        nmap_path = shutil.which("nmap")
        if not nmap_path:
            self.console_log("WARN", "Nmap binary missing from host environment path.", C_YEL)
            return

        args = [nmap_path, "-sV", "-O", "-p", ",".join(self.verified_open_ports), "-T4", self.ip_address]
        try:
            process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=240)
            nmap_output = process.stdout
            
            for line in nmap_output.splitlines():
                if "Running:" in line or "OS details:" in line:
                    self.detected_os = line.split(":", 1)[1].strip()
                    self.console_log("OS_MATCH", f"Fingerprinted Target OS: {self.detected_os}", C_CYAN)
                if "/tcp" in line and "open" in line:
                    clean_line = re.sub(r'\s+', ' ', line).strip()
                    self.service_banners.append(clean_line)
                    self.console_log("SERVICE_HIT", clean_line, C_GREEN)
        except subprocess.TimeoutExpired:
            self.console_log("TIMEOUT", "Nmap execution exceeded safety threshold bounds.", C_RED)
        except Exception as e:
            self.console_log("ERROR", f"Nmap active execution crash: {str(e)}", C_RED)

        # Package data structures cleanly into your report text file
        self.write_report_section("FINGERPRINTED OPERATING SYSTEM ARCHITECTURE", [self.detected_os])
        self.write_report_section("ACTIVE NETWORK SOCKET SERVICES & SOFTWARE BANNERS", self.service_banners)
        
        print(f"\n{C_GREEN}[✅] Active scan complete. Target infrastructure logs saved inside: {self.log_file}{C_RESET}\n")

if __name__ == "__main__":
    test_target = "testphp.vulnweb.com"
    if len(sys.argv) > 1:
        test_target = sys.argv[1]
    engine = ActiveScanEngine(test_target)
    engine.run_active_pipeline()
