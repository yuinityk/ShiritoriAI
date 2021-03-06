# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
import time
import Shiritori
import jtalk

# events
RECORD = 1
RECOGNIZED = 2

# states
TITLE = -1
LEVEL = -2
PLAY = -3
LOSE = -4
WIN = -5

myfont = "fonts/ipaexg.ttf"

class GUI:
    # constants for events
    RECORD = 1
    RECOGNIZED = 2

    # states
    TITLE = -1
    LEVEL = -2
    PLAY = -3
    LOSE = -4
    WIN = -5

    def __init__(self):
        pygame.init()
        self.screensize = (1530,835)
        self.screen = pygame.display.set_mode(self.screensize,FULLSCREEN,32)
        self.isFullScreen = True
        pygame.display.set_caption('WordChainer')

        self.title = Title()
        self.level = Level()
        self.play = Play(30)
        self.win = Win()
        self.lose = Lose()

        self.playerword = ''

        self.fps = 30 
        self.game_state = TITLE
        self.mainloop()

    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            self.update()
            self.render()
            pygame.display.update()
            self.check_event()


    def update(self):
        if self.game_state == TITLE:
            self.title.update()
        elif self.game_state == LEVEL:
            self.level.update()
        elif self.game_state == PLAY:
            self.play.update(self.playerword)
        elif self.game_state == LOSE:
            self.lose.update()
        elif self.game_state == WIN:
            self.win.update()


    def render(self):
        if self.game_state == TITLE:
            self.title.draw(self.screen)
        elif self.game_state == LEVEL:
            self.level.draw(self.screen)
        elif self.game_state == PLAY:
            self.play.draw(self.screen)
        elif self.game_state == LOSE:
            self.lose.draw(self.screen)
        elif self.game_state == WIN:
            self.win.draw(self.screen)

    
    def check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE: #go to title
                self.game_state = TITLE
                self.play.reset()
            if event.type == KEYDOWN and event.key == K_F11:
                if self.isFullScreen:
                    self.screen = pygame.display.set_mode(self.screensize,0,32)
                    self.isFullScreen = False
                else:
                    self.screen = pygame.display.set_mode(self.screensize,FULLSCREEN,32)
                    self.isFullScreen = True
            if event.type == KEYDOWN and event.key == K_TAB: #for checking GUI
                if self.game_state == TITLE:
                    self.game_state = LEVEL
                elif self.game_state == LEVEL:
                    self.game_state = PLAY
                elif self.game_state == PLAY:
                    self.game_state = LOSE
                elif self.game_state == LOSE:
                    self.game_state = WIN
                elif self.game_state == WIN:
                    self.game_state = TITLE

            if self.game_state == TITLE:
                self.title_handler(event)
            elif self.game_state == LEVEL:
                self.level_handler(event)
            elif self.game_state == PLAY:
                self.play_handler(event)
            elif self.game_state == LOSE:
                self.lose_handler(event)
            elif self.game_state == WIN:
                self.win_handler(event)


    def title_handler(self, event):
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.game_state = LEVEL


    def level_handler(self, event):
        if event.type == KEYDOWN and event.key == K_1:
            self.play.set_difficulty('easy')
            self.game_state = PLAY
        elif event.type == KEYDOWN and event.key == K_2:
            self.play.set_difficulty('normal')
            self.game_state = PLAY
        elif event.type == KEYDOWN and event.key == K_3:
            self.play.set_difficulty('hard')
            self.game_state = PLAY
        elif event.type == KEYDOWN and event.key == K_4:
            self.play.set_difficulty('reverse')
            self.game_state = PLAY


    def play_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if (x-325)**2+(y-425)**2<25**2:
                self.play.voice_record(self.screen)
                self.play.playerschead, self.play.playersctail = self.play.word_recognize()
                self.play.playersentence = self.play.get_sentence()
                if self.play.playerword != "":
                    self.playerword = self.play.playerword
                    print("player:"+self.play.playerword)
                    self.play.is_pcturn = True
                    self.play.is_noinputerror = False
                else:
                    self.play.is_pcturn = False
                r = self.play.respond()
                if r == 'win':
                    self.game_state = WIN
                if r == 'lose':
                    self.game_state = LOSE

    def lose_handler(self, event):
        pass

    def win_handler(self, event):
        pass


class Title:
    def __init__(self):
        """
        self.title_img = load_image("title.png")
        """
        self.title_img = pygame.font.Font(None, 50).render('WordChainer', True, (0,0,0))
        self.start_msg = pygame.font.Font(None, 30).render('PRESS SPACE TO START', True, (0,0,0))
    def update(self):
      pass
    def draw(self,screen):
        screen.fill((160,80,100))
        screen.blit(self.title_img, (20,60))
        screen.blit(self.start_msg, (300,100))


class Level:
    def __init__(self):
        self.easy = pygame.font.Font(myfont, 40).render('1:かんたーん', True, (0,0,0))
        self.normal = pygame.font.Font(myfont, 40).render('2:ふつう', True, (0,0,0))
        self.hard = pygame.font.Font(myfont, 40).render('3:すごーいむずかしい', True, (0,0,0))
        self.reverse = pygame.font.Font(myfont, 40).render('4:あたまとり', True, (0,0,0))
        self.instruction = pygame.font.Font(myfont, 40).render('ゲームの難易度を選んで数字を押してね!', True, (0,0,0))
    def update(self):
        pass
    def draw(self, screen):
        screen.fill((160,80,100))
        screen.blit(self.instruction, (100,100))
        screen.blit(self.easy, (100,200))
        screen.blit(self.normal, (100,300))
        screen.blit(self.hard, (100,400))
        screen.blit(self.reverse, (100,500))


