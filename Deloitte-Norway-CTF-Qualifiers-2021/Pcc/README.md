## PCC100 - Geo Locations

*Writeup by Fredrik Magnussen*

initial domain given was a tcp:// link.

Connect via netcat:
hatman@caubeen:deloitte$ nc 136.243.68.77 17001

````

                                                                    ||
                                                  __..--".          ||
                                 __..--""`._..--"" . . . .`.        ||
                         __..--"". . . . . . .`. . . . . . .`.      ||
                 __..--"". . . . .`. . . . . . .`. . . . . . .`.   //
         __..--"". . `.  . . . . . .`. . . . . . .`. . . . . . .`.//
  _..--""  . . . . . . `.  . . . . . .`. . . . . . .`. . . . . . .||
:". . . .`.  . . . . . . `.  . . . . . .`. . . . . . .`. . . . . .||`.
`:. . . . .`.  . . . . . . `.  . . . . . .`. . . . . . .`. . . . .||__>
  `:. . . . .`.  . . . . . . `.  . . . . . .`. . . . . . .`.__..-o||
    `:. . . . .`.  . . . . . . `.  . . . . . .`. . . . .`;Y"->.  ""
      `:. . . . .`.  . . . . . . `.  . . . . . .`. . . __.>.:'
        `:. . . . .`.  . . . . . . `.  . . . . __..--"" ..+"`.
   _..-._ `:. . . . .`.  . . . . . . `.__..--"" ....:::::.|   `.
 ."`` \_--" >:. . . . .`.  . . __..,-|" . ..::::::::::::::`--""-:.
' ..`\J.-  "8-`:. . .  __..--"" ...-I  \ `. `::::::::::::::::::::".
`/'\\88o. ,O \  `:.--""....:|:::'''`'\ ='. }-._'::::::::::::::::::|
8  8|PP|"(:. \-" ""`:::::::|:::.((::='/ .\""-.:_ ':::::::::::''_.'  _..
 8  8|::/ \`::Y  _____`:::::|::::.\\[ .\ "/"..* *"-. '''__..--"")\,"".-.\_
`\b d/""===\==V::.--..__`:::|:::::.|,'*."".:.. "_-.*`.""    _.-"-""\? "_=``.
\\`".`"' .: :-.::.        `:|:::.'.'*.' __..--""   `.*`:--"".-"?,  .)=""`\ \\
 `.``...''_/   ``::      _\\--.'.'*.'-""   _..-._ _..>.*;-""@_.-/-" `\.-" "-.\
   `-::--"            .-"@"}.'.'*.:)     ."\` \ \`.--'_`-'     `\. \-'-""-   `.
                     <\  _...'*.'      .' \.`\ `\ \\""         `\ `' ' .-.\   |
                     _\"" .---'        -\. `\.-" "-.\           \`|    ._)/   '
                   ."\.`-"\`.         `\. \-'-""-   `.           \\  `---"   /
                 .' \.`\ `\ \\        `\ `' ' .-.\   |            `.       _/
                 -\. `\.-" "-.\        \`|    ._)/   '              `-..--"
                `\. \-'-""-   `.        \\  `---"   /
                `\ `' ' .-.\   |         `.       _/
                 \`|    ._)/   '           `-..--"
                  \\  `---"   /
                   `.       _/
         _ Seal _    `-..--"
````

Perseverance Distance Calculation Integrated Circuit

===== STATUS =====
    Temperature: -63 deg Celsius
    Current position: (x: 5081, y: 3532)
    Online time: 3 days, 10:00:38.836574

===== MAIN ROUTINE =====
[*] Navigating to new location
    New coordinates: (x: 8306, y: 8095)
    Enter distance in meters compared to original position:


If you respond to the query slowly (>1s) you get a timeout.

Script opens a TCP connection against the server, then receives data in multiple loops (server refuses to send out larger chunks.)

When the scripts sees "original position: ", we have reached the point where input is required.

We find the two points by using a regex that finds (x: [x], y: [y1]), with the two coordinate positions marked as a capture group. This allows us to easily iterate over the Returned Matches object and and pull out each coordinate.

We then do a simple 2d-distance calculation (sqrt((x2-x1)^2 + (y2-y1)^2)), and round the distance before sending it (with a trailing newline, to emulate enter.)

This loops many times, until the server responds with "validation successful" and the flag:

Awesome! Thanks for verifying our rover functionality.\nHere's a flag: CTF{2fe72454b43a0ab4603ff7c0c62fee3b}\n"

