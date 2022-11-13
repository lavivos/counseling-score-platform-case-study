"""
Baseline improvement strategy model
"""

import pandas as pd
from .base_improvement_strategy import BaseImprovementStrategy


class DefaultImprovementStrategy(BaseImprovementStrategy):
    """
    Default improvement strategy
    """
    default_strategy_config = {
        "studytime": 4,
        "absences": 0,
        "Dalc": 1,
        "Walc": 1,
        "freetime": 5,
        "schoolsup": "yes",
        "famsup": "yes",
        "paid": "yes"
    }

    def __init__(self,
                 X: pd.DataFrame,
                 y=None,
                 strategy_config=None,
                 inference_model=None):
        if strategy_config is None:
            strategy_config = self.default_strategy_config
        super().__init__(X=X,
                         y=y,
                         strategy_name="DefaultImprovementStrategy",
                         strategy_config=strategy_config,
                         inference_model=inference_model)
        self.actionable_features = list(strategy_config.keys())

    def apply_improvement_strategy(self):
        """Implement default strategy"""
        student_impovement_data = {key: [] for key in self.actionable_features}
        for student_id in self.X.index:
            for feature, target_value in self.strategy_config.items():
                if feature in self.metadata["binary"]:
                    complexity_val = 1 if self.X_target.loc[student_id][
                        feature] != target_value else 0
                    student_impovement_data[feature].append(complexity_val)
                elif feature in self.metadata["numeric"]:
                    complexity_val = abs(
                        self.X_target.loc[student_id][feature] -
                        target_value) if self.X_target.loc[student_id][
                            feature] != target_value else 0
                    student_impovement_data[feature].append(complexity_val)
                self.X_target.at[student_id, feature] = target_value

        for feature, values in student_impovement_data.items():
            self.X_target[f"{feature}_implevel"] = values

        self.infer_and_setup_expected_grades()
        self.setup_performance_gain()
        self.setup_heuristic_complexity()

    def infer_and_setup_expected_grades(self):
        """Infer the expected grades under the current strategy"""
        model_features = list(self.X.columns)
        expected_grades = self.inference_model.predict(
            self.X_target[model_features])
        self.X_target["ExpectedGrade"] = expected_grades

    def setup_heuristic_complexity(self):
        """Setup a mesure of student improvability's complexity"""
        self.X_target["Complexity"] = self.X_target[[
            f"{feat}_implevel" for feat in self.actionable_features
        ]].sum(axis=1)

    def setup_performance_gain(self):
        """Setup a mesure of counseling value"""
        self.X_target[
            "PerformanceGain"] = self.X_target["ExpectedGrade"] - self.y
