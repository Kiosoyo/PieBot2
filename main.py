from bot import bot
from obj import Message


Bot = bot('ws://127.0.0.1:6700')
reg = Bot.reg
Bot.run()

