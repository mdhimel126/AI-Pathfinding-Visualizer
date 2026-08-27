import pygame
import heapq

PURPLE=(119,107,219)
ORANGE=(255,152,0)

def getNeighbors(grid,node,rows,cols):

    neighbors=[]

    row,col=node.row,node.col

    if row >0 and not grid[row-1][col].is_wall:
        neighbors.append(grid[row-1][col])

    if row  < rows-1 and not grid[row+1][col].is_wall:
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
            pygame.time.delay(20)

def heuristic(nodeA,nodeB):
      x1,y1=nodeA.row,nodeA.col
      x2,y2=nodeB.row,nodeB.col

      return abs(x1-x2)+abs(y1-y2)


def aStar(drawFunc,grid,start,goal,rows,cols):
      count=0
      explore_nodes=0

      openSet=[]
      heapq.heappush(openSet,(0,count,start))

      cameFrom={}

      gScore={node:float("inf") for row in grid for node in row}
      gScore[start]=0

      fScore={node:float("inf") for row in grid for node in row}
      fScore[start]=heuristic(start,goal)

      openSetHash={start}

      while openSet:
            for event in pygame.event.get():
                  if event.type== pygame.QUIT:
                        pygame.quit()
                        return False

            current=heapq.heappop(openSet)[2]      
            openSetHash.remove(current)

            explore_nodes +=1

            if current==goal:
                  reconstructPath(cameFrom,current,drawFunc)
                  return True,explore_nodes


            for neighbor in getNeighbors(grid,current,rows,cols):

                  tempGScore=gScore[current]+1

                  if tempGScore < gScore[neighbor]:

                        cameFrom[neighbor]=current
                        gScore[neighbor]=tempGScore
                        fScore[neighbor]=tempGScore+heuristic(neighbor,goal)


                        if neighbor not in openSetHash:
                              count+=1
                              heapq.heappush(openSet,(fScore[neighbor],count,neighbor))
                              openSetHash.add(neighbor)

                              if not neighbor.is_goal:
                                    neighbor.color=PURPLE

                              drawFunc()
                              pygame.time.delay(40)

      return False,explore_nodes                    

