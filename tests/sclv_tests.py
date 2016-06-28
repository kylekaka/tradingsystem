# -*- coding: utf-8 -*-
#三重滤网交易系统
from nose.tools import *
import sclw

def setup():
	print "SETUP!"
	
def teardown():
	print "TEAR DOWN!"

def test_data_to_weekly():
    test_t=[]
    test_p=[]
    result_t, result_p = sclw.data_to_weekly(test_t, test_p)
    assert_equal(result_t, test_t)
    print "testing"	
    
def test_trade_record():
    test_t=[]
    test_p=[]
    result_t, result_p = sclw.trade_record(test_t, test_p)
    assert_equal(result_t, test_t)
    