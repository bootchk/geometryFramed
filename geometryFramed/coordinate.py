'''
'''

from scalar import Dimension


class Coordinate2(object):
    '''
    x,y tuple in a frame.
    
    A Coordinate differs from a Point in that no math operations are defined.
    
    Even unary positive and negation are not defined.
    (Since displacing a point in a direction is a vector operation.)
    '''
  
    __slots__ = ['x', 'y', 'frame']
    __hash__ = None

    def __init__(self, x=0, y=0, frame='NoneFrame'):
        assert frame is not None
        # Frame type safety
        if isinstance(x, Dimension):
          assert frame == x.frame # Dimension in same frame
          self.x = x.value
        else:
          self.x = x
        # TODO check y frame safety
        self.y = y
        self.frame = frame

    def __copy__(self):
        return self.__class__(self.x, self.y, self.frame)

    copy = __copy__

    def __repr__(self):
        return 'Coordinate2(%.2f, %.2f, %s)' % (self.x, self.y, self.frame)

    def __eq__(self, other):
        if isinstance(other, Coordinate2):
            return self.x == other.x and \
                   self.y == other.y and \
                   self.frame == other.frame
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return self.x == other[0] and \
                   self.y == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0 or self.y != 0

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __setitem__(self, key, value):
        l = [self.x, self.y]
        l[key] = value
        self.x, self.y = l

    def __iter__(self):
        return iter((self.x, self.y))

    
    
    