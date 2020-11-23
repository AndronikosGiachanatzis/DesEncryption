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

ROUNDS = 16

def toBinary(data, encoding=None, step=1):

    if encoding is None:
        temp = ''.join(format(ord(i),'b').zfill(8) for i in data)
    else:
        temp = [bin(int(data[i]+data[i+1], 16))[2:] for i in range(0, len(data), step)]
    return temp


def splitKey(s):

    # get the bits
    temp = toBinary(s, 16,  step=2)

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

def listToIntegers(keys):
    for i in range(len(keys)):
        for j in range(len(keys[i])):
            keys[i][j] = int(keys[i][j])
    return keys



def printSubkeysToFile(keys):
    with open("subkeys.txt", "w") as f:
        for i in keys:
            f.write(str(i))
            f.write("\n")


def getKeys(key):
    print(" creating subkeys...")
    # split the key and get the 16 subkeys
    key_list = splitKey(key)
    subkeys = des.key_schedule(key_list)
    subkeys = listToIntegers(subkeys)
    # print(type(subkeys[1][3]))
    return subkeys


# perform the initial permutation
def initialPermutation(block):
    print(" performing initial permutation on the block of data")
    # convert plaintext to bits
    block = toBinary(block)
    # perform the initial permutation of the block using the IP table
    perm_block = des.permutation(block, destables.IP)

    # convert to integers (will be corrected into one function afterwards)
    block = list()
    for i in perm_block:
        block.append(int(i))
    return block


def main():
    # validation could be added but since input is hardcoded there is no need to do that
    key = "133457799BBCDFF1"
    plaintext = "GIACHANA"

    # perform validity checks on input
    if len(plaintext) < 8:
        print("[-] Plaintext must be at least 64 bits (or 6 characters) long. Padding is not supported (yet).")
        print("Exiting...")
        exit(0)

    if len(key) < 16:
        print("[-] Key must be at least  128 bits (or 16 characters) long.")
        print("Exiting...")
        exit(0)


    print("[+] Starting")
    # split the key and get the 16 subkeys
    future_subkeys = None

    # create one thread for the creation of the 16 subkeys and another one for the
    # initial block calculation
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_subkeys = executor.submit(getKeys, key)
        # thread for blocks
        future_block = executor.submit(initialPermutation, plaintext)


    # get the subkeys
    subkeys = future_subkeys.result()
    printSubkeysToFile(subkeys)

    # get the ip of the block
    block = future_block.result()
    print(block)
    # split the block
    l, r = des.splitBlock(block)

    print(" starting rounds...")
    # start the 16 rounds
    for i in range(ROUNDS):
        # expand r to 48
        exp_r = des.expand(r, destables.E)
        x = des.xor(exp_r, subkeys[i])





if __name__ == "__main__":
    main()