import pygame
import random
import sys

speed = 2

level = 0
x = 0
y = 1

global head_pos, snake_body, food_pos, food_spawn, score, direction, death

# windows sizes

frame_size_x = 1380
frame_size_y = 840

pygame.init()

# initialized game window

pygame.display.set_caption("Zmeika")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
fiol = pygame.Color(99, 0, 205)

fps_controller = pygame.time.Clock()
# One zmeika square size
cell_size = 60


def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction,  speed, death
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // cell_size)) * cell_size,
                random.randrange(1, (frame_size_y // cell_size)) * cell_size]
    food_spawn = True
    score = 0
    speed = 2

    death = False


init_vars()


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)


# game loop
def game():
    global food_spawn, food_pos, score,  radius,   speed, level, center_food_x, center_food_y
    while True:
        check_events()
        check_death()
        level_up()

        # eating apple
        snake_body.insert(0, list(head_pos))
        if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # spawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // cell_size)) * cell_size,
                        random.randrange(1, (frame_size_y // cell_size)) * cell_size]

        food_spawn = True

        if death == False:
            game_window.fill(black)
            head = 1
            for pos in snake_body:
                center_x = pos[0] + 2 + (cell_size - 2) // 2
                center_y = pos[1] + 2 + (cell_size - 2) // 2
                radius = (cell_size - 2) // 2
                center_food_x = food_pos[0] + 2 + (cell_size - 2) // 2
                center_food_y = food_pos[1] + 2 + (cell_size - 2) // 2
                # pygame.draw.rect(game_window, green, pygame.Rect(
                #    pos[0] + 2, pos[1] + 2,
                #    square_size - 2, square_size - 2))
                if head == 1:
                    pygame.draw.circle(game_window, green, (center_x, center_y), radius, radius)
                    head = 0
                    continue
                pygame.draw.circle(game_window, blue, (center_x, center_y), radius, radius)

            pygame.draw.circle(game_window, red, (center_food_x, center_food_y), radius, radius)

        show_score(1, white, 'consolas', 20)
        print_text()
        pygame.display.update()
        fps_controller.tick(speed)


def check_events():
    global direction, event, death
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w")
                    and direction != "DOWN"):
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s")
                  and direction != "UP"):
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a")
                  and direction != "RIGHT"):
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d")
                  and direction != "LEFT"):
                direction = "RIGHT"
            elif (event.key == pygame.K_y):
                death = False
                init_vars()
            elif (event.key == pygame.K_n):
                pygame.quit()
    if direction == "UP":
        head_pos[y] -= cell_size
    elif direction == "DOWN":
        head_pos[y] += cell_size
    elif direction == "LEFT":
        head_pos[x] -= cell_size
    else:
        head_pos[x] += cell_size

def check_death():
    global death
    if head_pos[0] < 0:
        death = True

    elif head_pos[0] > frame_size_x - cell_size:
        death = True

    elif head_pos[1] < 0:
        death = True

    elif head_pos[1] > frame_size_y - cell_size:
        death = True

    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            death = True


def print_text():
  global death
  if death:
      font1 = pygame.font.SysFont('arial', 42)
      surface = font1.render('Game Over, Press Y to continue or press N to quit', True, blue)
      surface1 = font1.render('Your Level is ' +str(level),True, red)
      surface2 = font1.render('Your Score is ' +str(score),True, fiol)
      textrect = surface.get_rect()
      textrect.center = (690, 210)
      textrect1 = surface1.get_rect()
      textrect1.center = (690, 300)
      textrect2 = surface2.get_rect()
      textrect2.center = (690, 400)
      game_window.blit(surface, textrect)
      game_window.blit(surface1, textrect1)
      game_window.blit(surface2,textrect2)

def level_up():
    global score, level, speed
    if score == 5:
        speed = 5
        level = 1

    if score == 10:
        speed = 7
        level = 2

    if score == 15:
        speed = 9
        level = 3

    if score == 20:
        speed = 11
        level = 4


if __name__ == '__main__':
    game()
