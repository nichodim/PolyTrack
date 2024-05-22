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

## ERD Diagram

![Screenshot 2024-05-21 130617](https://github.com/mattsel/PolyTracks/assets/141775337/8aaabb13-15dd-4ef8-827b-ea3b9b9c6438)

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
with each possible direction that the track can be placed with rotation. The train is listening for the instructions from each track set, this is just some of the basic
and core concept behind the track and train implementaion
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
in that location. The same logic applies for the highlighting of the tracks, it simply draws a green hue where the mouse is dragging the track, but will change to a red hue if the system detects hovering of a non-None object
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
