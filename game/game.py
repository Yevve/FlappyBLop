import pygame,sys,random
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos+576,900))

def create_pipe():
    random_pipe_hight= random.choice(pipe_hight)
    buttom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_hight))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_hight-340))
    return buttom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes

def draw_pipes(pipes):

    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <=-100 or bird_rect.bottom >=900:
        return False   
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movment,1)
    return new_bird

def score_display(game_state):
    if game_state == 'Main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'Game_over':
        score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()

screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

#Game Var
gravity=0.25
bird_movment=0
game_active= True
score=0
high_score=0

bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
#Floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos=0
#Bird
bird_surface = pygame.image.load('assets/Blop.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect=bird_surface.get_rect(center=(100,512))
#Pipe
pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_hight=[400,500,600]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movment = 0
                bird_movment -=8
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movment = 0
                score = 0
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0))

    if game_active:
        #Bird
        bird_movment +=gravity
        rotated_bird= rotate_bird(bird_surface)
        bird_rect.centery +=bird_movment
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #Pipes
        pipe_list= move_pipe(pipe_list)
        draw_pipes(pipe_list)


        score +=0.005
        score_display('Main_game')
    else:
        high_score = update_score(score,high_score)
        score_display('Game_over')


    #Floor
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos=0
    

    pygame.display.update()
    clock.tick(120)


