import pytest
import pandas as pd
from src.use_cases.automl_facade import AutoMLFacade

def test_automl_facade_initialization():
    facade = AutoMLFacade(experiment_name="test_experiment")
    assert facade.experiment_name == "test_experiment"
    assert facade.logger is not None

def test_automl_facade_error_handling():
    facade = AutoMLFacade()
    invalid_data = pd.DataFrame() # DataFrame vacío debería fallar
    with pytest.raises(Exception):
         facade.train_and_compare_baselines(data=invalid_data, target="non_existent")
