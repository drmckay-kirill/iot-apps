from ABE import ABEEngine
import pickle, sys, json, argparse, string
from random import *

def GenerateRandomString(stringLength):
    return "".join(choice(string.ascii_letters) for x in range(stringLength))

def GenetarateAttrList(numberOfAttr):
    return [GenerateRandomString(10) for x in range(1, numberOfAttr + 1)]

def iteration(numberOfAttr, numberOfSteps):
    test_message = "TEST_MESSAGE"

    print("Number of attributes: %d"%numberOfAttr)
    attrList = GenetarateAttrList(numberOfAttr)
    test = ABEEngine()
    test.SetAttributesList(attrList)
    MK, PK = test.Setup()
    for i in range(numberOfSteps):
        test_attr = [ choice(attrList) for x in range(randint(1, numberOfAttr)) ]
        test_attr = list(set(test_attr))
        CT, encrypted = test.EncryptHybrid(PK, test_message, attrList)
        test_packet = test.SerializeCharmObject(CT)
        test_packet_bytes = pickle.dumps(test_packet)
        
        with open('data.csv', 'a') as data_file:
            data_file.write( str(numberOfAttr) + ";" + str(len(test_packet_bytes)) + "\n")        

def main():
    maxAttr = 80
    maxSteps = 25
    print("Test size of messages of AND-gates ABE schemes")
    print("Max number of attributes: %d"%maxAttr)
    with open('data.csv', 'w') as data_file:
        data_file.write("attr;size\n")
    for i in range(3, maxAttr + 1):
        iteration(i, maxSteps)

if __name__ == "__main__":
    main()