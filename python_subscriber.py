import os
import paho.mqtt.client as mqtt
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Connects the python file to the raw data database
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
def insert_master_string():
    cursor = connection.cursor()
    cursor.execute("INSERT INTO raw_data_table (raw_master_string) VALUES (%s)", (current_master_string,))
    connection.commit()
    cursor.close()

# Prints all rows in the table 
def retrieve_table():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM raw_data_table")
    rows = cursor.fetchall()
    for row in rows:
        print(f"id: {row[0]}, timestamp: {row[1]}, master string: {row[2]}")
    cursor.close()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    connect_to_database() #This should go somewhere (probably here) because we need to connect to the database first
    print("Connected with result code: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CarletonWeatherTower")
    # client.subscribe("test") #remove this after testing

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print("I have a message: ")
    global current_master_string
    current_master_string = msg.payload.decode("utf-8")
    insert_master_string()
    print(str(msg.payload.decode("utf-8"))) #for testing

# Creating the client object with an approporiate id
client = mqtt.Client(client_id="Python Handler")

# Setting the callback function for connections
client.on_connect = on_connect

# Setting the callback function for message reception 
client.on_message = on_message

# Connecting to broker
client.connect("test.mosquitto.org", 1883, 60)	# connect(host, port=1883, keepalive=60, bind_address=””)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
