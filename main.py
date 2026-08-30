import pygame
import random

from bfs_algorithm import bfs
from dfs_algorithm import dfs
from a_star_algorithm import aStar
from greedy_algorithm import greedy

FONT =None

algorithm_name=""
explore_nodes=0

width,height=750,600
rows,cols=25,25
cell_size=height // rows

grid_width=cols* cell_size

white=(255,255,255)
black=(30,30,30)
green=(0,200,0)
red=(200,0,0)
grey=(200,200,200)
panel_bg=(235,235,235)

class Node:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.x=col * cell_size
        self.y=row * cell_size
        self.color=white

        self.is_wall=False
        self.is_start=False
        self.is_goal=False

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,cell_size,cell_size))    

    def reset(self):
        self.color=white
        self.is_wall=False
        self.is_start=False
        self.is_goal=False

    def reset_search(self):
        if not self.is_start and not self.is_goal and not self.is_wall:
            self.color=white

    def make_wall(self):
        self.color=black
        self.is_wall=True

    def make_start(self):
        self.color=green
        self.is_start=True

    def make_goal(self):
        self.color=red
        self.is_goal=True

def make_grid():
    grid=[]
    for r in range(rows):
        row=[]
        for c in range(cols):
            row.append(Node(r,c)) 
        grid.append(row)
    return grid

def reset_search(grid):
    for row in grid:
        for node in row:
            node.reset_search() 

def random_obstacles(grid,start,goal,density=0.25):
    for row in grid:
        for node in row:
            if node !=start and node !=goal:
                if random.random() <density:
                    node.make_wall()                              

def draw_grid_lines(win):
    for r in range(rows+1):
        pygame.draw.line(win,grey,(0,r*cell_size),(grid_width,r*cell_size))
    for c in range(cols+1):    
        pygame.draw.line(win,grey,(c*cell_size,0),(c*cell_size,height))

def draw_legend(win):

    panel_rect=pygame.Rect(grid_width,0,width - grid_width,height)
    pygame.draw.rect(win,panel_bg,panel_rect)
    
    instructions=[
        "Controls:",
        "Left Click - Start/Goal/Wall",
        "Right Click - Reset a cell",
        "",
        "Algorithms:",
        "b - Run BFS",
        "d -Run DFS",
        "a - Run A*",
        "g -  Greedy",
        "",
        "Grid Controls:",
        "c - Clear grid",
        "r - Random Obstacles",
        "s - Reset search",
        "",
        f"Algorithm: {algorithm_name}",
        f"Explore Nodes: {explore_nodes}"
       
    ]        

    x_offset=grid_width+10
    y_offset=30

    for line in instructions:
        text_surface=FONT.render(line,True,(0,0,0))
        win.blit(text_surface, (x_offset,y_offset))
        y_offset +=30


def draw(win,grid):
    win.fill(white)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win)     
    draw_legend(win)           
    pygame.display.update()

def get_clicked_pos(pos):
    x,y=pos
    row=y //cell_size
    col =x //cell_size

    return row,col


def main():
    global FONT,algorithm_name,explore_nodes

    pygame.init()
    pygame.font.init()
    FONT=pygame.font.SysFont("arial",14)
    win=pygame.display.set_mode((width,height))
    pygame.display.set_caption("AI Pathfinding visualizer")

    grid=make_grid()

    start=None
    goal=None
    running=True

    while running:
        draw(win,grid)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running =False

            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos)
                if row <rows and col <cols:
                    node =grid[row][col]

                    if not start and node !=goal:
                        start= node
                        start.make_start()
                    elif not goal and node !=start:
                        goal=node
                        goal.make_goal()    
                    elif node!=start and node !=goal:
                        node.make_wall()    

            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos)
                
                if row < rows and col <cols:
                    node =grid[row][col]
                    node.reset()

                    if node ==start:
                        start=None
                    if node ==goal:
                        goal=None

            if event.type ==pygame.KEYDOWN:
                if event.key ==pygame.K_c:
                    start=None
                    goal=None
                    grid=make_grid()

                    algorithm_name=""  
                    explore_nodes=0

                if event.key ==pygame.K_r:
                    random_obstacles(grid,start,goal) 

                if event.key ==pygame.K_s:
                    reset_search(grid)       

                if event.key==pygame.K_b and start and goal:
                    algorithm_name="BFS"
                    explore_nodes=0
                    success,explore_nodes=bfs(lambda:draw(win,grid),grid,start,goal,rows,cols)
                    draw(win,grid)

                if event.key==pygame.K_d and start and goal:
                     algorithm_name="DFS"
                     explore_nodes=0
                     success,explore_nodes=dfs(lambda:draw(win,grid,),grid,start,goal,rows,cols)                      
                     draw(win,grid)

                if event.key ==pygame.K_a and start and goal:
                     algorithm_name="A*"
                     explore_nodes=0
                     success,explore_nodes=aStar(lambda:draw(win,grid),grid,start,goal,rows,cols)
                     draw(win,grid)

                if event.key ==pygame.K_g and start and goal:
                     algorithm_name="Greedy"
                     explore_nodes=0
                     success,explore_nodes=greedy(lambda:draw(win,grid),grid,start,goal,rows,cols)    
                     draw(win,grid)
                    




    pygame.quit()

if __name__=="__main__":
    main()    