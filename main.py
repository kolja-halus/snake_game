import pygame
import random

# Ініціалізація (підготовка до роботи) всіх необхідних модулів
pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 240)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
SILVER = (240, 240, 240)

# Ширина та висота клієнтської області
SCREEN_WIDTH = 620
SCREEN_HEIGHT = 720

# Створюємо і зберігаємо в змінній 'screen' вікно гри з розмірами
# display_width x display_height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Встановлюємо заголовок вікна гри на "Snake game"
pygame.display.set_caption("Snake game")

# Шрифт для виведення прогресу гравця
score_font = pygame.font.SysFont('arial', 25)
# Шрифт для виведення вікна з повідомленням про програш
loss_font = pygame.font.SysFont('arial', 20, True)

# Встановлюємо FPS на 60 та створюємо годинник для керування оновленням гри
FPS = 60
clock = pygame.time.Clock()

# Розмір блоку
block_size = 20

# Поверхня для відображення прогресу
score_surface = pygame.Surface((SCREEN_WIDTH, 100))
score_surface.fill(BLACK)

# Поверхня для руху змійки
game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 100))
game_surface.fill(WHITE)

game_rect = game_surface.get_rect(topleft=(0, score_surface.get_height()))
game_surface_local_center = (SCREEN_WIDTH // 2, game_rect.centery - 100)

# Поверхня для сегмента змійки
segment = pygame.Surface((block_size, block_size))

# Прямокутник який відповідає розмірам сегмента
segment_rect = segment.get_rect(center=game_surface_local_center)
new_x, new_y = segment_rect.topleft

snake_list = [segment_rect]

# поверхня для їжі
food = pygame.Surface((block_size, block_size))
food.fill(RED)
food_rect = food.get_rect()


# Генерує випадкові координати для їжі
def randomize_food_position():
    food_rect.x = random.randrange(0, SCREEN_WIDTH, 20)
    food_rect.y = random.randrange(0, SCREEN_WIDTH, 20)


randomize_food_position()

# напрям руху
direction = ""

# частота зміни координат змійки
frame = 0
move = 5

points = 0


def get_score_surface():
    score_text_surface = score_font.render(
        f"Score: {points}", 1, WHITE
    )
    score_text_rect = score_text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, 100 // 2)
    )
    return score_text_surface, score_text_rect


score_surface.blit(*get_score_surface())


