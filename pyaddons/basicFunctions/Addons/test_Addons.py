import unittest, Addons as add

class test_Addons(unittest.TestCase):
    
    def test_strToList(self):
        self.assertEqual(add.strToList("hello world!"), ["h", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d", "!"])