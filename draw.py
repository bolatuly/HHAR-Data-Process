import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

from scipy import signal

def butter_lowpass_filter(data, cut, fs, order, zero_phase=False):
    from scipy.signal import butter, lfilter, filtfilt

    nyq = 0.5 * fs
    cut = cut / nyq

    b, a = butter(order, cut, btype='low')
    y = (filtfilt if zero_phase else lfilter)(b, a, data)
    return y

if __name__ == "__main__":

    data = {}
    for files in ['17-gear_s2-receive_lecture']:
        currAcc = []
        currGyr = []
        fileIn = open(os.path.join("/Users/azamatbolat/Desktop/real-case-data/paired/", files))
        line = fileIn.readline()
        while len(line) > 0:
            curElem = eval(line)
            currAcc.append(deepcopy(curElem['Accelerometer']))
            currGyr.append(deepcopy(curElem['Gyroscope']))
            line = fileIn.readline()
        temp = {"acc": currAcc, "gyr": currGyr}
        data[files] = temp

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0, 0].get_yaxis().set_label_coords(-0.20, 0.5)
    test = np.array(data['17-gear_s2-receive_lecture']["gyr"])
    axes[0, 0].set_title('Listening')
    axes[0, 0].plot(test)

    medium = signal.medfilt(test)
    axes[0, 1].plot(medium)
    axes[0, 1].set_ylim(-500, 400)

    low = butter_lowpass_filter(test[0], 2, 50, 4, zero_phase=True)

    axes[1, 0].plot(low)
    axes[1, 0].set_ylim(-500, 400)

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