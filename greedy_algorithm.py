import pygame
import heapq

PURPLE=(119,107,219)
ORANGE=(255,152,0)

def getNeighbors(grid,node,rows,cols):

    neighbors=[]

    row,col= node.row, node.col

    if row >0 and not grid[row-1][col].is_wall:
        neighbors.append(grid[row-1][col])

    if row <rows-1 and not grid[row+1][col].is_wall:
        neighbors.append(grid[row+1][col])  

    if col >0 and not grid[row][col-1].is_wall:
        neighbors.append(grid[row][col-1])      

    if col < cols-1 and not grid[row][col+1].is_wall:
        neighbors.append(grid[row][col+1])   

    return neighbors


def reconstructPath(cameFrom,current,drawFunc):
    while current in cameFrom:
        current=cameFrom[current]

        if not current.is_start:
            current.color=ORANGE
        drawFunc()
        pygame.time.delay(40)

def heuristic(nodeA,nodeB):
    x1,y1= nodeA.row, nodeA.col
    x2,y2= nodeB.row, nodeB.col

    return abs(x1-x2)+ abs(y1-y2)         

def greedy(drawFunc,grid,start,goal,rows,cols):


    count=0

    openSet=[] 
    heapq.heappush(openSet,(heuristic(start,goal),count,start))

    cameFrom={} 
    visited={start}          

    while openSet:

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                return False

        current =heapq.heappop(openSet)[2]    
      

        if current ==goal:
            reconstructPath(cameFrom,current,drawFunc)
            return True

        for neighbor in getNeighbors(grid,current,rows,cols):
           
                if neighbor not in visited:
                    visited.add(neighbor)
                    cameFrom[neighbor]=current
                    count+=1

                    heapq.heappush(openSet,(heuristic(neighbor,goal),count,neighbor))

                    if not neighbor.is_goal:
                        neighbor.color=PURPLE

                    drawFunc()
                    pygame.time.delay(40)

    return False                    