'''
'''


from geometricalABC import Geometrical2D

import point
import vector
import algorithms
from scalar import Dimension


class Line2(Geometrical2D):
    '''
    Common behavior of linelike things???
    Is an infinite line the same thing???
    
    Inherited by Ray and LineSegment.
    '''
    __slots__ = ['p', 'v']

    def __init__(self, *args):
        self.constructLinelike(self, *args)
        '''
        not assert vector.length() > 0
        I.E. a null Line2 may exist,
        and its direction methods (e.g. angle, perp) raise exceptions.
        '''

    def __copy__(self):
        return self.__class__(self.p, self.v)

    copy = __copy__

    def __repr__(self):
        return 'Line2(<%.2f, %.2f> + u<%.2f, %.2f>)' % \
            (self.p.x, self.p.y, self.v.x, self.v.y)

    p1 = property(lambda self: self.p)
    p2 = property(lambda self: point.Point2(self.p.x + self.v.x, 
                                      self.p.y + self.v.y,
                                      self.p.frame))
      
      
    def _u_in(self, u):
        return True


    '''
    Methods delegated to underlying vector.
    A Line2 is NOT a Vector, only has-a Vector.
    '''
      
    def perp(self):
      return self.v.perp()
    
    def angleToXAxis(self):
      return self.v.angleToXAxis()
    

    '''
    Geometry
    '''

    def intersect(self, other):
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      return other._intersect_line2(self)

    def connect(self, other):
      assert self.frame == other.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(other.frame)
      return other._connect_line2(self)



    def _intersect_point2(self, other):
        return algorithms.intersectPoint2Line2(other, self)
      
    def _intersect_line2(self, other):
        return algorithms.intersectLine2Line2(self, other)

    def _intersect_circle(self, other):
        return algorithms.intersectLine2Circle(self, other)


    def _connect_point2(self, other):
        return algorithms.connectPoint2Line2(other, self)

    def _connect_line2(self, other):
        return algorithms.connectLine2Line2(other, self)

    def _connect_circle(self, other):
        return algorithms.connectCircleLine2(other, self)
      
    
    def constructLinelike(self, *args):
      '''
      Construct internal representation of Line2
      Ensure self.p and self.v exist.
      
      Polymorphic in args:
        Point, Vector, multiplier
        Point, Vector
        Point, Point
        Line2
      '''
    
      if len(args) == 3:
          " 3rd arg is a multiplier. ???"
          assert isinstance(args[0], point.Point2)
          assert isinstance(args[1], vector.Vector2)
          ## assert type(args[2]) == float, str(type(args[2]))
          assert isinstance( args[2], Dimension)
          assert args[0].frame == args[1].frame
          self.p = args[0].copy()
          # TODO does division by zero raise ValueError?
          self.v = args[1] * args[2] / abs(args[1])
      elif len(args) == 2:
          assert args[0].frame == args[1].frame
          if isinstance(args[0], point.Point2) and isinstance(args[1], point.Point2):
              self.p = args[0].copy()
              self.v = args[1] - args[0]
          elif isinstance(args[0], point.Point2) and isinstance(args[1], vector.Vector2):
              self.p = args[0].copy()
              self.v = args[1].copy()
          else:
              raise TypeError, '%r %s %s' % (args, type(args[0]), type(args[1]) )
      elif len(args) == 1:
          if isinstance(args[0], Line2):
              self.p = args[0].p.copy()
              self.v = args[0].v.copy()
          else:
              raise TypeError, '%r' % (args,)
      else:
          raise TypeError, '%r' % (args,)


# TODO break this out

class Ray2(Line2):
    def __repr__(self):
        return 'Ray2(<%.2f, %.2f> + u<%.2f, %.2f>)' % \
            (self.p.x, self.p.y, self.v.x, self.v.y)

    def _u_in(self, u):
        return u >= 0.0