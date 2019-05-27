from processes import *

def main():

    n = 35
    size = 700

    framerate = 20
    paused = True
    showGrid = True
    taxonomyPath = os.getcwd() + "/taxonomy.txt"

    current = createMatrix(n)

    pygame.init()
    screen = pygame.display.set_mode((size, size))

    while True:

        draw(screen, size, current, (255, 235, 235), (40, 40, 40))

        if paused:
            if showGrid:
                drawGrid(screen, size, current, (50, 50, 50))

        else:
            current = interact(current)
            if showGrid:
                drawGrid(screen, size, current, (45, 45, 45))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: quit()

                if event.key == pygame.K_RETURN:
                    paused = not paused
                if event.key == pygame.K_SPACE:
                    current = interact(current)
                if event.key == pygame.K_BACKSPACE:
                    current = createMatrix(n)
                if event.key == pygame.K_r:
                    current = createMatrix(n, "random")
                if event.key == pygame.K_g:
                    showGrid = not showGrid

                if event.key == pygame.K_RIGHTBRACKET:
                    framerate = int(framerate*10)
                if event.key == pygame.K_LEFTBRACKET:
                    framerate = int(framerate/5)

                if event.key == pygame.K_BACKQUOTE:
                    printOrganism(current)
                if event.key == pygame.K_1:
                    current = generateOrganism(taxonomyPath, "Glider", current)
                if event.key == pygame.K_2:
                    current = generateOrganism(taxonomyPath, "Lightweight spaceship", current)
                if event.key == pygame.K_3:
                    current = generateOrganism(taxonomyPath, "Middleweight spaceship", current)
                if event.key == pygame.K_4:
                    current = generateOrganism(taxonomyPath, "Heavyweight spaceship", current)
                if event.key == pygame.K_0:
                    current = generateOrganism(taxonomyPath, "Gosper Glider Gun", current)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHTBRACKET:
                    framerate = int(framerate/10)
                if event.key == pygame.K_LEFTBRACKET:
                    framerate = int(framerate*5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                current = toggleCellState(size, current)

        pygame.display.update()
        pygame.time.Clock().tick(framerate if not paused else 500)

if __name__ == "__main__":
    main()
