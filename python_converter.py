import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Connects the python file to the raw data database
# and creates the global connection object for other functions
# to use
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

# Retrieves the last row from the raw_data_database to 
# be formatted later on
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

# Splits the raw_master_string into an array
# using tabs as delimiters since the raw master string
# is tab seperated
def create_raw_data_array(raw_data_string):
    raw_data_array = raw_data_string.split('\t')
    return raw_data_array

# def insert_in_cooked_table():
    # create the row by defaulting column values to NULL
    # update each column after the formatting takes place

# Calling the connect_to_database() function to connect
connect_to_database()

# Calling the get_last_row() function and using the returned
# raw_master_string in an array format
print(create_raw_data_array(get_last_row()))
