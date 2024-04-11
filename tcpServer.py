import socket
import database_manager
import logging

class tcpServer:
    def __init__(self, host, port, logs = "serverlogs\general.txt"):
        self.__host = host
        self.__port = port
        self.__dbHandler = database_manager.databaseHandler()
        self.__logs = logs
        self.__myLogger = self.__setup_logger("tcp_server_logger", self.__logs)
        self.__srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__srvSocket.bind((self.__host, self.__port))
        
    def start(self):
        self.__srvSocket.listen()
        self.__myLogger.info(f"Szerver a kovetkezo cimen hallgatozik: {self.__host}:{self.__port}")
        while True:
            cl_socket, cl_addr = self.__srvSocket.accept()
            self.__myLogger.info(f"Uj kapcsolat errol a cimrol: {cl_addr[0]}:{cl_addr[1]}")
            self.__handle_client(cl_socket)
    
    def __handle_client(self, cl_socket):
        try:
            while True:
                incoming = cl_socket.recv(1024).decode().split("#")
                if incoming[1] == "FETCH":
                    records = self.__dbHandler._get_records(incoming[0])
                    if records == "Empty":
                        cl_socket.sendall("Empty".encode())
                        self.__myLogger.info("Adatlekerdezes tortent: az adatbazis jelenleg ures!")
                    else:
                        response = "\n".join(records)
                        cl_socket.sendall(response.encode())
                        self.__myLogger.info("Adatlekerdezes tortent: adatok elkuldve!")
                elif incoming[1] == "\q":
                    cl_socket.sendall("A kapcsolat lezárult az adatbázis-szerverrel.".encode())
                    self.__myLogger.info("A kliens lezarta a kapcsolatot!")
                    break
                else:
                    self.__dbHandler._save_to_db(incoming[1])
                    cl_socket.sendall(b"Sikeresen mentve!")
                    self.__myLogger.info("Ujabb adatrekord kerult az adatbazisba!")
        except Exception as ex:
            self.__myLogger.warning(f"Kliens-kezelesi hiba: {ex}")
        
    def __setup_logger(self, name, logs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(logs)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
        
    def __close(self):
        self.__srvSocket.close()
        
if __name__ == "__main__":
    srv = tcpServer("127.0.0.1", 53435)
    srv.start()