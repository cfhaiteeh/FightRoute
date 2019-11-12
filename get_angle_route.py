from math import sqrt, acos, pi
from model.model import Model
from data_processing import csv_processing
from sympy import *
from sympy.abc import x, y, z
from scipy.optimize import fsolve
import math


csv_data = csv_processing.get_data('data/data2.csv')



class Vector(object):
    def __init__(self, coordinates):
        super(Vector, self).__init__()
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    # 叉乘
    def crossProduct(self, w):
        new_cordinates = []
        new_cordinates.append(self.coordinates[1] * w.coordinates[2] - w.coordinates[1] * self.coordinates[2])
        new_cordinates.append(-(self.coordinates[0] * w.coordinates[2] - w.coordinates[0] * self.coordinates[2]))
        new_cordinates.append(self.coordinates[0] * w.coordinates[1] - w.coordinates[0] * self.coordinates[1])
        return Vector(new_cordinates)

# data1##############################################################
# ans_min= 103512, curve length = 103652
# [0, 503, 200, 80, 237, 170, 278, 369, 214, 397, 612]
# ans_min= 103603, curve length = 103733
# [0, 503, 200, 80, 237, 170, 278, 369, 214, 67, 612]
# ans_min= 103611, curve length = 103765
# [0, 503, 200, 80, 237, 170, 278, 369, 214, 397, 18, 612]
# ans_min= 103613, curve length = 103762
# [0, 503, 200, 80, 237, 170, 278, 369, 214, 67, 397, 612]
# ans_min= 103614, curve length = 103763
# [0, 503, 200, 80, 237, 170, 278, 369, 214, 397, 302, 612]

# data2############################################################
# ans_min= 109336, curve length = 109533.611637498
# [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 61, 292, 326]
# ans_min= 109813, curve length = 110093.870199261
# [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 61, 292, 135, 326]
# ans_min= 114059, curve length = 114357.829792971
# [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 38, 110, 99, 326]
# ans_min= 114395, curve length = 114800.401777845
# [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 38, 287, 99, 326]
# ans_min= 114672, curve length = 115114.138909153
# [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 38, 287, 61, 326]


# 第一组数据，使用data1
# 第二组数据，使用data2
# array = [0, 503, 200, 80, 237, 170, 278, 369, 214, 397, 612]
# array = [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 61, 292, 326]
# array = [0, 503, 69, 506, 371, 183, 194, 450, 113, 485, 248, 612]
array = [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 61, 292, 326]

