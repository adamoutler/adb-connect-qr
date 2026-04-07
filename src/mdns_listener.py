import time
from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo

class AdbPairingListener:
    def __init__(self, target_service_name: str):
        self.target_service_name = target_service_name
        self.ip_address = None
        self.port = None

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            # name is typically like "adb-cli-test._adb-tls-pairing._tcp.local."
            if self.target_service_name in name:
                self.on_service_found(info, name)
                
    def update_service(self, zeroconf, type, name):
        pass

    def on_service_found(self, info: ServiceInfo, name: str):
        addresses = info.parsed_addresses()
        if addresses:
            self.ip_address = addresses[0]
            self.port = info.port

def discover_service(service_type: str, target_name: str, timeout: int = 60):
    zeroconf = Zeroconf()
    listener = AdbPairingListener(target_name)
    browser = ServiceBrowser(zeroconf, service_type, listener)
    
    start_time = time.time()
    while listener.ip_address is None and (time.time() - start_time) < timeout:
        time.sleep(0.5)
        
    zeroconf.close()
    return listener.ip_address, listener.port
