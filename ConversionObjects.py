from unicodedata import decimal


class ConversionObject:
	field_dict = {}

	def __init__(self, given_data_name, given_data_type, given_typical_lower_limit, given_typical_upper_limit, given_integer_count, given_decimal_count, given_lower_limit, given_upper_limit):
		self.data_name = given_data_name
		self.data_type = given_data_type
		self.typical_lower_limit = given_typical_lower_limit
		self.typical_upper_limit  = given_typical_upper_limit
		self.integer_count = given_integer_count 
		self.decimal_count = given_decimal_count 
		self.lower_limit = given_lower_limit
		self.upper_limit = given_upper_limit
	
	def __str__(self): 
		print("\n---------------" + self.data_name + "---------------\n" +
		"Data Type: " + self.data_type + "\n" +
		"Typical Lower Limit: " + str(self.typical_lower_limit) + "\n" +
		"Typical Upper Limit: " + str(self.typical_upper_limit) + "\n" +
		"Number of Integers: "  + str(self.integer_count) + "\n" +
		"Number of Integers After Decimal: " + str(self.decimal_count) + "\n" +
		"Sensors Lower Limit: " + str(self.lower_limit) + "\n" +
		"Sensors Upper Limit: " + str(self.upper_limit) + "\n")

	def format(self, rawdata):
		converted = float(rawdata)
		return converted

#===================================================================================================================
#													GEIGER BLOCK
#===================================================================================================================
# Raw data format: dec5 ticks, 9, dec4 volts, dec4 amps, 9, dec5 tempr, 9, hex2 status, 13
#-------------------------------------------------------------------------------------------------------------------
#													TICKS:
# This is the number of Geiger tube ticks that occur in 1 minute.
# Typical background levels are around 100-120.
# Requires no conversion or response.

class GeigerTicks(ConversionObject):
	def __init__(self):
		data_name = "geiger_ticks"
		data_type = "dec"
		data_typical_lower_limit = 100
		data_typical_upper_limit = 120
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 5
		sensor_upper_limit = 2000
		self.index = 1
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		ConversionObject.field_dict[2] = GeigerTicks()

	def format(self, rawdata):
		converted = int(rawdata)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													VOLTS:
# This is the high voltage for the geiger tube.
# To convert from raw voltage, divide by 1024, multiply by 5, and multiply by 250.
# The result is in volts.

class GeigerHighVolts(ConversionObject):
	def __init__(self):
		data_name = "geiger_high_volts"
		data_type = "dec"
		data_typical_lower_limit = 800
		data_typical_upper_limit = 900
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 800
		sensor_upper_limit = 900
		self.index = 2
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)* float("1.2207")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													AMPS:
# This is the current drawn by the geiger circuit.
# Each volt of raw data corresponds to 16.66 mA actual load current.
# The result is in mA.

class geiger_current(ConversionObject):
	def __init__(self):
		data_name = "geiger_current"
		data_type = "dec"
		data_typical_lower_limit = 3
		data_typical_upper_limit = 3.6
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 10
		sensor_upper_limit = 55
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float("0.08138")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEMPERATURE:
# This is the temperature inside the geiger circuit in degrees F.

class geiger_temperature(ConversionObject):
	def __init__(self):
		data_name = "geiger_temperature"
		data_type = "dec"
		data_typical_lower_limit = -20
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = -20
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * float(".72") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------|
#|																													|
#|																													|
#|																													|
#|								GEIGER STATUS CLASS SHOULD BE IMPLEMENTED HERE 										|
#|																													|
#|																													|
#|																													|
#-------------------------------------------------------------------------------------------------------------------|

#===================================================================================================================
#													VORTEX BLOCK
#===================================================================================================================
# 
#-------------------------------------------------------------------------------------------------------------------
#													AVERAGE SPEED:
# Average windspeed over last minute measured by vortex anemometer. Result is in mph.

