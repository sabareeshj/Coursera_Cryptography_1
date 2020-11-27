import requests
# r = requests.get('http://crypto-class.appspot.com/po?er=f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4')

def xorb(a, b):
    return bytes(x^y for x,y in zip(a,b))
target = 'http://crypto-class.appspot.com/po?er='
q = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

iv = bytes.fromhex(q)[:16]
ct = q[32:64]
print(iv)
print(ct)
cattack = bytes(16)
padxor = bytes(15) + b'\x01'
pt = []
for position in reversed(range(0,16)):
    padding = bytes(position) + bytes([16 - position])*(16 - position)
    print('**************************The padding is')
    print(padding)
    print('**************************The IV is')
    print(iv)
    for i in range(0,256):
        bytemodify = bytes(position) + bytes([i]) + bytes(15 - position)
        ciphermodified = xorb(iv, bytemodify)
        finalcipher = xorb(padding, ciphermodified)
        q = finalcipher.hex() + ct
        r = requests.get(target + q)
        if r.status_code == 404:
            print(q + '...checking...position-' + str(position) + '...byte-'+ str(i) + '...status code...' + str(r.status_code))
            iv = ciphermodified
            pt.append(bytes([i]))
            break


print(pt)
    


# first try for first block
# keep the padding x01 and keep changing the last bit
#after first block move to nwxt block, lopp all these


