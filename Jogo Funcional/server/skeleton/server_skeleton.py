import logging
import server.server_impl as server
from server.server_impl.gamemech import GameMech
from middleware.socket_impl.sockets import Socket
from server.server_impl import LOG_FILENAME, LOG_LEVEL, SERVER_ADDRESS, PORT
import client_server


# ---------------------------- iniciando classe --------------------------------
class GameServerSkeleton:
    def __init__(self, gamemech: GameMech) -> None:
        """
        Cria um cliente dado o servidor a ser utilizado
        """
        # Mantém informações sobre a execução do programa
        logging.basicConfig(filename=LOG_FILENAME,
                            level=LOG_LEVEL,
                            format='%(asctime)s (%(levelname)s): %(message)s')

        self.gamemech = gamemech

    # ------------------- execução do servidor -------------------------------------
    def run(self) -> None:
        """
        Executa o servidor até que o cliente envie uma ação de "terminar"
        """
        socket = None
        try:
            socket = Socket.create_server_connection(SERVER_ADDRESS, PORT)
        except OSError as e:
            logging.error(f"A porta {PORT} já está em uso: {e}")
            # Tenta outra porta se a atual estiver em uso
            nova_porta = PORT + 1
            try:
                socket = Socket.create_server_connection(SERVER_ADDRESS, nova_porta)
                logging.info(f"Alterado para nova porta {nova_porta}")
            except OSError as e:
                logging.critical(f"Falha ao vincular à nova porta {nova_porta}: {e}")
                return

        logging.info(f"Aguardando conexões de clientes na porta {socket.port}")
        keep_running = True

        try:
            # Enquanto keep_running, obtém conexões e então interage com o cliente conectado
            while keep_running:
                current_connection, address = socket.server_connect()
                logging.debug(f"Cliente {address} acabou de se conectar")
                client_server.ClientThread(self.gamemech, current_connection, address).start()
                # Com o cliente conectado, aguarda suas demandas e despacha as solicitações
                # with current_connection:
                #    last_request = False
                #    # Se não for a última solicitação, recebe a solicitação
                #    while not last_request:
                #        keep_running, last_request = self.dispatch_request()
                #    # Se for a última solicitação, o cliente está se desconectando...
                #    logging.debug("Cliente " + str(address) + " desconectou")
        except Exception as e:
            logging.error(f"Ocorreu um erro: {e}")
        finally:
            if socket:
                socket.close()
            logging.info("Servidor parado")


if __name__ == '__main__':
    gamemech = GameMech()  # Instancia o objeto de mecânica do jogo
    server_skeleton = GameServerSkeleton(gamemech)
    server_skeleton.run()
