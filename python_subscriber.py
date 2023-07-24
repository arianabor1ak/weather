import paho.mqtt.client as mqtt
import weather_db_wrapper
import sys
import logging

weather_db = weather_db_wrapper.Weather_DB()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.debug(f"Connected with result code: {str(rc)}")
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("CarletonWeatherTower")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    current_master_string = msg.payload.decode("utf-8")
    weather_db.insert_master_string(current_master_string)

def main():
    # Creating the client object with an approporiate id
    client = mqtt.Client(client_id="Python Handler")

    # Setting the callback function for connections
    client.on_connect = on_connect

    # Setting the callback function for message reception
    client.on_message = on_message

    # Connecting to broker
    client.connect("test.mosquitto.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="{levelname}:({filename}:{lineno}) {message}", style="{")
    main()
