# -*- coding: utf-8 -*-
#三重滤网交易系统
from os.path import exists
import time, datetime, calendar
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_file(filename):
    date_list =[]
    close_list = []
    vol_list =[]
    close_ref_list = []
    high_list = []
    low_list = []
    file = open(filename, 'r')
    s = []
    #f = file.readline()
    num_lines = sum(1 for line in file)
    file = open(filename, 'r')
    #print num_lines
    for i in range(int(num_lines)):
        #print i
        #file = open('300_test.txt', 'r')
        f = file.readline()
        s = f.split('\t')
        #print '*-' * 10
        #print f
        #print s
        close_list.append(float(s[3]))
        high_list.append(float(s[4])) 
        low_list.append(float(s[5])) 
        vol_list.append(float(s[-2]))
        date_list.append(s[0])
        close_ref_list.append(float(s[-5]))
    
    #price_data[str(s[0])] = s
    
    #print s[3]
    #print '1' * 10
    #print close_list
    #print vol_list
    #print date_list
    file.close()
    return close_list, vol_list, date_list, close_ref_list, high_list, low_list

def write_file(filename, c1, v1, d1):
    file = open(filename, 'w')
    for i in range(len(d1)):
        file.write(d1[i])
        file.write('\t')
        #print d1[0]
        #print c1[0]
        file.write(str(c1[i]))
        file.write('\t')
        file.write(str(v1[i]))
        file.write('\n')
    #print file
    file.close()

#下面是函数是将数据按周期统计
def data_to_weekly(t=[], p=[]):
    week_time_list = []
    week_pirce_list = []
    #year_nd, month_nd, day_nd = t[i].split('-')
    #new_date = date.today()
    #new_date = date(int(year_nd), int(month_nd), int(day_nd))

    #year_p, month_p, day_p = t[0].split('-')
    #day_new_p = date(int(year_p), int(month_p), int(day_p))
    #week_num_p = day_new_p.strftime('%Y%W')
    #week_num = day_new_p.strftime('%Y%W')
    week_num = '0'
    #i_count = 0
    for i in range(len(t)):
        year_p, month_p, day_p = t[i].split('-')
        day_new_p = date(int(year_p), int(month_p), int(day_p))
        week_num_p = day_new_p.strftime('%Y%W')
        #week_num_p_int = int(week_num_p)
        #print '/*-' * 9
        #print i
        #print int(len(week_time_list))
        #print week_num_p
        #x = int(week_num) - int(week_num_p)
        #print x
        #print week_num
        #print week_num_p
        #print 
        if week_num != week_num_p :
            #print '123' * 5
            week_time_list.append(t[i])
            week_pirce_list.append(p[i])
            #week_num_int = day_new_p.strftime('%Y%W')
            #i_count -= 1
            #print 'p[i]',p[i],i
        #elif week_num_int > week_num_p_int :
            #week_time_list.append(t[i])
            #week_pirce_list.append(p[i])
            #week_num_int -= 2
        else:
            pass
        
        year_c, month_c, day_c = week_time_list[-1].split('-')
        day_new_c = date(int(year_c), int(month_c), int(day_c))
        week_num = day_new_c.strftime('%Y%W')    
            
    #print 'p[i]',p[i],i        
    return week_time_list, week_pirce_list

#计算收盘价的MA移动平均，这个函数可以考虑优化
def ma(n1=13, p=[]):
    ma_list = []
    x = 0
    print len(p)
    for i in range(len(p)):
        #print i
        if int(len(p)) - i <= n1 + 1:
            ma_list.append(0.00)
        else:
            close_price_n1 = sum(p[i:n1+i])    
            #print '-' * 15
            #print i
            #print x
            #print len(p[i:n1+i])
            #print p[i:n1+i]
            close_ma =     close_price_n1 / n1
            ma_list.append(close_ma)
            x += 1
            
    #print sum(p[-n1:])
    result = ma_list
    #print result
    return result

#计算EMA    
def ema(n1=13, p=[], emafirst=0.0):
    ema_list = []
    k = 2.0 / (n1 + 1)
    x = 2
    #print len(p)
    for i in range(len(p)):
        #print i
        
        if i < 1:
            ema_list.insert(0, emafirst)
        else:    
            ema_yest = ema_list[0]
            #print ema_list
            #print 'ema_yest', ema_yest
            p_tod = p[-x]
            #print i
            #print 'p_tod', p_tod
            ema_tod = p_tod * k + ema_yest * (1 - k)
            #print 'ema_tod', ema_tod
            #print '-' * 15
            #print x
            #print len(p[x:n1+x])
            #print p[x:n1+x]
            ema_list.insert(0, ema_tod)            
            x += 1
            
    result = ema_list
    #print result
    return result    

