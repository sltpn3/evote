from datetime import datetime, timedelta
import sqlite3
import random


def insert_stat1():
    conn = sqlite3.connect('stat.sqlite')
    cursor = conn.cursor()

    for i in range(1000):
        _date = datetime.now() - timedelta(days=i)
        s = '''INSERT INTO stat1 VALUES('{}','{}','{}','{}')'''.format(_date.strftime('%Y'), _date.strftime('%Y%m'), _date.strftime('%Y%m%d'), random.randint(10000, 50000))
        cursor.execute(s)

    conn.commit()


def insert_stat2():
    conn = sqlite3.connect('stat.sqlite')
    cursor = conn.cursor()

    kota = ['kota_semarang', 'kota_bandung', 'kota_surabaya']

    for i in range(1000):
        for k in kota:
            _date = datetime.now() - timedelta(days=i)
            s = '''INSERT OR IGNORE INTO stat2 VALUES('{}','{}','{}','{}','{}','{}','{}')'''\
                .format(k, _date.strftime('%Y%m%d'), _date.strftime('%Y%m'), _date.strftime('%Y'),
                        random.randint(0, 500), random.randint(0, 500), random.randint(0, 100))
            print(s)
            cursor.execute(s)

    conn.commit()


insert_stat2()
