import ezdxf
import sys


def connectPoints(infile):
    print("connecting Points")
    getAllPointCoords(infile)

def getAllPointCoords(infile):
    try:
        source = ezdxf.readfile(infile)
    except IOError:
        print("Not a DXF file or generic IO Err")
    except ezdxf.DXFStructureError:
        print("Invalid or corrupt DXF File")
        sys.exit(2)
    print("gathering points")
    points = []
        
    msp = source.modelspace()
    out = ezdxf.new( units=0)
    outMsp = out.modelspace()
    for e in msp:
        points.append((e.dxf.location.x, e.dxf.location.y))
    for point in points:
        print(point)

    outMsp.add_spline(points)
    out.saveas("testPointConnect.dxf")