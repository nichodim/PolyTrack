# Created by Nicholas Seagal, 4/28/2024
# Is a part of the UI that allows the player to place a powerup from a selection of powerup slots
from constants import *
from powerup import *
from powerup_slot import PowerupSlot


class PowerupMenu:
    # TODO replace track width/height with actual powerup width/height
    def __init__(self, track_box_rect):
        self.rows, self.cols = 2, 3
        self.gap, margin_from_track_box = 10, 30
        menu_width = self.cols * SLOT_WIDTH + self.gap * (self.cols + 1)
        menu_height = track_box_rect.height
        menu_x = track_box_rect.left - margin_from_track_box - menu_width
        menu_y = track_box_rect.top
        self.rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        self.slots = {}
        self.generate_slots()

    # Save every powerup slot to a dictionary (self.slots) with the type as the key
    def generate_slots(self):
        # Since height matches the track box, there is extra padded height above and below powerup rows
        needed_height = self.rows * SLOT_HEIGHT + self.gap * (self.rows + 1)
        extra_height = self.rect.height - needed_height
        originalX = self.rect.left + self.gap
        x, y = originalX, self.rect.top + self.gap + extra_height / 2 - 30
        self.powerup_types_list = list(PowerUpTypes.keys())
        powerup_index = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if powerup_index >= len(self.powerup_types_list): return

                type_name = self.powerup_types_list[powerup_index]
                slot = PowerupSlot(
                    type_name=type_name,
                    pos=(x, y)  # topleft
                )
                self.slots[type_name] = slot
                x += SLOT_WIDTH + self.gap
                powerup_index += 1
            x = originalX
            y += SLOT_HEIGHT + self.gap

    def find_powerup(self, pos):
        for type in self.powerup_types_list:
            slot = self.slots[type]
            if slot.powerup == None: continue
            if slot.powerup.rect.collidepoint(pos): return slot.powerup
        return None

    def remove_powerup(self, powerup):
        slot = self.slots[powerup.type_name]
        slot.remove_powerup()

    def draw(self, game_surf):
        game_surf.blit(PowerupSprites.background_image, self.rect)                  # Modified: Matthew Selvaggi 5-8-24
        for type in self.powerup_types_list:                                        # Blit the background image to the screen
            slot = self.slots[type]
            slot.draw(game_surf)
