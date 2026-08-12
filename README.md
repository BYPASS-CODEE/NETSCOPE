<!-- ══════════════════════════════ NETSCOPE X ══════════════════════════════ -->

```
╔══════════════════════════════════════════════════════════════════════════╗
║ ███╗   ██╗███████╗████████╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗ ║
║ ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝  ║
║ ██╔██╗ ██║█████╗     ██║   ███████╗██║   ██║██████╔╝██████╔╝█████╗   ║
║ ██║╚██╗██║██╔══╝     ██║   ╚════██║██║   ██║██╔═══╝ ██╔═══╝ ██╔══╝   ║
║ ██║ ╚████║███████╗   ██║   ███████║╚██████╔╝██║     ██║     ███████╗ ║
║ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝ ║
╚══════════════════════════════════════════════════════════════════════════╝
```

<p align="center">
  <b style="color:#00E5FF;font-family:monospace;">ADVANCED LAN INTELLIGENCE · TERMINAL DISCOVERY DASHBOARD</b><br/>
  <sub>One file · No C2 · No bloat — Know your network before it knows you.</sub>
</p>

<div align="center">

<img src="https://img.shields.io/badge/PYTHON-3.8%2B-7D4698?style=for-the-badge&logo=python&logoColor=00E5FF&labelColor=0D0D0D" />
<img src="https://img.shields.io/badge/RICH_TUI-00E5FF?style=for-the-badge&logo=python&logoColor=000000&labelColor=0D0D0D" />
<img src="https://img.shields.io/badge/WINDOWS_FIRST-15E0C5?style=for-the-badge&logo=windows&logoColor=00E5FF&labelColor=0D0D0D" />
<img src="https://img.shields.io/badge/SINGLE_FILE-003B57?style=for-the-badge&logo=github&logoColor=00E5FF&labelColor=0D0D0D" />
<img src="https://img.shields.io/badge/TCP_CONNECT-2CA5E0?style=for-the-badge&logo=socketdotio&logoColor=00E5FF&labelColor=0D0D0D" />
<img src="https://img.shields.io/badge/LICENSE-MIT-00E5FF?style=for-the-badge&labelColor=0D0D0D" />

</div>

<br/>

```
┌──(root@netscope)-[~]───────────────────────────────────────────────┐
│ cat /etc/netscope/about                                            │
└────────────────────────────────────────────────────────────────────┘
```

<table>
<tr>
<td width="55%" valign="top">

```yaml
system:
  name:      "NETSCOPE_X"
  version:   "2.0"
  role:      "LAN discovery & network diagnostics"
  engine:    "ARP cache + ICMP + TCP connect"
  interface: "Rich-powered terminal UI"
  platform:  "Windows-first · Linux/macOS compatible"
  scope:     "local IPv4 /24 only"
  deps:      "python 3.8+ · rich"

executes:
  - discovery — passive ARP parse + ICMP reachability sweep
  - port scan — 26 common TCP services (conservative connect scan)
  - vendor    — OUI fingerprint lookup (44 prefixes / 17 vendors)
  - hostname  — reverse-DNS hints where available
  - classify  — device type estimation (8 categories)
  - export    — timestamped JSON report to disk

creed:
  "know your network before it knows you."

[ STATUS ]: ONLINE — DASHBOARD v2.0 / ENGINE v2.0
```

</td>
<td width="45%" valign="top">

```
        ┌─────────────────────┐
        │       INTERNET      │
        └──────────┬──────────┘
             ┌─────┴─────┐
        ┌────┴────┐  ┌───┴─────┐
        │ GATEWAY │  │  Wi-Fi  │
        │ .1.1    │  │    AP   │
        └────┬────┘  └───┬─────┘
       ┌─────┼───────────┼─────┐
   ┌───┴──┐ ┌┴────┐ ┌────┴─┐ ┌─┴───┐
   │  PC  │ │PHONE│ │  NAS │ │ PRN │
   │ .100 │ │ .104│ │  .10 │ │ .50 │
   └──────┘ └─────┘ └──────┘ └─────┘

  ┌─[ SCAN STATE ]─────────┐
  │ /24    SWEEP    DONE   │
  │ ARP    CACHE    PARSED │
  │ PORTS  ENGINE   READY  │
  │ EXPORT ARMED     ✓     │
  └────────────────────────┘
```

