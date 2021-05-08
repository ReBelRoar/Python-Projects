import pygame
from pygame.locals import *
import sys
import random
import time


class Game:
    def __init__(self):
        self.width = 800
        self.height = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0'
        self.result = 'Time:0 Accuracy:0 Wpm:0'
        self.wpm = 0
        self.end = False
        self.word = ''

        pygame.init()
        self.open_img = pygame.image.load('open.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.width, self.height))
        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Typing Speed')

    def run(self):
        self.game_reset()
        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 700, 50))
            pygame.draw.rect(self.screen, (155, 204, 102), (50, 250, 700, 50), 2)
            self.draw_text(self.screen, self.input_text, 270, 25, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x >= 50 and x <= 650 and y >= 250 and y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    if x >= 310 and x <= 510 and y >=390 and self.end:
                        self.game_reset()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_result(self.screen)
                            print(self.result)
                            self.draw_text(self.screen, self.result, 350, 28, (255, 70, 70))
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()
            print('hi')

    def game_reset(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.word = self.get_sentence()
        if not self.word:
            self.game_reset()
        self.screen.blit(self.bg, (0, 0))
        msg = 'Check your Typing Speed '
        self.draw_text(self.screen, msg, 80, 60, (255, 104, 102))
        self.draw_text(self.screen, self.word, 200, 26, (240, 240, 240))
        pygame.display.update()

    def get_sentence(self):
        with open('Sentence.txt') as l:
            sentence = random.choice(l.readlines())
            return sentence

    def draw_text(self, screen, msg, y, size, color):
        font = pygame.font.Font(None, size)
        text = font.render(msg, 50, color)
        rect = text.get_rect(center=(self.width // 2, y))
        screen.blit(text, rect)
        pygame.display.update()

    def show_result(self, screen):
        if not self.end:
            self.total_time = time.time() - self.time_start
            # Accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100
            # Calculate WPM
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
            self.result = 'Time:'+str(round(self.total_time))+' secs Accuracy:'+str(round(self.accuracy))+'%'+' Wpm:'+str(round(self.wpm))
            # Draw icon image
            self.icon_img = pygame.image.load('icon.png')
            self.icon_img = pygame.transform.scale(self.icon_img, (150, 150))
            screen.blit(self.icon_img, (self.width/2-75, self.height-140))
            self.draw_text(screen, "Reset", self.height-70, 26, (100, 100, 100))
            print(self.result)
            pygame.display.update()

obj = Game()
obj.run()


