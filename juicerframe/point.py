from itertools import product

class IncompatibleException(Exception):
    pass

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

class Point:
    
    def __init__(self, coords, values):
        self.coords = coords
        self.values = values
    
    @staticmethod
    def sum(*points):
        sum_coords = {}
        for point in points:
            if not issubclass(type(point), Point):
                raise TypeError
            for ax, coord in point.coords.items():
                if not ax in sum_coords:
                    sum_coords[ax] = coord
                    continue
                if sum_coords[ax] != coord:
                    raise IncompatibleException
        sum_values = sum((p.values for p in points), ())
        return Point(sum_coords, sum_values)
    
    @staticmethod
    def compatible(*points):
        try:
            Point.sum(*points)
        except IncompatibleException as e:
            return False
        return True
    
    
    def map(self, func):
        return Point(self.coords, func(self.values))
    
    def __eq__(self, __o: object) -> bool:
        return self.coords == __o.coords and self.values == __o.values


_flatten = {
    list : lambda x: x,
    dict: lambda x: [component for key, val in x.items() for component in [key,val]]
        }
_unflatten = {
    list : list,
    dict : lambda x: {key:val for key,val in pairwise(x)}
}
class PointList(list):
    
    def __init__(self, obj):
        cls = type(self)
        sup = super(PointList, cls)
        
        t = type(obj)
        if t is cls:
            sup.__init__(self, obj)
            return
        if not t in _flatten:
            if not t is Point:
                obj = Point({}, (obj,))
            sup.__init__(self, [obj])
            return
        prepared = [cls(component) for component in _flatten[t](obj)]
        prod = cls.product(*prepared)
        sup.__init__(self, prod.map(_unflatten[t]).map(lambda x : (x,)))
    
    def distribute(self, axis):
        l = PointList([])
        for point in self:
            for i, val in enumerate(point.values):
                new_coords = {**point.coords, axis:i}
                l.append(Point(new_coords, (val,)))
        return l
    
    def values(self):
        for p in self:
            yield p.values
    
    @classmethod
    def product(cls, *pointlists):
        newpoints = cls.__new__(cls)
        for ps in product(*pointlists):
            for p in ps:
                if not issubclass(type(p), Point):
                    raise TypeError
            try:
                newpoints.append(Point.sum(*ps))
            except IncompatibleException as e:
                continue
        
        return newpoints
    
    @classmethod
    def vary(cls, iterable_like, axis):
        return cls.make(iterable_like).map(lambda x: x[0]).distribute(axis)

    @classmethod
    def pointwise(cls, func):
        def inner(*args, **kwargs):
            pl = cls([args, kwargs])
            return pl.map(lambda x, y: func(*x, **y))
    
        return inner
        
    def map(self, func):
        cls = type(self)
        newpoints = cls.__new__(cls)
        for point in self:
            newpoints.append(point.map(func))
        return newpoints
    
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for p1, p2 in zip(self, other):
            if p1 != p2:
                return False
        return True


