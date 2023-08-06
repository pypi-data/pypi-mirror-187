"""
Module with the template classes for models
"""
from abc import ABC, abstractmethod

import numpy as np


class Model(ABC):  # pylint: disable=too-few-public-methods
    """
    Generic model class
    """

    @abstractmethod
    def predict(self, x_pred):
        """
        Prediction function
        :param x_pred: the input dataset, a pandas dataframe or numpy array
        :return:
        """


class SupervisedModel(Model):
    """
    Generic supervised model class
    """

    @abstractmethod
    def train(self, x_train, y_train):
        """

        :param x_train:
        :param y_train:
        :return:
        """


class UnsupervisedModel(Model):
    """
    Generic supervised model class
    """

    @abstractmethod
    def train(self, x_train):
        """

        :param x_train:
        :return:
        """


class ConstantModel(Model):  # pylint: disable=too-few-public-methods
    """
    Constant model: dummy model for basic tests.
    """

    def __init__(self, y_val):
        self.y_val = y_val

    def predict(self, x_pred):
        return np.ones(len(x_pred)) * self.y_val
