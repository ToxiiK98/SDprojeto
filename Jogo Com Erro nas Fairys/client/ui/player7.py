import pygame
from client.stub.client_stub import ClientStub
from client.stub import UP, DOWN, LEFT, RIGHT

# Player 7 is part of the test example 7
# It defines a sprite with size rate
class Player(pygame.sprite.DirtySprite):
    def __init__(self,nr_player:int, pos_x:int, pos_y:int, size:int, *groups ):
        super().__init__(*groups)
        self.my_id = nr_player
        self.size = size
        self.image = pygame.image.load('images/Gnome.png')
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * size ,pos_y * size), self.image.get_size())
        self.pos:list = [pos_x, pos_y]
        #Mecanicas de Jogo
        self.health = 5  # Vida do Jogador
        self.damage = 0  # Dano do jogador

    def get_size(self):
        return self.new_size

    # Já não definimos a velocidade. Eles irão deslocar-se todos à mesma velocidade...
    def update(self, game:object, cs: ClientStub ):
        last = self.rect.copy()
        key = pygame.key.get_pressed()
        new_pos = self.pos
        if key[pygame.K_LEFT]:
             # new
             new_pos = cs.execute(self.my_id,LEFT )
             self.rect.x = new_pos[0] * self.size
             self.rect.y = new_pos[1]* self.size
        if key[pygame.K_RIGHT]:
            # new
            new_pos = cs.execute(self.my_id,RIGHT )
            self.rect.x = new_pos[0]* self.size
            self.rect.y = new_pos[1]* self.size
        if key[pygame.K_UP]:
            # new
            new_pos = cs.execute(self.my_id,UP )
            self.rect.x = new_pos[0]* self.size
            self.rect.y = new_pos[1]* self.size
        if key[pygame.K_DOWN]:
            # new
            new_pos = cs.execute(self.my_id,DOWN )
            self.rect.x = new_pos[0]* self.size
            self.rect.y = new_pos[1]* self.size

        self.pos = new_pos

        # Keep visible
        self.dirty = 1