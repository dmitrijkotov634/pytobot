# pytobot
Turns any script into a telegram bot
 
![pypi](https://badge.fury.io/py/pytobot.svg)
 
## Install
`pip install --upgrade pytobot`
 
## Usage
*Script*:
```python
while True:
    message = input()
    if message == "/hello":
        print("Hello, world!")
```

*Console*:
```console
$ pytobot script.py -t TOKEN
```