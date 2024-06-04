import paho.mqtt.client as mqtt # Import the MQTT library
import numpy as np

broker_port = 1885
broker_ip_address = '10.8.42.100'
upmEmail = "emil.soleim@alumnos.upm.es"
numeroDespacho = "?"
bufLen = 5
bufs = {
        "temperatura" : [],
        "humedad" : [],
        "aire" : [],
        "luz" : []
}
limits = {
        "temperatura" : (20, 25),
        "humedad" : (30, 60),
        "aire" : (0, 1000),
        "luz" : (300, 500)
}
sensors = ["temperatura", "humedad", "aire", "luz"]

def processValue(buf: list, value: float):
    buf.append(value)
    if len(buf) > bufLen:
        buf.pop(0)
    return sum(buf)/len(buf)

# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    splitTopic = topic.split('/')
    global numeroDespacho
    if (splitTopic[-1] == "email_ocupante" and message == upmEmail and numeroDespacho == "?"):
        # Assign desk number and subscribe to tasks
        print(topic, message, splitTopic[3])
        numeroDespacho = splitTopic[3]
        client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/temperatura") 
        client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/aire") 
        client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/humedad") 
        client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/luz") 
    if (splitTopic[-1] in sensors):
        print(f"{splitTopic[-1]} recibida: {message}")
        avg = processValue(bufs[splitTopic[-1]], float(message))
        print(f"Average {splitTopic[-1]}: {avg}")
        # Check if the average exceeds the limits
        if (avg < limits[splitTopic[-1]][0] or avg > limits[splitTopic[-1]][1]):
            client.publish("LSE/trabajadores/" + upmEmail + "/alerta", splitTopic[-1])
            print(f"!!!!!!!! ALERTA de {splitTopic[-1]}")



def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LSE/instalaciones/despachos/+/email_ocupante") 

ourClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)# Create a MQTT client object
ourClient.on_connect = on_connect
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

input("Press a key to exit...\n")
