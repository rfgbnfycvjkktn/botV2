import requests
import json
from datetime import date, timedelta


# приходит словарь
def get_bonds(param):
    # запрос данных по бумагам
    # "/iss/engines/stock/markets/bonds/boardgroups/58/securities.json?iss.dp=comma&iss.meta=off&iss.only=securities,marketdata&securities.columns=SECID,SECNAME,PREVLEGALCLOSEPRICE,BOARDID&marketdata.columns=SECID,YIELD,DURATION"

    bonds = []

    yieldless = param['yieldless']
    yieldmore = param['yieldmore']
    priceless = param['priceless']
    pricemore = param['pricemore']
    durationless = param['durationless']
    durationmore = param['durationmore']
    volume = param['volume']

    for g in ['7', '58', '193']:
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/bonds/boardgroups/' + g + '/securities.json'
                                                                                      '?iss.dp=comma&iss.meta=off&iss.only=securities,marketdata&securities.columns=SECID,'
                                                                                      'SECNAME,PREVLEGALCLOSEPRICE,BOARDID&marketdata.columns=SECID,YIELD,DURATION')

        if response.status_code == 200:
            alldata = json.loads(response.text)
            securities = alldata['securities']['data']
            marketdata = alldata['marketdata']['data']

            count = len(securities)
            i = 0
            while i < count:
                bondid = securities[i][0]
                bondname = securities[i][1]
                bondprice = securities[i][2] or 0
                bondboardid = securities[i][3]
                bondyield = marketdata[i][1]
                bondduration = round((marketdata[i][2] or 0) / 30, 1)

                i += 1
                if bondprice > priceless and bondprice < pricemore and bondyield > yieldless and bondyield < yieldmore and bondduration > durationless and bondduration < durationmore:
                    bondvolume = get_bondvolume(bondid, bondboardid)
                    if bondvolume > volume:
                        bonds.append([bondid, bondname, bondprice, bondyield, bondvolume, bondduration])
            print('Данные получены')

        else:
            return bonds

    return bonds


def get_bondvolume(secid, boardid):
    datevolume = str(date.today() - timedelta(days=15))
    # print(date.today() - timedelta(days=15))
    response = requests.get(
        'https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/' + boardid + '/securities/' + secid + '.json?iss.meta=off&iss.only=history&history.columns=SECID,TRADEDATE,VOLUME,NUMTRADES&limit=20&from=' + datevolume + '')

    if response.status_code == 200:
        vol = 0
        data = json.loads(response.text)
        for key in data['history']['data']:
            vol += key[2]
        return vol

    return 0
