#-*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600,500))
    pygame.display.set_caption("しりとりゲーム")
    button_rec = pygame.image.load("button_s.png").convert_alpha()
    r = 25
    font = pygame.font.Font(None, 55)
    font_pos = pygame.font.Font(None, 20)
    text = font.render("Let's begin Shiritori!", True, (0,0,0))

    draw_text_timer = [] # 一定時間で消えるテキスト描画用


    while(1):
        pygame.display.update()
        pygame.time.wait(30)
        screen.fill((160,80,100))
        screen.blit(button_rec,(150,100))
        
        # 一定時間で消えるテキスト描画/削除
        for [text,pos,timer] in draw_text_timer:
            screen.blit(text, pos)
            if timer > 0:
                i = draw_text_timer.index([text,pos,timer])
                draw_text_timer[i][2] -= 1
            else:
                draw_text_timer.remove([text,pos,timer])
        
        #常にマウスのx,y座標を表示
        x, y = pygame.mouse.get_pos()
        mouse_pos = font_pos.render("{0}, {1}".format(x, y), True, (0,0,0))
        screen.blit(mouse_pos,[0,0])


        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if (x-175)**2+(y-125)**2<r**2:
                    draw_text_timer.append([text,[20,100],int(1000/30.)])
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
