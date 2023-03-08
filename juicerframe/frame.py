

from juicerframe.point import Point, PointList
import time

class Pointer:
    
    def __init__(self, obj):
        self.obj = obj
    
    def set(self, new):
        self.obj = new
    
    def get(self):
        return self.obj

class SkipException(Exception):
    pass

class Cursor:
    
    def __init__(self, skip, key_path):
        self.skip = skip
        self.key_path = key_path
    
    def retrieve(self, data):
        if self.skip:
            raise SkipException
        for key in self.key_path:
            data = data[key]
        return data



class Frame:
    
    def __init__(self):
        self.plist = Pointer(PointList([Point({},{})]))
        self.cursors = PointList([Point({}, Cursor(skip = True, key_path=[]))])
    
    def __iter__(self):
        for point in self.plist.get().product(self.cursors):
            data, cursor = point.value
            try:
                retrieved = cursor.retrieve(data)
            except SkipException as e:
                continue
            yield retrieved
    
    