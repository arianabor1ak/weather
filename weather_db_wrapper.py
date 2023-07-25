import os
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv, find_dotenv
import sys
import logging

class Weather_DB:
	def __init__(self):
		self.connection = None
		self.cursor = None

	"""
	------------------------------------------DATABASE CONNECTION------------------------------------------
	"""

	# Connects the python file to the weather database 
	# and creates the global connection object for other functions to use
	def db_connect(self):
		if self.connection is None:
			load_dotenv(find_dotenv())
			self.connection = psycopg2.connect(
				user = os.getenv("WEATHER_TOWER_USER"),
				password = os.getenv("WEATHER_TOWER_PASSWORD"),
				host = os.getenv("WEATHER_TOWER_HOST"),
				database = os.getenv("WEATHER_TOWER_DATABASE")
			)
			self.cursor = self.connection.cursor()
		assert (self.connection and self.connection.closed == 0) #everything that calls this function will have to catch an assertion error
		logging.debug(f"Database connection: {self.connection.closed}")
	
	def db_commit(self):
		self.connection.commit()

	def db_close(self):
		#logging info
		if self.cursor is not None:
			self.cursor.close()
			self.cursor = None
		if self.connection is not None:
			self.connection.close()
			self.connection = None
		# logging.debug(f"Database connection: {self.connection.closed}") 

	"""
	------------------------------------------DATABASE INSERTION------------------------------------------
	"""

	# Insert the newly recieved raw_string into the raw_data table
	# Add error handling
	def insert_raw_string(self, raw_string):
		try:
			self.db_connect()
			self.cursor.execute("INSERT INTO raw_data (raw_string) VALUES (%s)", (raw_string,))
			self.db_commit()
			self.db_close()
		except AssertionError as err:
			logging.error(f"{err}\nString to insert: {raw_string}")
		except Exception as err:
			logging.error(f"{err}")

	# Creates a new row and inserts the Unix time into a row in formatted_data
	def insert_first(self, value):
		assert (self.connection and self.connection.closed == 0) # call to this function will catch errors, don't catch in the function
		command = """
		INSERT INTO formatted_data (unix_time)
		VALUES (%s)
		RETURNING id
		"""
		self.cursor.execute(command, (value,))
		formatted_id = self.cursor.fetchone()
		self.db_commit()
		return formatted_id

	# Inserts the formatted_id into the corresponding raw_data row
	def insert_formatted_id(self, raw_id, formatted_id):
		assert (self.connection and self.connection.closed == 0) #don't catch this in the function
		command = """
		UPDATE raw_data
		SET formatted_id = %s
		WHERE id = %s;
		"""
		self.cursor.execute(command, (formatted_id, raw_id,))
		self.db_commit()

	# Inserts converted data into formatted_data
	def insert_data(self, column_name, value, row_id):
		try:
			assert (self.connection and self.connection.closed == 0)
			command = """
			UPDATE formatted_data
			SET "%s" = %s
			WHERE id = %s
			"""
			self.cursor.execute(command, (AsIs(column_name), value, row_id,))
		except Exception as err:
			logging.error(f"Error: '{err}'")

	# Inserts converted data into formatted_data
	def insert_formatted_data(self, column_name, value, range_value, row_id):
		try:
			assert (self.connection and self.connection.closed == 0)
			column_name_range = str(column_name) + "_range"
			command = """
			UPDATE formatted_data
			SET "%s" = %s, "%s" = %s
			WHERE id = %s
			"""
			self.cursor.execute(command, (AsIs(column_name), value, AsIs(column_name_range), range_value, row_id,))
		except Exception as err:
			logging.error(f"Error: '{err}'")

	def insert_flags(self, row_flag, one_flag, two_flag, three_flag, four_flag, kz_flag, row_id):
		try:
			assert (self.connection and self.connection.closed == 0)
			command = """
			UPDATE formatted_data
			SET row_flag = %s, one_flag = %s, two_flag = %s, three_flag = %s, four_flag = %s, kz_flag = %s
			WHERE id = %s
			"""
			self.cursor.execute(command, (row_flag, one_flag, two_flag, three_flag, four_flag, kz_flag, row_id,))
		except Exception as err:
			logging.error(f"Error: '{err}'")
		self.db_commit()

	"""
	------------------------------------------DATABASE RETRIEVAL------------------------------------------
	"""

	# Finds all the rows in raw data that have not yet been formatted
	def find_null(self):
		try:
			self.db_connect()
			query = """
			SELECT id
			FROM raw_data
			WHERE formatted_id IS NULL
			ORDER BY id;
			"""
			self.cursor.execute(query)
			null_array = self.cursor.fetchall()
			return null_array
		except Exception as err:
			logging.error(f"Error: '{err}'")
			return None

	# Retrieve the raw string from a specified row in the raw_data table
	def get_raw_string(self, id):
		try:
			assert (self.connection and self.connection.closed == 0)
			query = """
			SELECT raw_string
			FROM raw_data
			WHERE id = %s;
			"""
			self.cursor.execute(query, (id,))
			raw_string = self.cursor.fetchone()
			return raw_string[0]
		except Exception as err:
			logging.error(f"Error: '{err}'")
			return ""
		
	def get_column_ids(self):
		try:
			self.db_connect()
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
		# except AssertionError as err:
		# 	logging.error(f"{err}")
		except Exception as err:
			logging.error(f"Error: '{err}'")
			self.db_close()
			return []

def main():
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="{levelname}:({filename}:{lineno}) {message}", style="{")

	weather_db = Weather_DB()
	weather_db.find_null()

if __name__ == "__main__":
	main()