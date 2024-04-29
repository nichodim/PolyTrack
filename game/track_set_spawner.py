import random
from constants import *
from track_set import TrackSet
from track_set_types import SpawnTracks, TrackSetTypes

class TrackSetSpawner:
    def __init__(self, rect):
        self.rect = rect
        self.item = None

        # Modified by Kelvin Huang, April 28, 2024
        # new randomly generate track system using weights

        # create a basic dictionary that stores the weight of each track types
        self.type_weight = {}
        # make all of their weights start at 1
        for type in range(len(SpawnTracks)):
            self.type_weight[type] = 1

    # Spawner logic
    def spawn_track_set(self):
        if self.item: return None
        
        # modified by Kelvin Huang, April 28, 2024
        # new randomly generate track system using weights
        
        # add all the weights together 
        total = 0
        for key in self.type_weight:
            total += self.type_weight[key]
        # use that to generate a number between 1 and the total
        random_number = random.randint(1, total)

        # using randomly generate number check the key that associate with that number

        # count is use to compare the range
        count = 1
        for key in self.type_weight:
            # add number to count to find the maximum of that range
            count += self.type_weight[key]
            # if the weight is 0 we add 1 to the weight for that key
            if self.type_weight[key] == 0:
                self.type_weight[key] += 1
            # if the randomly generate number is within that range
            # that track type with will be selected and it weight will be reset to 0
            elif count - self.type_weight[key] <= random_number < count:
                set_type = SpawnTracks[key]
                self.type_weight[key] = 0
            # tracks that are not selected have their weight increased by 1
            else:
                self.type_weight[key] += 1
        
        #set_type = random.choice(SpawnTracks)
        track_set = TrackSet(
            pos = self.rect.topleft,
            type = set_type
        )
        track_set.set_position_by_center(self.rect.center)
        
        self.item = track_set
        return track_set



    # Rendering
    def draw(self, game_surf):
        pygame.draw.rect(game_surf, Colors.black, self.rect)
