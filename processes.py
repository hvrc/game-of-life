import os, ast, random, pygame

# creates a nested list of dimensions n by n, containing 0s
# if key is "random", matrix is populated with random choice of 0s or 1s
def createMatrix(n, key=""):
    return [[random.choice([0, 1]) if key == "random" else 0 for x in range(n)] for x in range(n)]

# two matrices are swapped with each other and the first matrix is returned
def swapMatrices(matrix1, matrix2):
    for i in range(len(matrix2)):
        for j in range(len(matrix2)):
            matrix1[i][j] = matrix2[i][j]

    return matrix1

# returns the sum of the states of cells neighbouring the spcified location
def countNeighbours(matrix, location):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = (location[0] + i + len(matrix)) % len(matrix)
            y = (location[1] + j + len(matrix)) % len(matrix)
            neighbours += matrix[x][y]

    neighbours -= matrix[location[0]][location[1]]

    return neighbours

# SEE: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules
# creates a copy of the current matrix, iterates over each cell in current matrix,
# counts neighbours of the cell being iterated over, changes state of cell in the
# copied matrix according to the number of neighbours, returns copied matrix
def interact(matrix):
    next = swapMatrices(createMatrix(len(matrix)), matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            neighbours = countNeighbours(matrix, (i, j))
            if matrix[i][j] == 0 and neighbours == 3:
                next[i][j] = 1
            elif matrix[i][j] == 1 and (neighbours < 2 or neighbours > 3):
                next[i][j] = 0

    return swapMatrices(matrix, next)

# spawns organism by reading the taxonomy file
def generateOrganism(taxonomy, organism, matrix):
    data = open(taxonomy, "r")
    for line in data:
        if organism == line.split(":")[0]:
            organismData = ast.literal_eval(line.split(":")[1])
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in organismData:
                if k[0] == i and k[1] == j:
                    matrix[i][j] = 1

    return matrix

# prints co-ordinates of live cells
def printOrganism(matrix):
    locations = []
    [[locations.append((i, j)) for j in range(len(matrix)) if matrix[i][j] == 1] for i in range(len(matrix))]
    print(locations)

# toggles state of cell being hovered over
def toggleCellState(size, matrix):
    cellsize = int(size/len(matrix))
    cursor = pygame.mouse.get_pos()
    for x in range(0, size, cellsize):
        for y in range(0, size, cellsize):
            if x < cursor[0] < x + cellsize and y < cursor[1] < y + cellsize:
                matrix[int(y/(cellsize))][int(x/(cellsize))] = 1 - matrix[int(y/(cellsize))][int(x/(cellsize))]

    return matrix

# draw cells
def draw(screen, size, matrix, colour1, colour2):
    cellsize = int(size/len(matrix))
    [[pygame.draw.rect(screen, colour1, (j*(cellsize), i*(cellsize), cellsize, cellsize)) for i in range(len(matrix)) if matrix[i][j] == 1] for j in range(len(matrix))]
    [[pygame.draw.rect(screen, colour2, (j*(cellsize), i*(cellsize), cellsize, cellsize)) for i in range(len(matrix)) if matrix[i][j] == 0] for j in range(len(matrix))]

# draw grid
def drawGrid(screen, size, matrix, colour):
    cellsize = int(size/len(matrix))
    [pygame.draw.line(screen, colour, (0, i*(cellsize)), (size, i*(cellsize))) for i in range(len(matrix))]
    [pygame.draw.line(screen, colour, (i*(cellsize), 0), (i*(cellsize), size)) for i in range(len(matrix))]
