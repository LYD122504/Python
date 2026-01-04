import unittest
import stock
class TestStock(unittest.TestCase):
    def test_create(self):
        s = stock.stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
    def test_cost(self):
        s = stock.stock('GOOG', 100, 490.1)
        self.assertEqual(s.cost, 49010.0)
    def test_sell(self):
        s = stock.stock('GOOG', 100, 490.1)
        s.sell(40)
        self.assertEqual(s.shares, 60)
    def test_set_price(self):
        s = stock.stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
            s.shares = '100'# 断言异常一定会被抛出不然测试失败
if __name__ == '__main__':
    unittest.main()