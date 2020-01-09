# thepaper telegram bot

获取[澎湃新闻](https://www.thepaper.cn/)热点新闻资讯。

## 使用

机器人 URL：[澎湃新闻](https://t.me/thepapercn_bot)

频道 URL：[澎湃热点]( https://t.me/thepapercn )

频道每日 **8** 点及 **20** 点发送最新今日热点新闻。

## Bot 命令

- `/get_day` - **获取今日热点新闻**
- `/get_days` - 获取三天热点新闻
- `/get_week` - 获取这周热点新闻
- `/get_day_topic` - 获取今日热点话题
- `/get_days_topic` - 获取三天热点话题
- `/get_week_topic` - 获取这周热点话题
- `/get_comment` - **获取今日热评**
- `/get_answer`- **获取热点问答**

## 配置

- `Token`：机器人 TOKEN，通过`@BotFather`获取。
- `Allow_User`：执行特权命令的允许用户（如重启 Bot），元素为 UserID（在`getupdates`方式有效）。

## 说明

1. `getupdates`文件夹：使用 [getUpdates](https://core.telegram.org/bots/api#getupdates) 方式, 通过使用长轮询不断接受传入的更新（updates），返回更新对象数组。

2. `thepaper_bot`文件夹：使用 [Webhook](https://core.telegram.org/bots/api#setwebhook) 方式，当有请求发送到机器人，机器人将 POST 一个请求到 webhook url，POST 内包含请求的 JSON 数据。

   1. [设置 webhook](https://core.telegram.org/bots/api#setwebhook)：

      ```bash
      curl https://api.telegram.org/bot{TOKEN}/setwebhook?url={URL}
      ```

   2. [查看 webhook 信息](https://core.telegram.org/bots/api#getwebhookinfo)

      ```bash
      curl https://api.telegram.org/bot{TOKEN}/getwebhookinfo
      ```

   3. [删除 webhook](https://core.telegram.org/bots/api#deletewebhook)

      ```bash
      curl https://api.telegram.org/bot{TOKEN}/deletewebhook
      ```
      
3. 即时预览（Instant View）

   原始 URL：`https://www.thepaper.cn/newsDetail_forward_5442188`

   使用即时预览 URL：`https://t.me/iv?url=https://www.thepaper.cn/newsDetail_forward_5442188&rhash=71b085e544938c`
