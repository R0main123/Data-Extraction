from excel import Excel_IV, Excel_JV
from init_BD import create_db
from plot_and_powerpoint import PowerPoint_IV, PowerPoint_JV
from flask import Flask, render_template, request, redirect, url_for, session


all_files=[]

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    files = request.files.getlist('file[]')

    for file in files:
        print(f"File name: {file.filename}")
        all_files.append(file)
    print(all_files)

    # Retourne l'URL de redirection comme réponse
    return url_for('options')


@app.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        form_data = request.form.getlist('options')
        files = session.get('files', [])

        options_functions = {
            'register_iv': create_db,
            'register_jv': create_db,  # à remplacer par votre fonction
            'excel_iv': Excel_IV,
            'excel_jv': Excel_JV,
            'ppt_iv': PowerPoint_IV,
            'ppt_jv': PowerPoint_JV,
        }

        for file in files:
            register_iv = 'register_iv' in form_data
            register_jv = 'register_jv' in form_data
            if register_iv or register_jv:
                data_list = create_db(file, register_jv)
            else:
                continue  # Skip this file if no register is checked

            for option in form_data:
                if option in ['register_iv', 'register_jv']:
                    continue
                func = options_functions[option]
                for data in data_list:
                    func(data)
        return 'Operation completed!'
    else:
        return render_template('options.html')


if __name__ == '__main__':
    app.run(debug=True, port = 5000)