count = 0
start = array[0]
length = []
# 切线
qdX = []
qdY = []
qdZ = []
qdX.append(0)
qdY.append(50000)
qdZ.append(5000)
# 圆心
yX = []
yY = []
yZ = []
# 法向量
fX = []
fY = []
fZ = []
# 校验点
xx = []
yy = []
zz = []
xx.append(csv_data[start][1])
yy.append(csv_data[start][2])
zz.append(csv_data[start][3])
for i in range(1, len(array)):
    # 设置入射和出射方向向量 (a, b, c)
    if i == 1:
        outdirVector = Vector([csv_data[array[i]][1] - csv_data[start][1], csv_data[array[i]][2] - csv_data[start][2], csv_data[array[i]][3] - csv_data[start][3]])
        length.append(((csv_data[array[i]][1] - csv_data[start][1]) ** 2 +
                       (csv_data[array[i]][2] - csv_data[start][2]) ** 2 +
                       (csv_data[array[i]][3] - csv_data[start][3]) ** 2) ** 0.5)
        start = array[i]
        xx.append(int(csv_data[array[i]][1]))
        yy.append(int(csv_data[array[i]][2]))
        zz.append(int(csv_data[array[i]][3]))
        # qiedianX = csv_data[start][1]
        # qiedianY = csv_data[start][2]
        # qiedianZ = csv_data[start][3]
        continue
    else:
        indirVector = outdirVector
        xx.append(int(csv_data[array[i]][1]))
        yy.append(int(csv_data[array[i]][2]))
        zz.append(int(csv_data[array[i]][3]))


    # 起始点 (x0, y0, z0)
    begin = Vector([csv_data[start][1], csv_data[start][2], csv_data[start][3]])

    # 目标点 (x1, y1, z1)
    end = Vector([csv_data[array[i]][1], csv_data[array[i]][2], csv_data[array[i]][3]])

    # 垂直向量 (m, n, k)
    # temp 为两点之间的方向向量
    temp = Vector([csv_data[array[i]][1] - csv_data[start][1], csv_data[array[i]][2] - csv_data[start][2], csv_data[array[i]][3] - csv_data[start][3]])
    t = indirVector.crossProduct(temp)
    fX.append(int(t.coordinates[0]/10000))
    fY.append(int(t.coordinates[1]/10000))
    fZ.append(int(t.coordinates[2]/10000))

    #print('t: ', t.coordinates[0])

    A = indirVector.coordinates[0] * begin.coordinates[0] + indirVector.coordinates[1] * begin.coordinates[1] + indirVector.coordinates[2] * begin.coordinates[2]
    B = end.coordinates[0] * t.coordinates[0] + end.coordinates[1] * t.coordinates[1] + end.coordinates[2] * t.coordinates[2]
    aa = solve([indirVector.coordinates[0] * x + indirVector.coordinates[1] * y + indirVector.coordinates[2] * z - A,
                t.coordinates[0] * x + t.coordinates[1] * y + t.coordinates[2] * z - B,
                (x - begin.coordinates[0])**2 + (y - begin.coordinates[1])**2 + (z - begin.coordinates[2])**2 - 40000], [x, y, z])

    # 圆心坐标 从第二个点开始的
    yuanX1 = aa[0][0]
    yuanY1 = aa[0][1]
    yuanZ1 = aa[0][2]

    yuanX2 = aa[1][0]
    yuanY2 = aa[1][1]
    yuanZ2 = aa[1][2]

    dis1 = ((end.coordinates[0] - yuanX1)**2 + (end.coordinates[1] - yuanY1)**2 + (end.coordinates[2] - yuanZ1)**2)**0.5
    dis2 = ((end.coordinates[0] - yuanX2)**2 + (end.coordinates[1] - yuanY2)**2 + (end.coordinates[2] - yuanZ2)**2)**0.5
    if dis1 < dis2:
        yuanX = yuanX1
        yuanY = yuanY1
        yuanZ = yuanZ1
    else:
        yuanX = yuanX2
        yuanY = yuanY2
        yuanZ = yuanZ2
    yX.append(int(yuanX))
    yY.append(int(yuanY))
    yZ.append(int(yuanZ))
    # print(aa)

    print('x: ', yuanX, 'y: ', yuanY, 'z: ', yuanZ)



    # 求切点 从第二个点开始
    bb = solve([(x - yuanX)**2 + (y - yuanY)**2 + (z - yuanZ)**2 - 40000,
                (x - yuanX) * t.coordinates[0] + (y - yuanY) * t.coordinates[1] + (z - yuanZ) * t.coordinates[2],
                (x - yuanX) * (x - end.coordinates[0]) + (y - yuanY) * (y - end.coordinates[1]) + (z - yuanZ) * (z - end.coordinates[2])],
               [x, y, z])

    #print(bb)
    #break

    # 选点
    qiedianX1 = bb[0][0]
    qiedianY1 = bb[0][1]
    qiedianZ1 = bb[0][2]

    qiedianX2 = bb[1][0]
    qiedianY2 = bb[1][1]
    qiedianZ2 = bb[1][2]

    # 按切点与目标点连线与方向向量的夹角选择切点
    # 如果是第一次，切点即入射点
    if i == 1:
        qiedianX = begin.coordinates[0]
        qiedianY = begin.coordinates[1]
        qiedianZ = begin.coordinates[2]
    else:
        # 先求夹角
        try:
            qiedianEnd1 = math.acos(((end.coordinates[0] - qiedianX1) * indirVector.coordinates[0] + (end.coordinates[1] - qiedianY1) * indirVector.coordinates[1] + (end.coordinates[2] - qiedianZ1) * indirVector.coordinates[2])
                                / ((end.coordinates[0] - qiedianX1)**2 + (end.coordinates[1] - qiedianY1)**2 + (end.coordinates[2] - qiedianZ1))**0.5
                                / (indirVector.coordinates[0]**2 + indirVector.coordinates[1]**2 + indirVector.coordinates[2]**2)**0.5)
        except:
            qiedianEnd1 = 1
            pass
        try:
            qiedianEnd2 = math.acos(((end.coordinates[0] - qiedianX2) * indirVector.coordinates[0] + (end.coordinates[1] - qiedianY2) * indirVector.coordinates[1] + (end.coordinates[2] - qiedianZ2) * indirVector.coordinates[2])
                                / ((end.coordinates[0] - qiedianX2)**2 + (end.coordinates[1] - qiedianY2)**2 + (end.coordinates[2] - qiedianZ2))**0.5
                                / (indirVector.coordinates[0]**2 + indirVector.coordinates[1]**2 + indirVector.coordinates[2]**2)**0.5)
        except:
            qiedianEnd2 = 1
            pass

        if qiedianEnd1 > qiedianEnd2:
            qiedianX = qiedianX1
            qiedianY = qiedianY1
            qiedianZ = qiedianZ1
            qdX.append(int(qiedianX))
            qdY.append(int(qiedianY))
            qdZ.append(int(qiedianZ))
        else:
            qiedianX = qiedianX2
            qiedianY = qiedianY2
            qiedianZ = qiedianZ2
            qdX.append(int(qiedianX))
            qdY.append(int(qiedianY))
            qdZ.append(int(qiedianZ))

    print('qx: ', qiedianX, 'qy: ', qiedianY, 'qz: ', qiedianZ)
    #break

    outdirVector = Vector([csv_data[array[i]][1] - qiedianX, csv_data[array[i]][2] - qiedianY, csv_data[array[i]][3] - qiedianZ])

    # calculate the huchang
    if i == 1:
        length.append(((end.coordinates[0] - begin.coordinates[0]) ** 2 +
                       (end.coordinates[1] - begin.coordinates[1]) ** 2 +
                       (end.coordinates[2] - begin.coordinates[2]) ** 2) ** 0.5)
    else:
        jiajiao = math.acos((outdirVector.coordinates[0] * indirVector.coordinates[0] +
                             outdirVector.coordinates[1] * indirVector.coordinates[1] +
                             outdirVector.coordinates[2] * indirVector.coordinates[2]) /
                            ((outdirVector.coordinates[0] ** 2 + outdirVector.coordinates[1] ** 2 +
                              outdirVector.coordinates[2] ** 2) ** 0.5) /
                            (indirVector.coordinates[0] ** 2 + indirVector.coordinates[1] ** 2 +
                             indirVector.coordinates[2] ** 2) ** 0.5)
        # print(jiajiao)
        huchang = 200 * jiajiao
        print(huchang)
        yuanxinju = (40000 + ((end.coordinates[0] - yuanX) ** 2 + (end.coordinates[1] - yuanY) ** 2 + (
                    end.coordinates[2] - yuanZ) ** 2)) ** 0.5
        # print('a: ', end.coordinates[0], 'b: ', end.coordinates[1], 'c: ', end.coordinates[2])
        print(yuanxinju)
        length.append(huchang + yuanxinju)

    count += 1
    # print(count)
    print(length[count - 1])
    start = array[i]

print('qx =', qdX)
print('qy =', qdY)
print('qz =', qdZ)

print('yuanxinX =', yX)
print('yuanxinY =', yY)
print('yuanxinZ =', yZ)

print('fx =', fX)
print('fy =', fY)
print('fz =', fZ)

print('x =', xx)
print('y =', yy)
print('z =', zz)

sum = 0
for i in range(len(length)):
    sum += length[i]

print('length =', length)
print('the length is: ', sum)

