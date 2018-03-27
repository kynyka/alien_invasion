# -*- coding:utf-8 -*-
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    ai_settings = Settings()  # 创建实例并存储于变量
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invation')

    # 创建一艘飞船
    ship = Ship(screen)  # 位置参数

    # 开始游戏主循环
    while 1:
        gf.check_events()  # 同时移除本主程序sys模块
        gf.update_screen(ai_settings, screen, ship)

run_game()
