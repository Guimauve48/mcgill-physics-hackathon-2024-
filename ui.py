import pygame 
import math
  
pygame.init() 

windowWidth = 1500
windowHeight = 800

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("McGill Physics Hackathon 2024") 

colors = {"black":(0,0,0), "white":(255,255,255), "lgray": (211,211,211), "gray": (175,175,175), 
          "lblue":(173,216,230), "hblue":(120,195,215), "red":(220,20,60), "blue":(0,0,205), "green":(50,205,50)}
centerPos = ((windowWidth*5/6)/2 + windowWidth/6, windowHeight/2)
theta = math.atan(math.cos(math.pi/4))
beta = math.atan(2/3)
alpha = theta - beta
gamma = math.pi/2 -theta - beta
phi = math.atan(1/2)
epsilon = theta - phi
tau = math.pi/2 -theta - phi

def to2d(x,y,z, main):
    center = centerPos if not main else (0,0)
    return (center[0]+y-x*math.cos(theta), center[1]+z+x*math.sin(theta))

def moveX(pos, x):
    return (pos[0]+x/2*math.cos(theta), pos[1]-x/2*math.sin(theta))

def ellipse(rY, rZ, c, x):
    delta = ((1-((x-c[0])**2)/rY) * rZ)**0.5
    return (c[1] - delta, c[1] + delta)

#? Prism class
class Prism:
    def __init__(self, position, size, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.sizeZ = size[2]
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]

        self.create()


    def create(self):
        p0 = to2d(self.x, self.y, self.z, self.main)
        p1 = (p0[0], p0[1]-self.sizeZ)
        p2 = (p1[0]+self.sizeY, p1[1])
        p3 = (p0[0]+self.sizeY, p0[1])
        p4 = moveX(p1,self.sizeX)
        p5 = moveX(p2,self.sizeX)
        p6 = moveX(p3,self.sizeX)
        self.points = [p0,p1,p2,p3,p4,p5,p6]
        self.corners = (p0,p5)
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face1 = (*p1, self.sizeY, self.sizeZ)
        self.face2 = (p1, p4, p5, p2)
        self.face3 = (p2, p5, p6, p3)

    def draw(self):
        self.create()
        pygame.draw.rect(window, self.color, self.face1)
        pygame.draw.polygon(window, self.color, self.face2)
        pygame.draw.polygon(window, self.color, self.face3)
        pygame.draw.lines(window, colors["black"], False, [self.points[3],self.points[0],self.points[1],self.points[2],self.points[3],self.points[6],self.points[5],self.points[4],self.points[1]])
        pygame.draw.line(window, colors["black"],self.points[2],self.points[5])


#? Cylinder class
class Cylinder:
    def __init__(self, position, r1, r2, height, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.r1 = r1
        self.r2 = r2
        self.height = height
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]
        
        self.create()


    def create(self):
        self.center = to2d(self.x, self.y, self.z, self.main)
        self.corners = ((self.center[0]-self.r1, self.center[1]+self.r1/2),(self.center[0]+self.r1, self.center[1]-self.height-self.r1/2))
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face1 = ((self.center[0]-self.r1,self.center[1]),
                      (self.center[0]-self.r2,self.center[1]-self.height),
                      (self.center[0]+self.r2,self.center[1]-self.height),
                      (self.center[0]+self.r1,self.center[1]))
        self.bottom = (self.center[0]-self.r1, self.center[1]-self.r1/2, self.r1*2, self.r1)
        self.top = (self.center[0]-self.r2, 
                    self.center[1]-self.height-self.r2/2, 
                    self.r2*2, 
                    self.r2)

    def draw(self):
        self.create()

        pygame.draw.ellipse(window, self.color, self.bottom)
        pygame.draw.ellipse(window, colors["black"], self.bottom,1)

        pygame.draw.polygon(window, self.color, self.face1)

        pygame.draw.ellipse(window, self.color, self.top)
        pygame.draw.ellipse(window, colors["black"], self.top,1)

        pygame.draw.line(window, colors["black"],(self.center[0]-self.r1,self.center[1]),(self.center[0]-self.r2,self.center[1]-self.height))
        pygame.draw.line(window, colors["black"],(self.center[0]+self.r1,self.center[1]),(self.center[0]+self.r2,self.center[1]-self.height))


