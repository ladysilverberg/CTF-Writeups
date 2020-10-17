# Constant returned by Lambda 3
const_string = 'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1A'

flag = ''

with open('flag_enc', 'rb') as file:
    enc_flag = file.read()

for i in range(len(enc_flag)):
    byte = ord(enc_flag[i])
    o5 = byte ^ 1 # Reverse XORing of output byte
    o4 = o5 ^ 90 # Reverse Lambda 1
    o3 = o4 - 20 # Reverse Lambda 2
    o2 = ord(const_string[i]) # Reverse Lambda 3
    o1 = o3 ^ o2 # Reverse Lambda 1
    flag += chr(o1)

print(flag)