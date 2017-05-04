from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pygame
from pygame.locals import *
import sys
import time
import Shiritori
import jtalk

class MenuWidget(QWidget):

    def __init__(self, parent=None):

        super(MenuWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        label = QLabel('難易度を選んでね!', self)
        font = QFont()
        font.setPointSize(10)
        label.setFont(font)

        self.button1 = QPushButton('easy')
        self.button2 = QPushButton('normal')
        self.button3 = QPushButton('hard')
        self.button1.setToolTip('かんたーん')
        self.button2.setToolTip('ふつう')
        self.button3.setToolTip('すごーいむずかしい')
        # button1.setIcon(QIcon("easy.png"))
        # button1.setIcon(QIcon("normal.png"))
        # button1.setIcon(QIcon("hard.png"))

        layout = QHBoxLayout()

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.setLayout(layout)



class RecordWidget(QWidget):

    def __init__(self, parent=None):
        super(RecordWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.player = QLineEdit()
        self.PC = QLineEdit()
        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("あなた"), 0, 0)
        lineLayout.addWidget(self.player, 0, 1)
        lineLayout.addWidget(QLabel("PC"), 1, 0)
        lineLayout.addWidget(self.PC, 1, 1)
        self.record_button = QPushButton('record')

        recordLayout = QVBoxLayout()
        recordLayout.addLayout(lineLayout)
        recordLayout.addWidget(self.record_button)

        self.setLayout(recordLayout)



class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initUI()
        self.play = Play(30)

    def initUI(self):
        self.setWindowTitle('WordChainer')
        self.menu = MenuWidget(self)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.menu)
        self.setLayout(self.vbox)
        self.menu.button1.clicked.connect(self.record_handler)
        self.menu.button2.clicked.connect(self.record_handler)
        self.menu.button3.clicked.connect(self.record_handler)
        self.setFixedSize(800,500)
        self.show()

    def record_handler(self):
        self.menu.close()
        sender = self.sender()
        self.play.set_difficulty(sender.text())
        self.record = RecordWidget(self)
        self.vbox.addWidget(self.record)
        self.setLayout(self.vbox)
        self.record.record_button.clicked.connect(self.play_handler)

    def play_handler(self):
        self.play.voice_record()
        self.play.playerschead, self.play.playersctail = self.play.word_recognize()
        self.play.playersentence = self.play.get_sentence()
        if self.play.playerword != "":
            self.record.player.setText(self.play.playerword)
            self.play.is_pcturn = True
            self.play.is_noinputerror = False
            r = self.play.respond()
            if self.notsflag == 1:
                QMessageBox.warning(self, 'おっと', 'しりをとろう！')
            elif r == 'win':
                QMessageBox.about(self, 'WIN', 'すごーい!あなたの勝ちだよ!')
                self.__init__()
            elif r == 'lose':
                QMessageBox.about(self, 'LOSE', 'ざんねん…')
                self.__init__()
            else:
                self.record.PC.setText(self.play.pcword)
        else:
            self.play.is_pcturn = False
            QMessageBox.warning(self, '聞き取れなかった…', 'なにか話して!')




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
        # self.rec = pygame.image.load("button_s.png").convert_alpha()
        # self.recording = pygame.font.Font(myfont, 40).render('録音中...', True, (0,0,0))
        # self.thinking = pygame.font.Font(myfont, 40).render('考え中...', True, (0,0,0))

    def update(self,playerword):
        self.playerword = playerword

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

    def voice_record(self):
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
