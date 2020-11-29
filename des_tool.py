#!/usr/bin/python3
'''
Author: Andronikos Giachanatzis

Description: This module is the main module which initializes the encryption process of DES (ECB)
'''

import des
import destables
import concurrent.futures

# number of rounds
ROUNDS = 16


def bit_lst_to_string(lst):
    '''
    Transforms a bit array into a string representation of the data
    Parameters:
        -lst (list): The bit list:
    Returns:
        -(String): The String representation of the given bit array:
    '''
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in b]) for b in nsplit(lst, 8)]])
    return res


def nsplit(lst, n):
    '''
    Splits a given list into sub-lists of size n
    Parameters:
        -s (list): The list which will be splitted:
        -n (int): The size of each sublist:
    Returns:
        -(list): A list comprised by sublists each of size n:
    '''
    return [lst[k:k+n] for k in range(0, len(lst), n)]


def to_binary(data, encoding=None, step=1):
    '''
    Converts a string (decimal or hexadecimal) to binary
    Parameters:
        -data (String): The data to be converted to binary
        -encoding (int): the format (none for decimal, 16 for hexadecimal) of the given data
        -step (int): the step with which the data will be read
    Returns:
        -(String/list): The data in binary format. The return type is based on the input. If it is in decimal -> String
            otherwise -> list
    '''

    if encoding is None:
        temp = ''.join(format(ord(i), 'b').zfill(8) for i in data)
    else:
        temp = [bin(int(data[i]+data[i+1], 16))[2:] for i in range(0, len(data), step)]
    return temp


def split_key(s):
    '''
    Splits the given string and produces the key
    Paramaters:
        -s: The string from which the keys will be produced:
    Returns:
        -(list): The key as derived from the string:
    '''

    # get the bits
    temp = to_binary(s, 16, step=2)

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


def list_to_integers(lst):
    '''
    Converts a list's elements into integers
    Parameters:
        -lst (list): The lists whose elements will be converted to integers
    Returns:
        -(list): The list with integer elements:
    '''
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = int(lst[i][j])
    return lst


def get_keys(key):
    '''
    Creates the sub-keys from the given key. It is higher-level method than other functions similar to it (in the des.py
    module specifically)
    Parameters:
        -key (list): The original key from which the sub-keys will be derived
    Returns:
        -(list): The 16 sub-keys
    '''
    print(" creating subkeys...")
    # split the key and get the 16 subkeys
    key_list = split_key(key)
    subkeys = des.key_schedule(key_list)
    subkeys = list_to_integers(subkeys)

    return subkeys


# perform the initial permutation
def initial_permutation(block):
    '''
    Performs the initial permutation on the first block before the 16 rounds commence
    Parameters:
        -block (list): The block on which the permutation will be applied:
    Returns:
        -(list): The block after the permutation
    '''
    print(" performing initial permutation on the block of data")
    # convert plaintext to bits
    block = to_binary(block)
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
        future_subkeys = executor.submit(get_keys, key)
        # thread for blocks
        future_block = executor.submit(initial_permutation, plaintext)


    # get the subkeys
    subkeys = future_subkeys.result()

    # get the ip of the block
    block = future_block.result()
    # split the block
    l, r = des.split_block(block)

    print(" starting rounds...")
    result = list()
    # start the 16 rounds
    for i in range(ROUNDS):
        # expand r to 48
        exp_r = des.expand(r, destables.E)
        # xor r with key
        x = des.xor(exp_r, subkeys[i])
        # apply SBOXes to x (splitting is done internally)
        x = des.substitute(x)
        # perform permutation
        x = des.permutation(x, destables.P)
        # xor x with r
        x = des.xor(l, x)
        l = r
        r = x

    # perform the final permutation
    result += des.permutation(r+l, destables.FP)
    print("[+] ENCRYPTION SUCCESSFUL")

    # print ciphertext
    ciphertext = bit_lst_to_string(result)
    print("\n\nciphertext: %r"  %ciphertext)

    # print hex format
    hex_ciphertext = ''.join([hex(int(ord(i)))[2:]+" " for i in ciphertext])
    print("\tas hex: ", hex_ciphertext)

    # write to file
    print("\nWriting to file: 'ciphertext.txt'")
    with open('ciphertext.txt', "w") as fout:
        fout.write(ciphertext)
        fout.write("\n\n\n")
        fout.write(hex_ciphertext)


if __name__ == "__main__":
    main()