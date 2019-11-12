# -*- coding: utf-8 -*-
import csv

def get_data(file_name):
    point_data=[]
    with open(file_name) as csv_file:
        sum0=0
        sum0_0=0
        sum1=0
        sum1_1=0
        csv_reader=csv.reader(csv_file)
        point_header=next(csv_reader)
        for row in csv_reader:

            point_data.append(row)
            row[0]=int(row[0])
            row[1]=float(row[1])
            row[2]=float(row[2])
            row[3]=float(row[3])
            row[4]=int(row[4])
            row[5]=int(row[5])
            if row[4]==1:
                sum1_1+=1
            if row[4]==0:
                sum0_0+=1
            if row[4]==1 and row[5]==1:
                sum1+=1
            if row[4]==0 and row[5]==1:
                sum0+=1
            # print(row)
        print(sum1,sum0)
        print(sum1_1-36,sum0_0-46)
    return point_data
if __name__=='__main__':
    get_data('../data/data2.csv')