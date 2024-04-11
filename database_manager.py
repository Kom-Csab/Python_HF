import sqlite3
import logging

class databaseHandler:
    def __init__(self, logs = "serverlogs\db.txt", dbName = "SQlite\data.db"):
        self.__logs = logs
        self.__dbName = dbName
        self.__myLogger = self.__setup_logger("databaseHandler_logger", self.__logs)
        
    def _get_records(self, index):
        try:
            conn = sqlite3.connect(self.__dbName)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS kliens_adatok (id INTEGER PRIMARY KEY, data TEXT)''')
            conn.commit()
            if int(index) <= 0:
                cursor.execute("SELECT * FROM kliens_adatok")
            else:
                cursor.execute("SELECT * FROM kliens_adatok WHERE id=?", (index))
            records = cursor.fetchall()
            data = self.__format_records(records)
            conn.close()
            return data
        except Exception as ex:
            self.__myLogger.warning(f"Hiba az adatok lekérése közben: {ex}")
            
    def _save_to_db(self, data):
        try:
            conn = sqlite3.connect(self.__dbName)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS kliens_adatok (id INTEGER PRIMARY KEY, data TEXT)''')
            cursor.execute("INSERT INTO kliens_adatok (data) VALUES (?)", (data,))
            conn.commit()
            conn.close()
        except Exception as ex:
            self.__myLogger.warning(f"Hiba az adatok mentése közben: {ex}")
            
    def __setup_logger(self, name, logs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(logs)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
    
    def __format_records(self, rawRecords):
        if rawRecords == []:
            return "Empty"
        else:
            printable_data = ""
            for record in rawRecords:
                stringRecord = f"{record[0]}.\t{record[1]}\n"
                printable_data += stringRecord
            return printable_data.split("\n")