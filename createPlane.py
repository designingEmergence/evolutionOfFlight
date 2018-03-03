import rhinoscriptsyntax as rs
import math
import random

maxPointOffset = 0.1
maxPoints = 10

def createVariables():
    
    global Fw,Fh,Fwx,Fwy,Fpt,Fpb,Fpl,Fpr,Ww,Wh,Wsd,Wpt,Wpb,Wps
    Fw = random.uniform(1,10)
    Fh = random.uniform(1,3)
    Fwx = random.uniform(0.5,Fw-0.5)
    Fwy = random.uniform(0.5,Fh-0.5)    
    Fpt = createPointOffset(random.randint(2,maxPoints))
    Fpb = createPointOffset(random.randint(2,maxPoints))
    Fpl = createPointOffset(random.randint(2,maxPoints))
    Fpr = createPointOffset(random.randint(2,maxPoints))
    
    Ww = random.uniform(1,10)
    Wh = random.uniform(1,3)
    Wsd = random.uniform(0.2,0.8)
    Wpt = createPointOffset(random.randint(2,maxPoints))
    Wpb = createPointOffset(random.randint(2,maxPoints))
    Wps = createPointOffset(random.randint(2,maxPoints))

def createPointOffset(numPoints):
    pointList =[]
    for i in range(0,numPoints-1):
        pOffsetX = random.uniform(-maxPointOffset,maxPointOffset)
        pOffsetY = random.uniform(-maxPointOffset,maxPointOffset)
        offset = rs.VectorCreate((0,0,0),(pOffsetX,pOffsetY,0))
        pointList.append(offset)
    return pointList

def createAirplane():
    #CREATE FUSELAGE
    rectangleFuselage = rs.AddRectangle(rs.WorldXYPlane(),Fw,Fh)
    endPointsF = rs.PolylineVertices(rectangleFuselage)
    fPtsB = offsetPoints(Fpb,endPointsF[0],endPointsF[1])
    fPtsR = offsetPoints(Fpr,endPointsF[1],endPointsF[2])
    fPtsT = offsetPoints(Fpt,endPointsF[2],endPointsF[3])
    fPtsL = offsetPoints(Fpl,endPointsF[3],endPointsF[0])
    fPtsL.append(fPtsB[0])
    fCurveOpen = rs.AddCurve(fPtsB+fPtsR+fPtsT+fPtsL,2)
    
    #CREATE WING SLOT
    wingSlotStart = rs.VectorAdd(endPointsF[0],(Fwx,Fwy,0))
    wingSlotEnd = rs.VectorAdd(wingSlotStart,(Fw-Fwx+maxPointOffset*2,0,0))
    wingSlot = rs.AddLine(wingSlotStart,wingSlotEnd)
    wingSlotOffset = rs.OffsetCurve(wingSlot,(0,1,0),1/32)
    rs.AddLine(rs.CurveStartPoint(wingSlot),rs.CurveStartPoint(wingSlotOffset))
    
    #CREATE WING
    wPlaneOffY = Wh+1
    wPlaneOffX = Fw/2
    wingPlane = rs.MovePlane(rs.WorldXYPlane(),(wPlaneOffX,-wPlaneOffY,0))
    rectangleWing = rs.AddRectangle(wingPlane,Ww,Wh)
    endPointsW= rs.PolylineVertices(rectangleWing)
    wPtsB = offsetPoints(Wpb,endPointsW[0],endPointsW[1])
    wPtsR = offsetPoints(Wps,endPointsW[1],endPointsW[2])
    wPtsT = offsetPoints(Wpt,endPointsW[2],endPointsW[3])
    wPtsT.append(endPointsW[3])
    wPtsB.insert(0,endPointsW[0])
    wingCurve = rs.AddCurve(wPtsB+wPtsR+wPtsT)
    #wingLine = rs.AddLine(endPointsW[3],endPointsW[0])
    rs.MirrorObject(wingCurve,endPointsW[3],endPointsW[0],True)
    
    #CREATE WING GROOVE
    wingGrooveStart = rs.VectorAdd(endPointsW[3],(-1/64,maxPointOffset,0))
    wingGrooveEnd = rs.VectorAdd(wingGrooveStart,(0,-(maxPointOffset+Wh*Wsd),0))
    wingGroove = rs.AddLine(wingGrooveStart,wingGrooveEnd)
    wingGrooveOffset = rs.OffsetCurve(wingGroove,(1,0,0),-1/32)
    rs.AddLine(rs.CurveEndPoint(wingGroove),rs.CurveEndPoint(wingGrooveOffset))
        
    #DELETE RECTANGLES
    rs.DeleteObject(rectangleFuselage)
    rs.DeleteObject(rectangleWing)
    
def offsetPoints(pList,startPt,endPt):
    pointList = []
    sideVector = rs.VectorCreate(endPt,startPt)
    pointSpacing = (rs.VectorLength(sideVector)/len(pList))
    gapVector = rs.VectorUnitize(sideVector)
    gapVector = rs.VectorScale(gapVector,pointSpacing)
    for i in range(0,len(pList)):
        scaledVector = rs.VectorScale(gapVector,i)
        pointMove = rs.VectorAdd(startPt,scaledVector)
        offsetPoint = rs.VectorAdd(pointMove,pList[i]*rs.VectorLength(sideVector))
        point = (0,0,0)
        movedPoint = rs.PointAdd(point,offsetPoint)
        pointList.append(movedPoint)
    return pointList


if __name__ == "__main__":
    newLayer = rs.AddLayer()
    rs.CurrentLayer(newLayer)
    createVariables()
    createAirplane()

