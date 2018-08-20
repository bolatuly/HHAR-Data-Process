import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

if __name__ == "__main__":

    data = {}
    for files in ['listen_4_404_sample', 'speak_4_404_sample', 'type_4_422_sample', 'write_4_422_sample']:
        currAcc = []
        currGyr = []
        fileIn = open(os.path.join("C:\projects\data(09.08.2018)\\app_sensor", files))
        line = fileIn.readline()
        while len(line) > 0:
            line = line + "}"
            curElem = eval(line)
            currAcc.append(deepcopy(curElem['Accelerometer']))
            currGyr.append(deepcopy(curElem['Gyroscope']))
            line = fileIn.readline()
        temp = {"acc": currAcc, "gyr": currGyr}
        data[files] = temp

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0, 0].get_yaxis().set_label_coords(-0.20, 0.5)
    test = np.array(data['listen_4_404_sample']["gyr"])
    axes[0, 0].set_title('Listening')
    axes[0, 0].plot(test[:100000])

    axes[0, 1].set_title('Speaking')
    axes[0, 1].plot(np.array(data['speak_4_404_sample']["gyr"])[:100000])

    axes[1, 0].set_title('Typing')
    axes[1, 0].plot(np.array(data['type_4_422_sample']["gyr"])[:100000])
    axes[1, 0].get_yaxis().set_label_coords(-0.20, 0.5)

    axes[1, 1].set_title('Writing')
    axes[1, 1].plot(np.array(data['write_4_422_sample']["gyr"])[:100000])

    axes[0, 0].set_xlabel('Samples (n)')
    axes[0, 0].set_ylabel('Rate of rotation (rad/s)')
    axes[0, 1].set_xlabel('Samples (n)')
    axes[0, 1].set_ylabel('Rate of rotation (rad/s)')
    axes[1, 0].set_xlabel('Samples (n)')
    axes[1, 0].set_ylabel('Rate of rotation (rad/s)')
    axes[1, 1].set_xlabel('Samples (n)')
    axes[1, 1].set_ylabel('Rate of rotation (rad/s)')

    axes[0, 0].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    axes[0, 1].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    axes[1, 0].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    axes[1, 1].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    fig.tight_layout()
    plt.show()