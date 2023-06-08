from excel import Excel_IV, Excel_JV, Excel_CV, Excel_TDDB
from init_BD import create_db
from plot_and_powerpoint import PowerPoint_IV, PowerPoint_JV
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from converter import handle_file
import os

all_files=[]

app = Flask(__name__)
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
        form_data = request.form.getlist('options')
        files = all_files
        options_functions = {
            'excel_iv': Excel_IV,
            'excel_jv': Excel_JV,
            'excel_cv':Excel_CV,
            'excel_TDDB': Excel_TDDB,
            'ppt_iv': PowerPoint_IV,
            'ppt_jv': PowerPoint_JV,
        }

        for file in all_files:
            register_jv = 'register_jv' in form_data
            data_list = create_db(file, register_jv)

            for option in form_data:
                if option in ['register_iv', 'register_jv']:
                    continue
                func = options_functions[option]
                for data in data_list:
                    func(data)
        all_files.clear()
        return render_template("finish.html")
    else:
        return render_template('options.html')


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
