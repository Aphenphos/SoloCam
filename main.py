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
            fPointAccuracy = 0
            match machine:
                case "burny":
                    fPointAccuracy = 4
                case "atr":
                    fPointAccuracy = 4
                case "torch":
                    fPointAccuracy = 3
            coords = getCoords(infile, machine, fPointAccuracy)
            parseCoords(coords, machine, fPointAccuracy)
        case "d":
            connectPoints(infile)

main()