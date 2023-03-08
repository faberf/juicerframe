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
    
    def __init__(self, points):
        super().__init__(points)
    
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
    
    @staticmethod
    def product(*pointlists):
        newpoints = []
        for ps in product(*pointlists):
            for p in ps:
                if not issubclass(type(p), Point):
                    raise TypeError
            try:
                newpoints.append(Point.sum(*ps))
            except IncompatibleException as e:
                continue
        return PointList(newpoints)
    
    @staticmethod
    def vary(iterable_like, axis):
        return PointList.make(list(iterable_like)).map(lambda x: x[0]).distribute(axis)

    @staticmethod
    def make(obj):
        t = type(obj)
        if t is PointList:
            return obj
        if not t in _flatten:
            return PointList([Point({}, (obj,))])
        prepared = [PointList.make(component) for component in _flatten[t](obj)]
        prod = PointList.product(*prepared)
        return prod.map(_unflatten[t]).map(lambda x : (x,))
        
        
    def map(self, func):
        return PointList([p.map(func) for p in self])
    
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for p1, p2 in zip(self, other):
            if p1 != p2:
                return False
        return True
