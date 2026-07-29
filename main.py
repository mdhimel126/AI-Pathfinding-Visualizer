import pygame

width,height=600,600
rows,cols=25,25
cell_size=width // cols

white=(255,255,255)
black=(30,30,30)
green=(0,200,0)
red=(200,0,0)
grey=(200,200,200)
blue=(0,120,255)
yellow=(255,215,0)

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

def draw_grid_lines(win):
    for r in range(rows+1):
        pygame.draw.line(win,grey,(0,r*cell_size),(width,r*cell_size))
    for c in range(cols+1):    
        pygame.draw.line(win,grey,(c*cell_size,0),(c*cell_size,height))


def draw(win,grid):
    win.fill(white)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win)                
    pygame.display.update()

def get_clicked_pos(pos):
    x,y=pos
    row=y //cell_size
    col =x //cell_size

    return row,col


def main():
    pygame.init()
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


    pygame.quit()

if __name__=="__main__":
    main()    