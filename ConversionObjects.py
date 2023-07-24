from unicodedata import decimal
import datetime
import re
from math import log
import sys
import logging

class ConversionObject:

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
		self_string =  "\n---------------" + self.data_name + "---------------\n" + \
		"Data Type: " + self.data_type + "\n" + \
		"Typical Lower Limit: " + str(self.typical_lower_limit) + "\n" + \
		"Typical Upper Limit: " + str(self.typical_upper_limit) + "\n" + \
		"Number of Integers: "  + str(self.integer_count) + "\n" + \
		"Number of Integers After Decimal: " + str(self.decimal_count) + "\n" + \
		"Sensors Lower Limit: " + str(self.lower_limit) + "\n" + \
		"Sensors Upper Limit: " + str(self.upper_limit) + "\n"
		return self_string

	def format(self, rawdata):
		converted = float(rawdata)
		return converted
	
	def check_range(self, converted_data):
		if self.typical_lower_limit and self.typical_upper_limit:
			if converted_data >= self.typical_lower_limit:
				if converted_data <= self.typical_upper_limit:
					return 2
				else:
					return 3
			else:
				return 1
		else:
			return 0
	
class unix_time(ConversionObject):
	def __init__(self):
		data_name = "unix_time"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 6
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		# Need the fields year, month, day, hour, minute, second, clock source, and stardate
		converted = datetime.datetime.fromtimestamp(int(rawdata))
		converted_list = re.split(r"\s|-|:", str(converted))
		converted_list.append("RTC")
		return converted_list

#===================================================================================================================
#													GEIGER BLOCK
#===================================================================================================================
# Raw data format: dec5 ticks, 9, dec4 volts, dec4 amps, 9, dec5 tempr, 9, hex2 status, 13
#-------------------------------------------------------------------------------------------------------------------
#													TICKS:
# This is the number of Geiger tube ticks that occur in 1 minute.
# Typical background levels are around 100-120.
# Requires no conversion or response.

class geiger_ticks(ConversionObject):
	def __init__(self):
		data_name = "geiger_ticks"
		data_type = "dec"
		data_typical_lower_limit = 100
		data_typical_upper_limit = 120
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 5
		sensor_upper_limit = 2000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = int(rawdata)
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												HIGH VOLTS:
# This is the high voltage for the geiger tube.
# To convert from raw voltage, divide by 1024, multiply by 5, and multiply by 250.
# The result is in volts.

class geiger_high_volts(ConversionObject):
	def __init__(self):
		data_name = "geiger_high_volts"
		data_type = "dec"
		data_typical_lower_limit = 800
		data_typical_upper_limit = 900
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 800
		sensor_upper_limit = 900
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * 625) / 512
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
		sensor_lower_limit = 1
		sensor_upper_limit = 55
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * 125) / 1536
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
		converted = (((float(rawdata) * .4) - 273.16) * 1.8) + 32
		return converted

#-------------------------------------------------------------------------------------------------------------------
#|													GEIGER_STATUS

class geiger_status(ConversionObject):
	def __init__(self):
		data_name = "geiger_status"
		data_type = "hex"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 0
		integer_count = None
		decimal_count = None
		sensor_lower_limit = 0
		sensor_upper_limit = 0x0F
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata

#===================================================================================================================
#													VORTEX BLOCK
#===================================================================================================================

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
		converted = float(rawdata) / float(24)
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
		converted = float(rawdata) / float(24)
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
		converted = float(rawdata) / float(600)
		return converted

#===================================================================================================================
#													RAIN GAUGE BLOCK
#===================================================================================================================

#-------------------------------------------------------------------------------------------------------------------
#													DRIP CODE:
class rain_drip_code(ConversionObject):
	def __init__(self):
		data_name = "rain_drip_code"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		return rawdata

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
		converted = float(rawdata) / float(100)
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
		return int(rawdata)

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
		converted = float(rawdata) * 10
		return int(converted)

#-------------------------------------------------------------------------------------------------------------------
#													BATTERY VOLTAGE:
class rain_battery_voltage(ConversionObject):
	def __init__(self):
		data_name = "rain_battery_voltage"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 0
		integer_count = 0
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 0
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)
		
	def format(self, rawdata):
		return rawdata

#===================================================================================================================
#													TEMP HEAD BLOCK
#===================================================================================================================
#-------------------------------------------------------------------------------------------------------------------
#													RTD_1K_COMBINED
# Temperature in Fahrenheit
class RTD_1K_upper(ConversionObject):
	def __init__(self):
		data_name = "RTD_1K_upper"
		data_type = "hex"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 4
		sensor_lower_limit = -40
		sensor_upper_limit = 105
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		r = float.fromhex("0x" + rawdata) / 8388608 * 2.5 / .0005 / 10
		kelvin = -247.29 + (2.3992 * r) + (.00063962 * (r ** 2)) + ((1.0241 * (10 ** (-6))) * (r ** 3))
		converted = kelvin * (9 / 5) - 459.67
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RTD_100_COMBINED
# Temperature in Fahrenheit
class RTD_100_upper(ConversionObject):
	def __init__(self):
		data_name = "RTD_100_upper"
		data_type = "hex"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 4
		sensor_lower_limit = -40
		sensor_upper_limit = 105
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		r = float.fromhex("0x" + rawdata) / 8388608 * 2.5 / .0005
		kelvin = -247.29 + (2.3992 * r) + (.00063962 * (r ** 2)) + ((1.0241 * (10 ** (-6))) * (r ** 3))
		converted = kelvin * (9 / 5) - 459.67
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RTD_DAVIS_COMBINED
# Temperature in Fahrenheit
class RTD_Davis_upper(ConversionObject):
	def __init__(self):
		data_name = "RTD_Davis_upper"
		data_type = "hex"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 4
		sensor_lower_limit = -40
		sensor_upper_limit = 105
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		r = float.fromhex("0x" + rawdata) / 8388608 * 2.5 / .0005 / 10
		kelvin = -247.29 + (2.3992 * r) + (.00063962 * (r ** 2)) + ((1.0241 * (10 ** (-6))) * (r ** 3))
		converted = kelvin * (9 / 5) - 459.67
		return converted

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
		converted = (float(rawdata) * 32.2) - 25.8
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
		converted = (float(rawdata) * 32.2) - 25.8
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

	def format(self, rawdata):
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
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
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
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
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
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
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
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
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
		return converted
