## REV300 - Python reversing

The file *flag_enc* contains the python bytecode of a program. By reading the bytecode, we can manually construct the program in a reassembled form (manual_reassembly.py).

We can also disassemble the lambdas:
```python=
import dis
import marshal
l1, l2, l3, l4 = marshal.loads(<snip>)
print(dis.dis(l1))
print(dis.dis(l2))
print(dis.dis(l3))
print(dis.dis(l4))
````

This gives us the bytecode:

```
Lambda 1:
  1           0 LOAD_FAST                0 (a)
              3 LOAD_FAST                1 (b)
              6 BINARY_XOR          
              7 RETURN_VALUE        
None
-------------------------------------------
Lambda 2:
  1           0 LOAD_FAST                0 (a)
              3 LOAD_FAST                1 (b)
              6 BINARY_ADD          
              7 RETURN_VALUE        
None
-------------------------------------------
Lambda 3:
  1           0 LOAD_CONST               1 ('Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1A')
              3 RETURN_VALUE        
None
-------------------------------------------
Lambda 4:
  1           0 LOAD_GLOBAL              0 (raw_input)
              3 CALL_FUNCTION            0
              6 RETURN_VALUE       
```

Lambda 1 simply XORs two inputs together. Lambda 2 adds two inputs and Lambda 3 returns a constant string. Finally, lambda 4 takes some user input.
With this in hand, we have everything we need to reverse the flag.
Running solution.py then yields the flag:

Flag: `CTF{b853e27db2e3ae06794d32a53f6ee356}`