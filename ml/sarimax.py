import os
import pandas as pd
import statsmodels.api as sm

from datetime import date, timedelta
from dotenv import load_dotenv
from typing import Optional

from util.exceptions import InvalidDateError, UnfittedModelError
from .models import Model


load_dotenv()


class SarimaxModel(Model) :

    def __init__(self, region : str) :
        super(SarimaxModel, self).__init__("SARIMAX", region)

    def fit(self, input_data: pd.DataFrame) -> None :
        # Create model
        self.model = sm.tsa.statespace.SARIMAX(
            input_data,
            order = (1, 0, 0),
            trend = "c",
            seasonal_order = (1, 1, 1, 365),
            simple_differencing = True
        )
        # Fit model
        self.model.fit(maxiter = os.getenv("SARIMAX_FIT_ITER"))

        # Set flag
        self.is_fitted = True

    def predict(self, start : date, end : Optional[date]) :
        if end is None :
            end = start + timedelta(days = 5)

        if end < start :
            raise InvalidDateError("End date is anterior to start date")

        if not self.is_fitted :
            raise UnfittedModelError("Model has not been fitted")

        return self.model.predict(start, end)
