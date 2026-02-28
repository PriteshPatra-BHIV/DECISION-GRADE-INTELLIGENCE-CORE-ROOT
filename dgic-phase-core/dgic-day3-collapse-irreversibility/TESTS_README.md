# Test Suite

## Running Tests

### Run all tests
```bash
pytest -v
```

### Run specific test folders
```bash
pytest irreversibility_tests/ -v
pytest stress-tests/ -v
```

### Run specific test file
```bash
pytest stress-tests/test_ambiguity_persistence.py -v
```

## Test Summary

**Total: 6 tests**

### Irreversibility Tests (3)
- `test_illegal_collapse_from_known` - Ensures collapse from Known state is blocked
- `test_evidence_required` - Validates evidence requirement
- `test_append_only_behavior` - Verifies ledger append-only behavior

### Stress Tests (3)
- `test_ambiguity_persistence` - Tests ambiguity archiving
- `test_multiple_collapses` - Validates hash chain integrity
- `test_mutation_attack` - Detects ledger tampering

## Status
✅ All tests passing
