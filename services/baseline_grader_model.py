"""
Baseline grading model. For version 1, this baseline model supports online inference only.
"""

import pandas as pd
from .base_grader_model import BaseGraderModel
from .utils import load_joblib


class BaselineGraderModel(BaseGraderModel):
    """Grade inference model version 1"""
    _categotical_features = [
        "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
        "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
        "nursery", "higher", "internet", "romantic"
    ]

    def __init__(self, X: pd.DataFrame, y: pd.Series = None):
        super().__init__(X, y)
        self.model_name = "grader-model-v1"
        self.encoder_name = "grader-encoder-v1"
        self.regressor = load_joblib(
            f"./assets/models/{self.model_name}.joblib")
        self.encoder = load_joblib(
            f"./assets/models/{self.encoder_name}.joblib")

    def predict(self, X: pd.DataFrame):
        """Infere grade"""
        X.loc[:,
              self.encoder.get_feature_names_out()] = self.encoder.transform(
                  X[self._categotical_features]).toarray()
        X.drop(self._categotical_features, axis=1, inplace=True)
        return self.regressor.predict(X)
