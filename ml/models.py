from typing import Optional
from pathlib import Path

import joblib
import pandas as pd

from abc import ABC, abstractmethod


class Model(ABC) :
    """
    Abstract class to expose model behaviour
    """

    model_name : str
    region_name : str
    is_fitted : bool
    file_root : str
    last_true_date : str

    def __init__(self, model_name : str, region_name : str) :
        self.model_name = model_name
        self.region_name = region_name
        self.is_fitted = False
        self.model = None
        self.file_root = f"{self.model_name}_{self.region_name}"

    @abstractmethod
    def fit(self, input_data : pd.DataFrame) -> None :
        """
        Fit the model with the given input data

        :param input_data: the data to fit the model to
        """
        pass

    @abstractmethod
    def predict(self, start : str, end : Optional[str]) :
        """
        Predict the values between set dates

        :param start: the start date
        :param end: the end date, optional, default to 5 days after start
        :return: the predicted values for the date range
        :raises UnfittedModelError: if the model was not fitted before the prediction
        :raises InvalidDateError: if the end date is before the start date
        """
        pass

    def save(self) -> None :
        """
        Saves the model to a local file
        """

        joblib.dump(self.model, filename = self.filename, compress = True)

    def load(self, filename : Optional[str] = None) -> None :
        """
        Loads the model contained in the local field.

        :param filename: the name of the file if not the default name
        """

        filename = f"{self.file_root}.joblib" if filename is None else filename

        self.model = joblib.load(filename = filename)
        self.is_fitted = True

