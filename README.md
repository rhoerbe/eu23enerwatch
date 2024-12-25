# eu23enerwatch
grabbing some energy management data for Viz

sensors:
Temperature
Moisture

data grabbing:
wetteralarm.at

## temperature sensors

- sample_temp.sh    start shell, loop forever to write sensor values to logdir
- mqtt_pub_discovery_msg.py  message mqtt discovery data to home assisstant
- mqtt_pub.sh       start mqtt.py from crontab
- mqtt.py           export data from 1-wire temperature sensory via MQTT


## DHT22 temp + humidity: 

python code not yet working