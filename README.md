# ☠️ WebSlamX: Advanced Multi-Stage Surface Reconnaissance & Exploitation Framework

```
                              @@@@@        @@@@@@@@@         
                             @@@@@@@      @@@@@@@@@@@ @@@@@@@@@@@@             
                           @@@@@@@@@@@@  @@@@@@ @@@@@ @@@@@@@@@@@@@  @@@@      
  @@@@          @@@@@@@@@@ @@@@@@@@@@@@@ @@@@@@ @@@@  @@@@@%   @@@ @@@@@@@@@   
@@@@@@@@@    @@@@@@@@@@@@@ #@@@@@@@@@@@@ @@@@@@      @@@@@@@     @@@@@@@@@@@@@ 
@@@@@@@@@@   @@@@@@@@@@@@  @@@@@  @@@@@ #&&&&&&&&    @@@@@@@@@@ @@@@@@ @@@@@@@@
 @@@@@@@@@@   @@@@@@@@@@@@  @@@@@  @@@@@ #&&&&&&&&   @@@@@@@@@@ @@@@@   @@@@@@@
  @@@@@@@@@@&  @@@@@@@@@    @@@@&  &&&&&  &&&&&&&&% &&&&&&&&@  &@@@@    @@@@@@@
   @@@@  %@&&&  @@@&&&       &&&&&  &&&&    &&&&&&& &&&&      &&&&@     (@@@@# 
    @@@&   &&&&  &&&&&.      &&&&&  &&&&      %%%% %&&&      &&&&              
     &&&&   &&&%  &&%%%%%%%%  %%%%  %%%% /%%   %%% %%%%%%%  %&&& &&&&&&        
      &&&&   %%%#  %%%%%%%%#  %%%%  %%%% %%%%%%%%% %%%%%%% %%%%&&&&&&          
       %%%%   %%%   %######   ##### #### ########  ##%%%%  %%%%%%%&            
        %%%%   ###  #####      #### #### (######             %%%%               
         %###  ####  #((((     ((((((((/   (##                                  
          ####  #(((  (((( (((( ((((((                                         
           ##(( ((((   ((////// (((                                            
            ((((((((/   ///////                                               
             ((((((//    ///                                                   
              ///////                                          
               ////
                ☠️  [ P R O D U C E D   B Y   D E D S E C ]  ☠️
                [     AUTOMATED BY DEVELOPER: Unknownx007     ]
```

# 📝 Description
WebSlamX is a high-performance, command-line multi-stage security auditing and passive intelligence ingestion framework engineered natively for Kali Linux setups. Built around an automated cascading event loop architecture, the pipeline orchestrates native binary subprocesses alongside custom multi-threaded Python verification modules. It bridges the gap between passive open-source intelligence gathering (OSINT) and intensive, browser-masked active vulnerability analysis.The framework automatically handles low-level system privilege verification, dynamic proxy-agent rotation to evade Web Application Firewalls (WAF), precise parameter-rich URL sifting, and unified forensic data aggregation. Rather than dumping raw, noisy text logs, WebSlamX sanitizes, removes duplicates, and consolidates all metrics into structured JSON databases and an executive Markdown vulnerability dashboard.

# ⚙️ Core Architectural Pipeline
WebSlamX drives your security assessment operations sequentially across 7 distinct operational phases:
1. **Phase 1:** Passive Intelligence HarvestingAggregates subdomain metrics, index registries, historic zone DNS intercepts, and exposed target user credentials via subfinder, amass, dnsrecon, and theHarvester.
2. **Phase 2:** Active Network Port ScanningPerforms high-speed port validation mapping via native low-level sockets with adaptive fallback to deep version banner probes via nmap.
3. **Phase 3:** Web Stack Technology FingerprintingQueries web server response metrics, security fields, and cookie signatures via whatweb and native response scraping routines.
4. **Phase 4:** Workspace Surface MappingDeploys dirsearch combined with multi-threaded dictionary checks over modern standard paths to filter dynamic variables, authentication gateways, and file uploads.
5. **Phase 5:** Automated Exploit Injection CoreActively queries parameter links using browser-masked desktop headers, running rapid single-quote error reflections alongside structured multi-threaded sqlmap and nikto passes.
6. **Phase 6:** Transport Encryption Cipher AuditEvaluates target cryptographic configurations for protocol anomalies (SSLv2/v3, TLS 1.0/1.1) and broken cipher arrays using testssl.sh and sslyze.
7. **Phase 7:** Forensic Master Aggregation EngineIngests all separate, temporary sub-module log streams, removes duplicate data, filters systemic telemetry noise, and generates machine-readable JSON states and Markdown dashboards.

## 🛠️ Installation & Dependency Configuration

```

1. Clone the Framework Treebash
git clone https://github.com/Unknownx007/WebslamX
cd WebslamX
2. Configure Native Kali System Tools
The framework requires a suite of backend auditing binaries. Run the automated deployment shell manifest as root to configure dependencies cleanly:
sudo chmod +x setup_dependencies.sh
sudo ./setup_dependencies.sh
3. Build Your Python Environment
Install the strict architectural extensions and environment models via pip:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# 🚀 Operational Workflow Instructions
Because the framework injects raw network packets and accesses kernel sockets for advanced OS fingerprinting and scanning procedures, it strictly requires root privileges (sudo) to execute.

```
sudo ./venv/bin/python3 main.py
```

# 📂 Output Reporting Architecture
Upon final execution, the system clears out temporary module scratch text sheets and provides two production-grade outputs:
**Markdown Dashboard (<domain>_final_report.md):**A beautiful, human-readable vulnerability assessment log card mapping threat classifications (Critical, High, Medium, Low) and clean, categorized application topology maps.
**Machine JSON State (<domain>_security_report.json):**A structured, raw JSON database tree recording target asset metadata node parameters for long-term storage or programmatic integration.

### ⚖️ Legal & Ethical Usage Notice
This software development repository card is built solely for authorized security auditing, defensive gap analysis, educational research, and infrastructure assessment compliance. Executing active scanning sequences against unauthorized production targets without explicit, written mutual contractual permission is strictly prohibited. The framework author assumes zero legal accountability for environmental system downtime or programmatic misuse.

## Issue:
If you have any issue you can create an issue at Issue :))



