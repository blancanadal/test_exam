
import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
#suscriber_topic1 = 'NETWORK1/HOUR'
#suscriber_topic2 = 'NETWORK1/DATE'
suscriber_topic_temp = 'LSE/instalaciones/despachos/8/temperatura'
suscriber_topic_luz = 'LSE/instalaciones/despachos/8/luz'
suscriber_topic_humedad = 'LSE/instalaciones/despachos/8/humedad'
suscriber_topic_aire = 'LSE/instalaciones/despachos/8/aire'

topics = [suscriber_topic_humedad, suscriber_topic_aire, suscriber_topic_luz, suscriber_topic_temp]
alerta = ''
publisher_topic = 'LSE/trabajadores/sergio.beltran@alumnos.upm.es/alerta'

# Our "on message" event
def messageFunction (client, userdata, message):
    message_st = str(message.payload.decode("utf-8"))
    
    #print(message.topic)
    #print(float(message_st))
    if message.topic == suscriber_topic_temp:
        if float(message_st)<20.0 or float(message_st)> 25.0:
            alerta = 'temperatura'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker                 
    
    if message.topic == suscriber_topic_humedad:
        if float(message_st)<30.0 or float(message_st)> 60.0:
            alerta = 'humedad'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker                 
            
    if message.topic == suscriber_topic_aire:
        if float(message_st)<0.0 or float(message_st)> 1000.0:
            alerta = 'aire'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker                     

    if message.topic == suscriber_topic_luz:
        if float(message_st)<300.0 or float(message_st)> 500.0:
            alerta = 'luz'
            ourClient.publish(publisher_topic, publisher_topic +'{\”' + alerta + '\"}') # Publish message to MQTT broker                 
    
  
    
ourClient = mqtt.Client("SUSCRIBER1") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
for topic in topics:
    ourClient.subscribe(topic)
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
    #print(alerta)
    #if alerta != '':
        #ourClient.publish(publisher_topic, publisher_topic +'{\”' + str(alerta.decode()) + '\"}') # Publish message to MQTT broker
    
    time.sleep(3) # Sleep for 3 seconds
