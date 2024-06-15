import pygame
import sys
from sprites import BG, Ground, Plane, Obsticale

class Game(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    pygame.init()
    self.screen = pygame.display.set_mode((480, 700))
    pygame.display.set_caption("Flappy Plane")
    self.clock = pygame.time.Clock()
    self.active = False
    self.score = 0
    self.start_timer = 0
    self.music = pygame.mixer.Sound("sounds/sounds_music.wav")
    self.music.set_volume(0.1)
    self.music.play(loops= -1)

    self.background_height = pygame.image.load("images/background1.png").get_height()
    self.scale_factor = 700 / self.background_height

    self.all_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()
    BG(self.all_sprites, self.scale_factor)
    Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
    if self.active:
      self.plane = Plane(self.all_sprites, self.scale_factor)
  
    self.obsticale_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(self.obsticale_timer, 1200)

    self.font = pygame.font.Font("font/Pixeltype.ttf", 60)
    self.ui_font = pygame.font.Font("font/Pixeltype.ttf", 40)
    self.menu_surf = pygame.image.load("images/menu.png")
    self.menu_surf = pygame.transform.scale(self.menu_surf, pygame.math.Vector2(self.menu_surf.get_size()) * (self.scale_factor / 1.4))
    self.menu_rect = self.menu_surf.get_rect(center = (240, 350))


  def collision(self):
    if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
        for sprite in self.collision_sprites.sprites():
          if sprite.sprite_type == "obsticale":
            sprite.kill()
        self.active = False
        self.plane.kill()

  def display_score(self):
    self.score_surf = self.font.render(f"{self.score}", False, "Black")
    self.score_rect = self.score_surf.get_rect(center = (240, 100))
    if self.active:
      self.score = int(pygame.time.get_ticks() / 1000 - self.start_timer)
    else:
      if self.score != 0:
        self.score_rect = self.score_surf.get_rect(center = (240, 450))
    self.screen.blit(self.score_surf, self.score_rect)

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          if self.active:
            self.plane.jump() 
            self.jump_sound = pygame.mixer.Sound("sounds/sounds_jump.wav") 
            self.jump_sound.set_volume(0.1)
            self.jump_sound.play()
          else:
            self.active = True
            self.plane = Plane(self.all_sprites, self.scale_factor)
            self.start_timer = pygame.time.get_ticks() / 1000
        if event.type == self.obsticale_timer and self.active:
          Obsticale([self.all_sprites, self.collision_sprites], self.scale_factor)

        

      self.screen.fill("Black")
      self.all_sprites.draw(self.screen)
      self.all_sprites.update()
      if self.active:
        self.collision()
      else:
        self.screen.blit(self.menu_surf, self.menu_rect)  
        if self.score == 0:
          self.instruction_surf = self.ui_font.render("Press space to start and jump", False, "black")
          self.instruction_rect = self.instruction_surf.get_rect(center = (240, 430))
          self.screen.blit(self.instruction_surf, self.instruction_rect)
      self.display_score()

      pygame.display.update()
      self.clock.tick(120)


if __name__ == "__main__":
  game = Game()
  game.run()