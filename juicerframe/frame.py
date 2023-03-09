

import abc
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

class AbstractCursor(abc.ABC):
    
    @abc.abstractmethod
    def retrieve(self, data):
        pass

class SelectCursor(AbstractCursor):
    
    def __init__(self, key_path):
        self.key_path = key_path
    
    def retrieve(self, data):
        for key in self.key_path:
            data = data[key]
        return data

class SkipCursor(AbstractCursor):
    def retrieve(self, data):
        raise SkipException

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
        self.cursors = DerivedPointList(SelectCursor(key_path=[]))
    
    def vary(self):
        return Frame(DerivedPointList.vary(DerivedPointList(self)))
        
    
    def where(self, mask):
        f = Frame.__new__(Frame)
        
        @DerivedPointList.pointwise
        def create_cursor(cursor, m):
            if not m:
                return SkipCursor()
            return cursor
        
        f.plist = self.plist
        f.cursors = create_cursor(self.cursors, mask)
        return f
    
    def configure(self, *dict_list, **kwargs):
        
        @DerivedPointList.pointwise
        def update_data(data, _dict_list, _kwargs):
            updated = {**data}
            for d in _dict_list + [_kwargs]:
                for k, v in d.items:
                    updated[k] = v
            return updated
        
        self.plist.set(update_data(self.plist.get(), dict_list, kwargs))
        return self
    
    def select(self, key):
        f = Frame.__new__(Frame)
        
        @DerivedPointList.pointwise
        def create_cursor(cursor, k):
            return SelectCursor(cursor.key_path +  [k])
        
        f.plist = self.plist
        f.cursors = create_cursor(self.cursors, key)
        return f

    def __getitem__(self, key):
        return self.select(key)
    
    def __setitem__(self, key, value):
        return self.configure({key:value})
        
    def __iter__(self):
        for point in DerivedPointList.product(self.plist.get(),self.cursors):
            data, cursor = point.values
            try:
                retrieved = cursor.retrieve(data)
            except SkipException as e:
                continue
            yield retrieved
    
    