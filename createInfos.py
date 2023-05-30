import pandas as pd

def spliter(line):
    return line.split(' : ')[-1][:-1]

def dataSpliter(line):
    return line[:-1].split('\t')

def create(original_file):
    df = pd.DataFrame(columns = ['wafer', 'coordinates', 'testdeviceID', 'testdeviceArea', 'sign'])

    with open(original_file, 'r') as file:
        while True:
            line = file.readline()
            while "wafer" not in line:
                line = file.readline()
                if not line:
                    break
            wafer = spliter(line)

            while "chipX" not in line:
                line = file.readline()
                if not line:
                    break
            coordinates = '('+spliter(line)+','

            while "chipY" not in line:
                line = file.readline()
                if not line:
                    break
            coordinates += spliter(line)+')'

            while "testdeviceID" not in line:
                line = file.readline()
                if not line:
                    break
            testdeviceID = spliter(line)

            while "testdeviceArea" not in line:
                line = file.readline()
                if not line:
                    break
            testdeviceArea = spliter(line)

            while "BOD" not in line:
                line = file.readline()
                if not line:
                    break

            line = file.readline()
            if not line:
                break

            line = file.readline()
            if not line:
                break

            data = dataSpliter(line)


            if float(data[0]) > 0:
                sign = '+'
            else:
                sign = '-'
            df1 = pd.DataFrame([[wafer,coordinates,testdeviceID,testdeviceArea,sign]], columns=['wafer', 'coordinates', 'testdeviceID', 'testdeviceArea', 'sign'])
            df = pd.concat([df,df1])

    df.to_excel(original_file.split('/')[-1].split('.')[0]+'_infos.xlsx',index=False)

