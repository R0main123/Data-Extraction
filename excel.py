import timeit
import os
import pandas as pd
from openpyxl.reader.excel import load_workbook
from pymongo import MongoClient

def Excel_IV(structure_id=str, values=list,wafer=str, df_dict=dict, filename=str, list_of_sheets=list):
    """
    This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
    :param <str> path: The path to the .txt file
    :return: None
    """

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

            #i += 1

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


    #print(f"I-V Excel successfully Ended in {execution_time} seconds for {wafer_id} ({i} iterations)")

def Excel_JV(wafer_id=str):
    """
    This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
    :param <str> path: The path to the .txt file
    :return: None
    """
    if os.path.exists(f"ExcelFiles\\{wafer_id}_JV.xlsx"):
        return
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
            i += 1

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

    print(f"J-V excel successfully created for {wafer_id}. Ended in {execution_time} secondes")


def Excel_CV(wafer_id=str):
    """
     This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
     :param <str> path: The path to the .txt file
     :return: None
     """

    if os.path.exists(f"ExcelFiles\\{wafer_id}_CV.xlsx"):
        return
    start_time = timeit.default_timer()

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    # creating directory if it doesn't exist
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    # Creating Excel File
    filename = 'ExcelFiles\\' + wafer_id + '_CV.xlsx'

    # Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    # Processing files
    i = 1
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'

            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            testdeviceID = structure["structure_id"]
            voltages = ['Voltage (V)']
            CS = ['CS (Ω)']
            RS = ['RS (Ω)']
            for double in matrix["results"]["C"]["Values"]:
                voltages.append(double["V"])
                CS.append(double["CS"])
                RS.append(double["RS"])

            new_df = pd.DataFrame(list(zip(voltages, CS, RS)), columns=[testdeviceID, testdeviceID + " ", testdeviceID+ "  "])
            df_dict[coord] = df_dict[coord].merge(new_df, left_index=True, right_index=True, how='outer')

            i += 1

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

    print(f"C-V Excel successfully Ended in {execution_time} seconds for {wafer_id} ({i} iterations)")

def Excel_TDDB(wafer_id=str):
    """
    This function takes a path to a .txt file in argument and creates an excel files with the values of current depending on corresponding voltage
    :param <str> path: The path to the .txt file
    :return: None
    """

    if os.path.exists(f"ExcelFiles\\{wafer_id}_TDDB.xlsx"):
        return
    start_time = timeit.default_timer()

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})

    #creating directory if it doesn't exist
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    #Creating Excel File
    filename = 'ExcelFiles\\'+wafer_id+'_TDDB.xlsx'

    #Creating lists of sheets that already exists in the excel files
    list_of_sheets = []
    df_dict = {}  # using dictionary to store dataframes by coord keys

    #Processing files
    i = 1
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            coord = "("+matrix["coordinates"]["x"]+','+matrix["coordinates"]["y"]+')'

            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            testdeviceID = structure["structure_id"]
            voltages = ['Voltage (V)']
            It = ['TDDB']
            for double in matrix["results"]["It"]["Values"]:
                voltages.append(double["V"])
                It.append(double["It"])

            new_df = pd.DataFrame(list(zip(voltages, It)), columns=[testdeviceID, testdeviceID+" "])
            df_dict[coord] = df_dict[coord].merge(new_df, left_index=True, right_index=True, how = 'outer')

            i += 1

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

    print(f"TDDB Excel successfully Ended in {execution_time} seconds for {wafer_id} ({i} iterations)")


def writeExcel():
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    for wafer in collection.find():
        wafer_id = wafer["wafer_id"]

        for structure in wafer["structures"]:
            structure_id = structure["structure_id"]

            for matrix in structure["matrices"]:

                for result in matrix["results"]:

                    for element in result:
                        if element == "I":
                            I_values = Excel_IV(structure_id, result[element]["Values"])

                        elif element == "J":
                            J_values = Excel_JV()

                        elif element == "C":
                            C_values = Excel_CV()

                        elif element == "It":
                            It_values = Excel_TDDB()


#writeExcel()
