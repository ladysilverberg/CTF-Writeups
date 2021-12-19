from pwn import *
from ctypes import *
import time
import random

SECRET_KEY = [0x6c, 0x6f, 0x6c, 0x20, 0x69, 0x74, 0x73, 0x20, 0x72, 0x61, 0x6e, 0x64]

libRandom = CDLL("./librandom.so")
r = remote("io.ept.gg", 30050)
epoch_time = int(time.time())

def burn_rng():
	for i in range(3):
		random = libRandom.getRandom()

def update_secret():
	new_key = []
	random = libRandom.getRandom()
	for i in range(random&0xc0de):
		libRandom.getRandom()
	for i in range(0xc):
		key_byte = SECRET_KEY[i]
		random = libRandom.getRandom()
		new_byte = (key_byte ^ random) << (i & 0x1f)
		new_key.append(new_byte)
	return new_key

# Predict the future	
libRandom.seedRandom(epoch_time)
burn_rng()
sol = update_secret()
print(sol)

# Hack
for x in range(4):
	r.recvuntil(b"> ")
	r.send(b'1\n')
out = r.readrepeat(1)
print(out.decode())
for num in sol:
	r.send(str(num).encode()+b"\n")
	out = r.readrepeat(.1)
print(out)
out = r.readrepeat(1)
print(out)


	