import re
import os
from .annotation import retry,sleep
# 格式化文件标题
def validateFileTitle(title:str) -> str:
    return re.sub(r"[\/\\\:\*\?\"\<\>\|]", '_', title.replace("/r","").replace("\n",""))

# 验证文件路径 如果不存在会创建
def validatePath(path) -> bool:
    if os.path.exists(path):
        return True
    else:
        try:
            os.makedirs(path)
        except:
            raise Exception
        else:
            return True

# 获取文件流
def validateFileStream(path,mode="a",retryNumber=10,sleepTime=0.5,encoding="gbk"):

    @retry(retryNumber)
    @sleep(sleepTime)
    def spin(path,mode):
        try:
            f = open(path,mode=mode,encoding=encoding,newline="")
        except:
            print("尝试获取 {} 写入权失败~重新尝试".format(path))
            raise Exception
        else:
            return f
    return spin(path,mode)


# 对list 进行统一编码 包括深层次的遍历
def codingList(dataList,coding="gbk") -> list:
    newData = []
    for item in dataList:
        if isinstance(item,str):
            newData.append(item.encode(coding,"ignore").decode(coding,"ignore"))
        elif isinstance(item,list):
            newData.append(codingList(item,coding))
        else:
            newData.append(item)
    return newData