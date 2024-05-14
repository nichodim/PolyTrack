'''
    Created by Kelvin Huang, May 13, 2024
    timer object that can be used for cooldown or delays
    call: Timer(x location, y location, radius, duration (second))
    methods:
            tick(speed) -   Return True when time hit <= 0
                            else return false
                            optional speed parameter to speed up time
'''
import pygame
import math

class Timer:
    def __init__(self, x, y, radius, duration = 3):
        self.x = x
        self.y = y
        self.duration = duration * 60
        self.radius = radius
        self.clock_object = []

        self.rect = pygame.Rect(self.x - radius, self.y - radius, 2 * radius, 2 * radius)
        self.clock()
        
        self.degree = math.pi/2
        self.rate = 2 * math.pi/self.duration
        self.tick()
    
    def clock(self):
        # number of large tick and smaller tick
        large_tick = 6
        small_tick = 3
        
        lt_degree_interval = (2*math.pi)/large_tick
        st_degree_interval = lt_degree_interval/(small_tick + 1)

        # how far from center is the starting point of each tick
        lt_radius = .6 * self.radius
        st_radius = .9 * self.radius

        # start from the 12 hour hand
        degree = math.pi/2

        # store the 2 point of each tick
        for i in range(large_tick):
            point1 = (self.x + lt_radius * math.cos(degree), self.y + lt_radius * -math.sin(degree))
            point2 = (self.x + self.radius * math.cos(degree), self.y + self.radius * -math.sin(degree))
            self.clock_object.append((point1, point2))

            for i in range(small_tick):
                degree -= st_degree_interval
                point1 = (self.x + st_radius * math.cos(degree), self.y + st_radius * -math.sin(degree))
                point2 = (self.x + self.radius * math.cos(degree), self.y + self.radius * -math.sin(degree))
                self.clock_object.append((point1, point2))

            degree -= st_degree_interval

    def tick(self, speed = 1):
        self.tick_object = []
        total_points = 300
        
        interval = speed * abs(5 * math.pi/2 - self.degree)/total_points
        degree = self.degree
        self.tick_object.append((self.radius, self.radius))

        for i in range(total_points):
            self.tick_object.append((self.radius + self.radius * math.cos(degree), self.radius + self.radius * -math.sin(degree)))
            degree += interval
        
        self.degree -= self.rate
        self.duration -= 1
        if self.duration <= 0:
            del self
            return True
        return False

    def draw(self, game_surf):
        # reference to https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame
        
        # draw the clock
        color = pygame.Color(255, 255, 255, 255)
        target_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (self.radius, self.radius), self.radius)
        game_surf.blit(shape_surf, target_rect)

        pygame.draw.arc(game_surf, (0, 0, 0), self.rect, 0, 2*math.pi, width=1)
        
        for object in self.clock_object:
            point1, point2 = object
            pygame.draw.line(game_surf, (0, 0, 0), point1, point2, width=1)

        # draw the timer
        color = pygame.Color(100, 100, 100, 255)
        target_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, self.tick_object)
        game_surf.blit(shape_surf, target_rect)

    def __del__(self):
        pass
        #print("Item successfully deleted")