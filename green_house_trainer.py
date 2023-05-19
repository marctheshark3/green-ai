#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 19:03:12 2023

@author: marctheshark
"""

import torch
import torch.nn as nn
import torch.optim as optim

class GreenhouseTrainer:
    def __init__(self, model=None, criterion=None, optimizer=None, lr=0.001):
        self.model = model or GreenhouseNet()
        self.criterion = criterion or nn.CrossEntropyLoss()
        self.optimizer = optimizer or optim.Adam(self.model.parameters(), lr=lr)

    def _run_epoch(self, data, mode):
        if mode == 'train':
            self.model.train()
            loader = torch.utils.data.DataLoader(data, batch_size=32, shuffle=True)
        else:
            self.model.eval()
            loader = torch.utils.data.DataLoader(data, batch_size=32, shuffle=False)

        running_loss = 0.0
        running_corrects = 0

        for batch in loader:
            inputs, labels = batch
            self.optimizer.zero_grad()

            with torch.set_grad_enabled(mode == 'train'):
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = self.criterion(outputs, labels)

                if mode == 'train':
                    loss.backward()
                    self.optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(data)
        epoch_acc = running_corrects.double() / len(data)

        return epoch_loss, epoch_acc

    def train(self, train_data):
        return self._run_epoch(train_data, mode='train')

    def validate(self, val_data):
        return self._run_epoch(val_data, mode='val')

    def test(self, test_data):
        return self._run_epoch(test_data, mode='test')

    def save_model(self, filename):
        torch.save(self.model.state_dict(), filename)


if __name__ == '__main__':
    from green_ai.create_loader import GreenhouseDataset
    from green_ai.models.feed_forward import GreenhouseNet
    
    # create the data loader
    dataset = GreenhouseDataset(n_samples=365*12*5, use_case='daily')

    # specify the sizes of the train, val, and test sets
    train_size = int(0.7 * len(dataset))
    val_size = int(0.2 * len(dataset))
    test_size = len(dataset) - train_size - val_size

    # use random_split to split the dataset into train, val, and test sets
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, val_size, test_size])

    trainer = GreenhouseTrainer()
    
    # train the model
    for epoch in range(10):
        train_loss, train_acc = trainer.train(train_dataset)
        val_loss, val_acc = trainer.validate(val_dataset)
        print(f'Epoch {epoch+1}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_loss={val_loss:.4f}, val_acc={val_acc:.4f}')
    
    # test the model
    test_loss, test_acc = trainer.test(test_dataset)
    print(f'Test loss={test_loss:.4f}, Test accuracy={test_acc:.4f}')

    trainer.save_model('../green_ai/data/trained_model.pth')
