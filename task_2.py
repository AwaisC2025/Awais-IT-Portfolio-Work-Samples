import sys
from napalm import get_network_driver

driver = get_network_driver("ios")

connection = driver(
    hostname="192.168.56.135",  # same working IP
    username="admin",
    password="cisco123",
    timeout=5,
    optional_args={
        "port": 30004,          # same port
        "transport": "telnet",
        "secret": "cisco123"
    }
)

try:
    connection.open()
    users = connection.get_users()
    with open("users.txt", "w") as f:
        for user in users:
            f.write(user + "\n")
except Exception as e:
    print(e, file=sys.stderr)
finally:
    connection.close()
