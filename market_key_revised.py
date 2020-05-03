# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:40:28 2020

@author: KIC
"""

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

data = pd.read_csv("C:/Users/developer/PycharmProjects/Jesse_livermore/venv/test_price.csv",
                   index_col="Date", parse_dates=True)
initial_set = "downtrend"
key_figure = 2

dic_data = {'price': np.nan,
            'state': np.nan,
            'prev_state': np.nan,
            'latest_uptrend': np.nan,
            'latest_downtrend': np.nan,
            'latest_rally': np.nan,
            'latest_reaction': np.nan,
            'latest_second_rally': np.nan,
            'latest_second_reaction': np.nan,
            'redline_uptrend': np.nan,
            'redline_reaction': np.nan,
            'blackline_downtrend': np.nan,
            'blackline_rally': np.nan}


def from_uptrend(df_data, k_figure=key_figure):
    ## to downturn
    if np.isnan(df_data['latest_downtrend']) == False and df_data['price'] < df_data['latest_downtrend']:
        df_data['state'] = "downtrend"
        df_data['latest_downtrend'] = df_data['price']
    ## to reaction or secondary reaction
    elif df_data['price'] < df_data['latest_uptrend'] - k_figure:
        # if np.isnan(df_data['latest_reaction']) != True and df_data['price'] > df_data['latest_reaction']:
        #     df_data['state'] = "second_reaction"
        #     df_data['latest_second_reaction'] = df_data['price']
        # else:
        df_data['state'] = "reaction"
        df_data['latest_reaction'] = df_data['price']
    ## continue
    else:
        df_data['state'] = "uptrend"
        if df_data['price'] > df_data['latest_uptrend'] or np.isnan(df_data['latest_uptrend']) == True:
            df_data['latest_uptrend'] = df_data['price']

    return (df_data)


def from_downtrend(df_data, k_figure=key_figure):
    ## to uptrend
    if np.isnan(df_data['latest_uptrend']) == False and df_data['price'] > df_data['latest_uptrend']:
        df_data['state'] = "uptrend"
        df_data['latest_uptrend'] = df_data['price']
    ## to rally or secondary rally
    elif df_data['price'] > df_data['latest_downtrend'] + k_figure:
        # if np.isnan(df_data['latest_rally']) != True and df_data['price'] < df_data['latest_rally']:
        #     df_data['state'] = "second_rally"
        #     df_data['latest_second_rally'] = df_data['price']
        # else:
        df_data['state'] = "rally"
        df_data['latest_rally'] = df_data['price']
    ## continue
    else:
        df_data['state'] = "downtrend"
        if df_data['price'] < df_data['latest_downtrend'] or np.isnan(df_data['latest_downtrend']) == True:
            df_data['latest_downtrend'] = df_data['price']

    return (df_data)


def from_rally(df_data, k_figure=key_figure):
    ## to uptrend
    if np.isnan(df_data['latest_uptrend']) == False and df_data['price'] > df_data['latest_uptrend']:
        df_data['state'] = "uptrend"
        df_data['latest_uptrend'] = df_data['price']
    elif df_data['price'] > df_data['blackline_rally'] + k_figure / 2:
        df_data['state'] = "uptrend"
        df_data['latest_uptrend'] = df_data['price']

    ## to reaction
    elif df_data['price'] < df_data['latest_rally'] - k_figure:
        if np.isnan(df_data['latest_reaction']) == False and df_data['price'] > df_data['latest_reaction']:
            df_data['state'] = "second_reaction"
            df_data['latest_second_reaction'] = df_data['price']
        else:
            df_data['state'] = "reaction"
            df_data['latest_reaction'] = df_data['price']

    ## continue
    else:
        df_data['state'] = "rally"
        if df_data['price'] > df_data['latest_rally'] or np.isnan(df_data['latest_rally']) == True:
            df_data['latest_rally'] = df_data['price']

    return (df_data)


def from_reaction(df_data, k_figure=key_figure):
    ## to downtrend
    if np.isnan(df_data['latest_downtrend']) == False and df_data['price'] < df_data['latest_downtrend']:
        df_data['state'] = "downtrend"
        df_data['latest_downtrend'] = df_data['price']
    elif df_data['price'] < df_data['redline_reaction'] - k_figure / 2:
        df_data['state'] = "downtrend"
        df_data['latest_downtrend'] = df_data['price']

    ## to rally
    elif df_data['price'] > df_data['latest_reaction'] + k_figure:
        if np.isnan(df_data['latest_rally']) == False and df_data['price'] < df_data['latest_rally']:
            df_data['state'] = "second_rally"
            df_data['latest_second_rally'] = df_data['price']
        else:
            df_data['state'] = "rally"
            df_data['latest_rally'] = df_data['price']

    ## continue
    else:
        df_data['state'] = "reaction"
        if df_data['price'] < df_data['latest_reaction'] or np.isnan(df_data['latest_reaction']) == True:
            df_data['latest_reaction'] = df_data['price']

    return (df_data)


def from_second_rally(df_data, k_figure=key_figure):
    ## to rally
    if df_data['price'] > df_data['latest_rally']:
        df_data['state'] = "rally"
        df_data['latest_rally'] = df_data['price']

    ## to reaction
    elif df_data['price'] < df_data['latest_reaction']:
        df_data['state'] = "reaction"
        df_data['latest_reaction'] = df_data['price']

    ## continue
    else:
        df_data['state'] = "second_rally"
        df_data['latest_second_rally'] = df_data['price']

    return(df_data)


def from_second_reaction(df_data, k_figure=key_figure):
    ## to reaction
    if df_data['price'] < df_data['latest_reaction']:
        df_data['state'] = "reaction"
        df_data['latest_reaction'] = df_data['price']

    ## to rally
    elif df_data['price'] > df_data['latest_rally']:
        df_data['state'] = "rally"
        df_data['latest_rally'] = df_data['price']

    ## continue
    else:
        df_data['state'] = "second_reaction"
        df_data['latest_second_reaction'] = df_data['price']

    return (df_data)


def liner(df_data, k_figure=key_figure):
    ## (a) 통상적인 조정 칸에 수치를 기록하기 시작한 첫 날, 상승 추세 칸에 기록한 가장 최근 수치 밑에 빨간 줄을 긋는다.
    ## 상승 추세 칸의 가장 최근 가격에서 처음으로 약 6포인트 조정이 이루어졌을 때 시작하면 된다
    if df_data['state'] == "reaction" and df_data['prev_state'] != "reaction":
        if np.isnan(df_data['latest_uptrend']) == False:
            df_data['redline_uptrend'] = df_data['latest_uptrend']

    ## (b) 통상적인 반등 칸 혹은 상승 추세 칸에 수치를 기록하기 시작한 첫날,
    ## 통상적인 조정 칸의 가장 최근 수치 밑에 빨간 줄을 긋는다.
    ## 통상적인 조정 칸의 최근 가격에서 처음으로 약 6포인트의 반등이 이루어졌을 때를 출발점으로 하면 된다.
    if df_data['state'] == "rally" and df_data['prev_state'] != "rally":
        if np.isnan(df_data['latest_reaction']) == False:
            df_data['redline_reaction'] = df_data['latest_reaction']

    if df_data['state'] == "uptrend" and df_data['prev_state'] != "uptrend":
        if np.isnan(df_data['latest_reaction']) == False:
            df_data['redline_reaction'] = df_data['latest_reaction']

    ## (c) 통상적인 반등 칸에 수치를 기록하기 시작한 첫날, 하락 추세 칸의 가장 최근 수치 밑에 검은 줄을 긋는다.
    ## 하락 추세 칸의 가장 최근 가격에서 처음으로 약 6포인트 반등이 이루어졌을 때 시작하면 된다.
    if df_data['state'] == "rally" and df_data['prev_state'] != "rally":
        if np.isnan(df_data['latest_downtrend']) == False:
            df_data['blackline_downtrend'] = df_data['latest_downtrend']

    ## (d) 통상적인 조정 칸에 혹은 하락 추세 칸에 수치를 기록하기 시작한 첫날,
    ## 통상적인 반등 칸의 가장 최근 수치 밑에 검은 줄을 긋는다.
    ## 통상적인 반등 칸의 가장 최근 가격에서 처음으로 약 6포인트 조정이 이루어졌을 때 시작하면 된다.
    if df_data['state'] == "reaction" and df_data['prev_state'] != "reaction":
        if np.isnan(df_data['latest_reaction']) == False:
            df_data['blackline_rally'] = df_data['latest_rally']

    if df_data['state'] == "downtrend" and df_data['prev_state'] != "downtrend":
        if np.isnan(df_data['latest_reaction']) == False:
            df_data['blackline_rally'] = df_data['latest_rally']

    return (df_data)


## Initial Setting

prev_data = dic_data.copy()
prev_data['price'] = data['Price'][0]
prev_data['prev_state'] = initial_set

df = pd.DataFrame(prev_data, index=[0])

## Iteration

for i in data['Price'][1:]:
    cur_data = prev_data.copy()
    cur_data['price'] = i
    cur_data['state'] = np.nan

    if cur_data['prev_state'] == "downtrend":
        cur_data = from_downtrend(cur_data)
    elif cur_data['prev_state'] == "uptrend":
        cur_data = from_uptrend(cur_data)
    elif cur_data['prev_state'] == "rally":
        cur_data = from_rally(cur_data)
    elif cur_data['prev_state'] == "reaction":
        cur_data = from_reaction(cur_data)
    elif cur_data['prev_state'] == "second_rally":
        cur_data = from_second_rally(cur_data)
    elif cur_data['prev_state'] == "second_reaction":
        cur_data = from_second_reaction(cur_data)

    cur_data = liner(cur_data)

    prev_data = cur_data.copy()
    prev_data['prev_state'] = prev_data['state']

    df = df.append(cur_data, ignore_index=True)
    df.to_csv("C:/Users/developer/PycharmProjects/Jesse_livermore/venv/df.csv")

## plotting

range_list = []
range_list2 = []
range_list3 = []
range_list4 = []

for idx, val in (df['state'] == "reaction").iteritems():
    if val != False:
        start = idx
        range_list.append(start)

for idx, val in (df['state'] == "rally").iteritems():
    if val != False:
        start = idx
        range_list2.append(start)

for idx, val in (df['state'] == "uptrend").iteritems():
    if val != False:
        start = idx
        range_list3.append(start)

for idx, val in (df['state'] == "downtrend").iteritems():
    if val != False:
        start = idx
        range_list4.append(start)

plt.plot(df['price'],color="black")
# plt.plot(df['latest_reaction'], color="blue",linestyle='--')
# plt.plot(df['latest_rally'], color="blue",linestyle=':')
plt.plot(df['blackline_downtrend'], color="blue",linestyle='--')
plt.plot(df['blackline_rally'], color="blue",linestyle='--')
plt.plot(df['redline_uptrend'], color="red",linestyle='--')
plt.plot(df['redline_reaction'], color="red",linestyle='--')

for x in range_list:
    plt.axvspan(x, x + 1, facecolor="grey", alpha=0.5)
for x in range_list2:
    plt.axvspan(x, x + 1, facecolor="orange", alpha=0.5)
for x in range_list3:
    plt.axvspan(x, x + 1, facecolor="red", alpha=0.5)
for x in range_list4:
    plt.axvspan(x, x + 1, facecolor="black", alpha=0.5)

plt.show()