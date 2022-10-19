import pygame
from sys import exit
from random import randint , choice

class Player(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def anim_state(self):
        if self.rect.bottom < 300: # jump
            self.image = self.player_jump
        else: # walk
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index =0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.anim_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
        
        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def anim_state(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.frames): self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def update(self):
        self.anim_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    curr_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(f'Score: {curr_time}',False,'olivedrab4')
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return curr_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

# def obstacle_move(obstacle_list):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5
#             if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
#             else: screen.blit(fly_surf,obstacle_rect)
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#         return obstacle_list
#     else: return []

# def collision(player,obstacles):
#     if obstacles:
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect): return False
#     return True

# def player_anim():
#     global player_surf, player_index

#     if player_rect.bottom < 300: # jump
#         player_surf = player_jump
#     else: # walk
#         player_index += 0.1
#         if player_index >= len(player_walk): player_index =0
#         player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Learning PyGame')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
bgm = pygame.mixer.Sound('audio/music.wav')
bgm.set_volume(0.01)
bgm.play()

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#active game background
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#game over screen / intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2.5)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_title = test_font.render('Astro Runner',False,'black')
game_title_rect = game_title.get_rect(midtop = (400,50))

game_instruct = test_font.render('Press Space to Start',False,'black')
game_instruct_rect = game_instruct.get_rect(midbottom = (400,350))

#Timer
obstactle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstactle_timer,1500)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
             if event.type == obstactle_timer: 
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                game_active = True
                
                start_time = pygame.time.get_ticks() 

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        score = display_score()        

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
            
    else:
        screen.fill('#19A5AF')
        screen.blit(player_stand,player_stand_rect)        

        score_message = test_font.render(f'Your Score: {score}',False,'black')
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(game_title,game_title_rect)

        if score == 0: screen.blit(game_instruct,game_instruct_rect)
        else: screen.blit(score_message,score_message_rect)
        

    pygame.display.update()
    clock.tick(60)
