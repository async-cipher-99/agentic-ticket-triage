from src.eval.metrics import accuracy_score, micro_f1


def test_accuracy_zero_for_empty_predictions():
    assert accuracy_score([]) == 0.0


def test_micro_f1_handles_matching_labels():
    assert micro_f1(["billing", "shipping"], ["billing"]) > 0.0


def test_micro_f1_handles_empty_inputs():
    assert micro_f1([], []) == 1.0
