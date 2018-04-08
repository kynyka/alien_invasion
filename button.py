# -*- coding:utf-8 -*-
import pygame.font


class Button(object):
    def __init__(self, ai_settings, screen, msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # 默认字体, 48号大小

        # 创建按钮的rect对象, 并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''将msg渲染为图像, 并使其在按钮上居中'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)  # True开启反锯齿;最后个是文字rect的背景色,若空着则pygame以透明背景方式渲染文本,若用self.button_color则是将文字背景弄成与按钮颜色一样,当然也可以弄得与按钮颜色不同,比如(0,100,0)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮, 再绘制文本
        self.screen.fill(self.button_color, self.rect)  # 绘制矩形
        # 传递图像及与该图像关联的rect对象
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Button1(Button):
    def __init__(self, ai_settings, screen, msg):
        super(Button1, self).__init__(ai_settings, screen, msg)
        self.rect.centery = self.screen_rect.centery + 80

    def prep_msg(self, msg):
        super(Button1, self).prep_msg(msg)
        self.msg_image_rect.centery = self.rect.centery + 80
