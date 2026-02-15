import json
import os
import paho.mqtt.client as mqtt

broker_addr = "10.4.4.17"
broker_port = 1883
state_topic = "home/temperature"

# Discovery message
discovery_template = {
    "name": "placeholder sensor_id",
    "state_topic": "placeholder state_topic",
    "state_class": "measurement",
    "device_class": "temperature",
    "unit_of_measurement": "°C",
    "value_template": "{{ value_json.temperature }}",
    "unique_id": "placeholder sensor_id",
    "device": {
        "identifiers": "placeholder [device_id]",
        "name": "placeholder device_id",
        "model": "D18B20 1wire temperature sensor",
        "manufacturer": "Cloudberry"
    }
}
sensors_heatpump = (
    't04-Holzofen_Rücklauf',
    't06-Boiler-oben',
    't07-Puffer-oben',
    't09-FBH-Vorlauf',
    't10-FBH-Rücklauf',
)
sensors_air = (
    't01-Keller-Abluft',
    't05-EG-Abluft',
    't08-OG-Abluft',
)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="cloudberry")
    try:
        password = os.environ['MQTT_PASSWORD']
        userid = os.environ['MQTT_USERID']
    except KeyError:
        raise KeyError(f"Environment variable MQTT_PASSWORD or MQTT_USERID not found.")
    client.username_pw_set(userid, password)
    client.connect(broker_addr, broker_port, 60)

    # Publish discovery message for heatpump sensors
    for sensor in (sensors_heatpump + sensors_air):
        message = discovery_template.copy()
        message["name"] = sensor
        message["state_topic"] = state_topic + "/" + sensor
        message["unique_id"] = "id_" + sensor
        message["device"]["identifiers"] = ["heatpump_temperatures"]
        message["device"]["name"] = "heatpump_temperatures"
        client.publish("homeassistant/sensor/" + sensor + "/config", json.dumps(message), retain=True)


if __name__ == '__main__':
    main()

