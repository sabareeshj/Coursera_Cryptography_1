# read the video file in 1kbs
#append them to a array
from Crypto.Hash import SHA256

video = open('6.1.intro.mp4_download', 'rb')
vBytes = video.read(1024)
vBlocks = []
while vBytes:
    # read block of 1024 bytes and append to array
    vBlocks.append(vBytes)
    vBytes = video.read(1024)
video.close()
h = SHA256.new()
h.update(vBlocks[-1])
last_hash = h.digest()
for i in reversed(vBlocks[:-1]):
    #perform the hash
    h = SHA256.new()
    h.update(i)
    h.update(last_hash)
    last_hash = h.digest()
print(h.digest().hex())
