# Written by Kelvin Huang
import pygame 
import random
import math
from constants import *
from wparticles import Wparticles

class Weather:
    def __init__(self, type = "random", speed = 1, degree = 0, direction = "center", freq = .3, duration = 999, gradual = False):
        self.type = type
        self.freq = freq
        self.speed = speed
        self.degree = degree
        self.direction = direction

        self.timer = 0
        self.duration = duration * 60
        self.gradual = gradual

        if self.type == "snow" or self.type == "rain":
            self.particles = []
            if direction == "left":
                self.spawn = [-math.tan(degree * math.pi/180) * GAME_HEIGHT, 0]
            elif direction == "right":
                self.spawn = [GAME_WIDTH, GAME_WIDTH + math.tan(degree * math.pi/180) * GAME_HEIGHT]
            else:
                self.spawn = [0, GAME_WIDTH]

    def update(self):
        if self.timer < self.duration and (self.type == "snow" or self.type == "rain"):
            if self.direction == "left" and self.spawn[1] < GAME_WIDTH:
                self.spawn[1] += 1
            elif self.direction == "right" and self.spawn[0] > 0:
                self.spawn[0] -= 1
            
            # try to spawn new particles
            self.spawn_new_particles()
        self.move()
        self.timer += 1

        if self.timer > self.duration and len(self.particles) == 0:
            self.stop()

    def spawn_new_particles(self):
        if self.gradual == True:
            # equations that I made up to stimulate what will the probability be if it increase and decrease gradually
            # link to desmos page: https://www.desmos.com/calculator/mxu2syamzy for the two graths
            if self.timer <= self.duration/2:
                freq = (self.freq)*(math.atan(10/self.duration * (20*self.timer - self.duration))/math.pi + .5)
            else:
                freq = (self.freq)*(math.atan(10/self.duration * (20*self.timer) - 190)/math.pi - .5)
        else:
            freq = self.freq
        
        if random.random() < freq:
            start, end = self.spawn
            position = start + random.random() * (end - start)
            if self.direction == "left":
                self.particles.append(Wparticles(self.type ,self.speed, self.degree, position))
            else:
                self.particles.append(Wparticles(self.type ,self.speed, -self.degree, position))

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
