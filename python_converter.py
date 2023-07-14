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
        print("I'm special casing for concatenating")
        eval_string = "ConversionObjects." + str(find_field) + "()"

        eval_string = "ConversionObjects." + str(find_field) + "()"
        converted = eval(eval_string) # Creates instance of specific data object subclass

        converted = eval(eval_string) # Creates instance of specific data object subclass
        data_to_convert = ""

        for i in range(3):
            if raw_data_array[field] == "S-" or \
            raw_data_array[field] == "1-" or \
            raw_data_array[field] == "2-" or \
            raw_data_array[field] == "3-" or \
            raw_data_array[field] == "4-" or \
            raw_data_array[field] == "Z-": # should only need this for simulation data
                field += 1
            data_to_convert += raw_data_array[field]
            field += 1
        converted_data = converted.format(data_to_convert)
        for j in range(3):
            weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
            column_id += 1
        # class_id += 1
        
    elif "soil_temp" in find_field: #special case for soil_temp_below
        converted = ConversionObjects.soil_temp_below()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        # if find_field == "soil_temp_48_below": #increment the class_id only if it is the last soil_temp_below field
        # class_id += 1
        field += 1
        column_id += 1

    elif "soil_moist" in find_field: #special case for soil_moist
        converted = ConversionObjects.soil_moist()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1

    elif "_above" in find_field: #special case for soil_temp_above
        converted = ConversionObjects.soil_temp_above()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1
        
    elif "s_X" in find_field or "s_Y" in find_field: #special case for sway_sensor_xy_data
        converted = ConversionObjects.sway_sensor_XY_data()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1

    elif "f_T" in find_field: #special case for fluxgate_magnetometer_t_data
        converted = ConversionObjects.fluxgate_magnetometer_t_data()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1

    elif "f_X" in find_field or "f_Y" in find_field or "f_Z" in find_field: #special case for fluxgate_magnetometer_xyz_data
        converted = ConversionObjects.fluxgate_magnetometer_xyz_data()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1

    elif "t_T" in find_field: #special case for triaxial_magnetometer_t_data
        converted = ConversionObjects.triaxial_magnetometer_t_data()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1

    elif "t_X" in find_field or "t_Y" in find_field or "t_Z" in find_field: #special case for triaxial_magnetometer_xyz_data
        converted = ConversionObjects.triaxial_magnetometer_xyz_data()
        converted_data = converted.format(raw_data_array[field])
        
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id)
        field += 1
        column_id += 1
        
    else: #non-special cases
        eval_string = "ConversionObjects." + str(find_field) + "()"
        converted = eval(eval_string) # Creates instance of specific data object subclass
        
        converted_data = converted.format(raw_data_array[field]) #perform the conversion
        weather_db.insert_formatted_data(columns[column_id], converted_data, row_id) #insert the converted value into the database
        
        field += 1
        # class_id += 1
        column_id += 1
        
    return field, column_id

# Parses through the raw data array and manages when to perform conversions
# Updates the raw data table with the corresponding formatted table row id
def parse_data(raw_data_array, raw_id, columns):
    field = 0
    column_id = 2 #id of sql column data should be inserted into
    # class_id = 1 #id of subclass
    length = len(raw_data_array)
    row_id = 0

    if raw_data_array[-1] != "@":
        print("Last element: ", raw_data_array[-2])
        raise ValueError("Master string must end with \'@\'")
        return

    while raw_data_array[field] != "@" and field < length: #should be length with actual data instead of 68
        if field == 0: #Unix timestamp
            row_id = weather_db.insert_first(raw_data_array[0]) #column_id is 1
            weather_db.insert_formatted_id(raw_id, row_id)
            converted = ConversionObjects.unix_time()
            converted_time = converted.format(raw_data_array[0]) #extrapolate into specified fields
            
            star_id = 0
            stardate = ""
            for time in converted_time:
                column_name = columns[column_id]
                weather_db.insert_formatted_data(column_name, time, row_id) #insert each field into own column
                column_id += 1

                if star_id == 5:
                    stardate += "."
                if star_id < 6:
                    stardate += time
                star_id += 1
            weather_db.insert_formatted_data('stardate', stardate, row_id)
            column_id += 2 #increment an extra space to account for the future_time column
            field += 1
        elif raw_data_array[field] == "S-" or \
            raw_data_array[field] == "1-" or \
            raw_data_array[field] == "2-" or \
            raw_data_array[field] == "3-" or \
            raw_data_array[field] == "4-" or \
            raw_data_array[field] == "Z-":
            field += 1
        else: 
            #do some error checking to make sure it's not null?
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
            print("Row[0]: ", row)
            parse_data(string_list, row, columns)

if __name__ == "__main__":
    main()