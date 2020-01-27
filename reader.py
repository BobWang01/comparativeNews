import csv

def csvReader(path,encoding="gbk"):
    csvFile = open(path, encoding=encoding)
    csvReader = csv.reader(csvFile)
    dataList = list(csvReader)
    csvFile.close()
    return dataList

