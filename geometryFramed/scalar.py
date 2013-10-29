'''
Copyright 2013 Lloyd K. Konneker, 2006 Alex Holkner

Licensed under the LGPLv3
'''
# This must be at beginning and provides Python3 division semantics for the '/' operator
# See also below, where we define __div__ equal to __truediv__ for certain classes.
from __future__ import division


class Dimension(object):
  '''
  Signed scalar with frame safety.
  Commonly the result of certain operations on vectors i.e. magnitude, scalarProjection.
  '''

  def __init__(self, value, frame='NoneFrame'):
    assert isinstance(value, (int, float))
    assert frame is not None
    self.value = value
    self.frame = frame
  
  
  def __repr__(self):
    return 'Dimension(' + str(self.value) + ', ' + repr(self.frame) + ')'
  
  def __str__(self):
    return str(self.value)
  
  def __mul__(self, other):
    ''' Multiplication by pure number or other Dimension '''
    if isinstance(other, Dimension):
      # Multiplication of two Dimensions returns a Dimension (not a pure number?)
      assert self.frame == other.frame, 'Frames differ'
      return Dimension(self.value * other.value,
                     self.frame)
    else:
      # Multiplication by pure number stays in same frame. 
      assert type(other) in (int, float)
      return Dimension(self.value * other,
                     self.frame)
      
      
  def __truediv__(self, other):
    ''' Division by pure number or other Dimension '''
    if isinstance(other, Dimension):
      # Division of two Dimensions returns a pure number (ratio)
      assert self.frame == other.frame, 'Frames differ'
      return self.value / other.value
    else:
      # Division by pure number stays in same frame. 
      assert type(other) in (int, float)
      return Dimension(self.value / other,
                     self.frame)
      
  __div__ = __truediv__
    
  def __neg__(self):
    return Dimension(-self.value,
                     self.frame)
    
  '''
  Rich comparisons
  '''
  
  def checkFrames(self, other):
    if not isinstance(other, Dimension):
      raise TypeError("Can't compare Dimension to other types.")
    assert self.frame == other.frame, 'Frames differ'
    pass
    
  def __eq__(self, other):
    ''' Unsafe for floats. '''
    self.checkFrames(other)
    return self.value == other.value

  def __ne__(self, other):
    ''' Unsafe for floats. '''
    self.checkFrames(other)
    return self.value != other.value
  
  def __lt__(self, other):
    self.checkFrames(other)
    return self.value < other.value
  
  def __gt__(self, other):
    self.checkFrames(other)
    return self.value > other.value
  
  def __le__(self, other):
    self.checkFrames(other)
    return self.value <= other.value
  
  def __ge__(self, other):
    self.checkFrames(other)
    return self.value >= other.value
    
    
  def near(self, other):
    ''' Floating point safe check for equality '''
    assert self.frame == other.frame
    return abs(self.value - other.value) < 0.000000000001
  
  
  """
  Python2
  def __cmp__(self, other):
    ''' 
    Frame safe, rich comparison between dimensions.
    
    !!! Note this is not lt, gt, etc.
    '''
    assert isinstance(other, Dimension), str(type(other))
    assert self.frame == other.frame
    if self.value < other.value:
      return -1
    elif self.value == other.value:
      return 0
    else:
      return 1
  """
  
    
  def __abs__(self):
    ''' abs of Dimension is positive Dimension. '''
    return Dimension(abs(self.value), self.frame)
  
  
  def isPositive(self):
    ''' A caller cannot compare to pure zero without a type error, so implement isPositive(). '''
    return self.value >= 0