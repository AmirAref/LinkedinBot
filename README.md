# Linkedin Bot
a telegram robot that uploads media from the Linkedin.com posts into telegram.


# Installation :
this project has been dockerized and you can easily run and dploy it using docker.

so first of all, clone the repository and go to the repo directory, then do as following :


## Configuartion :  
before running the robot, you must to set the environment variables in `.env` file. so to do this you copy the `.env-sample` file to `.env` and fill out with your data.
```bash
cp .env-sample .env
```

## Run Method 1 (Docker) :
to run the robot using docker, just run the docker compose with following command (you must have installed the [docker](https://docs.docker.com/engine/install/)):
```bash
docker compose up --build -d
```

> [!NOTE]
    the `-d` flag will run the container in deattached mode, so if you don't want this, remove it.


## Run Method 2 (Manually) :
in this method you have install the dependencies and run the robot manually.
so first install the requirements using poetry (you must have installed the [poetry](https://python-poetry.org/)):  
```bash
poetry install
```
<!-- - `api_id` and `api_hash` : get your api detail from https://my.telegram.org/auth
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
 ``` -->
 
and then run the program :
```bash
poetry run python -m LinkedinBot.bot
```
<br>

<!-- CONTRIBUTING -->

## Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:
### Report Bugs

Report bugs at [issues page][repo-url]

If you are reporting a bug, please include:
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

### Implement Features
Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

<!--
### Write Documentation

Linkedin Bot could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.
-->

### Submit Feedback
The best way to send feedback is to file an issue at [issues page][repo-url].

If you are proposing a new feature:
- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)


<!-- LICENSE -->

## License

Distributed under the GPL-V3 License. See [`LICENSE`](./LICENSE) for more information.


## TODO:
- [x] use poetry
- [x] change the telegram-bot client (python-telegram-bot)
- [x] use pydantic settings (.env)
- [x] add Dockerfile
- [ ] add logs
- [ ] setup linter
- [ ] add tests
- [ ] use connection pooling



[repo-url]: https://github.com/AmirAref/LinkedinBot/issues