</td>
</tr>
</table>

---

<div align="center">

### ⟨ ./features --list ⟩

</div>

| ⟦ capability ⟧ | ⟦ details ⟧ |
|:--|:--|
| 🖥 **Live Discovery** | full local /24 ICMP reachability sweep with 64 concurrent workers |
| 📡 **ARP Intelligence** | parses the OS ARP cache (`arp -a`) to map IPs → MACs instantly, zero packets sent |
| 🏭 **Vendor Fingerprint** | OUI lookup table — Apple · Samsung · Xiaomi · Huawei · TP-Link · Cisco · Intel · VMware · VirtualBox · Raspberry Pi … |
| 🚪 **Port Engine** | conservative TCP connect scan of 26 common ports (SSH, HTTP, SMB, RDP, VNC, MQTT, ADB …) with 280 ms per-port timeout |
| 🧭 **Device Classification** | estimates device type from vendor + hostname: iOS, Android, Windows PC, macOS, Printer, Network device, Linux SBC |
| ⏱ **Latency Meter** | per-device ping RTT in milliseconds, refreshed on every scan |
| 📊 **Live Dashboard** | Rich TUI: network status · device inventory · port results · device intelligence · control center |
| 📤 **JSON Export** | one-key full report → `netscope_report_<timestamp>.json` |
| 🔁 **Auto-Refresh** | re-scan anytime from the menu; all results persist in the session |
| 🪶 **Zero-Intrusion** | no authentication, no exploitation, no packet capture, no file access, no credential collection |

---

<div align="center">

### ⟨ ./dashboard_preview --ascii ⟩

</div>

> No screenshots needed — the whole UI is ASCII. This is exactly what you get:

```text
┌─ NETWORK STATUS ──────────────────────────────────────────────────┐
│ INTERFACE    Wi-Fi / active IPv4                                  │
│ LOCAL IP     192.168.1.100                                        │
│ GATEWAY      192.168.1.1                                          │
│ NETWORK      192.168.1.0/24                                       │
│ DEVICES      14                                                   │
│ LAST SCAN    15:30:42                                             │
└───────────────────────────────────────────────────────────────────┘
┌─ LIVE DEVICE INVENTORY ──────────────────────────────────────────┐
│ #  STATUS    IP             MAC           VENDOR    TYPE          │
│ 1  ● ONLINE  192.168.1.1    D8:BB:2C:..   Samsung   Network device│
│ 2  ● ONLINE  192.168.1.100  3C:5A:37:..   Google    THIS PC       │
│ 3  ● ONLINE  192.168.1.104  F4:F5:D8:..   Apple     iOS / Apple   │
│ 4  ● ONLINE  192.168.1.105  AC:84:C6:..   Xiaomi    Android       │
│ 5  ● ONLINE  192.168.1.50   B8:27:EB:..   Raspberry Linux SBC     │
└───────────────────────────────────────────────────────────────────┘
┌─ CONTROL CENTER ─────────────────────────────────────────────────┐
│ [1] Discover   [2] Select/Scan   [3] Details                     │
│ [4] Refresh    [5] Export JSON   [Q] Quit                        │
└───────────────────────────────────────────────────────────────────┘
```

---

<div align="center">

### ⟨ ./quick_start --guide ⟩

</div>

```bash
# ── 1) Install the only dependency ──────────────────────────
pip install rich

# ── 2) Run ──────────────────────────────────────────────────
python netscope_x.py          # Windows
python3 netscope_x.py         # Linux / macOS

# ── 3) Optional: standalone .exe with PyInstaller ──────────
pip install pyinstaller
pyinstaller --onefile --console --name netscope_x netscope_x.py
```

