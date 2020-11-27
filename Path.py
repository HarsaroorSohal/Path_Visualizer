#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import random
import math
from queue import PriorityQueue


# In[2]:


# capitol variables -> global
SIZE = 800
GAME = pygame.display.set_mode((SIZE,SIZE)) #initialize a screen for display
pygame.display.set_caption("A* Algorithm Visualization") #naming the game.


# In[3]:


#colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# In[4]:


#self refers to this instance of the object.
class Node:
    def __init__(self,row,col,size, n): #row index, col index, size of a node
        self.row = row
        self.col = col
        self.size = size
        self.n = n # total number of rows/cols
        self.x = row * size # x position
        self.y = col * size # y position
        self.color = WHITE # initially all nodes are white
        self.neighbors = [] # empty list initally
    def get_pos(self):
        return(self.row,self.col) # return index of row and col
    def is_visited(self):
        return self.color == RED
    def is_blocked(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == TURQUOISE
    def is_end(self):
        return self.color == ORANGE
    
    def reset(self):
        self.color = WHITE 
    def path(self):
        self.color = PURPLE
    def block(self):
        self.color = BLACK
    def visit(self):
        self.color = BLUE
    def close(self):
        self.color = RED
    def start(self):
        self.color = TURQUOISE
    def end(self):
        self.color = ORANGE
        
    def draw(self,screen): #drawing a rectangle at x,y postion in the screen.
        pygame.draw.rect(screen,self.color, (self.x,self.y,self.size,self.size))
    
    def get_neighbors(self,grid,n):
        if self.row > 0 and not grid[self.row-1][self.col].is_blocked():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.row < n-1 and not grid[self.row+1][self.col].is_blocked():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.col > 0 and not grid[self.row][self.col-1].is_blocked():
            self.neighbors.append(grid[self.row][self.col-1])
        if self.col < n-1 and not grid[self.row][self.col+1].is_blocked():
            self.neighbors.append(grid[self.row][self.col+1])
    def __lt__(self,other):
        return False


# In[5]:


def heuristic(nodeA, nodeB): # the distance variable in A* (manhattan distance)
    x1,y1 = nodeA
    x2,y2 = nodeB
    return(abs(x1-x2) + abs(y1-y2)) #manhatan distance

def path(parent,curr,draw): #retracing the path using parent
    path_size = 0
    while curr in parent:
        path_size = path_size + 1
        curr = parent[curr]
        curr.path()
        draw()
    print(path_size)
def maze(grid):
    density = SIZE//10
    for i in range(density):
        row = random.randrange(len(grid))
        col = random.randrange(len(grid))
        grid[row][col].block()
        
def astar(draw , grid, start,end):
    pq = PriorityQueue()
    pq.put((0,start)) #insert (dist,start)
    parent = {}
    dist = {node : float("inf") for row in grid for node in row} #initialize the distance of all nodes as infinity in a list
    dist[start] = 0
    f_score = {node : float("inf") for row in grid for node in row} #initialize the distance of all nodes as infinity in a list
    f_score[start] = dist[start] + heuristic(start.get_pos(),end.get_pos())
    visits = 0
    visiting_set = {start} #acts as a set
    while not pq.empty():
        for event in pygame.event.get(): #breaking out of the while loop
            if event.type == pygame.QUIT:
                pygame.quit()
        visits = visits + 1
        curr = pq.get()[1] #it returs an array of (dist,node)
        visiting_set.remove(curr) #poping that element
        if(curr==end): #construct the path using parent array
            path(parent,end, draw)
            end.path()
            print(visits)
            return True
        for neighbor in curr.neighbors:
            if dist[neighbor] > dist[curr] + 1:
                dist[neighbor] = dist[curr] + 1
                parent[neighbor] = curr
                f_score[neighbor] = dist[neighbor] + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in visiting_set:
                    pq.put((f_score[neighbor],neighbor))
                    visiting_set.add(neighbor)
                    neighbor.visit() #changing its color to blue
        
        draw()
        if(curr!=start):
            curr.close()

def dijkstra(draw , grid, start,end):
    pq = PriorityQueue()
    pq.put((0,start)) #insert (dist,start)
    parent = {}
    dist = {node : float("inf") for row in grid for node in row} #initialize the distance of all nodes as infinity in a list
    dist[start] = 0
    visiting_set = {start} #acts as a set
    while not pq.empty():
        for event in pygame.event.get(): #breaking out of the while loop
            if event.type == pygame.QUIT:
                pygame.quit()
        curr = pq.get()[1] #it returs an array of (dist,node)
        visiting_set.remove(curr) #poping that element
        if(curr==end): #construct the path using parent array
            path(parent,end, draw)
            end.path()
            return True
        for neighbor in curr.neighbors:
            if dist[neighbor] > dist[curr] + 1:
                dist[neighbor] = dist[curr] + 1
                parent[neighbor] = curr
                if neighbor not in visiting_set:
                    pq.put((dist[neighbor],neighbor))
                    visiting_set.add(neighbor)
                    neighbor.visit() #changing its color to blue
        
        draw()
        if(curr!=start):
            curr.close()


# In[6]:




#making a 2D grid of size (n x n) nodes.
def make_grid(n,size): #n -> numbers of rows/cols
    grid = []
    node_size = size // n #integer division
    #size is the width/height of the grid
    for i in range(n): # range returns an iterable object of rows size
        curr_node = []
        for j in range(n):
            new_node = Node(i,j,node_size,n)
            curr_node.append(new_node)
        grid.append(curr_node)
    return grid

def draw_grid(screen,n,size):
    node_size = size // n
    for i in range(n): #horizontal lines, (0,0) is top left.
        pygame.draw.line(screen,GREY,(0,i * node_size),(size,i*node_size))
    for i in range(n): #vertical lines
        pygame.draw.line(screen,GREY,(i*node_size,0), (i*node_size, size))

def draw(screen, grid,n,size):
    screen.fill(WHITE) #continous loop
    for row in grid:
        for node in row:
            node.draw(screen) #draw all the nodes with their colors
    draw_grid(screen,n,size)
    pygame.display.update() #updates the whole screen if no arguement
    
      


# In[7]:


def click_pos(mouse_pos, n , size):
    node_size = size // n
    y,x = mouse_pos
    row_index = y // node_size
    col_index = x // node_size
    return row_index,col_index


# In[8]:


def main(screen, size): #calling all functions
    n = 50
    grid = make_grid(n, size)
    start = None 
    end = None #intially start node and end node are not defined
    running = True # is game running
    started = False # Algo started
    
    while running:
        draw(screen,grid,n,size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if started:
                continue # ignore all events when algo is running    
            if pygame.mouse.get_pressed()[0]: #left mouse button
                pos = pygame.mouse.get_pos()
                row_index, col_index = click_pos(pos,n,size)
                clicked_node = grid[row_index][col_index]
                
                if not start and not end:
                    start = clicked_node
                    clicked_node.start()
                elif not end and clicked_node != start:
                    end = clicked_node
                    clicked_node.end()
                elif clicked_node != start and clicked_node != end:
                    clicked_node.block()
                
            elif pygame.mouse.get_pressed()[2]: #right mouse button
                pos = pygame.mouse.get_pos()
                row_index, col_index = click_pos(pos,n,size)
                clicked_node = grid[row_index][col_index]
                clicked_node.reset()
                if clicked_node == start:
                    start = None
                if clicked_node == end:
                    end = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and not started and start and end:
                    for row in grid:
                        for node in row:
                            node.get_neighbors(grid,n)
                    #temp_grid = grid
                    astar(lambda: draw(screen,grid,n,size),grid,start,end)
                    #passing an anonymous function to algo so that we can call it later.
                if event.key == pygame.K_d and not started and start and end:
                    for row in grid:
                        for node in row:
                            node.get_neighbors(grid,n)
                    #temp_grid = grid
                    dijkstra(lambda: draw(screen,grid,n,size),grid,start,end)
                if event.key == pygame.K_r and not started:
                    maze(grid)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(n,size)
                if event.key == pygame.K_z:
                    grid = temp_grid
    pygame.quit()
    
main(GAME,SIZE)


# In[ ]:





# In[ ]:





# In[ ]:


8

