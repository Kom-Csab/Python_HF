import socket

class tcpClient:
    def __init__(self, host, port):
        self.__clSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
    
    def connect(self):
        try:    
            self.__clSocket.connect((self.__host, self.__port))
            print("Csatlakozva az adatbázis-szerverhez!\n")
        except Exception as ex:
            print(f"Csatlakozási hiba, keresse fel a szolgáltatót! {ex}")
            return False
        return True
            
    def send_data(self, data):
        try:
            self.__clSocket.sendall(data.encode())
            response = self.__clSocket.recv(1024).decode()
            print(f"\nA kiszolgáló válasza: {response}\n")
        except Exception as e:
            print(f"Küldés közben hiba lépett fel! {e}")

    def fetch_records(self):
        try:
            self.__clSocket.sendall(b"FETCH")
            response = self.__clSocket.recv(1024).decode()
            if response == "Az adatbázis jelenleg üres!":
                print("Az adatbázis nem tartalmaz adatrekordot. Töltsön fel adatot!")
            else:
                records = response.split("\n")
                print("Adatbázisban lévő rekordok:")
                for record in records:
                    print(record)
        except Exception as e:
            print(f"Hiba a lekérdezés során! {e}")
            
    #Lehessen választani, hogy küldeni akarok adatot, vagy lekérdezni
    #amíg le nem akarom zárni a kapcsolatot            
    # def main(self):
    #     closed = False
    #     while not closed:
            
    def close(self):
        self.__clSocket.close()
        
if __name__ == "__main__":
    cl = tcpClient("127.0.0.1", 53435)
    if cl.connect():
        # cl.main()
        cl.fetch_records()
        cl.send_data("Teszt üzenet")
        cl.fetch_records()
        cl.send_data("\q")
        cl.close()