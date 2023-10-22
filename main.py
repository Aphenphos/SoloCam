import sys
from dxfParser import *
from dxfToCam import *
from pointConnector import *
def main():
    operation = sys.argv[1]
    infile = sys.argv[2]
    match operation:
        case "c":
            print("Parsing DXF file")
            print("Parsing Coords")
            machine = sys.argv[3]
            coords = getCoords(infile)
            parseCoords(coords, machine)
        case "d":
            connectPoints(infile)

main()