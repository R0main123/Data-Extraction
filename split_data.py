def spliter(line):
    """
    This function takes a line of a header from a .txt file in argument and returns the relevant information in this line
    :param <str> line: The line you want to extract the information
    :return: the information needed
    :rtype: str
    """
    return line.split(' : ')[-1][:-1]

def dataSpliter(line):
    """
    This function takes a line of datas from a .txt file in argument and returns a list with voltage in first position and current in second position
    :param <str> line: The line you want to extract the information
    :return: the information needed
    :rtype: list of str
    """
    datas = [float(line[:-1].split('\t')[0]), float(line[:-1].split('\t')[-1])]
    return datas