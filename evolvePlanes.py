import rhinoscriptsyntax as rs
import math
import random
import pickle

#GLOBAL VARIABLES
maxPointOffset = 0.1
maxPoints = 10
numCols = 10
numPlanesSelected = 10


#HELPER FUNCTIONS
def createPointOffset(numPoints):
    pointList =[]
    for i in range(0,numPoints-1):
        pOffsetX = random.uniform(-maxPointOffset,maxPointOffset)
        pOffsetY = random.uniform(-maxPointOffset,maxPointOffset)
        offset = rs.VectorCreate((0,0,0),(pOffsetX,pOffsetY,0))
        pointList.append(offset)
    return pointList      

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

def maprange( a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

#CLASSES

class Population:
    
    def __init__(self,tPop,gen):
        self.totalPopulation = tPop
        self.generation = gen
        self.population = []
        self.selectedPlanes = {}
        newLayer = rs.AddLayer("generation: " + str(generation))
        rs.CurrentLayer(newLayer)
    
    def createNewPopulation(self):
        x =0
        y =0
        for p in range (0,self.totalPopulation):
            if(x>numCols-1):
                x = 0
                y += 1
            newLoc = rs.MovePlane(rs.WorldXYPlane(),(x*20,y*-10,0))
            d = DNA()
            pl = Plane(newLoc, d,p)
            self.population.append(pl)
            x += 1
    
    def dnaToFile(self):
        filename = "generation" + str(self.generation) + ".p"
        identity = {}
        for p in self.population:
            identity[self.population.index(p)] = p.genes.values
        
        with open(filename,"wb") as f:
            pickle.dump(identity,f)
        
    
    def dnaFromFile(self):
        file = "generation" +str(self.generation -1) +".p"
        #allGenes = pickle.load(open(file,"rb"))        
        with open(file,"rb") as f:
            allGenes = pickle.load(f)
        for i in range (0, numPlanesSelected):
            planeNum = rs.GetInteger("Select Plane to evolve", None,0,99)
            planeFitness = rs.GetInteger("Plane Fitness",None,1,1000)
            for i  in range (0,planeFitness):
                self.selectedPlanes[i*self.totalPopulation + planeNum] = allGenes.get(planeNum)
            #self.selectedPlanes[planeNum] = allGenes.get(planeNum)
        
    
    def evolvePlanes(self):
        x =0
        y =0
        for i in range (0,self.totalPopulation):
            if(x>numCols-1):
                x = 0
                y += 1
            newLoc = rs.MovePlane(rs.WorldXYPlane(),(x*20,y*-10,0))
            a = random.choice(self.selectedPlanes.values())
            b = random.choice(self.selectedPlanes.values())
            d = self.crossover(a,b)
            d.mutate()
            pl = Plane(newLoc,d,i)
            
            self.population.append(pl)
            x += 1
    
    def crossover(self, parentA, parentB):
        child = DNA()
        midpoint = 0.5        
        for key, value in child.values.items():
            chance = random.random()
            if(chance<midpoint):
                child.values[key] = parentA.get(key)
            else: 
                child.values[key] = parentB.get(key)
        
        return child

class DNA:
    
    def __init__(self):        
        self.mutationRate = 0.05
        self.Fw = random.uniform(1,5)
        self.Fh = random.uniform(1,2)
        self.Fwx = random.uniform(0.5,self.Fw-0.5)
        self.Fwy = random.uniform(0.5,self.Fh-0.5)    
        self.Fpt = createPointOffset(random.randint(2,maxPoints))
        self.Fpb = createPointOffset(random.randint(2,maxPoints))
        self.Fpl = createPointOffset(random.randint(2,maxPoints))
        self.Fpr = createPointOffset(random.randint(2,maxPoints))
        
        self.Ww = random.uniform(1,5)
        self.Wh = random.uniform(1,2)
        self.Wsd = random.uniform(0.2,0.8)
        self.Wpt = createPointOffset(random.randint(2,maxPoints))
        self.Wpb = createPointOffset(random.randint(2,maxPoints))
        self.Wps = createPointOffset(random.randint(2,maxPoints))
        
        self.values = {'Fw':self.Fw,'Fh':self.Fh,'Fwx':self.Fwx,'Fwy':self.Fwy,'Fpt':self.Fpt,'Fpb':self.Fpb,'Fpl':self.Fpl,'Fpr':self.Fpr,'Ww':self.Ww,'Wh':self.Wh,'Wsd':self.Wsd,'Wpt':self.Wpt,'Wpb':self.Wpb,'Wps':self.Wps}
    
    def mutate(self):
        mutateChance = random.random()
        if (mutateChance < self.mutationRate):
            dnaMutate = random.choice(list(self.values.keys()))
            print(dnaMutate)
            mutatedDNA = None
            if (dnaMutate == 'Fw' or dnaMutate == 'Ww'):
                mutatedDNA = random.uniform(1,10)
            elif (dnaMutate == 'Fh' or dnaMutate == 'Wh'):
                mutatedDNA = random.uniform(1,3)
            elif (dnaMutate == 'Fwx'):
                mutatedDNA = random.uniform(0.5,self.Fw-0.5)
            elif (dnaMutate == 'Fwy'):
                mutatedDNA = random.uniform(0.5,self.Fh-0.5) 
            elif (dnaMutate == 'Wsd'):
                mutatedDNA = random.uniform(0.2,0.8)                
            elif (dnaMutate == 'Fpt' or dnaMutate == 'Fpb' or dnaMutate == 'Fpl' or dnaMutate == 'Fpr' or dnaMutate == 'Wpt' or dnaMutate == 'Wpb' or dnaMutate == 'Wps'):
                mutatedDNA = createPointOffset(random.randint(2,maxPoints))
            
            self.values[dnaMutate] = mutatedDNA
        #self.values = {'Fw':self.Fw,'Fh':self.Fh,'Fwx':self.Fwx,'Fwy':self.Fwy,'Fpt':self.Fpt,'Fpb':self.Fpb,'Fpl':self.Fpl,'Fpr':self.Fpr,'Ww':self.Ww,'Wh':self.Wh,'Wsd':self.Wsd,'Wpt':self.Wpt,'Wpb':self.Wpb,'Wps':self.Wps}


class Plane:
    
    def __init__(self,loc,_dna,num):
        self.genes = _dna
        self.location = loc
        self.number = str(num)
        self.createAirplane()        
        
    
    def createAirplane(self):
        #CREATE FUSELAGE
        
        rectangleFuselage = rs.AddRectangle(self.location,self.genes.values['Fw'],self.genes.values['Fh'])
        endPointsF = rs.PolylineVertices(rectangleFuselage)
        fPtsB = offsetPoints(self.genes.values['Fpb'],endPointsF[0],endPointsF[1])
        fPtsR = offsetPoints(self.genes.values['Fpr'],endPointsF[1],endPointsF[2])
        fPtsT = offsetPoints(self.genes.values['Fpt'],endPointsF[2],endPointsF[3])
        fPtsL = offsetPoints(self.genes.values['Fpl'],endPointsF[3],endPointsF[0])
        fPtsL.append(fPtsB[0])
        fCurveOpen = rs.AddCurve(fPtsB+fPtsR+fPtsT+fPtsL,2)
        
        #CREATE WING SLOT
        wingSlotStart = rs.VectorAdd(endPointsF[0],(self.genes.values['Fwx'],self.genes.values['Fwy'],0))
        wingSlotEnd = rs.VectorAdd(wingSlotStart,(self.genes.values['Fw']-self.genes.values['Fwx']+maxPointOffset*2,0,0))
        wingSlot = rs.AddLine(wingSlotStart,wingSlotEnd)
        #guideLine = rs.AddLine(wingSlotStart,rs.VectorAdd(wingSlotStart,(0,0.2,0)))
        #rs.ObjectColor(guideLine,(0,0,200))
        #wingSlotOffset = rs.OffsetCurve(wingSlot,(0,1,0),1/32)
        #rs.AddLine(rs.CurveStartPoint(wingSlot),rs.CurveStartPoint(wingSlotOffset))
        
        #CREATE WING
        wPlaneOffY = self.genes.values['Wh']+1
        wPlaneOffX = self.genes.values['Fw']/2
        wingPlane = rs.MovePlane(self.location,(wPlaneOffX+self.location[0].X,-wPlaneOffY+self.location[0].Y,0))
        rectangleWing = rs.AddRectangle(wingPlane,self.genes.values['Ww'],self.genes.values['Wh'])
        endPointsW= rs.PolylineVertices(rectangleWing)
        wPtsB = offsetPoints(self.genes.values['Wpb'],endPointsW[0],endPointsW[1])
        wPtsR = offsetPoints(self.genes.values['Wps'],endPointsW[1],endPointsW[2])
        wPtsT = offsetPoints(self.genes.values['Wpt'],endPointsW[2],endPointsW[3])
        wPtsT.append(endPointsW[3])
        wPtsB.insert(0,endPointsW[0])
        wingCurve = rs.AddCurve(wPtsB+wPtsR+wPtsT)
        #wingLine = rs.AddLine(endPointsW[3],endPointsW[0])
        wingCurveM = rs.MirrorObject(wingCurve,endPointsW[3],endPointsW[0],True)
        
        #CREATE WING GROOVE
        wingGrooveStart = rs.VectorAdd(endPointsW[3],(0,maxPointOffset,0))
        wingGrooveEnd = rs.VectorAdd(wingGrooveStart,(0,-(maxPointOffset+self.genes.values['Wh']*self.genes.values['Wsd']),0))
        wingGroove = rs.AddLine(wingGrooveStart,wingGrooveEnd)
        #wingGrooveOffset = rs.OffsetCurve(wingGroove,(1,0,0),-1/32)
        #rs.AddLine(rs.CurveEndPoint(wingGroove),rs.CurveEndPoint(wingGrooveOffset))
            
        #DELETE RECTANGLES
        rs.DeleteObject(rectangleFuselage)
        rs.DeleteObject(rectangleWing)
        
        textPlane = rs.MovePlane(self.location,(self.location[0].X+.25,self.location[0].Y+.25,0))
        text = rs.AddText(self.number, textPlane,0.25)
        textCurves = rs.ExplodeText(text,True)
        rs.ObjectColor(textCurves,(0,0,200))
        planeGroup = rs.AddGroup()
        rs.AddObjectsToGroup([fCurveOpen,wingCurveM,wingSlot,wingCurve,wingGroove,text],planeGroup)
        
if __name__ == "__main__":
    generation = rs.GetInteger("Generation")
    pop = Population(100,generation)
    if(generation == 0):
        pop.createNewPopulation()
    else:
        pop.dnaFromFile()
        pop.evolvePlanes()
    pop.dnaToFile()
