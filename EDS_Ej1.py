import paho.mqtt.client as mqtt # Import the MQTT library

broker_port = 1885
broker_ip_address = '10.8.42.100'
upmEmail = "emil.soleim@alumnos.upm.es"
numeroDespacho = "?"

# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    splitTopic = topic.split('/')
    global numeroDespacho
    if (splitTopic[-1] == "email_ocupante" and message == upmEmail and numeroDespacho == "?"):
        print(topic, message, splitTopic[3])
        numeroDespacho = splitTopic[3]
        client.subscribe("LSE/instalaciones/despachos/" + numeroDespacho + "/temperatura") 
    elif (splitTopic[-2] + splitTopic[-1] == numeroDespacho + "temperatura"):
        print(topic, message)

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
