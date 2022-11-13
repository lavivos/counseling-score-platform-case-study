"""
Imporvement strategy base interface.

Practically, a strategy represents a set of actionable feature modifications
that academic advisors could apply in their program to improve students conditions.
Having those modifications and the grading model, we can estimate the effect of such
improvements on students performance, therefore allowing an estimation of student improvability
depending on the advisor's strategy. In addition, we get a mesure of the complexity
having the modifications done for each student.
"""

from abc import ABC, abstractmethod
from uuid import uuid4
from .utils import get_metadata
from .base_grader_model import BaseGraderModel
from .baseline_grader_model import BaselineGraderModel


class BaseImprovementStrategy(ABC):
    """Base class for an improvement strategy"""

    def __init__(self,
                 X,
                 y,
                 strategy_config=None,
                 strategy_name=None,
                 inference_model: BaseGraderModel = None):
        self.X = X
        self.y = y
        self.strategy_config = strategy_config
        # strategy name defined by the user or set by default
        self.strategy_name = strategy_name
        if strategy_name is None:
            self.strategy_name = str(uuid4())
        # inference model used to compute expected students grades
        # after the application of the improvement strategy
        self.inference_model = inference_model
        if self.inference_model is None:
            self.inference_model = BaselineGraderModel(X)
        # features type metadata
        self.metadata = get_metadata()
        # X_target is meant to represent the student's new feature values
        # after applying the improvement strategy
        self.X_target = X.copy()

    @abstractmethod
    def apply_improvement_strategy(self):
        """
        Abstract method that fits the grading model
        """
