from typing import Any
import pygame
from random import choice, randint



class BG(pygame.sprite.Sprite):
  def __init__(self, groups, scale_factor):
    super().__init__(groups)
    bg = pygame.image.load("background1.png")
    scaled_bg= pygame.transform.scale(bg, (bg.get_width() * scale_factor, bg.get_height() * scale_factor))
    self.surf = pygame.surface.Surface((bg.get_width() * scale_factor * 2, 700))
    self.surf.blit(scaled_bg, (0, 0))
    self.surf.blit(scaled_bg, (bg.get_width() * scale_factor, 0))

    self.image = self.surf
    self.rect = self.image.get_rect(topleft = (0, 0))

  def update(self):
    if self.rect.centerx <= 0:
      self.rect.x = 0
    self.rect.x -= 2

class Ground(pygame.sprite.Sprite):
  def __init__(self, groups, scale_factor):
    super().__init__(groups)     
    self.sprite_type = "ground"
    ground = pygame.image.load("ground1.png").convert_alpha()
    self.image = pygame.transform.scale(ground, pygame.math.Vector2(ground.get_size()) * scale_factor)
    self.rect = self.image.get_rect(bottomleft = (0, 700))
    self.mask = pygame.mask.from_surface(self.image)

  def update(self):
    if self.rect.centerx <= 0:
      self.rect.x = 0    
    self.rect.x -= 2.5

class Plane(pygame.sprite.Sprite):
  def __init__(self, groups, scale_factor):
    super().__init__(groups)
    self.impurt_plane(scale_factor)    
    self.index = 0
    self.image = self.frames[self.index]
    self.rect = self.image.get_rect(midleft = (20, 350))

    self.gravity = 0
    self.mask = pygame.mask.from_surface(self.image)

  def impurt_plane(self, scale_factore):
    self.frames = []  
    for i in range(3):
      image = pygame.image.load(f"red{i}.png").convert_alpha()
      scaled_image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * (scale_factore / 1.5))
      self.frames.append(scaled_image)

  def animate_plane(self):
    self.index += 0.1
    if self.index >= len(self.frames): self.index = 0
    self.image = self.frames[int(self.index)]    

  def move_plane(self):
    self.gravity += 0.2
    self.rect.y += self.gravity  

  def jump(self):
    self.gravity = -8

  def rotate_plane(self):
    self.image = pygame.transform.rotozoom(self.image, -self.gravity + 5, 1)

  def update(self):
    self.animate_plane()  
    self.move_plane()
    self.rotate_plane()

class Obsticale(pygame.sprite.Sprite):
  def __init__(self, groups, scale_factor):
    super().__init__(groups)
    
    self.orientation = choice(["up", "down"])
    self.sprite_type = "obsticale"

    image = pygame.image.load(f"{choice([0, 1])}.png").convert_alpha()
    scaled_image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * scale_factor)
    self.image = scaled_image

    x_pos = randint(520, 560)
  
    if self.orientation == "up":
      self.rect = self.image.get_rect(midbottom = (x_pos, randint(710, 760)))
    else:
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect = self.image.get_rect(midtop = (x_pos, randint(-60, -10)))

    self.mask = pygame.mask.from_surface(self.image)

  def update(self):
    self.rect.x -= 3
    if self.rect.right <= -50:
      self.kill()