#-------------------------------------------------------------------------------------------------------------------
#													IR_SNOW_DEPTH
class IR_snow_depth(ConversionObject):
	def __init__(self):
		data_name = "IR_snow_depth"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 20
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 30
		self.height_of_sensor = 17.323 #in cm
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (self.height_of_sensor - ((((float(rawdata) / 65536. * 5.) ** (-0.935)) * 10650.08) - 10.)) * 0.393701
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													TEMP_HEAD_FAN_AIRFLOW:
# Result is in arbitrary units.
# Pressure of airflow
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
		converted = float(rawdata) * 5 / 131072
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
		converted = float(rawdata) * 25 / 131072
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
		converted = float(rawdata) * 5 / 786432
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													PTB_COMBINED:
# Result is in inches of mercury.
class PTB_upper(ConversionObject):
	def __init__(self):
		data_name = "PTB_upper"
		data_type = "hex"
		data_typical_lower_limit = 26
		data_typical_upper_limit = 31
		integer_count = 3
		decimal_count = 4
		sensor_lower_limit = 25
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((float.fromhex("0x" + rawdata) / 16777216 * 600) + 500) * .0295299831
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													AD_TEMPERATURE:
# Result is in degrees Fahrenheit.
class AD_temperature(ConversionObject):
	def __init__(self):
		data_name = "AD_temperature"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 90
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = 0
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((((float(rawdata) / 131072 ) * 10 ) - 2.7316) * 180) + 32
		return converted

#===================================================================================================================
#													FAN BLOCK
#===================================================================================================================

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
		converted = float(rawdata) * 25 / 1024
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
		converted = float(rawdata) * 625 / 768
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
#													ARDUINO_TEENSY_CURRENT:
# Result is in mA.
class Arduino_teensy_current(ConversionObject):
	def __init__(self):
		data_name = "Arduino_teensy_current"
		data_type = "dec"
		data_typical_lower_limit = 100
		data_typical_upper_limit = 140
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 100
		sensor_upper_limit = 150
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata) * 625 / 768
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
		converted = float(rawdata) * 625 / 768
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
		converted = int(rawdata)
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
		converted = (((float(rawdata) / 50) - 273.16) * 1.8) + 32
		return converted

#===================================================================================================================
#													TEN FOOT SENSORS
#===================================================================================================================

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
		self.height_of_sensor = 113 #in inches
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = self.height_of_sensor - (float(rawdata) / 25.4)
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BAROMETRIC_PRESSURE:
# 
class barometric_pressure(ConversionObject):
	def __init__(self):
		data_name = "barometric_pressure"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = 26
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		#long and complicated procedure
		return float(rawdata)

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
		converted = (((float(rawdata) * .4) - 273.16) * 1.8) +32
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
		converted = float(rawdata) * 125 / 1536
		return converted
#-------------------------------------------------------------------------------------------------------------------
#													ten_RTD_temperature:
# Result is in watts per meter squared
class ten_RTD_temperature(ConversionObject):
	def __init__(self):
		data_name = "ten_RTD_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = -30
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 4.096 #not sure if this is right
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													RH_PRECON:
# Result is humidity rounded to 1 decimal place.
class RH_Precon(ConversionObject):
	def __init__(self):
		data_name = "RH_Precon"
		data_type = "dec"
		data_typical_lower_limit = 10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 5
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = float(rawdata) / 131072 * 408.86 / 5
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
		converted = ((float(rawdata) / 131072 * 4.0886 / .02137) - 22) * .818
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
		converted = float(rawdata) * 32.2 - 25.8
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													TEN_AVG_WIND_SPEED:
# Result is humidity rounded to 1 decimal place.
class ten_avg_wind_speed(ConversionObject):
	def __init__(self):
		data_name = "ten_avg_wind_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		return int(rawdata) #tbd
	
#-------------------------------------------------------------------------------------------------------------------
#													TEN_INSTANT_WIND_SPEED:
# Result is humidity rounded to 1 decimal place.
class ten_instant_wind_speed(ConversionObject):
	def __init__(self):
		data_name = "ten_instant_wind_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		return float(rawdata) #tbd
	
#-------------------------------------------------------------------------------------------------------------------
#													TEN_WIND_DIRECTION:
# Result is humidity rounded to 1 decimal place.
class ten_wind_direction(ConversionObject):
	def __init__(self):
		data_name = "ten_wind_direction"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		return float(rawdata) #tbd

#===================================================================================================================
#													POWER SUPPLY BLOCK
#===================================================================================================================

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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 167 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 167 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 185 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 185 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = float(rawdata) / 1.2
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
		converted = float(rawdata) / 1000 * 5.02
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_BATTERY_CURRENT:
# Result is in mA.
class power_battery_current(ConversionObject):
	def __init__(self):
		data_name = "power_battery_current"
		data_type = "dec"
		data_typical_lower_limit = 2000
		data_typical_upper_limit = -15000
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = -15000
		sensor_upper_limit = 2000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		converted = (float(rawdata) - 2500) / 83 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 83 * 1000
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = (float(rawdata) - 2500) / 185 * 1000
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
		converted = float(rawdata) / 60
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
		converted = float(rawdata) / 6
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
		converted = (float(rawdata) - 2731.6) * .18 + 32
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
		converted = (float(rawdata) - 2731.6) * .18 + 32
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
		converted = (float(rawdata) - 2731.6) * .18 + 32
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
		converted = float(rawdata) / 500
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
		converted = float(rawdata) / 500
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
		converted = float(rawdata) / 6
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = float(rawdata) / 6
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
		converted = float(rawdata) / 1000 * 5.02
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
		converted = float(rawdata) / 6
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
		converted = float(rawdata) / 2
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
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.7316) * 180) + 32
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
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.7316) * 180) + 32
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
		converted = (((float(rawdata) / 1024 ) * 5 ) / 6) * 1000
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
		converted = (((float(rawdata) / 1024 ) * 5 ) / 60) * 1000
		return converted

#-------------------------------------------------------------------------------------------------------------------
#													POWER_STATUS
# first bit of the power_status byte: 1 => fan is on
# second bit of the power_status byte: 1=> heater is on
class power_status(ConversionObject):
	def __init__(self):
		data_name = "power_status"
		data_type = "dec"
		data_typical_lower_limit = "00"
		data_typical_upper_limit = "11"
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
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
		return float(rawdata)

