import unittest
import pytest

from util import ModelLibrary
from util.exceptions import ModelNotFoundError
from ml import SarimaxModel


class ModelLibraryTest(unittest.TestCase) :

    def setUp(self) -> None :
        self.modelA = SarimaxModel("FRA")
        self.modelB = SarimaxModel("59")
        self.modelC = SarimaxModel("62")

    def test_library_init(self) :
        lib = ModelLibrary(2)

        self.assertEqual(2, lib.max_models, "Max models should be set")
        self.assertEqual(0, lib.cur_models, "Current models should be 0")
        self.assertEqual(0, len(lib.model_library), "Library should be empty")

    def test_add_model_adds_model(self) :
        lib = ModelLibrary(2)
        self.assertEqual(0, lib.cur_models, "Current models should be 0")
        self.assertEqual(0, len(lib.model_library), "Library should be empty")
        lib.add_model(self.modelA)
        self.assertEqual(1, lib.cur_models, "Current models should be 1")
        self.assertEqual(1, len(lib.model_library), "Library should contain 1 element")

    def test_oldest_model_is_removed_when_full(self) :
        lib = ModelLibrary(2)
        self.assertEqual(0, lib.cur_models, "Current models should be 0")
        self.assertEqual(0, len(lib.model_library), "Library should be empty")
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)
        lib.add_model(self.modelC)
        self.assertEqual(2, lib.cur_models, "Current models should be 2")
        self.assertEqual(2, len(lib.model_library), "Library should contain 2 elements")

        models = lib.model_library
        self.assertTrue(self.modelB.file_root in models, "Library should contain later models")
        self.assertTrue(self.modelC.file_root in models, "Library should contain later models")
        self.assertFalse(self.modelA.file_root in models, "Library should contain later models")

    def test_get_model_returns_model(self) :
        lib = ModelLibrary(2)
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)

        model = lib.get_model(self.modelB.file_root)

        self.assertEqual(self.modelB, model, "Returned model should be the same")

    def test_get_model_returns_none_if_no_model(self) :
        lib = ModelLibrary(2)
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)

        model = lib.get_model(self.modelC.file_root)

        self.assertIsNone(model, "Returned model should be none")

    def test_remove_model_removes_model(self) :
        lib = ModelLibrary(2)
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)

        lib.remove_model(self.modelB.file_root)

        self.assertFalse(self.modelB.file_root in lib.model_library, "Model should be removed")
        self.assertEqual(1, lib.cur_models, "Model count should be decreased")

    def test_remove_model_throws_exception_if_no_model(self) :
        lib = ModelLibrary(2)
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)

        with pytest.raises(ModelNotFoundError) :
            lib.remove_model(self.modelC.file_root)

    def test_list_model_names_returns_correct_list(self) :
        lib = ModelLibrary(2)
        lib.add_model(self.modelA)
        lib.add_model(self.modelB)

        l = lib.list_model_names()

        self.assertTrue(self.modelB.file_root in l, "Should be in list")
        self.assertTrue(self.modelA.file_root in l, "Should be in list")
        self.assertFalse(self.modelC.file_root in l, "Should not be in list")

