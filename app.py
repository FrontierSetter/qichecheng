from flask import Flask, render_template, jsonify

app = Flask(__name__)

json_3_1 = {
    "msg": "",
    "code": 200,
    "resultData": [
        {
            "time": "1970-01-01 00:00:00",
            "mileage": 0.0,
            "duration": 5155.0,
            "autoMileage": 0.0,
            "autoDuration": 2990.0,
            "alartTimes": "",
            "drivemodeSwitchTimes": 0,
            "mileageTotal": 33188.4,
            "durationTotal": 6543331.0,
            "autoMileageTotal": 33188.4,
            "autoDurationTotal": 6543331.0,
            "alartTimesTotal": "",
            "drivemodeSwitchTimesTotal": 83932,
            "enterprise": "",
            "timeMon": "1970-01",
            "exitRate": ""
        },
        {
            "time": "2020-02-01 00:00:00",
            "mileage": 133.4,
            "duration": 76314.0,
            "autoMileage": 0.0,
            "autoDuration": 2990.0,
            "alartTimes": "",
            "drivemodeSwitchTimes": 0,
            "mileageTotal": 138.0,
            "durationTotal": 112700.0,
            "autoMileageTotal": 138.0,
            "autoDurationTotal": 112700.0,
            "alartTimesTotal": "",
            "drivemodeSwitchTimesTotal": 0,
            "enterprise": "",
            "timeMon": "2020-02",
            "exitRate": ""
        },
        {
            "time": "2020-03-01 00:00:00",
            "mileage": 993137.0,
            "duration": 4.63605718E8,
            "autoMileage": 591517.09,
            "autoDuration": 8.1837457E7,
            "alartTimes": 0,
            "drivemodeSwitchTimes": 714356,
            "mileageTotal": 1383257.8,
            "durationTotal": 5.42519009E8,
            "autoMileageTotal": 1383257.8,
            "autoDurationTotal": 5.42519009E8,
            "alartTimesTotal": 0,
            "drivemodeSwitchTimesTotal": 21200028,
            "enterprise": "",
            "timeMon": "2020-03",
            "exitRate": ""
        },
        {
            "time": "2020-04-01 00:00:00",
            "mileage": 115122.9,
            "duration": 3.9956361E7,
            "autoMileage": 54451.77,
            "autoDuration": 7913915.0,
            "alartTimes": 0,
            "drivemodeSwitchTimes": 431411,
            "mileageTotal": 1690539.1,
            "durationTotal": 4.1801587E8,
            "autoMileageTotal": 1690539.1,
            "autoDurationTotal": 4.1801587E8,
            "alartTimesTotal": 0,
            "drivemodeSwitchTimesTotal": 4394123,
            "enterprise": "",
            "timeMon": "2020-04",
            "exitRate": ""
        },
        {
            "time": "2020-05-01 00:00:00",
            "mileage": 47513.4,
            "duration": 1.8607013E7,
            "autoMileage": 12497.02,
            "autoDuration": 1919607.0,
            "alartTimes": 0,
            "drivemodeSwitchTimes": 39722,
            "mileageTotal": 295594.4,
            "durationTotal": 8.1813447E7,
            "autoMileageTotal": 295594.4,
            "autoDurationTotal": 8.1813447E7,
            "alartTimesTotal": 0,
            "drivemodeSwitchTimesTotal": 595823,
            "enterprise": "",
            "timeMon": "2020-05",
            "exitRate": ""
        }
    ]
}

@app.route('/')
def default():
    return render_template("realtime_map.html")

@app.route('/<html_name>')
def render_html(html_name):
    return render_template(html_name)


@app.route('/json_3_1')
def json_3_1_get():
    return jsonify(json_3_1)