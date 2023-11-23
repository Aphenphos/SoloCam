import sys
from dxfParser import *
from dxfToCam import *
from pointConnector import *
from Estimate import *
def main():
    operation = sys.argv[1]
    match operation:
        case "c":
            infile = sys.argv[2]
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
            quality = 4
            coords = getCoords(infile, machine, fPointAccuracy, quality)
            parseCoords(coords, machine, fPointAccuracy)
        case "d":
            infile = sys.argv[2]
            connectPoints(infile)
        case "e":
            print("Estimating")
            esitmate(Materials.MILD_STEEL, .5, 4, 4)
main()