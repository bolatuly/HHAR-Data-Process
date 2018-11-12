import os
from copy import deepcopy
import numpy as np
from scipy.interpolate import interp1d
from scipy.fftpack import fft

pairSaveDir = '/Users/azamatbolat/Desktop/real-case-data/paired/'
nameDev = 'gear_s2'
gtType = ["receive_lecture", "give_lecture", "working"]
fftSpan = 60.
wide = 20
sepcturalSamples = 10
dataDict = {}
idxList = range(len(gtType))
gtIdxDict = dict(zip(gtType, idxList))

if __name__ == "__main__":

    for user in range(18):
        for curGt in gtType:
            curType = gtIdxDict[curGt]
            wholeAction = []
            if os.path.exists(os.path.join(pairSaveDir, str(user) + '-' + nameDev + '-' + curGt)):
                curData_Sep = []
                fileIn = open(os.path.join(pairSaveDir, str(user) + '-' + nameDev + '-' + curGt))
                line = fileIn.readline()
                curData = []
                curAccList = []
                curGyroList = []
                curTimeList = []
                lastTime = -1
                startTime = -1
                count = 0
                realTime = -1
                while len(line) > 0:
                    curElem = eval(line)
                    curTime = curElem['Time']
                    if startTime < 0:
                        startTime = curTime
                        if count == 0:
                            realTime = curTime
                        if startTime < 0:
                            print 'Wrong!'
                            test = raw_input('continue')
                    if abs(curTime - startTime) > fftSpan:
                        if len(curData_Sep):
                            wholeAction.append(deepcopy(curData_Sep))
                        curData_Sep = []
                        if len(curAccList) > 0:
                            if curTimeList[-1] < fftSpan:
                                curAccList.append(deepcopy(curAccList[-1]))
                                curGyroList.append(deepcopy(curGyroList[-1]))
                                curTimeList.append(fftSpan)
                            curAccListOrg = np.array(curAccList).T
                            curGyroListOrg = np.array(curGyroList).T
                            curTimeListOrg = np.array(curTimeList)

                            curAccList = curAccListOrg + 0.
                            curGyroList = curGyroListOrg + 0.
                            curTimeList = curTimeListOrg + 0.

                            curTimeList = np.sort(curTimeList)
                            if curTimeList[-1] < fftSpan:
                                curTimeList[-1] = fftSpan
                            if curTimeList[0] > 0.:
                                curTimeList[0] = 0.

                            divTime = 0.0
                            step = 0.15
                            idto = 0
                            counter = 0
                            for id in xrange(wide * wide):

                                counter = 0
                                for time in curTimeList:
                                    if divTime <= time <= step:
                                        counter = counter + 1

                                wideTimeList = curTimeList[idto:idto + counter]
                                wideAccList = curAccList[:, idto:idto + counter]
                                wideGyroList = curGyroList[:, idto:idto + counter]

                                if len(wideTimeList) < 2:
                                    print "Bad device: " + fileIn.name
                                    curData = []
                                    break

                                if wideTimeList[-1] < step:
                                    wideTimeList[-1] = step
                                if wideTimeList[0] > divTime:
                                    wideTimeList[0] = 0.

                                accInterp = interp1d(wideTimeList, wideAccList)

                                accInterpTime = np.linspace(divTime, step * 1, sepcturalSamples * 1)
                                accInterpVal = accInterp(accInterpTime)

                                accFFT = fft(accInterpVal).T
                                accFFTSamp = accFFT[::1] / float(1)
                                accFFTFin = []
                                for accFFTElem in accFFTSamp:
                                    for axisElem in accFFTElem:
                                        accFFTFin.append(axisElem.real)
                                        accFFTFin.append(axisElem.imag)

                                gyroInterp = interp1d(wideTimeList, wideGyroList)
                                gyroInterpTime = np.linspace(divTime, step * 1, sepcturalSamples * 1)
                                gyroInterpVal = gyroInterp(gyroInterpTime)
                                gyroFFT = fft(gyroInterpVal).T
                                gyroFFTSamp = gyroFFT[::1] / float(1)
                                # print 'gyroFFTSamp', gyroFFTSamp.shape
                                gyroFFTFin = []
                                for gyroFFTElem in gyroFFTSamp:
                                    for axisElem in gyroFFTElem:
                                        gyroFFTFin.append(axisElem.real)
                                        gyroFFTFin.append(axisElem.imag)

                                curSenData = []
                                curSenData += accFFTFin
                                curSenData += gyroFFTFin

                                curData.append(deepcopy(curSenData))

                                idto = idto + counter
                                divTime = step
                                step = step + 0.15

                                if (id + 1) % 20 == 0:
                                    curData_Sep.append(deepcopy(curData))
                                    curData = []

                            startTime = -1
                            curAccList = []
                            curGyroList = []
                            curTimeList = []
                    if startTime < 0:
                        startTime = curTime
                        if startTime < 0:
                            print 'Wrong!'
                            test = raw_input('continue')
                    if curTime - startTime not in curTimeList:
                        curAccList.append(deepcopy(curElem['Accelerometer']))
                        curGyroList.append(deepcopy(curElem['Gyroscope']))
                        curTimeList.append(curTime - startTime)

                    count += 1
                    line = fileIn.readline()
                print("done")

            dataDict[str(user) + '-' + nameDev + '-' + curGt] = []
            for curData_Sep in wholeAction:
                i = 0
                dataDict[str(user) + '-' + nameDev + '-' + curGt][i] = [[], []]
                for sepData in curData_Sep:
                    dataDict[str(user) + '-' + nameDev + '-' + curGt][i][0].append(deepcopy(sepData))
                    curOut = [0.] * len(gtType)
                    curOut[curType] = 1.
                    dataDict[str(user) + '-' + nameDev + '-' + curGt][i][1].append(deepcopy(curOut))
                    i = i+1

    print("done")