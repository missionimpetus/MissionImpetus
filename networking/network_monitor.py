import os
import time
import subprocess

def ping(host):
    result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout.split("time=")[-1].split(" ")[0]
    else:
        return None

def monitor_network(host, interval=5):
    print(f"Monitoring network latency to {host} every {interval} seconds...")
    while True:
        latency = ping(host)
        if latency:
            print(f"Ping to {host}: {latency} ms")
