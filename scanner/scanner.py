import subprocess, json, datetime, os

SAVE_PATH = "/home/subhikshah/Cybertwin/scanner/scan_results.json"

def scan_network(target):
    print(f"Scanning {target}...")
    result = subprocess.run(["nmap", "-sV", "-oG", "-", target], capture_output=True, text=True)
    return result.stdout

def parse_results(raw):
    hosts = []
    for line in raw.splitlines():
        if "Host:" in line and "Ports:" in line:
            ip = line.split("Host: ")[1].split(" ")[0]
            open_ports = []
            for p in line.split("Ports: ")[1].split(", "):
                f = p.split("/")
                if len(f) >= 5 and f[1] == "open":
                    open_ports.append({"port": f[0], "service": f[4]})
            hosts.append({"ip": ip, "ports": open_ports})
    return hosts

def run_scan(target):
    raw = scan_network(target)
    hosts = parse_results(raw)
    record = {"timestamp": datetime.datetime.now().isoformat(), "target": target, "hosts": hosts}
    with open(SAVE_PATH, "w") as f:
        json.dump(record, f, indent=2)
    print(f"Found {len(hosts)} hosts. Saved to {SAVE_PATH}")
    return record

if __name__ == "__main__":
    run_scan("192.168.100.10")
