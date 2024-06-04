import paho.mqtt.client as mqtt # Import the MQTT library
import numpy as np

broker_port = 1885
broker_ip_address = '10.8.42.100'
numeroDespacho = "5"
email_ocupante = "?"
bufLen = 5
buf = []

# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    splitTopic = topic.split('/')
    global email_ocupante
    if (splitTopic[-1] == "email_ocupante"):
        print(f"Occupant of desk {numeroDespacho} is {message}")
        email_ocupante = message
    if (splitTopic[-1] == "temperatura"):
        print(f"temperatura recibida: {message}")
        buf.append(float(message))
        if len(buf) > bufLen:
            buf.pop(0)
        avg = sum(buf)/len(buf)
        print(f"Average temperature: {avg}")
        if email_ocupante != "?":
            client.publish("LSE/trabajadores/" + email_ocupante + "/promedios/temperatura", avg)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/email_ocupante") 
    client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/temperatura") 

ourClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)# Create a MQTT client object
ourClient.on_connect = on_connect
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

input("Press a key to exit...\n")
