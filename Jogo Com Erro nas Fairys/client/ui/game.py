import pygame
import player7
import wall
from client.stub.client_stub import ClientStub
from Fairy import Fairy  # Importa a classe Fairy
from Sword import Sword  # Importa a classe Sword
import random

class Game(object):
    def __init__(self, cs: ClientStub, size: int):
        self.cs = cs
        self.id = ""
        nr_x = self.cs.get_nr_quad_x()
        nr_y = self.cs.get_nr_quad_y()
        self.width, self.height = nr_x * size, nr_y * size
        self.max_x, self.max_y = nr_x, nr_y
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gnomes- Guardians of the Mythic Realm")
        self.clock = pygame.time.Clock()
        self.grid_size = size
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.draw_grid(self.width, self.height, self.grid_size, (0, 0, 0))
        pygame.display.update()
        self.fairy_spawn_time = None
        self.orc_spawn_time = pygame.time.get_ticks()  # Inicia o temporizador para gerar o orc
        self.orcs = None
        self.sword_spawn_timer = pygame.time.get_ticks()  # Inicia o temporizador para gerar novas espadas
        self.fairy_spawn_timer = pygame.time.get_ticks()  # Inicia o temporizador para gerar nova fada
        self.fairies = pygame.sprite.GroupSingle()  # Initialize as an empty single sprite group
    def draw_grid(self, width: int, height: int, size: int, colour: tuple):
        """
        Desenha uma grelha na tela.
        """
        for pos in range(0, height, size):
            pygame.draw.line(self.screen, colour, (0, pos), (width, pos))
        for pos in range(0, width, size):
            pygame.draw.line(self.screen, colour, (pos, 0), (pos, height))

    def create_player(self, size: int) -> None:
        """
        Cria os jogadores e adiciona-os ao grupo de sprites.
        """
        self.players = pygame.sprite.LayeredDirty()
        name = input("What is your name?")
        (self.id, pos) = self.cs.set_player(name)
        print("Player ", name, " created with id: ", self.id)
        self.playerA = player7.Player(self.id, pos[0], pos[1], size, self.players)
        self.players.add(self.playerA)

    def create_walls(self, size: int):
        """
        Cria os obstáculos (paredes) ao redor do mundo.
        """
        self.walls = pygame.sprite.Group()
        walls: dict = self.cs.get_walls()
        for wl in walls.values():
            (x, y) = wl[1]
            w = wall.Wall(0, x, y, size, self.walls)
            self.walls.add(w)

    def create_swords(self):
        """
        Cria as espadas e as adiciona ao grupo de sprites.
        """
        self.swords = pygame.sprite.Group()
        for _ in range(5):  # Gera 5 espadas
            x = random.randint(0, self.width - self.grid_size)
            y = random.randint(0, self.height - self.grid_size)
            damage = 1  # Define o dano causado pela espada
            sword = Sword(x, y, self.grid_size, damage)
            self.swords.add(sword)

    def create_fairy(self):
        """
        Creates a new fairy and adds it to the sprite group.
        """
        fairy_position = self.cs.get_fairy_position()
        if fairy_position and fairy_position != (-1, -1):
            fairy = Fairy(self.playerA, fairy_position[0], fairy_position[1], 20)  # The fairy follows playerA
            self.fairies = pygame.sprite.GroupSingle(fairy)  # Initialize as a single sprite group
        else:
            self.fairies.empty()  # Ensure it's an empty group if no fairy is added

    def update_fairy_position(self):
        """
        Atualiza a posição da fada com base nos dados recebidos do servidor.
        """
        if not self.fairies:
            return
        fairy_position = self.cs.get_fairy_position()
        fairy = self.fairies.sprite
        fairy.rect.x = fairy_position[0]
        fairy.rect.y = fairy_position[1]

    def run(self):
        self.create_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.walls.update()
        self.create_player(self.grid_size)
        self.create_swords()  # Cria as espadas inicialmente
        self.create_fairy()  # Cria a fada inicialmente
        end = False
        while not end:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True

            self.screen.blit(self.background, (0, 0))
            self.draw_grid(self.width, self.height, self.grid_size, (0, 0, 0))

            self.players.update(self, self.cs)
            self.walls.draw(self.screen)
            print(f"Fairies type: {type(self.fairies)}")  # Add this line
            self.fairies.update()  # Ensure this is called correctly
            self.players.draw(self.screen)
            self.swords.draw(self.screen)
            pygame.display.update()

            # Verifica colisões entre o jogador e as espadas
            collisions = pygame.sprite.spritecollide(self.playerA, self.swords, True)
            for collision in collisions:
                self.playerA.damage += collision.damage
                print("O jogador apanhou uma espada! Damage:", self.playerA.damage)

            # Verifica colisões entre o jogador e a fada
            fairy_collision = pygame.sprite.spritecollide(self.playerA, self.fairies, False)
            if fairy_collision:
                if self.fairy_spawn_time is None:
                    self.fairy_spawn_time = pygame.time.get_ticks()
                    self.fairies.remove(self.fairies.sprites())
                    print("O jogador colidiu com a fada! A fada desapareceu.")
                elif pygame.time.get_ticks() - self.fairy_spawn_time >= 2000:
                    self.fairies.add(Fairy(self.playerA, 100, 100, 20))
                    self.fairy_spawn_time = None
                    print("A fada reapareceu.")
                    if self.playerA.damage >= 3:
                        self.playerA.damage -= 3
                        print("O jogador perdeu 3 pontos de dano ao tocar na fada! Damage atual:", self.playerA.damage)
                    elif self.playerA.damage < 3:
                        self.playerA.health -= 1
                        print("O jogador perdeu 1 ponto de vida ao tocar na fada! Health atual:", self.playerA.health)
                        if self.playerA.health < 0:
                            self.playerA.health = 0
                            print("O jogador perdeu! Game Over.")
                            end = True

            # Verifica se é hora de gerar novas espadas
            current_time = pygame.time.get_ticks()
            if current_time - self.sword_spawn_timer > 15000:
                self.create_swords()
                self.sword_spawn_timer = current_time

            # Verifica se é hora de gerar uma nova fada
            if current_time - self.fairy_spawn_timer > 10000:
                self.create_fairy()
                self.fairy_spawn_timer = current_time

            # Atualiza a posição da fada com base nos dados do servidor
            self.update_fairy_position()

            self.players.clear(self.screen, self.background)

        return

