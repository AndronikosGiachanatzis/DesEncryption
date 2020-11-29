#!/usr/bin/python3
'''
Author: Andronikos Giachanatzis

Description: This python module contains all the separate functions that appear during the DES encryption phase.
'''


import destables


def permutation(block, table):
    '''
    Performs a permutation of the elements in a given block according to a permutation table
    Parameters:
        -block (list): The block on which the permuation will be applied:
        -table (list): The table on which the permutation is based on:
    Returns:
        -(list) The block with the permutations applied according to the table parameter:
    '''
    return [block[i-1] for i in table]


def expand(block, table):
    '''
    Performs a permutation of the elements in a given block according to a permutation table. Same function as
    permutation but it's defined here also, for correspondence to the steps in DES and for clarity
    Parameters:
        -block (list): The block on which the permuation will be applied:
        -table (list): The table on which the permutation is based on:
    Returns:
        -(list): The block with the permutations applied according to the table parameter:
    '''
    return [block[i-1] for i in table]


def lshift(block, n):
    '''
    Shifts left the elements of the given by n positions
    Parameters:
        -block (list): The block of which the elements will be shifted:
        -n (int): The number of left shifts to be perfomed on the block:
    Returns:
        -(list): The block shifted left by n positions:
    '''
    return block[n:] + block[:n]


def split_key(key):
    '''
    Splits the key into two halves, which are represented as two lists
    Parameters:
        -key (string): The original key to be split:
    Returns:
        -(list): A list containing the two halves of the given key:
    '''
    c = []
    d = []
    # split the key into 2 halves
    for i in range(len(key)//2):
        c.append(key[i])
        d.append(key[i+len(key)//2])

    return c, d


def split_block(block):
    '''
    Splits a given block into two halves which are represented as two lists. Same funstion as splitKey(), but it's
    defined here also, for correspondence to the steps of DES and for clarity
    Parameters:
        -block (list): The block to be split:
    Returns:
        -(list): A list containing the two halves of the given block:
    '''
    return split_key(block)


def key_schedule(key):
    '''
    Creates the 16 sub-keys from the original key which are represented as 16 lists inside one list
    Parameters:
        -key (String): The original key:
    Returns:
        -(list): The 16 sub-keys
    '''
    # the list that contains all the subkeys
    keys = []

    # perform the Permutation Choice 1
    perm_key = permutation(key, destables.PC_1)
    # split the key in 2 halves
    c, d = split_key(perm_key)

    # generate the 16 subkeys
    for i in range(16):
        # shift the two parts of the subkeys for as many bits as the SHIFT table says
        c = lshift(c, destables.SHIFT[i])
        d = lshift(d, destables.SHIFT[i])

        # perform the Permutation Choice 2
        perm_key = c + d # merge the 2 halves

        # add the subkey to the subkey list
        keys.append(permutation(perm_key, destables.PC_2))

    return keys


def xor(r, key):
    '''
    XOR each element of r with the elements of key
    Parameters:
        -r (list): The first component of the XOR function:
        -key (list): The second component of the XOR function:
    Returns:
        -(list): A list containing the result of the XOR function for each element of two components:
    '''
    # zip every corresponding bit pair and perform bitwise xor
    return [x ^ y for x, y in zip(r,key)]


def substitute(block):
    '''
    Performs the substitution of the elements of a block using the appropriate SBOXes
    Parameters:
        -block (list): The block of which the elements will be substituted:
    Returns:
        -(list): The block with the substituted elements according to the SBOXes:
    '''

    # break block into 8 6-bit blocks
    sub_blocks = break_block(block)
    # apply the sboxes in each block
    result = list()
    for i in range(len(sub_blocks)):
        b = sub_blocks[i]
        # get the 1st and last bit together
        m_row = int(str(b[0]) + str(b[5]), 2)
        # get the 2-5 bits together
        n_column = int(''.join([str(i) for i in b[1:][:-1]]), 2)
        # get the value of the sbox
        s_value = destables.S_BOX[i][m_row][n_column]
        bin_svalue = bin(s_value)[2:].zfill(8)[4:]
        result += [int(i) for i in bin_svalue]
    return result


def break_block(block):
    '''
    Breaks the given block into 8 6-bit sub-blocks
    Parameters:
        -block (list): The block which will be broken:
    Returns:
        -(list): A list comprised by 8 lists, each of which contains an 6-bit sub-block of the original block:
    '''
    # break the block into 8 6-bit sub-blocks
    return [block[i:i+6] for i in range(0, len(block), 6)]

