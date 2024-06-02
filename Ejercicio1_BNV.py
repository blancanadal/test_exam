import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
UPM_email = 'blanca.nadal@alumnos.upm.es'

# Our "on message" event
def messageFunction (client, userdata, message):
    if (message.topic == "LSE/instalaciones/despachos/+/email_ocupante"):
    	message_desk = str(message.payload.decode("utf-8"))
        if (message_desk == UPM_email):
            topic_desk = message.topic.split('/') # Splits the topic every /
            desk_number = topic_desk[3];
            print(desk_number)
            OurClient.suscribe("LSE/instalaciones/despachos/"+desk_number+"/temperatura")
    if (message.topic == "LSE/instalaciones/despachos/"+desk_number+"/temperatura"):
    	message_temp = str(message.payload.decode("utf-8"))
        print(message_temp)
 
ourClient = mqtt.Client("BLANCA") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.subscribe("LSE/instalaciones/despachos/+/email_ocupante") # Subscribe to the topic
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    time.sleep(3) # Sleep for 3 seconds