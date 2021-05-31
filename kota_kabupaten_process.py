import sqlite3
import json


def geojson_to_db():
    conn = sqlite3.connect('app.sqlite')
    cursor = conn.cursor()
    f1 = open('nebula.geojson')
    data = json.load(f1)
    for i in data:
        print(i)
    print('----')
    print(data['type'])
    print('----')
    j = 0
    for i in data['features']:
        sql = 'INSERT OR IGNORE INTO kota_geojson VALUES(?,?,?,?,?,?,?,?)'
        # print(sql)
        cursor.execute(sql, (j, i['type'], json.dumps(i['geometry']),
                             i['properties']['mhid'],
                             i['properties']['KABKOT'],
                             i['properties']['PROVNO'],
                             i['properties']['KABKOTNO'],
                             i['properties']['PROVINSI']))
        j += 1
    # print(data['features'])
    # for arc in data['arcs']:
    #     print(arc)
    # print(len(data['arcs']))
    conn.commit()
    cursor.close()
    conn.close()


def db_to_geojson():
    conn = sqlite3.connect('app.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = {'type': 'FeatureCollection',
            'features': []}
    sql = 'SELECT * FROM kota_geojson'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        geometry = json.loads(row['geometry'])
        properties = {'mhid': row['mhid'],
                      'KABKOT': row['kabkot'],
                      'KABKOTNO': row['kabkotno'],
                      'PROV': row['prov'],
                      'PROVNO': row['provno']}
        # print(properties)
        element = {'type': 'Feature',
                   'feature': geometry,
                   'properties': properties}
        data['features'].append(element)
    f = open('nebula2.geojson', 'w')
    f.write(json.dumps(data))
    cursor.close()
    conn.close()


def json_to_db():
    conn = sqlite3.connect('app.sqlite')
    cursor = conn.cursor()
    f1 = open('nebula.json')
    data = json.load(f1)
    j = 0
    # print(data['objects'])
    for i in data['objects']['nebula']['geometries']:
        '''test'''
        print(json.dumps(i['arcs']))
        sql = '''INSERT OR IGNORE INTO kota2 VALUES('{}','{}','{}','{}','{}','{}','{}','{}')'''\
            .format(j, i['arcs'], i['type'],
                    i['properties']['mhid'],
                    i['properties']['KABKOT'],
                    i['properties']['PROVNO'],
                    i['properties']['KABKOTNO'],
                    i['properties']['PROVINSI'])
        print(sql)
        cursor.execute(sql)
        j += 1
        # print i['arcs']
    conn.commit()
    cursor.close()
    conn.close()


def db_to_json():
    conn = sqlite3.connect('app.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    f1 = open('Indonesia-Level-Kota-dan-Kabupaten.json')
    data = json.load(f1)
    j = 0
    sql = 'SELECT * FROM kota2'
    cursor.execute(sql)
    rows = cursor.fetchall()
    geometries = data['objects']['Indonesia-Level-Kota-dan-Kabupaten']['geometries']
    for row in rows:
        # print(data['objects']['Indonesia-Level-Kota-dan-Kabupaten']['geometries'][row['order']]['properties'])
        geometries[row['order']]['properties']['KABKOT'] = row['kabkot']
        geometries[row['order']]['properties']['PROVINSI'] = row['prov']
        geometries[row['order']]['properties']['PROVNO'] = row['provno']
        geometries[row['order']]['properties']['KABKOTNO'] = row['kabkotno']
        # print(data['objects']['Indonesia-Level-Kota-dan-Kabupaten']['geometries'][row['order']]['properties'])
    f2 = open('Indonesia-Level-Kota-dan-Kabupaten2.json', 'w')
    f2.write(json.dumps(data))
    # conn.commit()
    cursor.close()
    conn.close()


def csv_to_db():
    conn = sqlite3.connect('app.sqlite')
    cursor = conn.cursor()
    with open('kota.csv') as f2:
        lines = f2.readlines()

    for line in lines:
        kota, nama, kode, provinsi = line.replace('\n', '').split(',')
        elm = [kota + ' ' + nama, kode, provinsi]
        sql = '''INSERT OR IGNORE INTO kota_only VALUES('{}', '{}', '{}')'''\
            .format(elm[1], elm[0], elm[2])
        print(sql)
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def fix_kota():
    conn = sqlite3.connect('app.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'SELECT * FROM kota_only'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        provno, kabkotno = row['kode'].split('.')
        sql = 'SELECT * FROM kota2 WHERE provno="{}" AND kabkotno="{}"'\
            .format(provno, kabkotno)
        cursor.execute(sql)
        row2 = cursor.fetchone()
        if row2:
            sql = """UPDATE kota2 SET kabkot='{}' WHERE provno='{}' AND kabkotno='{}'"""\
                .format(row['nama'].upper(), provno, kabkotno)
            print(sql)
            cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()


# geojson_to_db()
db_to_geojson()
# json_to_db()
# csv_to_db()
# fix_kota()
# db_to_json()
