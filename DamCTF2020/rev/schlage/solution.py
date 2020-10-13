from pwn import *
from ctypes import *
import random

libSchlage = CDLL("./libschlage.so")
r = remote("chals.damctf.xyz", 31932)

def wait_for_input(pinPrint=False):
    if pinPrint:
        line = r.recvuntil("Which pin would you like to open?\n> ")
    else:
        line = r.recvuntil("> ")
    print(line.decode())

def read_time_variable():
    for x in range(2):
        line = r.recvline()
        print(line.decode())
    time = r.recvline().decode()
    print(time)
    time = time.replace("\n", "")
    return int(time)

def crack_pin_4():
    wait_for_input(True)
    r.sendline("4")

    # Calculate next random number
    random_num = libSchlage.getRandom()
    value = random_num % 10 ^ 65
    
    # Calculate sentence
    line = r.recvuntil("What's your favorite sentence?")
    print(line.decode())
    
    byte = 0x61 ^ value # 0x123 / 3 = 0x61, value ^ value ^ 0x61 = 0x61
    sentence = bytes.fromhex(hex(byte)[2:]) * 3
    sentence = sentence.decode()
    print(sentence)
    r.sendline(sentence)

    # Check result
    line = r.recvline()
    print(line.decode())
    if "Not a big fan" in line.decode():
        return True
    else:
        return False

# Pin 3
wait_for_input(True)
r.sendline("3")
wait_for_input()
r.sendline("3449466328")

# Pin 1
wait_for_input(True)
r.sendline("1")
wait_for_input()
r.sendline("99")

# Pin 5
wait_for_input(True)
r.sendline("5")
libSchlage.seedRandom(0x42424242)
random_num = libSchlage.getRandom()
r.sendline(str(random_num))

# Pin 2
wait_for_input(True)
r.sendline("2")
time = read_time_variable()
libSchlage.seedRandom(time)
random_num = libSchlage.getRandom()
wait_for_input()
r.sendline(str(random_num))

# Pin 4
status = True
while status:
    status = crack_pin_4()
line = r.recvuntil("}")
print(line.decode())