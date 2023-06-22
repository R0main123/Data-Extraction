from pymongo import MongoClient

def get_wafer(wafer_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    return collection.find_one({"wafer_id": wafer_id})

def get_types(wafer_id=str):
    wafer = get_wafer(wafer_id)
    list_of_types = set()
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            for result in matrix["results"]:
                list_of_types.add(result)
                if len(list_of_types) >= 4:
                    return list(list_of_types)
    return list(list_of_types)

def get_temps(wafer_id=str):
    wafer = get_wafer(wafer_id)
    return list(set(matrix["results"][result]["Temperature"] for structure in wafer["structures"] for matrix in structure["matrices"] for result in matrix["results"]))

def get_coords(wafer_id=str):
    wafer = get_wafer(wafer_id)
    return list(set(f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})" for structure in wafer["structures"] for matrix in structure["matrices"]))

def get_filenames(wafer_id=str):
    wafer = get_wafer(wafer_id)
    return list(set(matrix['results'][result]['Filename'] for structure in wafer["structures"] for matrix in structure["matrices"] for result in matrix["results"]))

def get_compliance(wafer_id=str, structure_id=str):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            return structure.get("compliance")

    return None



