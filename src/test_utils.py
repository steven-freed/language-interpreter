import unittest
import utils


class TestUtils(unittest.TestCase):

    def test_isfloat(self):
        true = utils.isfloat("123.45")
        false = utils.isfloat("hey")
        self.assertTrue(true)
        self.assertFalse(false)

    def test_isstr(self):
        false = utils.isstr("123.45")
        true = utils.isstr('"hey"')
        self.assertTrue(true)
        self.assertFalse(false)
    
    def test_isbool(self):
        false1 = utils.isbool("123.45")
        false2 = utils.isbool("hey")
        true1 = utils.isbool("TRUE")
        true2 = utils.isbool("FALSE")
        self.assertFalse(false1)
        self.assertFalse(false2)
        self.assertTrue(true1)
        self.assertTrue(true2)


unittest.main()