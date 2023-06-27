CREATE TABLE formatted_data_table (
	id BIGSERIAL PRIMARY KEY NOT NULL,    
	datetime_utc TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAUlT CURRENT_TIMESTAMP(0),                -- internal representation of time measurement was saved

	geiger_ticks NUMERIC(3, 0),
	geiger_high_volts NUMERIC(4, 1),
	geiger_current NUMERIC(4, 1),
	geiger_temperature NUMERIC(4, 1),
	geiger_status text,

	vortex_avg_speed NUMERIC(3, 0),
	vortex_wind_gust NUMERIC(3, 0),
	vortex_calc_mph NUMERIC(3, 0),

	rain_drip_code text,
	rain_bucket NUMERIC(4, 2),
	rain_rate NUMERIC(3, 0),
	rain_ten_min_dry NUMERIC(5, 0),
	rain_battery_voltage text,

	RTD_1K_upper NUMERIC(7, 4),
	RTD_1K_middle NUMERIC(7, 4),
	RTD_1K_lower NUMERIC(7, 4),
	RTD_100_upper NUMERIC(7, 4),
	RTD_100_middle NUMERIC(7, 4),
	RTD_100_lower NUMERIC(7, 4),
	RTD_Davis_upper NUMERIC(7, 4),
	RTD_Davis_middle NUMERIC(7, 4),
	RTD_Davis_lower NUMERIC(7, 4),
	RH_sensor_1 NUMERIC(4, 1),
	RH_sensor_2 NUMERIC(4, 1),
	outer_shield_LM335 NUMERIC(6, 3),
	middle_shield_LM355 NUMERIC(6, 3),
	inner_shield_LM335 NUMERIC(6, 3),
	bowl_LM335 NUMERIC(6, 3),
	ambient_temp_LM335 NUMERIC(6, 3),
	IR_snow_depth NUMERIC(4,2),
	temp_head_fan_airflow NUMERIC(5, 4),
	temp_head_fan_voltage NUMERIC(4, 2),
	temp_head_fan_current NUMERIC(4, 1),
	PTB_upper NUMERIC(7,4),
	PTB_middle NUMERIC(7,4),
	PTB_lower NUMERIC(7,4),
	AD_temperature NUMERIC(6, 3),

	fan_voltage NUMERIC(4, 2),
	fan_current NUMERIC(4, 1), 
	fan_speed NUMERIC(4, 0),
	TS4200_current NUMERIC(4, 1),
	RF_link_current NUMERIC(4, 1),
	box_humidity NUMERIC(3, 0),
	ground_temperature NUMERIC(6, 3),

	snow_depth_sonic NUMERIC(4, 2),
	barometric_pressure NUMERIC(5,3),
	ten_enclosure_temp NUMERIC(4, 1),
	ten_circuit_current NUMERIC(4, 1),
	ten_RTD_temperature NUMERIC(5,2),
	RH_Precon NUMERIC(4, 1),
	Temperature_Precon NUMERIC(5, 2),
	RH_Honeywell NUMERIC(4, 1),
	ten_avg_wind_speed NUMERIC(3, 0),
	ten_instant_wind_speed NUMERIC(4, 1),
	ten_wind_direction NUMERIC(4, 1),

	power_100WA_voltage NUMERIC(4, 2),
	power_100WA_current NUMERIC(4 ,0),
	power_100WB_voltage NUMERIC(4, 2),
	power_100WB_current NUMERIC(4, 0),
	power_50W_voltage NUMERIC(4, 2),
	power_50W_current NUMERIC(4, 0),
	power_20WA_voltage NUMERIC(4, 2),
	power_20WA_current NUMERIC(4, 0),
	power_load_voltage NUMERIC(4, 2), 
	power_load_current NUMERIC(4, 0),
	power_battery_voltage NUMERIC(4, 2),
	power_battery_current NUMERIC(5, 0),
	power_solar_voltage NUMERIC(4, 2),
	power_solar_current NUMERIC(5, 0),
	power_20WB_voltage NUMERIC(4, 2),
	power_20WB_current NUMERIC(4, 0),
	power_fan_current_A NUMERIC(4, 1),
	power_heater_current_A NUMERIC(4, 1),
	power_battery_temperature_A NUMERIC(4, 1),
	power_cabinet_temperature NUMERIC(4, 1),
	power_MPPT_temperature NUMERIC(4, 1),
	power_5C_voltage NUMERIC(3, 2),
	power_5DAQ_voltage NUMERIC(3, 2),
	power_5DAQ_current NUMERIC(4, 0),
	power_VTOP_voltage NUMERIC(4, 2),
	power_VTOP_current NUMERIC(4, 0),
	power_VAUX_voltage NUMERIC(4, 2),
	power_VAUX_current NUMERIC(4, 1),
	power_DAQ_input_current NUMERIC(4, 0),
	power_battery_temperature_B NUMERIC(4, 1),
	power_box_temperature NUMERIC(4, 1),
	power_heater_current_B NUMERIC(4, 1),
	power_fan_current_B NUMERIC(4, 1),
	power_status text,
	power_enclosure_humidity NUMERIC(2, 0),
	power_fault_status text,

	soil_temp_1_below NUMERIC(6, 3),
	soil_temp_2_below NUMERIC(6, 3),
	soil_temp_3_below NUMERIC(6, 3),
	soil_temp_4_below NUMERIC(6, 3),
	soil_temp_5_below NUMERIC(6, 3),
	soil_temp_6_below NUMERIC(6, 3),
	soil_temp_7_below NUMERIC(6, 3),
	soil_temp_8_below NUMERIC(6, 3),
	soil_temp_10_below NUMERIC(6, 3),
	soil_temp_12_below NUMERIC(6, 3),
	soil_temp_20_below NUMERIC(6, 3),
	soil_temp_30_below NUMERIC(6, 3),
	soil_temp_40_below NUMERIC(6, 3),
	soil_temp_48_below NUMERIC(6, 3),

	soil_moist_b2 NUMERIC(4, 2),
	soil_moist_b4 NUMERIC(4, 2),
	soil_moist_b6 NUMERIC(4, 2),
	soil_moist_b8 NUMERIC(4, 2),
	soil_moist_b10 NUMERIC(4, 2),
	soil_moist_b15 NUMERIC(4, 2),
	soil_moist_b20 NUMERIC(4, 2),
	soil_moist_b40 NUMERIC(4, 2),

	temp_1_above NUMERIC(6, 3),
	temp_2_above NUMERIC(6, 3),
	temp_3_above NUMERIC(6, 3),
	temp_4_above NUMERIC(6, 3),
	temp_5_above NUMERIC(6, 3),
	temp_7_above NUMERIC(6, 3),
	temp_9_above NUMERIC(6, 3),
	temp_11_above NUMERIC(6, 3),
	temp_13_above NUMERIC(6, 3),
	temp_15_above NUMERIC(6, 3),

	soil_flux NUMERIC(4, 3),
	soil_electronics_temp NUMERIC(4, 1),
	soil_electronics_Vref NUMERIC(4, 3),
	soil_spare NUMERIC(5, 2),

	Geiger_burst_count NUMERIC(1, 0),
	Geiger_burst_time NUMERIC(6, 2),
	barometric_temperature NUMERIC(5, 2),

	load_dcdc_voltage_input NUMERIC(4, 2),
	load_dcdc_current_input NUMERIC(4, 3),
	load_dcdc_current_output NUMERIC(4, 3),
	load_dcdc_voltage_output NUMERIC(4, 2),
	battery_charger_current_input NUMERIC(4, 3),
	battery_charger_current_output NUMERIC(4, 3),
	battery_charger_temperature NUMERIC(4, 1),
	battery_charger_voltage_output NUMERIC(4, 2),
	solar_dcdc_input_voltage NUMERIC(4, 2),
	solar_dcdc_input_current NUMERIC(4, 3),
	solar_charger_current_output NUMERIC(4, 3),
	solar_charger_voltage_output NUMERIC(4, 2),
	load_voltage NUMERIC(4, 2),
	battery_voltage NUMERIC(4, 2),
	battery_temperature NUMERIC(4, 1),
	battery_protection_status NUMERIC(2, 0),
	weatherproof_enclosure_temperature NUMERIC(4, 1),
	power_supply_box_temperature NUMERIC(4, 1),
	power_supply_humidity NUMERIC(4, 1),
	"30V_supply_fan_speed" NUMERIC(4, 0),
	"30V_supply_fan_current" NUMERIC(4, 1),
	"30V_supply_current_output" NUMERIC(4, 3),
	"30V_supply_voltage_output" NUMERIC(4, 2),
	"30V_supply_24V_supply_voltage" NUMERIC(4, 2),
	"30V_converter_board_current_input" NUMERIC(4, 2),
	"30V_converter_board_voltage_input" NUMERIC(4, 2),
	MOSFET_switches_status NUMERIC(2, 0),
	protection_raw_voltage NUMERIC(4, 2),
	protection_protected_voltage NUMERIC(4, 2),
	protection_raw_input_current NUMERIC(4, 2),
	protection_circuit_status NUMERIC(2, 0),

	mux_current NUMERIC(5, 2),
	mux_temperature NUMERIC(6, 2),
	Peet_wind_rate NUMERIC(3, 0),
	Peet_wind_multl NUMERIC(3, 0),
	Peet_windlo NUMERIC(3, 0),
	Peet_wind_multh NUMERIC(3, 0),
	Peet_windhi NUMERIC(3, 0),
	Peet_vduce NUMERIC(3, 0),
	Peet_winddir NUMERIC(3, 2),
	Inspeed_wind_direction NUMERIC(3, 2),
	Hydreon_current NUMERIC(3, 2),
	Hydreon_temperature NUMERIC(6, 2),
	Hydreon_range_setting NUMERIC(1, 0),
	Hydreon_low_sense NUMERIC(4, 3),
	Hydreon_medium_sense NUMERIC(4, 3),
	Hydreon_high_sense NUMERIC(4, 3),
	sky_sensor_current NUMERIC(3, 2),
	sky_swiper_CW_current NUMERIC(3, 2),
	sky_swiper_CCW_current NUMERIC(3, 2),
	sky_dark_reading NUMERIC(1, 0),
	sky_bright_reading NUMERIC(1, 0),
	sky_IR_temperature NUMERIC(3, 2),
	sky_sensor_status NUMERIC(1, 0),
	sky_Hall_sensor NUMERIC(4, 3),
	sway_X40_reading NUMERIC(4, 3),
	sway_X1_reading NUMERIC(4, 3),
	sway_Y1_reading NUMERIC(4, 3),
	sway_Y40_reading NUMERIC(4, 3),
	sway_sensor_temperature NUMERIC(3, 2),
	sway_sensor_Vss NUMERIC(4, 3),
	sway_Z_offset NUMERIC(4, 3),
	sway_Z50_reading NUMERIC(4, 3),
	lightning_current NUMERIC(3, 2),
	lightning_UV_count NUMERIC(1, 0),
	lightning_high_voltage NUMERIC(3, 2),
	lightning_3001_lux NUMERIC(4, 3),
	lightning_Skyscan_current NUMERIC(3, 2),
	lightning_Skyscan_LEDs NUMERIC(1, 0),
	lightning_Skyscan_flash_time NUMERIC(3, 2),
	lightning_Skyscan_alarms NUMERIC(1, 0),
	lightning_OPT101_baseline NUMERIC(4, 3),
	lightning_OPT101_north NUMERIC(4, 3),
	lightning_OPT101_south NUMERIC(4, 3),
	lightning_OPT101_east NUMERIC(4, 3),
	lightning_OPT101_west NUMERIC(4, 3),
	lightning_OPT101_zenith NUMERIC(4, 3),
	lightning_thunder NUMERIC(3, 2),
	lightning_flag NUMERIC(1, 0),
	lightning_UVA_UVB NUMERIC(4, 3),
	lightning_OPT_temperature NUMERIC(4, 3),

	solar_box_temperature NUMERIC(3, 2),
	solar_pyran_upper_byte NUMERIC(8, 4),
	solar_pyran_middle_byte NUMERIC(8, 4),
	solar_pyran_lower_byte NUMERIC(8, 4),
	solar_par_upper_byte NUMERIC(8, 4),
	solar_par_middle_byte NUMERIC(8, 4),
	solar_par_lower_byte NUMERIC(8, 4),
	solar_UV_upper_byte NUMERIC(7, 4),
	solar_UV_middle_byte NUMERIC(7, 4),
	solar_UV_lower_byte NUMERIC(7, 4),
	solar_gold_grid_east NUMERIC(5, 4),
	solar_gold_grid_west NUMERIC(5, 4),
	solar_Decagon_horizontal NUMERIC(5, 4),
	solar_Decagon_tilted NUMERIC(5, 4),
	solar_frost NUMERIC(4, 3),
	solar_bud NUMERIC(4, 3),
	solar_globe_upper_byte NUMERIC(7, 4),
	solar_globe_middle_byte NUMERIC(7, 4),
	solar_globe_lower_byte NUMERIC(7, 4),
	solar_current NUMERIC(4, 3),
	solar_voltage NUMERIC(4, 2),
	solar_IR_ground_temperature NUMERIC(4, 3),

	MetOne_LED_current NUMERIC(5, 2),
	MetOne_pulsewidth NUMERIC(1, 0),
	MetOne_ticks_count NUMERIC(1, 0),

	fuses_Arbcam_current NUMERIC(4, 3),
	fuses_Arbcam_voltage NUMERIC(4, 2),
	"fuses_5.6_voltage" NUMERIC(4, 2),
	fuses_mux_current NUMERIC(4, 2),
	fuses_lightning_current NUMERIC(3, 2),
	fuses_solar_DAQ_current NUMERIC(3, 2),
	fuses_fluxgate_current NUMERIC(3, 2),
	fuses_triaxial_current NUMERIC(3, 2),
	fuses_future_current NUMERIC(3, 2),
	fuses_flag NUMERIC(1, 0),
	fuses_warn NUMERIC(1, 0),
	fuses_go_up NUMERIC(1, 0),
	fuses_monitor NUMERIC(1, 0),
	fuses_Arbcam_mode NUMERIC(1, 0),
	fuses_fault_status NUMERIC(1, 0),

	power_solar_panel_current NUMERIC(3, 2),
	power_solar_panel_voltage NUMERIC(3, 2),
	power_battery_current_B NUMERIC(3, 2),
	power_battery_voltage_B NUMERIC(3, 2),
	"power_current_into_5.6" NUMERIC(3, 2),
	"power_voltage_into_5.6" NUMERIC(3, 2),
	"power_5.6_load_current" NUMERIC(3, 2),
	"power_5.6_load_voltage" NUMERIC(3, 2),
	power_box_temperature_B NUMERIC(3, 2),
	"power_Arbcam_dc/dc_input_current" NUMERIC(3, 2),
	"power_Arbcam_dc/dc_input_voltage" NUMERIC(3, 2),
	power_Arbcam_current NUMERIC(3, 2),
	power_Arbcam_voltage NUMERIC(3, 2),
	power_battery_temperature NUMERIC(3, 2),
	power_128K_battery_voltage NUMERIC(1, 0),
	power_RTC_battery_voltage NUMERIC(1, 0),
	power_RTD_30ft_temperature NUMERIC(1, 0),
	power_hail_peak NUMERIC(3, 2),
	power_hail_average NUMERIC(3, 2),
	power_status_B NUMERIC(1, 0),
	power_OVP_cycles NUMERIC(1, 0),
	power_OVP_voltage NUMERIC(3, 2),
	power_hail_sensor_temperature NUMERIC(3, 2),
	power_hail_sensor_hits NUMERIC(1, 0),
	power_box_humidity NUMERIC(2, 0)
);