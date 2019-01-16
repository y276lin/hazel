# coding: utf-8
from __future__ import unicode_literals

from wxpy import *
from hazel import wechat_send_message
import traceback
import logging

MessageTypes = {
    # 文本
    "TEXT": 'Text',
    # 位置
    "MAP": 'Map',
    # 名片
    "CARD": 'Card',
    # 提示
    "NOTE": 'Note',
    # 分享
    "SHARING": 'Sharing',
    # 图片
    "PICTURE": 'Picture',
    # 语音
    "RECORDING": 'Recording',
    # 文件
    "ATTACHMENT": 'Attachment',
    # 视频
    "VIDEO": 'Video',
    # 好友请求
    "FRIENDS": 'Friends',
    # 系统
    "SYSTEM": 'System',
}

bot = Bot(cache_path=True)

my_friend = bot.friends().search('坚强嘟')[0]
print(my_friend)


@bot.register(my_friend)
def reply_my_friend(msg):
    if msg.type != MessageTypes['TEXT']:
        return 'Only Text is supported for now'

    if msg.text.lower() == 'tingzhi':
        print('>>> Stop requested')
        bot.stop()
        return '-'
    elif msg.text.lower() == 'tuichu':
        print(">>> Log out requested")
        bot.logout()
        return '-'
    else:
        try:
            ress = wechat_send_message(msg.text)
            for res in ress:
                my_friend.send(res)
        except Exception as e:
            print(e)
            logging.error(traceback.format_exc())

bot.join()
