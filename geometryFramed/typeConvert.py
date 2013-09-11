'''
Copyright 2013 Lloyd K. Konneker

Licensed under the LGPLv3


Type conversions from our types to Qt types.

Note below the name of the parameter is name of a type (but lower case.)

This somewhat knows the internals of the types, e.g. a point is 2D location with x and y.
'''

from PyQt4.QtCore import QPointF, QPoint, QEvent
from point import Point2
from vector import Vector2
from lineSegment import LineSegment2
from scalar import Dimension



def asPoint2(qpoint, coordinateSystem):
  '''
  Not just that is has attributes x and y,
  but that it is a certain type, from Qt,
  and not one of our own types.
  '''
  assert isinstance(qpoint, QPointF) or isinstance(qpoint, QPoint) or isinstance(qpoint, QEvent)
  return Point2(qpoint.x(), qpoint.y(), coordinateSystem)

def asVector2(qpoint, coordinateSystem):
  assert isinstance(qpoint, QPointF) or isinstance(qpoint, QPoint) or isinstance(qpoint, QEvent)
  return Vector2(qpoint.x(), qpoint.y(), coordinateSystem)

  
def asQPointF(point2):
  # TODOLOW not confuse points with vectors
  # There should be Vector2.endPoint() and this should not allow Vector2 parameter
  assert isinstance(point2, Point2) or isinstance(point2, Vector2)
  # Note pyeuclid has properties, not methods x(), y()
  return QPointF(point2.x, point2.y)

def asQPoint(point2):
  '''
  Strip Point2 or Vector2 of CS.
  
  Possible loss of precision.
  '''
  assert isinstance(point2, Point2) or isinstance(point2, Vector2)
  # Note pyeuclid has properties, not methods x(), y()
  return QPoint(point2.x, point2.y)




'''
Type, Frame checking
'''

def isFrameMatch(thing, CS):
  ''' is frame of thing equal to CS? '''
  if thing.frame != CS:
    #print "CS is:", thing.frame, " but should be:", CS
    return False
  else:
    return True
  
def isPointInCS(point, CS):
  if not isinstance(point, Point2):
    #print "Should be Point2, but is:", point.__class__
    return False
  return isFrameMatch(point, CS)
  
def isVectorInCS(vector, CS):
  if not isinstance(vector, Vector2):
    #print "Should be Vector2, but is:", vector.__class__
    return False
  return isFrameMatch(vector, CS)

def isDimensionInCS(thing, CS):
  if not isinstance(thing, Dimension):
    #print "Should be Dimension, but is:", thing.__class__
    return False
  return isFrameMatch(thing, CS)
  
  

def unitYAxis(frame):
  return Vector2(0, 1, frame)

def unitXAxis(frame):
  return Vector2(1, 0, frame)

def origin(frame):
  return Point2(0, 0, frame)


'''
Mapping between frames.

General strategy for vector is: map end point and origin.
Return vector as difference between mapped end point and mapped origin
'''

def mapVectorLocalToScene(vector, mapper):
  '''
  Map a bound vector from one CS to another.
  Direction of vector is preserved.
  Length of vector may be scaled.
  
  !!! A bound vector is NOT a line segment or ray.
  It has no location but is rooted at 0,0.
  Simply mapping the end point of vector is NOT sufficient.
  Algorithm is: map end points and create vector as difference of end points.
  '''
  assert vector.frame == 'Local'
  mappedEndPoint = mapper.mapToScene(asQPointF(vector))
  mappedOriginPoint = mapper.mapToScene(QPointF(0, 0))
  difference = mappedEndPoint - mappedOriginPoint # QPointF operation
  return asVector2(difference, 'Scene')


def mapVectorSceneToLocal(vector, mapper):
  '''
  '''
  assert vector.frame == 'Scene'
  mappedEndPoint = mapper.mapFromScene(asQPointF(vector))
  mappedOriginPoint = mapper.mapFromScene(QPointF(0, 0))
  difference = mappedEndPoint - mappedOriginPoint # QPointF operation
  return asVector2(difference, 'Local')


def mapIntVectorLocalToScene(vector, mapper):
  '''
  Same as above but vector is integer.
  Where mapper will only map integer.
  '''
  mappedEndPoint = mapper.mapToScene(asQPoint(vector))
  mappedOriginPoint = mapper.mapToScene(QPoint(0, 0))
  difference = mappedEndPoint - mappedOriginPoint # QPoint operation
  return asVector2(difference, 'Scene')

def mapVectorToParent(vector, mappingFunction):
  '''
  Map a bound vector from one CS to another.
  Direction of vector is preserved.
  Length of vector may be scaled.
  
  !!! A bound vector is NOT a line segment or ray.
  It has no location but is rooted at 0,0.
  Simply mapping the end point of vector is NOT sufficient.
  '''
  mappedEndPoint = mappingFunction(asQPointF(vector))
  mappedOriginPoint = mappingFunction(QPointF(0, 0))
  difference = mappedEndPoint - mappedOriginPoint # QPointF operation
  return asVector2(difference, 'Local')


'''
Map Point2 to Point2 between frames.
'''
def mapIntPointLocalToScene(point, mapper):
  ''' Typically View to Scene. '''
  # assert point is int
  return asPoint2(mapper.mapToScene(asQPoint(point)), 'Scene')
  
def mapPointLocalToScene(point, mapper):
  ''' Typically View to Scene. '''
  # assert point is int
  return asPoint2(mapper.mapToScene(asQPointF(point)), 'Scene')

def mapPointFromScene(point, mapper, newCS):
  return asPoint2(mapper.mapFromScene(asQPointF(point)), newCS)

def mapPointToParent(point, mappingFunction):
  # We don't distinguish the various Local CS's: new point is in Local CS of the parent
  return asPoint2(mappingFunction(asQPointF(point)), "Local")



def mapLineSegmentToParent(segment, mapper):
  origin = mapPointToParent(segment.p, mapper.mapToParent)
  vector = mapVectorToParent(segment.v, mapper.mapToParent)
  result = LineSegment2(origin, vector)
  return result