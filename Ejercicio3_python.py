/* MQTT (over TCP) Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

/* Here is the equivalent Python code. Note that the MQTT functionality is implemented using the Paho MQTT library, which is a popular choice for MQTT in Python. Also, note that Python does not have a direct equivalent to C's struct, so a class is used instead.
*/


import paho.mqtt.client as mqtt
import time

class Machine:
    def __init__(self, machine_name, IP_address, current_status, work_assignment, worker_assignment, progress, notification):
        self.machine_name = machine_name
        self.IP_address = IP_address
        self.current_status = current_status
        self.work_assignment = work_assignment
        self.worker_assignment = worker_assignment
        self.progress = progress
        self.notification = notification

    def print_machine(self):
        print(f"\nMACHINE REPORT\n--------------")
        print(f"machine_name: {self.machine_name}")
        print(f"IP_address: {self.IP_address}")
        print(f"current_status: {self.current_status}")
        print(f"work_assignment: {self.work_assignment}")
        print(f"worker_assignment: {self.worker_assignment if self.worker_assignment else 'UNASSIGNED'}")
        print(f"progress: {self.progress}")
        print(f"notification: {self.notification}")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("LSE/machines/+/progress")

def on_message(client, userdata, msg):
    print(f"TOPIC={msg.topic}")
    print(f"DATA={msg.payload.decode()}")
    machine_name = msg.topic.split('/')[2]
    print(f"machine_name = {machine_name}")

    if "delayed" in msg.payload.decode() or "completed" in msg.payload.decode():
        machines_generating_notifications.append(machine_name)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)

machines_generating_notifications = []
student_machine = Machine("machine23", "10.8.42.23", "running", "testing", "blanca.nadal@alumnos.upm.es", "normal", "por descubrir")

while True:
    client.loop_start()
    for machine_name in machines_generating_notifications:
        topic = f"LSE/blanca.nadal@alumnos.upm.es/workers/{machine_name}/worker_performance"
        payload = "good" if "completed" in student_machine.progress else "bad"
        print(f"\n[Publisher_Task]\n[TOPIC][{topic}]\n[PAYLOAD][{payload}]")
        client.publish(topic, payload)
    time.sleep(2)

/*This Python script connects to an MQTT broker, subscribes to the topic "LSE/machines/+/progress", and listens for messages. When a message is received, it checks if the payload contains "delayed" or "completed". If it does, the machine name is added to the list of machines generating notifications. The script then publishes a message to the topic "LSE/blanca.nadal@alumnos.upm.es/workers/{machine_name}/worker_performance" every 2 seconds, with the payload being "good" if the machine's progress is "completed", and "bad" otherwise.*/
/*pip install paho-mqtt
Also, this Python code assumes that the MQTT broker is running at "mqtt.eclipse.org" on port 1883. Please replace it with your actual MQTT broker address and port.*/
/* ALTERNATIVE*/



