import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
import ConversionObjects
import weather_db_wrapper

# Connects the python file to the raw data database and creates the 
# global connection object for other functions to use
# should be encapsulated by weather_db_wrapper
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
# should be encapsulated by weather_db_wrapper
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

# should be encapsulated by weather_db_wrapper
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

# Splits the raw_master_string into an array
# using tabs as delimiters since the raw master string
# is tab separated
def create_raw_data_array(raw_data_string):
    raw_data_array = raw_data_string.split('\t')
    return raw_data_array

#utility function for conversion
#performs SQL command
# should be encapsulated by weather_db_wrapper
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

def conversion(field, raw_data_array):
    find_field = ConversionObjects.field_dict[field] #use the number to index which geiger object to create
    converted = ConversionObjects.find_field #not sure if this will work #supposed to create instance of specific geiger object subclass
    converted_data = converted.format(raw_data_array[field]) #perform the conversion
    insert_into_formatted_data(field, converted_data) #insert the converted value into the database

def convert_data(raw_data_array):
    # create the row by defaulting column values to NULL
    # update each column after the formatting takes place
    field = 0
    while raw_data_array[field] != "@":
        if field == 0: #Unix timestamp
            #extrapolate into 10 specified fields
            #store in database
            field += 1
        if raw_data_array[field] == "S-": #bottom section data
            #check if field == 1
            field += 1
            while raw_data_array[field] != "1-": #probably don't need a while loop? somehow index sql columns?
                                                #need to include index number "and field < 160" or something
                conversion(field, raw_data_array)
                field += 1
        if raw_data_array[field] == "1-": #top mux data
            field += 1
            while raw_data_array[field] != "2-":
                conversion(field, raw_data_array)
                field += 1
        if raw_data_array[field] == "2-": #top sway sensor data
            field += 1
            while raw_data_array[field] != "3-":
                conversion(field, raw_data_array)
                field += 1
        if raw_data_array[field] == "3-": #top flux data
            field += 1
            while raw_data_array[field] != "4-":
                conversion(field, raw_data_array)
                field += 1
        if raw_data_array[field] == "4-": #top triaxial magnetometer
            field += 1
            while raw_data_array[field] != "5-": #might have to change to updated future field
                conversion(field, raw_data_array)
                field += 1
        if raw_data_array[field] == "5-": #top future data, will probably be changed
            field += 1
            while raw_data_array[field] != "@":
                conversion(field, raw_data_array)
                field += 1
        # else:
        #     #throw an error, data not in the correct format
        #     break

def main():
    # Calling the connect_to_database() function to connect
    connect_to_database()

    # Calling the get_last_row() function and using the returned
    # raw_master_string in an array format
    print(get_all())
    # print(get_last_row())
    string_list = create_raw_data_array(get_last_row())
    print(string_list)

if __name__ == "__main__":
    main()