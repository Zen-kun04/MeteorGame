import pygame
import random
from typing import List

pygame.init() # initialize pygame
pygame.mixer.init() # initialize pygame mixer (for sound effects)

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
best_score = 0

def draw_window(player: pygame.Rect, meteors: List[pygame.Rect]) -> None:
    """
    Function to draw:
    - The player (spaceship ?)
    - The meteors
    - Set the background to black
    """
    WIN.fill(0) # Black background
    pygame.draw.rect(WIN, (0, 157, 255), player) # Draw the player created by the "spawn_player" function
    
    """
    Drawing the meteors
    
    The for loop and the "update" method are useful when we decrease the Y axis of each meteor
    """
    for meteor in meteors:
        pygame.draw.rect(WIN, (255, 0, 0), meteor)
        
    pygame.display.update()

def spawn_player() -> pygame.Rect:
    return pygame.draw.rect(WIN, (255, 255, 255), (WIDTH / 2, HEIGHT - 50, 50, 50)) # Create the player but will not draw it

def spawn_meteor() -> pygame.Rect:
    """
    Create the meteor with a random X axis
    (between 1/4 of the screen and 3/4 of the 
    screen so meteors have a bigger % of chances 
    to touch the player) and a Y axis of 0
    """
    return pygame.draw.rect(WIN, 0, (random.randint(int(WIDTH / 4), int(WIDTH - (WIDTH / 4))), 0, 32, 32))

def game_over_screen(points: int) -> None:
    """
    Display the game over / victory screen.
    The victory screen appears only if you get a higher score than "best_score"
    """
    global best_score
    font = pygame.font.SysFont(None, 100) # Set the size of text to 100 and do not use any font (just the default one)
    if points > best_score:
        """
        If true, the player has a new high score so:
        - Display "NEW SCORE" instead of "Game Over"
        - Set the value of "best_score" as the current score
        - Play the victory sound
        """
        text = font.render(f"NEW SCORE | Points: {points}", True, (255, 255, 255))
        best_score = points
        pygame.mixer.music.load("sounds/victory.mp3")
        pygame.mixer.music.play()
    else:
        """
        If false, the player has not a new high score so:
        - Display "Game Over" instead of "NEW SCORE"
        - Play the game over sound
        """
        text = font.render(f"Game Over | Points: {points}", True, (255, 255, 255))
        pygame.mixer.music.load("sounds/game_over.wav")
        pygame.mixer.music.play()
    
    """
    Buttons to restart the game or quit the game
    (if you restart you will not lose your high score)
    """
    restart_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
    quit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 120, 200, 50)
    
    """
    Draw the buttons and the text
    """
    pygame.draw.rect(WIN, (0, 255, 0), restart_button)
    pygame.draw.rect(WIN, (255, 0, 0), quit_button)
    
    font = pygame.font.SysFont(None, 50)
    restart_text = font.render("Restart", True, (0, 0, 0))
    quit_text = font.render("Quit", True, (0, 0, 0))
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    WIN.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) / 2, restart_button.y + (restart_button.height - restart_text.get_height()) / 2))
    WIN.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) / 2, quit_button.y + (quit_button.height - quit_text.get_height()) / 2))
    
    pygame.display.update() # Update the screen to display the text and the buttons
    
    waiting = True
    while waiting:
        """
        Event loop to check if the player clicked on the restart button, 
        the quit button or if the player closed the window
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(pos):
                    waiting = False
                    main()
                elif quit_button.collidepoint(pos):
                    pygame.quit()
                    exit()

def main():
    """
    Main function to run the game
    """
    clock = pygame.time.Clock() # Create a clock object to control the FPS
    pygame.mixer.music.load("sounds/meteor_explosion.wav") # Load the sound effect by default because the player will only destroy meteors
    pygame.display.set_caption(f"Meteor Game | Points: 0") # Set the title of the window
    run = True
    frames_until_spawn_static = 80 # This is the reference for "frames_until_spawn" to know when to spawn a new meteor
    frames_until_spawn = 0 # This is the real counter to know when to spawn a new meteor
    meteors: List[pygame.Rect] = [] # List of meteors to draw/update
    player = spawn_player()
    
    points = 0 # Current points
    meteor_speed = 1 # Speed of the meteors by default
    while run:
        clock.tick(FPS)
        """
        Event loop to check if the player clicked on the close button
        or if the player clicked on a meteor
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, meteor in enumerate(meteors):
                    if meteor.collidepoint(pos):
                        """
                        If the player clicked on a meteor then:
                        - Remove the meteor from the list
                        - Increase the points by 1
                        - Update the title of the window
                        - Play the sound effect
                        - Increase the speed of the meteors if the points are divisible by 10 (but the speed will not exceed 5)
                        - Decrease the frames by 5 to spawn a new meteor if the points are divisible by 10 (but the frames will not be less than 5)
                        """
                        meteors.pop(i)
                        points += 1
                        pygame.display.set_caption(f"Meteor Game | Points: {points}")
                        # play sound
                        pygame.mixer.music.play()
                        if points % 10 == 0:
                            if meteor_speed < 5:
                                meteor_speed += 1
                            if frames_until_spawn_static > 5:
                                frames_until_spawn_static -= 5 # Decrease the reference counter by 5
                        break

        if frames_until_spawn <= 0: # If the counter is less than or equal to 0 then spawn a new meteor
            meteors.append(spawn_meteor())
            frames_until_spawn = frames_until_spawn_static # Reset the counter to the reference
        else:
            frames_until_spawn -= 1 # Decrease the counter by 1
        
        """
        For each meteor in the list, increase the Y axis by the speed of the meteors
        and check if the meteor collides with the player
        """
        for meteor in meteors:
            meteor.y += meteor_speed
            if meteor.colliderect(player):
                game_over_screen(points)
                run = False
        meteors = [m for m in meteors if m.y < HEIGHT] # Keep only the meteors that are not out of the screen
        
        draw_window(player, meteors)
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()