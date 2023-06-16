import timeit
from pymongo import MongoClient


def filter_by_meas(meas=list, wafer_id=str):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})

    list_of_structures = set()

    for structure in wafer["structures"]:
        if any(result in meas for result in
               (result for matrix in structure["matrices"] for result in matrix["results"])):
            list_of_structures.add(structure["structure_id"])

    return list(list_of_structures)

def filter_by_temp(temps=list, wafer_id=str):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    list_of_structures = set()

    for structure in wafer["structures"]:
        if any(matrix["results"][result]["Temperature"] in temps for matrix in structure["matrices"] for result in matrix["results"]):
            list_of_structures.add(structure["structure_id"])

    return list(list_of_structures)

def filter_by_coord(coords=list, wafer_id=str):
    coords = [tuple((couple.split(',')[0][1:], couple.split(',')[-1][:-1])) for couple in coords]

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    list_of_structures = set()

    for couple in coords:
        for structure in wafer["structures"]:
            for matrix in structure["matrices"]:
                if matrix["coordinates"]["x"] == couple[0] and matrix["coordinates"]["y"] == couple[1]:
                    list_of_structures.add(structure["structure_id"])
    return list(list_of_structures)

def filter_by_filename(files=list, wafer_id=str):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    list_of_structures = set()

    for file in files:
        for structure in wafer["structures"]:
            for matrix in structure["matrices"]:
                for result in matrix["results"]:
                    if matrix["results"][result]["Filename"] == file:
                        list_of_structures.add(structure["structure_id"])

    return list(list_of_structures)
