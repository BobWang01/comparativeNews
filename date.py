import time

def currentSecondTimestamp() -> int:
    # 秒级时间戳
    return int(time.time())
def currentMillisecondTimestamp() -> int:
    # 豪秒级时间戳
    return int(time.time()*1000)

def dateToTimestamp(date:str = None,format:str='%Y-%m-%d %H:%M:%S') -> int:
    if not date:return currentMillisecondTimestamp()
    # 格式化时间转时间戳
    timeTuple = time.strptime(date, format)  # 把格式化好的时间转换成元祖
    result = time.mktime(timeTuple)  # 把时间元祖转换成时间戳
    return int(result)

def timestampToDate(timestamp:int = currentMillisecondTimestamp()/1000,format:str='%Y-%m-%d %H:%M:%S') -> str:
    # 时间戳格式化 秒级
    timeTuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
    result = time.strftime(format, timeTuple)  # 把时间元祖转换成格式化好的时间
    return result

if __name__ == '__main__':
    print("秒级时间戳",currentSecondTimestamp())
    print("豪秒级时间戳",currentMillisecondTimestamp())
    print("日期转时间戳",dateToTimestamp())
    print("时间戳转日期",timestampToDate())
    print("ceshi",timestampToDate(currentSecondTimestamp()-60*24*60,format="%Y%m%d"))