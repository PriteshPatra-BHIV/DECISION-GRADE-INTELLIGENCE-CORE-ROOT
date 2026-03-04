def test_no_ambiguity_override(adapter):
    """
    Enforcement must not force collapse of ambiguous state.
    """

    snapshot = adapter._harness.generate_snapshot()

    if snapshot.epistemic_state == "AMBIGUOUS":
        risk = adapter.compute_risk_score()

        # Even if high risk, collapse must remain False
        assert snapshot.collapse_flag is False