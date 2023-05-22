#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 09:36:03 2023

@author: marctheshark
"""

import paho.mqtt.client as mqtt
import json
import time
import os
import pandas as pd
from datetime import datetime
import time

class MQTTSubscriber:
    def __init__(self, broker_address, broker_port, base_topic, output_dir):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.base_topic = base_topic

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.measurements_per_sensor = {}  # Dictionary to track the number of measurements per sensor
        self.sensor_data = {}  # Dictionary to hold the sensor data

        self.count = 0
        self.output_dir = output_dir

    def start(self):
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.subscribe(self.base_topic + '/#')
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            self.client.subscribe(self.base_topic)  # Subscribe to the top topic
        else:
            print("Failed to connect, error code:", rc)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        self.timestamp = time.time()
        try:
            data = json.loads(payload)
            sensor = topic.split('/')[-2]
            subtopic = topic.split('/')[-1]
            payload = self.process_data(sensor, subtopic, data, self.timestamp)
            
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
        if self.count > 5:
            # print(payload)
            self.save_json_payload(payload)
        self.count += 1

    def process_data(self, sensor, subtopic, data, timestamp):
        if sensor not in self.measurements_per_sensor:
            self.measurements_per_sensor[sensor] = set()

        if sensor not in self.sensor_data:
            self.sensor_data[sensor] = {}

        self.measurements_per_sensor[sensor].add(subtopic)
        self.sensor_data[sensor][subtopic] = data
        self.sensor_data['timestamp'] = timestamp
        # self.sensor_data[sensor]['timestamp'] = timestamp
        return json.dumps(self.sensor_data)

    def all_measurements_received(self, sensor):
        return len(self.measurements_per_sensor[sensor]) == len(self.sensor_data[sensor])

    def build_combined_json_payload(self, sensor):
        # measurements = list(self.measurements_per_sensor[sensor])
        return json.dumps(self.sensor_data)

    def save_json_payload(self, combined_payload):
        # sensor = combined_payload['sensor']
        # timestamp = combined_payload['timestamp']

        file_name = f"{self.timestamp}_sensor_data.json"
        file_path = os.path.join(self.output_dir, file_name)

        with open(file_path, 'w+') as file:
            json.dump(combined_payload, file)

        print(f"Saved JSON payload to {file_path}")

def convert_folder_to_dataframe(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data = []
    subtopics = set()

    for file in json_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as json_file:
            payload = eval(json.load(json_file))
            # print(payload, type(payload))
            timestamp = payload['timestamp']
            sensors = [sensor for sensor in payload.keys() if 'sensor' in sensor]
            for sensor in sensors:
                sensor_data = payload[sensor]
                sensor_data['timestamp'] = timestamp
                sensor_data['sensor'] = sensor
                data.append(sensor_data)
            # print(payload)
            # data.append(payload)
            # subtopics.update(payload['data'].keys())

    df = pd.DataFrame(data)
    # for subtopic in subtopics:
        # df[subtopic] = df['data'].apply(lambda x: x.get(subtopic))

    # df.drop(['data'], axis=1, inplace=True)
    return df

# Example usage

broker_address = "192.168.1.81"  # Replace with your MQTT broker address
broker_port = 1883  # Replace with your MQTT broker port

# Subscribe to MQTT topics
topic = "/feeds"

subscriber = MQTTSubscriber(broker_address, broker_port, topic, '../data/sensor_streams')
subscriber.start()

path = '../data/sensor_streams'
df = convert_folder_to_dataframe(path)
df = df[df['sensor'] == 'sensor_a']
col = [item.split('/')[-1] for item in df.columns]
df.columns = col
# df['timestamp'] = df['timestamp'] / 1000

df['year'] = [datetime.fromtimestamp(item).year for item in df.timestamp]
df['month'] = [datetime.fromtimestamp(item).month for item in df.timestamp]
df['weekday'] = [datetime.fromtimestamp(item).weekday() for item in df.timestamp]
df['day'] = [datetime.fromtimestamp(item).day for item in df.timestamp]
df['hour'] = [datetime.fromtimestamp(item).hour for item in df.timestamp]
df['minute'] = [datetime.fromtimestamp(item).minute for item in df.timestamp]
df['microsecond'] = [datetime.fromtimestamp(item).microsecond for item in df.timestamp]


df.plot('day', 'temp')
