import numpy
from middleware.socket_impl.sockets import Socket
import client.stub as client


class ClientStub:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self.socket = Socket.create_client_connection(self._host, self._port)

    def get_nr_quad_x(self) -> int:
        self.socket.send_str(client.QUADX_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def get_nr_quad_y(self) -> int:
        self.socket.send_str(client.QUADY_OP)
        return self.socket.receive_int(client.INT_SIZE)

    #new - protocol for setting player and receiving id
    def set_player(self, name: str) -> tuple:
        self.socket.send_str(client.PLAYER_OP)
        self.socket.send_str(name)
        # It will receive a tuple
        return self.socket.receive_obj(client.INT_SIZE)

    # new - protocol for updating position
    def execute(self, id: int, dir: int) -> tuple:
        self.socket.send_str(client.UPDATE_OP)
        self.socket.send_int(id, client.INT_SIZE)
        self.socket.send_int(dir, client.INT_SIZE)
        # It will receive a tuple
        return self.socket.receive_obj(client.INT_SIZE)

    # new - protocol for getting walls
    def get_walls(self) -> dict:
        self.socket.send_str(client.GET_WALLS_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def exec_stop_client(self):
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self):
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()

    # Protocol for getting fairy position
    def get_fairy_position(self):
        self.socket.send_str(client.GET_FAIRY_POSITION_OP)
        position = self.socket.receive_obj(client.INT_SIZE)  # Ensure this matches the server's data format
        return position