#? Ellipsoid class
class Ellipsoid:
    def __init__(self, position, rX, rY, rZ, main, masse):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.rX = rX
        self.rY = rY
        self.rZ = rZ
        self.main = main
        self.masse = masse
        self.color = colors["lblue"]

        self.create()


    def create(self):
        self.center = to2d(self.x, self.y, self.z, self.main)
        self.corners = ((self.center[0]-self.rY, self.center[1]+self.rZ),(self.center[0]+self.rY, self.center[1]-self.rZ))
        self.arrowC = (self.corners[1][0]/2+self.corners[0][0]/2,self.corners[0][1]/2+self.corners[1][1]/2)

        self.face = (self.center[0]-self.rY, self.center[1]-self.rZ, self.rY*2, self.rZ*2)

        #self.arcs = []
        #arcNb = self.rY // 10 - 1
        #for i in range(arcNb):
        #    radius = 2*self.rX*math.sin(i/(arcNb/3) + 0.5) + 50
        #    print(radius)
        #    arc = (self.center[0]+22*i-self.rY+5, self.center[1]-radius/2, radius, radius)
        #
        #    self.arcs.append(arc)


    def draw(self):
        self.create()

        pygame.draw.ellipse(window, self.color, self.face)
        pygame.draw.ellipse(window, colors["black"], self.face,1)

        #for (i,arc) in enumerate(self.arcs):
        #    print(i,arc)
        #    pygame.draw.arc(window, colors["black"], arc, math.pi*2/3, math.pi*4/3)

#! Object selection section
section_bg = pygame.rect.Rect(0,0, windowWidth/6, windowHeight)

mainPrism = Prism((0,windowWidth/12-55,windowHeight*1/6+80), (80,80,80), True, 100)
mainCylinder = Cylinder((0,windowWidth/12,windowHeight/2+40), 50,50,80, True, 100)
mainEllipsoid = Ellipsoid((0,windowWidth/12,windowHeight*5/6-20), 40,80,50, True, 100)

xGrab, yGrab, zGrab = False, False, False

shapeList = []
selectedShape = None

