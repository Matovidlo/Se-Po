##################
### curr_dt.py ###
##################

import time
import datetime


def cur_date():
    o_dat = (time.strftime("%d-%m-%Y"))
    return o_dat


def cur_time():
    tim = datetime.datetime.now()
    return tim
