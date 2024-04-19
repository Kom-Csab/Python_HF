import logging
import database_manager

class reqHandler:
    def __init__(self, logs = "tcpServer/serverlogs/general.txt"):
        self.__logs = logs
        self.__myLogger = self.__setup_logger("tcp_requests_handler", self.__logs)  
        self.__dbManager = database_manager.databaseHandler()
        
    def _handle_fetch(self, cl_socket, index):
        try:
            records = self.__dbManager._get_records(index)
            if records == "Empty":
                cl_socket.sendall(b"Empty")
                self.__myLogger.info("Adatlekerdezes tortent: az adatbazis jelenleg ures!")
            else:
                response = "\n".join(records)
                cl_socket.sendall(response.encode())
                self.__myLogger.info("Adatlekerdezes tortent: adatok elkuldve!")
        except Exception as ex:
            self.__myLogger.critical(f"Hiba tortent lekerdezes kozben! Hiba leiras: {ex}")
            
    def _handle_save(self, cl_socket, data):
        try:
            self.__dbManager._save_to_db(data)
            cl_socket.sendall(b"Sikeresen mentve!")
            self.__myLogger.info("Ujabb adatrekord kerult az adatbazisba!")
        except Exception as ex:
            self.__myLogger.critical(f"Hiba az adatok mentese kozben! Hiba leiras: {ex}")
            
    def _handle_quit(self, cl_socket):
        cl_socket.sendall("A kapcsolat lezárult az adatbázis-szerverrel.".encode())
        self.__myLogger.info("A kliens lezarta a kapcsolatot!")
        
    def __setup_logger(self, name, logs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(logs)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger