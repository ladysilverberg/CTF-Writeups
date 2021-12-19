## WEB75 - Information Disclosure

The challenge presented a website called Scrabble. It had a text input field where whatever input provided would be sent as a request to an endpoint asynchronously a the route /lookup. If more than 7 characters were provided, a message telling that too many characters are provided would be returned. Otherwise, an array telling which words could be made up from these letters would be returned.

None of this gives any tangible information. However, visiting https://29e94c4b474b08e40127008f14e392ea.challenge.hackazon.org/lookup reveals some source code:

```python=
File ./chall.py, line 23, in login
    17   def login():
 (...)
    19           if "letters" in request.args and len(request.args['letters']) > 7:
    20               return ret("toomany")
    21
    22           scrabble.connect(config.api_url, config.api_key, config.api_secret)
--> 23           letters = request.args['letters']
    24           possibilities = scrabble.lookup(letters)
    ..................................................
     request.args = ImmutableMultiDict
                    {}
     scrabble.connect = <function 'connect' scrabble.py:42>
     config.api_url = 'http://172.17.0.9:6000/ScrabbleService.wsdl'
     config.api_key = 'SCRAB_9uE3F5cKMy'
     config.api_secret = 'gghG00jaTYXA7UWCRHSlMs6kGjevmIGXV82IlIYJ'
     scrabble.lookup = <function 'lookup' scrabble.py:35>
    ..................................................

File /usr/local/lib/python3.6/dist-packages/werkzeug/datastructures.py, line 442, in getitem
    430  def getitem(self, key):
 (...)
    438      if key in self:
    439          lst = dict.getitem(self, key)
    440          if len(lst) > 0:
    441              return lst[0]
--> 442      raise exceptions.BadRequestKeyError(key)
    ..................................................
     self = ImmutableMultiDict
            {}
     key = 'letters'
     exceptions.BadRequestKeyError = <class 'werkzeug.exceptions.BadRequestKeyError'>
    ..................................................

BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.
````

Looking at the source code, we see a secret API key `gghG00jaTYXA7UWCRHSlMs6kGjevmIGXV82IlIYJ` being leaked and providing this as the flag solves the challenge.
