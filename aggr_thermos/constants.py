# sensor ids when querying /sys/bus/w1/devices/ on the raspberry with DS18B20 sensors connected
sensor_id = {
'28-3c01d6075254': 'therm01',
'28-0119354f4ef8': 'therm04',
'28-01193555a909': 'therm05',
'28-011935714abf': 'therm06',
'28-01202251809c': 'therm07',
'28-012022c38a09': 'therm08',
'28-0120222c37ec': 'therm09',
'28-0119354de282': 'therm10',
'28-012022bc4dd7': 'therm11',
'28-01193558950f': 'therm12',
'28-01193562b1ee': 'therm13',
}

# mapping sensor name to location
sensor_loc = {
    'therm01': 'Kellerabluft',
    'therm04': 'Ofenvorlauf',
    'therm05': 'EGabluft',
    'therm06': 'Boiler',
    'therm07': 'Puffer',
    'therm08': 'OGabluft',
    'therm09': 'FBHvorlauf',
    'therm10': 'FBHruecklauf',
}

sql_cretab = '''
CREATE TABLE samples (
    sampletime TIMESTAMP PRIMARY KEY,
    Kellerabluft DECIMAL(4,1),
    Ofenvorlauf DECIMAL(4,1),
    EGabluft DECIMAL(4,1),
    Boiler DECIMAL(4,1),
    Puffer DECIMAL(4,1),
    OGabluft DECIMAL(4,1),
    FBHvorlauf DECIMAL(4,1),
    FBHruecklauf DECIMAL(4,1)
)
'''

