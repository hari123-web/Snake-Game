import pygame
from pygame.locals import *     #import some local variables(KEYDOWN, QUIT)
import time
import random

SIZE =40    #40*40 BLOCK

class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("apple.jpg").convert()
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3
    
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()
    
    
    def move(self):
        self.x=random.randint(0,24)*SIZE  #  25*40=1000 (in between 0 to 1000)
        self.y=random.randint(0,19)*SIZE  #  20*40=800  (in between 0 to 800)



class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen=parent_screen
        self.block=pygame.image.load("block.jpg").convert() #loading img
        self.x=[SIZE]*length  # x coordinate of block
        self.y=[SIZE]*length # y coordinate of block
        self.direction = 'down'   #initial direction
    def draw(self):
        self.parent_screen.fill((110,110,5))  # initializing to plan window again 
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))  #placing that block on surface at given location
        pygame.display.flip()  #to update changes in the window (flip or update function)
    
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=='left':
            self.x[0]-=SIZE
        if self.direction=='right':
            self.x[0]+=SIZE
        if self.direction=='up':
            self.y[0]-=SIZE
        if self.direction=='down':
            self.y[0]+=SIZE                          
        self.draw()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction='right'
        
    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'


class Game:
    def __init__(self):
        pygame.init() #inialize whole module

        pygame.mixer.init()
        self.surface=pygame.display.set_mode((1000,800)) #initializing game window in pixels
        self.surface.fill((110,110,5)) #setting game window color using RGB
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2): #snake colliding with apple
        if x1>=x2 and x1<x2 + SIZE:
            if y1>=y2 and y1<y2 +SIZE:
                return True
        return False    

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound=pygame.mixer.Sound("ding-sound-effect_2.mp3")
            pygame.mixer.Sound.play(sound)
            
            self.snake.increase_length()
            self.apple.move()
        
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound=pygame.mixer.Sound("CymbalCrash CRT043807.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game over"   #throwing exception 
    

    def show_game_over(self):
        self.surface.fill((110,110,5))
        font = pygame.font.SysFont('arial',30)
        line1=font.render(f"Game is over ! Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(300,300))
        line2=font.render("To play press enter. To exit press Escape",True,(255,255,255))
        self.surface.blit(line2,(300,350))
        pygame.display.flip()

    def reset(self):
        self.snake=Snake(self.surface,1)
        self.apple=Apple(self.surface)

    def display_score(self):
        font =pygame.font.SysFont('arial',38)
        score = font.render(f"Score:{self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(800,10))
    
    


    def run(self):
        running =True
        pause=False

        while running:      #to show gaming window until user quit using cancel button
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  #exit when esc key is pressed
                        running=False
                    if event.key==K_RETURN:     #keyboard Enter key to play again
                        pause=False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()   #functions in class Snake
                        if event.key == K_DOWN:
                            self.snake.move_down() 
                        if  event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

            

                elif event.type == QUIT:     #exit when cancel button is pressed
                    running=False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
            time.sleep(0.3)  #in every 0.3 sec block move        



if __name__=="__main__":
    game = Game()
    game.run()
    
    