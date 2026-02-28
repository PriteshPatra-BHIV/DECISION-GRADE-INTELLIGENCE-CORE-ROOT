#!/usr/bin/env python3
"""
Stress Test Runner
Runs all stress tests and reports results
"""

import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return result"""
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        return {
            'name': test_file,
            'passed': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    except Exception as e:
        return {
            'name': test_file,
            'passed': False,
            'output': '',
            'error': str(e)
        }

def main():
    test_files = [
        'test_ambiguity_persistence.py',
        'test_collapse_replay.py', 
        'test_ledger_mutation.py'
    ]
    
    print("Running Stress Tests...")
    print("=" * 50)
    
    results = []
    for test_file in test_files:
        print(f"Running {test_file}...")
        result = run_test(test_file)
        results.append(result)
        
        if result['passed']:
            print(f"PASSED: {test_file}")
            if result['output'].strip():
                print(f"  Output: {result['output'].strip()}")
        else:
            print(f"FAILED: {test_file}")
            if result['error']:
                print(f"  Error: {result['error'].strip()}")
        print()
    
    # Summary
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print("=" * 50)
    print(f"Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("All stress tests passed!")
        return 0
    else:
        print("Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())