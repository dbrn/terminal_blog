# Database Module
from pymongo import MongoClient


class Database(object):
    def __init__(self, address, port, db_name):
        self.connection = MongoClient(str(address), int(port))
        self.database = self._open_db(db_name)

    def _open_db(self, db_name):
        return self.connection[str(db_name)]

    def __del__(self):
        self.connection.close()