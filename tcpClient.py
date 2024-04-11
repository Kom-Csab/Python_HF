import socket
import logging

class tcpClient:
    def __init__(self, host, port, logs = "clientlogs/general.txt"):
        self.__clSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__logs = logs
        self.__myLogger = self.__setup_logger("tcp_client_logger", self.__logs)
    
    def connect(self):
        try:    
            self.__clSocket.connect((self.__host, self.__port))
            print("Csatlakozva az adatbázis-szerverhez!\n")
            self.__myLogger.info(f"Csatlakozva a szerverhez: {self.__host}:{self.__port}")
        except Exception as ex:
            print(f"Csatlakozási hiba, keresse fel a szolgáltatót! {ex}")
            self.__myLogger.critical(f"Hiba csatlakozas kozben! Hibakod: {ex}")
            return False
        return True
            
    def send_data(self, data):
        try:
            message = "#" + str(data)
            self.__clSocket.sendall(message.encode())
            response = self.__clSocket.recv(1024).decode()
            print(f"\nA kiszolgáló válasza: {response}\n")
            self.__myLogger.info("Adatok elkuldve a szervernek!")
        except Exception as e:
            print(f"Küldés közben hiba lépett fel! {e}")
            self.__myLogger.critical(f"Hiba kuldes kozben! Elkuldott adat: {data}")

    def fetch_records(self, index = 0):
        try:
            input = str(index)
            if input.isdigit():
                message = input + "#FETCH"
                self.__clSocket.sendall(message.encode())
                response = self.__clSocket.recv(1024).decode()
                if response == "Empty" and index <= 0:
                    print(f"Az adatbázis nem tartalmaz rekordot ilyen azonosítóval: {index}.")
                    self.__myLogger.info(f"Nincs megfelelo adat! Azonosito: {index}")
                else:
                    records = response.split("\n")
                    print("Adatbázisban lévő rekordok:")
                    for record in records:
                        print(record)
            else:
                print("Ez nem egy szám, bro!")
                self.__myLogger.critical(f"Megadott index nem egy szam! Index: {index}")
        except Exception as e:
            print(f"Hiba a lekérdezés során! {e}")
            self.__myLogger.critical(f"Hiba lepett fel az adatok feldolgozasa kozben! Hiba leiras: {e}")

    def __setup_logger(self, name, logs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(logs)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
    
    def close(self):
        self.__clSocket.close()
        self.__myLogger.info("A kapcsolat lezarult a szerverrel!")
        
if __name__ == "__main__":
    cl = tcpClient("127.0.0.1", 53435)
    if cl.connect():
        # cl.main()
        cl.fetch_records()
        cl.send_data("Teszt üzenet")
        cl.fetch_records(3)
        cl.fetch_records()
        cl.send_data("\q")
        cl.close()