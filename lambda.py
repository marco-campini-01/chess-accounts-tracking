import os
import csv
import json
import boto3
import telebot
from io import StringIO
from chessdotcom import get_player_stats, Client

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)
table_name = os.environ.get('TABLE')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
my_accounts = [...]


def bot_send_message(msg):
    msg_id = bot.send_message(chat_id=xxxxxxxxx, text=msg).message_id
    table.put_item(Item={'pk': str(msg_id)})
        
def bot_del_messages():
    messages = get_message_ids()
    if messages:
        for msg_id in messages:
            bot.delete_message(chat_id=xxxxxxxxx, message_id=msg_id)
            table.delete_item(Key={'pk': str(msg_id)})
    
def get_message_ids():
    response = table.scan()
    return [int(msg_id['pk']) for msg_id in response['Items']]
    
    
def create_and_send_msg(my_chess_info_sorted_by_puzzle, my_chess_info_sorted_by_bullet, my_chess_info_sorted_by_blitz, my_chess_info_sorted_by_rapid):
    bot_del_messages()
    msg = "Puzzle Rush\n"
    for user in my_chess_info_sorted_by_puzzle:
        msg = msg + f'{user["Username"]}: {user["Puzzle Rush"]}\n'
    msg = msg + '\n Bullet\n'
    for user in my_chess_info_sorted_by_bullet:
        msg = msg + f'{user["Username"]}: {user["Bullet"]}\n'
    bot_send_message(msg)
    msg = 'Blitz\n'
    for user in my_chess_info_sorted_by_blitz:
        msg = msg + f'{user["Username"]}: {user["Blitz"]}\n'
    msg = msg + '\n Rapid\n'
    for user in my_chess_info_sorted_by_rapid:
        msg = msg + f'{user["Username"]}: {user["Rapid"]}\n'
    bot_send_message(msg)

def lambda_handler(event, context):
    Client.request_config["headers"]["User-Agent"] = (
        "Just checking my rating."
    )
    my_chess_info = []
    for acc in my_accounts:
        response = get_player_stats(acc)
        puzzle_score = response.stats.puzzle_rush.best.score
        bullet_rating = response.stats.chess_bullet.last.rating
        try:
            blitz_rating = response.stats.chess_blitz.last.rating
        except:
            blitz_rating = 0
        try:
            rapid_rating = response.stats.chess_rapid.last.rating
        except:
            rapid_rating = 0;
        my_chess_info.append({"Username": acc, "Puzzle Rush": puzzle_score, "Bullet": bullet_rating, "Blitz": blitz_rating, "Rapid": rapid_rating})
    
    my_chess_info_sorted_by_puzzle = sorted(my_chess_info, key=lambda x: x["Puzzle Rush"])
    my_chess_info_sorted_by_bullet = sorted(my_chess_info, key=lambda x: x["Bullet"])
    my_chess_info_sorted_by_blitz = sorted(my_chess_info, key=lambda x: x["Blitz"])
    my_chess_info_sorted_by_rapid = sorted(my_chess_info, key=lambda x: x["Rapid"])
    create_and_send_msg(my_chess_info_sorted_by_puzzle, my_chess_info_sorted_by_bullet, my_chess_info_sorted_by_blitz, my_chess_info_sorted_by_rapid)
