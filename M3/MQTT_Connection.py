import paho.mqtt.client as mqtt
import numpy as np
import json, sys
import time

message_exists = False
message_output = ""
count = 0

def mqtt_publisher():
    # 0. define callbacks - functions that run when events happen.
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("ECEM119")
        # The callback of the client when it disconnects.

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print('Unexpected Disconnect')
        else:
            print('Expected Disconnect')
        # The default message callback.
        # (won't be used if only publishing, but can still exist)

    def on_message(client, userdata, message):
        global message_exists
        message_exists = True
        # print(str(message.payload)[2:-1], flush=True, end='')
        global message_output
        message_output = str(message.payload)[2:-1]
        
                
    # 1. create a client instance.
    client = mqtt.Client()
    # add additional client options (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.
    # client.connect_async("test.mosquitto.org")
    client.connect_async('mqtt.eclipseprojects.io')

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()
    # 4. use subscribe() to subscribe to a topic and receive messages.
    # 5. use publish() to publish messages to the broker.
    # payload must be a string, bytearray, int, float or None.
    #client.publish("ECEM119", curr, qos=1)

    while not message_exists:
        global count
        count += 1
        if count > 15000000:
            break
        pass

    # 6. use disconnect() to disconnect from the broker.
    # client.loop_stop()
    # client.disconnect()

def main():
    mqtt_publisher()
    if (message_exists):
        print(message_output, flush=True, end='')

if __name__ == '__main__':
    main()

    11970779