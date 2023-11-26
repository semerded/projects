import unittest, ComparatorFunctions as comp


class test_ComparatorFunctions(unittest.TestCase):

    def test_isEven(self):
        self.assertTrue(comp.isEven(0))
        self.assertFalse(comp.isEven(1))
        self.assertTrue(comp.isEven(2))
        
    def test_isNumber(self):
        self.assertTrue(comp.isNumber(1))
        self.assertTrue(comp.isNumber(-1))
        self.assertTrue(comp.isNumber(545.976))
        self.assertFalse(comp.isNumber(True))
        self.assertFalse(comp.isNumber("teststring"))
        self.assertFalse(comp.isNumber([1, 2, 3]))
        
    def test_isNumberString(self):
        self.assertTrue(comp.isNumberString("12345"))
        self.assertFalse(comp.isNumberString("abc123"))
        self.assertFalse(comp.isNumberString("abcdefg"))
      
    def test_greater(self):
        self.assertTrue(comp.greater(3, 1))
        self.assertTrue(comp.greater(True, False)) 
        
        self.assertFalse(comp.greater(0, 0)) 
        self.assertFalse(comp.greater(5, 8)) 
        
    def test_smaller(self):
        self.assertTrue(comp.smaller(1, 3))
        self.assertTrue(comp.smaller(False, True)) 
        
        self.assertFalse(comp.smaller(0, 0)) 
        self.assertFalse(comp.smaller(8, 5)) 
    
    


if __name__ == '__main__':
    unittest.main()
