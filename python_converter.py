import ConversionObjects
import weather_db_wrapper

weather_db = weather_db_wrapper.Weather_DB()

# Splits the raw_master_string into an array using tabs as delimiters 
# since the raw master string is tab separated
def create_raw_data_array(raw_data_string):
    raw_data_array = raw_data_string.split('\t')
    return raw_data_array

# Creates a dictionary of the SQL column ids and the column names in formatted_data
def make_column_dict():
    column_dict = {}
    column_ids = weather_db.get_column_ids()
    for row in column_ids:
        column_dict[int(row[1])] = row[0]
    return column_dict

# Looks up the field index to determine which subclass is being handled
# Performs the conversion according the subclass
# Inserts the converted data into the formatted data table
def conversion(field, raw_data_array, column_name, row_id):
    find_field = ConversionObjects.field_dict[field] #use the number to index which object to create
    converted = find_field #not sure if this will work #supposed to create instance of specific data object subclass
    converted_data = converted.format(raw_data_array[field]) #perform the conversion

    weather_db.insert_formatted_data(column_name, converted_data, row_id) #insert the converted value into the database

# Parses through the raw data array and manages when to perform conversions
# Updates the raw data table with the corresponding formatted table row id
def parse_data(raw_data_array, raw_id, dictionary):
    # create the row by defaulting column values to NULL
    # update each column after the formatting takes place
    field = 0
    column_id = 3 #id of sql column data should be inserted into
    length = len(raw_data_array)
    row_id = 0

    if raw_data_array[-1] != "@":
        raise ValueError("Master string must end with \'@\'")
        return

    while raw_data_array[field] != "@" and field < length:
        if field == 0: #Unix timestamp
            #extrapolate into 10 specified fields
            #column_id is 3
            row_id = weather_db.insert_first(raw_data_array[0])
            weather_db.insert_formatted_id(raw_id, row_id)
            field += 1
            column_id += 1
        elif raw_data_array[field] == "S-" or \
            raw_data_array[field] == "1-" or \
            raw_data_array[field] == "2-" or \
            raw_data_array[field] == "3-" or \
            raw_data_array[field] == "4-" or \
            raw_data_array[field] == "5-":
            field += 1
            print("Skipping")
        else: #add data to the corresponding column in formatted_data
            # while raw_data_array[field] != "1-": #probably don't need a while loop? somehow index sql columns?
            #need to include index number "and field < 160" or something
            #do some error checking to make sure it's not null?
            column_name = dictionary[column_id]     #look up column name in dictionary
            # conversion(field, raw_data_array, column_name, row_id)
            field += 1
            column_id += 1

def main():
    dictionary = make_column_dict()
    weather_db.find_null()
    raw_rows = weather_db.null_array
    if raw_rows:
        print("Raw rows: ", raw_rows)
        for row in raw_rows:
            current_row = weather_db.get_master_string(row)
            string_list = create_raw_data_array(current_row)
            row = row[0]
            parse_data(string_list, row, dictionary)

if __name__ == "__main__":
    main()