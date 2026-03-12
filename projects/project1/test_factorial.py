# test_factorial.py: Unit tests for the factorial function

import unittest
from factorial import factorial  # Import the factorial function to test

class TestFactorial(unittest.TestCase):
    """
    Unit tests for the factorial function.
    """
    
    def test_factorial_0(self):
        """Test factorial of 0 as per success criteria."""
        self.assertEqual(factorial(0), 1)
    
    def test_factorial_1(self):
        """Test factorial of 1."""
        self.assertEqual(factorial(1), 1)
    
    def test_factorial_5(self):
        """Test factorial of 5 as per TASK-004."""
        self.assertEqual(factorial(5), 120)
    
    def test_factorial_10(self):
        """Test factorial of 10 for edge cases within recursion limits."""
        self.assertEqual(factorial(10), 3628800)
    
    # Note: We don't test invalid inputs here as error handling is in main.py;
    #       Instead, focus on valid inputs as per the function's responsibility.

if __name__ == '__main__':
    unittest.main()