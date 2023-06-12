import gc
import timeit
import io
from pymongo import MongoClient, UpdateOne
from split_data import spliter, dataSpliter, C_spliter
def create_db(path=str, is_JV=bool):
    """
    This function create a database or open it if it already exists, and fill it with measurement information
    """
    start_time = timeit.default_timer()
    list_of_wafers = set()
    print("Creating/opening database")
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Measurements']

    collection = db["Wafers"]

    print("Processing...")
    with io.open(path, 'r',buffering=128*128) as file:
        i=1
        while True:
            IV = False
            JV = False
            CV = False
            It = False
            start_iter = timeit.default_timer()
            line = next((l for l in file if 'wafer' in l), None)
            if not line:
                break
            wafer_id = spliter(line)

            if wafer_id not in list_of_wafers:
                list_of_wafers.add(wafer_id)

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

            if is_JV:
                line = next((l for l in file if 'testdeviceArea' in l), None)
                if not line:
                    break
                area = float(spliter(line))

            line = next((l for l in file if 'procedureName' in l), None)
            if not line:
                break
            procedure = spliter(line)

            if procedure == "oxide_breakdown":
                IV = True
                if is_JV:
                    JV=True
            elif "cv" in procedure: CV = True
            elif "it" in procedure: It = True
            else: return

            if IV:
                result1_values = []
                result2_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result1_values.append((data[0], data[1]))

                result_1 = [{"V": v, "I": i} for v, i in result1_values]

                if JV:
                    for double in result1_values:
                        result2_values.append((float(double[0]), float(double[1]) / area))
                    result_2 = [{"V": v, "J": j} for v, j in result2_values]

            elif CV:
                line = next((l for l in file if 'curveValue' in l), None)
                if not line:
                    break
                V1 = C_spliter(line)[0]
                V2 = C_spliter(line)[-1]

                result_c_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result_c_values.append((data[0], data[1], data[2]))
                result_c = [{"V": v, f"{V1}": cs, f"{V2}":rs} for v, cs, rs in result_c_values]

            elif It:
                result_it_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result_it_values.append((data[0], data[1]))
                result_it = [{"V": v, "It": it} for v, it in result_it_values]


            wafer_checker = collection.find_one({"wafer_id": wafer_id})

            # We search for the wafer we are studying. If it doesn't exist, we create it
            if wafer_checker is None:
                wafer = {"wafer_id": wafer_id, "structures": []}
            else:
                wafer = wafer_checker

            # Try to find the structure we want to update/add in the wafer document
            structure = next((s for s in wafer["structures"] if s["structure_id"] == testdeviceID), None)

            # ...
            # If the structure does not exist in the wafer, create a new structure
            if structure is None:
                structure = {"structure_id": testdeviceID, "matrices": []}
                wafer["structures"].append(structure)
                matrix_id = "die_1"
            else:
                # If the structure already exists, calculate the new matrix_id
                matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in structure["matrices"]]
                matrix_id = f"die_{max(matrix_ids) + 1}"

            # Now, structure refers to the structure we want to update/add in the wafer
            # Try to find the matrix we want to update/add in the structure
            matrix = next(
                (m for m in structure["matrices"] if m["coordinates"]["x"] == chipX and m["coordinates"]["y"] == chipY),
                None)

            # If the matrix does not exist in the structure, create a new matrix
            if matrix is None:
                matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                structure["matrices"].append(matrix)

            # ...

            # Now, matrix refers to the matrix we want to update/add in the structure
            # Update/add the results in the matrix
            if IV:
                if JV:
                    matrix["results"]["I"] = {"Type of meas": "I-V", "Values": result_1}
                    matrix["results"]["J"] = {"Type of meas": "J-V", "Values": result_2}
                else:
                    matrix["results"]["I"] = {"Type of meas": "I-V", "Values": result_1}
            elif CV:
                matrix["results"]["C"] = {"Type of meas": f"V-{V1}-{V2}", "Values": result_c}
            elif It:
                matrix["results"]["It"] = {"Type of meas": "V-TDDB", "Values": result_it}

            # Finally, replace the existing wafer document in the database with our updated wafer document
            # Or if the wafer did not exist in the database, this will create a new wafer document
            collection.replace_one({"wafer_id": wafer_id}, wafer, upsert=True)

            wafer = None
            structure = None
            matrix = None

            end_iter = timeit.default_timer()
            print(f"Iteration number {i} ended in {end_iter - start_iter} seconds.")
            i += 1
            gc.collect()
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    print(f"Success!\nEnded in {execution_time} secondes")

    return list_of_wafers
