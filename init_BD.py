import timeit

from pymongo import MongoClient
from txt_to_excel import spliter, dataSpliter
def create_db(path):
    """This function create a database or open it if it already exists, and fill it with measurement information """
    start_time = timeit.default_timer()
    print("Creating/opening database")
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Measurements']

    collection = db["Wafers"]
    wafer = None
    matrices = None

    print("Processing...")
    with open(path, 'r') as file:
        i=1
        while True:
            start_iter = timeit.default_timer()
            line = next((l for l in file if 'wafer' in l), None)
            if not line:
                break
            wafer_id = spliter(line)

            line = next((l for l in file if 'chipX' in l), None)
            if not line:
                break
            chipX = spliter(line)

            line = next((l for l in file if 'chipY' in l), None)
            if not line:
                break
            chipY = spliter(line)

            line = next((l for l in file if 'testdeviceID' in l), None)
            if not line:
                break
            testdeviceID = spliter(line)

            line = next((l for l in file if 'testdeviceArea' in l), None)
            if not line:
                break
            area = float(spliter(line))

            result1_values = []

            line = next((l for l in file if 'BOD' in l), None)
            if not line:
                break

            # Collecting measures values
            for line in file:
                if 'EOD' in line:
                    break
                data = dataSpliter(line)
                result1_values.append((data[0],data[1]))

            result2_values = []

            for double in result1_values:
                result2_values.append((float(double[0]), float(double[1])/area))

            wafer = collection.find_one({"wafer_id": wafer_id})

            #We search for the wafer we are studying. If it doesn't exists, we create it
            if wafer is None:
                new_wafer = {"wafer_id": wafer_id, "structures": []}

                structure = {"structure_id": testdeviceID, "matrices":[]}
                new_wafer["structures"].append(structure)

                matrix = {"matrix_id": "die_1", "coordinates": {"x": chipX, "y":chipY },"results":[]}
                structure["matrices"].append(matrix)

                result_1 = {"Type of meas": "I-V", "Values": result1_values}
                matrix["results"].append(result_1)

                result_2 = {"Type of meas": "J-V", "Values": result2_values}
                matrix["results"].append(result_2)

                collection.insert_one(new_wafer)

            #If the wafer exists, we check if he already has the structure we are treating
            else:
                my_wafer = collection.find_one({"wafer_id": wafer_id, "structures.structure_id":testdeviceID})

                #We search for the structure we want to add. If it doesn't exist, we create it
                if my_wafer is None:
                    structure = {"structure_id": testdeviceID, "matrices": []}

                    matrix = {"matrix_id": "die_1", "coordinates": {"x": chipX, "y": chipY}, "results": []}
                    structure["matrices"].append(matrix)

                    result_1 = {"Type of meas": "I-V", "Values": result1_values}
                    matrix["results"].append(result_1)

                    result_2 = {"Type of meas": "J-V", "Values": result2_values}
                    matrix["results"].append(result_2)

                    collection.update_one({"wafer_id": wafer_id}, {"$push": {"structures": structure}})

                #If the structure exists, we add it a new die

                #Here, we create the ID of the new die: we get all IDs that already exist and we
                else:
                    matrix_ids = []
                    for structure in my_wafer["structures"]:
                        if structure['structure_id'] == testdeviceID:
                            for matrix in structure["matrices"]:
                                matrix_ids.append(int(matrix["matrix_id"].split('_')[-1]))
                    matrix_id = f"die_{max(matrix_ids) + 1}"


                    matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": []}

                    result_1 = {"Type of meas": "I-V", "Values": result1_values}
                    matrix["results"].append(result_1)

                    result_2 = {"Type of meas": "J-V", "Values": result2_values}
                    matrix["results"].append(result_2)

                    collection.update_one({"wafer_id": wafer_id, "structures.structure_id": testdeviceID}, {"$push": {"structures.$.matrices": matrix}})

            wafer = None

            end_iter = timeit.default_timer()
            print(f"Iteration number {i} ended in {end_iter - start_iter} seconds.")
            i += 1
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"Success!\nEnded in {execution_time} secondes")


create_db("Datas\AL213656_D02_IV.txt")