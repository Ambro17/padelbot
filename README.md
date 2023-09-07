# PadelBot

Reporta partidos en progreso extraido desde https://www.padelfip.com/

## Como usar?
Hablarle a [@PremierPadelBot](https://t.me/PremierPadelBot) en telegram

## Como contribuir?
```bash
python3.10 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
export BOT_TOKEN=<your_bot_token>
python bot.py
```

## Como desplegar?
Yo elegí fly.io porque es gratis, es simple, y anda bien.
```bash
fly launch
fly secrets set BOT_TOKEN=<your_bot_token>
fly deploy
```
When testing locally you should run `fly scale count 0` 
to stop the remote bot as otherwise they conflict in a race condition for fetching new messages.
To use again the remote version, set `fly scale count 1`