class Play:
    def __init__(self,fps):
        self.fps = fps
        self.difficulty ='easy' 
        self.is_pcturn = False
        self.is_noinputerror = False
        self.counter = int(3*1000./fps)
        self.pcword = ''
        self.playerword = ''
        self.playerschead = ''
        self.playersctail = ''
        self.playersentence = ''
        self.pcword_former = ''
        self.pcsctail = ''
        self.wdic = {}
        self.notsflag = 0 #1のときしりをとっていない
        self.txtyou = pygame.font.Font(myfont, 40).render('あなた:', True, (0,50,0))
        self.txtpc = pygame.font.Font(None, 40).render('PC:', True, (0,0,50))
        self.rec = pygame.image.load("button_s.png").convert_alpha()
        self.recording = pygame.font.Font(myfont, 40).render('録音中...', True, (0,0,0))
        self.thinking = pygame.font.Font(myfont, 40).render('考え中...', True, (0,0,0))
    def update(self,playerword):
        self.playerword = playerword
    def draw(self, screen):
        screen.fill((160,80,70))
        if self.is_pcturn:
            screen.blit(self.txtyou,  (100,200))
            screen.blit(self.txtpc ,  (100,100))
            screen.blit(pygame.font.Font(myfont, 40).render(self.playersentence, True, (0,50,0)), (400,200))
            screen.blit(pygame.font.Font(myfont, 40).render(self.pcword_former, True, (0,0,50)),(400,100))
            screen.blit(self.thinking,(50,400))
            #print(self.playerword)
            #print(self.pcword)
            if self.counter>0:
                self.counter -= 1
            else:
                self.counter = int(3*1000./self.fps)
                self.is_pcturn = False

        else:
            screen.blit(self.txtyou, (100,100))
            screen.blit(self.txtpc , (100,200))
            screen.blit(pygame.font.Font(myfont, 40).render(self.playersentence, True, (0,50,0)), (400,100))
            screen.blit(pygame.font.Font(myfont, 40).render(self.pcword, True, (0,0,50)), (400,200))
            if self.notsflag == 1:
                if self.difficulty != 'reverse':
                    txt = 'しりをとろう'
                else:
                    txt = 'あたまをとろう'
                screen.blit(pygame.font.Font(myfont, 40).render(txt, True, (0,50,0)),(300,300))
            if self.is_noinputerror == True:
                screen.blit(pygame.font.Font(myfont, 40).render('なにか話して！', True, (0,50,0)),(300,300))
        screen.blit(self.rec, (300,400))
        
    def respond(self):
        if self.is_noinputerror == True:
            return ''
        self.pcword_former = self.pcword
        if self.playersctail in ['ん','ン']:
            return 'lose'
        #savedic = Shiritori.learn_word(self.playerword,{})
        #Shiritori.save_dic(savedic)
        #とりあえず辞書の更新はやめる
        if len(self.wdic[self.playersctail]) == 0:
            return 'win'
        #if self.pcword_former != '' and Shiritori.to_katakana(self.playerword[0]) != Shiritori.to_katakana(Shiritori.get_endletter(self.pcword_former)):
        if self.pcword_former != '' and self.playerschead != self.pcsctail:
            self.notsflag = 1
        else:
            re = Shiritori.return_word(self.playersctail,self.wdic)
            self.pcword = re
            if self.difficulty != 'reverse':
                self.pcsctail = Shiritori.get_endletter(self.pcword)
            else:
                self.pcsctail = self.pcword[0]
            self.wdic[self.playersctail].remove(re)
            self.notsflag = 0
            #jtalk.jtalk(re.encode('utf-8'))
            return ''
        
    def load_dic(self):
        pass

    def voice_record(self, screen):
        screen.blit(self.recording, (100,400))
        pygame.display.update()
        Shiritori.record()

    def get_sentence(self):
        sent = Shiritori.get_sentence()
        if sent != '_on':
            return sent
        else:
            return ""

    def word_recognize(self):
        #w = Shiritori.word_recognize(self.difficulty)
        head, tail = Shiritori.get_headntail(self.difficulty)
        if head != '_on' and tail != '_on':
            return head,tail
        else:
           self.is_noinputerror = True
           return '',''

    def set_difficulty(self,d):
        self.difficulty = d
        self.wdic = Shiritori.load_dic(d)
        #print(self.wdic.keys())

    def reset(self):
        self.is_pcturn = False
        self.pcword = ''
        self.playerword = ''
        self.pcword_former = ''
        self.wdic = {}


class Win:
    def __init__(self):
        self.txtwin = pygame.font.Font(myfont, 40).render('すごーい！あなたの勝ちだよ！', True, (0,50,0))
        self.txtreset = pygame.font.Font(myfont, 20).render('ESCキーでタイトルにもどるよ。', True, (0,0,0))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((200,50,50))
        screen.blit(self.txtwin, (40,40))
        screen.blit(self.txtreset, (400,400))


class Lose:
    def __init__(self):
        self.txtlose = pygame.font.Font(myfont, 40).render('ざんねん… ', True, (50,0,0))
        self.txtreset = pygame.font.Font(myfont, 20).render('ESCキーでタイトルにもどるよ。', True, (0,0,0))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((50,200,50))
        screen.blit(self.txtlose, (40,40))
        screen.blit(self.txtreset, (400,400))



if __name__ == '__main__':
    if Shiritori.get_usbmicindex() == -1:
        print('connect USB microphone.')
        sys.exit()
    GUI()
