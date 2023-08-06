<p align="center">
   <a href="https://github.com/Octra">
   </a>
</p>
<h1 align="center">
   <b> Octra Telegram Library </b> <br>  

</h1>

 * [![PyPI - Version](https://img.shields.io/pypi/v/Octra?style=round)](https://pypi.org/project/Octra) 
[![PyPI - Downloads](https://img.shields.io/pypi/dm/Octra?label=DOWNLOADS&style=round)](https://pypi.org/project/Octra) 

----

<b>About:</b> Octra is a Telegram Python Library mainly used for users and bots

<h4> Installation </h4>

```python
pip3 install Octra
```

<h4> Import functions </h4>

``` python
from Octra import <functions name>
```


<h4> Example </h4>

```python
from Octra import Veteran, Flow

app = Veteran("my_account")


@app.on_message(Flow.private)
async def hello(client, m):
    await m.reply("Hello from Octra.")


app.run()
```
 > [Click Here](https://github.com/Octra/Octra/tree/main/Octra/functions#-functions-available-) </b>