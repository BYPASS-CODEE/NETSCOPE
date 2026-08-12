"""
NETSCOPE X — Advanced terminal LAN discovery dashboard
Single-file, Windows-first, authorized-network diagnostics.

Install:
    py -m pip install rich

Run:
    py netscope_x.py

Notes:
- Discovery is limited to the local IPv4 /24.
- It uses passive ARP cache + ICMP reachability + optional mDNS/hostname
  hints where available.
- Port inspection is a conservative TCP connect scan of common ports.
- No authentication, exploitation, packet interception, credential capture,
  file access, or traffic manipulation is performed.
"""

from __future__ import annotations
import concurrent.futures
import datetime as dt
import ipaddress
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from rich import box
    from rich.console import Console, Group
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TaskProgressColumn, TimeRemainingColumn
    )
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("NETSCOPE X requires Rich.")
    print("Install: py -m pip install rich")
    raise SystemExit(1)

APP = "NETSCOPE X"
VERSION = "2.0"
IS_WINDOWS = platform.system().lower() == "windows"
console = Console()

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NETBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 515: "LPD", 631: "IPP",
    1433: "MSSQL", 1883: "MQTT", 3306: "MYSQL", 3389: "RDP",
    5000: "HTTP-ALT", 5353: "MDNS", 5555: "ADB", 5900: "VNC",
    8000: "HTTP-ALT", 8080: "HTTP-ALT", 8443: "HTTPS-ALT",
    9000: "HTTP-ALT",
}

# A small local OUI map. Unknown is displayed rather than guessed.
OUI = {
    "001A11": "Google",
    "3C5A37": "Google",
    "F4F5D8": "Apple",
    "A4C361": "Apple",
    "3C22FB": "Apple",
    "D8BB2C": "Samsung",
    "B0EC8F": "Samsung",
    "001A2B": "Samsung",
    "A4EBD8": "Samsung",
    "8C8590": "Xiaomi",
    "64CC2E": "Xiaomi",
    "AC84C6": "Xiaomi",
    "E8DB84": "Huawei",
    "00259E": "Huawei",
    "001E64": "Huawei",
    "B827EB": "Raspberry Pi",
    "DC4A3E": "Raspberry Pi",
    "00005E": "IANA/Virtual",
    "001C42": "Parallels",
    "000C29": "VMware",
    "005056": "VMware",
    "080027": "VirtualBox",
    "00155D": "Microsoft Hyper-V",
    "001DD8": "Microsoft",
    "3C7C3F": "Microsoft",
    "B44BD2": "Microsoft",
    "F8E43B": "Microsoft",
    "001C23": "Intel",
    "3C970E": "Intel",
    "F4CE46": "Intel",
    "001B21": "Intel",
    "001F3B": "Intel",
    "001D0F": "Atheros",
    "001A79": "Sony",
    "001C62": "Sony",
    "0021E9": "Sony",
    "0026E2": "Sony",
    "001E52": "Cisco",
    "001C58": "Cisco",
    "0026CB": "Cisco",
    "001E68": "TP-Link",
    "C46E1F": "TP-Link",
    "50C7BF": "TP-Link",
    "E4D332": "TP-Link",
}

@dataclass
class Device:
    ip: str
    mac: str = "—"
    vendor: str = "Unknown"
    hostname: str = "—"
    kind: str = "Unknown"
    status: str = "ONLINE"
    ports: list[int] | None = None
    services: list[str] | None = None
    latency_ms: float | None = None
    role: str = "HOST"

    def __post_init__(self):
        if self.ports is None:
            self.ports = []
        if self.services is None:
            self.services = []

def clear():
    os.system("cls" if IS_WINDOWS else "clear")

def sh(cmd, timeout=5):
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, errors="replace",
            timeout=timeout, shell=False
        )
        return p.stdout + p.stderr
    except Exception:
        return ""

