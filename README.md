# Hidden-Keylogger

This project is an educational tool designed to monitor various aspects of a computer system, including clipboard data, system information, browser history, connected devices, network information, and keystrokes. It also captures screenshots periodically. The gathered data is encrypted and can be sent to a remote server. A separate decryption program is provided to decrypt the data.  The project includes two primary scripts:

**Keylogger.py** - Gathers system information, network details, and browser history, captures keystrokes and screenshots, and encrypts the data
**Decrypter.py** - Decrypts the encrypted data produced by keylogger.py

## Features

- Clipboard monitoring
- System information gathering
- Connected devices information
- Network information
- Browser history extraction
- Screenshot capturing
- Keystroke logging
- Symmetric Data encryption 
- Sending encrypted data to a server

## Requirements

To run this project, you need to install the following dependencies:

- psutil
- pynput
- pyautogui
- clipboard
- cryptography
- requests
- sqlite3

Install the required libraries using:

```bash
pip install -r requirements.txt
```

# Explanation

## Data Gathering and Logging (Keylogger.py)
### Encryption and File Transfer:

*	symmetric_encrypt(data, key): Encrypts data using a symmetric key (AES) with CFB mode and a random IV.
*	send_file(file_path, url): Sends a file to a specified URL using an HTTP POST request.

### Clipboard Monitoring:
* copy_clipboard(): Copies clipboard content to a file.
* refresh_clipboard(): Monitors clipboard changes every 2 seconds.

### System Information:
* gather_system_information(): Gathers detailed system information and writes it to a file.
* gather_connected_devices(): Collects information about connected devices and writes it to a file.
* gather_network_information(): Retrieves network information and writes it to a file.

### Browser History:
* gather_browser_history(): Extracts browser history from the Chrome browser and writes it to a file.

### Screenshot Capturing:
* capture_screenshot(): Takes screenshots every 30 seconds and saves them in a folder.

### Keylogger:
* write_file(key): Writes key presses to a file.
* write_letters_file(key): Writes only letter key presses to a separate file.
* on_press(key), on_release(key): Handle key press and release events.

###	Encrypt Files and Folder:
* encrypt_files(): Encrypts specific files using symmetric encryption.
* encrypt_screenshots_folder(): Compresses the screenshots folder and encrypts it.

### Send Encrypted Files to Server:
* send_files_to_server(): Sends encrypted files to a remote server.


## Decryption Program (Decrypter.py)
### Decrypt Files and Folder:
*	symmetric_decrypt(data, key): Decrypts data using a symmetric key (AES) with CFB mode and a random IV.
* decrypt_files(): Decrypts encrypted files using the symmetric key.
* decrypt_screenshots_folder(): Decrypts and extracts the screenshots folder.

# Usage
## Setting Up
1.	Clone the repository
```bash
git clone https://github.com/anishvedant/Hidden-Keylogger.git
cd Hidden-Keylogger
```

2.	Install the required packages
```bash
pip install -r requirements.txt
```

## Running the Main Script
1.	Start the main script
```bash
python3 Keylogger.py
```

After the encrypted files are generated, run the decrypter program. 

## Running the Decryption Program
1.	Start the decryption program:
```bash
python3 Decrypter.py
```

# Limitations 

* Handling of Keystrokes: Currently, the combination of keystrokes with Ctrl is not handled properly.
* Numeric Numpad: Numeric numbers on the numpad cannot be captured properly.
* Resource Usage: The script could be optimized to use fewer system resources and be more efficient.
* Stealth Mode: Can be made to run in the background and undetectable.
* Browser History Access: Current implementation might not work if the browser's database schema changes or if multiple profiles are used.

# Scope for Improvements
1.	Email Notifications: Implement a feature to send collected data to an email address periodically or receive an alert once the contents are received by the server.
2.	Optimization: Reduce resource usage and improve efficiency.
3.	Stealth Mode: Enhance stealth capabilities to avoid detection by antivirus software.
4.	Enhanced Keystroke Logging: Improve handling of special key combinations and numeric numpad entries.
5.	Executable File: Convert the script into an executable file that can run in the background and undetectable.
   
# Browser History Gathering
* Function: The gather_browser_history function attempts to access the SQLite database used by browsers like Chrome to store browsing history.
* Implementation: This function reads the database and writes the history to a file. This will only work if the browser is not running, as the database will be locked otherwise.

# Contribution
Feel free to contribute by submitting pull requests. Ensure all contributions align with the educational purpose and ethical use of the software.

# License
This project is licensed under the MIT License.

# Disclaimer

## **Educational Purpose Only**
**This tool is intended to be used responsibly and for *educational purposes only*. The use of this software on any system or network without explicit permission from the owner is illegal and unethical. The developer is not responsible for any loss or damage resulting from the use or misuse of this software. Always follow ethical guidelines and ensure you have obtained the necessary permissions to monitor and log data on any system you use this software on.**  
