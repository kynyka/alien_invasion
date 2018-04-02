# -*- coding:utf-8 -*-
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    ai_settings = Settings()  # 创建实例并存储于变量
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invation')

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)  # 位置参数
    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个外星人
    alien = Alien(ai_settings, screen)

    # 开始游戏主循环
    while 1:
        gf.check_events(ai_settings, screen, ship, bullets)  # 同时移除本主程序sys模块
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, alien, bullets)

run_game()
