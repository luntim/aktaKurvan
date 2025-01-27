# TODO: lägg till 1 mer spelare och välja hur många spelare som ska spela och ge dem en annan färg.
# TODO: Launcha det online med multiplayer.
# TODO: Testa det med discord folk.

import pygame
import sys
import math
import random
import time

import pygame.draw_py

pygame.init()

screen = pygame.display.set_mode((1600, 900))

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

    def handle_input(self, keys, dt, index):
        #player 1
        if index == 0:
            if keys[pygame.K_a]:
                self.turn(-1, dt)
            if keys[pygame.K_d]:
                self.turn(1, dt)
        #player 2
        if index == 1:
            if keys[pygame.K_LEFT]:
                self.turn(-1, dt)
            if keys[pygame.K_RIGHT]:
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


def player_won_the_game(player):
    # display score and go to a winner screen or smth
    print(f"{player.color} won the game!!!")
    time.sleep(3)

def give_all_players_points(players):
    for player in players:
        if player.dead == False:
            player.score += 10

def is_game_over(players):
    for player in players:
        if player.score >= (len(players) * 10):
            player_won_the_game(player)
            return True
     
    return False


def display_score(players):
    increment = 5
    for index, player in enumerate(players):
        font = pygame.font.Font("freesansbold.ttf", 25)
        text = font.render(f"player{index + 1}:     {player.score}", True, player.color, "black")
        textRect = text.get_rect()
        textRect.topleft = (1205, 250 + increment)
        screen.blit(text, textRect)
        increment += 30

def reset_players(players):
    for player in players:
        player.x, player.y = player.spawn
        player.dead = False

    return players

def play_round(running, players):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    trails = []
    playersDead = 0

    screen.fill("black")
    display_score(players)
    border = [(400, 1), (1200, 1), (1200, 899), (400, 899)]
    pygame.draw.polygon(screen, "yellow", border, 3)

    while running:
        dt = clock.tick(144) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for index, player in enumerate(players):
            keys = pygame.key.get_pressed()
            player.handle_input(keys, dt, index)
            player.target_x = player.x + math.cos(player.direction) * 100 
            player.target_y = player.y + math.sin(player.direction) * 100 
        
            if player.jumping == False:
                player.jump()

            player.update(dt)

            circleRect = player.draw(screen, dt)

            if circleRect is not None:
                if player.check_border_collision(border) == True or player.check_trail_collision(trails) == True:
                    player.dead = True
                    playersDead += 1
                    give_all_players_points(players)
                    if len(players) - playersDead == 1:
                        running = False
                else:
                    trails.append(circleRect)

        pygame.display.flip()

    if is_game_over(players):
        return

    players = reset_players(players)
    time.sleep(3)
    play_round(running=True, players=players)


def main():
    players = []
    player1 = Player(x=580, y=230, direction=0.8, color="orange")
    player2 = Player(x=1020, y=670, direction=2.5, color="blue")
    players.extend([player1, player2])
    play_round(running=True, players=players)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

