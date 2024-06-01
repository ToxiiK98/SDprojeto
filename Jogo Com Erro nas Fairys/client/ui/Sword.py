import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, size, damage):
        super().__init__()
        # Carrega a imagem da espada
        self.image = pygame.image.load('images/sword.png').convert_alpha()
        # Redimensiona a imagem para o tamanho da célula do grid
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = damage  # Define a quantidade de dano causada pela espada