def banner():
    t = Text()
    t.append("╔════════════════════════════════════════════════════════════════════════════╗\n", "bright_cyan")
    t.append("║ ", "bright_cyan")
    t.append("███╗   ██╗███████╗████████╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗", "bold bright_white")
    t.append(" ║\n", "bright_cyan")
    t.append("║ ", "bright_cyan")
    t.append("████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝", "bold bright_white")
    t.append(" ║\n", "bright_cyan")
    t.append("║ ", "bright_cyan")
    t.append("██╔██╗ ██║█████╗     ██║   ███████╗██║   ██║██████╔╝██████╔╝█████╗  ", "bold bright_white")
    t.append(" ║\n", "bright_cyan")
    t.append("║ ", "bright_cyan")
    t.append("██║╚██╗██║██╔══╝     ██║   ╚════██║██║   ██║██╔═══╝ ██╔═══╝ ██╔══╝  ", "bold bright_white")
    t.append(" ║\n", "bright_cyan")
    t.append("║ ", "bright_cyan")
    t.append("██║ ╚████║███████╗   ██║   ███████║╚██████╔╝██║     ██║     ███████╗", "bold bright_white")
    t.append(" ║\n", "bright_cyan")
    t.append("╚════════════════════════════════════════════════════════════════════════════╝", "bright_cyan")
    return Panel(t, subtitle=f"[bright_black]ADVANCED LAN INTELLIGENCE • v{VERSION}[/bright_black]",
                 border_style="bright_cyan")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_gateway():
    if IS_WINDOWS:
        out = sh(["ipconfig"])
        for m in re.finditer(r"Default Gateway[ .]*:\s*([0-9.]+)", out):
            if m.group(1) and not m.group(1).startswith("0."):
                return m.group(1)
    else:
        m = re.search(r"default via ([0-9.]+)", sh(["ip", "route"]))
        if m:
            return m.group(1)
    return "Unknown"

def get_network(local_ip):
    try:
        return ipaddress.ip_network(f"{local_ip}/24", strict=False)
    except Exception:
        return None

def arp_table():
    found = {}
    out = sh(["arp", "-a"], 8)
    for line in out.splitlines():
        m = re.search(
            r"(?P<ip>\d+\.\d+\.\d+\.\d+)\s+"
            r"(?P<mac>[0-9a-fA-F:-]{11,17})", line
        )
        if m:
            found[m.group("ip")] = m.group("mac").replace("-", ":").upper()
    return found

def vendor_from_mac(mac):
    key = re.sub(r"[^0-9A-Fa-f]", "", mac).upper()[:6]
    return OUI.get(key, "Unknown")

def ping_latency(ip):
    if IS_WINDOWS:
        out = sh(["ping", "-n", "1", "-w", "700", ip], 2)
        m = re.search(r"time[=<]\s*(\d+)\s*ms", out, re.I)
        if m:
            return float(m.group(1))
        return None
    out = sh(["ping", "-c", "1", "-W", "1", ip], 2)
    m = re.search(r"time[=<]?\s*([\d.]+)\s*ms", out, re.I)
    return float(m.group(1)) if m else None

def hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "—"

def classify(vendor, host):
    s = f"{vendor} {host}".lower()
    if any(x in s for x in ("iphone", "ipad", "apple")):
        return "iOS / Apple"
    if any(x in s for x in ("android", "samsung", "xiaomi", "huawei", "pixel", "oneplus")):
        return "Android"
    if any(x in s for x in ("desktop", "laptop", "windows", "microsoft")):
        return "Windows PC"
    if any(x in s for x in ("macbook", "imac", "macos")):
        return "macOS"
    if any(x in s for x in ("printer", "epson", "canon", "brother", "hp-")):
        return "Printer"
    if any(x in s for x in ("router", "gateway", "tp-link", "cisco")):
        return "Network device"
    if "raspberry" in s:
        return "Linux SBC"
    return "Unknown"

def discover(network, local_ip, gateway):
    cache = arp_table()
    candidates = [str(x) for x in network.hosts()]
    alive = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]DISCOVERY[/bold cyan]"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    ) as prog:
        task = prog.add_task("Checking local /24", total=len(candidates))

        def check(ip):
            if ip == local_ip or ip == gateway:
                return (ip, 0.0)
            t0 = time.perf_counter()
            lat = ping_latency(ip)
            return (ip, lat if lat is not None else None)

        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as ex:
            for ip, lat in ex.map(check, candidates):
                if ip == local_ip or ip == gateway or lat is not None:
                    alive.append((ip, lat))
                prog.advance(task)

    devices = []
    for ip, lat in sorted(alive, key=lambda x: tuple(map(int, x[0].split(".")))):
        mac = cache.get(ip, "—")
        vend = vendor_from_mac(mac)
        host = hostname(ip)
        role = "THIS PC" if ip == local_ip else ("GATEWAY" if ip == gateway else "HOST")
        devices.append(Device(
            ip=ip, mac=mac, vendor=vend, hostname=host,
            kind=classify(vend, host), latency_ms=lat, role=role
        ))
    return devices

