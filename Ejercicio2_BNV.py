import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
desk_number = 12
list_temp = []

# Our "on message" event
def messageFunction (client, userdata, message):
    if (message.topic == "LSE/instalaciones" +UPM_email+ "promedios/temperatura"):
    	UPM_email = str(message.payload.decode("utf-8"))
        print(UPM_email)
        client_topic = "LSE/trabajadores/despachos/12/temperatura"
    if (message.topic == "LSE/instalaciones/despachos/12/temperatura"):
        new_data = str(message.payload.decode("utf-8"))
        list_temp.append(float(new_data))
        if len(list_temp) == 6:
            list_temp.pop(0)
            avg = (list_temp[0] + list_temp[1] + list_temp[2] + list_temp[3] + list_temp[4])/5
            print(avg)
            ourClient.publish(client_topic, client_topic +'{\"message\": \"' + str(avg) + '\"}') # Publish message to MQTT broker


ourClient = mqtt.Client("BLANCA") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.subscribe("LSE/instalaciones/despachos/12/email_ocupante") # Subscribe to the topic
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    time.sleep(3) # Sleep for 3 seconds