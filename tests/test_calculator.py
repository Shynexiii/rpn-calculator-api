import unittest
from core.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_operand(self):
        self.calc._add_operand('3')
        self.assertEqual(self.calc.stack, [3])

    def test_compute_addition(self):
        self.calc.stack = [3, 5]
        self.calc._compute('+')
        self.assertEqual(self.calc.stack, [8])

    def test_get_result_single_value(self):
        self.calc.stack = [4.0]
        result = self.calc._get_result()
        self.assertEqual(result, 4.0)

    def test_is_rpn_true(self):
        expression = "3 4 2 * 1 5 - / +"
        self.assertTrue(self.calc.is_rpn(expression))

    def test_is_rpn_false(self):
        expression = "3 + 4 * 2 / ( 1 - 5 )"
        self.assertFalse(self.calc.is_rpn(expression))

    def test_to_rpn_complex(self):
        infix_expr = "3 + 4 * 2 / ( 1 - 5 )"
        rpn_expr = self.calc.to_rpn(infix_expr)
        self.assertEqual(rpn_expr, "3 4 2 * 1 5 - / +")

    def test_is_operator_true(self):
        self.assertTrue(self.calc._is_operator('+'))
        self.assertTrue(self.calc._is_operator('-'))
        self.assertTrue(self.calc._is_operator('*'))
        self.assertTrue(self.calc._is_operator('/'))

    def test_compute_division_by_zero(self):
        self.calc.stack = [3, 0]
        self.calc._compute('/')
        self.assertEqual(self.calc.stack, [float('inf')])


if __name__ == '__main__':
    unittest.main()
