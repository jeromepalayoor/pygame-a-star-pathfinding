import pygame
import random
import math

width,height = 1000,700
win = pygame.display.set_mode((width,height))
size = 20
pygame.display.set_caption("A Star Pathfinding Algorithym")

class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.start = False
        self.end = False
        self.opened = False
        self.closed = False
        self.blocked = False
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.route = False

    def draw(self):
        if self.start:
            pygame.draw.rect(win, (255, 0, 255), (self.x*size, self.y*size, size,size))
        elif self.end:
            pygame.draw.rect(win, (255, 0, 0), (self.x*size, self.y*size, size,size))
        elif self.route:
            pygame.draw.rect(win, (255, 200, 100), (self.x*size, self.y*size, size,size))
        elif self.closed:
            pygame.draw.rect(win, (0, 0, 255), (self.x*size, self.y*size, size,size))
        elif self.opened:
            pygame.draw.rect(win, (0, 255, 0), (self.x*size, self.y*size, size,size))
        elif self.blocked:
            pygame.draw.rect(win, (0, 0, 0), (self.x*size, self.y*size, size,size))

    def calculate(self):
        self.g = math.sqrt((self.x-startx)**2+(self.y-starty)**2)
        self.h = math.sqrt((self.x-endx)**2+(self.y-endy)**2)
        self.f = self.g + self.h

    def open(self, x, y):
        self.parent = [x,y]
        self.opened = True

    def closing(self):
        for i in range(-1,2):
            for j in range(-1,2):
                if not (i==0 and j==0) and not self.end and abs(i) != abs(j):
                    if self.x + i != -1 and self.y + j != -1 and self.x + i != width//size and self.y + j != height//size:
                        if not cells[self.x+i][self.y+j].start and not cells[self.x+i][self.y+j].opened and not cells[self.x+i][self.y+j].closed and not cells[self.x+i][self.y+j].blocked:
                            cells[self.x+i][self.y+j].open(self.x,self.y)

cells = []

for i in range(width//size):
    cells.append([])
    for j in range(height//size):
        cell = Cell(i,j)
        cells[i].append(cell)

startx = random.randint(0,width/size-1)
starty = random.randint(0,height//size-1)
endx = random.randint(0,width/size-1)
endy = random.randint(0,height//size-1)
cells[startx][starty].start = True
cells[endx][endy].end = True

for row in cells:
    for cell in row:
        cell.calculate()

finished = False
startalgo = False
run = True
while run:
    win.fill((255,255,255))

    for row in cells:
        for cell in row:
            cell.draw()
    
    for i in range(width//size-1):
        pygame.draw.line(win, (0,0,0), (i*size+size, 0),(i*size+size, height), 2)
    for i in range(height//size-1):
        pygame.draw.line(win, (0,0,0), (0, i*size+size),(width, i*size+size), 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not finished:
                startalgo = True
                cells[startx][starty].closed = True
                cells[startx][starty].closing()
            if event.key == pygame.K_c:
                cells = []

                for i in range(width//size):
                    cells.append([])
                    for j in range(height//size):
                        cell = Cell(i,j)
                        cells[i].append(cell)

                startx = random.randint(0,width/size-1)
                starty = random.randint(0,height//size-1)
                endx = random.randint(0,width/size-1)
                endy = random.randint(0,height//size-1)
                cells[startx][starty].start = True
                cells[endx][endy].end = True

                for row in cells:
                    for cell in row:
                        cell.calculate()

                startalgo = False
                finished = False
    
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        cell = cells[pos[0]//size][pos[1]//size]
        if not cell.start and not cell.end and not cell.opened and not cell.closed:
            cell.blocked = True

    if startalgo:
        try:
            smallest = 10000000000000000
            smallcell = []
            for row in cells:
                for cell in row:
                    if cell.opened and not cell.closed:
                        if cell.f < smallest:
                            smallest = cell.f
                            smallcell = [cell.x,cell.y]

            cells[smallcell[0]][smallcell[1]].closed = True
            cells[smallcell[0]][smallcell[1]].closing()
            
            if cells[smallcell[0]][smallcell[1]].end:
                startalgo = False
                finished = True
                parentcell = cells[smallcell[0]][smallcell[1]].parent
                while parentcell:
                    cells[parentcell[0]][parentcell[1]].route = True
                    parentcell = cells[parentcell[0]][parentcell[1]].parent
        except:
            pass
       
    pygame.display.update()

pygame.quit()
exit()
