import pandas as pd

def get_testdeviceArea(testdeviceID, infofile):
    """
    This function takes the ID of a test device and a path to a .txt file and return the area of the test device
    :param <str> testdeviceID: ID of the test device
    :param <str> infofile: path to the file
    :return: the area of the test device
    :rtype: float
    """
    df = pd.read_excel(infofile)
    for index, row in df.iterrows():
        if row["testdeviceID"] == testdeviceID:
            area = row["testdeviceArea"]
            break
    return float(area)
