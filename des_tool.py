#!/usr/bin/python3
'''
Author: Andronikos Giachanatzis
'''

import des
import destables
import threading
import time
import concurrent.futures

# split the key in hex numbers
def splitKey(s):

    # get the bits
    temp = [bin(int(s[i]+s[i+1], 16))[2:] for i in range(0, len(s), 2)]

    # add padding
    for i in range(len(temp)):
        if len(temp[i]) < 8:
            diff = 8-len(temp[i])
            temp[i] = '0'*diff + temp[i]

    # convert it to a list and discard the parity bits
    key = []
    for char in temp:
        for bit in char:
            key.append(bit)
    return key

def getKeys(key):
    # split the key and get the 16 subkeys
    key_list = splitKey(key)
    subkeys = des.key_schedule(key_list)
    return subkeys


def block_function_here():
    time.sleep(2)
    return ("val1", "val2")

def main():
    # validation could be added but since input is hardcoded there is no need to do that
    key = "133457799BBCDFF1"
    plaintext = "GIACHANA"

    # split the key and get the 16 subkeys
    print("starting thread")
    future_subkeys = None
    # create one thread for the creation of the 16 subkeys and another one for the
    # initial block calculation
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_subkeys = executor.submit(getKeys, key)
        # thread for blocks
        future = executor.submit(block_function_here)

    # get the subkeys
    subkeys = future_subkeys.result()


    print("thread finished")






if __name__ == "__main__":
    main()