#!/usr/bin/env python3
import os
import sys
import time
from urllib.parse import urlparse

# Strict administrative enforcement gate check configuration
if os.getuid() != 0:
    print("\n\033[31m\033[1m[!] DEDSEC PRIVILEGE ERROR: This framework requires low-level kernel socket access.")
    print("[!] Please escalate to root permissions using: 'sudo python3 main.py'\033[0m\n")
    sys.exit(1)

try:
    from core.on import PassiveReconEngine
    from core.active_scan import ActiveScanEngine
    from core.tech_fingerprint import TechFingerprintEngine
    from core.dir_spider import DirectorySpiderEngine
    from core.vuln_scanner import VulnerabilityScannerEngine
    from core.ssl_auditor import SslAuditorEngine
    from core.report_aggregator import ReportAggregatorEngine
except ImportError as e:
    print(f"\033[31m[!] Architectural Error: Missing core pipeline script component ({str(e)})\033[0m")
    sys.exit(1)

# Terminal ANSI Color Escape Constants (Crimson DedSec Theme)
C_RED   = "\033[31m"
C_BOLD  = "\033[1m"
C_CYAN  = "\033[96m"
C_GREEN = "\033[92m"
C_YEL   = "\033[93m"
C_WHITE = "\033[97m"
C_RESET = "\033[0m"

