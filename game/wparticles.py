# Written By Kelvin Huang, April 21, 2024
# set up foundation of object

# Modified By Kelvin Huang, May 12, 2024
# add animation for hail weather

import math
import random
from constants import *

class Wparticles:
    def __init__(self, type, speed, degree, position, delete_particle):
        self.delete_particle = delete_particle

        self.type = type
        self.speed = speed
        self.degree = degree
        self.x = position
        # adjust y position so it out of the screen
        match self.type:
            case "snow":
                self.y = -(2 + 2 * random.random())
            case "rain":
                self.y = -(10 + 20 * random.random())
            case "hail":
                self.y = -(5 + 10 * random.random())
        
        self.size = -self.y

        match self.type:
            case "snow":
                # scaling speed of particle based on the particle size
                self.speed *= self.size / 2
            
            case "rain":
                # update speed based on size
                self.speed *= self.size / 10
                # set up surface
                self.surface = pygame.Surface([5, self.size])
                # color of the rain drops
                self.surface.fill(((0,0,255)))
                self.surface.set_colorkey(Colors.white)

                # rotation of the rain
                self.rotate = pygame.transform.rotate(self.surface, self.degree)
                self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))
            
            case "hail":
                self.speed *= self.size / 2
                number_of_points = random.randint(10, 30)
                max_radius = self.size
                self.points = []

                interval = 360/number_of_points
                min_degree = random.randint(0, 360)
                max_degree = min_degree + interval


                for i in range(number_of_points):
                    radius = max_radius * .8 + max_radius * .2 * random.random()
                    degree = min_degree + (max_degree - min_degree) * random.random()
                    self.points.append((self.x + radius * math.cos(math.radians(degree)), self.y + radius * math.sin(math.radians(degree))))

                    min_degree += interval
                    max_degree = min_degree + interval
                
                self.interal_degree = 0
                

    def move(self):
        # moved object
        self.x += self.speed * math.sin(self.degree * math.pi/180)
        self.y += self.speed
        
        # move individual points
        if self.type == "hail":
            self.interal_degree += 1
            center = self.x, self.y

            for i in range(len(self.points)):
                x = self.points[i][0] + self.speed * math.sin(self.degree * math.pi/180)
                y = self.points[i][1] + self.speed 

                x, y = self.rotate((self.x, self.y), (x, y), 0.1)
                self.points[i] = (x, y)
        
        # delete object if out of screen
        if (self.y - self.size) > GAME_HEIGHT or (self.degree > 0 and self.x - self.size > GAME_WIDTH) or (self.degree < 0 and self.x + self.size < 0):
            if self.type == "hail":
                pass
                #print("deleted hail object")
            self.delete_particle(self)
            del self
    
    def rotate(self, center, point, rate):
        x, y = center
        x1, y1 = point
        # radius
        radius = math.sqrt((x1 - x)**2 + (y1 - y)**2)

        # calculate point degree with respect to the center
        x_distance = (x1 - x)/radius
        y_distance = (y1 - y)/radius

        # first quadrant
        if x_distance >= 0 and y_distance >= 0:
            degree = math.acos(x_distance)
        # second quadrant
        elif x_distance <= 0 and y_distance >= 0:
            degree = math.acos(x_distance)
        # third quadrant
        elif x_distance <= 0 and y_distance <= 0:
            degree = math.acos(x_distance) - 2 * math.asin(y_distance)
        # forth quadrant
        elif x_distance >= 0 and y_distance <= 0:
            degree = math.asin(y_distance)

        return (radius * math.cos(degree + rate) + x, radius * math.sin(degree + rate) + y)

    def draw(self, game_surf):
        match self.type:
            # draw for snow
            case "snow":
                pygame.draw.circle(game_surf, (255, 255, 255), (self.x, self.y), self.size)
            # draw for rain
            case "rain":
                self.rotate_rect = self.rotate.get_rect(center = (self.x, self.y))
                game_surf.blit(self.rotate, self.rotate_rect)
            # draw for hail
            case "hail":
                pygame.draw.polygon(game_surf, (204, 221, 255), self.points)