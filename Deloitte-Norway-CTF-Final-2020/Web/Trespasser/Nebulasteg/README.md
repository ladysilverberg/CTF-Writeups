## WEB600 - Trespasser (Nebulasteg)
The challenge text mentions something juicy hidden in the clouds. Looking at the background in the game, we can see a galaxy with clouds. This is an image, and given the name of the task attempting some steganography techniques on this background image is likely the way to go.

![](https://i.imgur.com/B7vM40U.jpg)

After looking through color channels individually, check data in the LSB and running zSteg, binwalk and foremost we decided to run steghide. This show that a hidden txt file is hidden in the file.
Running *steghide extract -sf [file]* with a blank password extracts a text file with the flag.

Flag: `CTF{25285d3dc03b626eb7ea85dbd1e01c25}`