class WebSlamXOrchestrator:
    def __init__(self):
        self.target_url = ""
        self.domain = ""
        self.scheme = ""

    def render_crimson_skull_canvas(self):
        os.system("clear")
        print(f"{C_RED}{C_BOLD}")
        print(r"                              @@@@@         @@@@@@@@@         ")
        print(r"                             @@@@@@@      @@@@@@@@@@@ @@@@@@@@@@@@             ")
        print(r"                           @@@@@@@@@@@@  @@@@@@ @@@@@ @@@@@@@@@@@@@  @@@@      ")
        print(r"  @@@@          @@@@@@@@@@ @@@@@@@@@@@@@ @@@@@@ @@@@  @@@@@%   @@@ @@@@@@@@@   ")
        print(r"@@@@@@@@@    @@@@@@@@@@@@@ #@@@@@@@@@@@@ @@@@@@      @@@@@@@     @@@@@@@@@@@@@ ")
        print(r"@@@@@@@@@@   @@@@@@@@@@@@  @@@@@  @@@@@ #&&&&&&&&    @@@@@@@@@@ @@@@@@ @@@@@@@@")
        print(r" @@@@@@@@@@   @@@@@@@@@@@@  @@@@@  @@@@@ #&&&&&&&&   @@@@@@@@@@ @@@@@   @@@@@@@")
        print(r"  @@@@@@@@@@&  @@@@@@@@@    @@@@&  &&&&&  &&&&&&&&% &&&&&&&&@  &@@@@    @@@@@@@")
        print(r"   @@@@  %@&&&  @@@&&&       &&&&&  &&&&    &&&&&&& &&&&      &&&&@     (@@@@# ")
        print(r"    @@@&   &&&&  &&&&&.      &&&&&  &&&&      %%%% %&&&      &&&&              ")
        print(r"     &&&&   &&&%  &&%%%%%%%%  %%%%  %%%% /%%   %%% %%%%%%%  %&&& &&&&&&        ")
        print(r"      &&&&   %%%#  %%%%%%%%#  %%%%  %%%% %%%%%%%%% %%%%%%% %%%%&&&&&&          ")
        print(r"       %%%%   %%%   %######   ##### #### ########  ##%%%%  %%%%%%%&            ")
        print(r"        %%%%   ###  #####      #### #### (######             %%%%               ")
        print(r"         %###  ####  #((((     ((((((((/   (##                                  ")
        print(r"          ####  #(((  (((( (((( ((((((                                         ")
        print(r"           ##(( ((((   ((////// (((                                            ")
        print(r"            ((((((((/   ///////                                               ")
        print(r"             ((((((//    ///                                                   ")
        print(r"              ///////                                          ")
        print(r"               ////")
        print("                ☠️  [ P R O D U C E D   B Y   D E D S E C ]  ☠️")
        print("                [     AUTOMATED BY DEVELOPER: Unknownx007    ]")
        print(f"{C_RED}================================================================================{C_RESET}")

    def parse_and_validate_target(self, user_input: str) -> bool:
        clean_input = user_input.strip()
        if not clean_input: return False
        if not clean_input.startswith("http://") and not clean_input.startswith("https://"):
            clean_input = f"http://{clean_input}"
        try:
            parsed = urlparse(clean_input)
            self.target_url = clean_input
            self.scheme = parsed.scheme
            self.domain = parsed.netloc
            if ":" in self.domain:
                self.domain = self.domain.split(":")[0]
            return True
        except Exception:
            return False

    def initialize_orchestrator(self):
        self.render_crimson_skull_canvas()
        user_url = input("[+] Enter Target Assessment Website URL: ").strip()
        if not self.parse_and_validate_target(user_url):
            print(f"\n{C_RED}[!] Configuration Error: Invalid target URL template.\033[0m\n")
            return

        self.render_crimson_skull_canvas()
        print(f"{C_CYAN}[*] TARGET PROFILE ROUTE LOCKED : {self.target_url}")
        print(f"[*] RESOLVED BOUNDARY DOMAIN   : {self.domain}")
        print(f"[*] ASSIGNED CONNECTION MODE   : ROOT ENFORCED (Low-Level Kernel Access)")
        print(f"{C_RED}================================================================================{C_RESET}\n")
        time.sleep(1.0)

        # Phase 1: Passive Reconnaissance
        print(f"{C_WHITE}[✦] INITIATING PHASE 1: PASSIVE INTELLIGENCE HARVESTING...{C_RESET}")
        passive_engine = PassiveReconEngine(self.target_url)
        passive_engine.run_passive_pipeline()
        print("-" * 80)

        # Phase 2: Active Port Scan
        print(f"{C_WHITE}[✦] INITIATING PHASE 2: ACTIVE PERIMETER PORT SCANNING...{C_RESET}")
        active = ActiveScanEngine(self.target_url)
        active.run_active_pipeline()
        print("-" * 80)

        # Phase 3: Tech Fingerprinting
        print(f"{C_WHITE}[✦] INITIATING PHASE 3: APPLICATION TECHNOLOGY FINGERPRINTING...{C_RESET}")
        tech = TechFingerprintEngine(self.target_url)
        tech.run_tech_pipeline()
        print("-" * 80)

        # Phase 4: Directory Spidering
        print(f"{C_WHITE}[✦] INITIATING PHASE 4: RECURSIVE WORKSPACE PATH SPIDER...{C_RESET}")
        spider = DirectorySpiderEngine(self.target_url)
        spider.run_spider_pipeline()
        print("-" * 80)

        # Phase 5: Hardcore Scanner Module
        print(f"{C_WHITE}[✦] INITIATING PHASE 5: HARDCORE VULNERABILITY EXPLOITATION...{C_RESET}")
        vuln = VulnerabilityScannerEngine(self.target_url, active.service_banners, spider.parameter_rich_urls)
        vuln.run_vulnerability_pipeline()
        print("-" * 80)

        # Phase 6: SSL/TLS Auditor
        print(f"{C_WHITE}[✦] INITIATING PHASE 6: SSL/TLS CIPHER & TRANSPORT LAYER AUDIT...{C_RESET}")
        ssl = SslAuditorEngine(self.target_url)
        ssl.run_ssl_pipeline()
        print("-" * 80)

        # Phase 7: Forensic Master Aggregator
        print(f"{C_WHITE}[✦] INITIATING PHASE 7: FORENSIC DATA CONSOLIDATION AGGREGATION...{C_RESET}")
        aggregator = ReportAggregatorEngine(self.domain)
        aggregator.run_aggregator_pipeline()

        print(f"{C_RED}================================================================================{C_RESET}")
        print(f"{C_GREEN}[✅] CASCADING PIPELINE COMPLETE! SINGLE AGGREGATED REPORT COMPILED NATIVELY:{C_RESET}")
        print(f"{C_GREEN}    └── Markdown Dashboard : {self.domain}_final_report.md{C_RESET}")
        print(f"{C_RED}================================================================================{C_RESET}\n")

if __name__ == "__main__":
    try:
        WebSlamXOrchestrator().initialize_orchestrator()
    except KeyboardInterrupt:
        print(f"\n\033[31m[!] Execution aborted safely by operator.\033[0m\n")
