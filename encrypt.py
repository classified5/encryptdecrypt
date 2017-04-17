import binascii
import struct

def add(x, y):
    maxlen = max(len(x), len(y))

    # Normalize binary
    x = x.zfill(maxlen)
    y = y.zfill(maxlen)

    result = ''
    carry = 0

    for i in range(maxlen - 1, -1, -1):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0

        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0: result = '1' + result

    return result.zfill(maxlen)


def inverse(x):
    if x == 1:
        return 0
    else:
        return 1


encryptresult = ""

def encrypt(left, right):

    leftkey = left
    rightkey = right

    arrleftkey = map(int, leftkey)
    arrrightkey = map(int, rightkey)

    print "key: \n" + key

    # read file
    with open('data.txt', 'r') as myfile:
        data = myfile.read().replace('\n', '')

    # make sure input is % 64
    if (len(data) % 8 != 0):
        n = 8 - len(data) % 8
        for i in range(n):
            data = data + ' '

    print "input file content: \n" + data
    # convert input to binary
    stringnum = ''.join(format(ord(i), 'b').zfill(8) for i in data)

    print "stringnum", stringnum

    # mapping binary into 64 bit length
    datalength = len(stringnum)
    datanumber = 64
    stringmap = [stringnum[i:i + datanumber] for i in range(0, datalength, datanumber)]

    print "stringmap", stringmap

    encrypt = []

    for y in range(len(stringmap)):
        arr = map(int, stringmap[y])
        print "arr", arr
        xor = []

        # xor operation
        for i in range(len(arrleftkey)):
            tempxor = arrleftkey[i] ^ arr[i]
            xor.append(tempxor)

        print "xor", xor
        xorresult = ''.join(str(e) for e in xor)
        # print xorresult

        # add operation
        addresult = add(xorresult, rightkey)

        # mod operation
        if len(addresult) > 64:
            addresult = addresult[1:]
        else:
            addresult = addresult

        print "addresult", addresult

        encrypt.append(addresult)

    print "encrypt", encrypt

    # convert list to string
    encryptresult = ''.join(str(e) for e in encrypt)
    print "encryt result", encryptresult

    # convert string to character
    # result = "".join(map(chr,c))
    n = int(encryptresult, 2)
    print "n", n
    result = binascii.unhexlify('%x' % n)
    print "Ciphertext Encrypt \n" + result

    # save to file
    text_file = open("encrypted.txt", "w")
    text_file.write(result)
    text_file.close()

    return encryptresult


def decrypt(left, right, enc):
    encryptresult = enc
    leftkey = left
    rightkey = right

    arrleftkey = map(int, leftkey)
    arrrightkey = map(int, rightkey)

    # mapping binary into 64 bit length
    decryptlength = len(encryptresult)
    decryptnumber = 64
    decryptm = [encryptresult[i:i + decryptnumber] for i in range(0, decryptlength, decryptnumber)]

    print "stringmap", decryptm

    rightinverse = []
    # print rightkey

    # inverse rightkey
    for i in range(len(arrrightkey)):
        # print arrrightkey[i]
        tempinverse = inverse(arrrightkey[i])
        rightinverse.append(tempinverse)

    # convert list to string
    inverseresult = ''.join(str(e) for e in rightinverse)
    # print inverseresult

    # add 1 to inverse right key
    inv = add(inverseresult, '1')
    print "inverse", inv

    appendxor = []

    for y in range(len(decryptm)):
        decryptadd = ''.join(str(e) for e in decryptm[y])

        # add inverse with input
        decryptresult = add(inv, decryptadd)
        # mod process
        if len(decryptresult) > 64:
            decryptresult = decryptresult[1:]
        else:
            decryptresult = decryptresult

        decryptmap = map(int, decryptresult)

        xorresult = []

        # xor process
        for s in range(len(arrleftkey)):
            tempx = arrleftkey[s] ^ decryptmap[s]
            xorresult.append(tempx)

        temp = ''.join(str(e) for e in xorresult)

        appendxor.append(temp)

    print "appendxor", appendxor

    decrypt = ''.join(str(e) for e in appendxor)

    print "xor result", decrypt

    # convert binary to char
    decryptint = int(decrypt, 2)
    decryptfinal = binascii.unhexlify('%x' % decryptint)
    print "Decrypted \n" + decryptfinal

    text_file = open("decrypted.txt", "w")
    text_file.write(decryptfinal)
    text_file.close()

    return 1



print "Encrypt Decrypt Program"
print "Please input text in data.txt"
print "Input key (MUST BE 8 character)"

key = raw_input()
key = key.strip()

# convert input to binary
stringkey = ''.join(format(ord(i), 'b').zfill(8) for i in key)

rstringkey = stringkey[::-1]

e = encrypt(stringkey, rstringkey)
if e is not None:
    print "Encrypt Successfull!!!"

d = decrypt(stringkey, rstringkey,e)
if d == 1:
    print "Decrypt Successfull!!!"


