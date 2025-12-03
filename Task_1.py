import sys
from napalm import get_network_driver

driver = get_network_driver("ios")

connection = driver(
    hostname="192.168.56.135",
    username="admin",
    password="cisco123",
    timeout=5,
    optional_args={
        "port": 30004,
        "transport": "telnet",
        "secret": "cisco123"
    }
)

try:
    connection.open()
    interfaces = connection.get_interfaces()
    with open("interfaces.txt", "w") as f:
        for iface in interfaces:
            f.write(iface + "\n")
except Exception as e:
    print(e, file=sys.stderr)
finally:
    connection.close()
