import paramiko
import time
from datetime import datetime

class SSHClientRouter:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None
        self.shell = None

    def connect(self):
        print(f"Connecting to {self.hostname}...")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print("Connected successfully!")

    # Modified shell method for lab exercise 6
    def send_shell_command(self, command, user_input=""):
        if self.shell is None:
            self.shell = self.client.invoke_shell()
            time.sleep(0.5)
            if self.shell.recv_ready():
                self.shell.recv(9999)

        # Send the main command
        self.shell.send(command + "\n")
        time.sleep(1)

        # Send additional input if length > 0
        if len(user_input) > 0:
            self.shell.send(user_input + "\n")
            time.sleep(1)

        # Return the latest output
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(9999).decode(errors="ignore")

        return output


    def send_command(self, command):
        if self.client is None:
            raise Exception("SSH connection not established.")
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode()
        print(output)
        return output

    def save_output(self, command, output):
        now = datetime.now()
        filename = f"command_{command.replace(' ', '_')}_{now.strftime('%d_%B_%Y-%H_%M')}.txt"
        with open(filename, 'w') as file:
            file.write(output)
        print(f"Output saved as {filename}")

    def close(self):
        if self.client:
            self.client.close()
            print("Connection closed.")
