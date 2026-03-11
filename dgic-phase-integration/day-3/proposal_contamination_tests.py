def test_orchestrator_does_not_mutate_core(adapter, core):

    original_state = core.get_state()

    for _ in range(50):
        adapter.propose_decision()

    new_state = core.get_state()

    assert original_state == new_state