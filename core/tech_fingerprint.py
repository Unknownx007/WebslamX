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

class TechFingerprintEngine:
    def __init__(self, target_url: str):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            self.target_url = f"http://{target_url}"
        else:
            self.target_url = target_url
            
        self.domain = self.extract_clean_domain(self.target_url)
        self.log_file = f"{self.domain}_tech_report.txt"
        
        # Operational result trackers
        self.detected_cms = "None Detected (Custom Stack Architecture)"
        self.backend_languages = []
        self.web_frameworks = []
        self.is_wordpress = False

    def extract_clean_domain(self, url: str) -> str:
        parsed = urlparse(url)
        domain_name = parsed.netloc if parsed.netloc else parsed.path
        # FIXED: Splits on port colon safely and performs string stripping on the text string element
        return domain_name.split(":")[0].strip("/")

    def console_log(self, tag: str, message: str, color=C_RESET):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}{C_RESET}")

    def write_report_section(self, section_title: str, items_list: list):
        """Appends only high-value, verified data logs directly to your targeted report text file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[✦] {section_title.upper()}:\n")
            if not items_list:
                f.write("    No matching technological markers identified.\n")
            else:
                for item in sorted(list(set(items_list))):
                    f.write(f"    - {item}\n")
            f.write("=" * 80 + "\n")

    def run_command_sync(self, args: list) -> str:
        binary_name = args[0]
        if not shutil.which(binary_name):
            return ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=120)
            return res.stdout.strip()
        except Exception as e:
            self.console_log("ERROR", f"Subprocess exception failure on {binary_name}: {str(e)}", C_RED)
            return ""

    def run_tech_pipeline(self):
        """Main driver driving your web stack technology fingerprint task loops."""
        print(f"{C_RED}{C_WHITE}[*] INITIALIZING TECH FINGERPRINT PIPELINE FOR: {self.target_url}{C_RESET}")
        print(f"{C_RED}[*] Report Output Location File Hook: {self.log_file}{C_RESET}\n" + "-"*80)
        
        # Initialize or clear the target file report
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"☠️ DEDSEC WEB APPLICATION TECHNOLOGY PROFILE REPORT: {self.domain.upper()}\n")
            f.write(f"🎯 TARGET URL ROUTE: {self.target_url}\n")
            f.write(f"🎯 TIMESTAMP GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        # 🚀 STEP 1: WEB ENGINE & CONTENT ANALYSIS VIA NATIVE WHATWEB
        self.console_log("WHATWEB", "Parsing remote server application layers and response fields...", C_WHITE)
        whatweb_out = self.run_command_sync(["whatweb", "--color=never", "-v", self.target_url])
        
        if whatweb_out:
            for line in whatweb_out.splitlines():
                line_lower = line.lower()
                
                if "wordpress" in line_lower:
                    self.detected_cms = "WordPress CMS Core Platform"
                    self.is_wordpress = True
                    self.console_log("CMS_MATCH", self.detected_cms, C_BRED)
                elif "joomla" in line_lower:
                    self.detected_cms = "Joomla CMS Core Platform"
                    self.console_log("CMS_MATCH", self.detected_cms, C_YEL)
                    
                if "php" in line_lower and "php" not in self.backend_languages:
                    self.backend_languages.append("PHP Scripting Engine")
                    self.console_log("LANG_MATCH", "PHP Scripting Engine Found", C_GREEN)
                if "asp.net" in line_lower and "asp.net" not in self.backend_languages:
                    self.backend_languages.append("Microsoft ASP.NET Framework")
                    self.console_log("LANG_MATCH", "Microsoft ASP.NET Framework Found", C_GREEN)
                    
                framework_matches = ["jquery", "bootstrap", "react", "angular", "vue.js", "next.js"]
                for fm in framework_matches:
                    if fm in line_lower and fm not in self.web_frameworks:
                        self.web_frameworks.append(fm.upper())
                        self.console_log("FRAMEWORK_MATCH", f"Library / UI Component Found: {fm.upper()}", C_CYAN)

        # 🚀 STEP 2: CASCADING FALLBACK RECON THROUGH NATIVE SYSTEM SCRAPING
        if not self.backend_languages or not self.web_frameworks:
            self.console_log("FALLBACK", "WhatWeb logs empty or missing headers. Executing low-level HTTP signature checks...", C_YEL)
            try:
                import requests
                res = requests.get(self.target_url, timeout=5, verify=False)
                server_hdr = res.headers.get("Server", "").lower()
                powered_by = res.headers.get("X-Powered-By", "").lower()
                cookies_str = str(res.cookies.get_dict()).lower()
                
                if "php" in powered_by or "php" in server_hdr:
                    self.backend_languages.append("PHP Scripting Engine (Verified via Response Header)")
                if "asp" in powered_by or "aspnet" in cookies_str:
                    self.backend_languages.append("Microsoft ASP.NET Framework (Verified via Cookie Matrix)")
                if "wp-content" in res.text or "wp-includes" in res.text:
                    self.detected_cms = "WordPress CMS Core Platform (Verified via Response Content Code)"
                    self.is_wordpress = True
            except Exception:
                pass

        # Package data structures cleanly into your report text file
        self.write_report_section("IDENTIFIED CONTENT MANAGEMENT PLATFORM (CMS)", [self.detected_cms])
        self.write_report_section("SERVER-SIDE PROGRAMMING LANGUAGES & BACKENDS", self.backend_languages)
        self.write_report_section("CLIENT-SIDE JAVASCRIPT LIBRARIES & UI FRAMEWORKS", self.web_frameworks)
        
        # Log a compact structural parameter line for master orchestration use later
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n- IS_WORDPRESS={self.is_wordpress}\n")
            
        print(f"\n{C_GREEN}[✅] Fingerprinting complete. Application tech profile archived: {self.log_file}{C_RESET}\n")

if __name__ == "__main__":
    test_target = "testphp.vulnweb.com"
    if len(sys.argv) > 1:
        test_target = sys.argv
    engine = TechFingerprintEngine(test_target)
    engine.run_tech_pipeline()