running = True  
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            xGrab, yGrab, zGrab = False, False, False

        if selectedShape != None:
            c = selectedShape.arrowC
            cX = moveX(c, -180)
            cY = (c[0]+100, c[1])
            cZ = (c[0], c[1]-100)
            
            if (pygame.mouse.get_pos()[0] >= c[0] and pygame.mouse.get_pos()[0] <= cY[0] and
                pygame.mouse.get_pos()[1] >= c[1] - 10 and pygame.mouse.get_pos()[1] <= c[1] + 10):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    diff = pygame.mouse.get_pos()[0] - selectedShape.y
                    yGrab = True
            
            elif (pygame.mouse.get_pos()[0] >= c[0] - 10 and pygame.mouse.get_pos()[0] <= c[0] + 10 and
                pygame.mouse.get_pos()[1] >= cZ[1] and pygame.mouse.get_pos()[1] <= c[1]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    diff = pygame.mouse.get_pos()[1] - selectedShape.z
                    zGrab = True
            
            elif (pygame.mouse.get_pos()[0] >= cX[0] and pygame.mouse.get_pos()[0] <= c[0] and
                  pygame.mouse.get_pos()[1] <= cX[1] and pygame.mouse.get_pos()[1] >= c[1]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    lastVal = pygame.mouse.get_pos()
                    xGrab = True
                
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    found = False
                    for shape in shapeList[::-1]:
                        if not found:
                            if (pygame.mouse.get_pos()[0] >= shape.corners[0][0] and pygame.mouse.get_pos()[0] <= shape.corners[1][0] and
                                pygame.mouse.get_pos()[1] >= shape.corners[1][1] and pygame.mouse.get_pos()[1] <= shape.corners[0][1]):
                                
                                if selectedShape != None:
                                        selectedShape.color = colors["lblue"]

                                if shape == selectedShape:
                                    selectedShape = None
                                else:
                                    selectedShape = shape
                                    selectedShape.color = colors["hblue"]

                                found = True
                            else:
                                selectedShape = None

        elif (pygame.mouse.get_pos()[0] >= mainPrism.corners[0][0] and pygame.mouse.get_pos()[0] <= mainPrism.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainPrism.corners[1][1] and pygame.mouse.get_pos()[1] <= mainPrism.corners[0][1]):
            mainPrism.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Prism((0,0,0), (100,100,100), False, 100))

        elif (pygame.mouse.get_pos()[0] >= mainCylinder.corners[0][0] and pygame.mouse.get_pos()[0] <= mainCylinder.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainCylinder.corners[1][1] and pygame.mouse.get_pos()[1] <= mainCylinder.corners[0][1]):
            mainCylinder.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Cylinder((0,0,0), 40, 40, 80, False, 100))

        elif (pygame.mouse.get_pos()[0] >= mainEllipsoid.corners[0][0] and pygame.mouse.get_pos()[0] <= mainEllipsoid.corners[1][0] and
            pygame.mouse.get_pos()[1] >= mainEllipsoid.corners[1][1] and pygame.mouse.get_pos()[1] <= mainEllipsoid.corners[0][1]):
            mainEllipsoid.color = colors["hblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN:
                shapeList.append(Ellipsoid((0,0,0), 40, 80, 50, False, 100))
        
        else:
            mainPrism.color = colors["lblue"]
            mainEllipsoid.color = colors["lblue"]
            mainCylinder.color = colors["lblue"]
            mainEllipsoid.color = colors["lblue"]
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.MOUSEBUTTONDOWN:
                found = False
                for shape in shapeList[::-1]:
                    if not found:
                        if (pygame.mouse.get_pos()[0] >= shape.corners[0][0] and pygame.mouse.get_pos()[0] <= shape.corners[1][0] and
                            pygame.mouse.get_pos()[1] >= shape.corners[1][1] and pygame.mouse.get_pos()[1] <= shape.corners[0][1]):
                            if selectedShape != None:
                                    selectedShape.color = colors["lblue"]

                            if shape == selectedShape:
                                selectedShape = None
                            else:
                                selectedShape = shape
                                selectedShape.color = colors["hblue"]

                            found = True    

        


    window.fill(colors["white"])

    #! Movement
    if selectedShape != None:
        if xGrab:
            mouseNow = pygame.mouse.get_pos()
            yChange = mouseNow[0] - lastVal[0]
            zChange = mouseNow[1] - lastVal[1]

            sign = -1 if yChange > 0 and zChange < 0 else 1
            changeX = (yChange**2 + zChange**2)**0.5 * sign

            selectedShape.x += changeX
            lastVal = pygame.mouse.get_pos()
        if yGrab:
            selectedShape.y = pygame.mouse.get_pos()[0] - diff
        if zGrab:
            selectedShape.z = pygame.mouse.get_pos()[1] - diff


    #! Axis
    pygame.draw.line(window, colors["gray"], (centerPos[0]-windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3, centerPos[1]))
    pygame.draw.aaline(window, colors["gray"], (centerPos[0]+windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3-15, centerPos[1]+10),2)
    pygame.draw.aaline(window, colors["gray"], (centerPos[0]+windowWidth/3, centerPos[1]),(centerPos[0]+windowWidth/3-15, centerPos[1]-10),2)

    pygame.draw.line(window, colors["gray"], (centerPos[0], centerPos[1]+windowHeight*3/7),(centerPos[0], centerPos[1]-windowHeight*3/7))
    pygame.draw.aaline(window, colors["gray"], (centerPos[0], centerPos[1]-windowHeight*3/7),(centerPos[0]-10, centerPos[1]-windowHeight*3/7+15),2)
    pygame.draw.aaline(window, colors["gray"], (centerPos[0], centerPos[1]-windowHeight*3/7),(centerPos[0]+10, centerPos[1]-windowHeight*3/7+15),2)
    
    pygame.draw.line(window, colors["gray"], moveX(centerPos,windowWidth*4/7),moveX(centerPos,-windowWidth*4/7))
    pt = moveX(centerPos,-windowWidth*4/7)
    pygame.draw.line(window, colors["gray"], pt, (pt[0]+(325**0.5)*math.cos(alpha), pt[1]+(325**0.5)*math.sin(alpha)))
    pygame.draw.line(window, colors["gray"], pt, (pt[0]+(325**0.5)*math.sin(gamma), pt[1]-(325**0.5)*math.cos(gamma)))

    
    #! Main shapes
    pygame.draw.rect(window, colors["lgray"], section_bg)
    mainPrism.draw()
    mainCylinder.draw()
    mainEllipsoid.draw()

    #! Added shapes
    for shape in shapeList:
        shape.draw()

    #! Selected shape arrows
    if selectedShape != None:
        c = selectedShape.arrowC
        cX = moveX(c, -180)
        cY = (c[0]+100, c[1])
        cZ = (c[0], c[1]-100)

        pygame.draw.line(window, colors["blue"], moveX(c, -8), cX, 4)
        pygame.draw.circle(window, colors["blue"], moveX(moveX(c, -8)[::-1],2)[::-1], 2)
        pygame.draw.polygon(window, colors["blue"], (moveX(cX,-24), moveX((cX[0]+(180**0.5)*math.cos(epsilon), cX[1]+(180**0.5)*math.sin(epsilon-0.1)),-24),moveX((cX[0]+(180**0.5)*math.sin(tau), cX[1]-(180**0.5)*math.cos(tau)),-24)))

        pygame.draw.line(window, colors["red"], (c[0], c[1]-8), cZ, 4)
        pygame.draw.circle(window, colors["red"], (c[0]+1, c[1]-8), 2)
        pygame.draw.polygon(window, colors["red"], ((cZ[0], cZ[1]-12), (cZ[0]-6, cZ[1]), (cZ[0]+6, cZ[1])))

        pygame.draw.line(window, colors["green"], (c[0]+8, c[1]), cY, 4)
        pygame.draw.circle(window, colors["green"], (c[0]+8, c[1]+1), 2)
        pygame.draw.polygon(window, colors["green"], ((cY[0]+12, cY[1]), (cY[0], cY[1]-6), (cY[0], cY[1]+6)))


    pygame.display.update() 

pygame.quit()