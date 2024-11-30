import unittest
from example_transactions import summary

class TestExampleTransactions(unittest.TestCase):

    def test_summary(self):
        self.assertEqual(summary['IncomeTotal'], 48105.54)
        self.assertEqual(summary['IncomeCount'], 23)
        self.assertEqual(summary['ExpenseTotal'], 9835.78)
        self.assertEqual(summary['ExpenseCount'], 37)
        self.assertEqual(summary['CurrentBalance'], 38269.76)


if __name__ == '__main__':
    unittest.main()