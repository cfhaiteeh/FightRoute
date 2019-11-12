from model.model import Model
from data_processing import csv_processing

csv_data = csv_processing.get_data('data/data2.csv')


# 第二组数据结果，数据改为data2
# 使用array2
array = [0,
275,
150,
238,
234,
309,
305,
123,
231,
160,
191,
88,
50,
96,
61,
326
]

# 第一组数据结果，数据改为data1
# 使用array2
array22 = [0,
303,
64,
607,
170,
278,
369,
457,
388,
555,
436,
612]



length = [13287.897610734834, 5349.21377749100, 13960.7636756738, 5572.14959759202, 5975.49613040355, 9226.36297676330, 10012.3792019406, 7490.98242490963, 5783.45581049399, 9489.42469771288, 9838.78588118708, 6560.39210604205, 6986.30774655331]

array2 = [0, 163, 114, 8, 309, 305, 123, 45, 160, 92, 93, 61, 292, 326]

# data1
ALPHA1 = 25
ALPHA2 = 15
BETA1 = 20
BETA2 = 25
SITA = 30

# data2
# ALPHA1 = 20
# ALPHA2 = 10
# BETA1 = 15
# BETA2 = 20
# SITA = 20

SIGAMA = 0.001

start = array2[0]
sumCZ = 0
sumSP = 0
sum = 0
boolean = True
for i in range(1, len(array2)):
    # sumCZ += model.dist_data[start][array2[i]] * SIGAMA
    # sumSP += model.dist_data[start][array2[i]] * SIGAMA
    sumCZ += length[i - 1] * SIGAMA
    sumSP += length[i - 1] * SIGAMA
    sum += length[i - 1]
    print('chuizhi: ', sumCZ, 'shuiping: ', sumSP, 'type: ', csv_data[array2[i]][4])
    #print('shuiping: ', sumSP)
    #print('type: ', model.csv_data[array[i]][4])

    if csv_data[array2[i]][4] == 1:
        print('standCZ: ', ALPHA1, '   standSP: ', ALPHA2)
        print('--------------------------------------')
        if int(sumCZ) > ALPHA1 or int(sumSP) > ALPHA2:
            boolean = False
            break
        else:
            sumCZ = 0

    elif csv_data[array2[i]][4] == 0:
        print('standCZ: ', BETA1, '   standSP: ', BETA2)
        print('--------------------------------------')
        if int(sumCZ) > BETA1 or int(sumSP) > BETA2:
            boolean = False
            break
        else:
            sumSP = 0
    elif csv_data[array2[i]][4] == 4:
        print('standCZ: ', SITA, '   standSP: ', SITA)
        print('--------------------------------------')
        if sumCZ > SITA or sumSP > SITA:
            boolean = False
            break
    start = array2[i]

print(boolean)


if boolean:
    print('sum length: ', sum)
else:
    print('the false point: ', array2[i])

