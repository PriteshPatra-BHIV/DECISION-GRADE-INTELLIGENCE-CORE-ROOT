import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Cleanup test files before and after each test"""
    files = [
        Path("ambiguity_archive.json"),
        Path("collapse_ledger.json")
    ]
    
    # Cleanup before test
    for f in files:
        if f.exists():
            f.unlink()
    
    yield
    
    # Cleanup after test
    for f in files:
        if f.exists():
            f.unlink()
