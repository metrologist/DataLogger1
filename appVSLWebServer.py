import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_from_directory, make_response, request

data_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'graphdata')
app = Flask(__name__)


import sqlite3
import dateutil.parser
from datetime import datetime, timedelta
import csv

# Retrieve data from database
def getLastData():
    conn = sqlite3.connect('Sensors_Database/sensorsData.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM VSL_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp = row[1]
        hum = row[2]
    conn.close()
    return time, temp, hum

def getHistDataDate(start, stop):
    start = "'" + start + " 00:00:00" + "'"
    stop = "'" + stop + " 23:59 59" + "'"
    print(start, stop)
    conn = sqlite3.connect('Sensors_Database/sensorsData.db')
    curs = conn.cursor()
    sqcommand = "SELECT * FROM VSL_data  WHERE TIMESTAMP BETWEEN " + start + " AND " + stop + " ORDER BY TIMESTAMP"
    curs.execute(sqcommand)
    data = curs.fetchall()
    dates = []
    temps = []
    hums = []
    for row in data:
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    conn.close()
    return dates, temps, hums

def file_it(csvData):
    target_file = os.path.join(data_file_dir, 'download.csv')
    with open(target_file, 'w', newline = '') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()

# main route 
@app.route("/")
def index():
    global start_date
    nowish = datetime.utcnow()-timedelta(days = 2)
    start_date = nowish.strftime("%Y-%m-%d")
    global finish_date
    now = datetime.utcnow()
    finish_date = now.strftime("%Y-%m-%d")	
    time, temp, hum = getLastData()
    temp = round(temp, 2)
    hum = round(hum, 2)
    templateData = {
            'time': time,
            'temp': temp,
            'hum': hum,
            'start_date': start_date,
            'finish_date': finish_date
    }
    return render_template('index.html', **templateData)

@app.route('/', methods = ['POST'])
def my_form_post():
    global start_date
    start_date = request.form['start_date']
    global finish_date
    finish_date = request.form['finish_date']
    time, temp, hum =getLastData()
    templateData = {
            'time' : time,
            'temp' : temp,
            'hum'  : hum,
            'start_date' : start_date,
            'finish_date' : finish_date
                 }
    return render_template('index.html', **templateData)

@app.route('/plot/temp')
def plot_temp():
    times, temps, hums =getHistDataDate(start_date, finish_date)
    ys = temps
    ys2 = hums
    fig1 = Figure(figsize=(10, 4))
    axis = fig1.add_subplot(2, 1, 1)
    axis2 = fig1.add_subplot(2, 1, 2)
    axis.set_title("Primary Laboratory")
    axis.set_ylabel("°C")
    axis2.set_ylabel("% RH")
    axis2.set_xlabel("DateTime UTC")
    axis.grid(True)
    axis2.grid(True)

    xs = []
    for x in times:
        xs.append(dateutil.parser.parse(x))

    file_data = [['Date UTC', 'Temperature VSI', 'Humidity VSI']]
    for i in range(len(xs)):
        file_data.append([xs[i], ys[i], ys2[i]])

    file_it(file_data)

    axis.plot(xs, ys, 'r', linewidth = 0.5)
    axis2.plot(xs, ys2,'b', linewidth = 0.5)
    fig1.autofmt_xdate()
    canvas = FigureCanvas(fig1)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimeType = 'image/png'
    return response

@app.route('/<path:path>', methods = ['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(data_file_dir, path)):
        path = os.path.join(path, 'download.csv')
    return send_from_directory(data_file_dir, path)




