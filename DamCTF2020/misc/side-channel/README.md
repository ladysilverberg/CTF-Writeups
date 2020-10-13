## misc/side-channel
>We built a super-secure password checker.
Can you guess what my password is?
>
>This challenge does NOT require brute forcing, you can get the flag with one connection.


* Timing attack, measuring the time lookups take when passing in "f"

**Solution Script**
(May need to be run several times, since the timing lookup is not too accurate and a bit messy)

Flag: `dam{d0nT_d3l4y_th3_pRoC3sSiNg}`