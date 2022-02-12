from fibonacci import fibonacci_search_recursive
import unittest

class TestFibonacci(unittest.TestCase):
    """
    Code a program (in python) that displays the fibonacci series number for the number inserted.

        - n = string number
    """

    def test_fibonnaci_find(self):
        actual = fibonacci_search_recursive(30)
        expected = 514229
        self.assertEqual(actual, expected)

    def test_no_number(self):
        text_enter = 'abc'
        with self.assertRaises(ValueError) as exception_context:
            fibonacci_search_recursive(n=text_enter)
        self.assertEqual(
            str(exception_context.exception),
            "Please insert a valid number  "
        )
        
    
    def test_range_numbers(self):
        text_enter = 40
        with self.assertRaises(ValueError) as exception_context:
            fibonacci_search_recursive(n=text_enter)
        self.assertEqual(
            str(exception_context.exception),
            "needs to be in the range between of 1 to 40 "
        )
