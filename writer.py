import os
import csv
import xlwt,xlrd
from xlutils.copy import copy
from .validate import validateFileStream,codingList


def writerToCsv(path:str,data:list,append=True,encoding="gbk")->bool:
    assert path.endswith(".csv"),"该路径非 .csv 结尾"
    mode = "a" if append else "w"
    csvFile = validateFileStream(path,mode=mode,encoding=encoding)
    csvWriter = csv.writer(csvFile)
    for item in data:
        if isinstance(item,list):
            csvWriter.writerow(codingList(item))
    csvFile.close()

def writerToXls(path:str,data:list,sheetByNameOrIndex=0,appendSheet=True,appendBook=True,encoding="gbk"):
    assert path.endswith(".xls"),"该路径非 .xls 结尾"

    if os.path.exists(path):
        if not appendBook:
            os.remove(path)
            return writerToXls(path,data,sheetByNameOrIndex,appendSheet,appendBook,encoding)
        readWorkbook = xlrd.open_workbook(path, formatting_info=True)
        writerWorkbook = copy(wb=readWorkbook)  # 完成xlrd对象向xlwt对象转换
        if sheetByNameOrIndex in readWorkbook.sheet_names():
            if type(sheetByNameOrIndex) == "int":
                sheet = readWorkbook.get_sheet(sheetByNameOrIndex)  # 获得要操作的页
            else:
                sheet = readWorkbook.sheet_by_name('{}'.format(sheetByNameOrIndex))
            rowNum = sheet.nrows  # 获得行数

            sheet = writerWorkbook.get_sheet(sheetByNameOrIndex)
            assert appendSheet ,"该 xls 文件已经存在 但 .xls 不支持覆盖 sheet"
        else:
            rowNum = 0
            sheet = writerWorkbook.add_sheet('{}'.format(sheetByNameOrIndex))
    else:
        # 创建一个workbook 设置编码
        writerWorkbook = xlwt.Workbook(encoding=encoding)
        # 创建一个worksheet
        sheet = writerWorkbook.add_sheet('{}'.format(sheetByNameOrIndex))
        rowNum = 0

    index = -1
    for rowIndex in range(rowNum,rowNum + len(data)):
        index += 1
        for cloIndex in range(0,len(data[index])):
            print(rowIndex, cloIndex, data[index][cloIndex])
            sheet.write(rowIndex, cloIndex, data[index][cloIndex])  # 因为单元格从0开始算，所以row不需要加一
    writerWorkbook.save(path)
    return True