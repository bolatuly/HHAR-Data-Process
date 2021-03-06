import os
import sys
from copy import deepcopy

dataDir = '/Users/azamatbolat/Desktop/real-case-data/'
device = 'gear_s2'
#activities = ['working', 'give_lecture', 'receive_lecture']
activities = ['receive_lecture']


for activity in activities:

    fileList = os.listdir(dataDir + "/" + activity)

    dotList = []
    for fileName in fileList:
        if fileName[0] == '.':
            dotList.append(fileName)

    for elem in dotList:
        fileList.remove(elem)

    pairList = []
    singleList = []
    while len(fileList) > 1:
        curA = fileList[0]
        curPair = [curA]
        nameElem = curA.split('_')
        curLabel = '_'.join(nameElem[1:])
        for idx in xrange(1, len(fileList)):
            if curLabel in fileList[idx]:
                curPair.append(fileList[idx])
        if len(curPair) == 2:
            pairList.append(deepcopy(curPair))
            for pairElem in curPair:
                fileList.remove(pairElem)
        elif len(curPair) == 1:
            # print curLabel
            fileList = fileList[1:]
            singleList.append(curPair[0])
        else:
            print curLabel
            print 'Wrong', len(curPair), curPair
            fileList = fileList[1:]
            fileList.append(curPair[0])

    timeLabel = 'Creation_Time'
    pairSaveDir = '/Users/azamatbolat/Desktop/real-case-data/paired/'

    timeScale = 1000000.

    if not os.path.exists(pairSaveDir):
        os.mkdir(pairSaveDir)

    for pairElem in pairList:
        for fileElem in pairElem:
            if 'acc' in fileElem:
                pair1 = fileElem
            else:
                pair2 = fileElem
        # pair1, pair2 = pairElem
        nameElem = pair1.split('_')
        curLabel = '_'.join(nameElem[1:])

        pairFile1 = []
        print pair1
        fileIn1 = open(os.path.join(dataDir + '/'+activity, pair1))
        line = fileIn1.readline()
        count = 0
        while len(line) > 0:
            eval_line = eval(line)
            curElem = {}
            #curElem['Index'] = eval(curElem['Index'])
            curElem['Creation_Time'] = eval_line[3]
            #curElem['Arrival_Time'] = eval(curElem['Arrival_Time'])
            curElem['x'] = eval_line[0]
            curElem['y'] = eval_line[1]
            curElem['z'] = eval_line[2]
            pairFile1.append(deepcopy(curElem))
            line = fileIn1.readline()
            count += 1
            print '\r', count,
            sys.stdout.flush()
        print ''
        fileIn1.close()

        pairFile2 = []
        print pair2
        fileIn2 = open(os.path.join(dataDir + '/' + activity, pair2))
        line = fileIn2.readline()
        count = 0
        while len(line) > 0:
            eval_line = eval(line)
            curElem = {}
            #curElem['Index'] = eval(curElem['Index'])
            curElem['Creation_Time'] = eval_line[3]
            #curElem['Arrival_Time'] = eval(curElem['Arrival_Time'])
            curElem['x'] = eval_line[0]
            curElem['y'] = eval_line[1]
            curElem['z'] = eval_line[2]
            pairFile2.append(deepcopy(curElem))
            line = fileIn2.readline()
            count += 1
            print '\r', count,
            sys.stdout.flush()
        print ''
        fileIn2.close()

        idx1 = 0
        idx2 = 0
        fileOut = open(os.path.join(pairSaveDir, curLabel.split(".")[0].split("_")[1] + '-' + device+'-' + activity), 'w')
        print 'Write', fileOut
        count = 0
        while idx1 < len(pairFile1) and idx2 < len(pairFile2):
            curItem1 = pairFile1[idx1]
            curItem2 = pairFile2[idx2]
            curTime1 = curItem1[timeLabel] / timeScale
            curTime2 = curItem2[timeLabel] / timeScale

            # print curTime1, curTime2, curTime1==curTime2
            if abs(curTime1 - curTime2) < 0.1:
                curSaveElem = {}
                curSaveElem['Time'] = 0.5 * (curTime1 + curTime2)  # round(curTime1,1)
                curSaveElem['Accelerometer'] = deepcopy([curItem1['x'], curItem1['y'], curItem1['z']])
                curSaveElem['Gyroscope'] = deepcopy([curItem2['x'], curItem2['y'], curItem2['z']])
                fileOut.write(str(curSaveElem) + '\n')
                idx1 += 1
                idx2 += 1
                count += 1
                print '\r', count,
                sys.stdout.flush()
            elif curTime1 - curTime2 >= 0.1:
                idx2 += 1
            else:
                idx1 += 1
        print ''
        fileOut.close()
