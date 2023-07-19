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
    print("Columns: ", column_dict)
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
            print("ValueError: ", err)
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
        print("ValueError: ", err)
    weather_db.insert_formatted_data(columns[column_id], converted_data, in_range_data, row_id) #insert the converted value into the database
        
    field += 1
    column_id += 1
        
    return field, column_id

# Parses through the raw data array and manages when to perform conversions
# Updates the raw data table with the corresponding formatted table row id
def parse_data(raw_data_array, raw_id, columns):
    field = 0
    column_id = 2 #id of sql column data should be inserted into
    length = len(raw_data_array)
    row_id = 0

    try:
        assert (raw_data_array[-1] == "@"), "Master string must end with \'@\'"
    except IndexError as err:
        print(err)
        print("Master string cannot be empty")
        return
    except AssertionError as error:
        print(error)
        weather_db.insert_first(raw_data_array[0])
        return #does this have to return? could still try to parse string based on length

    while raw_data_array[field] != "@" and field < length:
        if field == 0: #Unix timestamp
            row_id = weather_db.insert_first(raw_data_array[0]) #column_id is 1
            weather_db.insert_formatted_id(raw_id, row_id)
            converted = ConversionObjects.unix_time()
            converted_time = converted.format(raw_data_array[0]) #extrapolate into specified fields
            
            star_id = 0
            stardate = ""
            for time in converted_time:
                column_name = columns[column_id]
                weather_db.insert_time_data(column_name, time, row_id) #insert each field into own column
                column_id += 1

                if star_id == 5:
                    stardate += "."
                if star_id < 6:
                    stardate += time
                star_id += 1
            weather_db.insert_time_data('stardate', stardate, row_id)
            column_id += 2 #increment an extra space to account for the future_time column
            field += 1
        elif raw_data_array[field] == "S-":
            print("S- index: ", field)
            try:
                assert (field == 1), "S- is at the wrong index"
            except AssertionError as err:
                print(err)
            field = 2
        elif raw_data_array[field] == "1-":
            print("1- index: ", field)
            # assert ()
            field += 1 #update field to correct field once it's known
        elif raw_data_array[field] == "2-":
            print("2- index: ", field)
            # assert ()
            field += 1
        elif raw_data_array[field] == "3-":
            print("3- index: ", field)
            # assert ()
            field += 1
        elif raw_data_array[field] == "4-":
            print("4- index: ", field)
            # assert ()
            field += 1
        elif raw_data_array[field] == "Z-":
            print("Z- index: ", field)
            # assert ()
            field += 1
        else: 
            field, column_id = conversion(field, raw_data_array, column_id, columns, row_id)

def main():
    columns = make_column_dict()

    raw_rows = weather_db.find_null()
    if raw_rows:
        for row in raw_rows:
            current_row = weather_db.get_master_string(row)
            string_list = create_raw_data_array(current_row)
            print("Row string: ", string_list)
            print("Row: ", row)
            row = row[0]
            parse_data(string_list, row, columns)

if __name__ == "__main__":
    main()