class vortex_avg_speed(ConversionObject):
	def __init__(self):
		data_name = "vortex_avg_speed"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		converted = float(rawdata)/float(12)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													GUST:
# Peak gust over last minute measured by vortex anemometer in mph.
class vortex_wind_gust(ConversionObject):
	def __init__(self):
		data_name = "vortex_wind_gust"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		converted = float(rawdata)/float(12)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													CALCULATED WIND SPEED:
class vortex_calc_mph(ConversionObject):
	def __init__(self):
		data_name = "vortex_calc_mph"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		converted = float(rawdata)/float(600)
		return converted

#===================================================================================================================
#													RAIN GAUGE BLOCK
#===================================================================================================================
#
#-------------------------------------------------------------------------------------------------------------------
#													DRIP CODE:
#-------------------------------------------------------------------------------------------------------------------|
#|																													|
#|																													|
#|																													|
#|										RAIN DRIP CODE SHOULD BE IMPLEMENTED HERE 									|
#|										IN THE FUTURE																|
#|																													|
#|																													|
#-------------------------------------------------------------------------------------------------------------------|
#-------------------------------------------------------------------------------------------------------------------
#													INCHES OF RAIN:
# Rain received in a day. Result is in inches.
class rain_bucket(ConversionObject):
	def __init__(self):
		data_name = "rain_bucket"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 1500
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		converted = float(rawdata)/float(100)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													INCHES OF RAIN:
# Lower numbers indicate faster rainfall.
class rain_rate(ConversionObject):
	def __init__(self):
		data_name = "rain_rate"
		data_type = "dec"
		data_typical_lower_limit = 200
		data_typical_upper_limit = 60000
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 200
		sensor_upper_limit = 65536
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = int(rawdata)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													INCHES OF RAIN:
# Time in minutes since last bucket tip to nearest ten minutes.
class rain_ten_min_dry(ConversionObject):
	def __init__(self):
		data_name = "rain_ten_min_dry"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 65535
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 28000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)


	def format(self, rawdata):
		converted = float(rawdata)*float(10)
		return int(converted)

#-------------------------------------------------------------------------------------------------------------------
#													BATTERY VOLTAGE:
#-------------------------------------------------------------------------------------------------------------------|
#|																													|
#|																													|
#|																													|
#|										BATTERY VOLTAGE SHOULD BE IMPLEMENTED HERE 									|
#|										IN THE FUTURE																|
#|																													|
#|																													|
#-------------------------------------------------------------------------------------------------------------------|

#===================================================================================================================
#													TEMP HEAD BLOCK
#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
#													RTD_1K_COMBINED
#-------------------------------------------------------------------------------------------------------------------
#													RTD_100_COMBINED
#-------------------------------------------------------------------------------------------------------------------
#													RTD_DAVIS_COMBINED
#-------------------------------------------------------------------------------------------------------------------
#													RH_SENSOR_1:
# Result is humidity in %. Sensor is HIH-5030.
class RH_sensor_1(ConversionObject):
	def __init__(self):
		data_name = "RH_sensor_1"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 15
		sensor_upper_limit = 101
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float("32.2") - float("25.8") 
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RH_SENSOR_2:
# Result is humidity in %. Sensor is HIH-5030.
class RH_sensor_2(ConversionObject):
	def __init__(self):
		data_name = "RH_sensor_2"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 15
		sensor_upper_limit = 101
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		converted = float(rawdata)*float("32.2") - float("25.8") 
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													OUTER_SHIELD_LM335:
# Result is in degrees Fahrenheit.
class outer_shield_LM335(ConversionObject):
	def __init__(self):
		data_name = "outer_shield_LM335"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def fromat(self, rawdata):
		converted = float(rawdata)*float(".0274658") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													MIDDLE_SHIELD_LM335:
