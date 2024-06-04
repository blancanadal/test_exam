
import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

broker_port = 1885
broker_ip_address = '10.8.42.100'
#suscriber_topic1 = 'NETWORK1/HOUR'
#suscriber_topic2 = 'NETWORK1/DATE'
suscriber_topic_temp = 'LSE/instalaciones/despachos/20/temperatura'
suscriber_topic_email = 'LSE/instalaciones/despachos/20/email_ocupante'

temperatura_list = []
promedio = 0
publisher_topic_email = ''

# Our "on message" event
def messageFunction (client, userdata, message):
    message_st = str(message.payload.decode("utf-8"))
    #print(message_st)
    if message.topic == suscriber_topic_email:
        email_name = message_st
        publisher_topic_email = 'LSE/trabajadores/'+email_name+'/promedios/temperatura'
        
       # print(publisher_topic_email)
    if message.topic == suscriber_topic_temp:
        temperatura_list.append(float(message_st))
        print(temperatura_list)
        if len(temperatura_list) == 6:
            temperatura_list.pop(0)
            suma_total = sum(temperatura_list)
            promedio = suma_total/5
            ourClient.publish(publisher_topic_email, publisher_topic_email +'{\”' + str(promedio) + '\"}') 
            print(promedio)

            

         
    
ourClient = mqtt.Client("SUSCRIBER1") # Create a MQTT client object
ourClient.connect(broker_ip_address, broker_port) # Connect to the test MQTT broker
ourClient.subscribe(suscriber_topic_temp) # Subscribe to the topic 1
ourClient.subscribe(suscriber_topic_email) # Subscribe to the topic 2
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
    ourClient.on_message = messageFunction # Attach the messageFunction to subscription
   
    time.sleep(3) # Sleep for 3 seconds
