from bs4 import BeautifulSoup

def gengeralParamForParserTable(tag:str,attrs:dict=None,splitStart:int=None,splitEnd:int=None) -> dict:
    param = {'tag': tag, 'attrs': attrs, 'splitStart': splitStart, 'splitEnd': splitEnd}
    return param

def parserTable(soup:BeautifulSoup,searchParams:list,curFloor = 0,searchData=[]) -> list:
    if curFloor==len(searchParams):
        return searchData
    param = searchParams[curFloor]
    curFloor+=1
    tags = soup.find_all(param['tag'], attrs=param['attrs'])[param['splitStart']: param['splitEnd']]

    dataItem = []
    for tag in tags:
        if curFloor == len(searchParams):
            dataItem.append(tag.get_text().replace("\xa0",""))
        else:
            parserTable(tag,searchParams,curFloor,searchData)
    if dataItem:
        searchData.append(dataItem)
    return searchData
