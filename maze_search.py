import pygame, time
from collections import deque

def search_maze():

    def load_maze(filename):
        with open(filename, 'r') as f:
            maze_data = []

            for line in f:
                line = line.rstrip('\n')
                maze_data.append(line)

        start = tuple(map(int, maze_data[-2].strip().split())) if len(maze_data) >= 2 else ()
        end = tuple(map(int, maze_data[-1].strip().split())) if len(maze_data) >= 1 else ()

        return maze_data[:-2], start, end

    maze_data, start_point, end_point = load_maze('maze.txt')

    def generate_maze_graph(maze_data):
        maze_graph = {}
        for y in range(1, len(maze_data), 2):
            for x in range(1, min(len(maze_data[y]), len(maze_data[y-1]), len(maze_data[(y+1)%len(maze_data)])), 2):
                if maze_data[y][x] == ' ':
                    moves = set()
                    # check north
                    if y > 1 and maze_data[y-1][x] == ' ':
                        moves.add('N')
                    # check south
                    if y < len(maze_data)-2 and maze_data[y+1][x] == ' ':
                        moves.add('S')
                    # check west
                    if x > 1 and maze_data[y][x-1] == ' ':
                        moves.add('W')
                    # check east
                    if x < len(maze_data[y])-2 and maze_data[y][x+1] == ' ':
                        moves.add('E')
                    maze_graph[(y//2, x//2)] = moves  # Convert coordinates to match cell locations
        return maze_graph

    maze_graph = generate_maze_graph(maze_data)



    

    # Maze settings
    maze_width = 8  # Width of the maze in cells
    maze_height = 8  # Height of the maze in cells

    #start_point = (0, 0)
    #end_point = (0, 4)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Maze cell size
    CELL_SIZE = 40

    # Initialize pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((maze_width * CELL_SIZE, maze_height * CELL_SIZE))

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    def draw_maze_from_graph(maze_graph, surface):
        for (y, x), moves in maze_graph.items():
            pygame.draw.rect(surface, LIGHT_GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if 'N' not in moves:
                pygame.draw.line(surface, BLACK, (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE), 2)
            if 'S' not in moves:
                pygame.draw.line(surface, BLACK, (x * CELL_SIZE, (y + 1) * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 2)
            if 'W' not in moves:
                pygame.draw.line(surface, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE), 2)
            if 'E' not in moves:
                pygame.draw.line(surface, BLACK, ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), 2)

    def draw_start_and_end_points(surface):
        end_rect = pygame.Rect(end_point[1] * CELL_SIZE + 5, end_point[0] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(surface, RED, end_rect)
        start_rect = pygame.Rect(start_point[1] * CELL_SIZE + 5, start_point[0] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(surface, GREEN, start_rect)

    def bfs(maze_graph, start_point, end_point):
        queue = deque([(start_point, [])])
        visited = set()

        start_time = time.time()  # Start measuring time

        while queue:
            node, path = queue.popleft()
            if node == end_point:
                end_time = time.time()  # Stop measuring time
                execution_time = end_time - start_time  # Calculate execution time
                return path + [node], execution_time

            if node in visited:
                continue

            visited.add(node)

            for direction in maze_graph[node]:
                if direction == 'N':
                    neighbor = (node[0] - 1, node[1])
                elif direction == 'S':
                    neighbor = (node[0] + 1, node[1])
                elif direction == 'W':
                    neighbor = (node[0], node[1] - 1)
                elif direction == 'E':
                    neighbor = (node[0], node[1] + 1)

                queue.append((neighbor, path + [node]))

        return None, None



    def dfs(maze_graph, start_point, end_point):
        stack = [(start_point, [])]
        visited = set()

        start_time = time.time()  # Start measuring time

        while stack:
            node, path = stack.pop()  # Different from BFS, DFS uses stack
            if node == end_point:
                end_time = time.time()  # Stop measuring time
                execution_time = end_time - start_time  # Calculate execution time
                return path + [node], execution_time

            if node in visited:
                continue

            visited.add(node)

            for direction in maze_graph[node]:
                if direction == 'N':
                    neighbor = (node[0] - 1, node[1])
                elif direction == 'S':
                    neighbor = (node[0] + 1, node[1])
                elif direction == 'W':
                    neighbor = (node[0], node[1] - 1)
                elif direction == 'E':
                    neighbor = (node[0], node[1] + 1)

                stack.append((neighbor, path + [node]))  # Push neighbor to the stack

        return None, None


    #path = dfs(maze_graph, start_point, end_point)
    #print(path)

    # Set up the display
    window_width = maze_width * CELL_SIZE
    window_height = maze_height * CELL_SIZE
    line_width = 5
    screen_width=window_width * 2+line_width
    screen_height=window_height + 140
    screen = pygame.display.set_mode((screen_width, screen_height))  # Double the width to accommodate two mazes

    def draw_path(path, color, surface):
        for point in path:
            path_rect = pygame.Rect(point[1] * CELL_SIZE + 5, point[0] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
            pygame.draw.rect(surface, color, path_rect)

    path_bfs, execution_time_bfs = bfs(maze_graph, start_point, end_point)
    path_dfs, execution_time_dfs = dfs(maze_graph, start_point, end_point)

    # Create a font object
    font = pygame.font.Font(None, 45)  # None for default font, font_size for font size
    small_font = pygame.font.Font(None, 30)

    bfs_text = "BFS"
    dfs_text = "DFS"

    # Create two separate surfaces for BFS and DFS
    surface_bfs = pygame.Surface((window_width, window_height))
    surface_dfs = pygame.Surface((window_width, window_height))
    line_surface = pygame.Surface((line_width, screen_height))
    bfs_text_surface = font.render(bfs_text, True, BLACK)  
    dfs_text_surface = font.render(dfs_text, True, BLACK) 



    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        surface_bfs.fill(WHITE)
        surface_dfs.fill(WHITE)
        line_surface.fill(BLACK)

        draw_maze_from_graph(maze_graph, surface_bfs)
        draw_maze_from_graph(maze_graph, surface_dfs)
    
        if path_bfs is not None:
            draw_path(path_bfs, BLUE, surface_bfs)
            
        if path_dfs is not None:
            draw_path(path_dfs, YELLOW, surface_dfs)

        bfs_route_length = len(path_bfs) if path_dfs else float('inf')
        dfs_route_length = len(path_dfs) if path_dfs else float('inf')
    
        bfs_length_text = "Length: " + str(bfs_route_length)
        dfs_length_text = "Length: " + str(dfs_route_length)

        bfs_time_text = str(round(execution_time_bfs, 10)) + " seconds"
        dfs_time_text = str(round(execution_time_dfs, 10)) + " seconds"
        
        bfs_length_surface = font.render(bfs_length_text, True, BLACK)  
        dfs_length_surface = font.render(dfs_length_text, True, BLACK)   

        bfs_time_surface = small_font.render(bfs_time_text, True, RED)  
        dfs_time_surface = small_font.render(dfs_time_text, True, RED) 
        
        draw_start_and_end_points(surface_bfs)
        draw_start_and_end_points(surface_dfs)

        # Draw the BFS and DFS surfaces onto the screen side by side
        screen.blit(surface_bfs, (0, 0))
        screen.blit(line_surface, (window_width, 0))
        screen.blit(surface_dfs, (window_width+line_width-2, 0))
        screen.blit(bfs_text_surface, (window_width*0.41, window_height+20))
        screen.blit(dfs_text_surface, (window_width*1.42, window_height+20))
        screen.blit(bfs_length_surface, (window_width*0.26, window_height+60))
        screen.blit(dfs_length_surface, (window_width*1.28, window_height+60))
        screen.blit(bfs_time_surface, (50, window_height+100))
        screen.blit(dfs_time_surface, (window_width+line_width+48, window_height+100))

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()
