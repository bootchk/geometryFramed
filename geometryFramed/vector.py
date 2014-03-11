'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''
# This must be at beginning and provides Python3 division semantics for the '/' operator
# See also below, where we define __div__ equal to __truediv__ for certain classes.
from __future__ import division

import math



# Python2
# from operator import div, floordiv, truediv

from .coordinate import Coordinate2
from .scalar import Dimension
# see circular imports at end of this file



class Vector2(Coordinate2):
    '''
    A Vector is a Coordinate
    with math operations.
    
    Vectors:
    - operations: 
    -- add
    -- sub
    - vector operations:
    -- dot
    -- cross
    - magnitude
    - direction
    '''
    
    def __repr__(self):
        return 'Vector2(%.2f, %.2f, %s)' % (self.x, self.y, self.frame)
    
    def __bool__(self):
      ''' 
      Python special method for checking truth value. 
      A vector is not a null vector if its Coordinate2 is not zero.
      '''
      # Note Python2 syntax for super() is compatible with Python3 but not vice versa: can't use super() here.
      return super(Vector2, self).__bool__()
      
    
    __nonzero__ = __bool__  # Python2
    
    def __neg__(self):
        return Vector2(-self.x,
                        -self.y,
                        self.frame)
    
    # __pos__ = __copy__
    
    
    def __add__(self, other):
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        if isinstance(other, Vector2):
            # Vector + Vector -> Vector
            # Vector + Point -> Point
            if self.__class__ is other.__class__:
                _class = Vector2
            else:
                _class = Point2
            return _class(self.x + other.x,
                          self.y + other.y,
                          self.frame)
        else:
            assert hasattr(other, '__len__') and len(other) >= 2
            return Vector2(self.x + other[0],
                           self.y + other[1],
                           self.frame)
            
    __radd__ = __add__
    
       
    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other[0]
            self.y += other[1]
        return self

    def __sub__(self, other):
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        if isinstance(other, Vector2):
            # Vector - Vector -> Vector
            # Vector - Point -> Point
            # Point - Point -> Vector
            # !!! Point subtraction is defined but not Point addition
            if self.__class__ is other.__class__:
                _class = Vector2
            else:
                _class = Point2
            return _class(self.x - other.x,
                          self.y - other.y,
                          self.frame)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(self.x - other[0],
                           self.y - other[1])

   
    def __rsub__(self, other):
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        if isinstance(other, Vector2):
            return Vector2(other.x - self.x,
                           other.y - self.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(other.x - self[0],
                           other.y - self[1])

    def __mul__(self, other):
        # assert type(other) in (int,, float)
        assert isinstance(other, Dimension)
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        return Vector2(self.x * other.value,
                       self.y * other.value,
                       self.frame)

    __rmul__ = __mul__

    def __imul__(self, other):
        assert type(other) in (int, float)
        self.x *= other
        self.y *= other
        return self

    
    
    """
    Python2: 
    def __div__(self, other):
      
        # assert type(other) in (int, float)
        assert isinstance(other, Dimension)
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        return Vector2(self.x / other.value,
                       self.y / other.value,
                       self.frame)


    def __rdiv__(self, other):
        assert type(other) in (int, float)
        return Vector2(other / self.x,
                       other / self.y,
                       self.frame)
    """

    def __floordiv__(self, other):
        assert type(other) in (int, float)
        return Vector2(self.x // other,
                       self.y // other,
                       self.frame)


    def __rfloordiv__(self, other):
        assert type(other) in (int, float)
        return Vector2( other // self.x,
                        other // self.y,
                        self.frame)

    def __truediv__(self, other):
        assert isinstance(other, Dimension)
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        return Vector2( self.x / other.value,
                        self.y / other.value,
                        self.frame)


    def __rtruediv__(self, other):
        assert type(other) in (int, float)
        return Vector2( other / self.x,
                        other / self.y,
                        self.frame)
    """
    Note above: from __future__ import division.
    These aliases support Python2, which only expects __div__  to implement the '/' operator (and not __truediv__)
    """
    __div__ = __truediv__
    __rdiv__ = __rtruediv__
    

    '''
    Coercion
    '''
    def asPoint2(self):
      return Point2(self.x, self.y, self.frame)
    
    
    '''
    Magnitude.
    
    !!! len() is not magnitude.
    len(Vector2) is 2, i.e. len() is count of elements in Vector2 as a sequence.
    
    !!! abs() is not similar to abs for scalars: not a change in sign, but change in type.
    See positive() for sign change.
    '''
      
    def __abs__(self):
      ''' Magnitude, length, distance from (0,0) '''
      return Dimension(math.sqrt(self.x ** 2 + self.y ** 2), self.frame)

    " Alias abs() operator as magnitude() method. I.E. length of vector. "
    magnitude = __abs__


    def magnitude_squared(self):
        ''' A variant 'magnitude' '''
        # TODOLOW Dimension
        return self.x ** 2 + \
               self.y ** 2
               
               
    def manhattanLength(self):
      ''' 
      Another variant magnitude.
      
      Note that Qt implements this on QPoint, but a point is NOT a vector. 
      '''
      return abs(self.x) + abs(self.y)
      
    
    def positive(self):
      ''' Copy of self with same magnitude but positive signed components. '''
      return Vector2(abs(self.x), abs(self.y), self.frame)
    
    
    def positiveComponent(self):
      '''
      Copy of self having positive or zero components equal to max of zero and original component.
      I.E. if vector is in positive quadrant, return it,
      else return 'projection' into positive quadrant.
      '''
      return Vector2(max(0, self.x), max(0, self.y), self.frame)

      
      
    '''
    Normal is another vector in same direction but magnitude 1.
    
    No normalize() in place.
    '''

    def normal(self):
        '''
        Unit vector in same direction. 
        Copy.
        If self has zero length, result is copy self.
        '''
        d = abs(self)
        if d != Dimension(0, self.frame):
            result = Vector2(self.x / d.value, 
                           self.y / d.value,
                           self.frame)
        else:
            result = self.copy()
        
        assert abs(result).near(Dimension(1.0, self.frame)) or abs(result).near(Dimension(0, self.frame)), str(abs(result))             
        return result


    def rotate(self, theta):
      ''' Return self rotated by angle in radians where positive angle is clockwise '''
      xprime = self.x * math.cos(-theta) - self.y * math.sin(-theta)
      yprime = self.x * math.sin(-theta) + self.y * math.cos(-theta)
      self.x = xprime
      self.y = yprime
      return self
    
    
    def normalizeDirectionTo(self, other):
      '''
      Return copy of self rotated by angle that brings other onto x-axis. 
      '''
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      result = self.copy()
      result.rotate(other.angleTo(Vector2(1, 0, self.frame)))
      return result
      

    
    def dot(self, other):
        " Inner or scalar product (Wikipedia) "
        assert isinstance(other, Vector2)
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        return Dimension(value=self.x * other.x + self.y * other.y, frame=self.frame)
               
    " alias "
    scalarProduct = dot
    
    
    def cross(self):
        return Vector2(self.y, -self.x)

    def reflect(self, other):
        # assume other is normal
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        assert isinstance(other, Vector2)
        d = 2 * (self.x * other.x + self.y * other.y)
        return Vector2(self.x - d * other.x,
                       self.y - d * other.y)

    def angle(self, other):
        '''
        Positive (unsigned) scalar that is angle of self to other, in radians.
        Range [0, pi]
        !!! Doesn't tell which vector is ahead of the other: use atan2 for that.
        '''
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        assert self.magnitude().value > 0
        assert other.magnitude().value > 0
        return math.acos(self.dot(other) / (self.magnitude()*other.magnitude()))


    def angleToXAxis(self):
      ''' 
      Signed scalar angle in radians to the x-axis.
      Range [-pi, pi] 
      
      Implementation note: params to atan2 y, x is in reverse order !!!
      '''
      return math.atan2(self.y, self.x)
    
    
    def angleTo(self, other):
      '''
      Signed scalar angle in radians of self to other.
      Angle in range [-2 pi, 2 pi]
      '''
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      return other.angleToXAxis() - self.angleToXAxis()
    
      
    def project(self, other):
        ''' Vector that is projection of self onto other. '''
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        n = other.normal()
        return self.dot(n)*n


    def perp(self):
      ''' 
      Vector that is:
      - orthogonal (i.e. perpendicular) to self
      - same length as self
      - from direction of self to direction of perp requires left turn.
      
      antiPerp is simply -perp().  antiPerp requires right turn.
      '''
      return Vector2(-self.y, self.x, self.frame)
    
    
    def unitPerpBySignOf(self, handednessSign):
      ''' Perp (left turning) if handednessSign is positive, else antiperp (right turning.) '''
      if handednessSign >= 0:
        return self.perp().normalize()
      else:
        return -self.perp().normalize()
      
    
    def scalarProjection(self, other):
      '''
      Scalar projection (wikipedia) of self onto other.
      
      Scalar projection is magnitude of self.projection(other).
      Sign is significant:  Negative means in opposite direction of other.
      
      NOT equivalent to abs(self.project(other)) since that is always positive.
      '''
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      ## return Dimension(value=self.dot(other/other.magnitude()), frame=self.frame)
      return self.dot(other/other.magnitude())
    

    def isInDirectionOf(self, other):
      " Is self direction within 90 degrees left or right of other direction."
      return self.scalarProjection(other) >= Dimension(0, self.frame)
    
      
    def roundedInt(self):
      ''' 
      Copy that is:
      - rounded to nearest int. 
      - coords are ints.
      '''
      return Vector2(int(round(self.x)),
                    int(round(self.y)),
                    self.frame)
      
    def inverse(self):
      # TODOLOW not invertible if zero.
      return Vector2(1.0/self.x, 1.0/self.y, self.frame)


# circular
from geometryFramed.point import Point2