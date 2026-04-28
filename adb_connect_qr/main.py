#!/usr/bin/env python3
import sys
import argparse
from .qr_generator import generate_random_string, generate_pairing_string, print_qr_code
from .mdns_listener import discover_service
from .adb_wrapper import pair_device, connect_device

def main():
    parser = argparse.ArgumentParser(description="Pair Android device via QR code wireless debugging")
    parser.add_argument("--invert", action="store_true", help="Display inverted QR code (white on black)")
    args = parser.parse_args()
    
    print("Starting ADB QR Code Pairing...")
    
    # 1. Generate Config
    service_name = f"adb-cli-{generate_random_string(6)}"
    password = generate_random_string(6)
    
    # 2. Render QR
    payload = generate_pairing_string(service_name, password)
    print(f"\nScan this QR code in Android > Developer Options > Wireless Debugging > Pair device with QR code\n")
    print(f"Service Name: {service_name}")
    print(f"Password: {password}\n")
    print_qr_code(payload, invert=args.invert)
    
    # 3. Discover Pairing Service
    print(f"\nWaiting for device to scan QR code (timeout 60s)...")
    ip, pairing_port = discover_service("_adb-tls-pairing._tcp.local.", service_name)
    
    if not ip or not pairing_port:
        print("Timeout waiting for device.")
        sys.exit(1)
        
    print(f"Device found at {ip}:{pairing_port}. Initiating pairing...")
    
    # 4. Pair
    if not pair_device(ip, pairing_port, password):
        print("Pairing failed.")
        sys.exit(1)
        
    print("Pairing successful! Waiting for connection service...")
    
    # 5. Discover Connect Service (The device switches to this after pairing)
    # We look for ANY adb-tls-connect from this IP, or we can just try connecting to the standard connect broadcast.
    # Note: connect service broadcast name usually starts with adb- but isn't our service_name.
    # We will filter by the IP we just paired with.
    
    # Modified discovery for connection - waiting for _adb-tls-connect._tcp.local. from the same IP
    import time
    from zeroconf import ServiceBrowser, Zeroconf
    from .mdns_listener import AdbPairingListener
    
    class ConnectListener(AdbPairingListener):
        def __init__(self, target_ip):
            super().__init__("")
            self.target_ip = target_ip
            
        def add_service(self, zeroconf, type, name):
            info = zeroconf.get_service_info(type, name)
            if info:
                addresses = info.parsed_addresses()
                if addresses and addresses[0] == self.target_ip:
                    self.on_service_found(info, name)

    zeroconf = Zeroconf()
    listener = ConnectListener(ip)
    browser = ServiceBrowser(zeroconf, "_adb-tls-connect._tcp.local.", listener)
    
    start_time = time.time()
    while listener.port is None and (time.time() - start_time) < 15:
        time.sleep(0.5)
        
    zeroconf.close()
    
    connect_port = listener.port
    if not connect_port:
        print(f"Could not discover connection port for {ip}. Try running 'adb connect {ip}:<port>' manually from the Wireless Debugging screen.")
        sys.exit(1)
        
    # 6. Connect
    if not connect_device(ip, connect_port):
        print("Connection failed.")
        sys.exit(1)
        
    print("\nSuccessfully paired and connected!")

if __name__ == '__main__':
    main()
