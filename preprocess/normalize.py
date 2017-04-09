# Normalize time series data
from sklearn import preprocessing
import pandas as pd

df = pd.read_csv('data/m_fm_3_601318_20150301_20160302.csv')
# print df
dff = df.drop(df.columns[[0, 1, 2]], axis=1).dropna(axis=1).dropna()

print dff

x = dff
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
# print x_scaled
dfop = pd.DataFrame(x_scaled, columns=dff.columns)
print dfop
dfop.to_csv("norm_m_fm_601318.csv")
