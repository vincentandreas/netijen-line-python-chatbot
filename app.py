from flask import Flask, request, abort
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import requests

app = Flask(__name__)

access_key = json.load(open('accessKey.json'))

line_bot_api = LineBotApi(access_key['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(access_key['CHANNEL_SECRET'])

user_manual = "Supaya bisa ngasih perintah ke gw, *awali* dengan tanda seru '!' boleh ngespam juga\nKetik !meme untuk dapetin meme baru\n!fakta unik untuk melihat fakta golongan darah lu\n!top gosip untuk melihat gosip terbaru\n!gosip <nama artis> untuk mencari gosip artis terbaru. Misal !gosip atta halilintar\n!sepi untuk ramein\n!info kalo lupa keyword"

def cut_text(text, maxLength):
    start_index = maxLength -5
    index = -1
    while index == -1:
        index = text.find(' ' , start_index,maxLength)
        start_index -= 5
        if start_index <= 0:
          index = maxLength
          break          
    return text[:index]

def generate_news_carousel(url, altText):
    response = requests.get(url)
    jsonObj = response.json()
    list_carousel = []
    for i, articles in enumerate(jsonObj['articles']):
        carousel = CarouselColumn(
            thumbnail_image_url = articles['urlToImage'],
            title = cut_text(articles['title'],40),
            text = cut_text(articles['description'],60),
            actions=[
                URIAction(
                    label='Baca',
                    uri= articles['url']
                )
            ]
        )
        list_carousel.append(carousel)
        if i == 6:
            break

    if len(list_carousel) == 0:
        message = TextSendMessage(text="maaf, gw gak nemu")
    else:
        message = TemplateSendMessage(
            alt_text='Berita',
            template = CarouselTemplate(
                columns =list_carousel
            )
        )
    return message

def generate_spam():
    text = open('spamText.txt')
    return text.read()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    greeting = 'makasi udah temenan sama gw\n'
    message = TextSendMessage(text=greeting + user_manual)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(JoinEvent)
def handle_follow(event):
    greeting = 'makasi udah undang gw\n'
    message = TextSendMessage(text=greeting + user_manual)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(LeaveEvent)
def handle_follow(event):
    message = TextSendMessage(text='kurang ajar kalian, uda kick gw')
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    message = TextSendMessage(text='makin seru nih ngerumpi nya, welcome')
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = None
    message_list = event.message.text.split(' ')
    url = 'http://newsapi.org/v2/top-headlines?country=id&category=entertainment&apiKey=' + access_key['NEWS_API_KEY']
    if event.message.text == '!info':
        message = TextSendMessage(text=user_manual)

    elif event.message.text == '!top gosip':        
        message = generate_news_carousel(url,'top gosip hari ini')

    elif len(message_list) > 1 and message_list[0] == '!gosip':
        queryStr = message_list[1]
        if len(message_list) > 2:
            for query in message_list[2:]:
                queryStr += '%20' + query
        query_url = url + '&q=' +   queryStr 
        message = generate_news_carousel(query_url ,'gosip yang lu cari')
        
    elif event.message.text == '!meme':
        message = ImageSendMessage(
    original_content_url='https://assets.beepdo.com/wp-content/uploads/2020/05/08174609/meme-lucu-tetangga-1.jpg',
    preview_image_url='https://assets.beepdo.com/wp-content/uploads/2020/05/08174609/meme-lucu-tetangga-1.jpg'
    )

    elif event.message.text == '!fakta unik':
        message = TemplateSendMessage(
            alt_text='fakta unik golongan darah',
            template=CarouselTemplate(
                columns=[
                   CarouselColumn(
                        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Fablood.jpg?alt=media&token=9a5f6e7d-396f-4dfd-ab27-e48016b71b92',
                        title='Golongan A',
                        text='Golongan A',
                        actions=[
                            MessageAction(
                                label='Pilh',
                                text='!GolA'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Fbblod.jpg?alt=media&token=aff54303-cc10-4c7c-9525-383ac4f93073',
                        title='Golongan B',
                        text='Golongan B',
                        actions=[
                            MessageAction(
                                label='Pilh',
                                text='!GolB'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Fabblood.jpg?alt=media&token=e97d1369-015a-41db-bfd4-4ff8b22a586b',
                        title='Golongan AB',
                        text='Golongan AB',
                        actions=[
                            MessageAction(
                                label='Pilh',
                                text='!GolAB'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Foblood.jpg?alt=media&token=daf91a58-564d-487d-a20d-ba45a7e4fb6b',
                        title='Golongan O',
                        text='Golongan O',
                        actions=[
                            MessageAction(
                                label='Pilh',
                                text='!GolO'
                            )
                        ]
                    )
                ]
            )
        )
    elif event.message.text == '!GolA':
        message = TextSendMessage(text='dari hasil gw googling, gw menemukan bahwa gol darah A memiliki risiko lebih tinggi terkena penyakit kardiovaskular sebanyak lima persen, dan memiliki kemungkinan 10 persen lebih besar terkena diabetes tipe 2. HAYOLOH!!!')
    elif event.message.text == '!GolB':
        message = ImageSendMessage(original_content_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Fbbebas.jpg?alt=media&token=ab560921-ee87-43a7-9727-8c606d6c7cb1', preview_image_url='https://firebasestorage.googleapis.com/v0/b/sunib-hackathon-service.appspot.com/o/vincent%2Fbbebas.jpg?alt=media&token=ab560921-ee87-43a7-9727-8c606d6c7cb1'
    )
    elif event.message.text == '!GolAB':
        message = TextSendMessage(text='lu bisa tenang, karena gol darah AB adalah resipien universal. jadi kalau lu kecelakaan, dan kekurangan darah, bisa nerima darah dari golongan darah apapun!! selamat ya')

    elif event.message.text == '!GolO':
        message = TextSendMessage(text='selamat, lu ditakdirin buat berbagi darah, karena lu termasuk donor universal')

    elif event.message.text == '!sepi':
        message = TextSendMessage(text=generate_spam())
    elif event.message.text[0] == '!':
        message = TextSendMessage(text="kyknya salah ketik keyword deh.. coba ketik '!info'")
    if message != None:
        line_bot_api.reply_message(event.reply_token, message)
    

@handler.add(JoinEvent, message=TextMessage)
def handle_join(event):
    message = TextSendMessage(text="Terima kasih sudah nambahin gw!!!")
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