#-------------------------------------------------------------------------------------------------------------------
#													POWER_FAULT_STATUS
# fault.0=top fault, .1=daq box fault, .2=aux fault, .3=20WB in circuit
class power_fault_status(ConversionObject):
	def __init__(self):
		data_name = "power_fault_status"
		data_type = "dec"
		data_typical_lower_limit = "0000"
		data_typical_upper_limit = "1111"
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_TEMP_BELOW:
# Sensors are 100 ohm TRD
class soil_temp_below(ConversionObject):
	def __init__(self):
		data_name = "soil_temp_below"
		data_type = "dec"
		data_typical_lower_limit = -10
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		value = float(rawdata) / 524288 * 4.096 / 10
		r = (20000 * value) / (4.096 - value)
		kelvin = -247.29 + (2.3992 * r) + (.00063962 * (r ** 2)) + ((1.0241 * (10 ** (-6))) * (r ** 3))
		converted = kelvin * (9 / 5) - 459.67
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_MOIST:
# Value is in volts
class soil_moist(ConversionObject):
	def __init__(self):
		data_name = "soil_moist"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 50
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 50
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		value = float(rawdata) / 1000
		try:
			assert (value >= 0 and value <= 2.2), "Soil moist value out of index"
		except AssertionError as err:
			logging.error(f"{err}")
			converted = value
		else:
			if value >= 0 and value < 1.1:
				converted = 10 * value - 1
			elif value >= 1.1 and value < 1.3:
				converted = 25 * value - 17.5
			elif value >= 1.3 and value < 1.82:
				converted = 48.08 * value - 47.5
			elif value >= 1.82 and value <= 2.2:
				converted = 26.32 * value - 7.89
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_TEMP_ABOVE:
class soil_temp_above(ConversionObject):
	def __init__(self):
		data_name = "soil_temp_above"
		data_type = "dec"
		data_typical_lower_limit = -20
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = -30
		sensor_upper_limit = 120
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		r = (float(rawdata) / 131072 * 4.096 * 20000) / (4.096 - (float(rawdata) / 131072 * 4.096))
		a = .001125308852122
		b = .000234711863267
		c = .000000085663516
		kelvin = 1 / (a + (b * log(r)) + (c * (log(r) ** 3)))
		converted = kelvin * (9 / 5) - 459.67
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_FLUX:
# Result is in watts per meter squared
class soil_flux(ConversionObject):
	def __init__(self):
		data_name = "soil_flux"
		data_type = "dec"
		data_typical_lower_limit = .2
		data_typical_upper_limit = .8
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .15
		sensor_upper_limit = .85
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 262144 * 4.096 - .5026
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_ELECTRONICS_TEMP:
# Temperature is in Fahrenheit
class soil_electronics_temp(ConversionObject):
	def __init__(self):
		data_name = "soil_electronics_temp"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 20
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.7316) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_ELECTRONICS_VREF:
# In volts
class soil_electronics_Vref(ConversionObject):
	def __init__(self):
		data_name = "soil_electronics_Vref"
		data_type = "dec"
		data_typical_lower_limit = 4.096
		data_typical_upper_limit = 4.096
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = 4.08
		sensor_upper_limit = 4.1
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024 ) * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOIL_SPARE:
# For future use
class soil_spare(ConversionObject):
	def __init__(self):
		data_name = "soil_spare"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													GEIGER_BURST_COUNT:
# Not sure
class Geiger_burst_count(ConversionObject):
	def __init__(self):
		data_name = "Geiger_burst_count"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													GEIGER_BURST_TIME:
# Not sure
class Geiger_burst_time(ConversionObject):
	def __init__(self):
		data_name = "Geiger_burst_time"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata) # need to change
	
#-------------------------------------------------------------------------------------------------------------------
#													BAROMETRIC_TEMPERATURE:
# Not sure
class barometric_temperature(ConversionObject):
	def __init__(self):
		data_name = "barometric_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata) # need to change
	
#-------------------------------------------------------------------------------------------------------------------
#													LOAD_DCDC_VOLTAGE_INPUT:
# In volts
class load_dcdc_voltage_input(ConversionObject):
	def __init__(self):
		data_name = "load_dcdc_voltage_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 20
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LOAD_DCDC_CURRENT_INPUT:
# In amps
class load_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "load_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 8
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LOAD_DCDC_CURRENT_OUTPUT:
# In amps
class load_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "load_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = 1
		sensor_upper_limit = 3
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LOAD_DCDC_VOLTAGE_OUTPUT:
# In volts
class load_dcdc_voltage_output(ConversionObject):
	def __init__(self):
		data_name = "load_dcdc_voltage_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 12
		sensor_upper_limit = 15
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 200
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												BATTERY_CHARGER_CURRENT_INPUT:
# In amps
class battery_charger_current_input(ConversionObject):
	def __init__(self):
		data_name = "battery_charger_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 4
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												BATTERY_CHARGER_CURRENT_OUTPUT:
# In amps
class battery_charger_current_output(ConversionObject):
	def __init__(self):
		data_name = "battery_charger_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 5
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BATTERY_CHARGER_TEMPERATURE:
# Temperature is in Fahrenheit
class battery_charger_temperature(ConversionObject):
	def __init__(self):
		data_name = "battery_charger_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((float(rawdata)  - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BATTERY_CHARGER_VOLTAGE_OUTPUT:
# In volts
class battery_charger_voltage_output(ConversionObject):
	def __init__(self):
		data_name = "battery_charger_voltage_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 12
		sensor_upper_limit = 16
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 200
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOLAR_DCDC_INPUT_VOLTAGE:
# In volts
class solar_dcdc_input_voltage(ConversionObject):
	def __init__(self):
		data_name = "solar_dcdc_input_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 15
		sensor_upper_limit = 24
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_DCDC_INPUT_CURRENT:
# In amps
class solar_dcdc_input_current(ConversionObject):
	def __init__(self):
		data_name = "solar_dcdc_input_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 6
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 600
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_CHARGER_CURRENT_OUTPUT:
# In amps
class solar_charger_current_output(ConversionObject):
	def __init__(self):
		data_name = "solar_charger_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 5
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 600
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													SOLAR_CHARGER_VOLTAGE_OUTPUT:
# In volts
class solar_charger_voltage_output(ConversionObject):
	def __init__(self):
		data_name = "solar_charger_voltage_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 12
		sensor_upper_limit = 16
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 200
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LOAD_VOLTAGE:
# In volts
class load_voltage(ConversionObject):
	def __init__(self):
		data_name = "load_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 12
		sensor_upper_limit = 16
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 200
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BATTERY_VOLTAGE:
# In volts
class battery_voltage(ConversionObject):
	def __init__(self):
		data_name = "battery_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 11
		sensor_upper_limit = 15
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 200
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BATTERY_TEMPERATURE:
# Temperature is in Fahrenheit
class battery_temperature(ConversionObject):
	def __init__(self):
		data_name = "battery_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													BATTERY_PROTECTION_STATUS:
class battery_protection_status(ConversionObject):
	def __init__(self):
		data_name = "battery_protection_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													WEATHERPROOF_ENCLOSURE_TEMPERATURE:
# Temperature is in Fahrenheit
class weatherproof_enclosure_temperature(ConversionObject):
	def __init__(self):
		data_name = "weatherproof_enclosure_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((float(rawdata)  - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_SUPPLY_BOX_TEMPERATURE:
