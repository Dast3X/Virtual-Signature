#!/usr/bin/env python3
import importlib.util
import os
import sys
import time
import unittest
from datetime import datetime
from io import StringIO

from PySide6.QtWidgets import QApplication


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

class TestResults:
    def __init__(self):
        self.results = []

    def add_result(self, test_file, total_tests, passed, failures, errors, time_taken):
        self.results.append({
            "test_file": test_file,
            "total_tests": total_tests,
            "passed": passed,
            "failures": failures,
            "errors": errors,
            "time_taken": time_taken
        })

    def generate_table(self):
        """Generate a markdown table with the tests results."""
        if not self.results:
            return "No tests were run."

        # Calculate total statistics
        total_tests = sum(r["total_tests"] for r in self.results)
        total_passed = sum(r["passed"] for r in self.results)
        total_failures = sum(r["failures"] for r in self.results)
        total_errors = sum(r["errors"] for r in self.results)
        total_time = sum(r["time_taken"] for r in self.results)

        # Create table header
        table = "# Test Results\n\n"
        table += f"**Run Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        table += "| Test File | Total Tests | Passed | Failed | Errors | Time (s) | Status |\n"
        table += "|-----------|-------------|--------|--------|--------|----------|--------|\n"

        # Add rows for each tests file
        for result in self.results:
            status = "PASS" if result["failures"] == 0 and result["errors"] == 0 else "FAIL"
            table += f"| {result['test_file']} | {result['total_tests']} | {result['passed']} | {result['failures']} | {result['errors']} | {result['time_taken']:.3f} | {status} |\n"

        # Add summary row
        status = "PASSED" if total_failures == 0 and total_errors == 0 else "FAILED"
        table += f"| **TOTAL** | **{total_tests}** | **{total_passed}** | **{total_failures}** | **{total_errors}** | **{total_time:.3f}** | **{status}** |\n\n"

        # Add pass rate
        pass_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        table += f"**Pass Rate:** {pass_rate:.2f}%\n"

        return table


def run_test_module(test_file):
    """Run a tests module and return the results."""
    # Extract just the filename without extension
    module_name = os.path.splitext(os.path.basename(test_file))[0]

    # Load the tests module from the file
    spec = importlib.util.spec_from_file_location(module_name, test_file)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Create a tests loader and load the tests from the module
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)

    # Redirect stdout during tests execution
    original_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    # Run the tests and time them
    start_time = time.time()
    result = unittest.TextTestRunner(stream=sys.stdout, failfast=False, verbosity=2).run(suite)
    end_time = time.time()
    time_taken = end_time - start_time

    # Restore stdout
    sys.stdout = original_stdout

    # Calculate statistics
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    return {
        "total_tests": total_tests,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "time_taken": time_taken,
        "output": captured_output.getvalue()
    }


def find_test_files():
    """Find all test_*.py files in the scripts directory relative to this script."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(base_dir, "scripts")

    if not os.path.exists(scripts_dir):
        print(f"Directory not found: {scripts_dir}")
        return []

    test_files = []
    for file in os.listdir(scripts_dir):
        if file.startswith("test_") and file.endswith(".py"):
            test_files.append(os.path.join(scripts_dir, file))
    return test_files


def main():
    # Create a QApplication instance if needed
    app = QApplication.instance() or QApplication(sys.argv)

    # Find all tests files
    test_files = find_test_files()
    if not test_files:
        print("No tests files found in the current directory.")
        return

    # Initialize results tracker
    results = TestResults()

    # Run each tests file
    for test_file in test_files:
        print(f"\nRunning tests in {test_file}...")
        test_result = run_test_module(test_file)

        # Add results to tracker
        results.add_result(
            os.path.basename(test_file),
            test_result["total_tests"],
            test_result["passed"],
            test_result["failures"],
            test_result["errors"],
            test_result["time_taken"]
        )

        # Print basic results
        print(f"Tests: {test_result['total_tests']}, "
              f"Passed: {test_result['passed']}, "
              f"Failed: {test_result['failures']}, "
              f"Errors: {test_result['errors']}, "
              f"Time: {test_result['time_taken']:.3f}s")

        # Print output if there were failures or errors
        if test_result["failures"] > 0 or test_result["errors"] > 0:
            print("\nTest output:")
            print(test_result["output"])

    # Generate and print the results table
    table = results.generate_table()
    print("\n" + table)

    # Write results to a file with UTF-8 encoding to support emoji
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write(table)
    print("\nResults saved to test_results.md")


if __name__ == "__main__":
    main()
