import sqlite3


class DatabaseManager:
	def __init__(self, db_name="database/database.db"):
		self.connection = sqlite3.connect(db_name)

		self.cursor = self.connection.cursor()

		self.cursor.execute("PRAGMA foreign_key = ON;")

	def create_tables(self):
		# TABLE USERS
		self.cursor.execute('''
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_name TEXT NOT NULL,
				user_id INTEGER NOT NULL,
				Name TEXT NOT NULL,
				Last_Name TEXT NOT NULL,
				modif_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY (user_id) REFERENCES password (id_us))
				''')

		# Create trigger fo automatic actualization modif_time for USERS
		self.cursor.execute('''
			CREATE TRIGGER IF NOT EXISTS update_modif_time
			AFTER UPDATE ON users
			FOR EACH ROW
			BEGIN
				UPDATE users SET modif_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
			END;
			''')

		# TABLE PASSWORD
		self.cursor.execute('''
			CREATE TABLE IF NOT EXISTS password (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				hashed_pwd TEXT NOT NULL,
				id_us INTEGER NOT NULL,
				modif_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY (id_us) REFERENCES users (user_id))
				''')

		# Create trigger fo automatic actualization modif_time for PASSWORD
		self.cursor.execute('''
				CREATE TRIGGER IF NOT EXISTS update_modif_time
				AFTER UPDATE ON password
				FOR EACH ROW
				BEGIN
					UPDATE users SET modif_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
				END;
				''')

		# TABLE URLMONITOR
		self.cursor.execute('''
			CREATE TABLE IF NOT EXISTS urlmonitor (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				url_id INTEGER NOT NULL,
				pers_id INTEGER NOT NULL,
				url TEXT NOT NULL,
				interval INTEGER NOT NULL,
				threshold INTEGER NOT NULL,
				status TEXT NOT NULL,
				response_time TEXT NOT NULL,
				modif_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY (pers_id) REFERENCES users (user_id))
				''')

		# Create trigger fo automatic actualization modif_time for URLMONITOR
		self.cursor.execute('''
				CREATE TRIGGER IF NOT EXISTS update_modif_time
				AFTER UPDATE ON urlmonitor
				FOR EACH ROW
				BEGIN
					UPDATE users SET modif_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
				END;
				''')

		self.connection.commit()

	def alter_table(self):
		self.cursor.execute('''
		    ALTER TABLE users
		    	ADD COLUMN Name TEXT NOT NULL DEFAULT '';
		    ''')

		self.cursor.execute('''
			ALTER TABLE users
				ADD COLUMN Last_Name TEXT NOT NULl DEFAULT '';
				''')
		self.cursor.execute('''
			ALTER TABLE users
				ADD COLUMN Email TEXT NOT NULL DEFAULT '';
				''')

		self.connection.commit()

	def close(self):
		self.connection.close()
