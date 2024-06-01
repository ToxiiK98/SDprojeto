from typing import Union
from client.ui.Fairy import Fairy

# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
class GameMech:
    def __init__(self, nr_x:int, nr_y:int):
        self.nr_max_x = nr_x
        self.nr_max_y = nr_y
        self.players = dict()
        self.fairy = None  # Use None instead of an empty dict for a single fairy
        self.walls = dict()
        self.world = dict()
        for x in range(self.nr_max_x):
            for y in range(self.nr_max_y):
                self.world[(x,y)]=[]
        # Número de jogadores
        self.nr_players = 0
        # Posição dos jogadores (assumo que as posições são menores que o número máximo de quadrículas)
        self.pos_players = [(5,5),(2,2),(1,1)]
        # Número de paredes
        self.nr_walls = 0
        # new: set walls around
        self.add_wall_around()

    def get_nr_x(self) -> int:
        return self.nr_max_x

    def get_nr_y(self) -> int:
        return self.nr_max_y

    def is_wall(self,objects)->bool:
        for obj in objects:
            if obj[0] =="wall" and obj[1]=="wall":
                return True
        return False

    def add_wall(self, x:int, y:int) -> bool:
        # If there is no all or ...

        if not self.is_wall(self.world[(x,y)]):
            self.walls[self.nr_walls]=["wall",(x,y)]
            self.world[(x,y)].append(["obst","wall",self.nr_walls])
            self.nr_walls += 1
            return True
        return False

    def get_walls(self) -> dict:
        return self.walls

    def add_wall_around(self) -> bool:
        """
        Adiciona obstáculos à volta do mundo
        :ret          self.world([2,2]).append(["obst","wall",self.nr_walls])
            self.nr_walls += 1
  urn: Retorna um booleano confirmando o sucesso da operação
        """
        for x in range(0,self.nr_max_x):
            for y in range(0,self.nr_max_y):
                if x in (0,self.nr_max_x - 1) or y in (0, self.nr_max_y - 1):
                    self.walls[self.nr_walls]=["wall",(x,y)]
                    self.world[(x,y)].append(["obst","wall",self.nr_walls])
                    self.nr_walls += 1
        return True

    def add_player(self, name:str) -> tuple:
        """
        Adiciona um jogador e retorna o seu número e a sua posição
        :param name: Nome do jogador
        :return: Retorna um túpulo com o número e posição do jogador com o formato (nr,(x,y))
        """
        self.players[self.nr_players] =[name,self.pos_players[self.nr_players]]
        self.world[self.pos_players[self.nr_players]].append(["player",name,self.nr_players])
        self.nr_players += 1
        return (self.nr_players - 1,self.pos_players[self.nr_players - 1])

    def move_to(self,pos:tuple, dir:int) -> tuple:
        if dir == UP:
            new_pos = (pos[0],pos[1]-1)
        elif dir == DOWN:
            new_pos = (pos[0],pos[1]+1)
        elif dir == LEFT:
            new_pos = (pos[0] - 1,pos[1])
        elif dir == RIGHT:
            new_pos = (pos[0] + 1,pos[1])
        return new_pos

    def obstacle_in_pos(self, pos:tuple)-> bool:
        objects = self.world[pos]
        for obj in objects:
            if obj[0] == "obst":
                return True
        return False

    def execute(self,nr_player:int, dir:int) -> tuple:
        # ALTERAR A POSICAO DO PLAYER
        #  -- ir buscar a posicao anterior
        pos = self.players[nr_player][1]
        name = self.players[nr_player][0]
        #  -- nova posição
        new_pos = self.move_to(pos, dir)
        #  -- verificar se se pode mover na direção desejada.
        if self.obstacle_in_pos(new_pos):
            new_pos = pos
        #  -- acrescentar ao dicionário players
        self.players[nr_player] = [name,new_pos]
        #  -- mudar o mundo
        self.world[pos].remove(["player",name,nr_player])
        self.world[new_pos].append(["player",name,nr_player])
        return new_pos

    def add_fairy(self, x: int, y: int):
        self.fairy = Fairy(self, x, y,20)  # Pass 'self' as the first argument
        self.world[(x, y)].append(["fairy"])

    def get_fairy_position(self) -> Union[tuple, None]:
        if self.fairy:
            return (self.fairy.rect.x, self.fairy.rect.y)
        return None


def main():
    gm = GameMech(10,10)
    print(gm.world[(0,2)])
    j1 = gm.add_player("PEDRO")
    j2 = gm.add_player("TOXIIK")

    gm.execute(j1[0],DOWN)
    print("Jogador 0:",gm.players[0])
    print("Posição (5,5):",gm.world[(5,5)])
    print("Posição (5,6):",gm.world[(5,6)])
    # Add a fairy and check its position
    #gm.add_fairy(3, 3)
    print("Posição da fada:", gm.get_fairy_position())

if __name__ == '__main__':
    main()