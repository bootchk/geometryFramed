'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''

import math

from geometricalABC import Geometrical2D
import point
import vector
from circle import Circle
from scalar import Dimension



class Ellipse(Geometrical2D):
    '''
    Ellipse:
    - having radii along x and y axis
    - aligned with frame axis !!!
    - having center (not just at origin of frame.)
    - in same frame as center.
    '''
  
    __slots__ = ['center', 'radiusX', 'radiusY']

    def __init__(self, center, radiusX, radiusY):
       
        assert isinstance(center, point.Point2) and isinstance(radiusX, (float, int)) and isinstance(radiusY, (float, int))
        self.center = center.copy()
        self.radiusX = float(radiusX)
        self.radiusY=float(radiusY)
        self.frame = center.frame
  
    
    def __repr__(self):
        return 'Ellipse(center=%.2f, %.2f, radiusX=%.2f, radiusY=%.2f, frame=%s)' % \
            (self.center.x, self.center.y, self.radiusX, self.radiusY, self.frame)


    '''
    Geometry
    
    !!! Reimplement Geometrical2D.connect() and intersect()
    
    Implementation is to:
    - get my scaled circle
    - similarly scale other,
    - delegate to scaled circle
    - unscale the result
    '''

    # TODO broken: implement similarly as connect
    def intersect(self, other):
      raise NotImplementedError
      return other._intersect_circle(self)


    def connect(self, other):
      '''
      Connection to ellipse is connection to circle of ellipse, scaled.
      '''
      assert self.frame == other.frame and self.frame is not None
      
      #print "other", other
      
      # assert center
      translationVector = vector.Vector2(-self.center.x, -self.center.y, "TEMP")
      inverseTranslationVector = vector.Vector2(self.center.x, self.center.y, self.frame)
      scaleVector = self.getScaleVectorToCircle()
      inverseScaleVector = scaleVector.inverse()
      #print "Scalevector", scaleVector
      
      centeredCircle = self.circleFor()
      #print "centeredCircle", centeredCircle
      
      # Translate and scale other to circle's temp frame
      scaleDownOther = other.translate(translationVector)
      scaleDownOther = scaleDownOther.stretch(scaleVector)
      #print "scaledTranslatedOther", scaleDownOther
      
      # connectionToCircle = scaleDownOther._connect_circle(centeredCircle)
      connectionToCircle = centeredCircle.connect(scaleDownOther)

      #print "connection", connectionToCircle

      
      # Scale both ends of connection out of circle's temp frame
      """
      point2 = connectionToCircle.p2
      scaledUpPoint2 = point2.stretch(-scaleVector)
      scaledUpPoint2 = scaledUpPoint2.translate(inverseTranslationVector)
      
      connectionToEllipse = LineSegment2(connectionToCircle.p, scaledUpPoint2)
      """
      connectionToEllipse = connectionToCircle.stretch(inverseScaleVector)
      connectionToEllipse = connectionToEllipse.translate(inverseTranslationVector)
      #print "scaled connection", connectionToEllipse
      # TODOLOW why need swap?
      connectionToEllipse._swap()
      return connectionToEllipse


    '''
    Strangeness:
    Unlike other geometrical classes,
    we don't invoke algorithms directly,
    but via self's reimplemented connect() and intersect()
    '''
    def _intersect_point2(self, other):
        return self.intersect(other)

    def _intersect_line2(self, other):
        return self.intersect(other)

    

    def _connect_point2(self, other):
      return self.connect(other)

    def _connect_line2(self, other):
      return self.connect(other)

    def _connect_circle(self, other):
      return self.connect(other)
    
    def _connect_ellipse(self, other):
      " Frightening to consider how to do it. "
      raise NotImplementedError
    
    
    
    def circleFor(self):
      " Circle enclosed by minorRadius centered at origin of TEMP frame. "
      # No need to translate, just set at 0,0
      # No need to scale, just use min
      return Circle(point.Point2(0,0, "TEMP"), min(self.radiusX, self.radiusY))
      # ensure center is near 0,0


    def getScaleVectorToCircle(self):
      " Vector that unstretches ellipse to circle. "
      if self.radiusX <= self.radiusY:
        scale = self.radiusX / self.radiusY
        result = vector.Vector2(1, scale, "TEMP")
      else:
        scale = self.radiusY / self.radiusX
        result = vector.Vector2(scale, 1, "TEMP")
      assert scale <= 1
      return result
      """
      else:
        result = vector.Vector2(1, self.radiusY / self.radiusX, "TEMP")
      """

    def tangent(self, point):
      '''
      Arbitrary length vector tangent to ellipse at point on (near) ellipse.
      '''
      if self.radiusX > self.radiusY:
        # major axis on X axis
        b = self.minorRadius()
        a = self.majorRadius()
      else:
        # major axis on Y axis
        a = self.minorRadius()
        b = self.majorRadius()
        
      vectorFromCenterToPoint = point - self.center
      if vectorFromCenterToPoint.y == 0:
        # Avoid division by zero
        # point is on X axis, tangent is Y axis
        result = vector.Vector2(0, 1, self.frame)
      else:
        slopeOfTangent = - ( b**2 * vectorFromCenterToPoint.x) / (a**2 * vectorFromCenterToPoint.y)
        result = vector.Vector2(1, slopeOfTangent, self.frame)
      return result
    
    
    def perp(self, point):
      '''
      Outward pointing normal to ellipse at point on (near) ellipse.
      '''
      vectorFromCenterToPoint = point - self.center
      # In upper half, normal points up
      if vectorFromCenterToPoint.angleToXAxis() > 0:
        return -self.tangent(point).perp()
      else:
        return self.tangent(point).perp()
    
    # Scrap
    def perp2(self, point):
      ''' 
      Vector perpendicular to self in direction of point (outward from center.)
      
      When point is center, result is (0,0) null vector.
      '''
      # TODO, for an ellipse, point is ON ellipse
      # return perpendicular to tangent at point.
      
      # TODOLOW this is tangent, not normal
      assert self.frame == point.frame
      vectorFromCenterToPoint = point - self.center
      angleToXAxis = vectorFromCenterToPoint.angleToXAxis()
      denominator = math.sqrt((self.minorRadius() * math.cos(angleToXAxis))**2 + (self.majorRadius() * math.sin(angleToXAxis))**2)
      x = self.majorRadius() * math.sin(angleToXAxis) / denominator
      y = self.minorRadius() * math.cos(angleToXAxis) / denominator
      return vector.Vector2(x, y, self.frame)  - vector.Vector2(point.x, point.y, self.frame)
      # - vector.Vector2(self.center.x, self.center.y, self.frame)
    
    
    def minorRadius(self):
      return min(self.radiusX, self.radiusY)
    
    def majorRadius(self):
      return max(self.radiusX, self.radiusY)
    
    def minorRadiusDimension(self):
      ''' minor radius as Dimension. '''
      return Dimension(self.minorRadius(), self.frame)


    '''
    TODO move to an ABC for all closed geometrical objects.
    '''
    def isEnclosed(self, other):
      assert isinstance(other, point.Point2)
      
      # algorithms.isEnclosedPoint2Circle(P, C)
      # Work in progress
      raise NotImplementedError
    

