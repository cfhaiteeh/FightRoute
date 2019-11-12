from model.model import Model
from data_processing import csv_processing

def verify(args,csv_data,dist_data,ans):




    array = ans

    ALPHA1 = args.alpha1
    ALPHA2 = args.alpha2
    BETA1 = args.beta1
    BETA2 = args.beta2
    thet = args.thet
    delta = args.delta

    start = array[0]
    sumCZ = 0
    sumSP = 0
    boolean = True
    for i in range(1, len(array)):
        sumCZ +=int( dist_data[start][array[i]] * delta)
        sumSP += int(dist_data[start][array[i]] * delta)
        print('chuizhi: ', sumCZ)
        print('shuiping: ', sumSP)
        print('dist=',dist_data[start][array[i]])
        print('type: ', csv_data[array[i]][4])
        print('now=',array[i])

        if csv_data[array[i]][4] == 1:
            if sumCZ > ALPHA1 or sumSP > ALPHA2:
                boolean = False
                break
            else:
                sumCZ = 0
                if args.prob and  csv_data[array[i]][5]==1:
                    sumCZ=5
        elif csv_data[array[i]][4] == 0:
            if sumCZ > BETA1 or sumSP > BETA2:
                boolean = False
                break
            else:
                sumSP = 0
                if args.prob and  csv_data[array[i]][5]==1:
                    sumSP=5
        elif csv_data[array[i]][4] == 4:
            if sumCZ > thet or sumSP > thet:
                boolean = False
                break
        start = array[i]

    print(boolean)
    if boolean^1:
        print('the false point: ', array[i])