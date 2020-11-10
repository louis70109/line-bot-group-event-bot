# LINE Bot Group API example(Unsend/Join/Leave), Chatroom(VideoComplete/Webhook)

This is a group/room demo bot.


# Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Webhook API routing:

- Version 1 (just `echo` and `upgrade`): /v1/webhooks/line
- Version 2: /v2/webhooks/line

# Trigger words

## 在群組(Group)/聊天室(Room)

- 群組資訊/聊天室資訊
- 我是誰
- 你走吧

> Nedd to invite chatbot into Group/Room.

## Chatroom

- If `v1` version:
  - Type `v2` to use webhook event migration.
- Type `video` to receive video, when watch complete you would get a message(Video Completed Event).

# Screenshot

![](https://i.imgur.com/4rMMe7Pm.png)

---

![](https://i.imgur.com/fBGAqpmm.png)

---

![](https://i.imgur.com/jFipsAJm.png)

# Developer Side

## LINE account

- Got A LINE Bot API developer account
  Make sure you already registered, if you need use LINE Bot.

- Go to LINE Developer Console
  - Close auto-reply setting on "Messaging API" Tab.
  - Setup your basic account information. Here is some info you will need to know.
    - Callback URL: `https://{NGROK_URL}/v1/webhooks/line`
    - Verify your webhook.
    - Enable bot join group button.
- You will get following info, need fill back to `.env` file.
  - Channel Secret
  - Channel Access Token (You need to issue one here)

## Localhost

1. first terminal window:

```
pip install -r requirements.txt --user
python api.py
```

2. Created a provisional Https:

```
ngrok http 5000
```

or maybe you have npm environment:

```
npx ngrok http 5000
```

![](https://i.imgur.com/azVdG8j.png)

3. Copied your ngrok url to:
   - `.env` MY_DOMAIN environment property.
   - LINE developer page and `Enabled` join group button:

![](https://i.imgur.com/8jU9CMM.png)

4. Joined bot in your `Group`/`Room`!

# License

MIT License
