import os
import ast
import random
import pygame

def createMatrix(n, key=""):
    return [[random.choice([0, 1]) if key == "random" else 0 for x in range(n)] for x in range(n)]

def swapMatrices(matrix1, matrix2):
    for i in range(len(matrix2)):
        for j in range(len(matrix2)):
            matrix1[i][j] = matrix2[i][j]

    return matrix1

def countNeighbours(matrix, location):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = (location[0] + i + len(matrix)) % len(matrix)
            y = (location[1] + j + len(matrix)) % len(matrix)
            neighbours += matrix[x][y]

    neighbours -= matrix[location[0]][location[1]]

    return neighbours

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

def printOrganism(matrix):
    locations = []
    [[locations.append((i, j)) for j in range(len(matrix)) if matrix[i][j] == 1] for i in range(len(matrix))]
    print(locations)

def toggleCellState(size, matrix):
    cellsize = int(size/len(matrix))
    cursor = pygame.mouse.get_pos()
    for x in range(0, size, cellsize):
        for y in range(0, size, cellsize):
            if x < cursor[0] < x + cellsize and y < cursor[1] < y + cellsize:
                matrix[int(y /(cellsize))][int(x/(cellsize))] = 1 - matrix[int(y/(cellsize))][int(x/(cellsize))]

    return matrix

def draw(screen, size, matrix, colour1, colour2):
    cellsize = int(size/len(matrix))
    [[pygame.draw.rect(screen, colour1, (j*(cellsize), i*(cellsize), cellsize, cellsize)) for i in range(len(matrix)) if matrix[i][j] == 1] for j in range(len(matrix))]
    [[pygame.draw.rect(screen, colour2, (j*(cellsize), i*(cellsize), cellsize, cellsize)) for i in range(len(matrix)) if matrix[i][j] == 0] for j in range(len(matrix))]

def drawGrid(screen, size, matrix, colour):
    cellsize = int(size/len(matrix))
    [pygame.draw.line(screen, colour, (0, i*(cellsize)), (size, i*(cellsize))) for i in range(len(matrix))]
    [pygame.draw.line(screen, colour, (i*(cellsize), 0), (i*(cellsize), size)) for i in range(len(matrix))]
