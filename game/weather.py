# Written by Kelvin Huang
import pygame 
import random
import math
from constants import *
from wparticles import Wparticles

class Weather:
    def __init__(self, type = "random", speed = 1, degree = 0, direction = "center", freq = .3):
        self.type = type
        self.freq = freq
        self.speed = speed
        self.degree = degree
        self.direction = direction
        if self.type == "snow" or self.type == "rain":
            self.particles = []
            if direction == "left":
                self.spawn = [-math.tan(degree * math.pi/180) * GAME_HEIGHT, 0]
            elif direction == "right":
                self.spawn = [GAME_WIDTH, GAME_WIDTH + math.tan(degree * math.pi/180) * GAME_HEIGHT]
            else:
                self.spawn = [0, GAME_WIDTH]

    def update(self):
        if self.type == "snow" or self.type == "rain":
            if self.direction == "left" and self.spawn[1] < GAME_WIDTH:
                self.spawn[1] += 1
            elif self.direction == "right" and self.spawn[0] > 0:
                self.spawn[0] -= 1
            
            # try to spawn new particles
            if random.random() < self.freq:
                start, end = self.spawn
                position = start + random.random() * (end - start)
                if self.direction == "left":
                    self.particles.append(Wparticles(self.type ,self.speed, self.degree, position))
                else:
                    self.particles.append(Wparticles(self.type ,self.speed, -self.degree, position))
        self.move()

    def move(self):
        if self.type == "snow" or self.type == "rain":
            for particle in self.particles:
                particle.move()
                

    def draw(self, game_surf):
        if self.type == "snow" or self.type == "rain":
            for particle in self.particles:
                particle.draw(game_surf)
    
    def stop(self):
        del self
        

# hurricane, tornado - spinning and moving
# landslide - moving

# large weather to clear the board
# hail
