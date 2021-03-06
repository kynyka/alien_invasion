# -*- coding:utf-8 -*-
import sys
import os
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True  # 向右移动飞船
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True  # 向左移
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹, 并将其加入到编组bullets[即Group()实例]中; 若还未达限制, 则发射一颗子弹
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, about_button, ship, aliens, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_about_button(ai_settings, screen, stats, about_button, mouse_x, mouse_y)


def check_about_button(ai_settings, screen, stats, about_button, mouse_x, mouse_y):
    '''点击About时显示说明文字'''
    button_clicked = about_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        text_color = (255, 0, 0)
        font = pygame.font.SysFont('kaiti', 30)  # 查看可用字体pygame.font.get_fonts() 或用自定义字体pygame.font.Font("my_font.ttf", 20)
        about = u'开始游戏：点击Play'  # 不支持任何形式的多行
        about1 = u'退出游戏：按q键或点击右上角×号'
        about2 = u'发射子弹：按空格键'
        about3 = u'向左移动：按←方向键'
        about4 = u'向右移动：按→方向键'

        about_image = font.render(about, True, text_color, ai_settings.bg_color)
        about_image_rect = about_image.get_rect()
        about_image_rect.left = 10
        about_image_rect.top = about_button.rect.bottom  # 也可进行xx_image_rect.center=(400,300)赋值操作
        screen.blit(about_image, about_image_rect)  # 也可替换xx_image_rect为某坐标,如(500,400)

        about1_image = font.render(about1, True, text_color, ai_settings.bg_color)
        about2_image = font.render(about2, True, text_color, ai_settings.bg_color)
        about3_image = font.render(about3, True, text_color, ai_settings.bg_color)
        about4_image = font.render(about4, True, text_color, ai_settings.bg_color)

        about1_image_rect = about1_image.get_rect()
        about2_image_rect = about2_image.get_rect()
        about3_image_rect = about3_image.get_rect()
        about4_image_rect = about4_image.get_rect()

        about1_image_rect.left = 10
        about2_image_rect.left = 10
        about3_image_rect.left = 10
        about4_image_rect.left = 10

        about1_image_rect.top = about_button.rect.bottom + 40
        about2_image_rect.top = about_button.rect.bottom + 80
        about3_image_rect.top = about_button.rect.bottom + 120
        about4_image_rect.top = about_button.rect.bottom + 160

        screen.blit(about1_image, about1_image_rect)
        screen.blit(about2_image, about2_image_rect)
        screen.blit(about3_image, about3_image_rect)
        screen.blit(about4_image, about4_image_rect)

        for t in xrange(5):
            pygame.display.flip()
            sleep(1)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''在玩家单击Play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:  # 修复游戏进行时误点按钮区域而导致重置游戏的问题
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人, 并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, about_button):
    '''更新屏幕上的图像, 并切换到新屏幕'''
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)  # 写本行同时删除先前单个外星人的绘制

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态, 就绘制Play按钮; 为使其位于其他所有屏幕元素上层,故在绘制其他所有游戏元素后再绘制这个按钮,然后切换到新屏幕
    if not stats.game_active:
        play_button.draw_button()
        about_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bullet_sound):
    '''更新子弹的位置, 并删除已消失的子弹'''
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹(在屏幕外不显示,但依然消耗内存)
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bullet_sound)


def check_high_score(stats, sb):
    '''检查是否诞生了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bullet_sound):
    '''响应子弹和外星人的碰撞'''
    # 删除相撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # sprite.groupcollide()返回一个字典,键为子弹,相应的值是被击中的外星人;倆实参True起刪除發生碰撞的子彈和外星人用

    if collisions:
        for aliens in collisions.values():
            bullet_sound.play()
            stats.score += ai_settings.alien_points * len(aliens)  # 每个值都是一个列表,包含被同一颗子弹击中的所有外星人
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人; 如果外星人都被消灭,就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width  # 用刚创建的外星人来获取外星人宽度
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # 上边距; 相邻外星人行的y坐标相差外星人高度的两倍; 行号
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    # 创建一个外星人, 并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)  # 此alien非aliens的成员
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)  # 删掉了引用alien_width的代码行, 因为现在这实在create_alien()中处理的
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in xrange(number_rows):
        for alien_number in xrange(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''将整群外星人下移, 并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 紧随命数-1, 更新剩余命数记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人, 并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 发出相撞声
        ship_sound.play()

        # 暂停
        sleep(0.5)
    else:
        ship_sound.play()
        stats.game_active = False
        pygame.mouse.set_visible(True)  # 没命结束游戏后重新显示光标
        compare_and_save_high_score(stats)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound)
            break


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound):
    '''检查是否有外星人位于屏幕边缘, 并更新整群外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):  #spritecollideany()接受俩实参:一sprite,一group. 它检查编组是否有成员与精灵发生碰撞, 并在找到与精灵发生了碰撞的成员后就停止遍历编组; 若没发生碰撞,则返回None; 若找到, 则返回这个编组成员
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound)  # 外星人与船相撞时损失一艘飞船

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, ship_sound)  # 外星人到底部时也损失一艘飞船


def get_local_score():
    '''获取本地存储的历史最高分'''
    if os.path.exists('score/highscore.txt'):
        with open('score/highscore.txt','rb') as f:
            local_high_score = int(f.read())
    else:
        local_high_score = 0
    return local_high_score


def compare_and_save_high_score(stats):
    '''比较本次分数与历史最高分, 并更新分数文件'''
    '''由于死前一直在check_high_score, 所以直接拿stats.high_score即可'''
    if int(round(stats.high_score, -1)) > get_local_score():
        with open('score/highscore.txt', 'wb') as f:
            f.write(str(stats.high_score))


def set_and_show_high_score(stats):
    if int(stats.high_score) < get_local_score():
        stats.high_score = get_local_score()
