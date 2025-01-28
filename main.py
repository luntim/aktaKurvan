# TODO: lägg till 2 mer spelare och välja hur många spelare som ska spela och ge dem en annan färg.
# TODO: Launcha det online med multiplayer.
# TODO: Testa det med discord folk.

import pygame
import sys
import math
import random
import time

from network import Network

import pygame.draw_py

pygame.init()

screen = pygame.display.set_mode((1600, 900))
border = [(400, 1), (1200, 1), (1200, 899), (400, 899)]
score_to_win = 10

class Player:
    def __init__ (self, x, y, direction, color):
        self.spawn = (x, y)
        self.x = x
        self.y = y
        self.speed = 55
        self.direction = direction # in radians
        self.turn_speed = 3
        self.target_x = x
        self.target_y = y
        self.sum_of_dt = 0
        self.jumping = False
        self.dead = False
        self.score = 0
        self.color = color

    def update(self, dt):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy **2) ** 0.5 # Euclidean distance

        if distance > 0:
            self.x += (dx / distance) * self.speed * dt 
            self.y += (dy / distance) * self.speed * dt 

    def draw(self, screen, dt):
        if self.jumping and self.sum_of_dt < 0.25:
            self.sum_of_dt += dt
            pygame.draw.circle(screen, "black", (self.x, self.y), 3)
            return None

        elif self.jumping and self.sum_of_dt >= 0.25: 
            self.sum_of_dt = 0
            self.jumping = False
            circleRect = pygame.draw.circle(screen, self.color, (self.x, self.y), 3)
            return circleRect

        else:
            circleRect = pygame.draw.circle(screen, self.color, (self.x, self.y), 3)
            return circleRect

    def turn(self, direction, dt):
        self.direction += direction * self.turn_speed * dt
        self.target_x = self.x + math.cos(self.direction)
        self.target_y = self.y + math.sin(self.direction)

    def handle_input(self, keys, dt):
        #player 1
        if self.color == "orange":
            if keys[pygame.K_1]:
                self.turn(-1, dt)
            if keys[pygame.K_2]:
                self.turn(1, dt)
        #player 2
        if self.color == "blue":
            if keys[pygame.K_LEFT]:
                self.turn(-1, dt)
            if keys[pygame.K_RIGHT]:
                self.turn(1, dt)
                #player 2
        if self.color == "green":
            if keys[pygame.K_COMMA]:
                self.turn(-1, dt)
            if keys[pygame.K_PERIOD]:
                self.turn(1, dt)
                #player 2
        if self.color == "red":
            if keys[pygame.K_z]:
                self.turn(-1, dt)
            if keys[pygame.K_x]:
                self.turn(1, dt)


    def jump(self):
        if random.randint(1, 500) == 1:
            self.jumping = True


    def check_border_collision(self, border):
        # if player is within the border upper line horizontally
        if border[0][1] >= self.y >= border[0][1] - 0.5:  # 0.5 is the width of the line
            if border[0][0] <= self.x <= border[1][0]:
                return True
        # if player is within border lower line horizontally
        if border[2][1] >= self.y >= border[2][1] - 0.5:
            if border[0][0] <= self.x <= border[1][0]:
                return True
        # if player is on left border vertically
        if border[0][0] <= self.x <= border[0][0] + 0.5:
            if border[2][1] >= self.y >= border[0][1]:
                return True
        # if player is on right border vertically
        if border[1][0] <= self.x <= border[1][0] + 0.5:
            if border[2][1] >= self.y >= border[0][1]:
                return True
    

    def check_trail_collision(self, trails):
        # so it wont collide with itself instantly, idk how many it puts out per second but its alot of boxes xd
        for rect in trails[:-50]:
            if rect.collidepoint((self.x, self.y)):
                return True


    def move(self, dt, trails):
            keys = pygame.key.get_pressed()
            self.handle_input(keys, dt)
            self.target_x = self.x + math.cos(self.direction) * 100 
            self.target_y = self.y + math.sin(self.direction) * 100 
        
            if self.jumping == False:
                self.jump()

            self.update(dt)

            circleRect = self.draw(screen, dt)

            if circleRect is not None:
                if self.check_border_collision(border) == True or self.check_trail_collision(trails) == True:
                    self.dead = True
                else:
                    return circleRect



def player_won_the_game(player):
    # display score and go to a winner screen or smth
    print(f"{player.color} won the game!!!")
    time.sleep(3)

def give_all_players_alive_points(players):
    for player in players:
        if player.dead == False:
            player.score += 1

def is_game_over(players):
    for player in players:
        if player.score >= score_to_win:
            player_won_the_game(player)
            pygame.quit()
            sys.exit()


def draw_board(players):
    screen.fill("black")
    pygame.draw.polygon(screen, "yellow", border, 3)

    increment = 5
    for player in players:
        font = pygame.font.Font("freesansbold.ttf", 25)
        text = font.render(f"{player.color}:     {player.score}", True, player.color, "black")
        textRect = text.get_rect()
        textRect.topleft = (1205, 250 + increment)
        screen.blit(text, textRect)
        increment += 30
        
    pygame.display.flip()

def reset_players(players):
    for player in players:
        player.x, player.y = player.spawn
        player.dead = False
        player.speed = 55

    return players


def read_pos(str):
    str = str.split(",")
    return float(str[0]), float(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])




def main():
    #n = Network()
    #startpos = read_pos(n.getPos())
    players = []
    player1 = Player(x=580, y=230, direction=0.8, color="orange")
    player2 = Player(x=1020, y=670, direction=-2.37, color="blue")
    player3 = Player(x=1020, y=230, direction=2.37, color="green")
    player4 = Player(x=580, y=670, direction=-0.8, color="red")
    players.extend([player1, player2, player3, player4])

    gameLoop = True
    while gameLoop:

        pygame.mouse.set_visible(True)
        clock = pygame.time.Clock()

        run = True
        trails = []
        playersDead = 0

        draw_board(players)
        is_game_over(players)
    
        while run:
            dt = clock.tick(60) / 1000
            """  player2Pos = read_pos(n.send(make_pos((player1.x, player1.y))))
            player2.x = player2Pos[0]
            player2.y = player2Pos[1]
            print(f"Received position: {player2Pos}") """
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameLoop = False

            for player in players:
                circleRect = player.move(dt, trails)
                if circleRect is not None:
                    trails.append(circleRect)

                if player.dead == True and player.speed is not 0:
                    playersDead += 1
                    print("playersDead: ", playersDead)
                    player.speed = 0
                    give_all_players_alive_points(players) 
                    if len(players) - playersDead == 1:
                        players = reset_players(players)
                        time.sleep(3)
                        run = False
                        break

            pygame.display.flip()

if __name__ == "__main__":
    main()

