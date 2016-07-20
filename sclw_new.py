# -*- coding: utf-8 -*-
#三重滤网交易系统
#from os.path import exists
import time, datetime, calendar
from datetime import date
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt


#下面是函数是将数据按周期统计
def data_to_weekly(df=pd.DataFrame()):
    df_week = pd.DataFrame()
    week_time_list = []
    week_pirce_list = []
    t = list(df['Date'])
    p = list(df['Close'])
    t.reverse()
    p.reverse()
    week_num = '0'
    for i in range(len(t)):
        year_p, month_p, day_p = t[i].split('-')
        day_new_p = date(int(year_p), int(month_p), int(day_p)) #转换为日期格式
        week_num_p = day_new_p.strftime('%Y%W')  #转换为字符格式
        if week_num != week_num_p :
            week_time_list.append(t[i])
            week_pirce_list.append(p[i])
        else:
            pass
        year_c, month_c, day_c = week_time_list[-1].split('-')
        day_new_c = date(int(year_c), int(month_c), int(day_c))
        week_num = day_new_c.strftime('%Y%W')
    week_time_list.reverse()
    week_pirce_list.reverse()
    df_week['wdate'] = week_time_list
    df_week['Close'] = week_pirce_list
    return df_week

#计算EMA
def ema(df=pd.DataFrame(), n1=13):
    df['ema_'+str(n1)] = df['Close'].ewm(span=n1).mean()
    return

#计算macd指标
def macd(df=pd.DataFrame(), n1=12, n2=26, n3=9):
    ema(df, n1)
    ema(df, n2)
    df['diff'] = df['ema_'+str(n1)] - df['ema_'+str(n2)]
    df['dea'] = df['diff'].ewm(span=n3).mean()
    df['macd'] = 2 * (df['diff'] - df['dea'])
    return

#计算强力指标
def findex(df=pd.DataFrame(), n1=2):
    ref_c_list = list(df['Close'])
    ref_c_list.insert(0, 0)
    ref_c_list.pop()
    df['ref_close'] = ref_c_list
    df['fi'] = df['Volume'] * (df['Close'] - df['ref_close'])
    df['ema_fi'] = df['fi'].ewm(span=n1).mean()
    return

#计算每天的周macd指标
def data_daily_wmacd(df=pd.DataFrame()):
    daily_wmacd_list = []
    for i in range(len(df['Date'])):
        df_temp = df[:i]
        df_week = data_to_weekly(df_temp)
        macd(df_week)
        weekly_macd_list = list(df_week['macd'])
        if weekly_macd_list:
            daily_wmacd_list.append(weekly_macd_list[-1])
        else:
            daily_wmacd_list.append(0)
    df['wmacd'] = daily_wmacd_list 
    return

#计算第一层滤网的趋势
def first_screen(df=pd.DataFrame()):
    ref_wmacd_list = list(df['wmacd'])
    ref_wmacd_list.insert(0, 0)
    ref_wmacd_list.pop()
    df['ref_wmacd'] = ref_wmacd_list
    df['weekly_temp_trend'] = df['wmacd'] - df['ref_wmacd']
    df['weekly_trend'] = []
    
    
    weekly_trend = []
    for i in range(len(wmacd_p)):
        p_list = p[i:]
        t_list = t[i:]
        weekly_t_list, weekly_p_list = data_to_weekly(t_list, p_list)
        weekly_macd_list = macd(12, 26, 9, weekly_p_list, 4562.03, 4049.35, 450.14)
        if i < len(wmacd_p) - 1 and len(weekly_macd_list) > 1:
            if wmacd_p[i] > weekly_macd_list[1]:
                weekly_trend.append(1)
            elif wmacd_p[i] < weekly_macd_list[1]:
                weekly_trend.append(-1)
            else:
                weekly_trend.append(0)
        else:
            weekly_trend.append(0)
    
    return 
    
    
