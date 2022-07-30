import pygame
from sys import exit
from random import randint


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surfs = [bird_mid_surf, bird_up_surf, bird_down_surf]
        self.surf_state = 0
        self.surf = bird_mid_surf
        self.rect = self.surf.get_rect(bottomleft = (100, 400))
        self.gravity = 0
        self.angle = 0

    def draw(self):
        self.surf = self.surfs[int(self.surf_state)]
        self.surf = pygame.transform.rotate(self.surf, self.angle * 0.8)
        screen.blit(self.surf, self.rect)
        self.surf_state = self.surf_state + 0.1
        self.angle -= 3

        if(self.surf_state >= len(self.surfs)):
            self.surf_state = 0

        self.gravity += 1
        self.rect.y += self.gravity

    def reset(self):
        self.surfs = [bird_mid_surf, bird_up_surf, bird_down_surf]
        self.surf_state = 0
        self.surf = bird_mid_surf
        self.rect = self.surf.get_rect(bottomleft = (100, 400))
        self.gravity = 0
        self.angle = 0


class Pipe(pygame.sprite.Sprite):
    def __init__(self, rotated, pos):
        super().__init__()
        self.rotated = rotated

        if rotated == True:
            self.image = pygame.transform.rotate(pipe_surf, 180)
            self.rect = self.image.get_rect(midbottom = (600, pos))
        else:
            self.image = pipe_surf
            self.rect = self.image.get_rect(midtop = (600, pos))

    def update(self):
        self.rect.x -= 10
        
        if self.rotated and self.rect.x == 100 - self.rect.width // 2:
            game.score += 1
            point_sound.play()

    def destroy(self):
        if(self.rect.x <= -100):
            self.kill()


class Game:
    def __init__(self):
        self.is_active = False
        self.floor_pos1 = 0
        self.floor_pos2 = 672
        self.high_score = 0
        self.score = 0
        self.first = True
        self.bird = Bird()
        bird_group.add(self.bird)

    def draw_floor(self):
        screen.blit(base_surf, (self.floor_pos1, 850))
        screen.blit(base_surf, (self.floor_pos2, 850))
        self.floor_pos1 -= 2
        self.floor_pos2 -= 2

        if self.floor_pos2 < 0:
            self.floor_pos1 = 0
            self.floor_pos2 = 672

    def generate_pipe(self):
        top_pos = randint(100, 500)
        bottom_pos = top_pos + 250
        top = Pipe(True, top_pos)
        bottom = Pipe(False, bottom_pos)
        pipe_group.add(top)
        pipe_group.add(bottom)

    def draw_bird(self):
        self.bird.draw()

    def draw_pipes(self):
        pipe_group.draw(screen)
        pipe_group.update()

    def draw_message(self):
        screen.blit(message_surf, message_rect)

    def draw_score(self):
        if self.is_active:
            score_surf = score_font.render(str(self.score), True, (255, 255, 255))
            score_rect = score_surf.get_rect(center = (288, 100))
            screen.blit(score_surf,score_rect)
        else:
            score_surf = score_font.render('Score: ' + str(self.score), True, (255, 255, 255))
            score_rect = score_surf.get_rect(center = (288, 100))
            screen.blit(score_surf,score_rect)

            high_score_surf = score_font.render('High score: ' + str(self.high_score), True, (255, 255, 255))
            score_rect = high_score_surf.get_rect(center = (288, 800))
            screen.blit(high_score_surf, score_rect)

    def detect_collision(self):
        if pygame.sprite.spritecollide(bird_group.sprite, pipe_group, False)\
            or self.bird.rect.y < 0 or self.bird.rect.y > 850:
            pipe_group.empty()
            
            if self.score > self.high_score:
                self.high_score = self.score

            hit_sound.play()
            self.is_active = False


pygame.init()
screen = pygame.display.set_mode((576, 1000))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

bg_day_surf = pygame.image.load('images/background-day.png').convert()
bg_day_surf = pygame.transform.scale2x(bg_day_surf)
bg_night_surf = pygame.image.load('images/background-night.png').convert()
bg_night_surf = pygame.transform.scale2x(bg_night_surf)
bg_surf = bg_day_surf

base_surf = pygame.image.load('images/base.png').convert()
base_surf = pygame.transform.scale2x(base_surf)

