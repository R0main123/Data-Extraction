import os
from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import pandas as pd
from getInfos import get_testdeviceArea
from createInfos import create

def IV(original_file):
    """
    This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current (A)
    :param <str> original_file: Path to your .txt file where measurements are stored
    :return: None
    """
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
    filename = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV.xlsx"

    title = filename.split("\\")[-1].split("_IV")[0] + ' IV'
    list_of_sheets = pd.ExcelFile(filename).sheet_names
    for sheet in list_of_sheets:
        mydf = pd.read_excel(filename, sheet_name=sheet)
        mydf.columns = [f"{col}#{i}" for i, col in enumerate(mydf.columns)]

        col_pairs = [(mydf.columns[i], mydf.columns[j]) for i in range(mydf.shape[1]) for j in
                     range(i + 1, mydf.shape[1])
                     if mydf.columns[i].split('#') == mydf.columns[j].split('#') and mydf.iloc[0, i] == mydf.iloc[0, j]]

        df = pd.DataFrame()
        processed_cols = set()
        for col1, col2 in col_pairs:
            temp_df = pd.concat([df[col1][1:].reset_index(drop=True), df[col2][1:].reset_index(drop=True)],
                                ignore_index=True)
            col_name = col1.split('#')[0]
            if col_name not in df:
                df[col_name] = temp_df
            else:
                df[col_name] = pd.concat([df[col_name], temp_df], ignore_index=True)
            processed_cols.add(col1)
            processed_cols.add(col2)

        for col in mydf.columns:
            if col not in processed_cols:
                df[col.split('#')[0]] = mydf[col].reset_index(drop=True)

        color_index = 0
        colonnes = []

        for col in df.columns:
            colonnes.append(col.split('.')[0])

        colonnes = set(colonnes)

        plt.figure()
        for col in colonnes:
            label_x = df[col].iloc[0]
            label_y = "Current Value (A)"

            df[col] = df[col].iloc[1:]
            df[col+'.1'] = df[col+'.1'].iloc[1:]

            df[col] = pd.to_numeric(df[col])
            df[col+'.1'] = abs(pd.to_numeric(df[col+'.1']))


            plt.plot(df[col], df[col+'.1'], color = str(colors[color_index%15]), label= col)


            plt.xlabel(label_x)
            plt.ylabel(label_y)

            plt.title(title + " " + sheet)

            plt.legend()

            plt.grid(True)


            color_index+=1
        plt.savefig("plots\\"+title + sheet+'.png')
        plt.close()

        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        left = Inches(1)
        top = Inches(1)

        slide.shapes.add_picture("plots\\"+title + sheet+'.png', left, top)


    prs.save("PowerPointFiles\plots_IV.pptx")
    print("Success !")

def JV(original_file):
    """
    This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current density (A/cm^2)

    :param <str> original_file: Path to your .txt file where measurements are stored
    :return: None
    """
    create(original_file)
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
    filename = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV.xlsx"
    fileInfo = original_file.split('/')[-1].split('.')[0] + '_infos.xlsx'

    title = filename.split("\\")[-1].split("_IV")[0] + ' JV'
    list_of_sheets = pd.ExcelFile(filename).sheet_names
    for sheet in list_of_sheets:
        mydf = pd.read_excel(filename, sheet_name=sheet)
        mydf.columns = [f"{col}#{i}" for i, col in enumerate(mydf.columns)]

        col_pairs = [(mydf.columns[i], mydf.columns[j]) for i in range(mydf.shape[1]) for j in
                     range(i + 1, mydf.shape[1])
                     if mydf.columns[i].split('#') == mydf.columns[j].split('#') and mydf.iloc[0, i] == mydf.iloc[0, j]]

        df = pd.DataFrame()
        processed_cols = set()
        for col1, col2 in col_pairs:
            temp_df = pd.concat([df[col1][1:].reset_index(drop=True), df[col2][1:].reset_index(drop=True)],
                                ignore_index=True)
            col_name = col1.split('#')[0]
            if col_name not in df:
                df[col_name] = temp_df
            else:
                df[col_name] = pd.concat([df[col_name], temp_df], ignore_index=True)
            processed_cols.add(col1)
            processed_cols.add(col2)

        for col in mydf.columns:
            if col not in processed_cols:
                df[col.split('#')[0]] = mydf[col].reset_index(drop=True)

        color_index = 0
        colonnes = []

        for col in df.columns:
            colonnes.append(col.split('.')[0])

        colonnes = set(colonnes)

        plt.figure()
        for col in colonnes:
            label_x = df[col].iloc[0]
            label_y = "Current Density (A/mm^2)"

            df[col] = df[col].iloc[1:]
            df[col+'.1'] = df[col+'.1'].iloc[1:]

            df[col] = pd.to_numeric(df[col])
            df[col+'.1'] = abs(pd.to_numeric(df[col+'.1']))

            df[col+'.1'] = df[col+'.1'] / get_testdeviceArea(col, fileInfo)

            plt.plot(df[col], df[col+'.1'], color = str(colors[color_index%15]), label= col)


            plt.xlabel(label_x)
            plt.ylabel(label_y)

            plt.title(title + " " + sheet)

            plt.legend()

            plt.grid(True)


            color_index+=1
        plt.savefig("plots\\"+title + sheet+'.png')
        plt.close()

        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)

        left = Inches(1)
        top = Inches(1)

        slide.shapes.add_picture("plots\\"+title + sheet+'.png', left, top)


    prs.save("PowerPointFiles\plots_JV.pptx")
    print("Success !")



#IV("AL213656_D02_IV.txt")