# Temperature is in Fahrenheit
class power_supply_box_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_supply_box_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((float(rawdata)  - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_SUPPLY_HUMIDITY:
# %RH
class power_supply_humidity(ConversionObject):
	def __init__(self):
		data_name = "power_supply_humidity"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = 60
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													30V_SUPPLY_FAN_SPEED:
# rpm
class V30_supply_fan_speed(ConversionObject): #have to change name because Python doesn't allow classes to start with a digit
	def __init__(self):
		data_name = "V30_supply_fan_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = 10
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * 60
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												30V_SUPPLY_FAN_CURRENT:
# In mA
class V30_supply_fan_current(ConversionObject):
	def __init__(self):
		data_name = "V30_supply_fan_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = .01
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 10000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												30V_SUPPLY_CURRENT_OUTPUT:
# In mA
class V30_supply_current_output(ConversionObject):
	def __init__(self):
		data_name = "V30_supply_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = .1
		sensor_upper_limit = 8
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) - 58) / 191
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												30V_SUPPLY_VOLTAGE_OUTPUT:
# In volts
class V30_supply_voltage_output(ConversionObject):
	def __init__(self):
		data_name = "V30_supply_voltage_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 30
		sensor_upper_limit = 50
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 50
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											30V_SUPPLY_24V_SUPPLY_VOLTAGE:
# In volts
class V30_supply_24V_supply_voltage(ConversionObject):
	def __init__(self):
		data_name = "V30_supply_24V_supply_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 22
		sensor_upper_limit = 26
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											30V_CONVERTER_BOARD_CURRENT_INPUT:
# In mA
class V30_converter_board_current_input(ConversionObject):
	def __init__(self):
		data_name = "V30_converter_board_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = .5
		sensor_upper_limit = 8
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 60 / .01
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											30V_CONVERTER_BOARD_VOLTAGE_INPUT:
# In volts
class V30_converter_board_voltage_input(ConversionObject):
	def __init__(self):
		data_name = "V30_converter_board_voltage_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 20
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 50
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													MOSFET_SWITCHES_STATUS:
class MOSFET_switches_status(ConversionObject):
	def __init__(self):
		data_name = "MOSFET_switches_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#											PROTECTION_RAW_VOLTAGE
# In volts
class protection_raw_voltage(ConversionObject):
	def __init__(self):
		data_name = "protection_raw_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 20
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5 * 10.09
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											PROTECTION_PROTECTED_VOLTAGE
# In volts
class protection_protected_voltage(ConversionObject):
	def __init__(self):
		data_name = "protection_protected_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 20
		sensor_upper_limit = 32
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5 * 10.09
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											PROTECTION_RAW_INPUT_CURRENT:
# In amps
class protection_raw_input_current(ConversionObject):
	def __init__(self):
		data_name = "protection_raw_input_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = .1
		sensor_upper_limit = 8
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) - 2.5) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											PROTECTION_CIRCUIT_STATUS:
class protection_circuit_status(ConversionObject):
	def __init__(self):
		data_name = "protection_circuit_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												MUX_CURRENT:
# In mA
class mux_current(ConversionObject):
	def __init__(self):
		data_name = "mux_current"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 430
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 12
		sensor_upper_limit = 490
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													MUX_TEMPERATURE:
# Temperature is in Fahrenheit
class mux_temperature(ConversionObject):
	def __init__(self):
		data_name = "mux_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WIND_RATE:
class Peet_wind_rate(ConversionObject):
	def __init__(self):
		data_name = "Peet_wind_rate"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WIND_MULTL:
class Peet_wind_multl(ConversionObject):
	def __init__(self):
		data_name = "Peet_wind_multl"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WINDLO:
class Peet_windlo(ConversionObject):
	def __init__(self):
		data_name = "Peet_windlo"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WIND_MULTH:
class Peet_wind_multh(ConversionObject):
	def __init__(self):
		data_name = "Peet_wind_multh"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WINDHI:
class Peet_windhi(ConversionObject):
	def __init__(self):
		data_name = "Peet_windhi"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_VDUCE:
class Peet_vduce(ConversionObject):
	def __init__(self):
		data_name = "Peet_vduce"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													PEET_WINDDIR:
class Peet_winddir(ConversionObject):
	def __init__(self):
		data_name = "Peet_winddir"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												INSPEED_WIND_DIRECTION:
# Direction in degrees
class Inspeed_wind_direction(ConversionObject):
	def __init__(self):
		data_name = "Inspeed_wind_direction"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) - 3277) / 58982 * 360
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												HYDREON_CURRENT:
# In mA
class Hydreon_current(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_current"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 150
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 30) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													HYDREON_TEMPERATURE:
# Temperature is in Fahrenheit
class Hydreon_temperature(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													HYDREON_RANGE_SETTING:
class Hydreon_range_setting(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_range_setting"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		value = int(rawdata)
		if value == 0:
			converted = .01
		elif value == 2:
			converted = .001
		elif value == 4:
			converted = .0001
		else:
			converted = value
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													HYDREON_LOW_SENSE:
# Rain is in inches
class Hydreon_low_sense(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_low_sense"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .01
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													HYDREON_MEDIUM_SENSE:
# Rain is in inches
class Hydreon_medium_sense(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_medium_sense"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = 0
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													HYDREON_HIGH_SENSE:
# Rain is in inches
class Hydreon_high_sense(ConversionObject):
	def __init__(self):
		data_name = "Hydreon_high_sense"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = 0
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .0001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_SENSOR_CURRENT:
# In mA
class sky_sensor_current(ConversionObject):
	def __init__(self):
		data_name = "sky_sensor_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 60) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_SWIPER_CW_CURRENT:
# In mA
class sky_swiper_CW_current(ConversionObject):
	def __init__(self):
		data_name = "sky_swiper_CW_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 60) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_SWIPER_CCW_CURRENT:
# In mA
class sky_swiper_CCW_current(ConversionObject):
	def __init__(self):
		data_name = "sky_swiper_CCW_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 60) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_DARK_READING:
# Result in lux
class sky_dark_reading(ConversionObject):
	def __init__(self):
		data_name = "sky_dark_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 6
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 65536) * 5) * 1000) / 3.399
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_BRIGHT_READING:
# Result in lux
class sky_bright_reading(ConversionObject):
	def __init__(self):
		data_name = "sky_bright_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 6
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 65536) * 5) * 1000) / 3.399
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_IR_TEMPERATURE:
# Temperature is in Fahrenheit
class sky_IR_temperature(ConversionObject):
	def __init__(self):
		data_name = "sky_IR_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 50) - 2.7315) * 180) + 32
		return converted

