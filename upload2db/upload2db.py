"""
Upload samples into database
"""

import os
import sys
import psycopg2
from pathlib import Path

import constants


def main():
    password = os.environ['PG_PASSWD']
    conn = psycopg2.connect(host="dc.idn.local", dbname="eu23enerwatch", user="eu23enerwatch", password=password)
    logdir = Path(sys.argv[1])
    for fpath in logdir.rglob('*'):
        if fpath.is_file() and not fpath.name.startswith('done_'):
            with open(fpath) as fd:
                row_values: dict = read_sample(fd)
            write_db(conn.cursor(), fpath.name, row_values)
            rename_inputfile(fpath)
            conn.commit()
    conn.close()


def read_sample(fd) -> dict:
    row_values = {}
    for line in fd.readlines():
        s_id, value = line.split()
        s_name = constants.sensor_id[s_id]
        s_location = constants.sensor_loc[s_name]
        row_values[s_location] = round(int(value)/1000, 1)
    return row_values


def write_db(cursor, sampletime: str, row_values: dict):
    sampletime_edited = sampletime.replace('_', ':')
    sql = f"""
    INSERT INTO samples (
        sampletime,
        Kellerabluft,
        Ofenvorlauf,
        EGabluft,
        Boiler,
        Puffer,
        OGabluft,
        FBHvorlauf,
        FBHruecklauf
    ) 
    VALUES (
        '{sampletime_edited}',
        {row_values['Kellerabluft']},
        {row_values['Ofenvorlauf']},
        {row_values['EGabluft']},
        {row_values['Boiler']},
        {row_values['Puffer']},
        {row_values['OGabluft']},
        {row_values['FBHvorlauf']},
        {row_values['FBHruecklauf']}
    )
    """
    try:
        cursor.execute(sql)
    except psycopg2.errors.UniqueViolation:
        pass


def rename_inputfile(fpath: Path):
    newpath = Path(fpath.parent, 'done_' + str(fpath.name))
    fpath.rename(newpath)

main()