'''
Geometry algorithms.

These are not private, but are generally hidden, called from similar named methods of geometrical objects,
rather than invoked directly.

Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''
import math

import point
import line
import lineSegment
from scalar import Dimension

# TODO combine these files
from intersectionAlgorithms import intersectLineSegmentsForPoints






'''
intersect Point
'''

def intersectPoint2Point2(A, B):
  '''
  Point of intersection between two points.
  
  Two points intersect iff they are the same point.
  '''
  if A == B:
    result = A.copy()
  else:
    result = None
  assert isinstance(result, point.Point2) or result is None
  return result
    
    
def intersectPoint2Line2(A, B):
  '''
  Point of intersection between a point and a line.
  
  A point intersects a line if point is on the line
  and the intersection is then the point.
  '''
  if A.connect(B).length == Dimension(0, A.frame):
    result = A
  else:
    result = None
  assert isinstance(result, point.Point2) or result is None
  return result

def intersectPoint2Circle(A, B):
  raise NotImplementedError

# TODO intersectPoint2Ellipse


'''
intersect Line
'''

'''
TODO
This is incorrect:
- degenerate case of line intersect self should return line, not a point
- fails for certain lines (horizontal or vertical???)
 which is a common problem with sloppy point slope algorithms for lines.
- may not be correct for line segments, 
do the same algorithms work for both Line and LineSegment?
'''

def intersectLine2Line2(A, B):
    d = B.v.y * A.v.x - B.v.x * A.v.y
    if d == 0:
        return None

    dy = A.p.y - B.p.y
    dx = A.p.x - B.p.x
    ua = (B.v.x * dy - B.v.y * dx) / d
    if not A._u_in(ua):
        return None
    ub = (A.v.x * dy - A.v.y * dx) / d
    if not B._u_in(ub):
        return None

    return point.Point2(A.p.x + ua * A.v.x,
                  A.p.y + ua * A.v.y,
                  A.p.frame)

''' FIXME broken '''
def intersectLine2Circle(L, C):
    
    a = L.v.magnitude_squared()
    b = 2 * (L.v.x * (L.p.x - C.center.x) + \
             L.v.y * (L.p.y - C.center.y))
    c = C.center.magnitude_squared() + \
        L.p.magnitude_squared() - \
        2 * C.center.dot(L.p) - \
        C.radius ** 2
    det = b ** 2 - 4 * a * c
    if det < 0:
        return None
    sq = math.sqrt(det)
    u1 = (-b + sq) / (2 * a)
    u2 = (-b - sq) / (2 * a)
    if not L._u_in(u1):
        u1 = max(min(u1, 1.0), 0.0)
    if not L._u_in(u2):
        u2 = max(min(u2, 1.0), 0.0)

    # Tangent
    if u1 == u2:
        return point.Point2(L.p.x + u1 * L.v.x,
                      L.p.y + u1 * L.v.y)

    return lineSegment.LineSegment2(point.Point2(L.p.x + u1 * L.v.x,
                               L.p.y + u1 * L.v.y),
                        point.Point2(L.p.x + u2 * L.v.x,
                               L.p.y + u2 * L.v.y))


'''
Intersect LineSegment
'''
  
def intersectLineSegmentLineSegment(segment1, segment2):
  '''
  Point of intersection between two line segments
  OR None when no point in common between point sets
  OR raise exception when parallel and overlap by more than a point.
  
  Implementation:
  adapt to an algorithm that takes points that define segments.
  
  ensure: a non-None result is a Point2
  '''
  # assert frame safety already checked
  # Convert from internal repr to points
  segment1Points = segment1.asPointPair()
  segment2Points = segment2.asPointPair()
  xyTuple = intersectLineSegmentsForPoints(segment1Points[0], segment1Points[1], segment2Points[0], segment2Points[1])

  if xyTuple is None:
    return None
  else:
    return point.Point2(xyTuple[0], xyTuple[1], segment1.frame)




'''
Connect
'''
  
def connectPoint2Point2(a, b):
  '''
  Connecting line segment from a point to other point.
  By definition, a line segment connects two points.
  '''
  return lineSegment.LineSegment2(a, b)
  
  
def connectPoint2Line2(P, L):
    '''
    Connecting line segment from Point P to Line L.
    
    L may be a null Line, i.e. a Point
    '''
    d = L.v.magnitude_squared()
    
    '''
    Special case: L is a null Line.
    Any point of L is closest to P.
    '''
    if d <= 0:
      return lineSegment.LineSegment2(P, L.p)
    
    assert d != 0, 'Divisor is not zero.'
    u = ((P.x - L.p.x) * L.v.x + \
         (P.y - L.p.y) * L.v.y) / d
    
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    
    return lineSegment.LineSegment2(P,
                            point.Point2(L.p.x + u * L.v.x,
                                   L.p.y + u * L.v.y,
                                   P.frame))
    

def connectPoint2Circle(P, C):
    assert isinstance(P, point.Point2)
    assert P.frame == C.frame
    
    v = P - C.center
    normalV = v.normal()
    radialV = normalV * C.radiusDimension()
    return lineSegment.LineSegment2(P, point.Point2(C.center.x + radialV.x, C.center.y + radialV.y, P.frame))
  

def connectLine2Line2(A, B):
    
    d = B.v.y * A.v.x - B.v.x * A.v.y
    if d == 0:
        # Parallel, connect an endpoint with a line
        if isinstance(B, line.Ray2) or isinstance(B, lineSegment.LineSegment2):
            p1, p2 = connectPoint2Line2(B.p, A)
            return p2, p1
        # No endpoint (or endpoint is on A), possibly choose arbitrary point
        # on line.
        return connectPoint2Line2(A.p, B)

    dy = A.p.y - B.p.y
    dx = A.p.x - B.p.x
    ua = (B.v.x * dy - B.v.y * dx) / d
    if not A._u_in(ua):
        ua = max(min(ua, 1.0), 0.0)
    ub = (A.v.x * dy - A.v.y * dx) / d
    if not B._u_in(ub):
        ub = max(min(ub, 1.0), 0.0)

    return lineSegment.LineSegment2(point.Point2(A.p.x + ua * A.v.x, A.p.y + ua * A.v.y),
                        point.Point2(B.p.x + ub * B.v.x, B.p.y + ub * B.v.y))

def connectCircleLine2(C, L):
    assert C.frame == L.frame
    d = L.v.magnitude_squared()
    assert d != 0
    u = ((C.center.x - L.p.x) * L.v.x + (C.center.y - L.p.y) * L.v.y) / d
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    aPoint = point.Point2(L.p.x + u * L.v.x, L.p.y + u * L.v.y, C.frame)
    v = (aPoint - C.center)
    vScaled = v.normal() * C.radiusDimension()
    return lineSegment.LineSegment2(point.Point2(C.center.x + vScaled.x, C.center.y + vScaled.y, C.frame),
                                     aPoint)


def connectCircleCircle(A, B):
    
    v = B.center - A.center
    d = v.magnitude()
    if A.radius >= B.radius and d < A.radius:
        #centre B inside A
        s1,s2 = +1, +1
    elif B.radius > A.radius and d < B.radius:
        #centre A inside B
        s1,s2 = -1, -1
    elif d >= A.radius and d >= B.radius:
        s1,s2 = +1, -1
    v.normalize()
    return lineSegment.LineSegment2(point.Point2(A.center.x + s1 * v.x * A.radius, A.center.y + s1 * v.y * A.radius),
                        point.Point2(B.center.x + s2 * v.x * B.radius, B.center.y + s2 * v.y * B.radius))



'''
Enclosure

TODO
'''

def isEnclosedPoint2Circle(P, C):
  ''' 
  Does point lie within circle?
  A circle is just its edge (not a partial plane of points.)
  This does not mean: does point lie on circle's edge? ( Which is intersectPoint2Circle2(). )
  
  True if magnitude of vector from circle's center to point is less than or equal to circle's radius.
  '''
  return abs(P - C.center) <= C.radius

