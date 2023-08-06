from abc import ABC, abstractmethod

import numpy as np


class Model(ABC):
    @abstractmethod
    def train(self, *args):
        pass

    @abstractmethod
    def predict(self, x):
        pass


class SupervisedModel(Model):
    @abstractmethod
    def train(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass


class UnsupervisedModel(Model):
    @abstractmethod
    def train(self, x):
        pass

    @abstractmethod
    def predict(self, x):
        pass


class ConstantModel(Model):
    def __init__(self, y):
        self.y = y

    def train(self):
        pass

    def predict(self, x):
        return np.ones(len(x)) * self.y
