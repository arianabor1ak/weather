import ConversionObjects
import weather_db_wrapper
import sys
import logging
from time import time

weather_db = weather_db_wrapper.Weather_DB()
delimiter_dict = {
    "S-": (1, "B"),
    "1-": (164, "1"),
    "2-": (281, "2"),
    "3-": (363, "3"),
    "4-": (427, "4"),
    "Z-": (512, "aux")
    } #index where the delimiter should be and the value that comes after the delimiter

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
    logging.debug(f"Columns: {column_dict}")
    return column_dict

# Creates a subclass based on the column_id
# Performs the conversion according the subclass
# Inserts the converted data into the formatted data table
def conversion(field, raw_data_array, column_id, columns, row_id):
    find_field = columns[column_id] #use column_id to index which subclass object to create
    
    if "upper" in find_field: #special case where three raw data fields will be concatenated
        eval_string = "ConversionObjects." + str(find_field) + "()"
        converted = eval(eval_string) # Creates instance of specific data object subclass
        data_to_convert = ""

        for i in range(3):
            data_to_convert += raw_data_array[field]
            field += 1
        try:
            converted_data = converted.format(data_to_convert)
            in_range_data = converted.check_range(converted_data)
        except ValueError as err:
            logging.error(f"ValueError: {err}")
        else:
            for j in range(3):
                weather_db.insert_formatted_data(columns[column_id], converted_data, in_range_data, row_id)
                column_id += 1
        return field, column_id
        
    elif "s_X" in find_field or "s_Y" in find_field: #special case for sway_sensor_xy_data
        converted = ConversionObjects.sway_sensor_XY_data()

    elif "f_X" in find_field or "f_Y" in find_field or "f_Z" in find_field: #special case for fluxgate_magnetometer_xyz_data
        converted = ConversionObjects.fluxgate_magnetometer_xyz_data()

    elif "t_X" in find_field or "t_Y" in find_field or "t_Z" in find_field: #special case for triaxial_magnetometer_xyz_data
        converted = ConversionObjects.triaxial_magnetometer_xyz_data()

    elif "f_T" in find_field: #special case for fluxgate_magnetometer_t_data
        converted = ConversionObjects.fluxgate_magnetometer_t_data()

    elif "t_T" in find_field: #special case for triaxial_magnetometer_t_data
        converted = ConversionObjects.triaxial_magnetometer_t_data()
        
    elif "soil_temp" in find_field: #special case for soil_temp_below
        converted = ConversionObjects.soil_temp_below()

    elif "soil_moist" in find_field: #special case for soil_moist
        converted = ConversionObjects.soil_moist()

    elif "_above" in find_field: #special case for soil_temp_above
        converted = ConversionObjects.soil_temp_above()
        
    else: #non-special cases
        eval_string = "ConversionObjects." + str(find_field) + "()"
        converted = eval(eval_string) # Creates instance of specific data object subclass
        
    try:
        converted_data = converted.format(raw_data_array[field]) #perform the conversion
        in_range_data = converted.check_range(converted_data)
    except ValueError as err:
        logging.error(f"ValueError: {err}")
    weather_db.insert_formatted_data(columns[column_id], converted_data, in_range_data, row_id) #insert the converted value into the database
        
    field += 1
    column_id += 1
        
    return field, column_id

# Parses through the raw data array and manages when to perform conversions
# Updates the raw data table with the corresponding formatted table row id
def parse_data(raw_data_array, raw_id, columns):
    field = 0
    column_id = 2 #id of sql column data should be inserted into
    row_id = 0

    row_flag = s_flag = one_flag = two_flag = three_flag = four_flag = kz_flag = 1

    try:
        assert (raw_data_array[-1] == "@"), "Master string must end with \'@\'"
    except IndexError as err:
        logging.error(f"Master string cannot be empty\n{err}")
        row_id = weather_db.insert_first(0)
        weather_db.insert_formatted_id(raw_id, row_id)
        return
    except AssertionError as error:
        logging.error(f"{error}")
        row_flag = 2

    length = len(raw_data_array)
    while field < length and raw_data_array[field] != "@":
        if field == 0: #Unix timestamp
            row_id = weather_db.insert_first(raw_data_array[0]) #column_id is 1
            weather_db.insert_formatted_id(raw_id, row_id)
            converted = ConversionObjects.unix_time()
            converted_time = converted.format(raw_data_array[0]) #extrapolate into specified fields
            
            star_id = 0
            stardate = ""
            for time in converted_time:
                column_name = columns[column_id]
                weather_db.insert_data(column_name, time, row_id) #insert each field into own column
                column_id += 1

                if star_id == 5:
                    stardate += "."
                if star_id < 6:
                    stardate += time
                star_id += 1
            weather_db.insert_data('stardate', stardate, row_id)
            column_id += 2 #increment an extra space to account for the future_time column
            field += 1
        elif raw_data_array[field] in delimiter_dict:
            logging.debug("I'm a delimiter in the dictionary, yeeeeoooouuuch!!!")
            logging.debug(f"{raw_data_array[field]} index: {field}")
            delimiter_tuple = delimiter_dict[raw_data_array[field]]
            try:
                assert (field == delimiter_tuple[0]), f"{raw_data_array[field]} is at the wrong index"
                assert (raw_data_array[field + 1] == delimiter_tuple[1]), f"Wrong data after {raw_data_array[field]}" #should be used after getting data from tower
            except AssertionError as err:
                logging.error(f"{err}")
            logging.debug(f"Here's the data after {raw_data_array[field]}: {raw_data_array[field + 1]}")
            field = delimiter_tuple[0] + 2
        else: 
            try:
                assert (field != 1 and field != 164 and field != 281 and field != 363 and field != 427 and field != 512), "This index should be a section separator"
            except AssertionError as err:
                logging.error(f"{err}")
            field, column_id = conversion(field, raw_data_array, column_id, columns, row_id)
    try:
        assert (field == 554), "String ends with wrong index"
    except AssertionError as err:
        logging.error(f"{err}")
        kz_flag = 0
    if s_flag == 0 and one_flag == 0 and two_flag == 0 and three_flag == 0 and four_flag == 0 and kz_flag == 0:
        row_flag = 0 #entire row is bad
    elif s_flag == 0 or one_flag == 0 or two_flag == 0 or three_flag == 0 or four_flag == 0 or kz_flag == 0 or row_flag == 2:
        row_flag = 2 #partially bad
    else:
        row_flag = 1
    weather_db.insert_flags(row_flag, one_flag, two_flag, three_flag, four_flag, kz_flag, row_id)

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="{levelname}:({filename}:{lineno}) {message}", style="{")

    columns = make_column_dict()

    start = time() - 6
    while True:
        if time() - start >= 5:
            start = time()
            raw_rows = weather_db.find_null()
            if raw_rows:
                for row in raw_rows:
                    current_row = weather_db.get_master_string(row)
                    string_list = create_raw_data_array(current_row)
                    logging.debug(f"Row: {row}")
                    logging.debug(f"Row string: {string_list}")
                    row = row[0]
                    parse_data(string_list, row, columns)
            weather_db.db_close()

if __name__ == "__main__":
    main()