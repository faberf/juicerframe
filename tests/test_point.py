
import unittest
from juicerframe.point import PointList, Point
from itertools import product

class TestPoint(unittest.TestCase):
    
    def test_compatible(self):
        l = [
            Point({"a":1, "b":1}, ("hi0",)),
            Point({"a":1, "b":1}, ("hi1",)),
            Point({"b":1}, ("hi2",)),
            Point({"b":1, "c":1}, ("hi3",)),
            Point({"d":1}, ("hi4",)),
        ]
        
        self.assertTrue(Point.compatible(*l))
        
    def test_incompatible(self):
        l1 = [
            Point({"g":1,"a":1, "b":1}, ("hi0",)),
            Point({"g":2,"a":1, "b":1}, ("hi1",)),
            Point({"g":3,"b":1}, ("hi2",)),
            Point({"g":4,"b":1, "c":1}, ("hi3",)),
            Point({"g":5,"d":1}, ("hi4",)),
        ]
        
        l2 = [
            Point({"g":6,"a":1, "b":1}, ("hi0",)),
            Point({"g":7,"a":1, "b":1}, ("hi1",)),
            Point({"g":8,"b":1}, ("hi2",)),
            Point({"g":9,"b":1, "c":1}, ("hi3",)),
            Point({"g":10,"d":1}, ("hi4",)),
        ]
        
        for p1, p2 in product(l1,l2):
            self.assertFalse(Point.compatible(p1, p2))
            self.assertFalse(Point.compatible(p2, p1))
    

    def test_sum(self):
        p1 = Point({"a":1, "b":1}, ("hi0",))
        p2 = Point({"b":1, "c":1}, ("hi3",))
        
        s1 = Point.sum(p1,p2)
        s2 = Point.sum(p2,p1)
        
        shouldcoords = {"a":1,"b":1,"c":1}
        
        for s in s1, s2:
            self.assertEqual(s.coords, shouldcoords)
        
        self.assertEqual(s1.values, ("hi0", "hi3"))
        self.assertEqual(s2.values, ("hi3", "hi0"))
    
    def test_product(self):
        l1 = [
            Point({"a":0, "b":0}, ("hi0",)),
            Point({"a":1, "b":0}, ("hi1",)),
            Point({"a":2, "b":0}, ("hi2",)),
            Point({"a":3, "b":0}, ("hi3",)),
            Point({"a":4}, ("hi4",)),
        ]
        
        
        l2 = [
            Point({"b":0}, ("hi0",)),
            Point({"b":1}, ("hi1",)),
            Point({"b":2}, ("hi2",)),
            Point({"b":3}, ("hi3",)),
            Point({"b":4}, ("hi4",)),
        ]
        
        should = PointList([
            Point({"a":0, "b":0}, ("hi0","hi0")),
            Point({"a":1, "b":0}, ("hi1","hi0")),
            Point({"a":2, "b":0}, ("hi2","hi0")),
            Point({"a":3, "b":0}, ("hi3","hi0")),
            Point({"a":4,"b":0}, ("hi4","hi0")),
            Point({"a":4,"b":1}, ("hi4","hi1")),
            Point({"a":4,"b":2}, ("hi4","hi2")),
            Point({"a":4,"b":3}, ("hi4","hi3")),
            Point({"a":4,"b":4}, ("hi4","hi4")),
        ])
        
        ps1 = PointList(l1)
        ps2 = PointList(l2)
        
        self.assertEqual(PointList.product(ps1, ps2), should)
    
    def test_make_list(self):
        
        l = [1, 2, 3, PointList([
            Point({"b":0}, ("hi0",)),
            Point({"b":1}, ("hi1",)),
            Point({"b":2}, ("hi2",)),
            Point({"b":3}, ("hi3",)),
            Point({"b":4}, ("hi4",)),
        ])]
        
        
        should = PointList([
            Point({"b":0}, ([1, 2, 3, 'hi0'],)),
            Point({"b":1}, ([1, 2, 3, 'hi1'],)),
            Point({"b":2}, ([1, 2, 3, 'hi2'],)),
            Point({"b":3}, ([1, 2, 3, 'hi3'],)),
            Point({"b":4}, ([1, 2, 3, 'hi4'],)),
        ])
        
        self.assertEqual(PointList.make(l), should)