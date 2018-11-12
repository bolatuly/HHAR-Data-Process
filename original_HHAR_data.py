import os
import sys
import numpy as np
from copy import deepcopy
from time import gmtime, strftime

from scipy.interpolate import interp1d
from scipy.fftpack import fft

timeLabel = 'Creation_Time'
pairSaveDir = '/Users/azamatbolat/PycharmProjects/HHAR-Data-Process/data-own-collected/paired'

#mode = 'one_user_out'
#select = 'a'

#curTime = gmtime()
#curRunDir = strftime("%a-%d-%b-%Y-%H_%M_%S+0000", curTime)

# fileIn = open(os.path.join(pairSaveDir, '#DeivceBadData.csv'))
badDevice = ['lgwatch_1', 'lgwatch_2', 's3mini_2']
# for line in fileIn.readlines():
# 	if line[-1] == '\n':
# 		badDevice.append(line[:-1])
# 	else:
# 		badDevice.append(line)

dataList = os.listdir(pairSaveDir)
nameDevList = []
for dataFile in dataList:
    if dataFile[0] == '.':
        continue
    if dataFile[0] == '#':
        continue
    elems = dataFile.split('-')
    curLable = '-'.join(elems[:-1])
    if curLable not in nameDevList:
        nameDevList.append(curLable)
# print nameDevList

sepcturalSamples = 10
fftSpan = 3.
SampSpan = 20.
timeNoiseVar = 0.2
accNoiseVar = 0.5
gyroNoiseVar = 0.2
augNum = 10

dataDict = {}
gtType = ["type", "sit", "stand", "walk"]
idxList = range(len(gtType))
gtIdxDict = dict(zip(gtType, idxList))
idxGtDict = dict(zip(idxList, gtType))
wide = 20
wideScaleFactor = 4
labEvery = False
for nameDev in nameDevList:
    for curGt in gtType:
        curType = gtIdxDict[curGt]
        curData_Sep = []
        if os.path.exists(os.path.join(pairSaveDir, nameDev + '-' + curGt)):
            fileIn = open(os.path.join(pairSaveDir, nameDev + '-' + curGt))
            line = fileIn.readline()
            curData = []
            curAccList = []
            curGyroList = []
            curTimeList = []
            lastTime = -1
            startTime = -1
            count = 0
            print nameDev + '-' + curGt
            while len(line) > 0:
                curElem = eval(line)
                curTime = curElem['Time']
                if startTime < 0:
                    startTime = curTime
                    if startTime < 0:
                        print 'Wrong!'
                        test = raw_input('continue')
                if abs(curTime - startTime) > fftSpan:
                    if len(curAccList) > 0:
                        if curTimeList[-1] < fftSpan:
                            curAccList.append(deepcopy(curAccList[-1]))
                            curGyroList.append(deepcopy(curGyroList[-1]))
                            curTimeList.append(fftSpan)
                        curAccListOrg = np.array(curAccList).T
                        curGyroListOrg = np.array(curGyroList).T
                        curTimeListOrg = np.array(curTimeList)


                        curAugNum = augNum

                        for augIdx in xrange(curAugNum):
                            # augIdx = 0
                            if augIdx == 0:
                                curAccList = curAccListOrg + 0.
                                curGyroList = curGyroListOrg + 0.
                                curTimeList = curTimeListOrg + 0.
                            else:
                                curAccList = curAccListOrg + np.random.normal(0., accNoiseVar, curAccListOrg.shape)
                                curGyroList = curGyroListOrg + np.random.normal(0., gyroNoiseVar, curGyroListOrg.shape)
                                curTimeList = curTimeListOrg + np.random.normal(0., timeNoiseVar, curTimeListOrg.shape)

                            curTimeList = np.sort(curTimeList)
                            if curTimeList[-1] < fftSpan:
                                curTimeList[-1] = fftSpan
                            if curTimeList[0] > 0.:
                                curTimeList[0] = 0.

                            accInterp = interp1d(curTimeList, curAccList)
                            accInterpTime = np.linspace(0.0, fftSpan * 1, sepcturalSamples * 1)
                            accInterpVal = accInterp(accInterpTime)
                            accFFT = fft(accInterpVal).T
                            accFFTSamp = accFFT[::1] / float(1)
                            accFFTFin = []
                            for accFFTElem in accFFTSamp:
                                for axisElem in accFFTElem:
                                    accFFTFin.append(axisElem.real)
                                    accFFTFin.append(axisElem.imag)

                            gyroInterp = interp1d(curTimeList, curGyroList)
                            gyroInterpTime = np.linspace(0.0, fftSpan * 1, sepcturalSamples * 1)
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

                            if augIdx == 0:
                                print

                            if len(curData) < augNum:
                                curData.append([deepcopy(curSenData)])
                            elif startTime - lastTime >= SampSpan: #and augIdx == 0:
                                for curAugData in curData:
                                    curData_Sep.append(deepcopy(curAugData))
                                curData = []
                                curData.append([deepcopy(curSenData)])
                            else:
                                curData[augIdx].append(deepcopy(curSenData))

                        lastTime = startTime + curTimeList[-1]
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
        print 'curData_Sep', np.array(curData_Sep).shape
        if not dataDict.has_key(nameDev):
            dataDict[nameDev] = [[], []]

        for sepData in curData_Sep:
            staIdx = 0
            while staIdx < len(sepData):
                endIdx = min(staIdx + wide, len(sepData))
                if endIdx - staIdx < 5:
                    # if endIdx - staIdx < wide:
                    break
                dataDict[nameDev][0].append(deepcopy(sepData[staIdx:endIdx]))
                curOut = [0.] * len(gtType)
                curOut[curType] = 1.
                if labEvery:
                    curOutPrep = []
                    for outIdx in xrange(endIdx - staIdx):
                        curOutPrep.append(deepcopy(curOut))
                    dataDict[nameDev][1].append(deepcopy(curOutPrep))
                else:
                    dataDict[nameDev][1].append(deepcopy(curOut))
                staIdx += int(wide / wideScaleFactor)

X = []
Y = []
maskX = []
evalX = []
paddingVal = 0.
inputFeature = sepcturalSamples * 6 * 2

count = 0
for nameDev in dataDict.keys():
    curX, curY = dataDict[nameDev]
    count += 1
    print '\r', count,
    sys.stdout.flush()

    X += deepcopy(curX)
    Y += deepcopy(curY)

for idx in xrange(len(X)):
    curLen = len(X[idx])
    maskX.append([[1.0]] * curLen)
    for addIdx in xrange(wide - curLen):
        X[idx].append([paddingVal] * inputFeature)
        maskX[idx].append([0.0])

X = np.array(X)
Y = np.array(Y)
maskX = np.array(maskX)

evalX = np.array(evalX)
print 'X', X.shape, X.dtype, 'Y', Y.shape, Y.dtype, 'maskX', maskX.shape, maskX.dtype

X = np.reshape(X, [-1, wide * inputFeature])
XY = np.hstack((X, Y))
print 'XY', XY.shape
evalX = np.reshape(evalX, [-1, wide * inputFeature])
out_dir = 'sepHARData_'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    os.mkdir(os.path.join(out_dir, 'train'))
idx = 0
for elem in XY:
    fileOut = open(os.path.join(out_dir, 'train', 'data_' + str(idx) + '.csv'), 'w')
    curOut = elem.tolist()
    curOut = [str(ele) for ele in curOut]
    curOut = ','.join(curOut) + '\n'
    fileOut.write(curOut)
    fileOut.close()
    idx += 1
idx = 0