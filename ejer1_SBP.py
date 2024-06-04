#Ejer1

import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
correo_personal = "sergio.beltran@alumnos.upm.es"
suscriber_topic = 'LSE/instalaciones/despachos/+/email_ocupante'
suscriber_topic_2 = 'LSE/instalaciones/despachos/8/temperatura'

# Our "on message" event
def messageFunction (client, userdata, message):
    flag = 0
    message_rc = str(message.payload.decode("utf-8"))
    print(message_rc)
    if message_rc == correo_personal:
        topic_personal = message.topic
        print(topic_personal) 
        topic_parts = message.topic.split("/")#separamos los topics
        numero_despacho = topic_parts[3] 
        print(numero_despacho)
        suscriber_topic_2 = 'LSE/instalaciones/despachos/'+numero_despacho+'/temperatura'
        ourClient.subscribe(suscriber_topic)
        flag = 1
    if flag ==1:
        if message.topic == 'LSE/instalaciones/despachos/'+numero_despacho+'/temperatura':
            temperatura_sergio = message_rc
            print(temperatura_sergio)

ourClient = mqtt.Client("SUSCRIBER1") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.subscribe(suscriber_topic) # Subscribe to the topic Hour
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    time.sleep(3) # Sleep for 3 seconds
 