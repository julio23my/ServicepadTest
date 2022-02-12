from fizzbuzz import exchange_for_fizz_buzz
import unittest

class TestExangeFizzBuzz(unittest.TestCase):
    """
    Code a program (in python) that displays the numbers from 1 to 100 on the
    screen, substituting the multiples of 3 for the word "fizz", the multiples of 5 for
    "buzz" and the multiples of both, that is, the multiples of 3 and 5, by the word
    "fizz buzz".

        - n = string number
    """

    def test_fizz_buzz(self):
        actual = exchange_for_fizz_buzz(20)
        expected = ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz']
        self.assertEqual(actual, expected)

    def test_no_number(self):
        text_enter = 'abc'
        with self.assertRaises(ValueError) as exception_context:
            exchange_for_fizz_buzz(n=text_enter)
        self.assertEqual(
            str(exception_context.exception),
            "Please insert a valid number  "
        )
        
    
    def test_range_numbers(self):
        text_enter = 10**5
        with self.assertRaises(ValueError) as exception_context:
            exchange_for_fizz_buzz(n=text_enter)
        self.assertEqual(
            str(exception_context.exception),
            "needs to be in the range between of 1 to 100 "
        )
