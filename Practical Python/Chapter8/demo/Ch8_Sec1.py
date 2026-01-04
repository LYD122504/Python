def add(x, y):
    assert isinstance(x, int), 'Expected int'
    assert isinstance(y, int), 'Expected int'
    return x + y
print(add(2,3))
def add(x, y):
    return x + y

assert add(2,2) == 4

import simple
import unittest
class TestAdd(unittest.TestCase):
    def test_simple(self):
        r=simple.add(2,3)
        self.assertEqual(r, 5)
    def test_str(self):
        # Test with strings
        r = simple.add('hello', 'world')
        self.assertEqual(r, 'helloworld')
if __name__ == '__main__':
    unittest.main()