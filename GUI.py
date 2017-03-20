# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
import time
import Shiritori


RECORD = 1
RECOGNIZED = 2


class GUI:
    '''
    A class for simulating the game
    '''
    def __init__(self):
        self.fps = 30
        self.draw_text_timer = []
        self.continuous_event = []
        pygame.init()
        self.screen = pygame.display.set_mode((600,500))
        pygame.display.set_caption("game")
        self.components = {'button':{}, 'text':{}}
        self.components['button']['rec'] = {'obj': pygame.image.load("button_s.png").convert_alpha(), 'pos': (150,100), 'rad': 25, 'c_x': 175, 'c_y': 125}


    def draw_text(self, string, pos, second, color=(0,0,0), px=35):
        font = pygame.font.Font(None, px)
        text = font.render(string, True, color)
        self.components['text'][time.time()] = {'obj' : text, 'pos' : pos, 'timelimit' : int(second * 1000./self.fps)}
        self.draw_text_timer.append([text, pos, int(second * 1000./self.fps)])


    def voice_record(self):
        print("recording")
        Shiritori.record()
        self.continuous_event.append([RECORD,None])


    def word_recognize(self):
        #word = Shiritori.word_recognize()
        word = "Hello"
        self.continuous_event.append([RECOGNIZED,word])


    def run(self):
      while(1):
        pygame.display.update()
        pygame.time.wait(self.fps)
        self.screen.fill((160,80,100))
        
        # draw mouse position
        x, y = pygame.mouse.get_pos()
        mouse_pos = pygame.font.Font(None, 20).render("{0}, {1}".format(x, y), True, (0,0,0))
        self.components['text']['mouse_pos'] = {'obj' : mouse_pos, 'pos' : (0,0)}

        # draw
        for kind in list(self.components):
            for key in list(self.components[kind]):
                self.screen.blit(self.components[kind][key]['obj'],self.components[kind][key]['pos'])
                if 'timelimit' in self.components[kind][key]:
                    if self.components[kind][key]['timelimit'] > 0:
                        self.components[kind][key]['timelimit'] -= 1
                    else:
                        del self.components[kind][key]

        # deal continuous events
        for [event,args] in self.continuous_event:
            if event == RECORD:
                self.word_recognize()
                self.continuous_event.remove([event,args])
            
            if event == RECOGNIZED:
                self.draw_text(string=args,pos=[100,200],second=2)
                self.continuous_event.remove([event,args])


        #deal events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for key in self.components['button']:
                    if (x-self.components['button'][key]['c_x'])**2+(y-self.components['button'][key]['c_y'])**2<self.components['button'][key]['rad']**2: #izure hannteishiki ni suru
                        if key == 'rec':
                            font = pygame.font.Font(None, 55)
                            self.screen.blit(font.render("recording...", True, (0,0,0)),(20,100))
                            pygame.display.update()
                            self.voice_record()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()



if __name__ == '__main__':

    WordChainer = GUI() 
    WordChainer.run()
    """
    font = pygame.font.Font(None, 55)
    font_pos = pygame.font.Font(None, 20)
    text = font.render("Let's begin Shiritori!", True, (0,0,0))

    draw_text_timer = [] # 一定時間で消えるテキスト描画用
    continuous_event = [] #イベント終了キュー

    while(1):
        pygame.display.update()
        pygame.time.wait(fps)
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

        for [event,args] in continuous_event:
            if event == RECORD:
                word_recognize()
                continuous_event.remove([event,args])
            if event == RECOGNIZED:
                draw_text(args, [100,200], 2)
                continuous_event.remove([event,args])
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if (x-175)**2+(y-125)**2<r**2:
                    screen.blit(text,[20,100])
                    record()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                """
