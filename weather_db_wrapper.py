import os
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv, find_dotenv

class Weather_DB:
	def __init__(self):
		self.connection = None
		self.cursor = None
		self.null_array = []

	"""
	------------------------------------------DATABASE CONNECTION------------------------------------------
	"""

	# Connects the python file to the weather database 
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
		# return self.connection #do we need to return anything?
	
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

	"""
	------------------------------------------DATABASE INSERTION------------------------------------------
	"""

	# Insert the newly recieved master_string into the raw data database
	# Add error handling
	def insert_master_string(self, master_string):
		self.db_connect()
		self.cursor.execute("INSERT INTO raw_data (raw_master_string) VALUES (%s)", (master_string,))
		self.db_commit()
		self.db_close()

	# Creates a new row and inserts the Unix time into the row
	def insert_first(self, value):
		self.db_connect()
		try:
			# Rough sketch of what query should be
			# Need to figure out how to access correct column with index
			# Need to know id of row to later insert into raw_data
			command = """
			INSERT INTO formatted_data (unix_time)
			VALUES (%s)
			RETURNING id
			"""
			self.cursor.execute(command, (value,))
			formatted_id = self.cursor.fetchone()
			self.db_commit()
			self.db_close()
			return formatted_id
		except Exception as err:
			print(f"Error: '{err}'")
		self.db_close()

	# Inserts converted data into formatted_data
	def insert_formatted_data(self, column_name, value, row_id):
		self.db_connect()
		try:
			# Rough sketch of what query should be
			# Need to figure out how to access correct column with index
			# Need to know id of row to later insert into raw_data
			command = """
			UPDATE formatted_data (%s)
			VALUES (%s)
			WHERE id = %s
			"""
			self.cursor.execute(command, (AsIs(column_name), value, row_id,))
			self.db_commit()
		except Exception as err:
			print(f"Error: '{err}'")
		self.db_close()

	# Inserts the formatted_id into the corresponding raw_data row
	def insert_formatted_id(self, raw_id, formatted_id):
		self.db_connect()
		try:
			# Rough sketch of what the query should be
			command = """
			UPDATE raw_data
			SET formatted_id = %s
			WHERE raw_data.id = %s;
			"""
			self.cursor.execute(command, (formatted_id, raw_id,))
		except Exception as err:
			print(f"Error: '{err}'")
		finally:
			self.db_commit()
			self.db_close()

	"""
	------------------------------------------DATABASE RETRIEVAL------------------------------------------
	"""

	# Finds all the rows in raw data that have not yet been formatted
	def find_null(self):
		self.db_connect()
		try:
			query = """
			SELECT id
			FROM raw_data
			WHERE formatted_id IS NULL;
			"""
			self.cursor.execute(query)
			self.null_array = self.cursor.fetchall()
		except Exception as err:
			print(f"Error: '{err}'")
		finally:
			self.db_close()

	def get_master_string(self, id):
		self.db_connect()
		try:
			query = """
			SELECT raw_master_string
			FROM raw_data
			WHERE id = %s;
			"""
			self.cursor.execute(query, (id,))
			raw_master_string = self.cursor.fetchone()
			self.db_close()
			return raw_master_string[0]
		except Exception as err:
			print(f"Error: '{err}'")
			self.db_close()
			return ""
		
	def get_column_ids(self):
		self.db_connect()
		try:
			query = """
			SELECT COLUMN_NAME, ORDINAL_POSITION AS column_id 
			FROM INFORMATION_SCHEMA.COLUMNS 
			WHERE TABLE_NAME = 'formatted_data' 
			ORDER BY ORDINAL_POSITION;
			"""
			self.cursor.execute(query)
			column_ids = self.cursor.fetchall()
			self.db_close()
			return column_ids
		except Exception as err:
			print(f"Error: '{err}'")
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
			FROM raw_data
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

	# Prints all rows in the table
	def retrieve_raw_data(self):
		self.db_connect()
		self.cursor.execute("SELECT * FROM raw_data")
		rows = self.cursor.fetchall() #maybe need to have some error handling if there is nothing in the table?
		for row in rows:
			print(f"id: {row[0]}, timestamp: {row[1]}, master string: {row[2]}")
		self.db_close()

	# retrieves all the master strings in the database
	def get_all(self):
		self.db_connect()
		try:
			query = """
			SELECT raw_master_string
			FROM raw_data
			ORDER BY id DESC;
			"""
			self.cursor.execute(query)
			self.db_commit()
			result = self.cursor.fetchall()
			self.db_close()
			return result
		except Exception as err:
			print(f"Error: '{err}'")
		self.db_close()

def main():
	weather_db = Weather_DB()
	weather_db.find_null()
	print(weather_db.null_array)

if __name__ == "__main__":
	main()