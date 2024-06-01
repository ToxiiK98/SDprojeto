from server.server_impl.gamemech import GameMech
from server.skeleton.server_skeleton import GameServerSkeleton
from server.server_impl import NR_QUAD_X, NR_QUAD_Y


def main():
    gamemech = GameMech(NR_QUAD_X, NR_QUAD_Y)
    skeleton =  GameServerSkeleton(gamemech)
    skeleton.run()

if __name__=="__main__":
    main()
