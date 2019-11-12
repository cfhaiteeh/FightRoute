# -*- coding: utf-8 -*-
from model.model import Model
# from model.model1 import Model
from data_processing import csv_processing
import verify as verify
import parse_args
def processing(args):
    csv_data=csv_processing.get_data(args.data_path)
    # print(csv_data)
    model=Model(csv_data,args)    #1

    # model=Angle_model(csv_data,args)
    # model=Prob_Model(csv_data,args)#3
    ans=model.run_raw()
    if args.top5:
        model.run_angle()
    else:
        verify.verify(args,csv_data,model.dist_data,ans)


import numpy as np


import decimal
from time import *
if __name__=='__main__':
    begin_time = time()
    args=parse_args.interpret_args()
    processing(args)
    end_time = time()
    run_time = end_time - begin_time
    print('该程序运行时间：', run_time)