```bash
# ── Typical workflow ────────────────────────────────────────
# 1. launch            → banner + authorized-use notice
# 2. auto-sweep /24    → ARP + ICMP, devices appear live
# 3. [2] select device → TCP port scan (26 common ports)
# 4. [3] details       → vendor, hostname, latency, ports
# 5. [5] export        → full JSON report to disk
```

---

<div align="center">

### ⟨ ./dashboard_commands --help ⟩

</div>

> Run the tool and use the Control Center menu — `py netscope_x.py`

| key | action |
|:--|:--|
| `1` | **Discover** — run a full /24 sweep (ARP + ICMP) |
| `2` | **Select/Scan** — pick a device, then TCP-scan its common ports |
| `3` | **Details** — full intelligence panel for any device |
| `4` | **Refresh** — re-run the whole discovery |
| `5` | **Export** — dump everything to `netscope_report_<timestamp>.json` |
| `Q` | **Quit** — clean exit |

---

<div align="center">

### ⟨ ./how_it_works --pipeline ⟩

</div>

```text
┌──────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────────┐
│  arp -a  │──►│  MAC → OUI   │──►│  classify    │──►│  dashboard  │
└──────────┘   └──────────────┘   └──────────────┘   └─────────────┘
┌──────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────────┐
│ ICMP 64x │──►│  alive hosts │──►│  reverse DNS │   │  JSON out   │
└──────────┘   └──────────────┘   └──────────────┘   └─────────────┘
```

1. **Parse ARP cache** — reads the OS ARP table for instant IP ↔ MAC mapping (passive, no packets sent).
2. **ICMP sweep** — pings every host in the /24 with 64 workers; only reachable hosts move forward.
3. **Reverse DNS** — asks the resolver for hostname hints (only where available).
4. **OUI lookup** — extracts the first 6 hex digits of the MAC and looks up the manufacturer.
5. **Classify** — combines vendor + hostname heuristics to guess the device type.
6. **Port engine** *(on demand)* — TCP connect scan of 26 common ports, 64 workers, 280 ms timeout.
7. **Export** — serializes the full session to a timestamped JSON file.

---

<div align="center">

### ⟨ ./modules --list ⟩

</div>

| ⟦ module ⟧ | ⟦ delivers ⟧ |
|:--|:--|
| `discovery engine` | ARP cache parse + ICMP reachability sweep + latency measurement |
| `port engine` | 26 common TCP services · 64-thread connect scan |
| `vendor engine` | OUI fingerprint database → manufacturer lookup |
| `classifier` | device-type estimation from vendor + hostname |
| `dashboard` | Rich panels: network status · inventory · ports · intelligence · control center |
| `exporter` | timestamped JSON report (`netscope_report_*.json`) |

---

<div align="center">

### ⟨ ./report --sample.json ⟩

</div>

```json
{
  "tool": "NETSCOPE X",
  "version": "2.0",
  "timestamp": "2026-08-12T15:30:42",
  "local_ip": "192.168.1.100",
  "gateway": "192.168.1.1",
  "network": "192.168.1.0/24",
  "devices": [
    {
      "ip": "192.168.1.1",
      "mac": "D8:BB:2C:11:22:33",
      "vendor": "Samsung",
      "hostname": "gateway.home",
      "kind": "Network device",
      "role": "GATEWAY",
      "status": "ONLINE",
      "ports": [80, 443],
      "services": ["80/HTTP", "443/HTTPS"],
      "latency_ms": 1.2
    },
    {
      "ip": "192.168.1.104",
      "mac": "F4:F5:D8:AA:BB:CC",
      "vendor": "Apple",
      "hostname": "iphone.local",
      "kind": "iOS / Apple",
      "role": "HOST",
      "status": "ONLINE",
      "ports": [],
      "services": [],
      "latency_ms": 8.7
    }
  ]
}
```

---

<div align="center">

### ⟨ ./security --notes ⟩

