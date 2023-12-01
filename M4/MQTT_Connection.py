import paho.mqtt.client as mqtt
import numpy as np
import time

data_out = None

class mqtt_publisher():
    # 0. define callbacks - functions that run when events happen.
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connection returned result: " + str(rc))
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
        message = str(message.payload)[2:-1]
        # print('Received message: ', message)
        data = message.split(';')

        mappings = {'Acceleration': {}, 'Gyroscope': {}}
        for d in data:
            degree, axis, value = d.split(',')
            mappings[degree][axis] = float(value)

        global data_out
        data_out = mappings
                
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

    # 6. use disconnect() to disconnect from the broker.
    # client.loop_stop()
    # client.disconnect()

def main():
    mqtt_client = mqtt_publisher()

    while True:
        print(data_out)


if __name__ == '__main__':
    main()