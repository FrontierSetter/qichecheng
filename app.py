from flask import Flask, render_template, jsonify, request
import requests
import os

# 5500

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

serverEnv = ((os.environ.get('OS') != None) and ('Windows' not in os.environ.get('OS')))

if serverEnv:
    routeEnv = 'http://10.55.8.52:8860/api/v1'
    print("server env")
else:
    routeEnv = 'http://127.0.0.1:5000/json'
    print("debug env")

@app.route('/')
def default():
    return render_template("realtime_map.html")

@app.route('/<html_name>')
def render_html(html_name):
    return render_template(html_name)

@app.route('/favicon.ico')
def render_favicon():
    return app.send_static_file('favicon.ico')


@app.route('/json/car_list')
def car_list_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    print(routeEnv+'/vehicle/list')
    response = requests.get(routeEnv+'/vehicle/list')
    print(response.json())
    return jsonify(response.json())

@app.route('/json/statistic_history')
def statistic_history_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    response = requests.get(routeEnv+'/statistic/history', params={'starttime':starttime,'endtime':endtime,'type':spanType})
    print(response.json())
    return jsonify(response.json())

@app.route('/json/statistic_history_vehicle')
def statistic_history_vehicle_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    vin = request.args.get("vin")
    # print(startTime+endtime+spanType+vin)
    # print(request.args)

    response = requests.get(routeEnv+'/statistic/history/vehicle', params={'starttime':starttime,'endtime':endtime,'type':spanType,'vin':vin})
    print(response.json())
    return jsonify(response.json())