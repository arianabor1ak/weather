import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Connects the python file to the raw data database 
# and creates the global connection object for other functions to use
def connect_to_database():
    load_dotenv(find_dotenv())
    global connection
    connection = psycopg2.connect(
        user = os.getenv("WEATHER_TOWER_USER"),
        password = os.getenv("WEATHER_TOWER_PASSWORD"),
        host = os.getenv("WEATHER_TOWER_HOST"),
        database = os.getenv("WEATHER_TOWER_DATABASE")
    )
    return connection

# Insert the newly recieved master_string into the raw data database
def insert_master_string(master_string):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO raw_data (raw_master_string) VALUES (%s)", (master_string,))
    connection.commit()
    cursor.close()

# Prints all rows in the table
def retrieve_table():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM raw_data")
    rows = cursor.fetchall() #maybe need to have some error handling if there is nothing in the table?
    for row in rows:
        print(f"id: {row[0]}, timestamp: {row[1]}, master string: {row[2]}")
    cursor.close()
    
# Retrieves the master string from the last row from the raw_data_database to
# be formatted later on
# The logic of this should be changed; instead of retrieving the last row,
# retrieve any rows in the database that have a NULL character in formatted_id
def get_last_row():
    cursor = connection.cursor()
    try:
        query = """
        SELECT raw_master_string
        FROM raw_data_table
        ORDER BY id DESC LIMIT 1;
        """
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception as err:
        print(f"Error: '{err}'")

# retrieves all the master strings in the database
def get_all():
    cursor = connection.cursor()
    try:
        query = """
        SELECT raw_master_string
        FROM raw_data_table
        ORDER BY id DESC;
        """
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result[0]
    except Exception as err:
        print(f"Error: '{err}'")
        
#utility function for convert_data
#performs SQL command
def insert_into_formatted_data(index, value):
    cursor = connection.cursor()
    try:
       command = """
        INSERT INTO formatted_data_table
        VALUES 
        """
       cursor.execute(command)
    except Exception as err:
        print(f"Error: '{err}'")