'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''
from PyQt4.QtGui import QPolygonF

from point import Point2
from lineSegment import LineSegment2
from typeConvert import asPoint2, unitXAxis, unitYAxis


class Rectangle(object):
  '''
  Rectangle.
  A polygon of four sides where each pair of sides is at right angle.
  Need not be aligned with axis of CS.
  '''

  def __init__(self, polygon):
    '''
    Constructor
    '''
    assert isinstance(polygon, QPolygonF)
    self.polygon = polygon
  
  
  def corners(self):
    ''' 
    Tuple of corners as Point2.  
    Order: first corner is upper left.  Clockwise.
    '''
    pointTuple = [asPoint2(pt, 'Scene') for pt in self.polygon]
    # Actually returns 5 points
    return pointTuple
  
  
  def diagonals(self):
    '''
    Tuple of diagonals as LineSegment2
    Order: upper left to lower right diagonal, then lower left to upper right.
    '''
    corners = self.corners()
    return ( LineSegment2(corners[0], corners[2]), LineSegment2(corners[3], corners[1]) )
  
  
  def topSide(self):
    corners = self.corners()
    return LineSegment2(corners[0], corners[1])
  
  
  def orthogonal(self, inDirectionOfPoint):
    '''
    Orthogonal of rect in direction of a point.
    I.E. outward pointing vector orthogonal to side nearest point.
    Point can be inside, outside, or on the rect.
    Orthogonal is NOT a line passing through the point.
    The orthogonal is just a vector.
    
    Implementation: four combinations of left and right of diagonals.
    That is, divide rect into quadrants by its two diagonals.
    Each quadrant has an orthogonal.
    
    The rect is aligned in its own coordinate system,
    but need not be aligned in the scene.
    '''
    assert isinstance(inDirectionOfPoint, Point2)
    
    diagonals = self.diagonals()
    upperLeftToLowerRightDiagonal = diagonals[0]
    lowerLeftToUpperRightDiagonal = diagonals[1]
    
    resultFrame = inDirectionOfPoint.frame
    
    if upperLeftToLowerRightDiagonal.isLeftOf(inDirectionOfPoint):
      if lowerLeftToUpperRightDiagonal.isLeftOf(inDirectionOfPoint):
        # nearest top side
        axis = -unitYAxis(resultFrame)
      else:
        #print  "nearest right side"
        #print inDirectionOfPoint, lowerLeftToUpperRightDiagonal
        axis = unitXAxis(resultFrame)
    else: # isRightOf upperLeftToLowerRight
      if lowerLeftToUpperRightDiagonal.isLeftOf(inDirectionOfPoint):
        # nearest left side
        axis =  -unitXAxis(resultFrame)
      else:
        #print  "nearest bottom side"
        axis =  unitYAxis(resultFrame)
    
    # Assert axis is unit vector in one of the four cardinal directions in the CS of the aligned rect.
    # Now rotate it by the rotation of rect in the scene.
    
    # !!! Use the top, since leftSide of the rectangle for a line is zero length
    topSide = self.topSide()
    assert abs(topSide).isPositive()
    angle = topSide.angleToXAxis()
    #print "Topside of rect", self.topSide(), "Angle to X axis", angle
    return axis.rotate(angle)
    
    """
    OLD and bogus?
    # translate points into coordinate systems of diagonals
    point1 = (inDirectionOfPoint - corners[0]).asPoint2()
    point2 = (inDirectionOfPoint - corners[3]).asPoint2()
    
    if magnitude_to_line(corners[0], corners[2], point1) < 0:
      # right of first diagonal
      if magnitude_to_line(corners[3], corners[1], point2) < 0 :
        # right of second diagonal
        # FIXME this is for aligned rect
        # return orthogonal to bottom side
        return unitXAxis(Point2.frame)
      else:
        return -unitXAxis(Point2.frame)
    else:
      if magnitude_to_line(corners[3], corners[1], point2) < 0 :
        return unitYAxis(Point2.frame)
      else:
        return -unitYAxis(Point2.frame)
    """
      
      