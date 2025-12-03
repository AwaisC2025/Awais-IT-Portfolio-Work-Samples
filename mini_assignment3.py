import paramiko
from datetime import datetime

class SSHClientRouter:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        print(f"Connecting to {self.hostname}...")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        print("Connected successfully!")

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

# === MAIN EXECUTION ===
if __name__ == "__main__":
    router = SSHClientRouter("192.168.56.20", "awais", "cisco")
    router.connect()
    output = router.send_command("show ip interface brief")
    router.save_output("show ip interface brief", output)
    router.close()
