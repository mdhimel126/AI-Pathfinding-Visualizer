import pygame
PURPLE=(119,107,219)
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

    if col < cols-1 and not grid[row][col+1].is_wall:
        neighbors.append(grid[row][col+1])

    return neighbors

def reconstructPath(cameFrom,current,drawFunc):

    while current in cameFrom:

        current=cameFrom[current]        

        if not current.is_start:
            current.color=ORANGE

        drawFunc()

        pygame.time.delay(50)



def dfs(drawFunc,grid,start,goal,rows,cols):
    stack=[]
    stack.append(start)

    cameFrom={}
    visited=set()

    explore_nodes=0

    while stack:

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                return False,explore_nodes

        current=stack.pop()

        if current in visited:
            continue

        visited.add(current)

        explore_nodes +=1

        if not current.is_start and not current.is_goal:
            current.color=PURPLE
        drawFunc()
        pygame.time.delay(40)    

        if current==goal:
            reconstructPath(cameFrom,current,drawFunc)
            return True,explore_nodes

        for neighbor in getNeighbors(grid,current,rows,cols):
            if neighbor not in visited:
                cameFrom[neighbor]=current
                stack.append(neighbor)   

       

    return False,explore_nodes                    
