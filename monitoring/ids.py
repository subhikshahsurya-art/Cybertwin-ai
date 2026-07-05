import subprocess, json, os, datetime

ALERTS_FILE = os.path.expanduser("~/Cybertwin/monitoring/alerts.json")
alerts = []

def save_alert(message, severity):
    alert = {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "severity": severity
    }
    alerts.append(alert)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts[-100:], f, indent=2)
    print(f"[{severity}] {message}")

def detect(line):
    if "SYN" in line and "192.168.100.20" in line:
        save_alert("SYN packet from attacker 192.168.100.20", "HIGH")
    if "ARP" in line:
        save_alert("ARP packet detected - possible MITM attack", "CRITICAL")
    if ".22 " in line:
        save_alert("SSH connection attempt detected", "MEDIUM")
    if ".80 " in line:
        save_alert("HTTP traffic detected on port 80", "LOW")

def start_ids():
    print("CyberTwin IDS started - monitoring network...")
    p = subprocess.Popen(
        ["/usr/bin/tcpdump", "-i", "enp0s8", "-l", "-n"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    for line in p.stdout:
        detect(line)

start_ids()
