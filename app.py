from pymongo import MongoClient
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import timeit

from excel import writeExcel
from init_BD import create_db
from plot_and_powerpoint import writeppt
from converter import handle_file
from getter import get_types, get_temps, get_filenames, get_coords
from filter import filter_by_meas, filter_by_temp, filter_by_coord, filter_by_filename


all_files=[]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = '.\DataFiles\\'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/write_excel/<wafer_id>', methods=['POST'])
def write_excel_route(wafer_id):
    writeExcel(wafer_id)
    return render_template('done.html', message='Excel file successfully created!')

@app.route('/get_structures/<wafer_id>', methods=['GET'])
def get_structures(wafer_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    wafer = db.Wafers.find_one({'wafer_id': wafer_id})
    structures = wafer["structures"]
    return jsonify(structures), 200

@app.route('/get_matrices/<wafer_id>/<structure_id>', methods=['GET'])
def get_matrices(wafer_id, structure_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})
    print(f"Wafer_id: {wafer_id}, structure_id: {structure_id}")
    structure = [s for s in wafer["structures"] if s["structure_id"] == structure_id][0]
    matrices = structure["matrices"]
    print(matrices)
    return jsonify(matrices)

@app.route('/get_all_types/<wafer_id>', methods=['GET'])
def get_all_types(wafer_id):
    return jsonify(get_types(wafer_id)), 200

@app.route('/get_all_temps/<wafer_id>', methods=['GET'])
def get_all_temps(wafer_id):
    return jsonify(get_temps(wafer_id)), 200

@app.route('/get_all_coords/<wafer_id>', methods=['GET'])
def get_all_coords(wafer_id):
    return jsonify(get_coords(wafer_id)), 200

@app.route('/get_all_filenames/<wafer_id>', methods=['GET'])
def get_all_filenames(wafer_id):
    return jsonify(get_filenames(wafer_id)), 200

@app.route('/filter_by_Meas/<wafer_id>/<selectedMeasurements>', methods=['GET'])
def filter_by_Meas(wafer_id, selectedMeasurements):
    return jsonify(filter_by_meas(selectedMeasurements, wafer_id)), 200

@app.route('/filter_by_Temps/<wafer_id>/<selectedMeasurements>', methods=['GET'])
def filter_by_Temps(wafer_id, selectedMeasurements):
    return jsonify(filter_by_temp(selectedMeasurements, wafer_id)), 200

@app.route('/filter_by_Coords/<wafer_id>', methods=['POST'])
def filter_by_Coords(wafer_id):
    print(f"Hello, wafer={wafer_id}")
    data = request.get_json()
    print(f"Data={data}")
    selectedMeasurements = data["coords"]
    return jsonify(filter_by_coord(selectedMeasurements, wafer_id)), 200

@app.route('/filter_by_Filenames/<wafer_id>/<selectedMeasurements>', methods=['GET'])
def filter_by_Filenames(wafer_id, selectedMeasurements):
    return jsonify(filter_by_filename(selectedMeasurements, wafer_id)), 200
@app.route('/write_ppt/<wafer_id>', methods=['POST'])
def write_ppt_route(wafer_id):
    writeppt(wafer_id)
    return render_template('done.html', message='PowerPoint file successfully created!')

@app.route('/delete_wafer/<wafer_id>', methods=['DELETE'])
def delete_wafer(wafer_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db.Wafers.delete_one({'wafer_id': wafer_id})
    return jsonify({'result': 'success'}), 200
@app.route('/open')
def open():
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Measurements']

    collection = db["Wafers"]

    wafers = collection.find({})

    return render_template('open.html', wafers=wafers)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("file")
    print(files)
    for file in files:
        filename = file.filename
        print(filename)

        """if not filename.startswith('AL'):
            lot_id = request.form.get('lot_id')
            wafer_id = request.form.get('wafer_id')
            filename = os.path.splitext(filename)[0].split("\\")[-1]+ "@@@" + lot_id + "_" +wafer_id +os.path.splitext(filename)[1]
            print(f"New filename: {filename}")"""


        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        processed_file=handle_file(file_path)
        if processed_file is not None:
            all_files.append(processed_file)
    print(all_files)
    return redirect(url_for('options'))  # Assurez-vous de rediriger vers la bonne route


@app.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        start_time = timeit.default_timer()
        form_data = request.form.getlist('options')
        options_functions = {
            'excel': writeExcel,
            'ppt': writeppt,
        }

        for file in all_files:
            register_jv = 'jv' in form_data
            filename=file.split("\\")[-1]
            socketio.emit('message', {'data': f"Creating database for file {filename}"})
            data_list = create_db(file, register_jv)
            print(type(data_list), data_list)
            for option in form_data:
                if option == 'jv':
                    continue
                func = options_functions[option]
                for data in data_list:
                    socketio.emit('message', {'data': f"Processing {option} on file {filename}"})
                    func(data)
        all_files.clear()
        socketio.emit('message', {'data': "Finished processing."})
        end_time = timeit.default_timer()
        print(f"Finished in {end_time-start_time} seconds")
        return render_template("finish.html")
    else:
        return render_template('options.html')


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
