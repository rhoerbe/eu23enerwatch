import argparse
from pathlib import Path
import paho.mqtt.client as mqtt


broker_addr = "10.4.4.17"
broker_port = 1883
sensor_root_path = Path('/sys/bus/w1/devices/w1_bus_master1/')

sensors_heatpump = {
    '28-0119354f4ef8': 't04-Holzofen_Rücklauf',
    '28-011935714abf': 't06-Boiler-oben',
    '28-01202251809c': 't07-Puffer-oben',
    '28-0120222c37ec': 't09-FBH-Vorlauf',
    '28-0119354de282': 't10-FBH-Rücklauf',
}
sensors_ventilation = {
    '28-3c01d6075254': 't01-Keller-Abluft',
    '28-01193555a909': 't05-EG-Abluft',
    '28-012022c38a09': 't08-OG-Abluft',
}

sensory_unused = {
    '28-012022bc4dd7': 't11',
    '28-01193558950f': 't12',
    '28-01193562b1ee': 't13',
}

##>>> pathlib.Path('/sys/bus/w1/devices/w1_bus_master1/28-012022c38a09/temperature').read_text()


def main():
    parser = argparse.ArgumentParser(description="Get W1 values and sent MQTT messages with these values.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()
    client = mqtt.Client(client_id="cloudberry")
    client.username_pw_set("mqtt", "Crsm7.pvbwb9")
    client.connect(broker_addr, broker_port, 60)
    for sensor in sensors_heatpump.keys():
        p = sensor_root_path / sensor / 'temperature'
        temp_str = p.read_text().strip()
        temp = round(int(temp_str) / 1000, 1)
        topic = 'home/temperature/' + sensors_heatpump[sensor]
        client.publish(topic, temp)
    for sensor in sensors_ventilation.keys():
        p = sensor_root_path / sensor / 'temperature'
        temp_str = p.read_text().strip()
        temp = '{"temperature": ' + str(round(int(temp_str) / 1000, 1)) + '}'
        topic = 'home/temperature/' + sensors_heatpump[sensor]
        try:
            topic = 'home/temperature/' + sensors_heatpump[sensor]
        except KeyError:
            print(f"Sensor {sensor} not found, no message sent")
            continue
        if args.verbose:
            print(topic + "   " + temp)
        client.publish(topic, temp)


if __name__ == '__main__':
    main()

