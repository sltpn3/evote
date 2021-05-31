from flask import Flask, request, render_template, flash, send_from_directory, Response

# from flask_bootstrap import Bootstrap

import sqlite3
import json

app = Flask(__name__, static_url_path='')
app.secret_key = b'MzgSuSc4yGm7zTx'
app.config['TESTING'] = True
# Bootstrap(app)


@app.route('/stat1', methods=['GET'])
def stat1():
    pub_year = request.args.get('pub_year', None)
    pub_month = request.args.get('pub_month', None)
    labels = []
    data = []
    if pub_year or pub_month:
        conn = sqlite3.connect('stat.sqlite')
        cursor = conn.cursor()
        if pub_month:
            sql = 'SELECT pub_day, count FROM stat1 WHERE pub_month="{}"'.format(pub_month)
        elif pub_year:
            sql = 'SELECT pub_month, SUM(count) FROM stat1 WHERE pub_year="{}" GROUP BY pub_month'.format(pub_year)

        for row in cursor.execute(sql):
            label, count = row
            labels.append(label)
            data.append(count)
        cursor.close()
        conn.close()

    result = {'labels': labels, 'data': data}
    response = Response()
    response.data = json.dumps(result)
    response.content_type = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stat2', methods=['GET'])
def stat2():
    kota = request.args.get('kota', None)
    pub_year = request.args.get('pub_year', None)
    pub_month = request.args.get('pub_month', None)
    labels = []
    data = []

    if pub_year or pub_month:
        conn = sqlite3.connect('stat.sqlite')
        cursor = conn.cursor()
        if pub_month:
            sql = 'SELECT pub_day, new_case, recovered, death FROM stat2 WHERE pub_month="{}" AND kota="{}"'.format(pub_month, kota)
        elif pub_year:
            sql = 'SELECT pub_month, SUM(new_case), SUM(recovered), SUM(death) FROM stat2 WHERE pub_year="{}" AND kota="{}" GROUP BY pub_month'.format(pub_year, kota)

        for row in cursor.execute(sql):
            label, new_case, recovered, death = row
            labels.append(label)
            data.append({'new_case': new_case, 'recovered': recovered, 'death': death})
        cursor.close()
        conn.close()

    result = {'labels': labels, 'data': data}
    response = Response()
    response.data = json.dumps(result)
    response.content_type = 'application/json'
#     response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stat2_pie', methods=['GET'])
def stat2_pie():
    kota = request.args.get('kota', None)
    pub_year = request.args.get('pub_year', None)
    pub_month = request.args.get('pub_month', None)
    labels = ['New Case, Recovered, Death']
    data = {}

    if pub_year or pub_month:
        conn = sqlite3.connect('stat.sqlite')
        cursor = conn.cursor()
        if pub_month:
            sql = 'SELECT SUM(new_case), SUM(recovered), SUM(death) FROM stat2 WHERE pub_month="{}" AND kota="{}"'.format(pub_month, kota)
        elif pub_year:
            sql = 'SELECT SUM(new_case), SUM(recovered), SUM(death) FROM stat2 WHERE pub_year="{}" AND kota="{}"'.format(pub_year, kota)

        cursor.execute(sql)
        row = cursor.fetchone()
        print(row)

        new_case, recovered, death = row
        data = {'new_case': new_case, 'recovered': recovered, 'death': death}

        cursor.close()
        conn.close()

    result = {'labels': labels, 'data': data}
    response = Response()
    response.data = json.dumps(result)
    response.content_type = 'application/json'
#     response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run('0.0.0.0', '9002')