yellowbird_up_surf = pygame.image.load('images/yellowbird-upflap.png')
yellowbird_up_surf = pygame.transform.scale2x(yellowbird_up_surf)
yellowbird_mid_surf = pygame.image.load('images/yellowbird-midflap.png')
yellowbird_mid_surf = pygame.transform.scale2x(yellowbird_mid_surf)
yellowbird_down_surf = pygame.image.load('images/yellowbird-downflap.png')
yellowbird_down_surf = pygame.transform.scale2x(yellowbird_down_surf)

bluebird_up_surf = pygame.image.load('images/bluebird-upflap.png')
bluebird_up_surf = pygame.transform.scale2x(bluebird_up_surf)
bluebird_mid_surf = pygame.image.load('images/bluebird-midflap.png')
bluebird_mid_surf = pygame.transform.scale2x(bluebird_mid_surf)
bluebird_down_surf = pygame.image.load('images/bluebird-downflap.png')
bluebird_down_surf = pygame.transform.scale2x(bluebird_down_surf)

redbird_up_surf = pygame.image.load('images/redbird-upflap.png')
redbird_up_surf = pygame.transform.scale2x(redbird_up_surf)
redbird_mid_surf = pygame.image.load('images/redbird-midflap.png')
redbird_mid_surf = pygame.transform.scale2x(redbird_mid_surf)
redbird_down_surf = pygame.image.load('images/redbird-downflap.png')
redbird_down_surf = pygame.transform.scale2x(redbird_down_surf)

bird_up_surf = yellowbird_up_surf
bird_mid_surf = yellowbird_mid_surf
bird_down_surf = yellowbird_down_surf

pipe_green_surf = pygame.image.load('images/pipe-green.png')
pipe_green_surf = pygame.transform.scale2x(pipe_green_surf)
pipe_red_surf = pygame.image.load('images/pipe-red.png')
pipe_red_surf = pygame.transform.scale2x(pipe_red_surf)
pipe_surf = pipe_green_surf

bird_group = pygame.sprite.GroupSingle()
pipe_group = pygame.sprite.Group()

message_surf = pygame.image.load('images/message.png').convert_alpha()
message_surf = pygame.transform.scale2x(message_surf)
message_rect = message_surf.get_rect(center = (288, 450))
score_font = pygame.font.Font("fonts/04B_19.TTF", 40)

flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
point_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
hit_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')

SPAWN_PIPES = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPES, 1000)
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game.is_active and event.type == SPAWN_PIPES:
            game.generate_pipe()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.is_active:
                    game.bird.gravity = -20
                    game.bird.angle = 50
                    flap_sound.play()
                else:
                    if game.first:
                        bg_surf = bg_day_surf
                        bird_up_surf = yellowbird_up_surf
                        bird_mid_surf = yellowbird_mid_surf
                        bird_down_surf = yellowbird_down_surf
                        pipe_surf = pipe_green_surf
                        game.first = False
                        game.is_active = True
                    else:
                        r = randint(0, 1)

                        if r == 0:
                            bg_surf = bg_day_surf
                        else:
                            bg_surf = bg_night_surf

                        r = randint(0, 1)

                        if r == 0:
                            pipe_surf = pipe_green_surf
                        else:
                            pipe_surf = pipe_red_surf

                        r = randint(0, 2)

                        if r == 0:
                            bird_up_surf = yellowbird_up_surf
                            bird_mid_surf = yellowbird_mid_surf
                            bird_down_surf = yellowbird_down_surf
                        elif r == 1:
                            bird_up_surf = bluebird_up_surf
                            bird_mid_surf = bluebird_mid_surf
                            bird_down_surf = bluebird_down_surf
                        else:
                            bird_up_surf = redbird_up_surf
                            bird_mid_surf = redbird_mid_surf
                            bird_down_surf = redbird_down_surf
                        
                        game.score = 0
                        game.bird.reset()
                        game.is_active = True

    screen.blit(bg_surf, (0, 0))
    
    if game.is_active:
        game.draw_bird()
        game.draw_pipes()
        game.detect_collision()
    else:
        game.draw_message()

    game.draw_floor()
    game.draw_score()
    pygame.display.update()
    clock.tick(60)
    