# Result is in degrees Fahrenheit.
class middle_shield_LM335(ConversionObject):
	def __init__(self):
		data_name = "middle_shield_LM335"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)


	def format(self, rawdata):
		converted = float(rawdata)*float(".0274658") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													INNER_SHIELD_LM335:
# Result is in degrees Fahrenheit.
class inner_shield_LM335(ConversionObject):
	def __init__(self):
		data_name = "inner_shield_LM335"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)


	def format(self, rawdata):
		converted = float(rawdata)*float(".0274658") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													BOWL_LM335:
# Result is in degrees Fahrenheit.
class bowl_LM335(ConversionObject):
	def __init__(self):
		data_name = "bowl_LM335"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float(".0274658") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													AMBIENT_TEMP_LM335:
# Result is in degrees Fahrenheit.
class ambient_temp_LM335(ConversionObject):
	def __init__(self):
		data_name = "ambient_temp_LM335"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float(".0274658") - float("459.688")
		return converted
#-------------------------------------------------------------------------------------------------------------------
#													IR_SNOW_DEPTH
#-------------------------------------------------------------------------------------------------------------------
#													TEMP_HEAD_FAN_AIRFLOW:
# Result is in arbitrary units.
class temp_head_fan_airflow(ConversionObject):
	def __init__(self):
		data_name = "temp_head_fan_airflow"
		data_type = "dec"
		data_typical_lower_limit = 0.17
		data_typical_upper_limit = 0.19
		integer_count = 1
		decimal_count = 4
		sensor_lower_limit = 0.1
		sensor_upper_limit = 0.25
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float("5") / float("65536")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEMP_HEAD_FAN_VOLTAGE:
# Result is in volts.
class temp_head_fan_voltage(ConversionObject):
	def __init__(self):
		data_name = "temp_head_fan_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 12
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 5
		sensor_upper_limit = 13
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float("25") / float("65536")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEMP_HEAD_FAN_CURRENT:
# Result is in volts.
class temp_head_fan_current(ConversionObject):
	def __init__(self):
		data_name = "temp_head_fan_current"
		data_type = "dec"
		data_typical_lower_limit = 250
		data_typical_upper_limit = 450
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 200
		sensor_upper_limit = 475
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float("5") / float("393216")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													PTB_CONVERTED:
# Result is in inches of mercury.
#-------------------------------------------------------------------------------------------------------------------
#													AD_TEMPERATURE:
# Result is in degrees Fahrenheit.
class AD_temperature(ConversionObject):
	def __init__(self):
		data_name = "AD_temparture"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 90
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = 0
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata)*float(".027466") - float("459.688")
		return converted

#===================================================================================================================
#													FAN BLOCK
#===================================================================================================================
# 
#-------------------------------------------------------------------------------------------------------------------
#													FAN_VOLTAGE:
# Result is in volts.
class fan_voltage(ConversionObject):
	def __init__(self):
		data_name = "fan_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 12
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 5
		sensor_upper_limit = 13
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("25") / float("1024")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													FAN_CURRENT:
# Result is in milliamps.
class fan_current(ConversionObject):
	def __init__(self):
		data_name = "fan_current"
		data_type = "dec"
		data_typical_lower_limit = 250
		data_typical_upper_limit = 450
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 200
		sensor_upper_limit = 475
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("5") / float("6144")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													FAN_SPEED:
# Result is in rpm.
class fan_speed(ConversionObject):
	def __init__(self):
		data_name = "fan_speed"
		data_type = "dec"
		data_typical_lower_limit = 1500
		data_typical_upper_limit = 1800
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 1200
		sensor_upper_limit = 1900
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def fromat(self, rawdata):
		converted = int(rawdata) * 20
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TS4200_CURRENT:
# Result is in mA.
class TS4200_current(ConversionObject):
	def __init__(self):
		data_name = "TS4200_current"
		data_type = "dec"
		data_typical_lower_limit = 100
		data_typical_upper_limit = 140
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 100
		sensor_upper_limit = 150
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata) * float("0.081380")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RF_LINK_CURRENT:
# Result is in mA.
class RF_link_current(ConversionObject):
	def __init__(self):
		data_name = "RF_link_current"
		data_type = "dec"
		data_typical_lower_limit = 100
		data_typical_upper_limit = 200
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 100
		sensor_upper_limit = 250
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata) * float("0.081380")
		return converted


