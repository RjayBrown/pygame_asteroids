import sys
import pygame
from constants import *
from logger import log_event, log_state
from sprites.player import Player
from sprites.asteroid import Asteroid
from sprites.asteroidfield import AsteroidField
from sprites.shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = updatable
    Player.containers = (drawable, updatable)
    Shot.containers = (shots, drawable, updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS)
    asteroidfield = AsteroidField()

    dt = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.kill()
                    shot.kill()

        for member in drawable:
            member.draw(screen)
        pygame.display.flip()
        ms_tick = clock.tick(60)
        dt = ms_tick / 1000


if __name__ == "__main__":
    main()
