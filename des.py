import destables



def permutation(block, table):
    return [block[i-1] for i in table]

def expand(block, table):
    return [block[i-1] for i in table]



def lshift(block, n):
    return block[n:] + block[:n]


def splitKey(key):
    c = []
    d = []
    for i in range(len(key)//2):
        c.append(key[i])
        d.append(key[i+len(key)//2])

    return c, d

def splitBlock(block):
    return splitKey(block)


def key_schedule(key):
    # the list that contains all the subkeys
    keys = []

    # perform the Permutation Choice 1
    perm_key = permutation(key, destables.PC_1)
    # split the key in 2 halves
    c, d = splitKey(perm_key)

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
    # zip every corresponding bit pair and perform bitwise xor
    return [x ^ y for x, y in zip(r,key)]


def substitute(block):

    # break block into 8 6-bit blocks
    sub_blocks = breakBlock(block)
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



def breakBlock(block):
    # break the block into 8 6-bit sub-blocks
    return [block[i:i+6] for i in range(0, len(block), 6)]

