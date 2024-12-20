#!/usr/bin/env python3
import unittest
import coverage
import sys
import os

def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    # Start coverage measurement
    cov = coverage.Coverage(
        branch=True,
        source=['ui'],
        omit=[
            '*/tests/*',
            '*/__init__.py'
        ]
    )
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage measurement and generate report
    cov.stop()
    cov.save()
    
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML coverage report
    coverage_dir = os.path.join('ui', 'tests', 'coverage_html')
    os.makedirs(coverage_dir, exist_ok=True)
    cov.html_report(directory=coverage_dir)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)
