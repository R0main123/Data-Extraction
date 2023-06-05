import tkinter as tk
from tkinterdnd2 import TkinterDnD
from excel import Excel_IV, Excel_JV
from init_BD import create_db
from plot_and_powerpoint import PowerPoint_IV, PowerPoint_JV
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5000)
