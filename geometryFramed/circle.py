'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''

from geometryFramed.geometricalABC import Geometrical2D
from geometryFramed.point import Point2
from geometryFramed.scalar import Dimension

import geometryFramed.algorithms


class Circle(Geometrical2D):
    __slots__ = ['center', 'radius']

    def __init__(self, center, radius):
        '''
        Circle having radius having center, in same frame as center.
        !!! Note radius is not a Dimension having a frame.
        '''
        assert isinstance(center, Point2) and isinstance(radius, (float, int))
        self.center = center.copy()
        self.radius = float(radius)
        self.frame = center.frame
        
    """
    def __copy__(self):
        return self.__class__(self.center, self.radius, self.frame)

    copy = __copy__
    """
    
    def __repr__(self):
        return 'Circle(center=%.2f, %.2f, radius=%.2f, frame=%s)' % \
            (self.center.x, self.center.y, self.radius, self.frame)

    """
    def _apply_transform(self, t):
        self.center = t * self.center
    """
    def translate(self, translationVector):
      " Only center is translated. "
      self.center = self.center.translate(translationVector)
      self.frame = translationVector.frame
      # ensure self is in new frame of translationVector
      

    def intersect(self, other):
        return other._intersect_circle(self)

    def connect(self, other):
      assert self.frame == other.frame and self.frame is not None
      return other._connect_circle(self)

    


    def perp(self, point):
      ''' 
      Vector perpendicular to circle in direction of point (outward from center.)
      
      When point is center, result is (0,0) null vector.
      
      Vector difference between center point and point.
      '''
      assert self.frame == point.frame
      return point - self.center
    
    
    def radiusDimension(self):
      ''' Radius as Dimension. '''
      return Dimension(self.radius, self.frame)



    def _intersect_point2(self, other):
        return geometryFramed.algorithms.intersectPoint2Circle(other, self)

    def _intersect_line2(self, other):
        return geometryFramed.algorithms.intersectLine2Circle(other, self)

    def _connect_point2(self, other):
        return geometryFramed.algorithms.connectPoint2Circle(other, self)

    def _connect_line2(self, other):
        result = geometryFramed.algorithms.connectCircleLine2(self, other)
        if result:
            return result._swap()

    def _connect_circle(self, other):
        return geometryFramed.algorithms.connectCircleCircle(other, self)

