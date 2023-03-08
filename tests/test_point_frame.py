
import unittest
from juicerframe.frame import Frame

class TestFrame(unittest.TestCase):
    
    def test_init(self):
        f = Frame()
        self.assertEqual(list(f), [{}])