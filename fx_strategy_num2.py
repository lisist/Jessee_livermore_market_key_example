from contextlib import nullcontext
from numpy.core.numeric import NaN
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("krw.csv",index_col="Date",parse_dates=True)
data = data.sort_index(ascending=True)
data = data[0:500]


max = data['KRW'].values[0]
min = data['KRW'].values[0]

previous_peak = max
previous_peak_count = 0
previous_trough = min
previous_trough_count = 0
buy_signal = []
sell_signal = []
daily_return = data.shift(-1)/data-1
total_return = 1

min_data = []
max_data = []

pivot =max * 0.005


for k in data.index[1:]:
    i = data[data.index==k].values[0][0]
    if i > max:
        max = i
    elif i < min :
        min = i
    elif i < max * 1-pivot and previous_peak != max:
        if previous_peak_count >= 2:
            previous_peak_count = 0
        previous_peak = max
        min = i
        previous_peak_count += 1
    
    elif i > min * 1 + pivot and previous_trough != min:
        previous_trough = min
        max = i
   
    min_data = min_data + [previous_trough]
    max_data = max_data + [previous_peak]


min_data= pd.DataFrame(min_data,index=data.index[1:])
max_data= pd.DataFrame(max_data,index=data.index[1:])

trend_buy = False
trend_sell = False

## buy sell signal
## 1. sell signal : 하방 추세선이 전 대비 하락한 상황에서 최근 가격이 그 하방 추세선을 하향 돌파할 때 진입
## 1.1 sell signal 종료 : sell-signal 상황일 때 최근 가격이 상방 추세선을 상향 돌파할 경우
## 2. buy signal : 상방 추세선이 전 대비 상승한 상황에서 최근 가격이 그 상방 추세선을 상향 돌파할 때 진입
## 2.1 buy signal 종료 : buy-signal 상황일 때 최근 가격이 하방 추세선을 하향 돌파할 때 
## 3. sell signal의 재점화 : 하방 추세선이 전 대비 상승한 상황에서도 최근 가격이 그 직전 하방 추세선을 하향 돌파할 때 sell-signal 재점화
## 4. buy signal의 재점화 : 상방 추세선이 전 대비 하락한 상황에서도 최근 가격이 그 직전 상방 추세선을 상향 돌파할 때 buy-signal 재점화
for i in data.index[1:]:
    price = data[data.index==i].values[0][0]
    floor = min_data[min_data.index==i].values[0][0]
    ceiling = max_data[max_data.index==i].values[0][0]
    
    if trend_buy == True:
        if ceiling_prev < ceiling and price < ceiling:
            trend_buy = False
        else:
            buy_signal = buy_signal +[i]
    elif trend_sell == True:
        if floor_prev > floor and price > floor:
            trend_sell = False
        else:
            sell_signal = sell_signal + [i]
    else:
        if price > ceiling * 1.01:
            buy_signal = buy_signal  + [i]
            trend_buy = True
        elif price < floor * 0.99:
            sell_signal = sell_signal + [i]
            trend_sell = True

    floor_prev = min_data[min_data.index==i].values[0][0]
    ceiling_prev = max_data[max_data.index==i].values[0][0]


### return graph
df_buy_sell = pd.DataFrame([0]*len(data.index),index=data.index[:],columns=['signal'])


for i in data.index[1:]:
    if i in buy_signal:
        df_buy_sell['signal'][i]=1

    elif i in sell_signal:
        df_buy_sell['signal'][i]=-1

# df_buy_sell.to_csv("buysell.csv")

df_buy_sell['return'] = daily_return[:]

df_buy_sell['st_return'] = df_buy_sell['signal'] * df_buy_sell['return']

total_return = 1
total_return_list = []
for i in df_buy_sell['st_return'][:-1]:
    total_return = total_return * (1+i)
    total_return_list = total_return_list + [total_return]

df_returns = pd.DataFrame(total_return_list,index=data[0:-1].index)

print(total_return)

ax = min_data.plot()
max_data.plot(ax=ax)
data[1:].plot(ax=ax)
df_returns.plot()
plt.show()
