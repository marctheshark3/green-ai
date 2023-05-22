#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 13:37:51 2023

@author: marctheshark
"""

import sqlite3
import pandas as pd


class GreenhouseDataDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS greenhouse_data (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          temperature REAL,
          humidity REAL,
          heat_index REAL,
          time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, temperature, humidity, heat_index):
        insert_query = '''
        INSERT INTO greenhouse_data (temperature, humidity, heat_index)
        VALUES (?, ?, ?)
        '''
        values = (temperature, humidity, heat_index)
        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def clear_database(self):
        clear_query = '''
        DELETE FROM greenhouse_data
        '''
        self.cursor.execute(clear_query)
        self.conn.commit()

    def close(self):
        self.conn.close()


class GreenhouseDataAnalyzer:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def query_data(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def create_dataframe(self):
        query = 'SELECT * FROM greenhouse_data'
        rows = self.query_data(query)
        columns = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    # Example usage
    # db = GreenhouseDataDB('green_data.db')
    # db.connect()

    # Insert data into the database
    # db.insert_data(25.3, 60.5, 27.8)
    # db.insert_data(25.3, 60.5, 27.8)
    # db.insert_data(25.3, 60.5, 27.8)

    # Example usage
    db_name = 'green_data.db'
    analyzer = GreenhouseDataAnalyzer(db_name)
    analyzer.connect()

    # Query data
    query = 'SELECT * FROM greenhouse_data WHERE temperature > 25'
    results = analyzer.query_data(query)
    for row in results:
        print(row)
    
    # Create a DataFrame
    df = analyzer.create_dataframe()
    print(df.head())
    
    # analyzer.close()

    # # Clear the database
    # db.clear_database()
    
    # # Close the database connection
    # db.close()
