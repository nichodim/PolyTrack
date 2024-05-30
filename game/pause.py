from constants import *
from menu import Menu

class PauseMenu:
    # Author: Matthew Selvaggi
    # Date: 5-29-24
    # Purpose: Call for pause/win/lose menu with respective button images.
    def menu(self, button1_image, button1_image_hover, button2_image, button2_image_hover, ):
        # Initial box dimensions
        box_width = 700
        box_height = 400
        border_width = 5
        button_width = 250
        button_height = 100
        button_spacing = 50
        threshold = 50

        # Center of the box x,y
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = (GAME_HEIGHT - box_height) // 2

        # Boarder to the box
        bordered_box_surf = pygame.Surface((box_width, box_height))
        bordered_box_surf.fill(Colors.black)
        blue_box_surf = pygame.Surface((box_width - 2 * border_width, box_height - 2 * border_width))
        blue_box_surf.fill(Colors.sky_blue)

        # Blit boxes
        self.game_surf.blit(bordered_box_surf, (box_x, box_y))
        self.game_surf.blit(blue_box_surf, (box_x + border_width, box_y + border_width))

        # Button position
        total_space = box_width - (2 * border_width)
        total_button_width = 2 * button_width + button_spacing
        available_space = total_space - total_button_width

        # Calculate x-cords for the buttons
        button_x1 = box_x + border_width + (available_space // 2)
        button_x2 = button_x1 + button_width + button_spacing

        button_y = box_y + (box_height - button_height) // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Scale button images
        button_image_normal1 = pygame.transform.scale(button1_image, (button_width, button_height))
        button_image_hover1 = pygame.transform.scale(button1_image_hover, (button_width, button_height))
        button_image_normal2 = pygame.transform.scale(button2_image, (button_width, button_height))
        button_image_hover2 = pygame.transform.scale(button2_image_hover, (button_width, button_height))

        # Calculate distances to button centers
        distance_to_button1 = math.sqrt(
            (button_x1 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)
        distance_to_button2 = math.sqrt(
            (button_x2 + button_width / 2 - mouse_x) ** 2 + (button_y + button_height / 2 - mouse_y) ** 2)

        # Change button to hover animation
        if distance_to_button1 < threshold:
            self.game_surf.blit(button_image_hover1, (button_x1, button_y))
        else:
            self.game_surf.blit(button_image_normal1, (button_x1, button_y))

        if distance_to_button2 < threshold:
            self.game_surf.blit(button_image_hover2, (button_x2, button_y))
        else:
            self.game_surf.blit(button_image_normal2, (button_x2, button_y))

        # Render Text
        font_time = pygame.font.Font('font/font.ttf', 36)
        font_message = pygame.font.Font('font/font.ttf', 45)
        elapsed_time_text = f'Time: {self.saved_time:.2f} seconds'
        text_surface = font_time.render(elapsed_time_text, True, (0, 0, 0))

        # Displays winner/loser if the game is completed
        if self.loser:
            result_message = f"Loser!"
            result_text = font_message.render(result_message, True, (255,0,0))
        elif self.winner:
            result_message = f"Winner!"
            result_text = font_message.render(result_message, True, (0,255,0))
        else:
            result_message = f"Paused"
            result_text = font_message.render(result_message, True, (0,0,0))
                
        # Text Position of Reult
        text_width = result_text.get_width()
        text_x = box_x + (box_width - text_width) // 2
        text_y = box_y + 50

        self.game_surf.blit(result_text, (text_x, text_y))


        # Text Position of Time
        text_width = text_surface.get_width()
        text_x = box_x + (box_width - text_width) // 2
        text_y = box_y + 280

        self.game_surf.blit(text_surface, (text_x, text_y))

        # Check for button clicks
        if distance_to_button1 < threshold and pygame.mouse.get_pressed()[0]:
            SFX.bleep.play()
            if self.resume:
                self.paused = not self.paused
            else:
                menu = Menu()
                menu.map_menu()

        elif distance_to_button2 < threshold and pygame.mouse.get_pressed()[0]:
            SFX.bleep.play()
            self.quit_game()