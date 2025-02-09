import sys

import pygame
import lvl
import configparser
import ButtonLib
from random import randrange as rnd

config = configparser.ConfigParser()  # создаём объект парсера
config.read("settings.ini")  # читаем конфиг

fps = 60
# display settings
display_w = 826
display_h = 675
# plying field
field_w = 800
field_h = 600
field_x = 13
field_y = 62
# paddle settings
paddle_w = 150
paddle_h = 19
paddle_speed = int(config["Paddle"]["paddle_speed"])
paddle = pygame.Rect(display_w // 2 - paddle_w // 2, display_h - paddle_h - 23, paddle_w, paddle_h)
# ball settings
ball_radius = 15
ball_speed = 0
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(display_w // 2 - ball_rect // 2, display_h - paddle_h - 23 - ball_rect, ball_rect, ball_rect)
dx, dy = 1, -1

Score, Hits = 0, 0


def detect_collision(dx, dy, bal, rect):
    if dx > 0:
        delta_x = bal.right - rect.left
    else:
        delta_x = rect.right - bal.left
    if dy > 0:
        delta_y = bal.bottom - rect.top
    else:
        delta_y = rect.bottom - bal.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


pygame.init()
dis = pygame.display.set_mode((display_w, display_h))
clock = pygame.time.Clock()
# background images
img = pygame.image.load('Fon_1.png').convert()
background = [img]
img = pygame.image.load('Fon_2.jpg').convert()
img = pygame.transform.scale(img, (display_w, display_h))
background.append(img)
img = pygame.image.load('Fon_3.jpg').convert()
img = pygame.transform.scale(img, (display_w, display_h))
background.append(img)
img = pygame.image.load('Fon_4.jpg').convert()
img = pygame.transform.scale(img, (display_w, display_h))
background.append(img)
img = pygame.image.load('Fon_5.jpg').convert()
img = pygame.transform.scale(img, (display_w, display_h))
background.append(img)
BG = 1


ramka = pygame.image.load('Ramka4.png').convert()
ramka.set_colorkey((255, 255, 255))
ramka = pygame.transform.scale(ramka, (826, 675))
heart = pygame.image.load('Heart.png').convert()
heart = pygame.transform.scale(heart, (33, 35))
bonusH = pygame.transform.scale(heart, (25, 26))
bonusH.set_colorkey((0, 0, 0))
heart.set_colorkey((0, 0, 0))
b1 = pygame.image.load('B1.jpg').convert()
b1.set_colorkey((255, 255, 255))
b1 = pygame.transform.scale(b1, (45, 45))
b2 = pygame.image.load('B2.jpg').convert()
b2.set_colorkey((255, 255, 255))
b2 = pygame.transform.scale(b2, (45, 45))
b4 = pygame.image.load('B4.jpg').convert()
b4.set_colorkey((255, 255, 255))
b4 = pygame.transform.scale(b4, (45, 45))
b5 = pygame.image.load('B5.jpg').convert()
b5.set_colorkey((255, 255, 255))
b5 = pygame.transform.scale(b5, (45, 45))
# many labels
HScore = config["Score"]["highScore"]

f1 = pygame.font.Font(None, 36)
text1 = f1.render('Уровень:', True, (0, 0, 0))
text2 = f1.render(str(1), True, (0, 0, 0))
textB = f1.render('Бесконечный', True, (0, 0, 0))
textS = f1.render('Очки:', True, (0, 0, 0))
textSN = f1.render(str(0), True, (0, 0, 0))
textHS = f1.render('Рекорд:', True, (0, 0, 0))
textHSN = f1.render(HScore, True, (0, 0, 0))

f2 = pygame.font.Font(None, 60)
labelW = f2.render("Вы выиграли!", False, (30, 155, 50), (0, 0, 0))
labelL = f2.render("Игра окончена", False, (130, 30, 50), (0, 0, 0))

labelS = f2.render('Настройки', True, (255, 255, 255))
labelA = f1.render('Оформление', True, (255, 255, 255))
labelMM = f1.render('Главное меню', True, (255, 255, 255))
labelRet = f1.render('Вернуться', True, (255, 255, 255))

f3 = pygame.font.Font(None, 25)
LSpace = f3.render('Космос', True, (255, 255, 255))
# Some buttons and it colors
Infinity = ButtonLib.Button()
Start = ButtonLib.Button()
Settings = ButtonLib.Button()
buttC = (30, 50, 255)
textC = (255, 255, 255)


def random_list():
    amou = rnd(5, 100, 1)
    temp = amou
    bl_list = []
    cl_list = []
    while temp != 0:
        x = rnd(16, 816, 80)
        y = rnd(71, 421, 35)
        if bl_list.count(pygame.Rect(x, y, 75, 30)) == 0:
            bl_list.append(pygame.Rect(x, y, 75, 30))
            temp -= 1
    for i in range(amou):
        cl_list.append((rnd(30, 255), rnd(30, 255), rnd(30, 255)))
    return amou, bl_list, cl_list


menu = True
game = False
InfGame = False
Settin = False
alreadyPressed = False
alreadyPMouse = False
apmUp = False
tempB = ball_speed

ap = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        alreadyPressed = (event.type == pygame.KEYDOWN)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            alreadyPMouse = True

    dis.blit(background[BG], (0, 0))
    if menu:
        # reset labels
        text2 = f1.render(str(1), True, (0, 0, 0))
        textSN = f1.render(str(0), True, (0, 0, 0))
        # reset paddle and ball
        paddle_speed = int(config["Paddle"]["paddle_speed"])
        ball_speed = 0
        paddle.topleft = (display_w // 2 - paddle_w // 2, display_h - paddle_h - 23)
        paddle.width = paddle_w
        ball.topleft = (display_w // 2 - ball_rect // 2, display_h - paddle_h - 23 - ball_rect)
        dx, dy = 1, -1
        # reset another parameters
        Score = 0
        Hits = 0
        lvlN = 1
        life = 3
        bonuses = []
        bonusesType = []
        # create buttons
        Str = ButtonLib.Button.create_button(Start, dis, buttC, display_w // 2 - 150, 300, 300, 50, 50, "Играть", textC)
        Inf = Infinity.create_button(dis, buttC, display_w // 2 - 225, 360, 450, 50, 90, "Бесконечная игра", textC)
        sett = Settings.create_button(dis, buttC, display_w // 2 - 150, 420, 300, 50, 65, "Настройки", textC)
        # Click the buttons
        if not Settin:
            if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and Start.pressed(pygame.mouse.get_pos()):
                # Score settings
                HScore = config["Score"]["highScore"]
                textHSN = f1.render(HScore, True, (0, 0, 0))
                # Block settings
                block_list, color_list, amount = lvl.lvl1()
                game = True
                menu = False
            if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and Settings.pressed(pygame.mouse.get_pos()):
                Settin = True
                alreadyPMouse = False

            if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and Infinity.pressed(pygame.mouse.get_pos()):
                HScore = config["Score"]["infHighScore"]
                textHSN = f1.render(HScore, True, (0, 0, 0))
                Score = 0
                Hits = 0
                amount, block_list, color_list = random_list()
                InfGame = True
                menu = False
    elif game:
        # Draw interface
        if life > 0:
            dis.blit(heart, (53, 27))
        if life > 1:
            dis.blit(heart, (90, 27))
        if life > 2:
            dis.blit(heart, (126, 27))

        dis.blit(ramka, (0, 0))
        dis.blit(text1, (200, 30))
        dis.blit(text2, (312, 30))
        dis.blit(textS, (375, 30))
        dis.blit(textSN, (450, 30))
        dis.blit(textHS, (590, 30))
        dis.blit(textHSN, (692, 30))
        # switch levels
        if not block_list:
            if lvlN == 1:
                ball.x, ball.y = paddle.x + ball_rect, paddle.y - ball_rect
                ball_speed = 0
                block_list, color_list, amount = lvl.lvl2()
                lvlN = 2
            elif lvlN == 2:
                ball.x, ball.y = paddle.x + ball_rect, paddle.y - ball_rect
                ball_speed = 0
                block_list, color_list, amount = lvl.lvl3()
                lvlN = 3
            elif lvlN == 3:
                ball.x, ball.y = paddle.x + ball_rect, paddle.y - ball_rect
                ball_speed = 0
                block_list, color_list, amount = lvl.lvl4()
                lvlN = 4
            elif lvlN == 4:
                ball.x, ball.y = paddle.x + ball_rect, paddle.y - ball_rect
                ball_speed = 0
                block_list, color_list, amount = lvl.lvl5()
                lvlN = 5
            else:
                dis.blit(labelW, (display_w // 2 - 150, display_h // 2))
                if Score > int(HScore):
                    config.set("Score", "highScore", str(Score))

                    HScore = config["Score"]["highScore"]
                    textHSN = f1.render(HScore, True, (130, 30, 50))
                ball_speed = 0
                paddle_speed = 0
                if pygame.key.get_pressed():
                    game = False
                    menu = True
            text2 = f1.render(str(lvlN), True, (0, 0, 0))
        hit = 0
        # Drawing world
        for i in range(amount):
            pygame.draw.rect(dis, pygame.Color(color_list[i]), block_list[i])
        pygame.draw.rect(dis, 'darkcyan', paddle)
        pygame.draw.circle(dis, pygame.Color('violet'), ball.center, ball_radius)
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        if bonuses:
            for bonus in bonuses:
                b = bonusesType[bonuses.index(bonus)]
                if b == 1:
                    dis.blit(b1, (bonus.x, bonus.y))
                elif b == 2:
                    dis.blit(b2, (bonus.x, bonus.y))
                elif b == 3:
                    pygame.draw.circle(dis, (30, 155, 255), bonus.center, bonus.height)
                    dis.blit(bonusH, (bonus.x - 2, bonus.y - 3))
                elif b == 4:
                    dis.blit(b4, (bonus.x, bonus.y))
                elif b == 5:
                    dis.blit(b5, (bonus.x, bonus.y))
                if not Settin:
                    bonus.y += 4
            hit_index = paddle.collidelist(bonuses)
            if hit_index != -1:
                hit_bonus = bonuses.pop(hit_index)
                hit_type = bonusesType.pop(hit_index)
                if hit_type == 1:
                    paddle.width += 50
                elif hit_type == 2:
                    if ball_speed > 2:
                        ball_speed /= 2
                elif hit_type == 3:
                    life += 1
                elif hit_type == 4:
                    paddle.width -= 50
                elif hit_type == 5:
                    if ball_speed < 8:
                        ball_speed += 2
        # collision blocks
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            amount = amount - 1
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            Hits += 1
            hit = True
            # bonuses
            b = rnd(1, 20)
            if b == 11 or b == 12:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(1)
            elif b == 14 or b == 15:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(2)
            elif b == 19:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(3)
            elif b == 17:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(4)
            elif b == 13 or b == 16:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(5)
            # special effect
            ball_speed += 0.5
        # collision left right
        if ball.centerx - field_x < ball_radius:
            dx = 1
        elif ball.centerx > 800 + field_x - ball_radius:
            dx = -1
        # collision top
        if ball.centery - field_y < ball_radius:
            dy = 1
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        # Ball out of screen
        if ball.y > 871:
            ball.x, ball.y = paddle.x + ball_rect, paddle.y - ball_rect
            ball_speed = 0
            life -= 1
            hits = 0
        elif ball.y < 50:
            ball.y = 75
            dy = 1
        # life parameters
        if life > 3:
            lifeText = f1.render(str(life-3)+"+", False, (150, 50, 50))
            dis.blit(lifeText, (15, 27))
        if life < 1:
            dis.blit(labelL, (display_w // 2 - 150, display_h // 2))
            if Score > int(HScore):
                config.set("Score", "highScore", str(Score))

                HScore = config["Score"]["highScore"]
                textHSN = f1.render(HScore, True, (130, 30, 50))
            ball_speed = 0
            paddle_speed = 0
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pressed(3)[0]:
                game = False
                menu = True
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > field_x:
            paddle.left -= paddle_speed
            if ball_speed == 0:
                ball.x -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < 800 + field_x:
            paddle.right += paddle_speed
            if ball_speed == 0:
                ball.x += paddle_speed
        # Ball on paddle
        if ball_speed == 0 and key[pygame.K_UP] and not Settin:
            ball_speed = 4
        # Score
        if hit:
            Score += Hits
            textSN = f1.render(str(Score), True, (0, 0, 0))
    elif InfGame:
        # Draw interface
        if life > 0:
            dis.blit(heart, (53, 27))
        if life > 1:
            dis.blit(heart, (90, 27))
        if life > 2:
            dis.blit(heart, (126, 27))

        dis.blit(ramka, (0, 0))
        dis.blit(textB, (193, 30))
        dis.blit(textS, (375, 30))
        dis.blit(textSN, (450, 30))
        dis.blit(textHS, (590, 30))
        dis.blit(textHSN, (692, 30))
        # switch levels
        if not block_list:
            ball.x, ball.y = paddle.x + paddle.width//2 - ball_rect//2, paddle.y - ball_rect
            ball_speed = 0
            amount, block_list, color_list = random_list()
        # Drawing world
        for i in range(amount):
            pygame.draw.rect(dis, pygame.Color(color_list[i]), block_list[i])
        pygame.draw.rect(dis, 'darkcyan', paddle)
        pygame.draw.circle(dis, pygame.Color('violet'), ball.center, ball_radius)
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # collision blocks
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            amount = amount - 1
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            Hits += 1
            Score += Hits
            textSN = f1.render(str(Score), True, (0, 0, 0))
            # bonuses
            b = rnd(1, 20)
            if b == 11 or b == 12:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(1)
            elif b == 14 or b == 15:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(2)
            elif b == 19:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(3)
            elif b == 17:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(4)
            elif b == 13 or b == 16:
                bonuses.append(pygame.Rect(hit_rect.x + 15, hit_rect.y, ball_rect, ball_rect))
                bonusesType.append(5)
            # special effect
            if ball_speed < 8:
                ball_speed += 0.5
            elif ball_speed > 8:
                ball_speed = 8
        # draw bonuses
        if bonuses:
            for bonus in bonuses:
                b = bonusesType[bonuses.index(bonus)]
                if b == 1:
                    dis.blit(b1, (bonus.x - 15, bonus.y - 12))
                elif b == 2:
                    dis.blit(b2, (bonus.x - 14, bonus.y - 8))
                elif b == 3:
                    pygame.draw.circle(dis, (30, 155, 255), bonus.center, bonus.height)
                    dis.blit(bonusH, (bonus.x - 2, bonus.y - 3))
                elif b == 4:
                    dis.blit(b4, (bonus.x, bonus.y))
                elif b == 5:
                    dis.blit(b5, (bonus.x, bonus.y))
                if not Settin:
                    bonus.y += 4
            hit_index = paddle.collidelist(bonuses)
            if hit_index != -1:
                hit_bonus = bonuses.pop(hit_index)
                hit_type = bonusesType.pop(hit_index)
                if hit_type == 1:
                    paddle.width += 50
                elif hit_type == 2:
                    if ball_speed > 2:
                        ball_speed /= 2
                elif hit_type == 3:
                    life += 1
                elif hit_type == 4:
                    paddle.width -= 50
                elif hit_type == 5:
                    if ball_speed < 8:
                        ball_speed += 2
        # collision left right
        if ball.centerx - field_x < ball_radius:
            dx = 1
        elif ball.centerx > 800 + field_x - ball_radius:
            dx = -1
        # collision top
        if ball.centery - field_y < ball_radius:
            dy = 1
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        # Ball out of screen
        if ball.y > 871:
            ball_speed = 0
            life -= 1
            hits = 0
            ball.topleft = (paddle.x + paddle.width // 2 - ball_rect // 2, display_h - paddle_h - 23 - ball_rect)
        elif ball.y < 50:
            clock.tick(fps)
            ball.y = 75
            dy = 1
        # life parameters
        if life > 3:
            lifeText = f1.render(str(life - 3) + "+", False, (150, 50, 50))
            dis.blit(lifeText, (15, 27))
        if life < 1:
            dis.blit(labelL, (display_w // 2 - 150, display_h // 2))
            if Score > int(HScore):
                config["Score"]["infHighScore"] = str(Score)
                HScore = config["Score"]["infHighScore"]
                textHSN = f1.render(HScore, True, (130, 30, 50))
            ball_speed = 0
            paddle_speed = 0
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.mouse.get_pressed(3)[0]:
                game = False
                menu = True
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > field_x:
            paddle.left -= paddle_speed
            if ball_speed == 0:
                ball.x -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < 800 + field_x:
            paddle.right += paddle_speed
            if ball_speed == 0:
                ball.x += paddle_speed
        # Ball on paddle
        if ball_speed == 0 and key[pygame.K_UP] and not Settin:
            ball_speed = 4
    # Setting menu
    if Settin:
        # Game pause
        ball_speed = 0
        paddle_speed = 0
        # Shadow
        s = pygame.Surface((display_w, display_h))
        s.fill((30, 30, 30))
        s.set_alpha(100)
        dis.blit(s, (0, 0))
        # menu window
        setMenu = pygame.Rect(225, 200, 375, 300)
        pygame.draw.rect(dis, (40, 85, 155), setMenu, 0, 25)
        dis.blit(labelS, (245, 215))
        dis.blit(labelA, (245, 290))

        # arrow buttons
        arrow1 = pygame.Rect(420, 291, 32, 24)
        arrow2 = pygame.Rect(550, 291, 32, 24)
        if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[0] > arrow1.topleft[0]:
            if pygame.mouse.get_pos()[1] > arrow1.topleft[1] and pygame.mouse.get_pos()[0] < arrow1.bottomright[0]:
                if pygame.mouse.get_pos()[1] < arrow1.bottomright[1]:
                    if BG == 0:
                        BG = 4
                    else:
                        BG -= 1
                alreadyPMouse = False

        if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[0] > arrow2.topleft[0]:
            if pygame.mouse.get_pos()[1] > arrow2.topleft[1] and pygame.mouse.get_pos()[0] < arrow2.bottomright[0]:
                if pygame.mouse.get_pos()[1] < arrow2.bottomright[1]:
                    if BG == 4:
                        BG = 0
                    else:
                        BG += 1
                alreadyPMouse = False

        d1 = (425, 302)
        pygame.draw.polygon(dis, textC, (d1, (435, 296), (435, 299), (445, 299), (445, 305), (435, 305), (435, 308)), 2)
        d2 = (575, 302)
        pygame.draw.polygon(dis, textC, (d2, (565, 296), (565, 299), (555, 299), (555, 305), (565, 305), (565, 308)), 2)
        dis.blit(LSpace, (471, 294))
        mainMenu = pygame.Rect(245, 390, 175, 25)
        returnB = pygame.Rect(245, 440, 130, 25)
        dis.blit(labelRet, (245, 440))
        dis.blit(labelMM, (245, 390))
        if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[0] > mainMenu.topleft[0]:
            if pygame.mouse.get_pos()[1] > mainMenu.topleft[1] and pygame.mouse.get_pos()[0] < mainMenu.bottomright[0]:
                if pygame.mouse.get_pos()[1] < mainMenu.bottomright[1]:
                    menu = True
                    Settin = False
                    game = False
                    InfGame = False
                    alreadyPMouse = False
        if alreadyPMouse and pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[0] > returnB.topleft[0]:
            if pygame.mouse.get_pos()[1] > returnB.topleft[1] and pygame.mouse.get_pos()[0] < returnB.bottomright[0]:
                if pygame.mouse.get_pos()[1] < returnB.bottomright[1]:
                    Settin = False
                    if game or InfGame:
                        paddle_speed = int(config["Paddle"]["paddle_speed"])
                        ball_speed = tempB
                    alreadyPMouse = False
    if not Settin:
        if alreadyPressed and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            Settin = True
            tempB = ball_speed
    # Update screen
    pygame.display.flip()
    clock.tick(fps)
