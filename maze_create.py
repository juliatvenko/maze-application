import pygame

def create_maze():
    # Maze settings
    maze_width = 10  # Width of the maze in cells
    maze_height = 10  # Height of the maze in cells
    start_point = None
    end_point = None

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    LIGHT_GRAY = (200, 200, 200)

    # Maze cell size
    CELL_SIZE = 40

    # Initialize pygame
    pygame.init()

    # Set up the display
    window_width = maze_width * CELL_SIZE
    window_height = maze_height * CELL_SIZE + 50  # Add space for menu bar
    screen = pygame.display.set_mode((window_width, window_height))

    # Maze grid
    maze_grid = [[[False, False, False, False] for _ in range(maze_width)] for _ in range(maze_height)]  # Walls: [top, right, bottom, left]

    # Button settings
    button_radius = 5  # The radius of the buttons
    button_colors = [BLACK, GREEN, RED]
    button_positions = [(i * (button_radius * 2 + 10) + 10, 10) for i in range(3)]

    # Current mode
    current_mode = 0  # 0 - Add Wall, 1 - Add Start, 2 - Add End

    def draw_start_and_end_points():
        if start_point is not None:
            pygame.draw.rect(screen, GREEN, (start_point[1] * CELL_SIZE + 5, start_point[0] * CELL_SIZE + 55, CELL_SIZE - 10, CELL_SIZE - 10))
        if end_point is not None:
            pygame.draw.rect(screen, RED, (end_point[1] * CELL_SIZE + 5, end_point[0] * CELL_SIZE + 55, CELL_SIZE - 10, CELL_SIZE - 10))

    def draw_grid(surface):
        for y in range(maze_height):
            for x in range(maze_width):
                pygame.draw.rect(surface, LIGHT_GRAY, (x * CELL_SIZE, y * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE), 1)

    def draw_walls():
        for y in range(maze_height):
            for x in range(maze_width):
                if maze_grid[y][x][0]:  # Top wall
                    pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE + 50), ((x + 1) * CELL_SIZE, y * CELL_SIZE + 50), 2)
                if maze_grid[y][x][1]:  # Right wall
                    pygame.draw.line(screen, BLACK, ((x + 1) * CELL_SIZE, y * CELL_SIZE + 50), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE + 50), 2)
                if maze_grid[y][x][2]:  # Bottom wall
                    pygame.draw.line(screen, BLACK, (x * CELL_SIZE, (y + 1) * CELL_SIZE + 50), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE + 50), 2)
                if maze_grid[y][x][3]:  # Left wall
                    pygame.draw.line(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE + 50), (x * CELL_SIZE, (y + 1) * CELL_SIZE + 50), 2)

    def get_clicked_side(cell_pos, mouse_pos):
        cell_x, cell_y = cell_pos
        cell_x_pixel = cell_x * CELL_SIZE
        cell_y_pixel = cell_y * CELL_SIZE + 50

        rel_x = mouse_pos[0] - cell_x_pixel
        rel_y = mouse_pos[1] - cell_y_pixel

        if rel_x < rel_y:  # upper left triangle
            if CELL_SIZE - rel_x < rel_y:  # lower left triangle
                return "bottom"
            else:
                return "left"
        else:  # lower right triangle
            if CELL_SIZE - rel_x < rel_y:  # lower left triangle
                return "right"
            else:
                return "top"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if any button is pressed
                for i, button_pos in enumerate(button_positions):
                    button_rect = pygame.Rect(button_pos[0], button_pos[1], button_radius * 2, button_radius * 2)
                    if button_rect.collidepoint(mouse_pos):
                        current_mode = i
                        break
                else:  # If no button is pressed, check the cells
                    cell_pos = (mouse_pos[1] - 50) // CELL_SIZE, mouse_pos[0] // CELL_SIZE
                    if 0 <= cell_pos[0] < maze_height and 0 <= cell_pos[1] < maze_width:
                        if current_mode == 0:
                            clicked_side = get_clicked_side(cell_pos, mouse_pos)
                            if clicked_side == "top" and cell_pos[0] > 0:
                                maze_grid[cell_pos[0]][cell_pos[1]][0] = not maze_grid[cell_pos[0]][cell_pos[1]][0]
                                maze_grid[cell_pos[0]-1][cell_pos[1]][2] = maze_grid[cell_pos[0]][cell_pos[1]][0]
                            elif clicked_side == "right" and cell_pos[1] < maze_width - 1:
                                maze_grid[cell_pos[0]][cell_pos[1]][1] = not maze_grid[cell_pos[0]][cell_pos[1]][1]
                                maze_grid[cell_pos[0]][cell_pos[1]+1][3] = maze_grid[cell_pos[0]][cell_pos[1]][1]
                            elif clicked_side == "bottom" and cell_pos[0] < maze_height - 1:
                                maze_grid[cell_pos[0]][cell_pos[1]][2] = not maze_grid[cell_pos[0]][cell_pos[1]][2]
                                maze_grid[cell_pos[0]+1][cell_pos[1]][0] = maze_grid[cell_pos[0]][cell_pos[1]][2]
                            elif clicked_side == "left" and cell_pos[1] > 0:
                                maze_grid[cell_pos[0]][cell_pos[1]][3] = not maze_grid[cell_pos[0]][cell_pos[1]][3]
                                maze_grid[cell_pos[0]][cell_pos[1]-1][1] = maze_grid[cell_pos[0]][cell_pos[1]][3]
                        elif current_mode == 1:
                            start_point = cell_pos
                        elif current_mode == 2:
                            end_point = cell_pos

        screen.fill(WHITE)

        draw_grid(screen)
        draw_start_and_end_points()
        draw_walls()

        # Draw buttons
        for button_pos, color in zip(button_positions, button_colors):
            pygame.draw.ellipse(screen, color, (button_pos[0], button_pos[1], button_radius * 2, button_radius * 2))

        pygame.display.flip()

    pygame.quit()







