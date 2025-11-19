from scapy.all import sniff, get_if_addr, get_if_list
import ipaddress

# List of target IPs to track
target_ips = [
    "192.168.137.12", # abhinav
    "192.168.137.33", # sanchay
    "192.168.137.179" # shreya
]
# removing any spaces/blank
target_ips = [ip.strip() for ip in target_ips]


# Detect Hotspot Interface

def get_hotspot_iface():
    '''   '''
    # Taking sample IP to determine network subnet
    sample_ip = ipaddress.ip_network(target_ips[0] + "/24", strict=False)
    
    # Iterate through all available network interfaces 
    for iface in get_if_list():
        try:
            # Get the IP address assigned to the current interface 
            ip = get_if_addr(iface)
            # Check if this interface's IP address falls within the defined sample network range
            if ipaddress.ip_address(ip) in sample_ip:
                # If a match is found, return the name of the network interface (e.g., 'Ethernet 2')
                return iface
        except:
            pass
    return None
 


# Bandwidth Monitor Using IP Layer
def get_bandwidth_usage(duration=1):
    # dictionary to store sent/received bytes for each IP
    usage = {ip: {"sent": 0, "received": 0} for ip in target_ips}

    def monitor_packet(packet):
        # Check if the packet contains an IP layer
        if packet.haslayer("IP"):
            src = packet["IP"].src  # Source IP address
            dst = packet["IP"].dst  # Destination IP address
            size = len(packet)      # Packet size in bytes

            # Compare packet's src/dst IP with each target IP
            for ip in target_ips:
                # If the packet is sent FROM a target device
                if src == ip:
                    usage[ip]["sent"] += size
                # If the packet is sent TO the target device
                elif dst == ip:
                    usage[ip]["received"] += size

    # Detect the correct network interface (Wi-Fi/Hotspot)
    iface = get_hotspot_iface()
    if iface is None:
        print("Hotspot interface not found.")
        return usage  # Return empty usage if interface not found

    # Start capturing packets for the duration (default = 1 second)
    sniff(prn=monitor_packet, iface=iface, timeout=duration, store=False)

    # Return the final bandwidth usage info for all IPs
    return usage

def get_bandwidth_data(duration=1):
    # Get raw bandwidth data 
    raw = get_bandwidth_usage(duration)

    result = {}

    # Process each IP and convert raw bytes into readable KB values
    for ip, stats in raw.items():
        sent = stats["sent"]              # Bytes sent by the IP
        received = stats["received"]      # Bytes received by the IP
        total = (sent + received) / 1024  # Total KB used in this duration

        # Store clean structured result for the Streamlit app
        result[ip] = {
            "sent_bytes": sent,
            "received_bytes": received,
            "total_kb": total
        }

    # Return final per-IP bandwidth stats
    return result
