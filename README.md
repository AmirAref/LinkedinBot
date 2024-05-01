# Linkedbot
a telegram robot that provides the details of the Linkedin.com posts

## Installation :
clone the repository and go to the repo directory, then do as following (you must have installed the [poetry](https://python-poetry.org/)):

install the requirements :  
```bash
poetry install
```

## Configuartion :  
you must to set up your custom configuration in the the [config.py](https://github.com/AmirAref/Linkedbot/blob/master/config.py)  
- `api_id` and `api_hash` : get your api detail from https://my.telegram.org/auth
- `bot_token` : get your robot token from [@BotFather](https://t.me/BotFather) (or if you don't have, make one there)
- `proxy` : the proxy is `None` by default but if you want to connect to the telegram with proxy, here is the proxy template that you can replace it with your data.
```python
 proxy = {
     "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
     "hostname": "11.22.33.44",
     "port": 1234,
     "username": "username",
     "password": "password"
 }
 ```

## Run :
finally run the program :
```bash
poetry run python -m LinkedinBot.bot
```


## TODO:
- [x] use poetry
- [x] change the telegram-bot client (python-telegram-bot)
- [ ] use pydantic settings (.env)
- [ ] add Dockerfile
- [ ] setup linter
- [ ] add tests
- [ ] use connection pooling