# adb-connect-qr

Easy connection for wireless adb.

## Example Session

```
$ adb-connect-qr
Starting ADB QR Code Pairing...

Scan this QR code in Android > Developer Options > Wireless Debugging > Pair device with QR code

Service Name: adb-cli-faXn2w
Password: Qp3hUJ

```

![QR Code](images/qr-code.png)

```
Waiting for device to scan QR code (timeout 60s)...
Device found at 192.168.1.39:37479. Initiating pairing...
Running: adb pair 192.168.1.39:37479 Qp3hUJ
Successfully paired to 192.168.1.39:37479 [guid=adb-57161FDCG001PE-HgzRvA]

Pairing successful! Waiting for connection service...
Running: adb connect 192.168.1.39:42865
connected to 192.168.1.39:42865

Successfully paired and connected!
```

## Setup Instructions

### Prerequisites
* Python 3.8+
* `adb` installed and available on your system PATH.

### Installation
You can install this tool directly from PyPI:

```bash
pip install adb-connect-qr
```

### Usage
Simply run the command in your terminal:
```bash
adb-connect-qr
```
Then go to your Android device:
1. Open **Settings** > **Developer Options** > **Wireless Debugging**.
2. Tap **Pair device with QR code**.
3. Scan the QR code displayed in your terminal.
