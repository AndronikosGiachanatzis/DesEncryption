import destables
#
# class des():


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
    pass





