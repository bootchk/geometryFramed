'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''
from geometryFramed.coordinate import Coordinate2
from geometryFramed.geometricalABC import Geometrical2D
# see circular imports at end of this file


class Point2(Geometrical2D, Coordinate2):
    '''
    A Point is a Coordinate 
    supplemented with math operations
    and geometry behaviour.
    '''
  
    def __repr__(self):
      return 'Point2(%.2f, %.2f, %s)' % (self.x, self.y, self.frame)

    def __str__(self):
      ## return '(%.2f,%.2f)' % (self.x, self.y)
      return '%.1f, %.1f' % (self.x, self.y)
    
    
    def asVector2(self):
      return Vector2(self.x, self.y, self.frame)
    

    '''
    Point to Point arithmetic: subtraction but not addition is defined.
    '''
  
    def __add__(self, other):
        '''
        Point + Vector is Point
        We implement Point.__add__ so that P + V does not resolve to V.__radd__ yielding Vector.
        '''
        if isinstance(other, Point2):
            raise NotImplementedError('Point addition is not defined and meaningless.')
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        assert isinstance(other, Vector2)
        return Point2(self.x + other.x,
                      self.y + other.y,
                      self.frame)
    
    
    def __sub__(self, other):
        assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
        if isinstance(other, Vector2):
            # Point - Vector -> Point
            _class = Point2
        else:
            # See below, duck type everything else as a Point2
            # Point - Point -> Vector
            _class = Vector2
      
        assert hasattr(other, '__len__') and len(other) >= 2
        return _class(self.x - other[0],
                       self.y - other[1],
                       self.frame)
  
    '''
    Specialize GeometricalABC methods.
    Delegate to other by binding my class name into a method name of other e.g. connect_'myClassName'
    This is a form of dispatch (an alternative to an: if isinstance(...): statement.)
    '''
    
    def connect(self, other):
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      return other._connect_point2(self)
    
    def intersect(self, other):
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      return other._intersect_point2(self)
    


    '''
    Class knows how to connect to and intersect with other classes.
    '''
    def _connect_point2(self, other):
      # Why is this reverse order: other, self ?
      return geometryFramed.algorithms.connectPoint2Point2(other, self)
    
    def _connect_line2(self, other):
        return geometryFramed.algorithms.connectPoint2Line2(self, other)._swap()

    def _connect_circle(self, other):
        return geometryFramed.algorithms.connectPoint2Circle(self, other)._swap()
    
    
    def _intersect_point2(self, other):
        return geometryFramed.algorithms.intersectPoint2Point2(self, other)
      
    def _intersect_line2(self, other):
        return geometryFramed.algorithms.intersectPoint2Line2(self, other)
      
    def _intersect_circle(self, other):
        return geometryFramed.algorithms.intersectPoint2Circle(self, other)
    
    
  
    
    def length(self):
      ''' 
      Points have length zero.
      So that connect().length() is zero???
      But connect always returns a LineSegment, not a point.
      '''
      return 0
    
    
    def roundedInt(self):
      ''' 
      Copy that is:
      - rounded to nearest int. 
      - coords are ints.
      '''
      return Point2(int(round(self.x)),
                    int(round(self.y)),
                    self.frame)
    

    def translate(self, vector):
      " Translate by vector between frames. "
      assert self.frame != vector.frame
      point = Point2(self.x, self.y, vector.frame)
      return point + vector

    def stretch(self, vector):
      '''
      Stretch by vector between frames.
      Does not allow flip (minus one.)
      Special case of scaling by a transform, where only one direction is scaled.
      Vector must be in same frame.
      '''
      assert self.frame == vector.frame
      assert abs(vector.x) == 1.0 or abs(vector.y) == 1.0
      if abs(vector.x) == 1.0:
        result = Point2(self.x, self.y * vector.y, vector.frame)
      else:
        result = Point2(self.x * vector.x, self.y, vector.frame)
      return result
    
from geometryFramed.vector import Vector2
import geometryFramed.algorithms