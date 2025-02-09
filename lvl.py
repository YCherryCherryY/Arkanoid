import pygame
cl = ['red', 'green', 'yellow', 'blue']
RED = 'red'
GREEN = 'green2'
BLUE = 'blue3'
YELLOW = 'yellow2'
BLACK = (35, 35, 35)
ORANGE = 'orange2'
BROWN = 'orange4'
CYAN = 'cyan'
Peach = (255, 160, 50)


def lvl1():
    block_list = [pygame.Rect(16 + 80 + 80 * j, 71 + 35*3 + 35 * i, 75, 30) for i in range(4) for j in range(8)]
    color_list = [RED, GREEN, YELLOW, GREEN, GREEN, BLUE, RED, GREEN,
                  BLUE, RED, GREEN, YELLOW, BLUE, RED, BLUE, RED,
                  YELLOW, BLUE, RED, BLUE, RED, YELLOW, YELLOW, BLUE,
                  GREEN, YELLOW, BLUE, RED, YELLOW, GREEN, GREEN, YELLOW]
    return block_list, color_list, 4*8


def lvl2():
    block_list = [pygame.Rect(176 + 80 * j, 71 + 35 * 2 + 35 * i, 75, 30) for i in range(7) for j in range(6)]
    block_list.append(pygame.Rect(176, 71, 75, 30))
    block_list.append(pygame.Rect(176, 106, 75, 30))
    block_list.append(pygame.Rect(576, 71, 75, 30))
    block_list.append(pygame.Rect(576, 106, 75, 30))
    color_list = [ORANGE] * 42
    color_list[13] = CYAN
    color_list[16] = CYAN
    color_list[26] = BROWN
    color_list[27] = BROWN
    color_list[32] = BROWN
    color_list[33] = BROWN
    color_list[38] = BROWN
    color_list[39] = BROWN
    color_list.append(BLACK)
    color_list.append(BLACK)
    color_list.append(BLACK)
    color_list.append(BLACK)
    return block_list, color_list, 46


def lvl3():
    block_list = [pygame.Rect(96 + 80 * j, 141, 75, 30) for j in range(8)]
    block_list.extend([pygame.Rect(256 + 80 * j, 176, 75, 30) for j in range(4)])
    block_list.extend([pygame.Rect(16 + 80 * j, 211, 75, 30) for j in range(10)])
    block_list.extend([pygame.Rect(256 + 80 * j, 246, 75, 30) for j in range(4)])
    block_list.extend([pygame.Rect(16 + 80 * j, 281, 75, 30) for j in range(10)])
    block_list.extend([pygame.Rect(256 + 80 * j, 316, 75, 30) for j in range(4)])
    block_list.extend([pygame.Rect(96 + 80 * j, 351, 75, 30) for j in range(3)])
    block_list.extend([pygame.Rect(496 + 80 * j, 351, 75, 30) for j in range(3)])
    block_list.append(pygame.Rect(96, 71, 75, 30))
    block_list.append(pygame.Rect(96, 106, 75, 30))
    block_list.append(pygame.Rect(656, 71, 75, 30))
    block_list.append(pygame.Rect(656, 106, 75, 30))
    block_list.append(pygame.Rect(96, 386, 75, 30))
    block_list.append(pygame.Rect(656, 386, 75, 30))
    block_list.append(pygame.Rect(336, 106, 75, 30))
    block_list.append(pygame.Rect(416, 106, 75, 30))

    color_list = [BLACK] * 52
    color_list.append(RED)
    color_list.append(RED)
    return block_list, color_list, 54


def lvl4():
    block_list = [pygame.Rect(16 + 80 + 160 * j, 71 + 70 * i, 75, 30) for i in range(5) for j in range(5)]
    block_list.extend([pygame.Rect(16 + 160 * j, 71 + 35 + 70 * i, 75, 30) for i in range(5) for j in range(5)])
    color_list = [Peach] * 50
    return block_list, color_list, 50


def lvl5():
    block_list = [pygame.Rect(16 + 80 * j, 71 + 35 * i, 75, 30) for i in range(10) for j in range(10)]
    color_list = [YELLOW] * 100
    color_list[13] = BLACK
    color_list[23] = BLACK
    color_list[33] = BLACK
    color_list[43] = BLACK
    color_list[16] = BLACK
    color_list[26] = BLACK
    color_list[36] = BLACK
    color_list[46] = BLACK
    color_list[61] = BLACK
    color_list[68] = BLACK
    for i in range(71,79):
        color_list[i] = BLACK
    color_list[86] = RED
    color_list[87] = RED
    color_list[96] = RED
    color_list[97] = RED
    return block_list, color_list, 100
