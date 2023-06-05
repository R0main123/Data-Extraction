import timeit
import os
import pandas as pd
from openpyxl.reader.excel import load_workbook
from pymongo import MongoClient

def Excel_IV(wafer_id=str):
    """
    This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
    :param <str> path: The path to the .txt file
    :return: None
    """
    start_time = timeit.default_timer()

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    #creating directory if it doesn't exist
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    #Creating Excel File
    filename = 'ExcelFiles\\'+wafer_id+'_IV.xlsx'

    #Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    #Processing files
    i = 1
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            start_iter = timeit.default_timer()
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

            end_iter = timeit.default_timer()
            print(f"Iteration number {i} ended in {end_iter - start_iter} seconds.")
            i += 1

    end_iter = timeit.default_timer()
    print(f"All iterations ended in {end_iter - start_iter} seconds.")
    pd.DataFrame().to_excel(filename, index=False)
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        for coord, df in df_dict.items():
            sheetName = coord
            if sheetName in list_of_sheets:
                df.to_excel(writer, sheet_name=sheetName, index=False, startcol=writer.sheets[sheetName].max_column)
            else:
                df.to_excel(writer, sheet_name=sheetName, index=False)
                list_of_sheets.append(sheetName)

    wb = load_workbook(filename)
    if 'Sheet1' in wb.sheetnames:
        del wb['Sheet1']
    wb.save(filename)

    end_time = timeit.default_timer()
    execution_time = end_time - start_time

    print(f"Ended in {execution_time} secondes")

def Excel_JV(wafer_id):
    """
    This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
    :param <str> path: The path to the .txt file
    :return: None
    """
    start_time = timeit.default_timer()

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    # creating directory if it doesn't exist
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    # Creating Excel File
    filename = 'ExcelFiles\\' + wafer_id + '_JV.xlsx'

    # Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    # Processing files
    i = 1
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            start_iter = timeit.default_timer()
            coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'

            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            testdeviceID = structure["structure_id"]
            voltages = ['Voltage (V)']
            I = ['J (A/cm^2)']
            for double in matrix["results"]["J"]["Values"]:
                voltages.append(double["V"])
                I.append(double["J"])

            new_df = pd.DataFrame(list(zip(voltages, I)), columns=[testdeviceID, testdeviceID + " "])
            df_dict[coord] = df_dict[coord].merge(new_df, left_index=True, right_index=True, how='outer')

            end_iter = timeit.default_timer()
            print(f"Iteration number {i} ended in {end_iter - start_iter} seconds.")
            i += 1

    end_iter = timeit.default_timer()
    print(f"All iterations ended in {end_iter - start_iter} seconds.")
    pd.DataFrame().to_excel(filename, index=False)

    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        for coord, df in df_dict.items():
            sheetName = coord
            if sheetName in list_of_sheets:
                df.to_excel(writer, sheet_name=sheetName, index=False, startcol=writer.sheets[sheetName].max_column)
            else:
                df.to_excel(writer, sheet_name=sheetName, index=False)
                list_of_sheets.append(sheetName)

    wb = load_workbook(filename)
    if 'Sheet1' in wb.sheetnames:
        del wb['Sheet1']
    wb.save(filename)

    end_time = timeit.default_timer()
    execution_time = end_time - start_time

    print(f"Ended in {execution_time} secondes")


