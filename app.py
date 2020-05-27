from flask import Flask, render_template, jsonify, request
import requests

# 5500

app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def default():
    return render_template("realtime_map.html")

@app.route('/<html_name>')
def render_html(html_name):
    return render_template(html_name)


@app.route('/json/car_list')
def car_list_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    print(response.json())
    return jsonify(response.json())

@app.route('/json/statistic_history')
def statistic_history_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    startTime = request.args.get("startTime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    response = requests.get('http://10.55.8.52:8860/api/v1/statistic/history', params={'startTime':startTime,'endtime':endtime,'type':spanType})
    print(response.json())
    return jsonify(response.json())

@app.route('/json/statistic_history_vehicle')
def statistic_history_vehicle_get():
    # response = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list')
    startTime = request.args.get("startTime")
    endtime = request.args.get("endtime")
    spanType = request.args.get("type")
    vin = request.args.get("vin")
    # print(startTime+endtime+spanType+vin)
    # print(request.args)

    response = requests.get('http://10.55.8.52:8860/api/v1/statistic/history/vehicle', params={'startTime':startTime,'endtime':endtime,'type':spanType,'vin':vin})
    print(response.json())
    return jsonify(response.json())