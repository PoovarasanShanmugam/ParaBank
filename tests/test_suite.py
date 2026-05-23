import os
import sys
import unittest

# Ensure working directory is the project root for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from runner.run_tests import ParaBankTestRunner

class ParaBankTestSuite(unittest.TestCase):
    """
    Test suite running scenarios mapped by Test Case IDs.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the test runner and prepares directories."""
        cls.runner = ParaBankTestRunner()
        cls.runner.generate_excel_documentation()
        cls.runner.prepare_directories()

    def test_TC_PB_01(self):
        """
        [TC_PB_01] Positive Flow: Successful User Registration, Sign-In, and Balance Retrieval.
        """
        print("\n=== [TEST CASE RUN] TC_PB_01: Successful Registration & Balance Parsing ===")
        exit_code = self.runner.run_tests_by_tag("@TC_PB_01")
        self.assertEqual(exit_code, 0, "BDD Scenario for TC_PB_01 failed execution.")

    def test_TC_PB_02(self):
        """
        [TC_PB_02] Negative Validation: Failed Registration - Password Mismatch.
        """
        print("\n=== [TEST CASE RUN] TC_PB_02: Failed Registration - Password Mismatch ===")
        exit_code = self.runner.run_tests_by_tag("@TC_PB_02")
        self.assertEqual(exit_code, 0, "BDD Scenario for TC_PB_02 failed execution.")

    def test_TC_PB_03(self):
        """
        [TC_PB_03] Negative Validation: Failed Registration - Missing Required Fields.
        """
        print("\n=== [TEST CASE RUN] TC_PB_03: Failed Registration - Missing Required Fields ===")
        exit_code = self.runner.run_tests_by_tag("@TC_PB_03")
        self.assertEqual(exit_code, 0, "BDD Scenario for TC_PB_03 failed execution.")

    def test_TC_PB_04(self):
        """
        [TC_PB_04] Negative Validation: Failed Sign-In - Invalid username/password.
        """
        print("\n=== [TEST CASE RUN] TC_PB_04: Failed Sign-In - Invalid Credentials ===")
        exit_code = self.runner.run_tests_by_tag("@TC_PB_04")
        self.assertEqual(exit_code, 0, "BDD Scenario for TC_PB_04 failed execution.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
