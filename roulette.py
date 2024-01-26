import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Russian Roulette")

# Set up colors
white = (255, 255, 255)
gray = (169, 169, 169)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up special move
special = 1
double = 1
shield = 1
cheat = False

# Cag

# Function to initialize the gun with a random number of real bullets (1 or 2)
def initialize_gun():
    gun_size = 6
    special = 1
    double = 1
    shield = 1
    num_real_bullets = random.choice([1, 2])
    gun = ['blank'] * (gun_size - num_real_bullets) + ['real'] * num_real_bullets
    random.shuffle(gun)
    return gun, double, special, shield

# Function to display text on the screen
def display_text(text, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

    
# Initialize players and lives
players = [1, 2]
initial_lives = 10
player_lives = {player: initial_lives for player in players}
current_player = 1
damage = 1
ricochet = False
gun, double, special, shield = initialize_gun()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                player_lives = {player: initial_lives for player in players}
                current_player = random.choice(players)
                gun, double, special, shield = initialize_gun()
                # Toggle cheat
            elif event.key == pygame.K_c:
                cheat = not cheat

    screen.fill(black)

    # Display cheat
    if (cheat):
        for i, bullet in enumerate(gun):
            pygame.draw.rect(screen, white if bullet == 'blank' else red, (250 + i * 50, 550, 40, 40))

    # Display lives
    display_text(f"Player 1's HP: {player_lives[1]}", white, (100, 50))
    display_text(f"Player 2's HP: {player_lives[2]}", white, (width - 400, 50))

    # Display player's turn
    if (damage == 2):
        display_text(f"Player {current_player}'s turn (2x Damage)*", green, (50, 100))
    else:
        display_text(f"Player {current_player}'s turn", white, (50, 100))

    # Display options
    display_text("(1). Use the gun on yourself", white, (80, 150))
    display_text("(2). Shoot your opponent", white, (80, 180))
    if (special >= 1):
        display_text(f"(3). Use special ability to see 2 next bullets x{special}", white, (80, 210))
    else: 
        display_text(f"(3). Use special ability to see 2 next bullets x{special}", gray, (80, 210))
    if (double >= 1):   
        display_text(f"(4). Use special ability for double damage x{double}", white, (80, 240))
    else:
        display_text(f"(4). Use special ability for double damage x{double}", gray, (80, 240))
    if (shield >= 1):   
        display_text(f"(5). Use special ability for shield x{shield} (N/a)", white, (80, 270))
    else:
        display_text(f"(5). Use special ability for shield x{shield} (N/a)", gray, (80, 270))
    display_text("Press 'r' to reset the game, 'c' for cheat", white, (50, 350))

    pygame.display.flip()

    # Get player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        action = 'self'
    elif keys[pygame.K_2]:
        action = 'opponent'
    elif keys[pygame.K_3]:
        action = 'special'
    elif keys[pygame.K_4]:
        action = 'double'
    elif keys[pygame.K_5]:
        action = 'shield'
    else:
        continue

    # Process player's turn
    if action == 'self':
        if gun.pop(0) == 'real':
            player_lives[current_player] -= damage
            display_text(f"Player {current_player} took a shot and lost {damage} hp! Lives remaining: {player_lives[current_player]}", white, (50, 400))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display the result for 3 seconds
            gun, double, special, shield = initialize_gun()
            damage = 1
            if player_lives[current_player] <= 0:
                print(f"Player {3 - current_player} wins!")
                pygame.quit()
                sys.exit()
            else:
                pygame.time.delay(1000)
        else:
            display_text(f"Player {current_player} took a shot and survived. They get another turn.", white, (50, 400))
            damage = 1

            
    elif action == 'opponent':
        if gun.pop(0) == 'real':
            player_lives[3 - current_player] -= damage
            display_text(f"Player {current_player} shot their opponent! Opponent lost {damage} hp. Lives remaining: {player_lives[3 - current_player]}", white, (50, 400))
            gun, double, special, shield = initialize_gun()
            damage = 1
            pygame.display.flip()
            pygame.time.delay(3000)  # Display the result for 3 seconds
            if player_lives[3 - current_player] <= 0:
                print(f"Player {current_player} wins!")
                pygame.quit()
                sys.exit()
        else:
            display_text(f"Player {current_player} missed. They give the gun to their opponent.", white, (50, 400))
            damage = 1
            current_player = 3 - current_player  # Switch player
            
    elif action == 'special':
        if (special == 0):
            display_text(f"Invalid choice", white, (50, 400))
        else:    
            visible_bullets =  ', '.join(map(str,gun[:2]))
            display_text(f"Next 2 bullets: {visible_bullets}", white, (50, 400))
            special -= 1
        
    elif action == 'double':
        if (double == 0):
            display_text(f"Invalid choice", white, (50, 400))
        else:
            damage = 2
            display_text(f"Double damage for the next shot", white, (50, 400))
            double -= 1
            
    elif action == 'shield':
        if (shield == 0):
            display_text(f"Invalid choice", white, (50, 400))
        else:
            ricochet = random.choice([True, False]); 
            display_text(f"Invalid choice", white, (50, 400))
            # display_text(f"Raise your Shield", white, (50, 400))
            shield -= 1

    pygame.display.flip()
    pygame.time.delay(2000)  # Display the turn result for 2 seconds
 
