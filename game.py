import pygame,os,sys,random,math,time
from pygame.locals import *
from pygame.version import PygameVersion
pygame.init()
print(PygameVersion)

#some rgb colors
background = pygame.Color(85,50,253)
fontColor = pygame.Color(0,162,232)
green =  pygame.Color(0,90,50)
buttonColor=pygame.Color(36,38,123)
white = pygame.Color(255,255,255)

#global variables
count=0
score=0
run=False
angle =160

display = pygame.display.set_mode((1920,1080))   #display size
pygame.display.set_caption("Mardi Gras On Mars")        #This simply writes the name of the game on the window's page
fps = pygame.time.Clock()                     #this is for frame per second


# Type the Jewelry toss code below here. This class initiates the position of the jewellery thrown in relation to the float and the crowd 
class Float:
    def __init__(self, pos, vel,image,angle):
        self.position = [pos[0]-45,pos[1]-45]
        self.velocity = [vel[0],vel[1]]
        self.angle = angle
        self.image = image
        self.forward = [0,0]
    def ThrowJewellery(self):  #throw a jewellery
        global jewellery
        throw.play()
        JewelleryPos = [self.position[0]+50 * self.forward[0], self.position[1]+30* self.forward[1]] #LUC 
        JewelleryVel = [self.velocity[0] + 6 * self.forward[0], self.velocity[1] + 6 * self.forward[1]]
        newJewelry = JewelleryImg[random.randrange(0,5)]
        jewellery.add(RoadElements(JewelleryPos, JewelleryVel, newJewelry,self.angle, throw))
    def Draw(self,canvas):    #add float to the display
        canvas.blit(self.image, self.position)
    def Update(self,angle):   #update jewellery angel
        self.angle = angle
        self.forward = AngleCalculate(math.radians(self.angle))


class RoadElements:
    def __init__(self, pos, vel, image,angle=None,sound = None,): #This function integrates the speed of the jewelry and the sound played when thrown
        if sound:
            sound.play()
        self.velocity = [vel[0],vel[1]]
        self.image = image
        self.up = False
        self.down=False
        self.position = pos
        self.angle=angle
        self.sound = sound


    def CrowdAndJewellery(self,jewel):    #this function will decide if the crowd can can catch any jewellery or not
        crowdPos=self.getPosition()
        crowdPos[0] += 80
        crowdPos[1] += 80
        jewelPos = jewel.getPosition()
        jewelPos[0] += 40
        jewelPos[1] += 40
        if DistanceCalculate(jewelPos, crowdPos) <= 80:
            return True
        else:
            return False
    def getPosition(self):   #return current position of crowd and jewellery
        return [int(self.position[0]), int(self.position[1])]
    def Celebrate(self):     #set the crowd to jump
        self.up = True
    def Draw(self, canvas):
        if self.angle != None:
            canvas.blit(RotateImage(self.image, self.angle), (int(self.position[0] - 40), int(self.position[1] - 40)))
        elif self.up:      #move up a crowed if it caught any jewellery
            canvas.blit(self.image,(self.position[0],self.position[1]-10))
            self.up=False
            self.down=True
        elif self.down:     #again move down to make a jump
            canvas.blit(self.image,(self.position[0],self.position[1]+10))
            self.down=False
        else:
            canvas.blit(self.image,self.position)

    def Update(self):      #update jewellery position and rotation
        if self.angle != None:
            self.angle += 10
        if self.sound != None:
            self.position[0] = (self.position[0] + self.velocity[0])
            self.position[1] = (self.position[1] + self.velocity[1])
        else:
            self.position[0] = (self.position[0] + self.velocity[0])
        if 0 > self.position[1] > 720 or self.position[0]>1280:
            return True
        return False


def RotateImage(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle) #This function rotates jewellery
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#Rotating Angle calculation
def AngleCalculate(ang):
    return [math.cos(ang), -math.sin(ang)]

