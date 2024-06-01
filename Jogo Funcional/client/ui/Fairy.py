import pygame


class Fairy(pygame.sprite.Sprite):
    def __init__(self, target, pos_x, pos_y, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load('images/Fairy.png')
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.target = target  # Referência ao jogador
        self.speed = 3  # Velocidade da fada

    def update(self):
        # Calcula o vetor de direção para o jogador
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = pygame.math.Vector2(dx, dy).length()

        # Move a fada na direção do jogador
        if distance > 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