'''    
#计算第一层滤网的趋势
def first_screen(wmacd_p=[], t=[], p=[]):
    weekly_trend = []
    for i in range(len(wmacd_p)):
        p_list = p[i:]
        t_list = t[i:]
        weekly_t_list, weekly_p_list = data_to_weekly(t_list, p_list)
        weekly_macd_list = macd(12, 26, 9, weekly_p_list, 4562.03, 4049.35, 450.14)
        if i < len(wmacd_p) - 1 and len(weekly_macd_list) > 1:
            if wmacd_p[i] > weekly_macd_list[1]:
                weekly_trend.append(1)
            elif wmacd_p[i] < weekly_macd_list[1]:
                weekly_trend.append(-1)
            else:
                weekly_trend.append(0)
        else:
            weekly_trend.append(0)
    return weekly_trend

#计算第二层滤网的信号
def second_screen(wmacd_trend=[], fi=[]):
    daily_flag = []
    for i in range(len(fi)):
        if wmacd_trend[i] > 0 and fi[i] < 0:
            daily_flag.append(2)
        elif wmacd_trend[i] < 0 and fi[i] > 0:
            daily_flag.append(-2)
        else:
            daily_flag.append(0)
    return daily_flag

#计算第三层滤网的信号
def thrid_screen(d_trend=[], p=[], h=[], l=[]):
    thrid_flag = []
    #print '*+' * 10
    #print 'len(d_trend)', len(d_trend)
    for i in range(len(d_trend)):
        if i == 0:
            pass
        elif i != 0 and (d_trend[i] > 0 and p[i-1] > h[i]):
            thrid_flag.append(3)
        elif i != 0 and (d_trend[i] < 0 and p[i-1] < l[i]):
            thrid_flag.append(-3)
        elif i == len(d_trend) - 1:
            thrid_flag.append(0)
            thrid_flag.append(0)
        else:
            thrid_flag.append(0)
    return thrid_flag

#计算止损价
def stop_loss(t_flag=[], p=[], h=[], l=[]):
    stop_flag = []
    hold_flag = 0
    stop_price = []
    buy_price = []
    sell_price = []
    #l1 = len(p)
    t_flag.reverse()
    p.reverse()
    h.reverse()
    l.reverse()
    for i in range(len(p)):
        if t_flag[i] == 3:
            stop_flag.append(4)
            hold_flag = 4
            stop_price.append(l[i-1])
            buy_price.append(h[i-1])
            sell_price.append(h[i-1])
        elif t_flag[i] == -3:
            stop_flag.append(-4)
            hold_flag = -4
            stop_price.append(h[i-1])
            buy_price.append(h[i-1])
        #已经有多头持仓并且价格没有达到止损
        elif hold_flag == 4 and l[i] > stop_price[-1]:
            stop_flag.append(4)
            stop_price.append(stop_price[-1])
        #多头持仓价格达到了止损
        elif hold_flag == 4 and l[ i] < stop_price[-1]:
            stop_flag.append(0)
            stop_price.append(0)
            hold_flag = 0
        #已经有空头持仓并且价格没有达到止损
        elif hold_flag == -4 and h[ i] < stop_price[-1]:
            stop_flag.append(-4)
            stop_price.append(stop_price[-1])
        #空头持仓价格达到了止损
        elif hold_flag == -4 and h[ i] > stop_price[-1]:
            stop_flag.append(0)
            stop_price.append(0)
            hold_flag = 0
        else:
            stop_flag.append(0)
            stop_price.append(0)
    stop_flag.reverse()
    stop_price.reverse()
    t_flag.reverse()
    return stop_flag, stop_price

#计算买入和卖出交易记录
def trade_record(s_flag=[], h=[], l=[]):
    open_record = []
    close_record = []
    porfit_record = []
    s_flag.reverse()
    for i in range(len(h)):
        if i == 0:
            open_record.append(0)
            close_record.append(0)
            porfit_record.append(0)
        #多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == 0:
            open_record.append(h[i-1])
            close_record.append(0)
            porfit_record.append(0)
        #空头平仓和多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == -4:
            open_record.append(h[i-1])
            close_record.append(h[i-1])
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        #多头持仓
        elif s_flag[i] == 4 and s_flag[i-1] == 4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(0)
        #多头平仓
        elif s_flag[i] == 0 and s_flag[i-1] == 4:
            open_record.append(0)
            close_record.append(l[i-1])
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 0:
            open_record.append(l[i-1])
            close_record.append(0)
            porfit_record.append(0)
        #多头平仓和空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 4:
            open_record.append(l[i-1])
            close_record.append(l[i-1])
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头持仓
        elif s_flag[i] == -4 and s_flag[i-1] == -4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(0)
        #空头平仓
        elif s_flag[i] == 0 and s_flag[i-1] == -4:
            open_record.append(0)
            close_record.append(h[i-1])
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        else:
            open_record.append(0)
            close_record.append(0)
            porfit_record.append(0)
    s_flag.reverse()
    open_record.reverse()
    close_record.reverse()
    porfit_record.reverse()
    return open_record, close_record, porfit_record

#资金管理
def money_manage(total_money=0, trade_min_num=0, s_flag=[], stop_price=[], open_record=[], close_record=[]):
    month_position = []
    position_num = []
    usable_money = []
    s_flag.reverse()
    stop_price.reverse()
    open_record.reverse()
    close_record.reverse()
    for i in range(len(s_flag)):
        if i == 0:
            month_position.append(0)
            position_num.append(0)
            usable_money.append(total_money)
        #多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == 0:
            position_temp_num = (usable_money[-1] * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)
            month_temp_p = (abs(open_record[i] - stop_price[i]) * int(position_temp_num)) / usable_money[-1]
            #print position_temp_num
            #print (abs(open_record[i] - stop_price[i]) * int(position_temp_num))
            #print 'month_temp_p', month_temp_p
            month_position.append(month_temp_p)
            position_num.append(int(position_temp_num))
            usable_temp_money = usable_money[-1] - (open_record[i] * int(position_temp_num))
            usable_money.append(usable_temp_money)
            #print usable_temp_money
        #空头平仓和多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == -4:
            position_temp_num = (usable_money[-1] * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)
            month_temp_p = (abs(open_record[i] - stop_price[i]) * int(position_temp_num)) / usable_money[-1]
            month_position.append(month_temp_p)
            position_num.append(int(position_temp_num))
            usable_temp_money = usable_money[-1] + (close_record[i] * int(position_num[i-1])) - (open_record[i] * int(position_temp_num))
            usable_money.append(usable_temp_money)
        #多头持仓
        elif s_flag[i] == 4 and s_flag[i-1] == 4:
            month_position.append(month_position[-1])
            position_num.append(position_num[-1])
            usable_money.append(usable_money[-1])
        #多头平仓
        elif s_flag[i] == 0 and s_flag[i-1] == 4:
            month_position.append(0)
            position_num.append(0)
            usable_temp_money = usable_money[-1] + (close_record[i] * int(position_num[i-1]))
            #print '********close_record[i]------', close_record[i]
            #print close_record[i] * int(position_num[i-1])
            #print usable_temp_money
            usable_money.append(usable_temp_money)
        #空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 0:
            position_temp_num = (usable_money[-1] * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)
            month_temp_p = (abs(open_record[i] - stop_price[i]) * int(position_temp_num)) / usable_money[-1]
            month_position.append(month_temp_p)
            position_num.append(int(position_temp_num))
            usable_temp_money = usable_money[-1] - (open_record[i] * int(position_temp_num))
            usable_money.append(usable_temp_money)
        #多头平仓和空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 4:
            position_temp_num = (usable_money[-1] * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)
            month_temp_p = (abs(open_record[i] - stop_price[i]) * int(position_temp_num)) / usable_money[-1]
            month_position.append(month_temp_p)
            position_num.append(int(position_temp_num))
            usable_temp_money = usable_money[-1] + (close_record[i] * int(position_num[i-1])) - (open_record[i] * int(position_temp_num))
            usable_money.append(usable_temp_money)
        #空头持仓
        elif s_flag[i] == -4 and s_flag[i-1] == -4:
            month_position.append(month_position[-1])
            position_num.append(position_num[-1])
            usable_money.append(usable_money[-1])
        #空头平仓
        elif s_flag[i] == 0 and s_flag[i-1] == -4:
            month_position.append(0)
            position_num.append(0)
            usable_temp_money = usable_money[-1] + (close_record[i] * int(position_num[i-1]))
            usable_money.append(usable_temp_money)
        else:
            month_position.append(0)
            position_num.append(0)
            usable_money.append(usable_money[-1])
    s_flag.reverse()
    stop_price.reverse()
    open_record.reverse()
    close_record.reverse()
    month_position.reverse()
    position_num.reverse()
    usable_money.reverse()
    return month_position, position_num, usable_money


#收益率的计算
def rate_calculate():
    pass


c_list, v_list, d_list, refc_list, h_list, l_list= read_file('300_test.txt')
d_wmacd_list = data_daily_wmacd(d_list, c_list)
fi2 = findex(2, v_list, c_list, refc_list, 51880529920.0)

first_w_list = first_screen(d_wmacd_list, d_list, c_list)
second_d_list = second_screen(first_w_list, fi2)
t_d_list = thrid_screen(second_d_list, c_list, h_list, l_list)
s_flag, s_price = stop_loss(t_d_list, c_list, h_list, l_list)
open_record1, close_record1, porfit_record1 = trade_record(s_flag, h_list, l_list)


month_position1, position_num1, usable_money1 = money_manage(1000000, 10, s_flag, s_price, open_record1, close_record1)
#print '-++-' * 10
#print len(month_position1), len(position_num1), len(usable_money1)

#读取历史数据格式模板
df_300 = pd.read_csv('399300.csv')

df_300['first_w_list'] = first_w_list
df_300['second_d_list'] = second_d_list
#df_300['d_wmacd_list'] = d_wmacd_list
df_300['t_d_list'] = t_d_list
df_300['Stopflag'] = s_flag
df_300['Stopprice'] = s_price
df_300['Openrecord'] = open_record1
df_300['Closerecord'] = close_record1
df_300['Porfitrecord'] = porfit_record1
df_300['Monthpositon'] = month_position1
df_300['PositionNum'] = position_num1
df_300['UsableMoney'] = usable_money1

#将处理后的数据写入到csv文件中
df_300.to_csv('df_300.csv', index=False)

print "Successful! Total is", len(t_d_list)

'''

df_510300 = pd.read_csv('ss_510300.csv')
df_510300.index = df_510300['Date']
data_daily_wmacd(df_510300)
findex(df_510300)

#df_510300['EMA12'] = df_510300['Close'].ewm(span=12).mean()
#df_510300['EMA13'] = df_510300['Close'].ewm(span=13).mean()
#df_510300['EMA26'] = df_510300['Close'].ewm(span=26).mean()
#df_510300['diff'] = df_510300['EMA12'] - df_510300['EMA26']
#df_510300['dea'] = df_510300['diff'].ewm(span=9).mean()
#df_510300['macd'] = 2 * (df_510300['diff'] - df_510300['dea'])



df_510300.to_csv('macd_fi_510300.csv', columns=['Date', 'Close', 'wmacd', 'ema_fi'])