#-------------------------------------------------------------------------------------------------------------------
#											SKY_SENSOR_STATUS:
class sky_sensor_status(ConversionObject):
	def __init__(self):
		data_name = "sky_sensor_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												SKY_HALL_SENSOR:
# Voltage proportional to hall sensor reading
class sky_Hall_sensor(ConversionObject):
	def __init__(self):
		data_name = "sky_Hall_sensor"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_X40_READING:
# In volts
class sway_X40_reading(ConversionObject):
	def __init__(self):
		data_name = "sway_X40_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_X1_READING:
# In volts
class sway_X1_reading(ConversionObject):
	def __init__(self):
		data_name = "sway_X1_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_Y1_READING:
# In volts
class sway_Y1_reading(ConversionObject):
	def __init__(self):
		data_name = "sway_Y1_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_Y40_READING:
# In volts
class sway_Y40_reading(ConversionObject):
	def __init__(self):
		data_name = "sway_Y40_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_SENSOR_TEMPERATURE:
# Temperature is in Fahrenheit
class sway_sensor_temperature(ConversionObject):
	def __init__(self):
		data_name = "sway_sensor_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) * .001) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_SENSOR_VSS:
# In volts
class sway_sensor_Vss(ConversionObject):
	def __init__(self):
		data_name = "sway_sensor_Vss"
		data_type = "dec"
		data_typical_lower_limit = 3.3
		data_typical_upper_limit = 3.3
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 3.1
		sensor_upper_limit = 3.4
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_Z_OFFSET:
# In volts
class sway_Z_offset(ConversionObject):
	def __init__(self):
		data_name = "sway_Z_offset"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_Z50_READING:
# In volts
class sway_Z50_reading(ConversionObject):
	def __init__(self):
		data_name = "sway_Z50_reading"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_CURRENT:
# In mA
class lightning_current(ConversionObject):
	def __init__(self):
		data_name = "lightning_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 60) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_UV_COUNT:
# Count of UVtron ticks
class lightning_UV_count(ConversionObject):
	def __init__(self):
		data_name = "lightning_UV_count"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_HIGH_VOLTAGE:
# In volts
class lightning_high_voltage(ConversionObject):
	def __init__(self):
		data_name = "lightning_high_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = ((float(rawdata) / 1024) * 5) * 214
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_3001_LUX:
# In lux
class lightning_3001_lux(ConversionObject):
	def __init__(self):
		data_name = "lightning_3001_lux"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 5
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = str(bin(int(rawdata))) #convert the data into a binary string
		converted = converted[2:] #take off the '0b' at the start of the string
		upper_bits = ""
		lower_bits = ""
		
		converted_length = len(converted)
		try:
			assert (converted_length == 15 or converted_length == 16), "Lightning 3001 lux value does not have correct number of bits"
		except AssertionError as err:
			logging.error(f"{err}")
			return 0
		else:
			if converted_length == 15:
				upper_bits = converted[:3]
				lower_bits = converted[3:]
			else:
				upper_bits = converted[:4]
				lower_bits = converted[4:]
			lux = .01 * (2 ** int(upper_bits, 2)) * int(lower_bits, 2)
			return lux
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_SKYSCAN_CURRENT:
# In mA
class lightning_Skyscan_current(ConversionObject):
	def __init__(self):
		data_name = "lightning_Skyscan_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 1024) * 5) / 30) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_SKYSCAN_LEDS:
class lightning_Skyscan_LEDs(ConversionObject):
	def __init__(self):
		data_name = "lightning_Skyscan_LEDs"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_SKYSCAN_FLASH_TIME:
# Indicates relative time of optical lightning flash
class lightning_Skyscan_flash_time(ConversionObject):
	def __init__(self):
		data_name = "lightning_Skyscan_flash_time"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_SKYSCAN_ALARMS:
class lightning_Skyscan_alarms(ConversionObject):
	def __init__(self):
		data_name = "lightning_Skyscan_alarms"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_BASELINE:
