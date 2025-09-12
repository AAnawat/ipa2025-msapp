import pika
import os


class rabbitCon:
    def __init__(self, host_ip):
        self.connection = None
        self.credential = pika.PlainCredentials(
            os.environ.get("RABBITMQ_DEFAULT_USER"),
            os.environ.get("RABBITMQ_DEFAULT_PASS"),
        )
        self.host = host_ip

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host, credentials=self.credential)
        )
        channel = self.connection.channel()
        return channel

    def __exit__(self, type, value, traceback):
        self.connection.close()


def produce(ip, message):
    inter_key = "check_interfaces"
    rabbit = rabbitCon(ip)

    with rabbit as channel:
        channel.exchange_declare(exchange="jobs", exchange_type="direct")
        channel.queue_declare(queue="router_jobs")
        channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key=inter_key)

        channel.basic_publish(exchange="jobs", routing_key=inter_key, body=message)


if __name__ == "__main__":
    produce(os.environ.get("RABBITMQ_URI"), "192.168.1.1")
