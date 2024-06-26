# Written by Kelvin Huang, April 21, 2024
# Lay out foundation of this class and created weather for rain and snow with features to change
# speed of particle, degree of particle, direction in which particle is coming from, frequency of particle, duration of weather event, and an option for gradual increase and decrease in percentage of particle spawning

# Modified by Nicholas Seagal, April 28, 2024
# Changed a little bit of variables

# Modified By Kelvin Huang, May 12, 2024
# add animation for hail weather

import pygame 
import random
import math
from constants import *
from wparticles import Wparticles


class Weather:
    types = ['snow', 'rain']

    def __init__(self, type = "random", speed = 1, degree = 0, direction = "center", freq = .3, duration = 10000, gradual = False):
        if type == 'random': self.type = random.choice(self.types)
        else: self.type = type
        self.freq = freq
        self.speed = speed
        self.degree = degree
        self.direction = direction
        
        self.timer = 0
        self.duration = duration * 60
        self.gradual = gradual

        self.is_falling_type = self.type == "snow" or self.type == "rain" or self.type == "hail"
        if self.is_falling_type:
            # set up list of particles for falling type
            self.particles = []

            # set up initial parameter of spawn
            if direction == "left":
                self.spawn = [-math.tan(degree * math.pi/180) * GAME_HEIGHT, 0]
            elif direction == "right":
                self.spawn = [GAME_WIDTH, GAME_WIDTH + math.tan(degree * math.pi/180) * GAME_HEIGHT]
            else:
                self.spawn = [0, GAME_WIDTH]

        # animation
        self.animate_weather = False
        
        # create faded white rectangle        
    def start_animation(self, w_type, duration = 3.0):
        # store previous data
        self.p_type = self.type
        self.p_freq = self.freq

        self.type = w_type
        self.freq = self.freq * 5

        self.animate_weather = True
        self.total_animate_duration = duration * 60
        self.animate_duration = self.total_animate_duration

        if self.type == "hail":
            # create background
            self.background = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            self.alpha = 1
            self.background.set_alpha(self.alpha)
            self.background_color = [255, 255, 255]
            self.background.fill(self.background_color)
    
    def animate(self, game_surf):
        # percentage of the time where the 'fog' will increase
        R_PER = .5
        # percentage of the time where the 'fog' will decrease
        D_PER = .2

        if self.animate_duration > 0:
            if self.animate_duration > (1 - R_PER) * self.total_animate_duration:
                self.alpha += (255 / (R_PER * self.total_animate_duration))
            
            elif self.animate_duration < D_PER * self.total_animate_duration:
                self.alpha -= (255 / (D_PER * self.total_animate_duration))

            # only draw background when animation is going on
            self.background.set_alpha(self.alpha)
            game_surf.blit(self.background, (0,0))
            self.animate_duration -= 1

            # stop animation
            if self.animate_duration == 0:
                self.animate_weather = False
                self.end_animation()

    def end_animation(self):
        self.type = self.p_type
        self.freq = self.p_freq

    def update(self):
        if self.timer < self.duration and self.is_falling_type:
            # gradual increase the range of spawn
            if self.direction == "left" and self.spawn[1] < GAME_WIDTH:
                self.spawn[1] += 1
            elif self.direction == "right" and self.spawn[0] > 0:
                self.spawn[0] -= 1
            
            # try to spawn new particles
            self.spawn_new_particles()
        self.move()
        self.timer += 1

        # when the weather is over and there is no particles del this object
        if self.timer > self.duration and len(self.particles) == 0:
            self.stop()

    def spawn_new_particles(self):
        # control weather if the weather is going to gradual increase/decrease or not
        if self.gradual == True:
            # equations that I made up to stimulate what will the probability be if it increase and decrease gradually
            # link to desmos page: https://www.desmos.com/calculator/mxu2syamzy for the two graths
            if self.timer <= self.duration/2:
                freq = (self.freq)*(math.atan(10/self.duration * (20*self.timer - self.duration))/math.pi + .5)
            else:
                freq = (self.freq)*(math.atan(10/self.duration * (20*self.timer) - 190)/math.pi - .5)
        else:
            freq = self.freq
        
        while freq > 0:
            if random.random() < freq:
                start, end = self.spawn
                position = start + random.random() * (end - start)
                if self.direction == "left":
                    self.particles.append(Wparticles(self.type, self.speed, self.degree, position, self.delete_particle))
                else:
                    self.particles.append(Wparticles(self.type, self.speed, -self.degree, position, self.delete_particle))
            freq -= 1
    
    def delete_particle(self, particle):
        self.particles.remove(particle)
    
    # moved each particles
    def move(self):
        if self.is_falling_type:
            for particle in self.particles:
                particle.move()

    # draw particles objects
    def draw(self, game_surf):
        if self.animate_weather == True:
            self.animate(game_surf)
        # print(len(self.particles))
        if self.is_falling_type:
            for particle in self.particles:
                particle.draw(game_surf)
        
    # delete this object when event is over
    def stop(self):
        del self
        

# hurricane, tornado - spinning and moving
# landslide - moving

# large weather to clear the board
# hail
