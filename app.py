from pymongo import MongoClient
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
import os
import timeit
import numpy as np

from excel import writeExcel, excel_structure
from manage_DB import create_db, register_compliance, register_VBD
from plot_and_powerpoint import writeppt, ppt_structure, ppt_matrix
from converter import handle_file
from getter import get_types, get_temps, get_filenames, get_coords, get_compliance, get_VBDs, get_matrices_with_I
from filter import filter_by_meas, filter_by_temp, filter_by_coord, filter_by_filename
from VBD import calculate_breakdown, get_vectors_in_matrix, create_wafer_map

all_files = []

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

@app.route('/excel_structure/<wafer_id>/<structure_ids>/<file_name>', methods=['GET'])
def excel_structure_route(wafer_id, structure_ids, file_name):
    structure_ids = structure_ids.split(',')
    excel_structure(wafer_id, structure_ids, file_name)
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
    structure = [s for s in wafer["structures"] if s["structure_id"] == structure_id][0]
    matrices = structure["matrices"]
    return jsonify(matrices)

@app.route('/plot_matrix/<wafer_id>/<coordinates>', methods=['GET'])
def plot_matrix(wafer_id=str, coordinates=str):
    return jsonify(ppt_matrix(wafer_id, coordinates))

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
    data = request.get_json()
    selectedMeasurements = data["coords"]
    return jsonify(filter_by_coord(selectedMeasurements, wafer_id)), 200

@app.route('/filter_by_Filenames/<wafer_id>/<selectedMeasurements>', methods=['GET'])
def filter_by_Filenames(wafer_id, selectedMeasurements):
    selectedMeasurements = selectedMeasurements.split(',')
    return jsonify(filter_by_filename(selectedMeasurements, wafer_id)), 200
@app.route('/write_ppt/<wafer_id>', methods=['POST'])
def write_ppt_route(wafer_id):
    writeppt(wafer_id)
    return render_template('done.html', message='PowerPoint file successfully created!')

@app.route('/ppt_structure/<wafer_id>/<structure_ids>/<file_name>', methods=['GET'])
def ppt_structure_route(wafer_id, structure_ids, file_name):
    structure_ids = structure_ids.split(',')
    ppt_structure(wafer_id, structure_ids, file_name)
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
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    files = request.files.getlist("file")
    for file in files:

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        processed_file = handle_file(file_path)

        if processed_file is not None:
            all_files.append(processed_file)

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

            for option in form_data:

                if option == 'jv':
                    continue

                func = options_functions[option]

                for data in data_list:

                    socketio.emit('message', {'data': f"Processing {option} on file {filename}"})
                    func(data)

            if os.path.isfile(file):
                os.remove(file)

        all_files.clear()

        if os.path.isdir("DataFiles"):
            if not os.listdir("DataFiles"):
                os.rmdir("DataFiles")

        socketio.emit('message', {'data': "Finished processing."})

        end_time = timeit.default_timer()
        print(f"Finished in {end_time-start_time} seconds")

        return render_template("finish.html")

    else:
        return render_template('options.html')

@app.route("/get_matrices_with_I/<wafer_id>/<structure_id>", methods=["GET"])
def get_matrices_for_VBD(wafer_id, structure_id):
    return jsonify(get_matrices_with_I(wafer_id, structure_id))


@app.route("/calculate_breakdown/<wafer_id>/<structure_id>/<x>/<y>/<compliance>", methods=["GET"])
def flask_calculate_breakdown(wafer_id, structure_id, x, y, compliance):
    X, Y = get_vectors_in_matrix(wafer_id, structure_id, x, y)

    if compliance !='null':
        Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y, compliance)

    else:
        Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y)

    if np.isnan(Breakd_Volt):
        return jsonify("NaN")
    else:
        return jsonify(Breakd_Volt)

@app.route("/calculate_breakdown/<wafer_id>/<structure_id>/<x>/<y>/", methods=["GET"])
def flask_calculate_breakdown_wout_compl(wafer_id, structure_id, x, y):
    X, Y = get_vectors_in_matrix(wafer_id, structure_id, x, y)

    Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y)

    if np.isnan(Breakd_Volt):
        return jsonify("NaN")
    else:
        return jsonify(Breakd_Volt)

@app.route("/get_breakdown/<wafer_id>/<structure_id>/<x>/<y>/", methods=["GET"])
def flask_get_breakdown(wafer_id, structure_id, x, y):
    return jsonify(get_VBDs(wafer_id, structure_id, x, y))

@app.route("/get_vectors_in_matrix/<waferId>/<structureId>/<x>/<y>")
def get_vectors_for_matrix(waferId, structureId, x, y):
    return jsonify(get_vectors_in_matrix(waferId, structureId, x, y))

@app.route("/get_compl/<waferId>/<structureId>")
def get_compl(waferId, structureId):
    compliance = get_compliance(waferId, structureId)
    if compliance is None:
        return jsonify("")
    else:
        return jsonify(compliance)

@app.route("/create_wafer_map/<waferId>/<structureId>")
def wafer_map(waferId, structureId):
    image = create_wafer_map(waferId, structureId)
    return jsonify({"image": image})


@app.route("/set_compl/<waferId>/<structureId>/<compliance>")
def set_compl(waferId, structureId, compliance):
    register_compliance(waferId, structureId, compliance)
    return jsonify({'result': 'success'}), 200

@app.route("/reg_vbd/<waferId>/<structureId>/<x>/<y>/<VBD>")
def reg_VBD(waferId, structureId, x, y, VBD):
    register_VBD(waferId, structureId, x, y, VBD)
    return jsonify({'result': 'success'}), 200

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
