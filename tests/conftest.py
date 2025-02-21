import sys
import types

# Mocking the pycaret module
if "pycaret.classification" not in sys.modules:
    dummy_classification = types.ModuleType("pycaret.classification")
    dummy_classification.load_model = lambda path: None
    dummy_classification.predict_model = lambda model, data: None

    dummy_pycaret = types.ModuleType("pycaret")
    dummy_pycaret.classification = dummy_classification

    sys.modules["pycaret"] = dummy_pycaret
    sys.modules["pycaret.classification"] = dummy_classification
    
