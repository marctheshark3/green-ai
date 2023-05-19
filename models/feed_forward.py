#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:56:55 2023

@author: marctheshark
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class GreenhouseNet(nn.Module):
    def __init__(self):
        super(GreenhouseNet, self).__init__()
        self.fc1 = nn.Linear(5, 32)
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

if __name__ == '__main__':
    import numpy as np
    # Create an instance of the GreenhouseNet model
    model = GreenhouseNet()

    # Generate a random data point
    data = np.random.rand(5).astype(np.float32)

    # Convert data to a PyTorch tensor and add batch dimension
    data = torch.from_numpy(data).unsqueeze(0)

    # Use the model to make a prediction
    with torch.no_grad():
        output = model(data)
        pred = torch.argmax(output, dim=1).item()

    # Print the prediction
    if pred == 0:
        print('Optimal conditions')
    else:
        print('Suboptimal conditions')