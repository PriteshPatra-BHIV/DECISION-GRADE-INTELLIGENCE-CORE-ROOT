def deterministic_consumption_test(adapter, iterations=1000):
    baseline = adapter.compute_risk_score()

    for _ in range(iterations):
        if adapter.compute_risk_score() != baseline:
            return False

    return True