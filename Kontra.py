import pygame
from pygame import mixer 
import os
import random
import csv
import button

mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('kontra')

# frame rate
clock = pygame.time.Clock()
FPS = 60

# define variabel game 
GRAVITY = 0.75
SCROLL_TRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

# variabel aksi
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False


#load musik dan Sound
pygame.mixer.music.load('aset game/audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('aset game/audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('aset game/audio/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('aset game/audio/grenade.wav')
grenade_fx.set_volume(0.05)

# load image
# button image
start_img = pygame.image.load('aset game/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('aset game/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('aset game/img/restart_btn.png').convert_alpha()
# background image
pine1_img = pygame.image.load('aset game/img/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('aset game/img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('aset game/img/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('aset game/img/background/sky_cloud.png').convert_alpha()
#menyimpan tile gambar dalam list
img_list = [] 
for x in range(TILE_TYPES):  
    img = pygame.image.load(f'aset game/img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# peluru
bullet_img = pygame.image.load('aset game/img/icons/bullet.png').convert_alpha()
#bom
grenade_img = pygame.image.load('aset game/img/icons/grenade.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('aset game/img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('aset game/img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('aset game/img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'health'  : health_box_img,
    'ammo'    : ammo_box_img,
    'grenade'  : grenade_box_img
}
#def color
BG = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0 ,0 , 0)
GREEN = (0 , 255, 0)
PINK = (235, 65, 54)

#def font
font = pygame.font.SysFont('futura', 30)


def draw_text(text,font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.9, SCREEN_HEIGHT - pine2_img.get_height()))

#fungsi untuk reset level
def reset_level():
    musuh_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    
    #membuat list tile kosong
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

class Tentara(pygame.sprite.Sprite):
    def __init__(seLf, char_type ,x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(seLf)
        seLf.alive = True
        seLf.char_type = char_type
        seLf.speed = speed
        seLf.ammo = ammo
        seLf.start_ammo = ammo
        seLf.shoot_cooldown = 0
        seLf.grenades = grenades
        seLf.health = 100
        seLf.max_health = seLf.health
        seLf.arah = 1
        seLf.vel_y = 0
        seLf.jump = False
        seLf.in_air = True
        seLf.flip = False
        seLf.arah = 1
        seLf.move_counter = 0
        seLf.animation_list = []
        seLf.frame_index = 0
        seLf.action = 0
        seLf.update_time = pygame.time.get_ticks()
        #spesifik veriabel ai
        seLf.move_counter = 0
        seLf.vision = pygame.Rect(0, 0, 150, 20)
        seLf.idling = False
        seLf.idling_counter = 0
        
   
        
        # === LOADING ANIMASI ===
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'aset game/img/{seLf.char_type}/{animation}'))
            
            for i in range(num_of_frames):
                img = pygame.image.load(f'aset game/img/{seLf.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
        
            seLf.animation_list.append(temp_list)
        
        seLf.image = seLf.animation_list[seLf.action][seLf.frame_index]
        seLf.rect = seLf.image.get_rect()
        seLf.rect.center = (x, y)
        seLf.width = seLf.image.get_width()
        seLf.height = seLf.image.get_height()
        
    def update(seLf):
        seLf.update_animation()
        seLf.check_alive()
        # === PERBAIKAN COOLDOWN COOLDOWN ===
        # Kurangi 1 per frame agar jeda 20 frame terasa nyata (~0.3 detik)
        if seLf.shoot_cooldown > 0:
            seLf.shoot_cooldown -= 1    
        
    def gerak(seLf, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0
        
        if moving_left:
            dx = -seLf.speed
            seLf.flip = True
            seLf.arah = -1
        if moving_right:
            dx = seLf.speed
            seLf.flip = False
            seLf.arah = 1
            
        if seLf.jump == True and seLf.in_air == False:
            seLf.vel_y = -13
            seLf.jump = False
            seLf.in_air = True
            
        seLf.vel_y += GRAVITY
        if seLf.vel_y > 10:
            seLf.vel_y = 10
        dy += seLf.vel_y
        
        #cek untuk tanah 
        for tile in world.obstacle_list:
            #chekk untuk collision di sumbu x
            if tile[1].colliderect(seLf.rect.x + dx, seLf.rect.y, seLf.rect.width, seLf.rect.height):
                dx = 0
                
                if seLf.char_type == 'enemy':
                    seLf.arah *= -1
                    seLf.move_counter = 0
            #chekk untuk collision di sumbu y
            if tile[1].colliderect(seLf.rect.x, seLf.rect.y + dy, seLf.rect.width, seLf.rect.height):
                    #chek if collision di bawah
                if seLf.vel_y < 0:
                    seLf.vel_y = 0
                    dy = tile[1].bottom - seLf.rect.top
                #chek if above the ground, i.e. falling
                elif seLf.vel_y >= 0:
                    seLf.vel_y = 0
                    seLf.in_air = False
                    dy = tile[1].top - seLf.rect.bottom
                    
                    
        #mengecek untuk air
        if pygame.sprite.spritecollide(seLf, water_group, False):
            seLf.health = 0
            
        #mengecek jika jatuh dari map
        level_complete = False
        if seLf.rect.bottom > SCREEN_HEIGHT:
            seLf.health = 0
            
        #mengecek untuk exit
        if pygame.sprite.spritecollide(seLf, exit_group, False):
            level_complete = True
            
        #cek untuk keluar dari layar
        if seLf.char_type == 'player': 
            if seLf.rect.left + dx < 0 or seLf.rect.right + dx > SCREEN_WIDTH:
                dx = 0  
        
        #update posisi karakter
        seLf.rect.x += dx
        seLf.rect.y += dy   
        
        #update scroll berdasarkan posisi karakter
        #update scroll berdasarkan posisi karakter
        if seLf.char_type == 'player':
           if (seLf.rect.right > SCREEN_WIDTH - SCROLL_TRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
              or (seLf.rect.left < SCROLL_TRESH and bg_scroll > abs(dx)):
               seLf.rect.x -= dx
               screen_scroll = -dx
                
        return screen_scroll, level_complete
        
    def shoot_bullet(seLf):  
        # === PERBAIKAN LOGIKA TEMBAK ===
        if seLf.shoot_cooldown == 0 and seLf.ammo > 0:
            seLf.shoot_cooldown = 20  # Jeda antar peluru (20 frame)
            seLf.ammo -= 1
            shot_fx.play()
            
            # Sekarang pembuatan objek peluru dimasukkan ke dalam IF statement ini
            bullet = Bullet(seLf.rect.centerx + (0.5 * seLf.rect.size[0] * seLf.arah),
            seLf.rect.centery,
            seLf.arah,seLf
            )
            bullet_group.add(bullet)
            
            
            # Print status ke terminal untuk cek sisa amunisi
            print(f"Peluru tersisa: {seLf.ammo}")
        
    def ai(self):
       if self.alive and player.alive:

        if self.idling == False and random.randint(1, 200) == 1:
            self.update_action(0)  # idle
            self.idling = True
            self.idling_counter = 50
        #cek untuk bagian if ai in near n plyer
        if self.vision.colliderect(player.rect):
            if player.rect.centerx > self.rect.centerx:
                self.arah = 1
                self.flip = False
            else:
                self.arah = -1
                self.flip = True
            self.update_action(0)
            self.shoot_bullet()
        else:
            if self.idling:
                self.idling_counter -= 1
            
                if self.idling_counter <= 0:
                    self.idling = False

            if self.arah == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False

            ai_moving_left = not ai_moving_right

            self.gerak(ai_moving_left, ai_moving_right)
            self.update_action(1)  # run
            self.move_counter += 1
            #update ai vision musuh
            self.vision.center = (self.rect.centerx + 75 * self.arah, self.rect.centery)
            

            if self.move_counter > TILE_SIZE:
                self.arah *= -1
                self.move_counter *= -1
            else:
                if self.idling:
                    self.idling_counter -= 1

                    if self.idling_counter <= 0:
                        self.idling = False
                
        self.rect.x += screen_scroll
        

            
    def update_animation(seLf):
        Animation_cooldown = 100
        if pygame.time.get_ticks() - seLf.update_time > Animation_cooldown:
            seLf.update_time = pygame.time.get_ticks()
            seLf.frame_index += 1 
            
        if seLf.frame_index >= len(seLf.animation_list[seLf.action]):
            if seLf.action == 3:
                seLf.kill()
                return
            else:
                seLf.frame_index = 0
            
        seLf.image = seLf.animation_list[seLf.action][seLf.frame_index]
        
    def update_action(seLf, new_action):
        if new_action != seLf.action:
            seLf.action = new_action
            seLf.frame_index = 0
            seLf.update_time = pygame.time.get_ticks()
            
    def check_alive(seLf):
        if seLf.health <= 0:
            seLf.health = 0
            seLf.speed = 0
            if seLf.alive:
                seLf.alive = False
                seLf.update_action(3) #mati  
        
    def draw(seLf):
        screen.blit(pygame.transform.flip(seLf.image, seLf.flip, False), seLf.rect)
        pygame
        
class World():
    def __init__(seLf):
        seLf.obstacle_list = []
        
    def process_data(seLf, data):
        seLf.level_length = len(data[0])
        #mengulang setiap nilai dalam data level untuk membuat dunia
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        seLf.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15: #player
                        player = Tentara('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 3, 10, 5)
                        health_bar = HealthBar(10,10, player.health , player.health)
                    elif tile == 16: #musuh
                        musuh = Tentara('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 10, 0)
                        musuh_group.add(musuh)
                    elif tile == 17: #membuat amunisi
                        item_box = itemBox('ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18: #membuat granat
                        item_box = itemBox('grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19: #membuat health
                        item_box = itemBox('health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20: #membuat exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                        
        return player, health_bar
                        
                        
    def draw(seLf):
        for tile in seLf.obstacle_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])
            
class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        def update(self):
            self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll
            
class Decoration(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
            
        def update(self):
            self.rect.x += screen_scroll

class itemBox(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.item_type = item_type
            self.image = item_boxes[self.item_type]
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll
            #cek player ambil box
            if pygame.sprite.collide_rect(self, player):
                #cek
                if self.item_type == 'health' :
                    print(player.health)
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                    print(player.health)
                elif self.item_type == 'ammo' :
                    player.ammo += 15
                elif self.item_type == 'grenade':
                    player.grenades += 3
                #hapus item box
                self.kill()

class HealthBar():
    def __init__(self,x ,y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        
    def draw(self, health):
        #update darah baru
        self.health = health
        #rasio darah
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x -2, self.y - 2, 150,20))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20 ))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20 ))
        
        

class Bullet(pygame.sprite.Sprite):
    def __init__(seLf, x, y, arah, owner):
        pygame.sprite.Sprite.__init__(seLf)
        seLf.speed = 10
        seLf.image = bullet_img      
        seLf.rect = seLf.image.get_rect()
        seLf.rect.center = (x, y)
        seLf.arah = arah    
        seLf.owner = owner
        
    def update(seLf):
        seLf.rect.x += (seLf.arah * seLf.speed) + screen_scroll
        if seLf.rect.right < 0 or seLf.rect.left > SCREEN_WIDTH:
            seLf.kill()   
        for tile in world.obstacle_list:
            if tile[1].colliderect(seLf.rect):
                seLf.kill()
                
            
        #check collision dengan karakter
        if seLf.owner != player and seLf.rect.colliderect(player.rect):
            if player.alive:
                player.health -= 10
                seLf.kill()
        if seLf.owner.char_type == 'player':
            for musuh in musuh_group:
                if seLf.owner != musuh and seLf.rect.colliderect(musuh.rect):
                    if musuh.alive:
                        musuh.health -= 25
                        seLf.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(seLf, x, y, arah):
        pygame.sprite.Sprite.__init__(seLf)
        seLf.timer= 100
        seLf.vel_y = -11
        seLf.speed = 6
        seLf.image = grenade_img      
        seLf.rect = seLf.image.get_rect()
        seLf.rect.center = (x, y)
        seLf.width = seLf.image.get_width()
        seLf.height = seLf.image.get_height()
        seLf.arah = arah
        
    def update(seLf):
        seLf.vel_y += GRAVITY
        dx = seLf.arah * seLf.speed
        dy = seLf.vel_y
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(seLf.rect.x + dx, seLf.rect.y, seLf.rect.width, seLf.rect.height):
                seLf.arah *= -1
                dx = seLf.arah * seLf.speed
        
            if tile[1].colliderect(seLf.rect.x, seLf.rect.y + dy, seLf.rect.width, seLf.rect.height):
                seLf.speed = 0
                if seLf.vel_y < 0:
                    seLf.vel_y = 0
                    dy = tile[1].bottom - seLf.rect.top
                elif seLf.vel_y >= 0:
                    seLf.vel_y = 0
                    dy = tile[1].top - seLf.rect.bottom
            
    
            
        seLf.rect.x += dx + screen_scroll
        seLf.rect.y += dy
        
        #timer bom
        seLf.timer -= 1
        if seLf.timer <= 0:
            seLf.kill()
            grenade_fx.play()
            explosion = Explosion(seLf.rect.x, seLf.rect.y, 0.5)
            explosion_group.add(explosion)
            #damage area
            if abs(seLf.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(seLf.rect.centery - player.rect.centery) < TILE_SIZE * 2 :
                    player.health -= 50
            for musuh in musuh_group :       
             if abs(seLf.rect.centerx - musuh.rect.centerx) < TILE_SIZE * 2 and \
                abs(seLf.rect.centery - musuh.rect.centery) < TILE_SIZE * 2 :
                    musuh.health -= 100

class Explosion(pygame.sprite.Sprite):
    def __init__(seLf, x, y, scale):
        pygame.sprite.Sprite.__init__(seLf)
        seLf.images = []
        for num in range(1, 6):
             img = pygame.image.load(f'aset game/img/explosion/exp{num}.png').convert_alpha() 
             img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) 
             seLf.images.append(img)
        seLf.frame_index = 0
        seLf.image = seLf.images[seLf.frame_index]
        seLf.rect = seLf.image.get_rect()
        seLf.rect.center = (x, y)
        seLf.counter = 0
        
        
    def update(seLf):
        seLf.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        #update animasi ledakan
        seLf.counter += 1
        
        if seLf.counter >= EXPLOSION_SPEED:
            seLf.counter = 0
            seLf.frame_index +=1
            #jika animasi selesai lalu hapus
            if seLf.frame_index >= len(seLf.images):
                seLf.kill()
            else: 
                seLf.image = seLf.images[seLf.frame_index]
        
        
class screenFade():
    def __init__(Self,arah, colour, speed):
        Self.arah = arah
        Self.colour = colour
        Self.speed = speed
        Self.fade_counter = 0 
        
    def fade(Self):
        fade_complete = False
        Self.fade_counter += Self.speed
        if Self.arah == 1:#whole screen fade
            pygame.draw.rect(screen, Self.colour,  (0 - Self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, Self.colour, (SCREEN_WIDTH // 2 + Self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, Self.colour, (0, 0 - Self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, Self.colour, (0, SCREEN_HEIGHT // 2  + Self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if Self.arah == 2:#vertikal layar fade down
            pygame.draw.rect(screen, Self.colour, (0, 0, SCREEN_WIDTH, 0 + Self.fade_counter))
        if Self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
            
        return fade_complete
    

#membuat layar fades
intro_fade = screenFade(1, BLACK, 4)
death_fade = screenFade(2, PINK, 4)

# membuat tombol
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)
        
# membuat grup sprite 
musuh_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()  


#membuat list tile kosong
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
    
#load level data and create world
with open(f'aset game/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)


            
run = True
while run:
    
    clock.tick(FPS)
    
    if start_game == False:
        #draw menu
        screen.fill(BG)
        #menamambah tombol
        if start_button.draw(screen):
            start_game = True
            start_intro = False
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()
        #tampil darah player
        health_bar.draw(player.health)
        #tmpil ammo
        draw_text('AMMO : ', font, BLACK,10 ,30)
        for x in range(player.ammo) :
            screen.blit(bullet_img , ( 90 + (x * 10), 40))
        #tmpil granad
        draw_text('GRENADES : ', font, BLACK,10 ,60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))
        
        
        player.update()
        player.draw()
        
        for musuh in musuh_group:
            musuh.ai()
            musuh.update()
            musuh.draw()
        
        
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        
        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0
        
        if player.alive:
            if shoot:
                player.shoot_bullet() 
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.arah), player.rect.top, player.arah)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
                print(player.grenades)
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.gerak(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #mengecek jika level selesai
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                #reset level
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load level data dan buat dunia
                    with open(f'aset game/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            if death_fade.fade():
             if restart_button.draw(screen):
                 death_fade.fade_counter = 0
                 start_intro = True
                 bg_scroll = 0
                 world_data = reset_level()
                 #load level data and create world
                 with open(f'aset game/level{level}_data.csv', newline='') as csvfile:
                     reader = csv.reader(csvfile, delimiter=',')
                     for x, row in enumerate(reader):
                         for y, tile in enumerate(row):
                             world_data[x][y] = int(tile)
                 world = World()
                 player, health_bar = world.process_data(world_data) 
                
            
            
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                 player.jump = True
                 jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
                
    
    pygame.display.update()
            
pygame.quit()
