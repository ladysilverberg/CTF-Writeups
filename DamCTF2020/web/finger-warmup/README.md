## web/finger-warmup
>A finger warmup to prepare for the rest of the CTF, good luck!
You may find this or this to be helpful.
finger-warmup.chals.damctf.xyz

```python=
import requests

def send_request(url_parameter):
    url = 'https://finger-warmup.chals.damctf.xyz/' + url_parameter
    response = requests.get(url)
    return response.content

running = True
parameter = 'un5vmavt8u5t5op1u94h'
while running:
    r = send_request(parameter)
    r = r.decode()
    if 'dam{' in r:
        print(r)
        running = False
    if 'click here, if you are patient enough I will give you the flag' in r:
        r = r.split('"')

````
Output: `Nice clicking, I'm very impressed! Now to go onwards and upwards! <br/><pre>dam{I_hope_you_did_this_manually}</pre>`

Python script which resursively visits the URLs until the flag is found.

Flag: `dam{I_hope_you_did_this_manually}`