import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from node_array import FatNodeArray

class TestFatNodeArray(unittest.TestCase):
    
    def test_add_element(self):
        arr = FatNodeArray()
        arr.add(5)
        self.assertEqual(arr.get(0)['value'], 5)  

    def test_insert_element(self):
        arr = FatNodeArray()
        arr.add(5)
        arr.insert(0, 10)
        self.assertEqual(arr.get(0)['value'], 10)  
        self.assertEqual(arr.get(1)['value'], 5)

    def test_remove_element(self):
        arr = FatNodeArray()
        arr.add(5)
        arr.add(10)
        arr.remove(0)
        self.assertEqual(arr.get(0)['value'], 10)  

    def test_pop_element(self):
        arr = FatNodeArray()
        arr.add(5)
        arr.add(10)
        popped_element = arr.pop()['value'] 
        self.assertEqual(popped_element, 10)

    def test_multiple_versions(self):
        arr = FatNodeArray()
        arr.add(5)
        arr.add(10)
        arr.add(15)
        arr.remove(1)
        self.assertEqual(arr.get(0)['value'], 5)  
        self.assertEqual(arr.get(1)['value'], 15)

if __name__ == '__main__':
    unittest.main()