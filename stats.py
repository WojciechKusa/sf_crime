import csv
import time
import numpy as np
import matplotlib.pyplot as plt
import pyradbas as pyrb

NUMBER_OF_CRIMES = 10000
INCLUDED_CRIMES = ['LARCENY/THEFT', 'VANDALISM', 'ROBBERY', 'VEHICLE THEFT', 'ASSAULT', 'DRUNKENNESS']

def importDataFromFile(filename, usedColumns, targetColumn):

    data = []
    target = []
    no = 0

    with open(filename, "r") as csvfile:

        for line in csv.reader(csvfile, skipinitialspace=True):

            if line[targetColumn] not in INCLUDED_CRIMES:
                continue

            columns = list(line[i] for i in usedColumns)
            columns[0] = int(columns[0].split(' ')[1].split(':')[0])
            columns[1] = float(columns[1])
            columns[2] = float(columns[2])

            data.append(columns)
            target.append(INCLUDED_CRIMES.index(line[1]))

            no += 1

            if no >= NUMBER_OF_CRIMES:
                break

    return [data, target]


def countCrimesPerHour(crimes):

    crimesPerHour = dict()

    for line in crimes:
        hour = int(line[0].split(' ')[1].split(':')[0])
        crime = line[1]

        if crime in crimesPerHour:
            crimesPerHour[crime][hour] += 1
        else:
            crimesPerHour[crime] = [0] * 24
            crimesPerHour[crime][hour] = 1

    return crimesPerHour


def plotCrimesPerHour(crimes):

    for key, value in crimes.items():
        plt.plot(value, label = key)

    plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
    plt.show()


def plotCityMap(crimes):
    return None

if __name__ == "__main__":

    start = time.time()

    [data, target] = importDataFromFile("train.csv", [ 0, 7, 8 ], 1)
    [data, target] = [np.array(data).reshape(len(data), 3), np.array(target).reshape(len(target), 1)]

    net = pyrb.train_ols(data, target, 10e-8, 0.8, verbose=True)
    S = net.sim(data)

    errors = 0
    count = 0

    for i in range(len(target)):
        count += 1

        if int(round(S[i][0])) != target[i]:
            errors += 1

    end = time.time()

    print('Learning error: ' + str(round((errors / count) * 100)) + '%')
    print('Time: ' + str(end - start) + ' seconds')