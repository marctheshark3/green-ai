#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:24:19 2023

@author: marctheshark
"""

import random

class GreenhouseDataGenerator:
    def __init__(self, n_samples):
        self.n_samples = n_samples
        self.sensor_names = ['temp_inside', 'temp_outside', 'humidity', 'light', 'water']
        self.optimal_ranges = {
            'temp_inside': (65, 75),
            'temp_outside': (20, 30),
            'humidity': (40, 60),
            'light': (5000, 10000),
            'water': (50, 75)
        }

    def generate_single_data_point(self):
        data = []
        for name in self.sensor_names:
            if name == 'temp_inside':
                optimal_range = self.optimal_ranges[name]
                data_point = random.uniform(optimal_range[0], optimal_range[1])
            elif name == 'temp_outside':
                data_point = random.uniform(15, 35)
            else:
                optimal_range = self.optimal_ranges[name]
                data_point = random.uniform(optimal_range[0], optimal_range[1])
            data.append(data_point)
        
        label = self.calculate_label(data)
        return data, label

    def calculate_label(self, data):
        temp_inside = data[0]
        optimal_range = self.optimal_ranges['temp_inside']
        if temp_inside < optimal_range[0] or temp_inside > optimal_range[1]:
            return 0
        else:
            return 1

    def generate_daily_data(self):
        daily_data = []
        for i in range(12):
            data_point, _ = self.generate_single_data_point()
            daily_data.append(data_point)

        daily_averages = []
        for j in range(len(self.sensor_names)):
            sensor_data = [row[j] for row in daily_data]
            daily_averages.append(sum(sensor_data) / len(sensor_data))
        
        label = self.calculate_label(daily_averages)
        return daily_averages, label

    def generate_dataset(self, use_case):
        dataset = []
        for i in range(self.n_samples):
            if use_case == 'single':
                data, label = self.generate_single_data_point()
            elif use_case == 'daily':
                data, label = self.generate_daily_data()
            else:
                raise ValueError('Invalid use case specified.')
            dataset.append((data, label))
        
        return dataset

if __name__ == '__main__':
    n_samples = 1000
    use_case = 'single'
    generator = GreenhouseDataGenerator(n_samples)
    dataset = generator.generate_dataset(use_case)
    print(dataset[:10]) # Print first 10 samples in the dataset