#-------------------------------------------------------------------------------------------------------------------
#													BOX_HUMIDITY:
# Sensor directly outputs humidity 0-100%.
class box_humidity(ConversionObject):
	def __init__(self):
		data_name = "box_humidity"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 50
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													GROUND_TEMPERATURE:
# Result is in degrees Fahrenheit.
class ground_temperature(ConversionObject):
	def __init__(self):
		data_name = "ground_temperature"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -45
		sensor_upper_limit = 130
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("0.036") - float("459.688")
		return converted

#===================================================================================================================
#													TEN FOOT BLOCK
#===================================================================================================================
#

#-------------------------------------------------------------------------------------------------------------------
#													SNOW_DEPTH_SONIC:
# 
class snow_depth_sonic(ConversionObject):
	def __init__(self):
		data_name = "snow_depth_sonic"
		data_type = "dec"
		data_typical_lower_limit = 90
		data_typical_upper_limit = 120
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 75
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(str(self.height_of_sensor)) - float(rawdata)/float("25.4")
		return converted


#-------------------------------------------------------------------------------------------------------------------
#													TEN_ENCLOSURE_TEMP:
# Result is in degrees Fahrenheit.
class ten_enclosure_temp(ConversionObject):
	def __init__(self):
		data_name = "ten_enclosure_temp"
		data_type = "dec"
		data_typical_lower_limit = -20
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = -20
		sensor_upper_limit = 115
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)*float("7.2") - float("4883.8")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEN_CIRCUIT_CURRENT:
# Result is in mA.
class ten_circuit_current(ConversionObject):
	def __init__(self):
		data_name = "ten_circuit_current"
		data_type = "dec"
		data_typical_lower_limit = 7
		data_typical_upper_limit = 35
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 5
		sensor_upper_limit = 40
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("12288")
		return converted
#-------------------------------------------------------------------------------------------------------------------
#													ten_RTD_temperature:
#-------------------------------------------------------------------------------------------------------------------
#													RH_PRECON:
# Result is humidity rounded to 1 decimal place.
class RH_Precon(ConversionObject):
	def __init__(self):
		data_name = "RH_Recon"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 5
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("0.0012477")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEMPERATURE_PRECON:
# Result is temperature (F) rounded to 1 decimal place.
class Temperature_Precon(ConversionObject):
	def __init__(self):
		data_name = "Temperature_Precon"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = -30
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("0.002388") - float("17.996")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RH_HONEYWELL:
# Result is humidity rounded to 1 decimal place.
class RH_Honeywell(ConversionObject):
	def __init__(self):
		data_name = "RH_Honeywell"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 5
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float("32.2") - float("25.8")
		return converted

