import destables
#
# class des():


def permutation(key, table):
    return [key[i-1] for i in table]


def key_schedule(key):
    # discard every 8th bit
    permut = permutation(key, destables.PC_1)
