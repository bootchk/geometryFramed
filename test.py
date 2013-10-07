'''
To run all test/foo.txt test files:

>cd geometry
>python test.py
'''
if __name__ == "__main__":
  
    import doctest
    
    " Invoke tests (separate from the modules, and .txt ) of each module in package"
    print("Running all tests in test directory")
    doctest.testfile('test/testCoordinate.txt')
    doctest.testfile('test/testScalar.txt')
    doctest.testfile('test/testPoint.txt')
    doctest.testfile('test/testVector.txt')
    #doctest.testfile('test/testLine.txt')
    doctest.testfile('test/testLineSegment.txt')
    #doctest.testfile('test/testCircle.txt')
    doctest.testfile('test/testEllipse.txt')
    doctest.testfile('test/testGeometry.txt')
    doctest.testfile('test/testFrameless.txt')
    doctest.testfile('test/testInheritance.txt')


    """
    Work in progress: I don't understand doctest well enough.
    import geometry
    doctest.testmod(geometryFramed)
    """