import pandas as pd

def get_testdeviceArea(testdeviceID, infofile):
    df = pd.read_excel(infofile)
    for index, row in df.iterrows():
        if row["testdeviceID"] == testdeviceID:
            area = row["testdeviceArea"]
            break
    return float(area)