#===================================================================================================================
#													POWER SUPPLY BLOCK
#===================================================================================================================
#
#-------------------------------------------------------------------------------------------------------------------
#													POWER_100WA_VOLTAGE:
# Result is in volts.
class power_100WA_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_100WA_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 21
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_100WA_CURRENT:
# Result is in mA.
class power_100WA_current(ConversionObject):
	def __init__(self):
		data_name = "power_100WA_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 5500
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 6000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("167")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_100WB_VOLTAGE:
# Result is in volts.
class power_100WB_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_100WB_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 21
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_100WB_CURRENT:
# Result is in mA.
class power_100WB_current(ConversionObject):
	def __init__(self):
		data_name = "power_100WB_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 5500
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 6000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("167")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_50W_VOLTAGE:
# Result is in volts.
class power_50W_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_50W_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 21
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_50W_CURRENT:
# Result is in mA.
class power_50W_current(ConversionObject):
	def __init__(self):
		data_name = "power_50W_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 3000
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 3100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("185")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_20WA_VOLTAGE:
# Result is in volts.
class power_20WA_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_20WA_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 21
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_20WA_CURRENT:
# Result is in mA.
class power_20WA_current(ConversionObject):
	def __init__(self):
		data_name = "power_20WA_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 1300
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 1400
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("185")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_LOAD_VOLTAGE:
# Result is in volts.
class power_load_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_load_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 14
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 15
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_LOAD_CURRENT:
# Result is in mA.
class power_load_current(ConversionObject):
	def __init__(self):
		data_name = "power_load_current"
		data_type = "dec"
		data_typical_lower_limit = 600
		data_typical_upper_limit = 1800
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 2
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1.2")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_BATTERY_VOLTAGE:
# Result is in volts.
class power_battery_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_battery_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 14
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_BATTERY_CURRENT:
# Result is in mA.
class power_battery_current(ConversionObject):
	def __init__(self):
		data_name = "power_battery_current"
		data_type = "dec"
		data_typical_lower_limit = -15000
		data_typical_upper_limit = 2000
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = -15000
		sensor_upper_limit = 2000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("83")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_SOLAR_VOLTAGE:
# Result is in volts.
class power_solar_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_solar_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 20
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_SOLAR_CURRENT:
# Result is in mA.
class power_solar_current(ConversionObject):
	def __init__(self):
		data_name = "power_solar_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 15000
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 15000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("83")*float("1000")
		return converted  

#-------------------------------------------------------------------------------------------------------------------
#													POWER_20WB_VOLTAGE:
# Result is in volts.
class power_20WB_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_20WB_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 20
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 19
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)/float("1000") * float("5.02")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_20WB_CURRENT:
# Result is in mA.
class power_20WB_current(ConversionObject):
	def __init__(self):
		data_name = "power_20WB_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 1300
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 1400
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - float("2500"))/float("185")*float("1000")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_FAN_CURRENT_A:
# Result is in mA.
class power_fan_current_A(ConversionObject):
	def __init__(self):
		data_name = "power_fan_current_A"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 40
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 50
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("60")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_HEATER_CURRENT:
# Result is in mA.
class power_heater_current_A(ConversionObject):
	def __init__(self):
		data_name = "power_heater_current_A"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 625
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 650
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("6")
		return converted


#-------------------------------------------------------------------------------------------------------------------
#													POWER_BATTERY_TEMPERATURE_A:
# Result is temperature in degrees Fahrenheit.
class power_battery_temperature_A(ConversionObject):
	def __init__(self):
		data_name = "power_battery_temperature_A"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 50
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = (float(rawdata)-float("2731.6"))*float(".18") + float("32")
		return converted
#-------------------------------------------------------------------------------------------------------------------
#													POWER_CABINET_TEMPERATURE:
# Result is temperature in degrees Fahrenheit.
class power_cabinet_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_cabinet_temperature"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 10
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = (float(rawdata)-float("2731.6"))*float(".18") + float("32")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_MPPT_TEMPERATURE:
# Result is temperature in degrees Fahrenheit.
class power_MPPT_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_MPPT_temperature"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 10
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata)-float("2731.6"))*float(".18") + float("32")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_5C_VOLTAGE:
# Result is in volts.
class power_5C_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_5C_voltage"
		data_type = "dec"
		data_typical_lower_limit = 4.95
		data_typical_upper_limit = 5.05
		integer_count = 1
		decimal_count = 2
		sensor_lower_limit = 4.7
		sensor_upper_limit = 5.1
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("500")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_5DAQ_VOLTAGE:
# Result is in volts.
class power_5DAQ_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_5DAQ_voltage"
		data_type = "dec"
		data_typical_lower_limit = 4.95
		data_typical_upper_limit = 5.05
		integer_count = 1
		decimal_count = 2
		sensor_lower_limit = 4.7
		sensor_upper_limit = 5.1
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("500")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_5DAQ_CURRENT:
# Result is in mA.
class power_5DAQ_current(ConversionObject):
	def __init__(self):
		data_name = "power_5DAQ_current"
		data_type = "dec"
		data_typical_lower_limit = 600
		data_typical_upper_limit = 1400
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 30
		sensor_upper_limit = 1500
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("6")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_VTOP_VOLTAGE:
# Result is in volts.
class power_VTOP_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_VTOP_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 14
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 8
		sensor_upper_limit = 15
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)*float(".00502")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_VTOP_CURRENT:
# Result is in mA.
class power_VTOP_current(ConversionObject):
	def __init__(self):
		data_name = "power_VTOP_current"
		data_type = "dec"
		data_typical_lower_limit = 50
		data_typical_upper_limit = 400
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 400
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("6")
		return converted


