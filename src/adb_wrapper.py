import subprocess

def pair_device(ip: str, port: int, password: str) -> bool:
    cmd = ['adb', 'pair', f'{ip}:{port}', password]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def connect_device(ip: str, port: int) -> bool:
    cmd = ['adb', 'connect', f'{ip}:{port}']
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0
