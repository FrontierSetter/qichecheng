from flask import Flask, render_template, jsonify, request
import requests
import os
import time


app = Flask(__name__)

routeEnv = 'http://10.55.8.52:8860/api/v1'
vehicleHistoryDict = {}
vehicleHistoryLocationDict = {}

locationCache = {}
expireTime = 9999999
baiduMapAK = 'DsRFuPOjLnZbSUUBGiL2bqL71rExox2a'

locationTransferHitCount = 0

def vehicleHistoryValidate(starttime, endtime, vin):
    return vin in vehicleHistoryDict

def getBaiduLocation(longitude, latitude):
    global locationTransferHitCount
    curTime = int(time.time())
    curKey = str(longitude)+str(latitude)
    if (curKey not in locationCache) or ((curTime - locationCache[curKey]['timeStamp']) > expireTime):
        print ("%d location transfer hit befor this miss" % (locationTransferHitCount))
        locationTransferHitCount = 0
        responseJson = requests.get('http://api.map.baidu.com/geoconv/v1/', params={'coords':str(longitude)+','+str(latitude),'from':1,'to':5,'ak':baiduMapAK}).json()
        resultTuple = (responseJson['result'][0]['x'], responseJson['result'][0]['y'])
        locationCache[curKey]={
            'timeStamp':curTime,
            'baiduLocation':resultTuple
        }
    else:
        locationTransferHitCount += 1
    
    return locationCache[curKey]['baiduLocation']

def refreshVehicleInfo(starttime, endtime, carVin):
    carHistoryRespondJson = requests.get('http://10.55.8.52:8860/api/v1/vehicle/history', params={'starttime':starttime, 'endtime':endtime, 'vin':carVin}).json()
    vehicleHistoryDict[carVin] = carHistoryRespondJson

    vehicleHistoryLocationDict[carVin] = {
        "msg": "",
        "code": 200,
        "requestData":[]
    }

    for curLog in vehicleHistoryDict[carVin]["resultData"]:
        curLocation = getBaiduLocation(curLog["longitude"], curLog["latitude"])
        curTime = curLog["positionTime"]
        vehicleHistoryLocationDict[carVin]["requestData"].append({
            "latitude":curLocation[1],
            "longitude":curLocation[0],
            "positionTime":curTime
        })


@app.route('/')
def default():
    return "cache host run properly"


@app.route('/proxy/baidumap/location_transfer')
def baidumap_location_transfer():
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")

    resultLocation = getBaiduLocation(longitude, latitude)

    result = {
        'status':0,
        'result':[{'x': resultLocation[0], 'y':resultLocation[1]}]
    }
    return jsonify(result)

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

@app.route('/json/vehicle/location/history')
def vehicle_location_history_get():
    starttime = request.args.get("starttime")
    endtime = request.args.get("endtime")
    vin = request.args.get("vin")

    if vehicleHistoryValidate(starttime, endtime, vin):
        print('cache hit')
        return jsonify(vehicleHistoryLocationDict[vin])
    else:
        print('cache miss')
        refreshVehicleInfo(starttime, endtime, vin)
        return jsonify(vehicleHistoryLocationDict[vin])

if __name__ == '__main__':
    # logFile = open('vehicle_')
    # TODO: 使用文件记录，加快启动速度

    print("requestList:")
    carListJson = requests.get('http://10.55.8.52:8860/api/v1/vehicle/list').json()
    carList = carListJson['resultData']

    carNum = int(input("carNum:"))
    
    print("constructVehicleInfo:")
    for car in carList:
        print(car['vinno'])
        refreshVehicleInfo('2019-08-13', '2020-05-20', car['vinno'])
        carNum -= 1
        if carNum <= 0:
            break

    # print("requestVehicleHistory:")
    # for car in carList:
    #     curVin = car['vinno']
    #     print(curVin)
    #     carHistoryRespondJson = requests.get('http://10.55.8.52:8860/api/v1/vehicle/history', params={'starttime':'2019-08-13', 'endtime':'2020-05-20', 'vin':curVin}).json()
    #     vehicleHistoryDict[curVin] = carHistoryRespondJson

    # print("requestVehicleLocationHistory:")
    # for carVin in vehicleHistoryDict:
    #     print(carVin)
    #     vehicleHistoryLocationDict[carVin] = {
    #         "msg": "",
    #         "code": 200,
    #         "requestData":[]
    #     }

    #     for curLog in vehicleHistoryDict[curVin]["resultData"]:
    #         curLocation = getBaiduLocation(curLog["longitude"], curLog["latitude"])
    #         curTime = curLog["positionTime"]
    #         vehicleHistoryLocationDict[carVin]["requestData"].append({
    #             "latitude":curLocation[1],
    #             "longitude":curLocation[0],
    #             "positionTime":curTime
    #         })


    print('1')
    app.run(port= 5001)