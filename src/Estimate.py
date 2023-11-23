class Material:
    #speedMulti is seconds per inch of cutting
    #CPI cost per inch
    #speedMulti default 1 inch per minute this multiplies that for accuracy
    def __init__(self, speedMulti, CPI, costMulti, cornerTimeMulti, cornerCostMulti):
        self.speedMulti = speedMulti
        self.CPI = CPI
        self.costMulti = costMulti
        self.cornerTimeMulti = self.speedMulti * cornerTimeMulti
        self.cornerCostMulti = cornerCostMulti
class Materials(enumerate):
    ALUMINUM =         Material(2.0, 1, 1, 1.4, 1.45)
    MILD_STEEL =       Material(1.5, 1, 1, 1.4, 1.45)
    STAINLESS_STEEL =  Material(1.1, 1, 1, 1.4, 1.45)
    TITANIUM =         Material(1.2, 1, 1, 1.4, 1.45)
#Pierce time in seconds for 1 inch thick
#Thickness and length in inches.
#Corners (count of corners) are anything over 60 deg for now (estimate)
#Garnet amount in LBS/MIN
#Pressure in PSI
#length is length of cut
#Per Hr to Second 21.63
#Garnet Price Per Pound = .31
GarnetPricePerSecond = .00516666
MachineCostPerSecond = .00600833

def esitmate(material, thickness, corners, length):
    cornerLength = corners / 2
    cutSpeed = material.speedMulti / thickness
    timeToCutCorners = cornerLength * material.cornerTimeMulti
    timeCuttingStraight = (length - cornerLength) / cutSpeed
    timeToCut = (timeToCutCorners + timeCuttingStraight) * 60


    fixedCost = timeToCut*GarnetPricePerSecond + timeToCut*MachineCostPerSecond
    cornerCutCost = cornerLength * material.cornerCostMulti
    straightCutCost = (length - cornerLength) * material.costMulti 

    costEstimate = cornerCutCost + straightCutCost + fixedCost
    print(f"Cut Time:{timeToCut}\n Cost Estimate: {costEstimate}")
    pass
