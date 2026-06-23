#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo -e "\033[31m[!] Please execute the installer as root: sudo ./setup_dependencies.sh\033[0m"
  exit 1
fi

echo -e "\033[96m[*] Synchronizing system repositories and configuring tools...\033[0m"
apt-get update -y

# Install all background binaries mapped to the framework core
apt-get install -y nmap subfinder amass feroxbuster gobuster testssl.sh sslyze python3-pip

echo -e "\033[92m[✅] System tool setups finalized successfully!\033[0m"
