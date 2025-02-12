# mp4-to-gif-telegram-bot

Can convert .mp4 to .gif

## Requirements

* `FFmpeg`
* `Python` 3.6+

## Installation 

```sh
git clone https://github.com/nuckle/mp4-to-gif-telegram-bot
cd mp4-to-gif-telegram-bot
```

Install dependencies


```sh
pip install -r requirements.txt
```

Run the bot

```sh
cd src/
python main.py
```

## Docker setup

You can use `docker compose` to run this bot

```sh
cp docker-compose.example.yaml docker-compose.yaml
docker compose up
```


## Configuration

1. Create `.env`  file in the project root and add your bot token from  [@BotFather](https://t.me/BotFather)

```
TG_TOKEN=1234567890:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

2. (Optional) Customize the storage directory for media files by setting the `FOLDER` variable in the `.env` file:

```
FOLDER=media/
```
