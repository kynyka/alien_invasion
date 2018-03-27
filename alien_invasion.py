# -*- coding:utf-8 -*-
import sys
import pygame
from settings import Settings
from ship import Ship

def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    ai_settings = Settings()  # 创建实例并存储于变量
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invation')

    # 创建一艘飞船
    ship = Ship(screen)  # 位置参数

    # 开始游戏主循环
    while 1:
        # 监视鼠标和事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # 每次循环是都重绘屏幕
        screen.fill(ai_settings.bg_color)
        ship.blitme()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


run_game()
