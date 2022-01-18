from pydantic import BaseModel
from typing import Optional

from datetime import datetime, date


class PredictionBody(BaseModel) :
    """
    Base Model for prediction request bodies
    """

    start_date : date
    end_date : Optional[date]
    region : Optional[str] = "FRA"
