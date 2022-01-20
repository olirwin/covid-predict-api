from datetime import datetime
from typing import Dict, Tuple, Optional, List

from .exceptions import ModelNotFoundError
from ml.models import Model


class ModelLibrary :
    """
    A container class to store ML models in memory.
    """
    max_models: int
    cur_models: int
    model_library: Dict[str, Tuple[datetime, Model]]

    def __init__(self, max_models : int) :
        self.max_models = max_models
        self.cur_models = 0
        self.model_library = {}

    def add_model(self, model : Model) -> None :
        """
        Adds a model to the library. If the maximum number of models has
        been reached, removes the oldest model in the library.

        :param model: the model to add
        """
        # Check current number of models
        if self.cur_models == self.max_models :
            # Remove oldest model
            sorted_models = [name for (name, (date, _)) in sorted(self.model_library.items(),
                                                                  key = lambda item : item[1][0])]

            oldest_model = sorted_models[0]
            del self.model_library[oldest_model]

            self.cur_models -= 1

        self.model_library[model.filename] = (datetime.now(), model)
        self.cur_models += 1

    def get_model(self, model_name : str) -> Optional[Model] :
        """
        Returns the model if it exists in the library.
        Updates last use time in library.

        :param model_name: the name of the model to return
        :return: the model from the library or None if the model does not exist
        """

        if model_name not in self.model_library :
            return None

        _, model = self.model_library[model_name]
        self.model_library[model_name] = (datetime.now(), model)

        return model

    def remove_model(self, model_name : str) -> None :
        """
        Removes the model from the library

        :param model_name: the name of the library
        :raises ModelNotFoundError: if the model does not exist in the library
        """

        if model_name not in self.model_library :
            raise ModelNotFoundError("Model is not in library")

        del self.model_library[model_name]
        self.cur_models -= 1

    def list_model_names(self) -> List[str] :
        return [name for name in self.model_library]
