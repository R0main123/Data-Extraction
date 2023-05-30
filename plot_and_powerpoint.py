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
    colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'w']
    filename_pos = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV_pos.xlsx"
    filename_neg = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV_neg.xlsx"
    input_files = [filename_pos, filename_neg]

    for file in input_files:
        title = file.split("\\")[-1].split("_IV")[0] + ' IV'
        list_of_sheets = pd.ExcelFile(file).sheet_names
        for sheet in list_of_sheets:
            df = pd.read_excel(filename_pos, sheet_name = sheet)

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
                df[col+'.1'] = pd.to_numeric(df[col+'.1'])


                plt.plot(df[col], df[col+'.1'], color = str(colors[color_index%8]), label= col)


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
    colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'w']
    filename_pos = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV_pos.xlsx"
    filename_neg = "ExcelFiles\\"+original_file.split('.')[0].split('/')[-1]+"_Data_IV_neg.xlsx"
    input_files = [filename_pos, filename_neg]
    fileInfo = original_file.split('/')[-1].split('.')[0] + '_infos.xlsx'

    for file in input_files:
        title = file.split("\\")[-1].split("_IV")[0] + ' JV'
        list_of_sheets = pd.ExcelFile(file).sheet_names
        for sheet in list_of_sheets:
            df = pd.read_excel(filename_pos, sheet_name = sheet)

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
                df[col+'.1'] = pd.to_numeric(df[col+'.1'])

                df[col+'.1'] = df[col+'.1'] / get_testdeviceArea(col, fileInfo)

                plt.plot(df[col], df[col+'.1'], color = str(colors[color_index%8]), label= col)


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
