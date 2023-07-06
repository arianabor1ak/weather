import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

class Weather_DB:
	def __init__(self):
		self.connection = None
		self.cursor = None

	# Connects the python file to the raw data database 
	# and creates the global connection object for other functions to use
	def db_connect(self):
		load_dotenv(find_dotenv())
		self.connection = psycopg2.connect(
			user = os.getenv("WEATHER_TOWER_USER"),
			password = os.getenv("WEATHER_TOWER_PASSWORD"),
			host = os.getenv("WEATHER_TOWER_HOST"),
			database = os.getenv("WEATHER_TOWER_DATABASE")
		)
		self.cursor = self.connection.cursor()
		print("Database connection: ", self.connection.closed)
		return self.connection #do we need to return anything?
	
	def db_commit(self):
		#logging info
		self.connection.commit()

	def db_close(self):
		#logging info
		if self.cursor is not None:
			self.cursor.close()
			self.cursor = None
		if self.connection is not None:
			self.connection.close()
			self.cursor = None

		return None

	# Insert the newly recieved master_string into the raw data database
	def insert_master_string(self, master_string):
		self.db_connect()
		self.cursor.execute("INSERT INTO raw_data (raw_master_string) VALUES (%s)", (master_string,))
		self.db_commit()
		self.db_close()

	# Prints all rows in the table
	def retrieve_raw_data(self):
		self.db_connect()
		self.cursor.execute("SELECT * FROM raw_data")
		rows = self.cursor.fetchall() #maybe need to have some error handling if there is nothing in the table?
		for row in rows:
			print(f"id: {row[0]}, timestamp: {row[1]}, master string: {row[2]}")
		self.db_close()
		
	# Retrieves the master string from the last row from the raw_data_database to
	# be formatted later on
	# The logic of this should be changed; instead of retrieving the last row,
	# retrieve any rows in the database that have a NULL character in formatted_id
	def get_last_row(self):
		self.db_connect()
		try:
			query = """
			SELECT raw_master_string
			FROM raw_data_table
			ORDER BY id DESC LIMIT 1;
			"""
			self.cursor.execute(query)
			self.db_commit()
			result = self.cursor.fetchone()
			self.db_close()
			return result[0]
		except Exception as err:
			print(f"Error: '{err}'")

			self.db_close()

	# retrieves all the master strings in the database
	def get_all(self):
		self.db_connect()
		try:
			query = """
			SELECT raw_master_string
			FROM raw_data_table
			ORDER BY id DESC;
			"""
			self.cursor.execute(query)
			self.db_commit()
			result = self.cursor.fetchall()
			self.db_close()
			return result[0]
		except Exception as err:
			print(f"Error: '{err}'")
		self.db_close()
			
	#utility function for convert_data
	#performs SQL command
	def insert_into_formatted_data(self, index, value):
		self.db_connect()
		try:
			command = """
				INSERT INTO formatted_data_table
				VALUES 
				"""
			self.cursor.execute(command)
		except Exception as err:
			print(f"Error: '{err}'")
		self.db_close()