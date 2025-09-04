from netmiko import ConnectHandler


class Rcontroller:
    def __init__(self, host, username="admin", password="cisco"):
        self.config = {
            "device_type": "cisco_ios",
            "host": host,
            "username": username,
            "password": password,
        }

    def makeConnection(self):
        connection = ConnectHandler(**self.config)
        return connection


if __name__ == "__main__":
    controller = Rcontroller("10.30.6.189")
    with controller.makeConnection() as connection:
        print(connection.send_command("show ip int br", use_textfsm=True))
