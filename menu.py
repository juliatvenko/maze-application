import pygame

from maze_create import create_maze
from maze_search import search_maze

def redrawWindow(win, button1, button2):
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (200, 200, 200), button1)
    pygame.draw.rect(win, (200, 200, 200), button2)
    font = pygame.font.SysFont('comicsans', 16)

    label1 = font.render('Create Maze', 1, (0, 0, 0))
    label2 = font.render('Search Maze', 1, (0, 0, 0))
    win.blit(label1, (button1.x + button1.width / 2 - label1.get_width() / 2, button1.y + button1.height / 2 - label1.get_height() / 2))
    win.blit(label2, (button2.x + button2.width / 2 - label2.get_width() / 2, button2.y + button2.height / 2 - label2.get_height() / 2))

def main_menu():
    pygame.init()
    win = pygame.display.set_mode((300, 350))
    run = True

    button1 = pygame.Rect(50, 100, 200, 50)
    button2 = pygame.Rect(50, 200, 200, 50)

    while run:
        redrawWindow(win, button1, button2)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(pos):
                    print('Clicked the "Create Maze" button')
                    create_maze()
                    return  # Return after the maze is created
                if button2.collidepoint(pos):
                    print('Clicked the "Search Maze" button')
                    search_maze()
                    return  # Return after the maze is searched

    pygame.quit()

if __name__ == "__main__":
    main_menu()

