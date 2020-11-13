
from itertools import combinations
from collections import Counter

def xorb(a,b):
    # This function XORs two byte arrays
    return bytes(x^y for x,y in zip(a,b))

# retrieve the ciphertexts from file
ctlst = [bytes.fromhex(x.strip()) for x in open('ciphers.txt')]

cnum = len(ctlst[-1])

KEY = [Counter() for i in range(cnum)]

# for all 55 combinations
for a,b in combinations(ctlst,2):
    for c in range(cnum):
        x = a[c]^b[c]   #xor 83 times down length of 2 cts
        if 64 < x <= 90 or 96 < x <= 122:
            #if result in range [a-zA-Z] one of the byte must be space so vote both for space
            KEY[c][a[c]^32]+=1
            KEY[c][b[c]^32]+=1

# The most voted bytes will be the values of key bytes
key = [k.most_common(1)[0][0] for k in KEY]

print(xorb(key,ctlst[-1]).decode())


