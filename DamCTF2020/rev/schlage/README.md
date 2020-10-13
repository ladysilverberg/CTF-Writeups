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


**Solution Script**
May need to run several times due to a bit of a messy pin 4 implementation

**libschlage:**
Used to gain access to srand() and rand() in python.

Compilation:
* gcc -c -fPIC schlage.c -o schlage.o
* gcc schlage.o -shared -o libschlage.so

Flag: `dam{p1ck1NG_l0Ck5_w1TH_gdB}`