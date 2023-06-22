import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
from pymongo import MongoClient
import seaborn as sns


def calculate_breakdown(X, Y, compliance=0.0001):

    if compliance is None:
        compliance = 0.0001


    if type(compliance) == str:
        compliance = float(compliance)

    X = np.array(X)
    Y = np.absolute(np.array(Y))
    #print(f"Y= {Y}")

    DiffY = np.gradient(Y, X)
    #print(f"DiffY= {DiffY}")
    pos = []

    for i in range(1, Y.shape[0]):
        if Y[i] > compliance and -1e-10 < DiffY[i] < 1e-10:
            pos.append(X[i])


    if len(pos) > 0:
        pos0 = pos[0]

        idx = pos0 if pos0 <= 1 else pos0 - 1

        Breakd_Leak = Y[np.where(X == pos[0])]
        Breakd_Volt = pos[0]

    else:
        Breakd_Leak = np.nan
        Breakd_Volt = np.nan

    if np.any(Y >= compliance):
        reached_comp = 1
        high_leak = compliance

    else:
        reached_comp = 0
        high_leak = np.max(Y)

    return Breakd_Volt, Breakd_Leak, reached_comp, high_leak

def get_vectors_in_matrix(wafer_id, structure_id, x, y):
    if type(x) != str:
        x = str(x)

    if type(y) != str:
        y = str(y)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                if matrix["coordinates"]["x"] == x and matrix["coordinates"]["y"] == y:
                    for result in matrix["results"]:
                        if result == "I":
                            X = []
                            Y = []
                            for double in matrix["results"][result]["Values"]:
                                X.append(double["V"])
                                Y.append(double["I"])
                    break
            break

    return X, Y

def get_matrices_with_I(wafer_id, structure_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    list_of_matrices = []

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                if "I" in matrix["results"]:
                    list_of_matrices.append(f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})")

    return list_of_matrices

def get_all_x(wafer_id, structure_id):
    all_x = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                all_x.append(matrix["coordinates"]["x"])

            all_x = list(map(float, all_x))
            all_x.sort()

            return list(set(all_x))

    return list(set(all_x))

def get_all_y(wafer_id, structure_id):
    all_y = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                all_y.append(matrix["coordinates"]["y"])

            all_y = list(map(float, all_y))
            all_y.sort()


            return list(set(all_y))

    return list(set(all_y))

def create_wafer_map(wafer_id, structure_id, compliance=float):
    X = np.array(get_all_x(wafer_id, structure_id))
    Y = np.array(get_all_y(wafer_id, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    VBDs = np.zeros((len_y, len_x))


    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                vec_X, vec_Y = get_vectors_in_matrix(wafer_id, structure_id, matrix["coordinates"]["x"], matrix["coordinates"]["y"])
                VBD = calculate_breakdown(vec_X, vec_Y, compliance)[0]

                if not (np.isnan(VBD)):
                    VBDs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = VBD

                else:
                    VBDs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = np.nan


    VBDs[VBDs==0] = np.nan

    x_ticks = np.linspace(min_x, max_x, VBDs.shape[1])
    y_ticks = np.linspace(min_y, max_y, VBDs.shape[0])

    cmap = colors.LinearSegmentedColormap.from_list(
        "mycmap", [(0, "blue"), (1, "red")]
    )

    sns.heatmap(VBDs, cmap=cmap)

    plt.xticks(np.arange(0, VBDs.shape[1], 2), x_ticks[::2])
    plt.yticks(np.arange(0, VBDs.shape[0], 4), y_ticks[::4])

    plt.show()

    return VBDs


#print(create_wafer_map("AL213656_D02", "CAP-BEOL11_19-1000_1000-BEOL11", 0.0001))




"""start_time = timeit.default_timer()
iter = 0
real = 0
compliance = 1e-5
client = MongoClient('mongodb://localhost:27017/')
db = client['Measurements']
collection = db["Wafers"]

wafers = collection.find({})

for wafer in wafers:
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
            for result in matrix["results"]:
                if result == "I":
                    iter+=1
                    X = []
                    Y = []
                    for double in matrix["results"][result]["Values"]:
                        X.append(double["V"])
                        Y.append(double["I"])

                    Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y, compliance)
                    if not np.isnan(Breakd_Volt):
                        real+=1
                        print(f"Wafer: {wafer['wafer_id']}, Structure: {structure['structure_id']}, matrice: ({matrix['coordinates']['x']}, {matrix['coordinates']['y']})")
                        print(f"Résultat: {Breakd_Volt, Breakd_Leak, reached_comp, high_leak}")

end_time = timeit.default_timer()
print(f"Time: {end_time - start_time}. {iter} itérations. {real} VBD trouvés")"""

