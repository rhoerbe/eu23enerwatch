from pathlib import Path
import paho.mqtt.client as mqtt


broker="10.4.4.17"
sensor_root_path = Path('/sys/bus/w1/devices/w1_bus_master1/')

sensors = {
    '28-3c01d6075254': 't01-Keller-Abluft',
    '28-0119354f4ef8': 't04-Holzofen_Ruecklauf',
    '28-01193555a909': 't05-EG-Abluft',
    '28-011935714abf': 't06-Boiler-oben',
    '28-01202251809c': 't07-Puffer-oben',
    '28-012022c38a09': 't08-OG-Abluft',
    '28-0120222c37ec': 't09-FBH-Vorlauf',
    '28-0119354de282': 't10-FBH-Rücklauf',
}

sensory_unused = {
    '28-012022bc4dd7': 't11',
    '28-01193558950f': 't12',
    '28-01193562b1ee': 't13',
}

##>>> pathlib.Path('/sys/bus/w1/devices/w1_bus_master1/28-012022c38a09/temperature').read_text()


def main():
    client = mqtt.Client(client_id="cloudberry",
                         transport='tcp',
                         protocol=mqtt.MQTTv5)

    client.username_pw_set("mqtt", "Crsm7.pvbwb9")
    client.connect(broker)
    for sensor in sensors.keys():
        p = sensor_root_path / sensor / 'temperature'
        temp_str = p.read_text().strip()
        temp = round(int(temp_str) / 1000, 1)
        topic = '/home/temperature/' + sensors[sensor]
        client.publish(topic, temp)


if __name__ == '__main__':
    main()

