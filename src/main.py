from simulator import StateSimulator
from placement_system import PlacementSystem
import pygame


pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

# Simulation Objects
placementSystem = PlacementSystem()
simulator = StateSimulator()


running = True
while running:
    mouseClicked = False
    keyX_Clicked = False
    keyC_Clicked = False
    
    # Poll Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                keyX_Clicked = True
            if event.key == pygame.K_c:
                keyC_Clicked = True
    
    # Main Loop
    simulator.Step(mouseClicked)
    placementSystem.Update(simulator, mouseClicked, keyX_Clicked, keyC_Clicked)

    # Draw and Render
    screen.fill((70, 70, 70))

    simulator.Draw(screen)
    placementSystem.Draw(screen, simulator)

    pygame.display.flip()
    
    # Limit FPS
    clock.tick(60)

pygame.quit()
