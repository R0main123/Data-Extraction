import timeit
from pymongo import MongoClient


def filter_by_meas(meas=list, wafer_id=str):
    """
    This function browse the database to find all structures that have the types of measurements specified.
    :param <list> meas: List of str, contains all Measurements that wants to be matched
    :param <str> wafer_id: Name of the wafer_id

    :return <list>: A list of structures that contains the specified measurements
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    if wafer is None:
        return []

    list_of_structures = set()

    for structure in wafer["structures"]:
        if any(result in meas for result in
               (result for matrix in structure["matrices"] for result in matrix["results"])):
            list_of_structures.add(structure["structure_id"])

    return list(list_of_structures)

def filter_by_temp(temps=list, wafer_id=str):
    """
        This function browse the database to find all structures that have the temperature specified.
        :param <list> temps: List of str, contains all temperatures that wants to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified temperatures
        """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    if wafer is None:
        return []
    list_of_structures = set()

    for structure in wafer["structures"]:
        if any(matrix["results"][result]["Temperature"] in temps for matrix in structure["matrices"] for result in matrix["results"]):
            list_of_structures.add(structure["structure_id"])

    return list(list_of_structures)

def filter_by_coord(coords=list, wafer_id=str):
    """
        This function browse the database to find all structures that have a matrix with the couple of coordinates specified.
        :param <list> coords: List of str, contains all couples of coordinates that want to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified coordinates
        """
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
    """
        This function browse the database to find all structures that have measurements from thr file specified.
        :param <list> files: List of str, contains all files that wants to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified files
        """
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
