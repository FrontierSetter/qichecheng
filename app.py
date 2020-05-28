from flask import Flask, render_template, jsonify, request
import requests
import os

# 5500
#  $env:FLASK_ENV = "development"

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

serverEnv = ((os.environ.get('OS') == None) or ('Windows' not in os.environ.get('OS')))

if serverEnv:
    routeEnv = 'http://10.55.8.52:8860/api/v1'
    print("server env")
else:
    routeEnv = 'http://127.0.0.1:5000/json'
    print("debug env")

cacheEnv = 'http://127.0.0.1:5001/json'

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
    # print(routeEnv+'/vehicle/list')
    response = requests.get(routeEnv+'/vehicle/list')
    # print(response.json())
    return jsonify(response.json())

@app.route('/json/statistic_history_exit')
def history_exit_get():
    response = requests.get(routeEnv+'/statistic/history/exit')
    # print(response.json())
    return jsonify(response.json())


@app.route('/json/statistic_history')
def statistic_history_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    if spanType == 'date':
        spanType = 'day'
    response = requests.get(routeEnv+'/statistic/history', params={'starttime':starttime,'endtime':endtime,'type':spanType})
    # print(response.json())
    return jsonify(response.json())

@app.route('/json/vehicle_history')
def vehicle_history_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    vin = request.args.get("vin")
    try:
        # 访问缓存服务器
        response = requests.get(cacheEnv+'/vehicle/history', params={'starttime':starttime,'endtime':endtime,'vin':vin})
    except:
        print('cache server wrong')
        response = requests.get(routeEnv+'/vehicle/history', params={'starttime':starttime,'endtime':endtime,'vin':vin})
    # print(response.json())
    return jsonify(response.json())

# 从缓存服务器请求已经经过预处理的车辆历史轨迹信息
@app.route('/json/vehicle_location_history')
def vehicle_location_history_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    vin = request.args.get("vin")

    response = requests.get(cacheEnv+'/vehicle/location/history', params={'starttime':starttime,'endtime':endtime,'vin':vin})
    return jsonify(response.json())

@app.route('/json/statistic_history_vehicle')
def statistic_history_vehicle_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    if spanType == 'date':
        spanType = 'day'
    vin = request.args.get("vin")
    response = requests.get(routeEnv+'/statistic/history/vehicle', params={'starttime':starttime,'endtime':endtime,'type':spanType,'vin':vin})
    # print(response.json())
    return jsonify(response.json())
