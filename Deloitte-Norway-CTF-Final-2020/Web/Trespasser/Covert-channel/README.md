## WEB600 - Trespasser (Covert Channel)
A set of rotate instructions was found in the javascript source code of the app, which is what the game level loops through. We can decode left rotations as 0 and right rotations as 1 to get a binary string. If we group these together in groups of 8, we can then decode them as ASCII.

Output: *`01100110 01101100 01100001 01100111 SPACE 01101001 01110011 SPACE 01000011 01010100 01000110 01111011 00110100 00111000 00110010 00111000 01100010 00111000 01100110 00110000 01100101 01100110 01100110 00111001 01100100 01100001 01100101 01100010 00110111 01100010 01100001 01100010 00110011 01100011 00110101 01100010 01100001 01100101 00110001 00111000 00110110 01100001 01100110 00110111 01111101`*

Decoding this as ASCII gives the string `flag is CTF{4828b8f0eff9daeb7bab3c5bae186af7}`