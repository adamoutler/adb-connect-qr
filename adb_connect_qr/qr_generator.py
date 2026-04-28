import qrcode
import string
import random

def generate_random_string(length: int) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def generate_pairing_string(service_name: str, password: str) -> str:
    return f"WIFI:T:ADB;S:{service_name};P:{password};;"

def print_qr_code(payload: str, invert: bool = False) -> None:
    qr = qrcode.QRCode()
    qr.add_data(payload)
    qr.print_ascii(invert=invert)
