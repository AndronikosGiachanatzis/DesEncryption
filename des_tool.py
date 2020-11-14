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
    # validation could be added but since input is hardcoded there is no need to do that
    key = "133457799BBCDFF1"
    plaintext = "GIACHANA"

    # split the key and get the 16 subkeys
    key_list = splitKey(key)
    subkeys = des.key_schedule(key_list)




if __name__ == "__main__":
    main()