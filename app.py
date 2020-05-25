from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def default():
    return render_template("realtime_map.html")

@app.route('/<html_name>')
def render_html(html_name):
    return render_template(html_name)
