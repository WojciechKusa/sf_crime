import csv
import time
import numpy as np
import matplotlib.pyplot as plt


def importDataFromFile(filename, usedColumns):

    crimes = dict()

    with open(filename, "r") as csvfile:

        for line in csv.reader(csvfile, skipinitialspace=True):
            columns = list(line[i] for i in usedColumns)
            hour = int(line[0].split(' ')[1].split(':')[0])
            crime = columns[1]
            
            if crime in crimes:
                crimes[crime][hour] += 1
            else:
                crimes[crime] = [0] * 24
                crimes[crime][hour] = 1

    return crimes


def plotCrimesPerHour(crimes):

    for key, value in crimes.items():
        plt.plot(value, label = key)

    plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
    plt.show()


def plotCityMap(crimes):
    return None

if __name__ == "__main__":

    crimes = importDataFromFile("train.csv", [ 0, 1, 7, 8 ])
    plotCrimesPerHour(crimes)
    plotCityMap(crimes)
