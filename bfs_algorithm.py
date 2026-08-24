import pygame
from collections import deque

PURPLE=(119, 107, 219)
ORANGE=(255,152,0)

def getNeighbors(grid,node,rows,cols):

    neighbors=[]
    row,col=node.row,node.col

    if row >0 and not grid[row-1][col].is_wall:
        neighbors.append(grid[row-1][col])

    if row <rows-1 and not grid[row+1][col].is_wall:
        neighbors.append(grid[row+1][col])

    if col >0 and not grid[row][col-1].is_wall:
        neighbors.append(grid[row][col-1])

    if col <cols-1 and not grid[row][col+1].is_wall:
        neighbors.append(grid[row][col+1])            

    return neighbors    

def reconstructPath(cameFrom,current,drawFunc):
    while current in cameFrom:
        current=cameFrom[current]
        if not current.is_start:
            current.color=ORANGE
        drawFunc()    
        pygame.time.delay(60)

def  bfs(drawFunc, grid,start,goal,rows,cols):

    queue=deque()
    queue.append(start)

    cameFrom ={}
    visited={start}

    while queue:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                return False

        current=queue.popleft()        

        if current ==goal:
            reconstructPath(cameFrom,current,drawFunc)
            return True

        for neighbor in getNeighbors(grid,current,rows,cols):
            if neighbor not in visited:
                visited.add(neighbor)   
                cameFrom[neighbor]=current 
                queue.append(neighbor)

                if not neighbor.is_goal:
                    neighbor.color=PURPLE
                drawFunc()            
                pygame.time.delay(20)    

        

    return False
