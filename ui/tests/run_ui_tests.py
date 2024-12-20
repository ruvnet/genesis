#!/usr/bin/env python3
import unittest
import coverage
import sys
import os

def run_ui_tests():
    """Run only the UI-related tests."""
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
    
    # Create test suite with only UI tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add UI test cases
    suite.addTests(loader.loadTestsFromName('ui.tests.test_ui_components'))
    suite.addTests(loader.loadTestsFromName('ui.tests.test_app'))
    
    # Run tests
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
    success = run_ui_tests()
    sys.exit(0 if success else 1)