def port_open(ip, port, timeout=.28):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def scan_ports(ip):
    open_ports = []
    ports = list(COMMON_PORTS)
    with Progress(
        SpinnerColumn(), TextColumn("[bold green]PORT ENGINE[/bold green]"),
        BarColumn(), TaskProgressColumn(), TimeRemainingColumn(),
        console=console, transient=True
    ) as prog:
        task = prog.add_task(f"Testing common TCP ports on {ip}", total=len(ports))
        def test(p):
            return p if port_open(ip, p) else None
        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as ex:
            for result in ex.map(test, ports):
                if result:
                    open_ports.append(result)
                prog.advance(task)
    return sorted(open_ports)

def service_list(ports):
    return [f"{p}/{COMMON_PORTS[p]}" for p in ports]

def status_panel(local_ip, gateway, network, devices, last_scan):
    t = Table.grid(expand=True)
    t.add_column(style="bright_black", width=16)
    t.add_column(style="bold white")
    t.add_row("INTERFACE", "Wi-Fi / active IPv4")
    t.add_row("LOCAL IP", local_ip)
    t.add_row("GATEWAY", gateway)
    t.add_row("NETWORK", str(network))
    t.add_row("DEVICES", str(len(devices)))
    t.add_row("LAST SCAN", last_scan)
    return Panel(t, title="[bold white]NETWORK STATUS[/bold white]", border_style="blue")

def devices_panel(devices, selected=None):
    table = Table(expand=True, box=box.SIMPLE_HEAVY, padding=(0, 1))
    table.add_column("#", width=4, justify="right", style="bright_black")
    table.add_column("STATUS", width=10)
    table.add_column("IP", style="bold white")
    table.add_column("MAC", style="bright_cyan")
    table.add_column("VENDOR", style="yellow")
    table.add_column("TYPE", style="magenta")
    table.add_column("HOSTNAME", style="green")
    table.add_column("ROLE", style="bright_blue")
    table.add_column("PING", justify="right")
    for i, d in enumerate(devices, 1):
        prefix = "❯ " if selected == i else "  "
        ping = f"{d.latency_ms:.0f}ms" if d.latency_ms is not None else "—"
        table.add_row(
            prefix + str(i), "[bold green]● ONLINE[/bold green]", d.ip, d.mac,
            d.vendor, d.kind, d.hostname, d.role, ping
        )
    if not devices:
        table.add_row("—", "[red]● NONE[/red]", "No hosts found", "—", "—", "—", "—", "—", "—")
    return Panel(table, title="[bold white]LIVE DEVICE INVENTORY[/bold white]",
                 border_style="bright_cyan")

def ports_panel(device):
    table = Table(expand=True, box=box.SIMPLE)
    table.add_column("PORT", justify="right", style="bold bright_cyan")
    table.add_column("STATE", style="green")
    table.add_column("SERVICE", style="yellow")
    for p in device.ports:
        table.add_row(str(p), "[bold green]OPEN[/bold green]", COMMON_PORTS.get(p, "unknown"))
    if not device.ports:
        table.add_row("—", "[green]NONE DETECTED[/green]", "No common TCP ports")
    return Panel(table, title=f"[bold white]PORTS • {device.ip}[/bold white]",
                 border_style="green")

def details_panel(d):
    grid = Table.grid(expand=True)
    grid.add_column(style="bright_black", width=18)
    grid.add_column(style="bold white")
    grid.add_row("IP", d.ip)
    grid.add_row("MAC", d.mac)
    grid.add_row("VENDOR", d.vendor)
    grid.add_row("DEVICE TYPE", d.kind)
    grid.add_row("HOSTNAME", d.hostname)
    grid.add_row("ROLE", d.role)
    grid.add_row("STATUS", "[green]ONLINE[/green]")
    grid.add_row("LATENCY", f"{d.latency_ms:.1f} ms" if d.latency_ms else "—")
    grid.add_row("OPEN PORTS", ", ".join(map(str, d.ports)) if d.ports else "None scanned")
    return Panel(grid, title="[bold white]DEVICE INTELLIGENCE[/bold white]",
                 border_style="magenta")

