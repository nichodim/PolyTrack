# PolyTracks
The objective of this project was to practice team development using Agile Methodologies and an Evolutionary software life cycle development. This game was created with the help of three
other developers as a means to become more proficient and collaborative programmers. Within this game, there are traces of excellent modular object-oriented programming which has allowed us
to build a foundation that is more scaleable for our product's needs. Our process for developing this game was through the use of a Scrum master, Kanban boards, and 3-week sprints. Each sprint
we set out to complete user stories along with documenting our team's progress through the use of burndown charts.

## Game Objective - Instructions
When the user loads into the game, they are greeted with a menu screen to allow them to select the terrain and map size that they would like to play on. After the user has selected a map, the game will begin
in which they are able to generate tracks and store them in the track box. The train will shortly begin spawning after the delay timer goes off, when this happens the user must orient the tracks accordingly to allow the user
to connect the tracks for the train to have a path to reach its destination. During this time the user is also able to use a variety of powerups in the game to such as slowdown, bomb, and freeze. For example, if the user has
run into a situation in which they placed a track in the wrong direction or an obstacle is blocking their direction, the user is able to drag the bomb and destroy the object in their way. The user is able to pause the game
by pressing `ESC` and they can rotate tracks by pressing `r`. After the user has either won or lost the game, they will be prompted with a screen describing their game with an option of `Restart` or `Quit`

## Video Overview
`Watch Me`
[![PolyTracks](https://github.com/mattsel/PolyTracks/assets/141775337/ef4d80fd-17d5-452d-82bb-280171b01317)](https://youtu.be/etNQuOJsIig)

## Train Logic
The train's features were built using a combination of math and lists. Each time a new train is created, it will follow ing the path of the train in front of it. If the train is the front train, it will simply follow the 
directions of the tracks through instructions from the tracks dictionary. The train can listen to the track's logic and adjust accordingly through this code.
```python
    def update_speed(self):
        if self.direction == 'forward' or self.direction == 'crash': return

        self.period = (2 * math.pi * (TRACK_WIDTH/2)) / self.speed 

        if self.direction == "clockwise":
            self.degree -= 360 / self.period #  minus degree since it going counter-clockwise

        # counter-clockwise
        if self.direction == "counter-clockwise":
            self.degree += 360 / self.period # add degree since it going counter-clockwise
        
        # the following if statement is used it case the speed is a number that not a factor of 90            
        if round(self.degree % 90, 5) < round(360 / self.period, 5): # check when it close full turns
            self.direction = "forward" # stop it from turning
            self.degree -= self.degree % 90 # correct it

        # update the turn on screen
        self.rotate = pygame.transform.rotate(self.surface, self.degree)
    
    def move(self):
        self.x += self.speed * math.cos(math.radians(self.degree)) 
        self.y += self.speed * -math.sin(math.radians(self.degree))
```

## Track Logic
Some of the basic track logic can be found in the track set dictionary of constants. For each track type, there is an appropriate dictionary with each attribute.
```python vertical = {
    'name': 'vertical', 
    'sprite': TrackSprites.vertical, 
    'directions': ["crash", "forward", "crash", "forward"]
}
horizontal = {
    'name': 'horizontal', 
    'sprite': TrackSprites.horizontal, 
    'directions': ["forward", "crash", "forward", "crash"]
}
```
This is for each track per block, but this gets more complicated when the tracks are combined to be larger sets. An example of our U-turn track set
with each possible direction that the track can be placed with rotation. The train is listening for the instructions from each track set, these is just some of the basic
and core concept behind the track and train implementation
```python
# u
    'u-1': [
        ('origin', left), 
        ('left', right)
    ], 
    'u-2': [
        ('origin', ileft), 
        ('up', left)
    ], 
    'u-3': [
        ('origin', iright), 
        ('right', ileft)
    ], 
    'u-4': [
        ('origin', right), 
        ('down', right)
    ],
```

## Track Dragging Logic
When the user grabs a track from the toolbox, they can drag the track onto the board. This is done through the use of mouse tracking and checking the position on the board. If the location
that the user is trying to drag a track is detected to be None, then the track will append to that position, but if the position on the board is filled, then the track will not be able to be placed
in that location. The same logic applies for the highlighting of the tracks, it simply draws a green hue where the mouse is dragging the track but will change to a red hue if the system detects hovering of a non-None object
```python
    def find_hovered_track_and_index(self, track_set):
        for i in range(100):
            mouse_pos = pygame.mouse.get_pos()
            hovered_track = track_set.find_track_in_pos(mouse_pos)
            if hovered_track != None:
                hovered_track_index = track_set.tracks.index(hovered_track)
                return (hovered_track, hovered_track_index)
        return None
```

## Powerups
Next, we will move into some of the implementation of powerups within the game. The user is able to utilize different powerups from the powerup menu, this functionality is closely related to the toolboxes. 
When the user grabs a power-up, they are able to drag it onto the map and drop it on a set location. There are a variety of powerups such as slow potions, bombs, and freeze types. The implementation of these bombs
is closely related to the implementation of the track direction in terms of configuration. Each powerup has its own configuration which the game will utilize as instructions. For example, the following is the bomb
configurations
```python
PowerUpTypes = { # Actual config
    'bomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.bomb,
        'effected attachments': ['Obstacle', 'Track'], # Empty to effect all

        # Type specific
        'highlight color': Colors.red,
        'blast radius': 1
    },
    'bigbomb': {
        # Generic definitions
        'dimensions': (50, 50),
        'sprite': PowerupSprites.bomb_lit,
        'effected attachments': ['Obstacle', 'Track'], # Empty to effect all

        # Type specific
        'highlight color': Colors.red,
        'highlight color': Colors.yellow,
        'blast radius': 2
    },
```
## Weather Types
Lastly, we will talk about the weather and animations involved in the snow maps. One cool feature within the snow map is that each time a bomb is dragged on top of an ice-type tile, the tile will become water and will not allow
the user to drag tracks onto the water. But we want to focus on the constant animation of snow on the user's screen to give the game a winter feel. Our team was able to implement weather types based on which type of weather it is 
such as snow, rain, or hail. The different initializations can be seen below
```python
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
```
Following these initializations based on which case of weather it is, the program will then animate the particle on the screen. The animation of the particles is done through
the use of rotations and `MATH` :)
```python
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
```

There are many more features to check out and we hope that you enjoyed taking a look at the project that our team has spent the last 14 weeks developing.
