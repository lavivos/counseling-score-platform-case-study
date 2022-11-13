"""
Grade model base interface. This interface could either be used to implement
models with potential online training or only online inference.
"""

from abc import ABC, abstractmethod


class BaseGraderModel(ABC):
    """Base class for the grading model"""

    def __init__(self, X, y=None):
        self.X = X
        self.y = y
        self.regressor = None

    @abstractmethod
    def predict(self, X):
        """
        Abstract method that conducts inference
        """
