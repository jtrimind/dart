import pandas as pd
import OpenDartReader

api_key = '133579488f1e7f9a44707b2a7d2be9999840935a'
dart = OpenDartReader(api_key)

def getFinstate(corp, year, quarter):
    # "11013"=1분기보고서,  "11012"=반기보고서,  "11014"=3분기보고서, "11011"=사업보고서
    reprt_code = {1: '11013',
                  2: '11012',
                  3: '11014',
                  4: '11011'}
    return dart.finstate(corp, year, reprt_code=reprt_code[quarter])


def getProfitFromFinstate(finstate):
    if finstate is None:
        return 0
    finstate = finstate.set_index('account_nm')
    profit = finstate.loc['당기순이익', 'thstrm_amount']
    if not isinstance(profit, str):
        profit = profit[0]
    if profit == '-':
        profit = 0
    else:
        profit = int(profit.replace(',', ''))
    return profit


def getAssetFromFinstate(finstate):
    if finstate is None:
        return 0
    finstate = finstate.set_index('account_nm')
    asset = finstate.loc['자본총계', 'thstrm_amount']
    if not isinstance(asset, str):
        asset = asset[0]
    asset = int(asset.replace(',', ''))
    return asset


def getProfit(corp, year, quarter):
    finstate = getFinstate(corp, year, quarter)
    return getProfitFromFinstate(finstate)


def getAsset(corp, year, quarter):
    finstate = getFinstate(corp, year, quarter)
    return getAssetFromFinstate(finstate)


def get4QProfit(corp, year, quarter):
    # 21. 1Q / 20. 4Q / 20. 1Q
    # A      / B     / C
    profit_a = getProfit(corp, year, quarter)
    profit_b = getProfit(corp, year - 1, 4)
    profit_c = getProfit(corp, year - 1, quarter)
    return profit_a + profit_b - profit_c


def getValue(corp, year, quarter):
    profit = (get4QProfit(corp, year, quarter) * 3 +
              get4QProfit(corp, year - 1, quarter) * 2 +
              get4QProfit(corp, year - 2, quarter)) / 6
    profit = profit * 10
    asset = getAsset(corp, year, quarter)
    return (int)(profit * 0.6 + asset * 0.4)
