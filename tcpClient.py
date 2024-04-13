import socket
import logging

class tcpClient:
    def __init__(self, host, port, logs = "clientlogs/general.txt"):
        self.__clSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__logs = logs
        self.__myLogger = self.__setup_logger("tcp_client_logger", self.__logs)
        self.__commands = {
            1 : self.__send_data,
            2 : self.__fetch_records,
            3 : self.__close
        }
    
    def connect(self):
        try:    
            self.__clSocket.connect((self.__host, self.__port))
            print("Csatlakozva az adatbázis-szerverhez!")
            self.__myLogger.info(f"Csatlakozva a szerverhez: {self.__host}:{self.__port}")
        except Exception as ex:
            print(f"Csatlakozási hiba, keresse fel a szolgáltatót! {ex}")
            self.__myLogger.critical(f"Hiba csatlakozas kozben! Hibakod: {ex}")
            return False
        return True
            
    def menu(self):
        is_finished = 0
        while not is_finished:
            try:
                self.__print_functions()
                choice = int(input("Kérem válasszon az alábbi opciók közül! "))
                if choice in self.__commands:
                    operation = self.__commands[choice]
                    operation()
                    if choice == 3:
                        is_finished = 1
            except Exception as ex:
                print("\nHelytelen választás, kérem próbálja újra!\n")
                self.__myLogger.error(f"Hiba a felhasznalo keresenek feldolgozas kozben! Hiba leirasa: {ex}")
                
            
    def __send_data(self):
        try:
            data = "#" + input("\nKérem adja meg, a letárolandó adatot! ")
            self.__clSocket.sendall(data.encode())
            response = self.__clSocket.recv(1024).decode()
            print(f"\nA kiszolgáló válasza: {response}\n")
            self.__myLogger.info("Adatok elkuldve a szervernek!")
        except Exception as e:
            print(f"Küldés közben hiba lépett fel! {e}")
            self.__myLogger.critical(f"Hiba kuldes kozben! Elkuldott adat: {data}")

    def __fetch_records(self):
        try:
            index = input("\nKérem adja meg, hányadik adatot kívánja megtekinteni! (0 esetén az összes rekordot megnézheti) ")
            if index.isdigit():
                message = index + "#FETCH"
                self.__clSocket.sendall(message.encode())
                response = self.__clSocket.recv(1024).decode()
                if response == "Empty":
                    print(f"\nAz adatbázis nem tartalmaz rekordot ilyen azonosítóval: {index}.")
                    self.__myLogger.info(f"Nincs megfelelo adat! Azonosito: {index}")
                else:
                    records = response.split("\n")
                    print("Adatbázisban lévő rekordok:")
                    for record in records:
                        print(record)
            else:
                print(f"A megadott index nem szám! Index: {index}")
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
    
    def __print_functions(self):
        print("\nLehetőségek:")
        print("1)\tAdatok küldése")
        print("2)\tAdat(ok) lekérdezése")
        print("3)\tKilépés\n")
    
    def __close(self):
        try:
            self.__clSocket.sendall(b"#\q")
            answer = self.__clSocket.recv(1024).decode()
            print(f"A kiszolgáló válasza: {answer}")
            self.__clSocket.close()
            self.__myLogger.info("A kapcsolat lezarult a szerverrel!")
        except Exception as ex:
            print(f"Hiba a kapcsolat lezárása közben! {ex}")
            self.__myLogger.critical(f"Hiba a kapcsolat lezárása közben! Hiba leírás: {ex}")
        
if __name__ == "__main__":
    cl = tcpClient("127.0.0.1", 53435)
    if cl.connect():
        cl.menu()