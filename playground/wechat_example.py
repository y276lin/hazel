# coding: utf-8
from __future__ import unicode_literals

from wxpy import *

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

my_friend = bot.friends().search('无敌可爱小仙女')[0]
print(my_friend)


@bot.register(my_friend)
def reply_my_friend(msg):
    print(msg)

    if msg.type == MessageTypes['TEXT']:
        if msg.text == 'lg':
            bot.logout()
        else:
            return 'received: {} ({})'.format(msg.text, msg.type)
    elif msg.type == MessageTypes['RECORDING']:
        print(msg.file_name)
        msg.get_file(save_path=msg.file_name)
        return 'received: {} ({} {} ms)'.format(msg.text, msg.type, msg.voice_length)
    else:
        return "Unknown message type"


bot.join()
