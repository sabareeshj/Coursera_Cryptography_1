from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import sys

cbcCiphers = [('140b41b22a29beb4061bda66b6747e14','4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'),('140b41b22a29beb4061bda66b6747e14','5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253')]

ctrCiphers = [('36f18357be4dbd77f050515c73fcf9f2','69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'),('36f18357be4dbd77f050515c73fcf9f2','770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451')]

plainTexts = []

def xorb(a,b):
    # This function XORs two byte arrays
    return bytes(x^y for x,y in zip(a,b))


for i in range(len(cbcCiphers)):
    #encryption key
    cbcKey = bytes.fromhex(cbcCiphers[i][0])

    #cipher text
    cbcCipherText = bytes.fromhex(cbcCiphers[i][1])

    #intialization vector
    cbcIV = cbcCipherText[:16]

    aes = AES.new(cbcKey, AES.MODE_CBC, cbcIV)

    #iv is prepended to the cipher text, 16 bytes
    plaintext = (aes.decrypt(cbcCipherText[16:]))

    #removing the padded block
    plaintext = plaintext[:-plaintext[-1]]
    
    print('The plain text derived using AES CBC library  is ' +  '\"' + plaintext.decode() + '\"')

    #CBC implementation using ECB
    aes = AES.new(cbcKey, AES.MODE_ECB)
    plaintext = bytes()

    #breaking into n blocks of 16 bytes
    cipherBlocks = [cbcCipherText[i: i+16] for i in range(0, len(cbcCipherText), 16)]

    #appending IV to the list of blocks for simpler code, m[-1] = IV
    cipherBlocks.append(cipherBlocks.pop(0))

    #decryption for each block, m[i] = D(k, c[i]) ^ m[i-1]
    for i in range(len(cbcCipherText)//16 - 1):
        plaintext += xorb(aes.decrypt(cipherBlocks[i]), cipherBlocks[i-1])
    
    plaintext = plaintext[:-plaintext[-1]]

    print('The plaintext derived using the CBC implementation is ' + '\"' + plaintext.decode() + '\"')

for i in range(len(ctrCiphers)):

    ctrKey = bytes.fromhex(ctrCiphers[i][0])
    ctrCipherText = bytes.fromhex(ctrCiphers[i][1])
    ctrIV = ctrCipherText[:16]
    ctrCipherText = ctrCipherText[16:]
    ctr = Counter.new(128, initial_value = bytes_to_long(ctrIV))
    aes = AES.new(ctrKey, AES.MODE_CTR, counter=ctr)
    plaintext = aes.decrypt(ctrCipherText)
    print('The plain text derived using AES CTR library  is ' +  '\"' + plaintext.decode() + '\"')

    #AES implemetation using ECB
    aes = AES.new(ctrKey, AES.MODE_ECB)
    plaintext = bytes()
    cipherBlocks = [ctrCipherText[i: i+16] for i in range(0, len(ctrCipherText), 16)]
    ctr = ctrIV.hex()
    ctr = int(ctr, 16)
    for j in range(len(cipherBlocks)):
        # creating a stream cipher andperforming XOR while incrementing counter
        plaintext += xorb(cipherBlocks[j], aes.encrypt(bytes.fromhex(hex(ctr+ j)[2:])))
    print('The plain text derived using AES CTR implementation  is ' +  '\"' + plaintext.decode() + '\"')



