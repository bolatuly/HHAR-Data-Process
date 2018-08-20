linked_files = {}
linked_locations = {}
linked_ds = {}
results = {}

users_to_be_test = {
    "1": "write",  # worker,  # hyngyou
    "2": "type",  # staff,  # tohun
         "3": "speak",  # speaker,  # dongmin
              "4": "listen",  # listener,  # byungon
                   "5": "listen",  # listener,  # youngbok
                        "6": "listen",  # student,  # hyemi
                             "7": "speak",  # lecturer,  # azamat
                                  "8": "listen",  # student,  # friend
                                       "9": "listen"  # student",  # frined 2
}
rooms = [404, 405, 410, 422]

gtType = ["write", "listen", "speak", "type"]
idxList = range(len(gtType))


def myrange(start, end):
    return range(start, end + 1)


if __name__ == "__main__":
    fileIn = open("C:\\projects\\HHAR-Data-Process\\out\\file_link_eval.txt")
    line = fileIn.readline()
    while len(line) > 0:
        curElem = eval(line)
        linked_files[curElem['filename']] = curElem['data']
        line = fileIn.readline()

    fileIn = open("C:\\projects\\HHAR-Data-Process\\out\\location.txt")
    line = fileIn.readline()
    while len(line) > 0:
        curElem = eval(line)
        linked_locations[curElem['filename']] = curElem['location']
        line = fileIn.readline()

    fileIn = open("C:\\projects\\HHAR-Data-Process\\out\\result.csv")
    line = fileIn.readline()  # skip line
    line = fileIn.readline()
    while len(line) > 0:
        curElem = line.split(",")
        f = curElem[0].split("/")[1]

        results[f] = curElem[2].rstrip()
        line = fileIn.readline()

    misses = 0
    success = 0
    for user in users_to_be_test:
        for link in linked_files.keys():
            #for type in users_to_be_test[user]:
            type = users_to_be_test[user]
            for room in rooms:
                if type + '_' + user + '_' + str(room) + '_sample' == link:
                    print type + '_' + user + '_' + str(room) + '_sample'
                    part_success = 0
                    part_misses = 0
                    for f in myrange(linked_files[link][0], linked_files[link][1]):
                        st = "data_" + str(f) + ".csv"
                        if st in results:
                            if type == gtType[int(results[st])]:
                                print st + " " + type + "1"
                                success = success + 1
                                part_success = part_success + 1
                            else:
                                print st + " " + type + "0"
                                misses = misses + 1
                                part_misses = part_misses + 1
                    print "part res: " + str(part_success) + " " + str(part_misses)

    print "total cases: " + str(success + misses)
    print "right: " + str(success)
    print "wrong: " + str(misses)
    print "percentage: " + str(100 - (float(misses*100)/float(success)))
