import os
import timeit

from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient

def PowerPoint_IV(wafer_id):
    """
    This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current (A)
    :param <str> original_file: Path to your .txt file where measurements are stored
    :return: None
    """
    start_time = timeit.default_timer()
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
    end_time = timeit.default_timer()
    print(f"I-V PowerPoint successfully created for {wafer_id} in {end_time-start_time} seconds!")


def PowerPoint_JV(wafer_id):
    """
        This function takes a path to a txt file in argument and creates a Powerpoint where are stored the plots between voltage (V) and current (A)
        :param <str> original_file: Path to your .txt file where measurements are stored
        :return: None
        """
    start_time = timeit.default_timer()
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
    end_time = timeit.default_timer()
    print(f"J-V PowerPoint successfully created for {wafer_id} in {end_time-start_time} seconds!")



def writeppt(wafer):
    print("Starting...")
    if not os.path.exists("plots"):
        os.makedirs("plots")
    if not os.path.exists("PowerPointFiles"):
        os.makedirs("PowerPointFiles")

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer})

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
    df_dict = {}

    prs = Presentation()
    wafer_id = wafer["wafer_id"]
    print(f"Processing wafer {wafer_id}")
    df_dict["I"] = {}
    df_dict["J"] = {}
    df_dict["C"] = {}
    df_dict["It"] = {}

    for structure in wafer["structures"]:
        structure_id = structure["structure_id"]
        print(f"Processing structure {structure_id} in wafer {wafer_id}")

        for matrix in structure["matrices"]:
            coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'
            print(f"Processing matrix {coord} in structure {structure_id} in wafer {wafer_id}")
            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            for element in matrix["results"]:
                print(f"Processing {element} for matrix {coord} in structure {structure_id} in wafer {wafer_id}")
                if element == "I":
                    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_{element}V.pptx"):
                        continue
                    if coord not in df_dict["I"]:
                        df_dict["I"][coord] = pd.DataFrame()

                    voltages = ['Voltage (V)']
                    I = ['I (A)']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        I.append(double["I"])

                    new_df = pd.DataFrame(list(zip(voltages, I)), columns=[structure_id, structure_id + " "])
                    df_dict["I"][coord] = df_dict["I"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')
                    I.clear()
                    voltages.clear()

                elif element == "J":
                    if coord not in df_dict["J"]:
                        df_dict["J"][coord] = pd.DataFrame()
                    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_{element}V.pptx"):
                        continue
                    voltages = ['Voltage (V)']
                    J = ['J (A/cm^2)']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        J.append(double["J"])

                    new_df = pd.DataFrame(list(zip(voltages, J)), columns=[structure_id, structure_id + " "])
                    df_dict["J"][coord] = df_dict["J"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')
                    J.clear()
                    voltages.clear()

                elif element == "C":
                    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_{element}V.pptx"):
                        continue

                    if coord not in df_dict["C"]:
                        df_dict["C"][coord] = pd.DataFrame()
                    voltages = ['Voltage (V)']
                    CS = ['CS (Ω)']
                    RS = ['RS (Ω)']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        CS.append(double["CS"])
                        RS.append(double["RS"])

                    new_df = pd.DataFrame(list(zip(voltages, CS, RS)),
                                          columns=[structure_id, structure_id + " ", structure_id + "  "])
                    df_dict["C"][coord] = df_dict["C"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')
                    voltages.clear()
                    CS.clear()
                    RS.clear()

                elif element == "It":
                    if os.path.exists(f"PowerPointFiles\{wafer_id} plots_{element}V.pptx"):
                        continue
                    if coord not in df_dict["It"]:
                        df_dict["It"][coord] = pd.DataFrame()
                    voltages = ['Voltage (V)']
                    It = ['TDDB']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        It.append(double["TDDB"])

                    new_df = pd.DataFrame(list(zip(voltages, It)), columns=[structure_id, structure_id + " "])
                    df_dict["It"][coord] = df_dict["It"][coord].merge(new_df, left_index=True, right_index=True,
                                                                      how='outer')
                    voltages.clear()
                    It.clear()

        for element in ["I","J","C","It"]:
            if df_dict[element] != {}:
                print(f"Making plots for {element} in wafer {wafer_id}")
                for coord, df in df_dict[element].items():
                    print(df.columns)
                    cols = [col.rstrip() for col in df.columns if col.endswith(' ')]
                    plt.figure()
                    color_index = 0
                    for col in cols:
                        label_x = df[col].iloc[0]
                        label_y = element

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
                        #df_dict[element].clear()

                    print(f"Making Powerpoint for {element} in wafer {wafer_id}")
                    plt.savefig("plots\\" + wafer_id + coord + '.png')
                    plt.close()

                    slide_layout = prs.slide_layouts[1]
                    slide = prs.slides.add_slide(slide_layout)

                    left = Inches(1)
                    top = Inches(1)

                    slide.shapes.add_picture("plots\\" + wafer_id + coord + '.png', left, top)

                prs.save(f"PowerPointFiles\{wafer_id} plots_{element}V.pptx")

    print("Success!")


