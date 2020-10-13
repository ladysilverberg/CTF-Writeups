## misc/electric-bovine
>Do androids dream of electric bovine? Find out on my new Discord server!

Discord API reference: https://discordpy.readthedocs.io/en/latest/api.html

* Bot Source Code at https://gist.github.com/dunklastarn/d3e3ca30bb4f476221bf42faebb19a12#file-bot_source-py-L221

Solution:
* Looking at authenticate(), send_msg() and role_add() in the source code of the bot, we can see that we can send messages to the #botspam channel. We can also calculate the results of authenticate() and manipulate our own nickname.
* DMing "!send_msg !role_add 000[your user id goes here]0 000[role id of 'private' role + (your user discrimatior * 4) goes here]0" to the bot grants private role permissions when nickname is set to private. We now have access to use the !cowsay command.

```python=
for char in arg:
    if char in " `1234567890-=~!@#$%^&*()_+[]\\{}|;':\",./?":
        await message.author.send("Invalid character sent. Quitting.")
        return

cow = "```\n" + os.popen("cowsay " + arg).read() + "\n```"

await message.author.send(cow)
````
* os.popen() is vulnerable to arbitrary code execution if the character filter can be bypassed. We note that the "<" character is not filtered!
* Messaging "!cowsay <flag" to the bot will pipe the contents of the file called flag into cowsay, and the flag gets printed by the bot:

```
 __________________________
< dam{discord_su_do_speen} >
 --------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
````
Flag: `dam{discord_su_do_speen}`
