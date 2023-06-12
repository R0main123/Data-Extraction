from excel import writeExcel
from init_BD import create_db
from plot_and_powerpoint import writeppt
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from converter import handle_file
import os
import timeit


all_files=[]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = '.\DataFiles\\'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("file")
    for file in files:
        # Utilisez la fonction secure_filename pour vous assurer qu'il n'y a pas de noms de fichiers malveillants
        filename = secure_filename(file.filename)
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
        print(f"Finished in {end_time-start_time}")
        return render_template("finish.html")
    else:
        return render_template('options.html')


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
