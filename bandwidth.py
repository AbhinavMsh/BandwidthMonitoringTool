from scapy.all import sniff, get_if_addr, get_if_list
import ipaddress

# List of target IPs to track
target_ips = [
    "192.168.137.12", # abhinav
    "192.168.137.33"
    # "192.168.137.202",
]
target_ips = [ip.strip() for ip in target_ips]


# Detect Hotspot Interface
def get_hotspot_iface():
    # pick first IP
    sample_ip = ipaddress.ip_network(target_ips[0] + "/24", strict=False)

    for iface in get_if_list():
        try:
            ip = get_if_addr(iface)
            if ipaddress.ip_address(ip) in sample_ip:
                return iface
        except:
            pass
    return None


# Bandwidth Monitor Using IP Layer
def get_bandwidth_usage(duration=1):
    usage = {ip: {"sent": 0, "received": 0} for ip in target_ips}

    def monitor_packet(packet):
        if packet.haslayer("IP"):
            src = packet["IP"].src
            dst = packet["IP"].dst
            size = len(packet)

            for ip in target_ips:
                if src == ip:
                    usage[ip]["sent"] += size
                elif dst == ip:
                    usage[ip]["received"] += size

    iface = get_hotspot_iface()
    if iface is None:
        print("Hotspot interface not found.")
        return usage

    sniff(prn=monitor_packet, iface=iface, timeout=duration, store=False)
    return usage


# Streamlit-Friendly Wrapper
def get_bandwidth_data(duration=1):
    raw = get_bandwidth_usage(duration)

    result = {}
    total_sent = 0
    total_received = 0

    for ip, stats in raw.items():
        sent = stats["sent"]
        received = stats["received"]
        total = (sent + received) / 1024  # KB

        result[ip] = {
            "sent_bytes": sent,
            "received_bytes": received,
            "total_kb": total
        }

        total_sent += sent
        total_received += received

    result["TOTAL"] = {
        "sent_bytes": total_sent,
        "received_bytes": total_received,
        "total_kb": (total_sent + total_received) / 1024
    }

    return result
