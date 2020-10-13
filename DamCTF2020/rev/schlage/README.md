## rev/schlage
>I went to the hardware store yesterday and bought a new lock, for some reason it came on a flash drive. Can you figure out how to unlock it? I really need to get into my apartment.

>Rather than traditional lock picks, you may find this, that, or this other expensive-looking thing to be helpful.

>nc chals.damctf.xyz 31932


Reversing the program with Ghidra shows that it needs five correct pins to be entered:

**Pin 1 - Simple XORing:**
* input ^ 0x3E ^ 0x57 ^ 0x81 ^ 0xD3 ^ 0x25 ^ 0x93 = 0xEE
* input ^ 0x80 = 0xEE
* input = 0x63 = 99

**Pin 2 - Seeding rand():**
* result from time() will be printed and used to seed rand()
* fetch time printed by the program, seed rand(), calculate rand()
* pass result as input

**Pin 3 - More XORing:**
* 0xDEADBEEF ^ 0x13371337 = 3449466328

**Pin 4 - Strings:**
* Gets input str of max 32 characters
* Calculates rand() as randNum
* For each character c in str:
    * pin = pin + (c ^ randNum % 10 + 65)
* Checks if pin = 0x123 (291)

**Pin 5 - Seeding rand() again:**
* srand(0x42424242)
* calculate rand()
* pass result as input


**Solution Script (May need to run several times due to a bit of a messy pin 4 implementation)**
```python=
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
````

**libschlage:**
Used to gain access to srand() and rand() in python.

Compilation:
* gcc -c -fPIC schlage.c -o schlage.o
* gcc schlage.o -shared -o libschlage.so

schlage.h
```c=
void seedRandom(unsigned int seed);
int getRandom();
````

schlage.c
```c=
#include <stdlib.h>
#include "schlage.h"

void seedRandom(unsigned int seed) {
    srand(seed);
}

int getRandom() {
    return rand();
}
````

Flag: `dam{p1ck1NG_l0Ck5_w1TH_gdB}`