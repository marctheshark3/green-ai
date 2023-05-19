#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 18:13:48 2023

@author: marctheshark
"""
import torch
from torch.utils.data import Dataset
from green_ai.greenhouse_data_sample import GreenhouseDataGenerator

class GreenhouseDataset(Dataset):
    def __init__(self, n_samples, use_case):
        self.generator = GreenhouseDataGenerator(n_samples)
        self.dataset = self.generator.generate_dataset(use_case)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        data, label = self.dataset[idx]
        data = torch.tensor(data, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.long)
        return data, label

class GreenhouseDataLoader:
    def __init__(self, data, batch_size=32, shuffle=True):
        self.data = data
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.loader = torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=shuffle)

    def get_loader(self):
        return self.loader

    def save_loader(self, filename):
        torch.save(self.loader, filename)

    def load_loader(self, filename):
        self.loader = torch.load(filename)
        return self.loader



if __name__ == '__main__':
    n_samples = 1000
    single_use_case = 'single'
    daily_use_case = 'daily'
    single_dataset = GreenhouseDataset(n_samples, single_use_case)
    daily_dataset = GreenhouseDataset(n_samples, daily_use_case)
    
    single_data= GreenhouseDataLoader(data=single_dataset, batch_size=32, shuffle=True)
    single_dataloader = single_data.get_loader()

    daily_data= GreenhouseDataLoader(data=daily_dataset, batch_size=32, shuffle=True)
    daily_dataloader = single_data.get_loader()

    single_file = '../green_ai/data/single_dataloader.pth'
    multi_file = '../green_ai/data/multi_dataloader.pth'

    single_data.save_loader(single_file)
    daily_data.save_loader(multi_file)

    for batch in single_dataloader:
        data, label = batch
        print(data.shape, label.shape) # Print shape of each batch
        print(data,label)
        break

    for batch in daily_dataloader:
        data, label = batch
        print(data.shape, label.shape) # Print shape of each batch
        break

    new_loader = single_data.load_loader(single_file)

    for batch in new_loader:
        data, label = batch
        print(data.shape, label.shape) # Print shape of each batch
        print(data,label)
        break