# In volts
class lightning_OPT101_baseline(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_baseline"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_NORTH:
# In volts
class lightning_OPT101_north(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_north"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_SOUTH:
# In volts
class lightning_OPT101_south(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_south"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_EAST:
# In volts
class lightning_OPT101_east(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_east"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_WEST:
# In volts
class lightning_OPT101_west(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_west"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_OPT101_ZENITH:
# In volts
class lightning_OPT101_zenith(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT101_zenith"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_THUNDER:
# In volts
class lightning_thunder(ConversionObject):
	def __init__(self):
		data_name = "lightning_thunder"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_FLAG:
class lightning_flag(ConversionObject):
	def __init__(self):
		data_name = "lightning_flag"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													LIGHTNING_UVA_UVB:
# In mW/cm^2
class lightning_UVA_UVB(ConversionObject):
	def __init__(self):
		data_name = "lightning_UVA_UVB"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 - 1) * 8.2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												LIGHTNING_OPT_TEMPERATURE:
# Temperature is in Fahrenheit
class lightning_OPT_temperature(ConversionObject):
	def __init__(self):
		data_name = "lightning_OPT_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) * .001) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_BOX_TEMPERATURE:
# Temperature is in Fahrenheit
class solar_box_temperature(ConversionObject):
	def __init__(self):
		data_name = "solar_box_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 65536 * 10) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_PYRAN_COMBINED:
# In watts per meter squared
class solar_pyran_upper_byte(ConversionObject):
	def __init__(self):
		data_name = "solar_pyran_upper_byte"
		data_type = "hex"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 1100
		integer_count = 4
		decimal_count = 4
		sensor_lower_limit = 0
		sensor_upper_limit = 1200
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 16777216 * 25 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_PAR_COMBINED:
# In umol per meter squared per second squared
class solar_par_upper_byte(ConversionObject):
	def __init__(self):
		data_name = "solar_par_upper_byte"
		data_type = "hex"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 2000
		integer_count = 4
		decimal_count = 4
		sensor_lower_limit = 0
		sensor_upper_limit = 2100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 16777216 * 25 * 1000
		return converted

	#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_UV_COMBINED:
# In watts per meter squared
class solar_UV_upper_byte(ConversionObject):
	def __init__(self):
		data_name = "solar_UV_upper_byte"
		data_type = "hex"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 170
		integer_count = 4
		decimal_count = 4
		sensor_lower_limit = 0
		sensor_upper_limit = 175
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 16777216 * 5 * 1.65 * 1000
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_GOLD_GRID_EAST:
# In volts
class solar_gold_grid_east(ConversionObject):
	def __init__(self):
		data_name = "solar_gold_grid_east"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 4
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_GOLD_GRID_WEST:
# In volts
class solar_gold_grid_west(ConversionObject):
	def __init__(self):
		data_name = "solar_gold_grid_west"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 4
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_DECAGON_HORIZONTAL:
# In volts
class solar_Decagon_horizontal(ConversionObject):
	def __init__(self):
		data_name = "solar_Decagon_horizontal"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 4
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 5
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_DECAGON_TILTED:
# In volts
class solar_Decagon_tilted(ConversionObject):
	def __init__(self):
		data_name = "solar_Decagon_tilted"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 5
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_FROST:
class solar_frost(ConversionObject):
	def __init__(self):
		data_name = "solar_frost"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = 24900 * (5 / (float(rawdata) / 65536 * 5) - 1)
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_BUD:
class solar_bud(ConversionObject):
	def __init__(self):
		data_name = "solar_bud"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = 24900 * (5 / (float(rawdata) / 65536 * 5) - 1)
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_GLOBE_COMBINED:
class solar_globe_upper_byte(ConversionObject):
	def __init__(self):
		data_name = "solar_globe_upper_byte"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 4
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 16777261 * 5 * 1000
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_CURRENT:
# In mA
class solar_current(ConversionObject):
	def __init__(self):
		data_name = "solar_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 5 / 30 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_VOLTAGE:
# In volts
class solar_voltage(ConversionObject):
	def __init__(self):
		data_name = "solar_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 50
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SOLAR_IR_GROUND_TEMPERATURE:
# Temperature is in Fahrenheit
class solar_IR_ground_temperature(ConversionObject):
	def __init__(self):
		data_name = "solar_IR_ground_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) / 50) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												METONE_LED_CURRENT:
# In mA
class MetOne_LED_current(ConversionObject):
	def __init__(self):
		data_name = "MetOne_LED_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 600 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												METONE_WIND_SPEED_AVERAGE:
# Number of ticks in a 60 second period, rolling average
class MetOne_wind_speed_average(ConversionObject):
	def __init__(self):
		data_name = "MetOne_wind_speed_average"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 8) / 16.787 + .63
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												METONE_WIND_SPEED_GUST:
# Count of ticks in 3 seconds to get the gust
class MetOne_wind_speed_gust(ConversionObject):
	def __init__(self):
		data_name = "MetOne_wind_speed_gust"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 8) * 20 / 1.788 + .63
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_ARBCAM_CURRENT:
# In mA
class fuses_Arbcam_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_Arbcam_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												FUSES_ARBCAM_VOLTAGE:
# In volts
class fuses_Arbcam_voltage(ConversionObject):
	def __init__(self):
		data_name = "fuses_Arbcam_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 * 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_5.6_VOLTAGE:
# In volts
class fuses_5_6_voltage(ConversionObject): #had to change name because not valid python class
	def __init__(self):
		data_name = "fuses_5_6_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 * 2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_MUX_CURRENT:
# In mA
class fuses_mux_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_mux_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_LIGHTNING_CURRENT:
# In mA
class fuses_lightning_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_lightning_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												FUSES_SOLAR_DAQ_CURRENT:
# In mA
class fuses_solar_DAQ_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_solar_DAQ_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_FLUXGATE_CURRENT:
# In mA, uses 1 ohm sense resistor
class fuses_fluxgate_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_fluxgate_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 60 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_TRIAXIAL_CURRENT:
# In mA
class fuses_triaxial_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_triaxial_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_FUTURE_CURRENT:
# In mA
class fuses_future_current(ConversionObject):
	def __init__(self):
		data_name = "fuses_future_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_FLAG:
class fuses_flag(ConversionObject):
	def __init__(self):
		data_name = "fuses_flag"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_WARN:
class fuses_warn(ConversionObject):
	def __init__(self):
		data_name = "fuses_warn"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_GO_UP:
class fuses_go_up(ConversionObject):
	def __init__(self):
		data_name = "fuses_go_up"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_MONITOR:
class fuses_monitor(ConversionObject):
	def __init__(self):
		data_name = "fuses_monitor"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_ARBCAM_MODE:
class fuses_Arbcam_mode(ConversionObject):
	def __init__(self):
		data_name = "fuses_Arbcam_mode"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												FUSES_FAULT_STATUS:
class fuses_fault_status(ConversionObject):
	def __init__(self):
		data_name = "fuses_fault_status"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_SOLAR_PANEL_CURRENT:
# In mA
class power_solar_panel_current(ConversionObject):
	def __init__(self):
		data_name = "power_solar_panel_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_SOLAR_PANEL_VOLTAGE:
# In volts
class power_solar_panel_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_solar_panel_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_BATTERY_CURRENT_B:
# In mA
class power_battery_current_B(ConversionObject):
	def __init__(self):
		data_name = "power_battery_current_B"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_BATTERY_VOLTAGE_B:
# In volts
class power_battery_voltage_B(ConversionObject):
	def __init__(self):
		data_name = "power_battery_voltage_B"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_CURRENT_INTO_5.6:
# In mA
class power_current_into_5_6(ConversionObject): #have to rename because not acceptable python class name
	def __init__(self):
		data_name = "power_current_into_5_6"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_VOLTAGE_INTO_5.6:
# In volts
class power_voltage_into_5_6(ConversionObject):
	def __init__(self):
		data_name = "power_voltage_into_5_6"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_5.6_LOAD_CURRENT:
# In mA
class power_5_6_load_current(ConversionObject):
	def __init__(self):
		data_name = "power_5_6_load_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_5.6_LOAD_VOLTAGE:
# In volts
class power_5_6_load_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_5_6_load_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_BOX_TEMPERATURE_B:
# Temperature is in Fahrenheit
class power_box_temperature_B(ConversionObject):
	def __init__(self):
		data_name = "power_box_temperature_B"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) * .001) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_ARBCAM_DC/DC_INPUT_CURRENT:
# In mA
class power_Arbcam_dcdc_input_current(ConversionObject):
	def __init__(self):
		data_name = "power_Arbcam_dcdc_input_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_ARBCAM_DC/DC_INPUT_VOLTAGE:
# In volts
class power_Arbcam_dcdc_input_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_Arbcam_dcdc_input_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_ARBCAM_CURRENT:
# In mA
class power_Arbcam_current(ConversionObject):
	def __init__(self):
		data_name = "power_Arbcam_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 / 6) * 1000
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_ARBCAM_VOLTAGE:
# In volts
class power_Arbcam_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_Arbcam_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001) * 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_BATTERY_TEMPERATURE:
# Temperature is in Fahrenheit
class power_battery_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_battery_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (((float(rawdata) * .001) - 2.7315) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_128K_BATTERY_VOLTAGE:
# In volts, not implemented
class power_128K_battery_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_128K_battery_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_RTC_BATTERY_VOLTAGE:
# In volts, not implemented
class power_RTC_battery_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_RTC_battery_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_RTD_30FT_TEMPERATURE:
class power_RTD_30ft_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_RTD_30ft_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 65536 * 4.096
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_HAIL_PEAK:
# Maximum hail hit voltage per 20 second cycle
class power_hail_peak(ConversionObject):
	def __init__(self):
		data_name = "power_hail_peak"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_HAIL_AVERAGE:
# Average hail hits voltage
class power_hail_average(ConversionObject):
	def __init__(self):
		data_name = "power_hail_average"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_STATUS_B:
class power_status_B(ConversionObject):
	def __init__(self):
		data_name = "power_status_B"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_OVP_CYCLES:
# Indicates the number of hail power ovp protection cycles
class power_OVP_cycles(ConversionObject):
	def __init__(self):
		data_name = "power_OVP_cycles"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												POWER_OVP_VOLTAGE:
class power_OVP_voltage(ConversionObject):
	def __init__(self):
		data_name = "power_OVP_voltage"
		data_type = "dec"
		data_typical_lower_limit = 5.6
		data_typical_upper_limit = 5.6
		integer_count = 1
		decimal_count = 2
		sensor_lower_limit = 5.4
		sensor_upper_limit = 5.8
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 1024 * 5 * 2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_HAIL_SENSOR_TEMPERATURE:
# Result is in degrees Fahrenheit
class power_hail_sensor_temperature(ConversionObject):
	def __init__(self):
		data_name = "power_hail_sensor_temperature"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 100
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 50
		sensor_upper_limit = 100
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_HAIL_SENSOR_HITS:
# Reads directly in number of precip hits in the 20 second window
class power_hail_sensor_hits(ConversionObject):
	def __init__(self):
		data_name = "power_hail_sensor_hits"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													POWER_BOX_HUMIDITY:
# Reads directly in percent relative humidity
class power_box_humidity(ConversionObject):
	def __init__(self):
		data_name = "power_box_humidity"
		data_type = "dec"
		data_typical_lower_limit = 20
		data_typical_upper_limit = 30
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = 15
		sensor_upper_limit = 40
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												SWAY_SENSOR_XY_DATA:
# Data point is in g, limits +/-2.3g
class sway_sensor_XY_data(ConversionObject):
	def __init__(self):
		data_name = "sway_sensor_XY_data"
		data_type = "dec"
		data_typical_lower_limit = 1600
		data_typical_upper_limit = 1700
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = 980
		sensor_upper_limit = 2300
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) * .001 - 1.65) / .3
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_MAGNETOMETER_T_DATA:
# Value is the place of the given reading
class fluxgate_magnetometer_t_data(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_magnetometer_t_data"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 14
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 14
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_MAGNETOMETER_XYZ_DATA:
# In Hz
class fluxgate_magnetometer_xyz_data(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_magnetometer_xyz_data"
		data_type = "dec"
		data_typical_lower_limit = 7000
		data_typical_upper_limit = 9000
		integer_count = 5
		decimal_count = 0
		sensor_lower_limit = 1000
		sensor_upper_limit = 12500
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * 10
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_CURRENT:
# In mA
class fluxgate_current(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_current"
		data_type = "dec"
		data_typical_lower_limit = 125
		data_typical_upper_limit = 600
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 125
		sensor_upper_limit = 980
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 6 * 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													FLUXGATE_TEMPERATURE:
# Result is in degrees Fahrenheit
class fluxgate_temperature(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_temperature"
		data_type = "dec"
		data_typical_lower_limit = 2380
		data_typical_upper_limit = 3160
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = 2350
		sensor_upper_limit = 3175
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_XSET:
# In volts
class fluxgate_xset(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_xset"
		data_type = "dec"
		data_typical_lower_limit = 1800
		data_typical_upper_limit = 2200
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 4000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_YSET:
# In volts
class fluxgate_yset(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_yset"
		data_type = "dec"
		data_typical_lower_limit = 1800
		data_typical_upper_limit = 2200
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 4000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_ZSET:
# In volts
class fluxgate_zset(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_zset"
		data_type = "dec"
		data_typical_lower_limit = 1800
		data_typical_upper_limit = 2200
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 4000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) * .001
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FLUXGATE_FLAG:
class fluxgate_flag(ConversionObject):
	def __init__(self):
		data_name = "fluxgate_flag"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 3
		integer_count = None
		decimal_count = None
		sensor_lower_limit = 0
		sensor_upper_limit = 3
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												TRIAXIAL_MAGNETOMETER_T_DATA:
# Value is the place in the sequence of data points
class triaxial_magnetometer_t_data(ConversionObject):
	def __init__(self):
		data_name = "triaxial_magnetometer_t_data"
		data_type = "dec"
		data_typical_lower_limit = 0
		data_typical_upper_limit = 20
		integer_count = 2
		decimal_count = 0
		sensor_lower_limit = 0
		sensor_upper_limit = 20
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												TRIAXIAL_MAGNETOMETER_XYZ_DATA:
# In uTesla
class triaxial_magnetometer_xyz_data(ConversionObject):
	def __init__(self):
		data_name = "triaxial_magnetometer_xyz_data"
		data_type = "dec"
		data_typical_lower_limit = 1500
		data_typical_upper_limit = 5000
		integer_count = 3
		decimal_count = 2
		sensor_lower_limit = 0
		sensor_upper_limit = 32000
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 62.48
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												TRIAXIAL_CURRENT:
# In mA
class triaxial_current(ConversionObject):
	def __init__(self):
		data_name = "triaxial_current"
		data_type = "dec"
		data_typical_lower_limit = 15
		data_typical_upper_limit = 15
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = 5
		sensor_upper_limit = 30
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 / 30 * 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												TRIAXIAL_VOLTS:
# In volts
class triaxial_volts(ConversionObject):
	def __init__(self):
		data_name = "triaxial_volts"
		data_type = "dec"
		data_typical_lower_limit = 5
		data_typical_upper_limit = 5
		integer_count = 1
		decimal_count = 3
		sensor_lower_limit = 4.8
		sensor_upper_limit = 5.2
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) / 1024) * 5 * 2
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													TRIAXIAL_TEMPERATURE:
# Result is in degrees Fahrenheit
class triaxial_temperature(ConversionObject):
	def __init__(self):
		data_name = "triaxial_temperature"
		data_type = "dec"
		data_typical_lower_limit = -40
		data_typical_upper_limit = 110
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = -40
		sensor_upper_limit = 110
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit) 


	def format(self, rawdata):
		converted = ((((float(rawdata) / 1024 ) * 5 ) - 2.73) * 180) + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PURPLEAIR_DC/DC_CURRENT_INPUT:
# In mA
class PurpleAir_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "PurpleAir_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted

#-------------------------------------------------------------------------------------------------------------------
#												PURPLEAIR_DC/DC_CURRENT_OUTPUT:
# In mA
class PurpleAir_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "PurpleAir_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PURPLEAIR_DC/DC_VOLTAGE:
# In volts
class PurpleAir_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "PurpleAir_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PARTICLES_DC/DC_CURRENT_INPUT:
# In mA
class Particles_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "Particles_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PARTICLES_DC/DC_CURRENT_OUTPUT:
# In mA
class Particles_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "Particles_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PARTICLES_DC/DC_VOLTAGE:
# In volts
class Particles_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "Particles_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												PARTICLES_DC/DC_TEMPERATURE:
# In degrees Fahrenheit
class Particles_dcdc_temperature(ConversionObject):
	def __init__(self):
		data_name = "Particles_dcdc_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) - 2731.6) * .18 + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_BOX_FANS_VOLTAGE:
# In volts
class Aux_box_fans_voltage(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_fans_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_B_DC/DC_CURRENT_INPUT:
# In mA
class Aux_B_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "Aux_B_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_B_DC/DC_CURRENT_OUTPUT:
# In mA
class Aux_B_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "Aux_B_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_B_DC/DC_VOLTAGE:
# In volts
class Aux_B_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "Aux_B_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_A_DC/DC_CURRENT_INPUT:
# In mA
class Aux_A_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "Aux_A_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_A_DC/DC_CURRENT_OUTPUT:
# In mA
class Aux_A_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "Aux_A_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_A_DC/DC_VOLTAGE:
# In volts
class Aux_A_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "Aux_A_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_A_DC/DC_TEMPERATURE:
# In degrees Fahrenheit
class Aux_A_dcdc_temperature(ConversionObject):
	def __init__(self):
		data_name = "Aux_A_dcdc_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) - 2731.6) * .18 + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_A_SPARE:
class Aux_A_spare(ConversionObject):
	def __init__(self):
		data_name = "Aux_A_spare"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												SCHUMANN_DC/DC_CURRENT_INPUT:
# In mA
class Schumann_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "Schumann_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SCHUMANN_DC/DC_CURRENT_OUTPUT:
# In mA
class Schumann_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "Schumann_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												SCHUMANN_DC/DC_VOLTAGE:
# In volts
class Schumann_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "Schumann_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												CFLUX-1_DC/DC_CURRENT_INPUT:
# In mA
class CFLUX_1_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "CFLUX_1_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												CFLUX-1_DC/DC_CURRENT_OUTPUT:
# In mA
class CFLUX_1_dcdc_current_output(ConversionObject):
	def __init__(self):
		data_name = "CFLUX_1_dcdc_current_output"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												CFLUX-1_DC/DC_VOLTAGE:
# In volts
class CFLUX_1_dcdc_voltage(ConversionObject):
	def __init__(self):
		data_name = "CFLUX_1_dcdc_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												CFLUX_SPARE_1:
class CFLUX_spare_1(ConversionObject):
	def __init__(self):
		data_name = "CFLUX_spare_1"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												CFLUX_SPARE_2:
class CFLUX_spare_2(ConversionObject):
	def __init__(self):
		data_name = "CFLUX_spare_2"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_BOX_INPUT_CURRENT:
# In mA
class Aux_box_input_current(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_input_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#												AUX_BOX_INPUT_VOLTAGE:
# In volts
class Aux_box_input_voltage(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_input_voltage"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												FIBER_OPTIC_LINK_DC/DC_CURRENT_INPUT:
# In mA
class fiber_optic_link_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "fiber_optic_link_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 4
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#											FIBER_OPTIC_LINK_DC/DC_VOLTAGE_INPUT:
# In volts
class fiber_optic_link_dcdc_voltage_input(ConversionObject):
	def __init__(self):
		data_name = "fiber_optic_link_dcdc_voltage_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												USB_JACK_DC/DC_CURRENT_INPUT:
# In mA
class USB_jack_dcdc_current_input(ConversionObject):
	def __init__(self):
		data_name = "USB_jack_dcdc_current_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 4
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#											USB_JACK_DC/DC_VOLTAGE_INPUT:
# In volts
class USB_jack_dcdc_voltage_input(ConversionObject):
	def __init__(self):
		data_name = "USB_jack_dcdc_voltage_input"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = float(rawdata) / 100
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#												USB_DC/DC_TEMPERATURE:
# In degrees Fahrenheit
class USB_dcdc_temperature(ConversionObject):
	def __init__(self):
		data_name = "USB_dcdc_temperature"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		converted = (float(rawdata) - 2731.6) * .18 + 32
		return converted
	
#-------------------------------------------------------------------------------------------------------------------
#													FANS_CURRENT:
# In mA
class fans_current(ConversionObject):
	def __init__(self):
		data_name = "fans_current"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 1
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													FAN_A_SPEED:
# In Hz
class fan_A_speed(ConversionObject):
	def __init__(self):
		data_name = "fan_A_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)

#-------------------------------------------------------------------------------------------------------------------
#													FAN_B_SPEED:
# In Hz
class fan_B_speed(ConversionObject):
	def __init__(self):
		data_name = "fan_B_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													FAN_C_SPEED:
# In Hz
class fan_C_speed(ConversionObject):
	def __init__(self):
		data_name = "fan_C_speed"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 3
		decimal_count = 0
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return int(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													AUX_BOX_HUMIDITY:
# In %RH
class Aux_box_humidity(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_humidity"
		data_type = "dec"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = 2
		decimal_count = 2
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return float(rawdata)
	
#-------------------------------------------------------------------------------------------------------------------
#													AUX_BOX_FAN_STATUS:
class Aux_box_fan_status(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_fan_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													AUX_BOX_MOSFET_STATUS:
class Aux_box_MOSFET_status(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_MOSFET_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													AUX_BOX_FUSE_STATUS:
class Aux_box_fuse_status(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_fuse_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata
	
#-------------------------------------------------------------------------------------------------------------------
#													AUX_BOX_OVER_CURRENT_STATUS:
class Aux_box_over_current_status(ConversionObject):
	def __init__(self):
		data_name = "Aux_box_over_current_status"
		data_type = "hex"
		data_typical_lower_limit = None
		data_typical_upper_limit = None
		integer_count = None
		decimal_count = None
		sensor_lower_limit = None
		sensor_upper_limit = None
		ConversionObject.__init__(self, data_name, data_type, data_typical_lower_limit, data_typical_upper_limit, integer_count, decimal_count, sensor_lower_limit, sensor_upper_limit)

	def format(self, rawdata):
		return rawdata


def main():
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="{levelname}:({filename}:{lineno}) {message}", style="{")

	geiger1 = ConversionObject()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="{levelname}:({filename}:{lineno}) {message}", style="{")
    main()