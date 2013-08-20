'''
'''


class Geometrical(object):
    '''
    Mixin behaviour for geometrical objects.
    Abstract base class (ABC), abstracting over dimension (2D, 3D, etc.)
    
    This is what it means to be a geometrical object: support these operations.
    Operations are 'metrical', i.e. measuring.
    '''
  
    def intersect(self, other):
      '''
      Geometrical object which is intersection of self and other.
      
      Typically a Point, but it can be otherwise.
      E.G. lineA.intersect(lineA) == lineA
      '''
      raise NotImplementedError


    def connect(self, other):
      '''
      The shortest LineSegment between self and other.
      
      Ensure: always a lineSegment, never None, but may have length() == 0
      '''
      raise NotImplementedError


    def distance(self, other):
      '''
      Scalar length of self.connect(other)
      '''
      return self.connect(other).length


    def nearestPoint(self, other):
      ''' 
      Point on other that is nearest self. 
      
      Implementation: second end point of directed line segment that connects self to other.
      
      TODO test cases to insure we always swap correctly.
      '''
      return self.connect(other).p2



class Geometrical2D(Geometrical):
  '''
  ABC Every subclass SHOULD reimplement.
  
  This class is not really necessary.
  The effective implementations of connect() and intersect() call this API.
  If this were not here, and you fail to effect these deferred methods,
  you would still get an exception, just not NotImplementedError.
  
  Specializes for 2D.
  '''
  def _intersect_point2(self, other):
    raise NotImplementedError
  def _intersect_line2(self, other):
    raise NotImplementedError
  def _intersect_circle(self, other):
    raise NotImplementedError
  
  def _connect_point2(self, other):
    raise NotImplementedError
  def _connect_line2(self, other):
    raise NotImplementedError
  def _connect_circle(self, other):
    raise NotImplementedError
  
  