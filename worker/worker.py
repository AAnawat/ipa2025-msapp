import pika, os, time

from router_controller import Rcontroller
from dbCon import upload_interface
from bson import json_util

def check_interface(ch, method, properties, body):
    info = json_util.loads(body)
    r1 = Rcontroller(info["ip"])
    
    try:
        with r1.makeConnection() as connection:
            result = connection.send_command("show ip int br", use_textfsm=True)
    except Exception as e:
        print("No router avalible.")
        return;

    upload_interface(info["ip"], result)

def work():
    credential = pika.PlainCredentials(os.environ.get("RABBITMQ_DEFAULT_USER"), os.environ.get("RABBITMQ_DEFAULT_PASS"))
    for _ in range(10):
        try:
            pikaCon = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", credentials=credential)
            )
            channel = pikaCon.channel()
            channel.queue_declare("router_jobs")
            break
        except Exception as e:
            print("Error occur.")
            time.sleep(10)
            

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='router_jobs', on_message_callback=check_interface, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    work()