
import time
from collections import deque
from heapq import heappush, heappop

# Reading the file and processing the input
with open("Sample1.txt", "r") as f:
    directionn = f.readlines()

for i in range(len(directionn)):
    directionn[i] = directionn[i].rstrip("\n")
    directionn[i] = directionn[i].split(",") 

b = directionn[0][0].split('*') 
n = int(b[0])
del directionn[0]

Start = directionn[n]
End = directionn[n+1]

start_list = [int(item.replace('(', '').replace(')', ''))-1 for item in Start]
End_list = [int(item.replace('(', '').replace(')', ''))-1 for item in End]

End_list = tuple(End_list)
start_list = tuple(start_list)

for i in range(2):
    del directionn[n] 

number_list = []
for i in range(len(directionn)):
    string_list = directionn[i][0].split()
    for num in string_list:
        number_list.append(int(num))

output_list = [number_list[i:i + n] for i in range(0, len(number_list), n)]

# BFS Algorithm
def bfs(matrix, start, end):
    n = len(matrix)
    m = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for direction in directions:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            new_point = (new_x, new_y)
            if 0 <= new_x < n and 0 <= new_y < m and matrix[new_x][new_y] == 0 and new_point not in visited:
                queue.append(new_point)
                visited.add(new_point)
                parent[new_point] = current
    return None

# DFS Algorithm
def dfs(matrix, start, end):
    n = len(matrix)
    m = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [start]
    visited = set([start])
    parent = {start: None}
    
    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for direction in directions:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            new_point = (new_x, new_y)
            if 0 <= new_x < n and 0 <= new_y < m and matrix[new_x][new_y] == 0 and new_point not in visited:
                stack.append(new_point)
                visited.add(new_point)
                parent[new_point] = current
    return None

# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1

def a_star(matrix, start, end):
    n = len(matrix)
    m = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        current = heappop(open_set)[2]
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m and matrix[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heappush(open_set, (f_score, tentative_g_score, neighbor))
    return None

# IDDFS Algorithm
def iddfs(matrix, start, end):
    def dfs_limit(node, depth):
        if depth == 0:
            if node == end:
                return [node]
            return None
        if depth > 0:
            for direction in directions:
                neighbor = (node[0] + direction[0], node[1] + direction[1])
                if 0 <= neighbor[0] < n and 0 <= neighbor[1] < m and matrix[neighbor[0]][neighbor[1]] == 0:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        path = dfs_limit(neighbor, depth - 1)
                        if path:
                            return [node] + path
                        visited.remove(neighbor)
        return None

    n = len(matrix)
    m = len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    depth = 0
    while True:
        visited = set()
        visited.add(start)
        path = dfs_limit(start, depth)
        if path:
            return path
        depth += 1

# Measure execution time for each algorithm
start_time = time.time()
path = bfs(output_list, start_list, End_list)
end_time = time.time()
print('bfs path:', path)
print('bfs time:', end_time - start_time)

start_time = time.time()
path = dfs(output_list, start_list, End_list)
end_time = time.time()
print("dfs Path:", path)
print('dfs time:', end_time - start_time)

start_time = time.time()
path = a_star(output_list, start_list, End_list)
end_time = time.time()
print("a* Path:", path)
print('a* time:', end_time - start_time)

start_time = time.time()
path = iddfs(output_list, start_list, End_list)
end_time = time.time()
print("iddfs Path:", path)
print('iddfs time:', end_time - start_time)

