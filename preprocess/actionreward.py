# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


BUY = 0
HOLD = 1
SELL = 2

ACT = {}
ACT[0] = 'BUY'
ACT[1] = 'HOLD'
ACT[2] = 'SELL'


batchSize = 30


def splitDataFrameIntoSmaller(df, batchSize=30):
    listOfDf = list()
    numberChunks = len(df) // batchSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i * batchSize:(i + 1) * batchSize])
    return listOfDf


df = pd.read_csv('data/m_fm_3_601318_20150301_20160302.csv')
# 去除空数据
state = df.drop(df.columns[[0, 1, 2]], axis=1).dropna(axis=1).dropna()
stateList = splitDataFrameIntoSmaller(state, batchSize)
data = []
for batch, sl in enumerate(stateList):
    print "batch: %d ====================" % batch
    money = 10000  # 余额
    total = 10000  # 总市值
    position = 0  # 持仓
    for i in range(len(sl) - 2):
        reward = 0
        highestPrice = sl.iloc[i]['highestPrice']
        closePrice = sl.iloc[i]['closePrice']
        lowestPrice = sl.iloc[i]['lowestPrice']
        if position > 0:
            if money >= 100 * highestPrice:
                action = np.random.randint(0, 3)
            else:
                action = np.random.randint(1, 3)
        else:
            if money >= 100 * highestPrice:
                action = np.random.randint(0, 2)
            else:
                action = HOLD

        if action == BUY:
            position = position + 100
            money = money - 100 * closePrice
            total = money + position * closePrice
            reward = sl.iloc[i + 2]['lowestPrice'] - \
                sl.iloc[i + 1]['closePrice']
        if action == SELL:
            position = position - 100
            money = money + 100 * closePrice
            total = money + position * closePrice
            reward = sl.iloc[i + 1]['lowestPrice'] - \
                sl.iloc[i + 2]['closePrice']
        if action == HOLD:
            total = money + position * closePrice
            reward = 0
        print "batch: %d  day: %d  action: %s  reward: %.4f money: %.2f  position: %d  total: %f" % (batch, i, ACT[action], reward, money, position, total)

        data.append(
            {'batch': batch, 'day': i,
             'action': action, 'reward': reward,
             'money': money,
             'position': position, 'total': total})


dfReward = pd.DataFrame(
    data, columns=['batch', 'day', 'action', 'reward', 'money',
                   'position', 'total'])


pd.DataFrame(data, columns=['batch', 'day', 'action',
                            'reward', 'money', 'position', 'total']).to_csv("601318_20150301_20160302.csv")