#Distance calculation between jewellery and crowd
def DistanceCalculate(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

#This function choose a cartoon randomly and add it to the road
def Crowd():
    global jewellery,run,CrowdImg
    if len(crowds) < 10:
        while 1:
            random_pos1 = [-200,0]     #to generate crowd in top of the screen
            random_pos2 = [-200,450]    #to generate crowd in bottom of the screen
            r=random.randrange(1,100)
            if r<50:
                crowd_pos=random_pos1
                rand = random.randrange(0,6)  #randomly choose any crowd image for top
            else:
                crowd_pos=random_pos2
                rand = random.randrange(5,9)   #randomly choose any crowd image for bottom
            break
        selectCrowd = CrowdImg[rand]
        cr_vel = [4,4]
        crowds.add(RoadElements(crowd_pos, cr_vel, selectCrowd))








#Type the Integrate crowd and crowd movement code lines here. This function draws all the crowd and jewellery in the display
        
def Draw_Components(canvas):
    for cr in list(crowds):
        cr.Draw(canvas)         #add all the crowds
        if cr.Update():
            crowds.remove(cr)  
    for jl in list(jewellery):   #add all the jewellery
        jl.Draw(canvas)
        if jl.Update():
            jewellery.remove(jl)
#It checks whether a crowed catch any jewellery or not
def Check_Caught(crowds,object):
    for cr in list(crowds):
        if cr.CrowdAndJewellery(object):
            cr.Celebrate()
            cr.Update()
            celebrate.play()
            return True      
    return False
#It takes jewellery groups and croweds group for checking
def Check_Jewellery(jewellry_group, crowd_group):
    for element in list(jewellry_group):
        if Check_Caught(crowd_group,element):
            jewellry_group.remove(element)
            return True
    return False






#Type in the Moving the float code here. It the movement variable is integrated into the diaplay window//All the components added to the display and calculates scores
def DrawBoard(canvas):
    global score,run,count,angle
    canvas.blit(RoadImg,(0,0))
    canvas.blit(RoadImg,(count*4,0))
    canvas.blit(RoadImg,(count*4-1280,0))
    GameObject.Draw(canvas)
    if run:
        Draw_Components(canvas)     #add crowds and jewellery to the screen
        GameObject.Update(angle)     #update angle of the jewellery
        if Check_Jewellery(jewellery,crowds):
            score += 10                #every successfull caught increses score by 10
    if score >= 420:          #game will over if you score 420
        run = False
        GameOver()
    myfont2 = pygame.font.SysFont("comicsansms", 20)
    label2 = myfont2.render("Score : "+str(score), 1, (255,255,0))
    canvas.blit(label2, (1150, 20))
def Counter():    #this function will add a crowd to the screen gradually after a certain period
    global count 
    if count <= 320:
        count += 1
        if count % 80 == 0:
            Crowd()
    else:
        count = 0






#Load Image Section

#Background/road/float Images are loaded here
IntroImg = pygame.image.load(os.path.join('images','background.png')) ###Function for loading the background
RoadImg = pygame.image.load(os.path.join('images','road.jpg'))
floatImg = pygame.image.load(os.path.join('images','float.png'))


#Jewelry Section, type in code for  loading the jewellery images here
JewelleryImg = []
JewelleryImg.append(pygame.image.load(os.path.join('images','jewel1.png')))
JewelleryImg.append(pygame.image.load(os.path.join('images','jewel2.png')))
JewelleryImg.append(pygame.image.load(os.path.join('images','jewel3.png')))
JewelleryImg.append(pygame.image.load(os.path.join('images','jewel4.png')))
JewelleryImg.append(pygame.image.load(os.path.join('images','jewel5.png')))


#Crowd Section, crowds images are loaded here
CrowdImg = []
CrowdImg.append(pygame.image.load(os.path.join('images','crowd1.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd2.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd3.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd4.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd5.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd6.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd7.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd8.png')))
CrowdImg.append(pygame.image.load(os.path.join('images','crowd9.png')))








# Type Audio Integration Block. Sound section, load Sounds and set their volume

pygame.mixer.music.load(os.path.join('sounds','LifeOnMars(2021 remaster).mp3'))   #background music
throw = pygame.mixer.Sound(os.path.join('sounds','throw.wav'))  #it works while a jewellery is thrown
throw.set_volume(0.4)
celebrate = pygame.mixer.Sound(os.path.join('sounds','celebration.wav'))   #celebration sound
celebrate.set_volume(0.3)


GameObject = Float([1000,320], [0,0],floatImg,angle) #Ship object

crowds= set([])      #empty sets that will contain all the crowds and jewelleries
jewellery = set([])






#Start/exit section loaded here,Introduction Window with 'Play' and 'Exit' button
def Intro():
    display.fill(background)
    display.blit(IntroImg,(350,50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Button("Exit",450,550,100,60,QuiteGame)
        Button("Start Game",650,550,150,60,NewGame)
        pygame.display.update()
        fps.tick(15)








#Type Button code blocks here. The Cursuor section ensures Buttons/keyboard are loaded here, This function contains button's behaviors
def Button(name,x,y,h,w,action=None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() #clicking the mouse throws jewelry into the crowd

    if x<pos[0]<x+h and y<pos[1]<y+w:
        pygame.draw.rect(display,green,[x,y,h,w])
        if click[0]==1 and action!=None:
            action()
    else:
        pygame.draw.rect(display,buttonColor,[x,y,h,w])
    font = pygame.font.SysFont("comicsansms",20)
    text = font.render(name,True,white)
    display.blit(text,(x+15,y+15))








#Type Quit game code blocks here. function for Quit Game
def QuiteGame():
    pygame.quit()
    sys.exit()









#Type game start code blocks here. function for start game
def NewGame():
    global run,score, crowds, jewellery, GameObject,count,angle
    pygame.mixer.music.play(-1)
    run = True
    score,count = 0,0
    crowds = set([])
    jewellery = set([])
    while True:
        DrawBoard(display)
        Counter()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                if click[0]==1:    #if mouse is clicked then an angel will set for throwing jewellery
                    if pos[0]>600 and pos[1]<300:
                        GameObject.Update(130)
                    elif pos[0]<600 and pos[1]<300:
                        GameObject.Update(160)
                    elif pos[0]>600 and pos[1]>350:
                        GameObject.Update(-130)
                    elif pos[0]<600 and pos[1]>350:
                        GameObject.Update (-160)
                    GameObject.ThrowJewellery()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()   #update display
        fps.tick(60)       #60 frames arrive per second






#clicking the keyboard command "Esc" pausing the game until you press "Esc" again, which would continue the game









#this adds a stopwatch, which counts up when playing the game until it is paused, it continues. It captures the time once you have reached the limit of the amounts 
def time():
    global time
    font = pygame.font.SysFont("comicsansms",20)
    text = font.render("time",True,green)
    







#Type play again code block here. This is the function for Game Over/Play Again window
def GameOver():
    global score
    font = pygame.font.SysFont("comicsansms",80)
    text = font.render("Task Complete",True,green)
    scoreText = font.render("Your Score : "+str(score),True,green)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display.blit(text,(460,150))
        display.blit(scoreText,(400,300))
        Button("Quit",450,450,80,60,QuiteGame)
        Button("Play Again",650,450,150,60,NewGame)
        pygame.display.update()
        fps.tick(15)
Intro()
pygame.quit()
sys.exit()
