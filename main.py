from Clases import *
from data import *
import asyncio, time, logging, schedule,handlers
from telethon import TelegramClient
from telethon.sessions import StringSession


a= lambda: loop.create_task(handlers.check_schedule())

list=[]

time.asctime()
loop = asyncio.get_event_loop()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

async def me(list):
    await asyncio.sleep(5)
    for client in list:
        await client.send_message('chtwrsbot',"🏅Me")

# Clientes 
bots=TelegramClient(StringSession(bot_string_session), api_id, api_hash)

bot_alejandro=TelegramClient(StringSession(bot_alejandro_string_session), api_id, api_hash)

bot_dariel=TelegramClient(StringSession(bot_dariel_string_session), api_id, api_hash)

yo = TelegramClient(StringSession(naldo_string_session), api_id, api_hash)

dariel = TelegramClient(StringSession(dariel_string_session), api_id, api_hash)

#detlaf = TelegramClient(StringSession(detlaf_string_session), api_id, api_hash)

#atomox = TelegramClient(StringSession(atomox_string_session), api_id, api_hash)

#void = TelegramClient(StringSession(void_string_session), api_id, api_hash)

alejandro = TelegramClient(StringSession(alejandro_string_session), api_id, api_hash)

all_bots = [bots,bot_alejandro,bot_dariel]
all_client = [yo,dariel,alejandro]

#referencia en consola
print(time.asctime(), '-', 'Auto- deploy....')

#events handlers
for client in all_client:
    client.add_event_handler(handlers.handle_updateMe)
    client.add_event_handler(handlers.Handle_Do_quest)
    client.add_event_handler(handlers.handle_Full_Stamina)
    client.add_event_handler(handlers.handle_stam_deplete)
    client.add_event_handler(handlers.handle_pldege_accept)
    client.add_event_handler(handlers.handle_Stop_Foray)
    client.add_event_handler(handlers.handle_trader)
    client.add_event_handler(handlers.handle_mobs)
    client.add_event_handler(handlers.handle_bichos_hunt)
    client.add_event_handler(handlers.handle_ambush_hunt)
    client.add_event_handler(handlers.handle_if_alive)
    client.add_event_handler(handlers.handle_if_death)
    client.add_event_handler(handlers.handle_evento_hunt)
    #client.add_event_handler(handlers.compras_auction)
    #client.add_event_handler(handlers.bets_auction)
    #client.add_event_handler(handlers.auto_OB_auction)
    #client.add_event_handler(handlers.auto_pogs)
    #client.add_event_handler(handlers.validar_pogs)


#bot handlers
for bot in all_bots:
    bot.add_event_handler(handlers.handle_StartBot)
    bot.add_event_handler(handlers.handle_status_bot)
    bot.add_event_handler(handlers.handle_suscrip_bot)
    bot.add_event_handler(handlers.handle_config_bot)
    bot.add_event_handler(handlers.handle_quest_bot)
    bot.add_event_handler(handlers.handleButtomBot1)
    bot.add_event_handler(handlers.handle_mobs_bot)
    bot.add_event_handler(handlers.handleButtomBot)
    #bot.add_event_handler(handlers.handle_quest_change_bot)
    #bot.add_event_handler(handlers.handle_hunt_on_bot)
    #bot.add_event_handler(handlers.handle_hunt_off_bot)
    #bot.add_event_handler(handlers.handle_ayudaMobs_chat_bot)
    #bot.add_event_handler(handlers.handle_removeMobs_chat_bot)
    bot.add_event_handler(handlers.handle_set_arena_time_bot)
    bot.add_event_handler(handlers.handle_go_bot)
    bot.add_event_handler(handlers.handleButtomBot2)
    #bot.add_event_handler(handlers.handle_set_trader_id_bot)
    bot.add_event_handler(handlers.handle_auction_bot)
    bot.add_event_handler(handlers.handleButtomBot3)
    bot.add_event_handler(handlers.handle_pogs_bot)
    bot.add_event_handler(handlers.handleButtomBot4)




#inicio clientes

print('Registrando clientes')
try:
    bots.start()
except: print('bots fallo')
'''try:
    bot_alejandro.start()
except: print('bot_alejandro fallo')
try:
    bot_dariel.start()
except: print('bot_dariel fallo')'''

try: 
    yo.start()
    loop.create_task(handlers.register(yo,quest=True,craft=True,arena=True,go=True,auction=True,hunt=True,pogs=True,scroll=True,orden=True,ranger=False,admin=True))
        
except: print('Fallo de cliente 1')

try: 
    dariel.start()
    loop.create_task(handlers.register(dariel,quest=True,craft=True,arena=True,go=True,auction=True,hunt=True,pogs=True,scroll=True,orden=True,ranger=False,admin=True))
        
except: print('Fallo de cliente 2')

try: 
    alejandro.start()
    loop.create_task(handlers.register(alejandro,quest=True,craft=True,arena=True,go=True,auction=True,hunt=True,pogs=True,scroll=True,orden=True,ranger=False,admin=True))
        
except: print('Fallo de cliente 3')

loop.create_task(handlers.scheduleArenas())
loop.create_task(me(all_client))

a()


yo.run_until_disconnected()

print(time.asctime(), '-', 'Stopped!')