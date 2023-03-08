

import juicerframe.point
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



class DerivedPointList(juicerframe.point.PointList):
    
    def __init__(self, obj):
        cls = type(self)
        sup = super(DerivedPointList, cls)
        if type(obj) is Frame:
            sup.__init__(self, sup.product(obj.plist.get(),obj.cursors)) 
            return
            
        sup.__init__(self, obj)
    

class Frame:
    
    def __init__(self, obj= {}):
        self.plist = Pointer(DerivedPointList(obj))
        self.cursors = DerivedPointList(Cursor(skip = False, key_path=[]))
    
    def where(self, mask):
        pass
    
        
    def __iter__(self):
        for point in DerivedPointList.product(self.plist.get(),self.cursors):
            data, cursor = point.values
            try:
                retrieved = cursor.retrieve(data)
            except SkipException as e:
                continue
            yield retrieved
    
    