import os
import sys
import numpy as np
from copy import deepcopy
from time import gmtime, strftime

from scipy.interpolate import interp1d
from scipy.fftpack import fft

pairSaveDir = 'C:\\projects\\data(09.08.2018)\\app_sensor'

sepcturalSamples = 10
# fftSpan = 0.25
# SampSpan = 5.
fftSpan = 5.
SampSpan = 20.

timeNoiseVar = 0.2
accNoiseVar = 0.5
gyroNoiseVar = 0.2
augNum = 10

dataDict = {}
gtType = ["write", "listen", "speak", "type"]
idxList = range(len(gtType))
gtIdxDict = dict(zip(gtType, idxList))
idxGtDict = dict(zip(idxList, gtType))
wide = 20
wideScaleFactor = 4
labEvery = False
nameDev = "galaxys8"
# mode = 'one_user_out'
# select = 'j'
print 'start!'

result = open("file_link_eval.txt", "a")
counting = 0
for users in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        for rooms in [404, 405, 410, 422]:
            for curGt in gtType:
                curType = gtIdxDict[curGt]
                curData_Sep = []
                if os.path.exists(os.path.join(pairSaveDir, curGt+'_'+str(users)+'_'+str(rooms)+'_'+'sample')):
                    fileIn = open(os.path.join(pairSaveDir, curGt+'_'+str(users)+'_'+str(rooms)+'_'+'sample'))
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
                        line = line + "}"
                        curElem = eval(line)
                        curTime = float(curElem['Time'] / 1000000000.0)
                        if startTime < 0:
                            startTime = curTime
                            if count == 0:
                                realTime = curTime
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

                                # curAugNum = 1

                                # if mode == 'one_user_out':
                                # if nameDev[0] == select:
                                # curAugNum = 1
                                # else:
                                # curAugNum = augNum
                                # elif mode == 'one_model_out':
                                # if select in nameDev[1:]:
                                # curAugNum = 1
                                # else:
                                # curAugNum = augNum
                                # else:
                                # curAugNum = augNum

                                curAccList = curAccListOrg + 0.
                                curGyroList = curGyroListOrg + 0.
                                curTimeList = curTimeListOrg + 0.

                                curTimeList = np.sort(curTimeList)
                                if curTimeList[-1] < fftSpan:
                                    curTimeList[-1] = fftSpan
                                if curTimeList[0] > 0.:
                                    curTimeList[0] = 0.

                                divTime = 0.0
                                step = 0.25
                                idto = 0
                                counter = 0
                                for id in xrange(wide):

                                    counter = 0
                                    for time in curTimeList:
                                        if divTime <= time <= step:
                                            counter = counter + 1


                                    wideTimeList = curTimeList[idto:idto + counter]
                                    wideAccList = curAccList[:, idto:idto + counter]
                                    wideGyroList = curGyroList[:, idto:idto + counter]

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


                                # lastTime = startTime + curTimeList[-1]
                                    idto = idto + counter
                                    divTime = step
                                    step = step + 0.25

                                #for curAugData in curData:
                                    #curData_Sep.append([deepcopy(curAugData)])
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
                    print curGt+'_'+str(users)+'_'+str(rooms)+'_'+'sample ' + str(counting) + " :", counting + (np.array(curData_Sep).shape[0] - 1)
                    result.write("{'filename': '"+curGt+'_'+str(users)+'_'+str(rooms)+'_'+"sample'"+",'data':["+str(counting)+", "+str(counting + (np.array(curData_Sep).shape[0] - 1))+"]}\n")
                    counting = counting + (np.array(curData_Sep).shape[0])

                if not dataDict.has_key(nameDev):
                    dataDict[nameDev] = [[], []]

                for sepData in curData_Sep:
                    #staIdx = 0
                    #while staIdx < len(sepData):
                        #endIdx = min(staIdx + wide, len(sepData))
                        #if endIdx - staIdx < 5:
                            #if endIdx - staIdx < wide:
                                #break
                        #else:
                            #print("no")
                 dataDict[nameDev][0].append(deepcopy(sepData))
                 curOut = [0.] * len(gtType)
                 curOut[curType] = 1.
                 dataDict[nameDev][1].append(deepcopy(curOut))

result.close()
X = []
Y = []
maskX = []
#evalX = []
#evalY = []
#evalMaskX = []
paddingVal = 0.
inputFeature = sepcturalSamples * 6 * 2

count = 0

for nameDev in dataDict.keys():
    curX, curY = dataDict[nameDev]
    count += 1
    print '\r', count,
    sys.stdout.flush()

    #evalX += deepcopy(curX)
    #evalY += deepcopy(curY)

    X += deepcopy(curX)
    Y += deepcopy(curY)
    continue
    # if mode == 'one_user_out':
    # if nameDev[0] == select:
    # evalX += deepcopy(curX)
    # evalY += deepcopy(curY)
    # continue
    # elif mode == 'one_model_out':
    # if select in nameDev[1:]:
    # evalX += deepcopy(curX)
    # evalY += deepcopy(curY)
    # continue
    # X += deepcopy(curX)
    # Y += deepcopy(curY)

for idx in xrange(len(X)):
    curLen = len(X[idx])
    maskX.append([[1.0]] * curLen)
    for addIdx in xrange(wide - curLen):
        X[idx].append([paddingVal] * inputFeature)
        maskX[idx].append([0.0])

#for idx in xrange(len(evalX)):
 #   curLen = len(evalX[idx])
  #  evalMaskX.append([[1.0]] * curLen)
   # for addIdx in xrange(wide - curLen):
    #    evalX[idx].append([paddingVal] * inputFeature)
     #   evalMaskX[idx].append([0.0])

X = np.array(X)
Y = np.array(Y)
maskX = np.array(maskX)

#evalX = np.array(evalX)
#evalY = np.array(evalY)
#evalMaskX = np.array(evalMaskX)

print 'X', X.shape, X.dtype, 'Y', Y.shape, Y.dtype, 'maskX', maskX.shape, maskX.dtype
#print 'evalX', evalX.shape, evalX.dtype, 'evalY', evalY.shape, evalY.dtype, 'evalMaskX', evalMaskX.shape, evalMaskX.dtype

X = np.reshape(X, [-1, wide * inputFeature])
XY = np.hstack((X, Y))
print 'XY', XY.shape

#evalX = np.reshape(evalX, [-1, wide * inputFeature])
#evalXY = np.hstack((evalX, evalY))
#print 'evalXY', evalXY.shape
out_dir = 'C:\\projects\\data(09.08.2018)'
if not os.path.exists(out_dir):
    #os.mkdir(out_dir)
    os.mkdir(os.path.join(out_dir, 'hhar_data'))
    #os.mkdir(os.path.join(out_dir, 'eval'))
idx = 0
for elem in XY:
    fileOut = open(os.path.join(out_dir, 'hhar_data', 'data_' + str(idx) + '.csv'), 'w')
    curOut = elem.tolist()
    curOut = [str(ele) for ele in curOut]
    curOut = ','.join(curOut) + '\n'
    fileOut.write(curOut)
    fileOut.close()
    idx += 1


#idx = 0
#for elem in evalXY:
 #   fileOut = open(os.path.join(out_dir, 'eval', 'eval_' + str(idx) + '.csv'), 'w')
  #  curOut = elem.tolist()
   # curOut = [str(ele) for ele in curOut]
    #curOut = ','.join(curOut) + '\n'
    #fileOut.write(curOut)
    #fileOut.close()
    #idx += 1

print 'finish!'
