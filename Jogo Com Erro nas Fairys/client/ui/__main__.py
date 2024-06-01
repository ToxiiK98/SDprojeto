import pygame
from client.stub.client_stub import ClientStub
from client.ui.game import Game
from client.stub import SQUARE_SIZE, PORT, SERVER_ADDRESS

def main():
    pygame.init()
    cs = ClientStub(SERVER_ADDRESS, PORT)
    game = Game(cs, SQUARE_SIZE)
    game.run()

if __name__ == '__main__':
    main()