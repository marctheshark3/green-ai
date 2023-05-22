#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 13:32:39 2023

@author: marctheshark
"""

import sqlite3

class SQLiteManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                     (sensor TEXT, timestamp INTEGER, temperature REAL, humidity REAL, heat_index REAL)''')

        conn.commit()
        conn.close()

    def insert_data(self, sensor, timestamp, temperature, humidity, heat_index):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Insert data into table
        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?)",
                  (sensor, timestamp, temperature, humidity, heat_index))

        conn.commit()
        conn.close()

    def query_data(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Query data from table
        c.execute("SELECT * FROM sensor_data")
        data = c.fetchall()

        conn.close()

        return data

# Example usage
db_file = "../data/green_data.db"  # Replace with the desired path to the SQLite database file

# Create an instance of the SQLiteManager class
manager = SQLiteManager(db_file)

# Create the table if it doesn't exist
manager.create_table()

# Insert data into the table
manager.insert_data("sensor_a", 1632567890, 25.3, 60.5, 27.8)

# Query the data from the table
result = manager.query_data()
print(result)