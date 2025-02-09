import pygame
import configparser
pygame.init()

config = configparser.ConfigParser()  # создаём объект парсера
config.read("settings.ini")  # читаем конфиг

fps = 60
# display settings
display_w = 826
display_h = 675
# plying field
field_x = 13
field_y = 62
# paddle settings
paddle_w = 150
paddle_h = 19
paddle_speed = int(config["Paddle"]["paddle_speed"])

clock = pygame.time.Clock()


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


# ball settings
ball_radius = 15
ball_rect = int(ball_radius * 2 ** 0.5)


def game(dis, hits, life, amount, paddle, color_list, block_list, ball, ball_speed, dx, dy):
    hit = 0
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
        hits += 1
        hit = True
        # special effect
        ball_speed += 0.5
    # collision left right
    if ball.centerx - field_x < ball_radius or ball.centerx > 800 + field_x - ball_radius:
        dx = -dx
    # collision top
    if ball.centery - field_y < ball_radius:
        dy = -dy
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
        clock.tick(fps)
        ball.y = 100
        dy = -1
    return dis, hits, hit, life, amount, paddle, color_list, block_list, ball, ball_speed, dx, dy