def macd(n1=12, n2=26, n3=9, p=[], ema12first=0.0, ema26first=0.0, deaemafirst=0.0):
    diff_list = []
    dea_list = []
    macd_list = []
    k = 2.0 / (n1 + 1)
    x = 2
    #print len(p)
    diff_short = ema(n1, p, ema12first)
    diff_long = ema(n2, p, ema26first)
    
    for i in range(len(p)):
        #print i
        diff = diff_short[i] - diff_long[i]
        diff_list.append(diff)
        
    dea_list = ema(n3, diff_list, deaemafirst)    
    
    for i in range(len(p)):
        macd_tod = 2 * (diff_list[i] - dea_list[i])
        macd_list.append(round(macd_tod, 2))
        

    result = macd_list
    #print result
    return result    

def findex(n1=2, v=[], p=[], refp=[], fiemafirst=0.0):
    fi_first_list = []
    fi_ema_list =[]
    result = []
    for i in range(len(p)):
        #print '*-' * 10
        #print i
        
        close_price = p[i]
        ref_c_price = refp[i]
        #print close_price
        #print ref_c_price
        vol = v[i] / 100.0
        fi = vol * (close_price - ref_c_price)
        fi_first_list.append(fi)
        
    fi_ema_list = ema(n1, fi_first_list, fiemafirst)
    for i in range(len(fi_ema_list)):
        result.append(round(fi_ema_list[i], 2))
    
    #print result
    return result
    
def data_daily_wmacd(t=[], p=[]):
    daily_wmacd_list = []
    #print len(p)
    for i in range(len(p)):
        #year_wt, month_wt, day_wt = wt[i].split('-')
        #data_new_wt = date(int(year_wt), int(month_wt), int(day_wt))
        #wt_week_num = data_new_wt.strftime('%Y%W')
        #year_p, month_p, day_p = t[i].split('-')
        #day_new_p = date(int(year_p), int(month_p), int(day_p))
        #p_week_num = day_new_p.strftime('%Y%W')
        #print '*' *10, i
        p_list = p[i:]
        #print len(p_list)
        #print sum(p_list)
        t_list = t[i:]
        weekly_t_list, weekly_p_list = data_to_weekly(t_list, p_list)
        #print 'weekly_t_list',  weekly_t_list
        #print 'weekly_p_list',  weekly_p_list
        weekly_macd_list = macd(12, 26, 9, weekly_p_list, 4562.03, 4049.35, 450.14)
        #print weekly_macd_list
        #print len(weekly_macd_list)
        daily_wmacd_list.append(round(weekly_macd_list[0],2))
        #print 'daily_wmacd_list', daily_wmacd_list
    #print 'daily_wmacd_list', daily_wmacd_list
    return daily_wmacd_list
    
def first_screen(wmacd_p=[], t=[], p=[]):
    weekly_trend = []
    #print '*+' * 10
    #print weekly_macd
    for i in range(len(wmacd_p)):
        #print i
        #print weekly_macd[i]
        p_list = p[i:]
        t_list = t[i:]
        weekly_t_list, weekly_p_list = data_to_weekly(t_list, p_list)
        weekly_macd_list = macd(12, 26, 9, weekly_p_list, 4562.03, 4049.35, 450.14)
        #print '*-' * 10
        #print weekly_macd_list
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

def second_screen(wmacd_trend=[], fi=[]):
    daily_flag = []
    #daily_fi = findex(2, v, p, refc, 670516800.0)
    #print '*+' * 10
    #print daily_fi
    for i in range(len(fi)):
        #print i
        #print daily_fi[i]
        if wmacd_trend[i] > 0 and fi[i] < 0:
            daily_flag.append(2)
        elif wmacd_trend[i] < 0 and fi[i] > 0:
            daily_flag.append(-2)
        else:    
            daily_flag.append(0)

    return daily_flag    

def thrid_screen(d_trend=[], p=[], h=[], l=[]):
    thrid_flag = []
    #daily_fi = findex(2, v, p, refc, 670516800.0)
    print '*+' * 10
    print 'len(d_trend)', len(d_trend)
    for i in range(len(d_trend)):
        #print i
        #print daily_fi[i]
        if i == 0:
            pass
        elif i != 0 and (d_trend[i] > 0 and p[i-1] > h[i]):
            thrid_flag.append(3)
        elif i != 0 and (d_trend[i] < 0 and p[i-1] < l[i]):
            thrid_flag.append(-3)
        elif i == len(d_trend) - 1:
            #print 'abc456789'
            
            thrid_flag.append(0)
            #print len(thrid_flag)
            thrid_flag.append(0)
            #thrid_flag.append(0)
        else:    
            thrid_flag.append(0)

    return thrid_flag     

def stop_loss(t_flag=[], p=[], h=[], l=[]):
    stop_flag = []
    hold_flag = 0
    stop_price = []
    buy_price = []
    sell_price = []
    #daily_fi = findex(2, v, p, refc, 670516800.0)
    #print '*+' * 10
    #print daily_fi
    l1 = len(p)
    t_flag.reverse()
    p.reverse()
    h.reverse()
    l.reverse()
    for i in range(len(p)):
        #print i
        #print daily_fi[i]
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

