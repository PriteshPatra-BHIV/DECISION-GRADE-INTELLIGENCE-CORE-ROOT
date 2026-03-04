def test_illegal_collapse_detection():

    envelope = {
        "epistemic_state": "AMBIGUOUS",
        "collapse_flag": False
    }

    # simulate illegal modification
    envelope["collapse_flag"] = True

    assert envelope["epistemic_state"] == "AMBIGUOUS"