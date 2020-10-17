## EXP150 - AdminOverfl0w
Disassembling the binary in Ghidra shows that the binary will take an input string, calculate the MD5 hash of it and then compare it against some operations performed on an MD5 hash stored as MASTER_PASSWORD, which has the value of "f13fd66c890923ba21d9e7112a36995a" on inspection:

![](https://i.imgur.com/NQxCYst.png)

Looking at the disassembly in GDB, the disassembly in Ghidra is likely a bit obfuscated in this case:

![](https://i.imgur.com/LADG19c.png)

By running the program a little in GDB, I figure out that the hex2int function takes in a character such as '5', 'A', 'f' etc. and return 0x5, 0xA, 0x5 respectively. Looking at the disassembly in GDB, hex2int is called on each byte of the MASTER_PASSWORD (at around main+150). This call simply starts by taking in the first value of the MASTER_PASSWORD, such as 'f' and translates it to 0xf. It then shifts this value to the left so a 0 is appended. The result becomd 0xf0. At main+190 there is another call to hex2int which takes in the next character of the MASTER_PASSWORD. In the first loop it will take in '1' since it follow 'f' and translate it to 0x1. the it adds this value to out previous value of 0xf0 to get 0xf1. Then it loops again with the next couple of characters of the MASTER_PASSWORD and does so 16 times.

In essence, each iteration of the loop takes two characters of MASTER_PASSWORD and translates it from string to hex, such as 'f1' to 0xf1. At the end of each iteration it takes the first byte of the MD5 result of our input. If we for example sent in "test" as our input string, the MD5 of this would be "098f6bcd4621d373cade4e832627b4f6". The loop would then take 'f1' and compare to '09', then take '3f' and compare to '8f' and so on. If a byte is equal, the variable stored at RBP-0x40 gets incremented by 1.

Every time this local variable is incremented, it will check if it equals 0x10 = 16. If it does, it will give us escalate our priviledges on the system through a call to setresuid() and system(). This essentially means that the MD5 hash of our input has to equal the MASTER_PASSWORD. One solution could be to find an MD5 collision, but this is too time consuming.

Instead, we note that in the beginning of the program, 0x68 is subtracted from RBP to allocate storage for local variables. Our input from scanf is eventually stored in RBP-0x30, while the local variable check mentioned earlier is stored at RBP-0x40. There is no check to ensure that our input is limited to 16 bytes (aka the length of an MD5 as a hex string). This means that if we provide input longer than 16 bytes, our local variable will be overwritten!

![](https://i.imgur.com/DeLxfXE.png)

Using python, I feed in the input of 16 A's and appends 0x10 represented in binary. This means the local variable at RBP-0x40 will be set to 0x10. The loop will run 16 times, and at the end it checks if this local variable equals 0x10. Despite the hashes not being equal at all, this check will succeed and we have gained administrator rights on the system.
