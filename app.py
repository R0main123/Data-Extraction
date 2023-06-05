import tkinter as tk
from tkinterdnd2 import TkinterDnD
from excel import Excel_IV, Excel_JV
from init_BD import create_db
from plot_and_powerpoint import PowerPoint_IV, PowerPoint_JV
from flask import Flask, render_template, request

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


















































if __name__ == '__main__':
    app.run(port = 5000)
