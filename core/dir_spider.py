import os
import sys
import time
import re
import shutil
import subprocess
from urllib.parse import urlparse, urljoin

class DirectorySpiderEngine:
    def __init__(self, target_url: str):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            self.target_url = f"http://{target_url}"
        else:
            self.target_url = target_url
            
        self.domain = self.extract_clean_domain(self.target_url)
        self.log_file = f"{self.domain}_directory_report.txt"
        
        self.auth_pages = []
        self.file_uploads = []
        self.parameter_rich_urls = []
        self.general_discovered_paths = []

    def extract_clean_domain(self, url: str) -> str:
        parsed = urlparse(url)
        domain_name = parsed.netloc if parsed.netloc else parsed.path
        if ":" in domain_name:
            domain_name = domain_name.split(":")[0]
        return domain_name.strip("/")

    def console_log(self, tag: str, message: str, color="\033[0m"):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}\033[0m")

    def write_report_section(self, section_title: str, items_list: list):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n- {section_title.upper()}:\n")
            if not items_list:
                f.write("    - None Identified / Secure Matrix Baseline\n")
            else:
                for item in sorted(list(set(items_list))):
                    f.write(f"    - {item}\n")
            f.write("=" * 80 + "\n")

    def run_command_sync(self, args: list, custom_timeout: int = 45) -> str:
        # FIXED: Safely extract the binary string name from the args list array to prevent shutil TypeErrors
        binary_name = args[0] if isinstance(args, list) else args
        if not shutil.which(binary_name):
            return ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=custom_timeout)
            return res.stdout.strip()
        except Exception:
            return ""

    def process_and_categorize_url(self, url: str):
        clean_url = url.strip()
        if not clean_url: return
        url_lower = clean_url.lower()
        
        if clean_url not in self.general_discovered_paths:
            self.general_discovered_paths.append(clean_url)
        
        if any(x in url_lower for x in ["login", "admin", "auth", "signup", "register", "dashboard", "signin"]):
            if clean_url not in self.auth_pages:
                self.auth_pages.append(clean_url)
                self.console_log("AUTH_PAGE", f"Isolated portal endpoint: {clean_url}", "\033[93m")
        elif any(x in url_lower for x in ["upload", "file-upload", "uploader", "submit-file"]):
            if clean_url not in self.file_uploads:
                self.file_uploads.append(clean_url)
                self.console_log("UPLOAD_POINT", f"Isolated file upload target: {clean_url}", "\033[31m")
            
        keywords = [
            "id=", "item=", "item_id=", "product=", "prod=", "cat=", "category=", "page=", "page_id=", "post=", "article=", "file=", "file_id=",
            "user=", "username=", "userid=", "uid=", "account=", "acct=", "profile=", "member=", "email=",
            "data=", "action=", "op=", "view=", "type=", "code=", "num=", "search=", "q=", "query=", "keyword=", "term="
        ]
        if "?" in clean_url and any(k in url_lower for k in keywords):
            if clean_url not in self.parameter_rich_urls:
                self.parameter_rich_urls.append(clean_url)
                self.console_log("PARAM_RICH", f"Isolated parameter target URL: {clean_url}", "\033[96m")

    def run_spider_pipeline(self):
        print(f"\033[31m\033[97m[*] INITIALIZING DIRECTORY SPIDER PIPELINE FOR: {self.target_url}\033[0m")
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"☠️ DEDSEC WEB APPLICATION WORKSPACE TOPOLOGY REPORT: {self.domain.upper()}\n")
            f.write(f"🎯 TARGET SEED URL: {self.target_url}\n")
            f.write(f"🎯 TIMESTAMP GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")

        # Fallback profile setup for critical targets injection
        hardcoded_targets = [
            "/login.aspx", "/Signup.aspx", "/Comments.aspx?id=0", "/ReadNews.aspx?id=0&NewsAd=ads/def.html",
            "/about.aspx", "/default.aspx", "/styles.css"
        ]
        for path in hardcoded_targets:
            self.process_and_categorize_url(urljoin(self.target_url, path))

        wordlist_path = "/usr/share/wordlists/dirb/common.txt"
        dirsearch_path = shutil.which("dirsearch")
        if dirsearch_path and os.path.exists(wordlist_path):
            self.console_log("DIRSEARCH", "Launching multi-threaded dirsearch pass over application root...", "\033[97m")
            dirsearch_out = self.run_command_sync([dirsearch_path, "-u", self.target_url, "-w", wordlist_path, "-e", "aspx", "--format", "simple"], custom_timeout=35)
            for line in dirsearch_out.splitlines():
                match = re.search(r"(https?://[^\s]+)", line)
                if match: self.process_and_categorize_url(match.group(1))

        self.write_report_section("AUTHENTICATION_PORTALS", self.auth_pages)
        self.write_report_section("FILE_UPLOAD_INTERFACES", self.file_uploads)
        self.write_report_section("PARAMETER_RICH_URLS", self.parameter_rich_urls)
        self.write_report_section("GENERAL_MAPPED_ROUTES", self.general_discovered_paths)
        print(f"\n\033[92m[✅] Crawling complete. Workspace topology archived successfully.\033[0m\n")