def show_game_over_screen():
    game_over_surface = pygame.Surface((400, 300))
    game_over_surface.fill(BLACK)
    game_over_rect = game_over_surface.get_rect(
        center=(SCREEN_WIDTH // 2, 260)
    )

    button_exit_surface = pygame.Surface((120, 40))
    button_exit_surface.fill(SILVER)
    button_exit_rect = button_exit_surface.get_rect(
        center=(200, 230)
    )

    button_restart_surface = pygame.Surface((120, 40))
    button_restart_surface.fill(SILVER)
    button_restart_rect = button_exit_surface.get_rect(
        center=(200, 140)
    )

    exit_font = pygame.font.SysFont("arial", 20, True)
    exit_mes_surf = exit_font.render("EXIT", 1, BLACK)
    exit_mes_rect = exit_mes_surf.get_rect(
        center=(60, 20)
    )
    button_exit_surface.blit(exit_mes_surf, exit_mes_rect)

    restart_font = pygame.font.SysFont("arial", 20, True)
    restart_mes_surf = restart_font.render("RESTART", 1, BLACK)
    restart_mes_rect = restart_mes_surf.get_rect(
        center=(60, 20)
    )
    button_restart_surface.blit(restart_mes_surf, restart_mes_rect)

    loss_message_surface = loss_font.render(
        "Ви програли :(", 1, WHITE
    )
    loss_message_rect = loss_message_surface.get_rect(
        center=(200, 60)
    )

    game_over_surface.blit(loss_message_surface, loss_message_rect)
    game_over_surface.blit(button_exit_surface, button_exit_rect)
    game_over_surface.blit(button_restart_surface, button_restart_rect)
    game_surface.blit(game_over_surface, game_over_rect)
    screen.blit(game_surface, (0, 100))

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                container_offset = (
                    game_rect.x + game_over_rect.x,
                    game_rect.y + game_over_rect.y
                )
                local_pos = (
                    click_pos[0] - container_offset[0],
                    click_pos[1] - container_offset[1]
                )
                if button_exit_rect.collidepoint(local_pos):
                    pygame.quit()
                elif button_restart_rect.collidepoint(local_pos):
                    restart_game()
                    game_over = False

        pygame.display.update()


def restart_game():
    global direction, segment_rect, snake_list, points, frame, new_x, new_y, \
        show_start_hints
    show_start_hints = True
    direction = ""
    segment_rect = segment.get_rect(center=(SCREEN_WIDTH // 2, 620 // 2))
    new_x, new_y = segment_rect.topleft
    snake_list = [segment_rect]
    points = 0
    frame = 0
    randomize_food_position()
    score_surface.fill(BLACK)
    score_surface.blit(*get_score_surface())
    while food_rect.topleft in snake_list:
        randomize_food_position()


hint_font = pygame.font.SysFont('arial', 25)

hint_message_surface = hint_font.render(
    "Use the W A S D keys to control the snake",
    1,
    BLACK
)
hint_message_surface.set_alpha(90)
hint_message_rect = hint_message_surface.get_rect(
    center=(
        game_surface_local_center[0],
        game_surface_local_center[1] - 200
    )
)


def create_direction_hint(dirrection):
    img = ""
    arrow_size = (0, 0)
    x, y = 0, 0
    letter = ""
    letter_x, letter_y = 0, 0
    if dirrection == "up":
        img = "img/arrow_up.png"
        arrow_size = (20, 60)
        x, y = game_surface_local_center[0], game_surface_local_center[1] - 60
        letter = "W"
        letter_x, letter_y = x, y - 50
    elif dirrection == "down":
        img = "img/arrow_down.png"
        arrow_size = (20, 60)
        x, y = game_surface_local_center[0], game_surface_local_center[1] + 60
        letter = "S"
        letter_x, letter_y = x, y + 50
    elif dirrection == "left":
        img = "img/arrow_left.png"
        arrow_size = (60, 20)
        x, y = game_surface_local_center[0] - 60, game_surface_local_center[1]
        letter = "A"
        letter_x, letter_y = x - 50, y
    elif dirrection == "right":
        img = "img/arrow_right.png"
        arrow_size = (60, 20)
        x, y = game_surface_local_center[0] + 60, game_surface_local_center[1]
        letter = "D"
        letter_x, letter_y = x + 50, y

    arrow = pygame.image.load(img).convert_alpha()
    arrow = pygame.transform.smoothscale(arrow, arrow_size)
    arrow.set_alpha(90)
    arrow_rect = arrow.get_rect(center=(x, y))

    hint_surf = hint_font.render(letter, 1, BLACK)
    hint_surf.set_alpha(90)
    hint_rect = hint_surf.get_rect(center=(letter_x, letter_y))

    return (arrow, arrow_rect), (hint_surf, hint_rect)


def start_hints():
    up = create_direction_hint("up")
    down = create_direction_hint("down")
    left = create_direction_hint("left")
    right = create_direction_hint("right")

    hints_pos = [
        hint_message_rect,
        up[0][1],
        down[0][1],
        left[0][1],
        right[0][1],
        up[1][1],
        down[1][1],
        left[1][1],
        right[1][1],
    ]

    flag = True
    while flag:
        for i in hints_pos:
            if food_rect.colliderect(i):
                randomize_food_position()
                break
        else:
            flag = False
            game_surface.blit(food, food_rect)

    game_surface.blit(*up[0])
    game_surface.blit(*down[0])
    game_surface.blit(*left[0])
    game_surface.blit(*right[0])

    game_surface.blit(*up[1])
    game_surface.blit(*down[1])
    game_surface.blit(*left[1])
    game_surface.blit(*right[1])

    game_surface.blit(hint_message_surface, hint_message_rect)


show_start_hints = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                show_start_hints = False
            if event.key == pygame.K_w:
                if direction != "down":
                    direction = "up"
            elif event.key == pygame.K_s:
                if direction != "up":
                    direction = "down"
            elif event.key == pygame.K_a:
                if direction != "right":
                    direction = "left"
            elif event.key == pygame.K_d:
                if direction != "left":
                    direction = "right"

    frame += 1

    if frame >= move:
        game_surface.fill(WHITE)

        if show_start_hints:
            start_hints()

        if direction == "up":
            new_y -= block_size
        elif direction == "down":
            new_y += block_size
        elif direction == "left":
            new_x -= block_size
        elif direction == "right":
            new_x += block_size

        new_x %= SCREEN_WIDTH
        new_y %= 620

        game_surface.blit(food, food_rect)

        for i in snake_list:
            if snake_list.index(i) == 0:
                segment.fill(GREEN)
                game_surface.blit(segment, i)
            else:
                segment.fill(BLACK)
                game_surface.blit(segment, i)

        segment_rect.x, segment_rect.y = new_x, new_y

        if segment_rect.colliderect(food_rect):
            points += 1
            score_surface.fill(BLACK)
            score_surface.blit(*get_score_surface())
            randomize_food_position()
            while food_rect.topleft in snake_list:
                randomize_food_position()
            snake_list.insert(0, (new_x, new_y))
        elif segment_rect.topleft in snake_list[1:]:
            show_game_over_screen()
        else:
            snake_list.insert(0, (new_x, new_y))
            snake_list.pop()

        frame = 0

    screen.blit(score_surface, (0, 0))
    screen.blit(game_surface, game_rect)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
