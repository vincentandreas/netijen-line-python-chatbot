# Netijen Indonesia Line Chatbot

![Alt text](blob/netijen.jpg?raw=true)

Inspired by Indonesian’s netizen behavior
Built using python Flask and Linebot SDK

Chatbot Features:

* Send sample meme image

* Search gossip news using carousel template, with two type, top gossip, and search gossip by artist name / topics, using Newsapi to search entertainment news in Indonesia.
* Send unique fact about blood type using carousel template.
* Handle error command using fallback message.
* Send spam message for entertainment purpose.

Example 
![Alt text](blob/feature.jpg?raw=true)
![Alt text](blob/gossip-news.jpg?raw=true)
How to use

1. Create account in [Newsapi](https://newsapi.org/) to get access key
2. Create account in [Line Developer](https://developers.line.biz/en/), add new channel and chatbot, to get Channel Access Token and Channel Secret.
3. Deploy code in server, you can use [Heroku](https://www.heroku.com/) or other service. Then copy the callback url (e.g. https://xxx.herokuapp.com/callback) to line webhook in Line developer
4. Try to add the chatbot and test the chatbot in Line.


