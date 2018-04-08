# -*- coding:utf-8 -*-
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button, Button1
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    pygame.mixer.init()  # 初始化音效模块
    ai_settings = Settings()  # 创建实例并存储于变量
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 对象screen是一个surface,在Pygame中,surface是屏幕的一部分,用于显示游戏元素.本游戏中,每个元素都是一个surface.现在的它代表整个游戏窗口.
    pygame.display.set_caption('Alien Invation')

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    about_button = Button1(ai_settings, screen, 'About')

    # 创建一个用于存储游戏统计信息的实例, 并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、一个用于存储子弹的编组、一个外星人编组
    ship = Ship(ai_settings, screen)  # 位置参数
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)  # 写本行同时删除先前import的Alien类及创建单个外星人的实例; 实质上类与创造单个的实例都移入了game_functions

    # 实例化音效
    bullet_sound = pygame.mixer.Sound("sound/ba_hit.wav")
    ship_sound = pygame.mixer.Sound('sound/as_hit.wav')

    # 开始游戏主循环
    while 1:
        gf.set_and_show_high_score(stats)  # 每次死了后都比较一遍当前最高分与历史最高分,挑高的显示
        gf.check_events(ai_settings, screen, stats, sb, play_button, about_button, ship, aliens, bullets)  # 同时移除本主程序sys模块

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bullet_sound)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound)  # 子弹再更新外星人, 因稍后要检查是否有子弹撞到了外星人

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, about_button)

run_game()
