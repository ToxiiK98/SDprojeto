from threading import Thread
from server.server_impl.gamemech import GameMech
import logging
import server.server_impl as server
import numpy as np
import ast


class ClientThread(Thread):
    def __init__(self, gamemech: GameMech, current_connection, address):
        self.current_connection = current_connection
        self.gamemech = gamemech
        self.address = address
        Thread.__init__(self)

    # new
    def process_update(self):
        id = self.current_connection.receive_int(server.INT_SIZE)
        dir = self.current_connection.receive_int(server.INT_SIZE)
        res: tuple = self.gamemech.execute(id,dir)
        self.current_connection.send_obj(res, server.INT_SIZE)
    # new
    def process_add_player(self):
        name = self.current_connection.receive_str(server.MAX_STR_SIZE)
        res: tuple = self.gamemech.add_player(name)
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_nr_x_quad_value(self):
        nr_x_quad = self.gamemech.get_nr_x()
        self.current_connection.send_int(nr_x_quad, server.INT_SIZE)

    def process_nr_y_quad_value(self):
        nr_y_quad = self.gamemech.get_nr_y()
        self.current_connection.send_int(nr_y_quad, server.INT_SIZE)

    def process_get_walls(self):
        walls = self.gamemech.get_walls()
        self.current_connection.send_obj(walls,server.INT_SIZE)

    #def process_add(self) -> None:
    #    a = self.current_connection.receive_int(server.INT_SIZE)
    #    b = self.current_connection.receive_int(server.INT_SIZE)
    #    result = self.mathserver.add(a, b)
    #    self.current_connection.send_int(result, server.INT_SIZE)
#    result = self.mathserver.sym(a)
    #    self.current_connection.send_int(result, server.INT_SIZE)

    #def process_subtract(self) -> None:
    #    a = self.current_connection.receive_int(server.INT_SIZE)
    #    b = self.current_connection.receive_int(server.INT_SIZE)
    #    result = self.mathserver.subtract(a, b)
    #    self.current_connection.send_int(result, server.INT_SIZE)


    #def process_matrix_sum(self) -> None:
    #    a = self.current_connection.receive_obj(server.INT_SIZE)
    #    #print("VALOR A (soma matriz):",a)
    #    b = self.current_connection.receive_obj(server.INT_SIZE)
    #    #print("VALOR B (soma matriz):",b)
    #    result = self.mathserver.matrix_add(a,b)
    #    self.current_connection.send_obj(result,server.INT_SIZE)

    def dispatch_request(self) -> (bool, bool):
        """
        Calls process functions based on type of request.
        """
        request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
        print(request_type)
        keep_running = True
        last_request = False
        if request_type == server.UPDATE_OP:
            logging.info("Update operation requested "+str(self.address))
            self.process_update()

        elif request_type == server.QUADX_OP:
            logging.info("Ask for nr. x quad operation requested "+str(self.address))
            self.process_nr_x_quad_value()

        elif request_type == server.QUADY_OP:
            logging.info("Ask for nr. y quad operation requested "+str(self.address))
            self.process_nr_y_quad_value()
        #new
        elif request_type == server.PLAYER_OP:
            logging.info("Adding player "+str(self.address))
            print("add player")
            self.process_add_player()

        elif request_type == server.GET_WALLS_OP:
            logging.info("Asking for walls position:"+str(self.address))
            print("get walls")
            self.process_get_walls()




        #if request_type == server.ADD_OP:
        #    logging.info("Add operation requested "+str(self.address))
        #    self.process_add()
        #elif request_type == server.SYM_OP:
        #    logging.info("Symetric operation requested")
        #    self.process_sym()
        #elif request_type == server.SUB_OP:
        #    logging.info("Subtract operation requested")
        #    self.process_subtract()
        #elif request_type == server.MATRIX_OP:
        #    print("Received MATRIX_OP!")
        #    logging.info("Matrix Sum operation requested")
        #    self.process_matrix_sum()

        elif request_type == server.BYE_OP:
            last_request = True
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        return keep_running, last_request


    def run(self):
        # While client connected, wait for its demmands and dispatch the requests
        #with self.current_connection:
        last_request = False
        #If it is not the last request receive the request
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        #If it is the last request, client is disconnecting...
        logging.debug("Client " + str(self.current_connection.get_address()) + " disconnected")

