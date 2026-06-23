import os
import sys
import time
import re
import json

# Terminal ANSI Color Escape Constants (Crimson DedSec Theme)
C_RESET = "\033[0m"
C_RED   = "\033[31m"
C_GREEN = "\033[92m"
C_YEL   = "\033[93m"
C_CYAN  = "\033[96m"
C_WHITE = "\033[97m"

class ReportAggregatorEngine:
    def __init__(self, domain_input):
        # FIXED: Core logic explicitly extracts the string element at index position 1 out of sys.argv arrays
        if isinstance(domain_input, list):
            domain_str = domain_input[1] if len(domain_input) > 1 else "testphp.vulnweb.com"
        else:
            domain_str = str(domain_input)

        self.domain = domain_str.replace("http://", "").replace("https://", "").strip("/")
        self.json_out = f"{self.domain}_security_report.json"
        self.md_out = f"{self.domain}_final_report.md"
        
        self.master_report = {
            "assessment_metadata": {
                "target_domain": self.domain,
                "generation_timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "author": "Unknownx007"
            },
            "findings_by_severity": {
                "CRITICAL": [],
                "HIGH": [],
                "MEDIUM": [],
                "LOW": []
            },
            "mapped_surface_topology": {
                "authentication_portals": [],
                "file_upload_interfaces": [],
                "general_mapped_routes": []
            }
        }

    def console_log(self, tag: str, message: str, color=C_RESET):
        timestamp = time.strftime('%H:%M:%S')
        print(f"{color}[{timestamp}][{tag}] {message}{C_RESET}")

    def categorize_severity_by_keyword(self, text: str) -> str:
        t_low = text.lower()
        if any(x in t_low for x in ["sql injection", "sqli", "remote code", "command injection", "overflow", "blueprint match"]):
            return "CRITICAL"
        elif any(x in t_low for x in ["lfi", "file inclusion", "xss", "cross-site", "traversal", "vulnerability", "vulnerable"]):
            return "HIGH"
        elif any(x in t_low for x in ["missing security header", "suggested security header", "clickjacking", "csp", "hsts", "tls", "ip address found", "location header", "disclosed", "leak", "retrieved x-"]):
            return "MEDIUM"
        else:
            return "LOW"

    def harvest_individual_module_files(self):
        self.console_log("HARVEST", f"Parsing sub-module scratch logs for target domain: {self.domain}...", C_WHITE)
        
        source_files = [
            f"{self.domain}_passive_report.txt",
            f"{self.domain}_active_report.txt",
            f"{self.domain}_tech_report.txt",
            f"{self.domain}_directory_report.txt",
            f"{self.domain}_vulnerability_report.txt",
            f"{self.domain}_ssl_report.txt"
        ]

        current_section = ""
        for filename in source_files:
            if not os.path.exists(filename):
                continue
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        line_clean = line.strip()
                        if not line_clean:
                            continue
                            
                        if line_clean.startswith("- ") and (line_clean.endswith(":") or "PORTALS" in line_clean or "INTERFACES" in line_clean or "URLS" in line_clean or "ROUTES" in line_clean):
                            current_section = line_clean.replace("- ", "").replace(":", "").strip().upper()
                            continue
                        elif "REPORT:" in line_clean or "=================" in line_clean:
                            continue
                            
                        if line_clean.startswith("- "):
                            data_payload = line_clean.replace("- ", "").strip()
                        else:
                            data_payload = line_clean
                            
                        if not data_payload or "none identified" in data_payload.lower() or "secure matrix" in data_payload.lower() or "baseline" in data_payload.lower():
                            continue
                        if any(x in data_payload for x in ["☠️", "🎯", "✦", "========", "TIMESTAMP", "TARGET"]):
                            continue
                        if any(x in data_payload.lower() for x in ["scan terminated", "end time:", "start time:", "1 host(s) tested", "items reported"]):
                            continue
                            
                        if data_payload.startswith("http://") or data_payload.startswith("https://"):
                            if "AUTHENTICATION" in current_section or "PORTALS" in current_section:
                                self.master_report["mapped_surface_topology"]["authentication_portals"].append(data_payload)
                            elif "UPLOAD" in current_section or "INTERFACES" in current_section:
                                self.master_report["mapped_surface_topology"]["file_upload_interfaces"].append(data_payload)
                            else:
                                self.master_report["mapped_surface_topology"]["general_mapped_routes"].append(data_payload)
                        else:
                            severity = self.categorize_severity_by_keyword(data_payload)
                            if data_payload not in self.master_report["findings_by_severity"][severity]:
                                self.master_report["findings_by_severity"][severity].append(data_payload)
            except Exception as e:
                self.console_log("FAIL", f"Error reading log file {filename}: {str(e)}", C_RED)

        # Enforce unique sets across lists
        for key in self.master_report["mapped_surface_topology"].keys():
            self.master_report["mapped_surface_topology"][key] = list(set(self.master_report["mapped_surface_topology"][key]))

    def compile_reports_to_disk(self):
        self.console_log("AGGREGATOR", "Wiping duplicate anomalies and generating master files...", C_WHITE)
        
        with open(self.json_out, "w", encoding="utf-8") as f:
            json.dump(self.master_report, f, indent=4)

        md_content = f"""# ☠️ DEDSEC ADVANCED AUDIT SURFACE RECONNAISSANCE REPORT
## TARGET ANALYSIS DOMAIN: `{self.domain.upper()}`
- **Assessment Generation Time** : {self.master_report['assessment_metadata']['generation_timestamp']}
- **Lead Penetration Tester Signature** : {self.master_report['assessment_metadata']['author']}

## 📊 THREAT SEVERITY SUMMARY MATRIX
"""
        severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        colors_map = {"CRITICAL": "🔴 CRITICAL EXPOSURE", "HIGH": "🟠 HIGH RISK", "MEDIUM": "🟡 MEDIUM CONFIG", "LOW": "🔵 LOW TRACK"}
        
        for sev in severities:
            md_content += f"\n### {colors_map[sev]} ({len(self.master_report['findings_by_severity'][sev])} Items Discovered)\n"
            findings_list = self.master_report["findings_by_severity"][sev]
            if not findings_list:
                md_content += "- Zero active vulnerabilities matched inside this classification layer.\n"
            else:
                for finding in findings_list:
                    md_content += f"- {finding}\n"

        md_content += f"\n## 📂 EXTRACTED APPLICATION SURFACE TOPOLOGY MAP\n"
        
        md_content += f"\n### 🔐 IDENTIFIED AUTHENTICATION PORTALS & ACCESS CHANNELS ({len(self.master_report['mapped_surface_topology']['authentication_portals'])} Links Mapped)\n"
        if not self.master_report["mapped_surface_topology"]["authentication_portals"]:
            md_content += "- No external portal gateways were mapped to active results registers.\n"
        else:
            for url in sorted(self.master_report["mapped_surface_topology"]["authentication_portals"]):
                md_content += f"- `{url}`\n"

        md_content += f"\n### 📤 DISCOVERED FILE UPLOAD INTERFACES & ENTRY FIELD PANELS ({len(self.master_report['mapped_surface_topology']['file_upload_interfaces'])} Links Mapped)\n"
        if not self.master_report["mapped_surface_topology"]["file_upload_interfaces"]:
            md_content += "- No input file submission entry lines matched this target category.\n"
        else:
            for url in sorted(self.master_report["mapped_surface_topology"]["file_upload_interfaces"]):
                md_content += f"- `{url}`\n"

        md_content += f"\n### 🌐 GENERAL SYSTEM MAP PATHS & WEB ASSETS ({len(self.master_report['mapped_surface_topology']['general_mapped_routes'])} Links Mapped)\n"
        if not self.master_report["mapped_surface_topology"]["general_mapped_routes"]:
            md_content += "- General map lists sit at baseline metrics.\n"
        else:
            for url in sorted(self.master_report["mapped_surface_topology"]["general_mapped_routes"]):
                md_content += f"- `{url}`\n"

        with open(self.md_out, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"\n{C_GREEN}[✅] Master aggregation complete! Complete data nodes written successfully:{C_RESET}")
        print(f"    └── Machine JSON State : {os.path.abspath(self.json_out)}")
        print(f"    └── Markdown Dashboard : {os.path.abspath(self.md_out)}\n")

    def run_aggregator_pipeline(self):
        self.harvest_individual_module_files()
        self.compile_reports_to_disk()

if __name__ == "__main__":
    engine = ReportAggregatorEngine(sys.argv)
    engine.run_aggregator_pipeline()
