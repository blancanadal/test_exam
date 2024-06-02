import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
desk_number = 23
list_temp = []
air_topic   = "LSE/trabajadores/blanca.nadal@alumnos.upm.es/promedios/aire"
temp_topic  = "LSE/trabajadores/blanca.nadal@alumnos.upm.es/promedios/temperatura"
hum_topic   = "LSE/trabajadores/blanca.nadal@alumnos.upm.es/promedios/humedad"
light_topic = "LSE/trabajadores/blanca.nadal@alumnos.upm.es/promedios/luz"

publisher_topic = "LSE/trabajadores/blanca.nadal@alumnos.upm.es/alerta"

# Our "on message" event
def messageFunction (client, userdata, message):
    message_rcv = str(message.payload.decode("utf-8"))
    if (message.topic == air_topic):
        if (float(message_rcv) > 1000):
            alerta = 'aire'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker
    if (message.topic == temp_topic):
        if (20 > float(message_rcv) > 25):
            alerta = 'temperatura'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker
    if (message.topic == hum_topic):
        if (30 > float(message_rcv) > 60):
            alerta = 'humedad'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker            
    if (message.topic == light_topic):
        if (300 > float(message_rcv) > 500):
            alerta = 'luz'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker

ourClient = mqtt.Client("BLANCA") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.subscribe(air_topic) # Subscribe to the topic
ourClient.subscribe(temp_topic) # Subscribe to the topic
ourClient.subscribe(hum_topic) # Subscribe to the topic
ourClient.subscribe(light_topic) # Subscribe to the topic
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    time.sleep(3) # Sleep for 3 seconds