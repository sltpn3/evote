from flask import Flask, request, render_template, flash, send_from_directory, Response

# from flask_bootstrap import Bootstrap
import sqlite3
from sqlite3 import IntegrityError
import hashlib
import json
import jwt
from datetime import datetime

app = Flask(__name__, static_url_path='')
app.secret_key = b'MzgSuSc4yGm7zTx'
app.config['TESTING'] = True
# Bootstrap(app)

jwt_secret = '6bff4caed85d39e940fe3d3f4719727b'


def build_response(data):
    response = Response()
    result = {'data': data,
              'status': 200}
    response.data = json.dumps(result)
    response.content_type = 'application/json'
    return response


def error_response(message):
    result = {'message': message,
              'status': 500}
    response = Response(json.dumps(result), status=500)
    response.content_type = 'application/json'

    return response


def get_hash(plain):
    salt = '7f95b733f4210c71482904eb422143f8'
    salted_plain = '{}{}'.format(plain, salt)
    hashed = hashlib.md5(salted_plain.encode('utf-8')).hexdigest()
    return hashed


def encode_jwt(payload):
    return jwt.encode(payload, jwt_secret, algorithm="HS256")


def row_to_dict(rows):
    result = []
    for row in rows:
        data = {}
        for key in row.keys():
            data[key] = row[key]
        result.append(data)
    return result


@app.route('/login', methods=['POST'])
def login():
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    try:
        conn = sqlite3.connect('app.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE email='{}'".format(email)
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            print(row['password'], get_hash(password))
            if row['password'] == get_hash(password):
                iat = int(datetime.now().timestamp())
                exp = iat + 3600
                payload = {'name': row['name'],
                           'id': row['id'],
                           'iat': iat,
                           'exp': exp}
                return encode_jwt(payload)
            else:
                return error_response('Incorrect Password')
        return error_response('User Not Found')
    except Exception as e:
        return error_response(e.args)


@app.route('/register', methods=['POST'])
def register():
    password = request.json.get('password')
    name = request.json.get('name')
    email = request.json.get('email')
    hashed = get_hash(password)
    try:
        conn = sqlite3.connect('app.sqlite')
        cursor = conn.cursor()
        sql = """INSERT INTO user(name, email, password)
                 VALUES ("{}","{}","{}")""".format(name, email, hashed)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return build_response({})
    except IntegrityError as e:
        if e.args[0] == "UNIQUE constraint failed: user.email":
            return error_response('Email already registered')
        else:
            return error_response(e.args)
    except Exception as e:
        return error_response(e.args)


@app.route('/propinsi', methods=['GET'])
def propinsi():
    try:
        conn = sqlite3.connect('app.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = """SELECT * FROM propinsi"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        rows = row_to_dict(rows)
        return build_response(rows)
    except Exception as e:
        return error_response(e.args)


@app.route('/kota/<string:propinsi>', methods=['GET'])
def kota(propinsi):
    try:
        conn = sqlite3.connect('app.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = """SELECT * FROM kota WHERE propinsi='{}'""".format(propinsi)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        rows = row_to_dict(rows)
        return build_response(rows)
    except Exception as e:
        return error_response(e.args)


if __name__ == "__main__":
    app.run('0.0.0.0', '9001')