def trade_record(s_flag=[], h=[], l=[]):
    open_record = []
    close_record = []
    porfit_record = []
    s_flag.reverse()
    #h.reverse()
    #l.reverse()
    for i in range(len(h)):
        if i == 0:
            open_record.append(0)
            close_record.append(0)
            porfit_record.append(0)
        #多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == 0:
            open_record.append(h[i-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #空头平仓和多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == -4:
            open_record.append(h[i-1])
            close_record.append(h[i-1])
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        #多头持仓    
        elif s_flag[i] == 4 and s_flag[i-1] == 4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #多头平仓    
        elif s_flag[i] == 0 and s_flag[i-1] == 4:
            open_record.append(0)
            close_record.append(l[i-1])   
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 0:
            open_record.append(l[i-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #多头平仓和空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 4:
            open_record.append(l[i-1])
            close_record.append(l[i-1])
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头持仓    
        elif s_flag[i] == -4 and s_flag[i-1] == -4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #空头平仓    
        elif s_flag[i] == 0 and s_flag[i-1] == -4:
            open_record.append(0)
            close_record.append(h[i-1]) 
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        else:
            open_record.append(0)
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
    s_flag.reverse()
    open_record.reverse()
    close_record.reverse()
    porfit_record.reverse()
    return open_record, close_record, porfit_record
    
#资金管理
'''
def money_manage(total_money, trade_min_num, t=[], s_flag, stop_price, open_record):
    month_position = []
    position_num = []
    
    t.reverse()
    s_flag.reverse()
    stop_price.reverse()
    open_record.reverse()
    for i in range(len(t)):
        if i == 0:
            month_position.append(0)
            position_num.append(0)
        #多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == 0:
            month_position.append( (abs(open_record[i] - stop_price[i]) / total_money)
            #position_num.append(int((total_money * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)))
        #空头平仓和多头开仓
        elif s_flag[i] == 4 and s_flag[i-1] == -4:
            open_record.append(h[i-1])
            close_record.append(h[i-1])
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        #多头持仓    
        elif s_flag[i] == 4 and s_flag[i-1] == 4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #多头平仓    
        elif s_flag[i] == 0 and s_flag[i-1] == 4:
            open_record.append(0)
            close_record.append(l[i-1])   
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 0:
            temp = abs(open_record[i] - stop_price[i]) / total_money
            month_position.append(temp + month_position[-1])
            position_num.append(int((total_money * 0.02) / (abs(open_record[i] - stop_price[i]) * trade_min_num)))
        #多头平仓和空头开仓
        elif s_flag[i] == -4 and s_flag[i-1] == 4:
            open_record.append(l[i-1])
            close_record.append(l[i-1])
            porfit_record.append(close_record[i]-open_record[i-1]+porfit_record[-1])
        #空头持仓    
        elif s_flag[i] == -4 and s_flag[i-1] == -4:
            open_record.append(open_record[-1])
            close_record.append(0)
            porfit_record.append(porfit_record[-1])
        #空头平仓    
        elif s_flag[i] == 0 and s_flag[i-1] == -4:
            open_record.append(0)
            close_record.append(h[i-1]) 
            porfit_record.append(open_record[i-1]-close_record[i]+porfit_record[-1])
        else:
            open_record.append(0)
            close_record.append(0)
            porfit_record.append(porfit_record[-1])   
    
    return position_num
'''  

#收益率的计算
def rate_calculate():
    pass    
        
    
def main():
    pass
    
c_list, v_list, d_list, refc_list, h_list, l_list= read_file('300_test.txt')
#print c_list
print len(c_list)

#ema13 = ema(13, c_list, 3022.70)
#print ema13
#print len(ema13)

#macd12269 = macd(12, 26, 9, c_list, 3018.26, 3118.57, -132.84)
#print macd12269

#print d_list
week_t_list, week_c_list = data_to_weekly(d_list, c_list)
#print 'week_t_list', week_t_list
#print '*-' * 10
#print week_c_list
weekly_macd12_list = macd(12, 26, 9, week_c_list, 4562.03, 4049.35, 450.14)

d_wmacd_list = data_daily_wmacd(d_list, c_list)
print d_wmacd_list

fi2 = findex(2, v_list, c_list, refc_list, 51880529920.0)
#print '*-' * 10
#print fi2

first_w_list = first_screen(d_wmacd_list, d_list, c_list)
print first_w_list

second_d_list = second_screen(first_w_list, fi2)
print second_d_list

t_d_list = thrid_screen(second_d_list, c_list, h_list, l_list)
#print t_d_list
#print '*-+' * 10
print len(t_d_list), len(d_list)

s_flag, s_price = stop_loss(t_d_list, c_list, h_list, l_list)
#print s_flag
#print s_price
print '/*-' * 10
print len(s_flag), len(s_price)

open_record1, close_record1, porfit_record1 = trade_record(s_flag, h_list, l_list)
print '-**-' * 10
print len(open_record1), len(close_record1), len(porfit_record1)

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

df_300.to_csv('df_300.csv', index=False)


