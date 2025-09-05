# chess-accounts-tracking
Since I have numerous chess.com accounts, all with different ratings, I want to know which account has which rating in order to bring them all more or less around the same level.
To do so, I created this litte project, here is how it works.
![Ups, no image available](./chess_projectscheme.png)

An EventBridge rule triggers a Lambda function everyday at 07:00 a.m.
The Lambda function calls the chess.com API to get the data of every account that I own. 
Once the Lambda function receives the data from the chess.com API, it creates 2 messages and sends them to a Telegram bot.
In order to have a cleaner bot chat, I also created a DynamoDB table where I store the IDs of the messages, in order to delete them just before sending the new ones.

This way, every morning I have an overview of my 80+ chess.com accounts just by opening telegram on my phone.
