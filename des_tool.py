import des
import destables

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


def main():
    key = "133457799BBCDFF1"
    plaintext = "GIACHANA"

    # split the key into a 8x7 list (with the parity bits removed
    key_list = splitKey(key)
    des.key_schedule(key_list)



if __name__ == "__main__":
    main()