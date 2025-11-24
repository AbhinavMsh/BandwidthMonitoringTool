# Bandwidth Monitoring Tool

A real-time per-device bandwidth monitoring dashboard built using Python, Scapy, and Streamlit.  
This tool captures network packets on your hotspot/Wi-Fi interface, measures upload and download traffic per IP, and displays a live rolling graph of bandwidth usage.

---

## Features

- Detects hotspot/Wi-Fi interface automatically
- Tracks multiple target IP addresses
- Measures sent bytes, received bytes, and total KB/s
- Real-time rolling graph (updates every second)
- Streamlit UI using Plotly
- Easy to customize and extend

---

## Project Structure

```
BandwidthMonitoringTool/
│
├── app.py                # Streamlit dashboard
├── bandwidth.py          # Packet capture and bandwidth calculation logic

```

---

## Requirements

### Python Version

Python 3.8 or higher recommended.

### Install Dependencies

Install dependencies via requirements file:

```bash
pip install -r requirements.txt
```
---

## How It Works

### bandwidth.py

- Defines a list of IPs to monitor:

```python
target_ips = ["192.168.137.12", "192.168.137.33", "192.168.137.179"]
```

- Detects the active hotspot interface automatically  
- Sniffs packets using Scapy  
- Measures:  
  - Bytes sent by a target IP  
  - Bytes received by a target IP  
  - Converts total usage to KB/s  
- Returns a structured dictionary of bandwidth statistics

### app.py

- Runs the Streamlit dashboard  
- Calls `get_bandwidth_data(duration=1)` every second  
- Maintains a rolling window of 50 data points  
- Displays data using Plotly line graphs  
- Updates continuously without refreshing the page

---

## Running the App

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

This will output something like:

```
Local URL: http://localhost:8501
Network URL: http://your-ip:8501
```

Open the URL in your browser to view the live bandwidth dashboard.

---

## Dashboard Details

- A line graph for each IP address  
- X-axis: time (seconds)  
- Y-axis: KB/s usage  
- Automatic color assignment  
- Updates every second  

---

## Customization

### Change Monitored IPs

Edit the list inside `bandwidth.py`:

```python
target_ips = [
    "192.168.1.10",
    "192.168.1.22",
    "192.168.1.35"
]
```

### Change Graph Window Size

In `app.py`:

```python
WINDOW = 50
```

Increase this value for a longer history.

### Change Sniff Duration

In `app.py`:

```python
data = get_bandwidth_data(duration=1)
```

Change the duration value to adjust sampling frequency.

---

## Important Notes

- Packet sniffing requires administrator/root permissions.  
  - Windows: run PowerShell or CMD as Administrator  
  - Linux/macOS: run using `sudo`  
- Works best when your PC is the hotspot host or acts as the gateway  
- Ensure Scapy has permission to read the network interface  

---

## License

This project is open-source.  
Users may modify and distribute it freely.
