from cryptography.fernet import Fernet
import base64
import os
import ctypes
import time

def load_key():
    """Load the encryption key with validation"""
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("Error: Decryption key not found!")
        return None

def decrypt_files():
    """Decrypt files with progress tracking"""
    key = load_key()
    if not key:
        return
    
    f = Fernet(key)
    decrypted_count = 0
    
    for filename in os.listdir():
        if filename.endswith(".encrypted"):
            try:
                original_name = filename.replace(".encrypted", "")
                
                with open(filename, "rb") as file:
                    encrypted_data = file.read()
                
                # Reverse the double encryption
                decrypted_data = base64.b64decode(encrypted_data)
                decrypted_data = f.decrypt(decrypted_data)
                
                with open(original_name, "wb") as file:
                    file.write(decrypted_data)
                
                os.remove(filename)
                decrypted_count += 1
                
            except Exception as e:
                print(f"Error decrypting {filename}: {str(e)}")
    
    return decrypted_count

def show_success_message():
    """Display decryption success message"""
    message = """
    DECRYPTION SUCCESSFUL!
    
    All your files have been restored to their original state.
    
    For your security:
    1. Update your operating system
    2. Change all passwords
    3. Install reputable antivirus software
    4. Be cautious with email attachments
    
    This was a cybersecurity awareness demonstration.
    """
    
    ctypes.windll.user32.MessageBoxW(0, message, "DECRYPTION COMPLETE", 0x40)

def main():
    """Main decryption function"""
    print("[+] Starting decryption process...")
    decrypted_count = decrypt_files()
    
    if decrypted_count > 0:
        print(f"[+] Successfully decrypted {decrypted_count} files")
        show_success_message()
        
        # Clean up ransomware files
        for f in ["secret.key", "READ_ME_FOR_DECRYPT.txt", "encrypted_files_log.csv", "countdown.txt"]:
            try:
                os.remove(f)
            except:
                pass
    else:
        print("[-] No files were decrypted")

if __name__ == "__main__":
    main()