</div>

| ⟦ aspect ⟧ | ⟦ detail ⟧ |
|:--|:--|
| 🕊 **Passive by default** | ARP cache reading sends zero packets; the sweep uses only standard ICMP echo |
| 🚪 **Connect scan only** | plain TCP `connect()` — no SYN flood, no fragmentation, no evasion |
| 🎯 **/24 only** | the tool refuses to leave the local IPv4 /24 |
| 🧊 **No auth / no exploit** | no credentials, no payloads, no code execution on targets |
| ⚠️ **Known limits** | ARP cache may be incomplete; some hosts drop ICMP; OUI map covers 17 vendors; hostnames need working reverse DNS |
| 📝 **Traces** | port scans are visible in target logs — stay inside your authorized scope |

---

<div align="center">

```diff
@@ ./usage_policy.sh @@

+ scan networks you own or are explicitly authorized to test
+ identify open services and close misconfigurations
+ export clean JSON reports for documentation and audits
- scan networks without permission
- touch third-party infrastructure outside your scope
- forget that port scans leave traces — stay in scope
```

</div>

---

<div align="center">

### ⟨ ./project --tree ⟩

</div>

```text
netscope-x/
├── netscope_x.py            # the entire tool — single file
├── README.md                # you are here
└── netscope_report_*.json   # generated scan reports (runtime)
```

---

<div align="center">

### ⟨ ./system_monitor ⟩

</div>

```text
┌─ SYSTEM MONITOR ─────────────────────────────────────────────────┐
│  session       active · since 15:30:42                           │
│  network       192.168.1.0/24 · gateway 192.168.1.1              │
│  devices       14 discovered · 26 common ports each              │
│  reports       3 exported · JSON format                          │
│  dependencies  python 3.8+ · rich only                           │
│  footprint     passive ARP + ICMP · no packets forged            │
└──────────────────────────────────────────────────────────────────┘
```

---

<div align="center">

### ⟨ ./contributing --guide ⟩

</div>

PRs, bug reports and ideas are welcome. Keep the single-file spirit alive:

- minimal dependencies — Rich is the only requirement
- conservative, non-intrusive scanning only
- Windows-first with graceful fallbacks on Linux/macOS
- document every new feature in the README

---

<div align="center">

### ⟨ ./github --setup ⟩

</div>

| field | value |
|:--|:--|
| **Repository name** | `NETSCOPE-X` |
| **Description** | Advanced terminal LAN discovery dashboard — ARP + ICMP /24 sweep, vendor fingerprinting, TCP port scan, live Rich TUI. Authorized networks only. |
| **Topics** | `python` · `network-scanner` · `lan-discovery` · `arp` · `network-diagnostics` · `rich-terminal` · `cybersecurity` · `port-scan` · `recon` · `tui` |

---

<div align="center">

### ⟨ ./connect --all ⟩

</div>

<div align="center">

<a href="https://t.me/your_handle"><img src="https://img.shields.io/badge/TELEGRAM-00E5FF?style=for-the-badge&logo=telegram&logoColor=black&label=CHANNEL&labelColor=0D0D0D" /></a>
<a href="https://github.com/your-username"><img src="https://img.shields.io/badge/GITHUB-0D0D0D?style=for-the-badge&logo=github&logoColor=00E5FF" /></a>
<a href="https://www.youtube.com/@your-channel"><img src="https://img.shields.io/badge/YOUTUBE-0D0D0D?style=for-the-badge&logo=youtube&logoColor=FF0000" /></a>
<a href="https://www.instagram.com/your_handle/"><img src="https://img.shields.io/badge/INSTAGRAM-0D0D0D?style=for-the-badge&logo=instagram&logoColor=E4405F" /></a>

</div>

<sub align="center">Replace the placeholder links above with your own profiles before publishing.</sub>

---

<div align="center">

<sub>NETSCOPE X v2.0 — MIT License · Use responsibly, on networks you own or are authorized to test.</sub>

</div>