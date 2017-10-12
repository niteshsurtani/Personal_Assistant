import unittest

class KnownGood(unittest.TestCase):
    def __init__(self, input, output):
        super(KnownGood, self).__init__()
        self.input = input
        self.output = output
    def runTest(self):
        self.assertEqual(is_prime(self.input), self.output)

def is_prime(number):
    """Return True if *number* is prime."""
    if number in (0, 1):
        return False

    for element in range(2, number):
        if number % element == 0:
            return False

    return True

# class TestStringMethods(unittest.TestCase):
#   def test_upper(self):
#       self.assertEqual('foo'.upper(), 'FOO')

#   def test_isupper(self):
#       self.assertTrue('FOO'.isupper())
#       self.assertFalse('Foo'.isupper())

#   def test_split(self):
#       s = 'hello world'
#       self.assertEqual(s.split(), ['hello', 'world'])
#       # check that s.split fails when the separator is not a string
#       with self.assertRaises(TypeError):
#           s.split(2)


def suite():
    suite = unittest.TestSuite()
    known_values = []
    for index in range(1, 10, 1):
    	known_values.append((index, is_prime(index)))

    suite.addTests(KnownGood(input, output) for input, output in known_values)
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
# suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
# unittest.TextTestRunner(verbosity=2).run(suite)