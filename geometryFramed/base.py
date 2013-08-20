'''
From "Computational Geometry in C" by O'Rourke.
Note there the discussion of correctness and special cases for the alternative  (slope algorithm.)

In what follows:
- all formal parameters are points.
- pairs of points define line segments (!!! not lines)

These are not "frame safe".  Points must be in the same frame.

These are algorithms in the sense they are not methods of objects.
Most users should not call these algorithms directly.
They are usually used by object oriented methods at a higher level.


>>> from pyeuclid import Point2
>>> a = Point2(0, 0, 'foo')
>>> b = Point2(0, 1, 'foo')
>>> c = Point2(0.1, 1, 'foo')

>>> isVertical(a,b)
True

>>> isVertical(a,c)
False

'''


def area2(a, b, c):
  '''
  Twice the signed integer area of triangle determined by three points.
  
  Usually only the sign is used.
  
  >>> from base import *
  >>> from pyeuclid import Point2
  >>> a = Point2(0,0, 'foo')
  >>> b = Point2(0,1, 'foo')
  >>> c = Point2(2,2, 'foo')
  
  Negative if a,b,c are oriented CW.
  >>> area2(a,b,c)
  -2
  
  Positive if a,b,c are oriented CCW.
  >>> area2(a,c,b)
  2
  
  Area of same point is zero.
  >>> area2(a,a,a)
  0
  
  Area of colinear points is zero.
  >>> d = Point2(0,2, 'foo')
  >>> area2(a,b,d)
  0
  
  
  
  '''
  # Check parameters here at the lowest level of call tree
  # But this causes circular import problems.
  # assert isinstance(a, Point2) and isinstance(b, Point2) and isinstance(c, Point2)
  assert a.frame == b.frame and b.frame == c.frame
  
  return a.x * b.y - a.y * b.x + \
         a.y * c.x - a.x * c.y + \
         b.x * c.y - c.x * b.y
        

def isLeftOf(a, b, c):
  '''
  Is point a left of the line b,c ?
  '''
  return area2(a, b, c) > 0


def isColinear(a, b, c):
  '''
  True if c is on line ab.
  '''
  return area2(a, b, c) == 0
  
  

def isSegmentsIntersect(a, b, c, d):
  '''
  True if segment ab and cd intersect, properly or improperly.
  '''
  return  isSegmentsIntersectProperly(a, b, c, d) or isSegmentsIntersectImproperly(a, b, c, d)
    

def isSegmentsIntersectProperly(a, b, c, d):
  '''
  True if segment ab and cd intersect properly:
  both segments are split.
  '''
  
  '''
  Eliminate improper cases: one segment is not split
  i.e. end of segment is on other segment
  '''
  if isColinear(a, b, c) or \
     isColinear(a, b, d) or \
     isColinear(c, d, a) or \
     isColinear(c, d, b) :
    return False
  else:
    # Python: ^ is boolean xor
    # c and d on different sides of ab and
    # a and b on different sides of cd
    return (isLeftOf(a, b, c) ^ isLeftOf(a, b, d)) and (isLeftOf(c, d, a) ^ isLeftOf(c, d, b))  


def isSegmentsIntersectImproperly(a, b, c, d):
  return isBetween(a, b, c) or isBetween(a, b, d) or isBetween(c, d, a) or isBetween(c, d, b)


def isBetween(a, b, c):
  '''
  True if c is on segment (!!! not line) ab.
  '''
  if not isColinear(a, b, c):
    return False
  # else colinear to line ab; now check bounds of segment ab
  '''
  if ab not vertical, check betweeness on x, else on y
  '''
  if not isVertical(a, b):
    return isXBetween(a, b, c)
  else:
    return isYBetween(a, b, c)
  
  
def isVertical(a, b):
  '''
  '''
  return a.x == b.x


def isXBetween(a, b, c):
  '''
  True if x coord of c is between the x coord of a and b
  '''
  return (a.x <= c.x and c.x <= b.x) or \
         (a.x >= c.x and b.x <= c.x)
         
         
def isYBetween(a, b, c):
  '''
  True if y coord of c is between the y coord of a and b
  '''
  return (a.y <= c.y and c.y <= b.y) or \
         (a.y >= c.y and b.y <= c.y)

  