#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 13:32:39 2023

@author: marctheshark
"""


import sqlite3
import json
import os
import pandas as pd

class SQLiteManager:
    def __init__(self, db_file, table_name, column_mapping):
        self.db_file = db_file
        self.table_name = table_name
        self.column_mapping = column_mapping
        self.timestamp = 0

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create table with columns based on column_mapping
        columns = ', '.join([f"{column} {data_type}" for column, data_type in self.column_mapping.items()])
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})")

        conn.commit()
        conn.close()

    def insert_data(self, data):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Prepare column names and placeholders for INSERT statement
        # print(data, type(data))
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])

        # Prepare values for INSERT statement
        values = tuple(data[column] for column in data)
        print(placeholders, values, 'oi ')

        # Insert data into table
        c.execute(f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})", values)

        conn.commit()
        conn.close()

    def compress_json_files(self, folder_path):
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

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
                    # print(type(timestamp))
                    # print(timestamp)
                    sensor_data['sensor'] = sensor
                    # print(sensor_data)
                    # data.append(sensor_data)
                    self.insert_data(sensor_data)

            # Remove the JSON file after compressing
            os.remove(file_path)

    def query_data_as_dataframe(self):
        conn = sqlite3.connect(self.db_file)

        # Use pandas to query the data and generate a DataFrame
        query = f"SELECT * FROM {self.table_name}"
        df = pd.read_sql_query(query, conn)

        conn.close()
        return df

    def clear_table(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Delete all rows from the table
        c.execute(f"DELETE FROM {self.table_name}")

        conn.commit()
        conn.close()


# Example usage
db_file = "../data/green_data.db"  # Replace with the desired path to the SQLite database file
table_name = "sensor_data"  # Replace with the desired table name
column_mapping = {
    "sensor": "VARCHAR40",
    "timestamp": "REAL",
    "temp": "REAL",
    "humidity": "REAL",
    "heat": "REAL"
}

# Create an instance of the SQLiteManager class
manager = SQLiteManager(db_file, table_name, column_mapping)

# Create the table if it doesn't exist
manager.create_table()

# Insert data into the table from JSON files
folder_path = "../data/sensor_streams/"  # Replace with the folder containing the JSON files
manager.compress_json_files(folder_path)
df = manager.query_data_as_dataframe()

# Example usage
# db_file = "../data/green_data.db"  # Replace with the desired path to the SQLite database file

# # Create an instance of the SQLiteManager class
# manager = SQLiteManager(db_file)

# # Create the table if it doesn't exist
# manager.create_table()

# # Insert data into the table
# manager.insert_data("sensor_a", 1632567890, 25.3, 60.5, 27.8)

# # Query the data from the table
# result = manager.query_data()
# print(result)