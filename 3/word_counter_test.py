from word_counter import word_counter
import unittest

class TestFibonacci(unittest.TestCase):
    """
    Code a program (in python) that returns a diccionary with all the counts of every word in a sentence.

        - sentence = string (Sentence)
    """

    def test_word_counter(self):
        insert = word_counter("Hi how are things? How are you? Are you a developer? I am also a developer")
        expected = {'hi': 1, 'how': 2, 'are': 3, 'things': 1, 'you': 2, 'a': 2, 'developer': 2, 'i': 1, 'am': 1, 'also': 1}
        self.assertEqual(insert,expected)

        
    def test_range_numbers(self):
        text_enter = "" 
        with self.assertRaises(ValueError) as exception_context:
            word_counter(sentence=text_enter)
        self.assertEqual(
            str(exception_context.exception),
            "Please write a sentence or word"
        )
