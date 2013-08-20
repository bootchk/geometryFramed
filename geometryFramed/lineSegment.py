'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''

import line
import algorithms

from base import isLeftOf



class LineSegment2(line.Line2):
    '''
    Directed line segment.
    TODO, make swapping NOT change the direction of a line segment??
    '''
  
    def __init__(self, *args):
        self.constructLinelike(*args)
        
        # assert constructLinelike insured all args of same frame
        self.frame = args[0].frame
        
        # It is not an exception to have zero length.
        
    
    def __repr__(self):
      ''' !!! repr looses accuracy but reconstructs object. '''
      points = self.asPointPair()
      return 'LineSegment2(' + repr(points[0]) + ', ' + repr(points[1]) + ')'
      
      """
      <%.2f, %.2f> to <%.2f, %.2f>)' % \
            (self.p.x, self.p.y, self.p.x + self.v.x, self.p.y + self.v.y)
      """
      
    def __str__(self):
      points = self.asPointPair()
      return 'LineSegment2 from' + str(points[0]) + " to " + str(points[1])
    
    def _u_in(self, u):
        return u >= 0.0 and u <= 1.0

    def __abs__(self):
        return abs(self.v)

    def magnitude_squared(self):
        return self.v.magnitude_squared()

    def _swap(self):
        # used by connect methods to switch order of points
        self.p = self.p2
        self.v *= -1
        return self
      
    def isLeftOf(self, point):
      '''
      Is point left of directed line segment self?
      '''
      assert self.frame == point.frame, 'Mismatched frames: ' + str(self.frame) + ', ' + str(point.frame)
      # convert to three points
      return isLeftOf(*self.asPointPair(), c=point)
      

    length = property(lambda self: abs(self.v))
    
    def asPointPair(self):
      ''' Pair of Point2 defining self. '''
      return (self.p.copy(), self.p + self.v)
      
      
    '''
    Connect and intersect are inherited.
    '''

    " _intersect_point(self, other) inherited. "
    
    '''
    Don't use intersectLine2Line2().
    Because it doesn't return the correct thing for parallel, overlapping linesegments???
    Use simpler, correct algorithm.
    '''
    def _intersect_line(self, other):
      return algorithms.intersectLineSegmentLineSegment(other, self)


    '''
    Limited transformation methods.
    '''
      
    def stretch(self, vector):
      ''' Stretched copy by stretching component points. '''
      assert self.frame == vector.frame
      return LineSegment2( self.p.stretch(vector), self.p2.stretch(vector))
    
    def translate(self, vector):
      '''
      Translate by vector between frames.
      Implementation: translate component points.
      '''
      assert self.frame != vector.frame
      result = LineSegment2( self.p.translate(vector), self.p2.translate(vector))
      assert result.frame == vector.frame
      return result
      
      
      
    """
    WIP
    def isIntersect(self, other):
      ''' Does other intersect self. '''
      assert self.frame == other.frame  # Segments are in same frame
      if isinstance(other, LineSegment2):
        return intersectLineSegments(self, other)
      else:
        raise NotImplementedError

    def isIntersectLineSegments(segment1, segment2):
    """





      