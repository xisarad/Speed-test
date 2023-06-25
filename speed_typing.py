import pygame
from pygame.locals import *
import sys
import time
import random
     
class Game:
   
    def __init__(self):
        self.w=750
        self.h=500
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Время:0 Точность:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (0,0,0)
        self.TEXT_C = (0,0,0)
        self.RESULT_C = (0,0,0)
        
       
        pygame.init()
        self.open_img = pygame.image.load('loading.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))


        self.bg = pygame.image.load('background.png')
        self.bg = pygame.transform.scale(self.bg, (self.w,self.h))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Тест скорости печати')
       
        
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()   
        
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if(not self.end):
            # Расчет времени
            self.total_time = time.time() - self.time_start
               
            # Расчет точности
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100
           
            # Расчет количества слов в минуту
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
                
            self.results = 'Время:'+str(round(self.total_time)) +" сек   Точность:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # Загрузка иконки
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150,150))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w/2-75,self.h-140))
            self.draw_text(screen," ", self.h - 70, 50, (255,0,0))
            
            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
    
       
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)
            # Обновление текста пользовательского ввода
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # Расположение окна ввода
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # Расположение кнопки сброса
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
         
                        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)  
                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
            
                
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)
        
        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Получаем случайное предложение 
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # Загрузка окна
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Тест скорости печати"
        self.draw_text(self.screen, msg,100, 90,self.HEAD_C)  
        # Отрисовка поля ввода
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)

        # Отрисовка строки предложения
        self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)
        
        pygame.display.update()



Game().run()

