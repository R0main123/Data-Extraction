import os
from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient

from getInfos import get_testdeviceArea
from createInfos import create

def PowerPoint_IV(wafer_id):
    """
    This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current (A)
    :param <str> original_file: Path to your .txt file where measurements are stored
    :return: None
    """
    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_IV.pptx"):
        return
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    # creating directory if it doesn't exist
    if not os.path.exists("plots"):
        os.makedirs("plots")
    if not os.path.exists("PowerPointFiles"):
        os.makedirs("PowerPointFiles")

    prs = Presentation()
    colors = [
        '#FF0000',  # Rouge
        '#00FF00',  # Vert
        '#0000FF',  # Bleu
        '#FFFF00',  # Jaune
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#800000',  # Marron
        '#808000',  # Olive
        '#008000',  # Vert foncé
        '#008080',  # Vert d'eau
        '#000080',  # Bleu marine
        '#800080',  # Violet
        '#7F7F7F',  # Gris
        '#FF6600',  # Orange
        '#663399'  # Rebecca Purple
    ]

    # Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    # Processing files
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            coord = "("+matrix["coordinates"]["x"]+','+matrix["coordinates"]["y"]+')'

            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            testdeviceID = structure["structure_id"]
            voltages = ['Voltage (V)']
            I = ['I (A)']
            for double in matrix["results"]["I"]["Values"]:
                voltages.append(double["V"])
                I.append(double["I"])

            new_df = pd.DataFrame(list(zip(voltages, I)), columns=[testdeviceID, testdeviceID+" "])
            df_dict[coord] = df_dict[coord].merge(new_df, left_index=True, right_index=True, how = 'outer')

    for coord, df in df_dict.items():
        cols = [col.rstrip() for col in df.columns if col.endswith(' ')]
        plt.figure()
        color_index = 0
        for col in cols:

            label_x = df[col].iloc[0]
            label_y = "Current Value (A)"

            df[col] = df[col].iloc[1:]
            df[col + ' '] = df[col + ' '].iloc[1:]
            df[col + ' '] = abs(df[col + ' '])

            plt.plot(df[col], df[col+" "], str(colors[color_index%15]), label = col)

            plt.xlabel(label_x)
            plt.ylabel(label_y)
            plt.title(wafer_id + " " + coord)
            plt.legend()
            plt.grid(True)

            color_index += 1

        plt.savefig("plots\\" + wafer_id + coord + '.png')
        plt.close()

        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        left = Inches(1)
        top = Inches(1)

        slide.shapes.add_picture("plots\\" + wafer_id + coord + '.png', left, top)

        prs.save(f"PowerPointFiles\{wafer_id} plots_IV.pptx")
    print(f"Success!")


def PowerPoint_JV(wafer_id):
    """
        This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current (A)
        :param <str> original_file: Path to your .txt file where measurements are stored
        :return: None
        """
    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_JV.pptx"):
        return
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    # creating directory if it doesn't exist
    if not os.path.exists("plots"):
        os.makedirs("plots")
    if not os.path.exists("PowerPointFiles"):
        os.makedirs("PowerPointFiles")

    prs = Presentation()
    colors = [
        '#FF0000',  # Rouge
        '#00FF00',  # Vert
        '#0000FF',  # Bleu
        '#FFFF00',  # Jaune
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#800000',  # Marron
        '#808000',  # Olive
        '#008000',  # Vert foncé
        '#008080',  # Vert d'eau
        '#000080',  # Bleu marine
        '#800080',  # Violet
        '#7F7F7F',  # Gris
        '#FF6600',  # Orange
        '#663399'  # Rebecca Purple
    ]

    # Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    # Processing files
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'

            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            testdeviceID = structure["structure_id"]
            voltages = ['Voltage (V)']
            J = ['J (A/cm^2)']
            for double in matrix["results"]["J"]["Values"]:
                voltages.append(double["V"])
                J.append(double["J"])

            new_df = pd.DataFrame(list(zip(voltages, J)), columns=[testdeviceID, testdeviceID + " "])
            df_dict[coord] = df_dict[coord].merge(new_df, left_index=True, right_index=True, how='outer')

    for coord, df in df_dict.items():
        cols = [col.rstrip() for col in df.columns if col.endswith(' ')]
        plt.figure()
        color_index = 0
        for col in cols:
            label_x = df[col].iloc[0]
            label_y = "Current density (A/cm^2)"

            df[col] = df[col].iloc[1:]
            df[col + ' '] = df[col + ' '].iloc[1:]
            df[col + ' '] = abs(df[col + ' '])

            plt.plot(df[col], df[col + " "], str(colors[color_index % 15]), label=col)

            plt.xlabel(label_x)
            plt.ylabel(label_y)
            plt.title(wafer_id + " " + coord)
            plt.legend()
            plt.grid(True)

            color_index += 1

        plt.savefig("plots\\" + wafer_id + coord + '.png')
        plt.close()

        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        left = Inches(1)
        top = Inches(1)

        slide.shapes.add_picture("plots\\" + wafer_id + coord + '.png', left, top)

        prs.save(f"PowerPointFiles\{wafer_id} plots_JV.pptx")
    print(f"Success!")





