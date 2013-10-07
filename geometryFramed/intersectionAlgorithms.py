'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3


Alternative intersection algorithms for line segments.
Note that the algorithms in algorithms.py are defective: 
they are not able to return a line segment for overlapping, parallel segments,
but always return a point or None.

From "Computational Geometry" by O'Rourke, p. 249

Work in progress (not finished for parallel segments)

Frame safety not enforced: require points in same frame
'''

from geometryFramed.base import isSegmentsIntersect



def intersectLineSegmentsForPoints(a, b, c, d): # point1, point2, point3, point4):
  '''
  Coordinate pair for point of intersection between two line segments defined by two pairs of points.
  OR None when no point in common between point sets
  OR raise exception when parallel and overlap is line segment (cardinality of intersection point set > 1.)
  
  !!! Does not return a Point2, returns a tuple.
  
  Use parametric form of line segment.
  Solve system of two vector equations.
  '''
  denominator = a.x * (d.y - c.y) + \
                b.x * (c.y - d.y) + \
                d.x * (b.y - a.y) + \
                c.x * (a.y - b.y)
  
  if denominator == 0.0:
    return intersectParallelSegments(a, b, c, d)
  else: # Not parallel
    s = ( \
            a.x * (d.y - c.y) \
          + c.x * (a.y - d.y) \
          + d.x * (c.y - a.y) \
          ) / denominator
          
    t = -( \
            a.x * (c.y - b.y) \
          + b.x * (a.y - c.y) \
          + c.x * (b.y - a.y) \
          ) / denominator
          
    intersectionX = a.x + s * ( b.x -a.x)
    intersectionY = a.y + s * ( b.y - a.y)
    
    if 0.0 <= s and s <= 1.0 and 0.0 <= t and t <= 1.0:
      return intersectionX, intersectionY
    else:
      #print "Don't intersect", s, t
      return None # Not parallel and don't intersect
  
  
def intersectParallelSegments(a, b, c, d):
  '''
  Coordinate pair for point intersection of parallel segments.
  
  Either segment may be zero length (parallel to every other segment.) Reduce such segment to point if it intersects.
  
  Segments may overlap, but then their intersection is either an end point or another line segment.
  Raise exception if overlap is a line segment.
  '''
  if not isSegmentsIntersect(a, b, c, d):
    # Segments parallel but don't overlap (non-intersecting segments of same line.)
    #print "Segments parallel but don't overlap"
    return None
  else: # Is an intersection
    # Determine whether one segment is a point (improper segment.)
    #print "Segments parallel and intersect"
    if a == b:  # first segment is a point
      return a.x, a.y
    elif c == d:  # second segment is a point
      return c.x, c.y
    else:   # neither segment is point
      #print 'here3'
      return endPointIntersectSegments(a, b, c, d)


def endPointIntersectSegments(a, b, c, d):
  ''' 
  Coordinate pair for end point of segment that equals end point of second segment,
  where the other end point of segment
  OR raise exception.
  
  Require: 
  - segments are parallel,
  - do intersect
  - neither segment is a point (improper segment.)
  
  Ensure:
  - segments intersect only at end points, or exception (they intersect at a proper line segment, i.e. overlap)
  '''
  '''
  if a == c:
    if b == d:
      raise RuntimeError
    else:
  '''
  raise NotImplementedError
  return None


