import sqlite3
class Connector:
    def get_db_connection(self):
        conn = sqlite3.connect("app/core/database.db")
        conn.row_factory = sqlite3.Row
        return conn