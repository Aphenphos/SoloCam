from enum import Enum

class Machines(Enum):
    AWJ_BURNY = 1
    AWJ_ATR = 2
    FLOW = 3
    PLASMA = 4

class GCODE(Enum):
    
    G0 = 0 #RAPID MOVE
    G1 = 1 #LINEAR FEED
    G2 = 2 #COUNTERCLOCKWISE ARC
    G3 = 3 #CLOCKWISE ARC
    G4 = 4 #EXACT STOP/DWELL
    G40 = 40 #KERF OFF
    G41 = 41 #KERF LEFT 
    G70 = 70 #SET INCHES
    G71 = 71 #SET MM (NEVER SEEN THIS USED)
    G90 = 90 #ABSOLUTE POSITIONING
    G92 = 92 #OFFSET

#(P) PLASMA (WJ) WATERJET EXLCUSIVES
class MCODE(Enum):
    
    M03 = 3 #OFF
    M04 = 4 #ON
    M30 = 30 #PROGRAM END
    M50 = 50 #ALL ON
    M51 = 51 #ALL OFF
    M67 = 67 #TOGGLE KERF
    M69 = 69 #(P) OFF
    M70 = 70 #SAVE STATE
    M73 = 73 #LOAD MODAL STATE
    M245 = 245 #(WJ)START ABRASIVE
    M246 = 246 #(WJ)STOP ABRASIVE
