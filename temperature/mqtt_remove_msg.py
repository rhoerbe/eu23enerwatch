import json
import paho.mqtt.client as mqtt

broker_addr = "10.4.4.17"
broker_port = 1883
state_topic = "home/temperature"

sensors_heatpump = (
    't04-Holzofen_Ruecklauf',
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
    client.username_pw_set("mqtt", "Crsm7.pvbwb9")
    client.connect(broker_addr, broker_port, 60)

    # Publish discovery message for heatpump sensors
    for sensor in sensors_heatpump:
        client.publish("/home/temperature/"  + sensor, None, retain=True)


if __name__ == '__main__':
    main()

