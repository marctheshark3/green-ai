#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:40:48 2023

@author: marctheshark
"""

import torch
from green_ai.models.feed_forward import GreenhouseNet
import numpy as np

class GreenhouseInference:
    def __init__(self, model_path):
        model_state_dict = torch.load(model_path)
        self.model = GreenhouseNet()
        self.model.load_state_dict(model_state_dict)


    def predict(self, input_data):
        input_tensor = torch.tensor(input_data, dtype=torch.float32)

        # use the model to make a prediction on the input tensor
        with torch.no_grad():
            output_tensor = self.model(input_tensor)

        # convert the output tensor to a NumPy array and extract the predicted class labels
        output_array = output_tensor.numpy()
        predicted_labels = np.argmax(output_array, axis=1)

        # apply the threshold to the output array to assign class labels
        # class_labels = np.where(output_array > 0.5, 1, 0)

        # return the predicted class labels
        return predicted_labels[0]

if __name__ == '__main__':
    inference = GreenhouseInference('../green_ai/data/trained_model.pth')
    input_data = [[70, 50, 5000, 30, 60]]
    output = inference.predict(input_data)
    print(output)