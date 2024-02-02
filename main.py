import sys

import pygame

from database import get_best, insert_result
from logics import *
import json
import os

GAMERS_DB = get_best()


def init_cons():
    global score,mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    score = 0
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)

mas= None
score=None
USERNAME = None
path = os.getcwd()
if 'data.txt' in os.listdir():
    with open('data.txt') as file:
        data=json.load(file)
        mas = data['mas']
        score = data['score']
        USERNAME = data['user']
    full_path= os.path.join(path,'data.txt')
    os.remove(full_path)
else:
    init_cons()

def draw_top_gamers():
    font_top = pygame.font.SysFont('simsun', 30)
    font_gamer = pygame.font.SysFont('simsun', 24)
    text_head = font_top.render("Best tries:", True, COLOR_TEXT)
    screen.blit(text_head, (250, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f"{index + 1}.{name}-{score}"
        text_gamer = font_gamer.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer, (250, 30 + 28 * index))
        print(index, name, score)


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont("stxingkai", 70)
    font_score = pygame.font.SysFont('simsun', 48)
    text_score = font_score.render("Score:", True, COLOR_TEXT)
    font_delta = pygame.font.SysFont('simsun', 16)
    text_score_value = font_score.render(f"{score}", True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (175, 35))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, COLOR_TEXT)
        screen.blit(text_delta, (180, 85))
    pretty_print(mas)
    draw_top_gamers()

    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCKS + (column + 1) * MARGIN
            h = row * SIZE_BLOCKS + (row + 1) * MARGIN + SIZE_BLOCKS
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCKS, SIZE_BLOCKS))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCKS - font_w) / 2
                text_y = h + (SIZE_BLOCKS - font_h) / 2
                screen.blit(text, (text_x, text_y))




COLORS = {
    0: (130, 130, 130),
    2: (244, 164, 96),
    4: (210, 105, 30),
    8: (255, 69, 0),
    16: (255, 127, 80),
    32: (255, 99, 71),
    64: (250, 128, 114),
    128: (220, 20, 60),
    256: (255, 0, 0),
    512: (178, 34, 34),
    1024: (139, 0, 0),
    2048: (128, 0, 0),
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
COLOR_TEXT = (255, 128, 0)
BLOCKS = 4
SIZE_BLOCKS = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCKS + (BLOCKS + 1) * MARGIN
HIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


pretty_print(mas)

# for gamer in get_best():
#    print(gamer)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("2048")


def draw_intro():
    img2048 = pygame.image.load("2048.jfif")
    font = pygame.font.SysFont("stxingkai", 76)
    text_welcome = font.render("Welcome", True, WHITE)
    name = 'Nickname'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Nickname':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break

        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (240, 60))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def save_game():
    data = {
        'user': USERNAME,
        'score':score,
        'mas':mas
    }
    with open('data.txt','w') as outfile:
        json.dump(data, outfile)


def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move  = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                if is_zero_in_mas(mas) and is_mas_move:
                    score += delta
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    is_mas_move= False
                    print(f'Ми заповнили елемент під номером', (random_num))
                draw_interface(score, delta)

                pygame.display.update()
        print(USERNAME)

def draw_game_over():
    global USERNAME, mas, score, GAMERS_DB
    img2048 = pygame.image.load("2048.jfif")
    font = pygame.font.SysFont("stxingkai", 64)
    text_game_over = font.render("Game over", True, WHITE)
    text_score = font.render(f"Ви набрали: {score}", True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = "Рекорд побито"
    else:
        text = f"Рекорд: {best_score}"
    text_record = font.render(text, True, WHITE)
    insert_result(USERNAME, score)
    GAMERS_DB = get_best()
    make_disicion = False
    while not make_disicion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_disicion = True
                    init_cons()
                    screen.fill(BLACK)
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_disicion = True
                    init_cons()
                    screen.fill(BLACK)
        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 80))
        screen.blit(text_score, (30, 250))
        screen.blit(text_record, (30, 300))
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        pygame.display.update()
    screen.fill(BLACK)


while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
