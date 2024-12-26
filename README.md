# eu23enerwatch
grabbing some energy management data for Viz

sensors:
Temperature
Moisture

data grabbing:
wetteralarm.at

## temperature sensors

- sample_temp.sh    start shell, loop forever to write sensor values to logdir
- mqtt_pub.sh       start mqtt.py from crontab
- mqtt.py           export data from 1-wire temperature sensory via MQTT

### Manual discovery

mqtt:
  sensor:
    - name: Test Dummy
      state_topic: home/temperature/t000-test
      unit_of_measurement: "°C"
      device_class: temperature
      value_template: "{{ value_json.temperature }}"
      unique_id: id_test_dummy
      device:
        identifiers:
          - test_device_id
        name: test_device_id
        model: D18B20 1wire temperature sensor
        manufacturer: Cloudberry


### Autodiscovery (incomplete!)

- mqtt_pub_discovery_msg.py  message mqtt discovery data to home assisstant
- mqtt_remove_msg.py  remove discovery messages


## DHT22 temp + humidity: 

python code not yet working