def controls():
    return Panel(
        "[bold cyan][1][/bold cyan] Discover   "
        "[bold cyan][2][/bold cyan] Select/Scan   "
        "[bold cyan][3][/bold cyan] Details   "
        "[bold cyan][4][/bold cyan] Refresh   "
        "[bold cyan][5][/bold cyan] Export JSON   "
        "[bold cyan][Q][/bold cyan] Quit",
        title="[bold white]CONTROL CENTER[/bold white]",
        border_style="bright_black"
    )

def notice():
    return Panel(
        "[bold yellow]AUTHORIZED USE ONLY[/bold yellow]  "
        "[bright_black]Local discovery + common TCP connect checks only. "
        "No authentication, exploitation, packet capture, file access, or credential collection.[/bright_black]",
        border_style="yellow"
    )

def choose(devices):
    if not devices:
        console.print("[red]No devices available.[/red]")
        return None
    console.print("\n[bold cyan]Select device number[/bold cyan]")
    for i, d in enumerate(devices, 1):
        console.print(f"  [bold]{i}[/bold]  {d.ip:<16} {d.kind:<16} {d.vendor}")
    try:
        n = int(console.input("[bold cyan]NETSCOPE> [/bold cyan]"))
        if 1 <= n <= len(devices):
            return devices[n - 1]
    except ValueError:
        pass
    console.print("[yellow]Invalid selection.[/yellow]")
    time.sleep(.6)
    return None

def export_json(devices, local_ip, gateway, network):
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path.cwd() / f"netscope_report_{stamp}.json"
    payload = {
        "tool": APP, "version": VERSION,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "local_ip": local_ip, "gateway": gateway, "network": str(network),
        "devices": [asdict(d) for d in devices],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path

def main():
    clear()
    console.print(banner())
    console.print(notice())

    local_ip = get_local_ip()
    gateway = get_gateway()
    network = get_network(local_ip)
    if not network:
        console.print("[red]Unable to determine local IPv4 network.[/red]")
        return

    console.print(
        f"\n[bright_black]Target:[/bright_black] [cyan]{network}[/cyan]   "
        f"[bright_black]Local:[/bright_black] [white]{local_ip}[/white]   "
        f"[bright_black]Gateway:[/bright_black] [magenta]{gateway}[/magenta]\n"
    )

    devices = discover(network, local_ip, gateway)
    last_scan = dt.datetime.now().strftime("%H:%M:%S")

    while True:
        clear()
        console.print(banner())
        console.print(status_panel(local_ip, gateway, network, devices, last_scan))
        console.print(devices_panel(devices))
        console.print(controls())
        choice = console.input("[bold cyan]NETSCOPE> [/bold cyan]").strip().lower()

        if choice == "q":
            clear()
            console.print(Panel(
                f"[bold bright_cyan]{APP}[/bold bright_cyan]\n"
                "[green]Session closed.[/green]",
                border_style="bright_cyan"
            ))
            return

        if choice in ("1", "4"):
            devices = discover(network, local_ip, gateway)
            last_scan = dt.datetime.now().strftime("%H:%M:%S")
            continue

        if choice in ("2", "3"):
            d = choose(devices)
            if not d:
                continue
            clear()
            console.print(banner())
            console.print(details_panel(d))
            if choice == "2":
                d.ports = scan_ports(d.ip)
                d.services = service_list(d.ports)
                console.print(ports_panel(d))
            console.input("\n[bright_black]Press Enter to return...[/bright_black]")
            continue

        if choice == "5":
            path = export_json(devices, local_ip, gateway, network)
            console.print(f"\n[bold green]Exported:[/bold green] {path}")
            time.sleep(1.2)
            continue

        console.print("[yellow]Use 1, 2, 3, 4, 5 or Q.[/yellow]")
        time.sleep(.7)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bright_black]Interrupted.[/bright_black]")