#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 09:10:31 2023

@author: marctheshark
"""

import paho.mqtt.client as mqtt
import time
# Callback function to handle connection event
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, error code:", rc)

# Callback function to handle message received event
def on_message(client, userdata, msg):
    print("Received message:", msg.topic, msg.payload.decode())

# Create an MQTT client
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
broker_address = "192.168.1.81"  # Replace with your MQTT broker address
broker_port = 1883  # Replace with your MQTT broker port
client.connect(broker_address, broker_port, 60)

# Subscribe to MQTT topics
topic = "/feeds/#"  # Replace with the MQTT topic you want to subscribe to
client.subscribe(topic)

# Start the MQTT client loop to listen for incoming messages
client.loop_start()

# Publish MQTT messages (if needed)
message = "42069"

# Keep the script running to continue receiving MQTT messages
count = 0
while True:

    client.loop_start()
    time.sleep(10)
    client.publish("/feeds/sensor_b/temp", message)
    client.publish("/feeds/sensor_b/humidity", message)
    client.publish("/feeds/sensor_b/heat", message)

