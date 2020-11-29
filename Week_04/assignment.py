import requests
import time


def xorb(a, b):
    return bytes(x^y for x,y in zip(a,b))
target = 'http://crypto-class.appspot.com/po?er='
q = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

freqOrder = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z','T', 'A', 'S', 'H', 'W', 'I', 'O', 'B', 'M', 'F', 'C', 'L', 'D', 'P', 'N', 'E', 'G', 'R', 'Y', 'U', 'V', 'J', 'K', 'Q', 'Z', 'X', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12, 13, 14, 15, 16, '.', ',', '-', '"', '_', '\'', ')', '(', ';', '=', ':', '/', '*', '!', '?', '$', '>', '{', '}', '[', ']', '\\', '+', '|', '&', '<', '%', '@', '#', '^', '`', '~']

byteOrder = []
message = bytes()


for i in range(len(freqOrder)):
    if(freqOrder[i] and type(freqOrder[i]) == str):
        byteOrder.append(ord(freqOrder[i]))
    else:
        byteOrder.append(freqOrder[i])

for i in range(17, 32):
    byteOrder.append(i)

for i in range(127, 256):
    byteOrder.append(i)



blocks = [q[i: i+32] for i in range(0, len(q), 32)]
start_time = time.time()
for i in range(2, 3):
    pt = []
    modBlock = bytes.fromhex(blocks[i])
    for position in reversed(range(16)):
        padBlock = bytes(position) + bytes([16 - position])*(16 - position)
        for j in byteOrder:
            print("block-", i, " positon-", position, " bytes-", j)
            guessBlock = bytes(position) + bytes([j]) + bytes(15 - position)
            ciphermodified = xorb(modBlock, guessBlock)
            finalcipher = xorb(padBlock, ciphermodified)
            q = "".join(blocks[:i]) + finalcipher.hex() + "".join(blocks[i+1:i+2])
            r = requests.get(target + q)
            if r.status_code == 404:
                print("Correct byte is ", j)
                modBlock = ciphermodified
                pt.append(bytes([j]))
                break
    pt = pt[::-1]
    message += b''.join(pt)


print(message)
print(f"Total runtime od program is {time.time() - start_time}")
    


# first try for first block
# keep the padding x01 and keep changing the last bit
#after first block move to nwxt block, lopp all these
# Total runtime od program is 2200.3635115623474


