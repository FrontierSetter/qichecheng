from flask import Flask, render_template, jsonify, request
import requests
import os


app = Flask(__name__)

routeEnv = 'http://10.55.8.52:8860/api/v1'
vehicleHistoryDict = {}

def vehicleHistoryValidate(starttime, endtime, vin):
    return vin in vehicleHistoryDict

@app.route('/')
def default():
    return "cache host run properly"


@app.route('/json/vehicle/history')
def vehicle_history_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    vin = request.args.get("vin")

    if vehicleHistoryValidate(starttime, endtime, vin):
        print('cache hit')
        return jsonify(vehicleHistoryDict[vin])
    else:
        response = requests.get(routeEnv+'/vehicle/history', params={'starttime':starttime,'endtime':endtime,'vin':vin})
        return jsonify(response.json())

if __name__ == '__main__':
    cnt = 0
    carListJson = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list').json()
    carList = carListJson['resultData']
    for car in carList:
        curVin = car['vinno']
        print(curVin)
        carHistoryRespond = requests.get('http://10.55.8.52:8860/api/v1/vehicle/history', params={'starttime':'2019-08-13', 'endtime':'2020-05-20', 'vin':curVin})
        vehicleHistoryDict[curVin] = carHistoryRespond.json()

        cnt += 1
        if cnt > 3:
            break
        


    print('1')
    app.run(port= 5001)