#-------------------------------------------------------------------------------------------------------------------
#													POWER_VAUX_VOLTAGE:
# Result is in volts.
class power_VAUX_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_VAUX_voltage"
		data_type = "dec"
		data_typical_lower_limit = 9
		data_typical_upper_limit = 14
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 8
		sensor_upper_limit = 15
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)*float(".00502")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_VAUX_CURRENT:
# Result is in volts.
class power_VAUX_current(ConversionObject):
	def __init__(self):
		data_name = "power_VAUX_current"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 400
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 400
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)/float("6")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_DAQ_INPUT_CURRENT:
# Result is in mA.
class power_DAQ_input_current(ConversionObject):
	def __init__(self):
		data_name = "power_DAQ_input_current"
		data_type = "dec"
		data_typical_lower_limit = 600
		data_typical_upper_limit = 1400
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 500
		sensor_upper_limit = 1500
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)/float("2")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_BATTERY_TEMPERATURE_B:
# Result is in degrees Fahrenheit.
class power_battery_temperature_B(ConversionObject):
	def __init__(self):
		data_name = "power_battery_temperature_B"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 50
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)*float("0.878906") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_BOX_TEMPERATURE:
# Result is in degrees Fahrenheit.
class power_box_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_box_temperature"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 120
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata)*float("0.878906") - float("459.688")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_HEATER_CURRENT_B:
# Result is in mA.
class power_heater_current_B(ConversionObject):
	def __init__(self):
		data_name = "power_heater_current_B"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 625
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 700
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata) * float("0.81380")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_FAN_CURRENT_B:
# Result is in mA.
class power_fan_current_B(ConversionObject):
	def __init__(self):
		data_name = "power_fan_current_B"
		data_type = "dec"
		data_typical_lower_limit = 30
		data_typical_upper_limit = 50
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 0
		sensor_upper_limit = 50
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = float(rawdata) * float("0.081380")
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_FAN_STATUS
# the first bit of the power_status byte. 1 => fan is on
#-------------------------------------------------------------------------------------------------------------------
#													POWER_HEATER_STATUS
# the second bit of the power_status byte. 1=> heater is on
#-------------------------------------------------------------------------------------------------------------------
#													POWER_ENCLOSURE_HUMIDITY
# Result is percent humidity.
class power_enclosure_humidity(ConversionObject):
	def __init__(self):
		data_name = "power_enclosure_humidity"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 30
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = 15
		sensor_upper_limit = 40
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_FAULT_STATUS
# fault.0=top fault, .1=daq box fault, .2=aux fault, .3=20WB in circuit
#-------------------------------------------------------------------------------------------------------------------
#													OLD_WIND_CHILL
#-------------------------------------------------------------------------------------------------------------------
#													NEW_WIND_CHILL

def main():
	geiger1 = ConversionObject()
	print()

if __name__ == "__main__":
    main()