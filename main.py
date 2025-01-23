# TODO: Lägg till hopp som i achtung die kurve
# TODO: Fixa collision på färgerna som skrivs ut (lagra koordinaterna och storleken som man ritade)
# TODO: lägg till 7 mer spelare och välja hur många spelare som ska spela och ge dem en annan färg.
# TODO: Lägg till poäng för 1a, 2a etc. Efter en viss mängd avslutas spelet. (man kanske kan få skriva in mängden själv?)
# TODO: Launcha det online med multiplayer.
# TODO: Testa det med discord folk.

import pygame
import sys
import math
import random

import pygame.draw_py

pygame.init()

screen = pygame.display.set_mode((1600, 900))

class Player:
    def __init__ (self, x, y, speed, turn_speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 0 # in radians
        self.turn_speed = turn_speed
        self.target_x = x
        self.target_y = y

    def update(self, dt):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy **2) ** 0.5 # Euclidean distance

        if distance > 0:
            self.x += (dx / distance) * self.speed * dt 
            self.y += (dy / distance) * self.speed * dt 

    def draw(self, screen):
        pygame.draw.circle(screen, "red", (int(self.x), int(self.y)), 3)

    def turn(self, direction, dt):
        self.direction += direction * self.turn_speed * dt
        self.target_x = self.x + math.cos(self.direction)
        self.target_y = self.y + math.sin(self.direction)

    def handle_input(self, keys, dt): 
        if keys[pygame.K_a]:
            self.turn(-1, dt)
        if keys[pygame.K_d]:
            self.turn(1, dt)

    def jump(self):
        jump = random.randint(1, 25)
        print(jump)
        if jump == 1:
            pygame.draw.circle(screen, "grey", (int(self.x), int(self.y)), 3)
            return True
        return False
    
def main():
    clock = pygame.time.Clock()
    player = Player(x=400, y=300, speed=55, turn_speed=3)
    screen.fill("grey")

    running = True
    while running:
        dt = clock.tick(240) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt)
        player.target_x = player.x + math.cos(player.direction) * 100 
        player.target_y = player.y + math.sin(player.direction) * 100 

        player.jump()
        player.update(dt)
        player.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

