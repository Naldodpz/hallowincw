from gc import callbacks
from Clases import *
import re
from telethon.client import messages
from settings import *
from patterns import *
import asyncio, schedule,pickle
from random import randint, choice, random
from telethon import events, types, Button

stats={}

schedule1 = schedule.Scheduler()
loop = asyncio.get_event_loop()


#def llamables
#info players
def getInfoFromMe(st):
    player=None
    Level=0
    HPmax=0
    HP=0
    Staminamax=0
    Stamina=0
    Manamax=0
    Mana=0
    Oro=0
    if 'minute!' in st:
        f=re.findall(r'\d+',st)
        nombre=re.search('(?<=minute!)\D+',st)
        result1=nombre.group(0).split()
        player=result1[0]
    elif 'minutes!' in st:
        f=re.findall(r'\d+',st)
        nombre=re.search('(?<=minutes!)\D+',st)
        result1=nombre.group(0).split()
        player=result1[0]

    idx = st.find("🏅Level: ")
    idy = st.find("\n")
    text = st[idx + 9:idx +12]
    chars='*'
    Level = text.translate(str.maketrans('','',chars))
    
    idx = st.find("❤️Hp: ")
    idy = st.find("Stamina: ")
    subs = st[idx+6:idy-1]
    
    HP = (int)(subs.split("/")[0])
    HPmax = (int)(subs.split("/")[1])

    idx = st.find("Stamina: ")
    idy = st.find("⏰",idx)
    if idy == -1:
        idy = st.find("\n",idx)
    subs = st[idx+9:idy]
    
    Stamina = (int)(subs.split("/")[0])
    Staminamax = (int)(subs.split("/")[1])

    idx = st.find("Mana: ")
    if idx == -1:
        idx = st.find("💰")
        idy = st.find("👝")
        Oro = st[idx+1:idy-1]
    else:
        idx = st.find("Mana: ")
        idy = st.find("💰")
        subs = st[idx+6:idy-1]

        Mana = (int)(subs.split("/")[0])
        Manamax = (int)(subs.split("/")[1])

            

        idx = st.find("💰")
        idy = st.find("👝")
        Oro = st[idx+1:idy-1]

    return[player,Level,HPmax,HP,Staminamax,Stamina,Manamax,Mana,Oro]
#info players end

#start arenas
def startArenas(cliente): #control de arenas
    loop.create_task(doArenas(cliente))
#start arenas end

#mensajes de menu
def msg_quest(id):#msg del menu quest
    stat = stats[id]
    listEvents = stat.favQuest
    msg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n🤖Configuracion quest:\n..............................\n'
    if stat.fullquest:
        msg+= 'AutoQuest: ✅\n'
    if stat.fullquest == False:
        msg+= 'AutoQuest: ❌\n'
    if stat.forest:
        msg+= 'Lugar Quest: 🌲Forest\n'
    if stat.swamp:
        msg+= 'Lugar Quest: 🍄Swamp\n'
    if stat.valley:
        msg+= 'Lugar Quest: 🏔Valley\n'
    if stat.foray:
        msg+= 'Lugar Quest: 🏇Foray\n'
    if stat.random:
        msg+= 'Lugar Quest: 🎲Random\n\n'
    if stat.forest:
        msg+='🌲Forest 🏎\n🍄Swamp\n🏔Mountain Valley\n🏇Foray\n🎲Random\n\n'
    if stat.swamp:
        msg+='🌲Forest\n🍄Swamp 🏎\n🏔Mountain Valley\n🏇Foray\n🎲Random\n\n'
    if stat.valley:
        msg+='🌲Forest\n🍄Swamp\n🏔Mountain Valley 🏎\n🏇Foray\n🎲Random\n\n'
    if stat.foray:
        msg+='🌲Forest\n🍄Swamp\n🏔Mountain Valley\n🏇Foray 🏎\n🎲Random\n\n'
    if stat.random:
        msg+='🌲Forest\n🍄Swamp\n🏔Mountain Valley\n🏇Foray\n🎲Random 🏎\n\n'
    
    return msg

def msg_hunt(id):#msg del menu hunt
    stat = stats[id]
    msg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🤖Configuracion de mobs:\n..............................\n'
    if stat.mobs:
        msg+= '👾Estado: Cazando🏇✅\n'
    else:
        msg+= '👾Estado: De vago🏇❌\n'
    if stat.grouphunter == []:
        msg+= '👂De chismoso en todas partes🌎\n'
    else:
        msg+= '👂De chismoso en: %s👂\n' %(stat.grouphunter)
    if stat.mobrenvio == []:
        msg+= '💪Yo estoy duro, no necesito ayuda🦾'
    else:
        msg+= '👨‍🦽De penco en: %s\n\n' %(stat.mobrenvio)
    
    return msg

def msg_go(id):#msg del menu go
    stat = stats[id]
    msg ='🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🤖Configuración del Go:\n..............................\n'
    if stat.gointervine:
        msg+= '⚔️intervine: ✅\n'
    else:
        msg+= '🏖intervine: ❌\n'
    if stat.trader:
        msg+= '💸trader: ✅\n'
    else:
        msg+= '🤦‍♂️trader: ❌\n'
    msg+= 'Recurso ID: %s\n' %(stat.traderId)
    if stat.pledge:
        msg+= '🤌🏻pledge: ✅\n'
    else:
        msg+= '😴pledge: ❌\n'
    return msg

def msg_auction(id):#msg del menu auction
    stat = stats[id]
    msg ='''
    🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
    🤖Configuración del Auction:
    ..............................
            
    Lista de suscripciones y precios:
            
    %s
            
    Lista de lotes en vigilancia:
            
    %s
            
    🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹''' %(stat.compras,stat.lots)
    return msg

def msg_pogs(id):#mensaje del menu pogs
    stat=stats[id]
    oro=stat.maxpog*120
    thre=stat.maxpog*12
    leath=stat.maxpog*2
    msg = '''🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
    🤖Configuración Auto Pogs:
    ..............................\n'''
    if stat.autopogs:
        msg+= 'Craft Automatico de pogs: ON✅\n'
    else:
        msg+= 'Craft Automatico de pogs: OFF❌\n'
    msg+='Cantidad minima de pogs a craftear: %s\n**Oro necesario:** %s💰\n**Thread requeridos:** %s🧵\n**Leather requerido:** %s🥓\n\n' %(stat.maxpog,str(oro),str(thre),str(leath))
    msg+= '(Trate siempre de tener las cantidades minimas sugeridas, de no hacerlo, puede generar gastos de oro no deseados)\n\nSe recomienda tener fijado el minimo por encima del limite predeterminado, pudiera generarse un bucle molesto'
    return msg

#mensajes de menu end

#bloque async
#info y registro player
async def register(client,quest=False,craft=False,arena=False,go=False,auction=False,hunt=False,pogs=False,scroll=False,orden=False,ranger=False,admin=False):
    global stats
    user = await client.get_me()
    stats[user.id] = clasePlayer(cuenta=client,quest=quest,craft=craft,arena=arena,go=go,auction=auction,hunt=hunt,pogs=pogs,scroll=scroll,orden=orden,ranger=ranger,admin=admin)
    print('registro de %i' %user.id)
    

async def getId(client):
    user = await client.get_me()
    return user.id

async def basic_info(client, text, order):
    me = await client.get_me()
    print(me.username)
    print(text)
    print(order)
    print('\n\n\n')

#handlers script
@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def handle_updateMe(event):
    if '🌟Congratulations! New level!🌟' in event.message.text: 
        me=getInfoFromMe(event.message.text)
        id = await getId(event.client)
        stat = stats[id]
        stat.player=me[0]
        stat.lvl=me[1]
        stat.Maxhp=me[2]
        stat.hp=me[3]
        stat.Maxstamina=me[4]
        stat.stamina=me[5]
        stat.Maxmana=me[6]
        stat.mana=me[7]
        stat.oro=me[8]
        

'''BLOCK ARENAS Y AIMING'''

async def doArenas(client):
    await client.send_message('chtwrsbot', '▶️Fast fight')
    await asyncio.sleep(randint(350, 400))
    await client.send_message('chtwrsbot', '▶️Fast fight')
    await asyncio.sleep(randint(350, 400))
    await client.send_message('chtwrsbot', '▶️Fast fight')
    await asyncio.sleep(randint(350, 400))
    await client.send_message('chtwrsbot', '▶️Fast fight')
    await asyncio.sleep(randint(350, 400))
    await client.send_message('chtwrsbot', '▶️Fast fight')

async def scheduleArenas():
    global schedule1
    await asyncio.sleep(20)
    for scripter in stats:
        if stats[scripter].arena:
            stats[scripter].arenaDeamon = schedule1.every().day.at(stats[scripter].arenaTime).do(startArenas, client=stats[scripter].cuenta)
            print('Las Arenas empezaran a las %s' %stats[scripter].arenaTime)

async def check_schedule():
    while True:
        schedule1.run_pending()
        await asyncio.sleep(2)
'''BLOCK ARENAS Y AIMING END'''

'''pogs'''
async def craft_pogs(element,client):
    id = await getId(client)
    stat = stats[id]
    i=0
    if stat.mana > 0:
        mn=int(stat.mana)//10
        man=round(element)
        if mn>=element:
            await asyncio.sleep(3)
            await client.send_message("@chtwrsbot",'/c_100 '+ str(man))
    else:
        while i<element:
            i+=1
            await asyncio.sleep(3)
            await client.send_message("@chtwrsbot",'/c_100')

#FULL STAMINAS
@events.register(events.NewMessage(from_users=cw_id, pattern=full_stamina_pattern, incoming=True))
async def handle_Full_Stamina(event):     
    id = await getId(event.client)
    stat = stats[id]
    if stat.quest and stat.fullquest:
        await event.respond("🗺Quests") 

@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def handle_stam_deplete(event):      
    msg = event.message
    if ("You received:" in msg.message and "stands victorious over" not in msg.message) or "It was a really nice and sunny day," in msg.message or "Looking at the overcast sky you decide to take a day off" in msg.message or "You fell asleep and in your dream there was a" in msg.message or "Walking through the swamp, you found yourself surrounded by" in msg.message or "As you were about to head out for an adventure" in msg.message  or "Mrrrrgl mrrrgl mrrrrrrgl mrrrgl. Mrrrrrrrrrrrgl mrrrrgl mrrrrrrrgl mrrrrrrgl mrrrrrrrrl. Mrrrrrgl." in msg.message or "As you were strolling through the forest" in msg.message or "It was a cool and refreshing night" in msg.message or "In the forest you came across a tavern" in msg.message or "In the forest you met a redhead woman" in msg.message or "Nothing interesting happened." in msg.message or "You found yourself in a land you where you did not want to appear again." in msg.message or "Wandering around, you saw a little golden ball flying around" in msg.message or 'On your quest you came to the town of Honeywood' in msg.message:  
        id = await getId(event.client)
        stat = stats[id]
        if stat.quest and stat.fullquest:
            await asyncio.sleep(randint(10,15))
            await event.respond("🗺Quests")

@events.register(events.NewMessage(from_users=cw_id, pattern=definitivequest_pattern, incoming=True))
async def Handle_Do_quest(event):
    id = await getId(event.client)
    stat = stats[id]
    await asyncio.sleep(1) 
    if stat.quest and stat.fullquest:
        if stat.foray:
            await asyncio.sleep(2)
            await event.message.buttons[1][0].click()
        elif stat.forest:
            await asyncio.sleep(2)
            await event.message.buttons[0][0].click()
        elif stat.swamp:
            await asyncio.sleep(2)
            await event.message.buttons[0][1].click()
        elif stat.valley:
            await asyncio.sleep(2)
            await event.message.buttons[0][2].click()
        elif stat.random:
            if '🔥' in event.message.text:
                temp = event.message.text.split('\n\n')
                for i in range(0,3):
                    if '🔥' in temp[i]:
                        await asyncio.sleep(2)
                        await event.message.buttons[0][i].click()
            elif '🔥🎩' in event.message.text:
                temp = event.message.text.split('\n\n')
                for i in range(0,3):
                    if '🔥🎩' in temp[i]:
                        await asyncio.sleep(2)
                        await event.message.buttons[0][i].click()
            elif  '🎩' in event.message.text:
                temp = event.message.text.split('\n\n')
                for i in range(0,3):
                    if '🎩' in temp[i]:
                        await asyncio.sleep(2)
                        await event.message.buttons[0][i].click()
            else:
                await asyncio.sleep(2)
                await event.message.buttons[0][choice(stat.favQuest)].click()
        
        
        
#STAMINA Y QUEST END

#INTERVINE, TRADER Y PLEDGe
@events.register(events.NewMessage(from_users=cw_id, pattern=foray_pattern, incoming=True))
async def handle_Stop_Foray(event):
    id = await getId(event.client)
    stat = stats[id]
    if stat.gointervine and stat.go:
        await asyncio.sleep(randint(15,30))
        await event.message.buttons[0][0].click()

@events.register(events.NewMessage(from_users=cw_id, pattern=pledge_pattern, incoming=True))
async def handle_pldege_accept(event):
    id = await getId(event.client)
    stat = stats[id]
    if stat.go and stat.pledge:
        await asyncio.sleep(randint(5,15))
        await event.respond("/pledge")   

@events.register(events.NewMessage(from_users=cw_id, pattern=trader_pattern, incoming=True))
async def handle_trader(event):
    id = await getId(event.client)
    stat = stats[id]
    if(stat.traderId is not None) and stat.trader and stat.go:
        idxq = event.message.text.find("carry")
        cant = event.message.text[idxq+6:idxq+9]
        await asyncio.sleep(2)
        await event.respond("/sc " + stat.traderId + " " + (str)(cant))
#INTERVINE END

#handler evento hallowin
@events.register(events.NewMessage(pattern=msg_evento_pattern, incoming=True))
async def handle_evento_hunt(event):
    if event.chat_id != cw_id:
        await event.client.send_message('chtwrsbot',event.text)

#HUNT Y MOBS
@events.register(events.NewMessage(from_users=cw_id, pattern=mods_pattern, incoming=True))
async def handle_mobs(event):
    id = await getId(event.client)
    stat = stats[id]
    if (stat.mobrenvio != []) and stat.hunt and stat.mobs:
        await asyncio.sleep(1)
        gmobs=stat.mobrenvio 
        for i in gmobs:
            await event.client.get_dialogs()
            temp = await event.client.get_entity(i)
            await asyncio.sleep(2)
            await event.client.forward_messages(temp, event.message)
    else:
        print('no group')
        
@events.register(events.NewMessage(pattern=mods_pattern, incoming=True))
async def handle_bichos_hunt(event):
    if event.chat_id != cw_id:
        m=event.message.text
        f=re.findall(r'\d+',m)    
        level=int(f[1])
        id = await getId(event.client)
        stat = stats[id]
        lvl=int(stat.lvl)
        stamina=int(stat.stamina)
        hp=int(stat.hp)
        if (level > lvl-10 and level < lvl+5 and stamina != 0 and hp >= hp/3) and (stat.hunt and stat.mobs):
            await event.client.send_message('chtwrsbot',event.text)

@events.register(events.NewMessage(pattern=ambush_pattern, incoming=True))#buscar pattern del ambush
async def handle_ambush_hunt(event):
    if event.chat_id != cw_id:
        m=event.message.text
        f=re.findall(r'\d+',m)    
        level=int(f[1])
        id = await getId(event.client)
        stat = stats[id]
        lvl=int(stat.lvl)
        stamina=int(stat.stamina)
        hp=int(stat.hp)
        if (level > lvl-10 and level < lvl+5 and stamina != 0 and hp > 500) and (stat.hunt and stat.mobs):
            await event.client.send_message('chtwrsbot',event.text) 

@events.register(events.NewMessage(from_users=cw_id, pattern=alive_pattern, incoming=True))
async def handle_if_alive(event):
    await asyncio.sleep(2)
    await event.message.buttons[0][0].click()
    await asyncio.sleep(2)
    await event.message.buttons[0][1].click()  
    await asyncio.sleep(2)
    await event.client.send_message('chtwrsbot',"🏅Me")

@events.register(events.NewMessage(from_users=cw_id, pattern=dead_pattern, incoming=True))
async def handle_if_death(event):
    await asyncio.sleep(2)
    await event.message.buttons[0][0].click()
    await asyncio.sleep(2)
    await event.message.buttons[0][1].click()  
    await asyncio.sleep(2)
    await event.client.send_message('chtwrsbot',"🏅Me")
#HUNT Y MOBS END

#auction
@events.register(events.NewMessage(chats=-1001209424945, incoming=True))
async def compras_auction(event):
    id = await getId(event.client)
    stat = stats[id]
    dict=stat.compras.keys()
    msg=event.message.text
    if ('🧩Chaos stone shard' in msg) and ('🧩Chaos stone shard' in dict):
            h='🧩Chaos stone shard'
            b=stat.compras[i]
            msg1=re.findall(r'\d+',msg)
            c=str(b)
            d=str(msg1[0])
            await event.client.send_message("@chtwrsbot",'/bet_{}_{}'.format(d,c))
    
    elif ('🧩Force stone shard' in msg) and ('🧩Force stone shard' in dict):
            h='🧩Force stone shard'
            b=stat.compras[i]
            msg1=re.findall(r'\d+',msg)
            c=str(b)
            d=str(msg1[0])
            await event.client.send_message("@chtwrsbot",'/bet_{}_{}'.format(d,c))
    else:
        if ('🧩Chaos stone shard' or '🧩Force stone shard') is not msg:
            for i in dict:
                if i in msg:
                    b=stat.compras[i]
                    msg1=re.findall(r'\d+',msg)
                    c=str(b)
                    d=str(msg1[0])
                    #await event.client.send_message("@chtwrsbot",'/bet_'+d+'_'+c)
                    await event.client.send_message("@chtwrsbot",'/bet_{}_{}'.format(d,c))
                else:
                    pass

@events.register(events.NewMessage(from_users=408101137, incoming=True))
async def bets_auction(event):
    id = await getId(event.client)
    stat = stats[id]
    msg=event.message.text
    if "Your bet on" in msg:
        msg1=re.findall(r'\d+', msg)
        lot=msg1[-1]
        val=stat.lots.keys()
        if lot in val:
            await asyncio.sleep(randint(450,800))
            print("viendo ob")
            await event.client.send_message("@chtwrsbot","/bet_"+ str(lot))
        else:
            pass

@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def auto_OB_auction(event):
    id = await getId(event.client)
    stat = stats[id]
    msg=event.message.text
    if "To make a bet:" in msg:
        msg1=re.findall(r'\d+', msg)
        lot=str(msg1[-2])
        real_bet=int(msg1[-1])
        val=stat.lots.keys()
        if lot in val:
            lim=stat.lots[lot]
            limt=int(lim)
            if limt>real_bet:
                await event.client.send_message("@chtwrsbot","/bet_"+ str(lot)+"_"+str(real_bet))
                print("haciendo ob")
            else:
                pass


@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def validar_pogs(event):
    if '🌟Congratulations! New level!🌟' in event.message.text:
        id = await getId(event.client)
        stat = stats[id]
        n= int(stat.oro)
        b=int(stat.maxpog)*120
        if stat.maxpog !=0 and n > b:
            global vu
            vu=n/120
            await asyncio.sleep(20)
            await event.client.send_message("@chtwrsbot",'📦Resources')
                
@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def auto_pogs(event):
    id = await getId(event.client)
    stat = stats[id]
    if 'Storage' in event.message.text and stat.autopogs:
        text=event.message.text
        global thread
        global leather

        idx=text.find('Thread ')
        if idx == -1:
            thread=0
        else:
            idy=text.find('\n',idx)
            thread=(int)(text[idx +8:idy-1])

        idx=text.find('Leather ')
        if idx == -1:
            leather = 0
        else:
            idy=text.find('\n',idx)
            leather=(int)(text[idx +9:idy-1])
            
        cuero=round(leather//2)
        hilo=round(thread//12)
        if cuero > 0 and hilo > 0:
            if vu<=cuero and vu<=hilo:
                await asyncio.sleep(3)
                await craft_pogs(vu,client=event.client)
                print('hecho')
            elif vu>cuero and vu<=hilo:
                await asyncio.sleep(3)
                await craft_pogs(cuero,client=event.client)
                print('hecho1')
            elif vu>hilo and vu<=cuero:
                await asyncio.sleep(3)
                await craft_pogs(hilo,client=event.client)
                print('hecho2')

        else:
            c=int(stat.maxpog)*2
            h=int(stat.maxpog)*12
            if cuero < c:
                await asyncio.sleep(3)
                await event.client.send_message("@chtwrsbot",'/wtb_20_'+str(c-leather))
                    
            if hilo < h:
                await asyncio.sleep(3)
                await event.client.send_message("@chtwrsbot",'/wtb_01_'+str(h-thread))
#auction end

'''#mensajes forward
@events.register(events.NewMessage(from_users=cw_id, incoming=True))
async def auto_forward(event):
    id = await getId(event.client)
    stat = stats[id]
    text = stat.msg.keys()
    for i in text:
        if i in event.message.text:
            chat = stat.msg[i]
            await asyncio.sleep(3)
            await event.client.forward_messages(chat, event.message)'''




################# HANDLERS BOT #################

@events.register(events.NewMessage(pattern='/start'))
async def handle_StartBot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    welcomeMsg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nHola. Bienvenido al bot de control de Iron Script\n❗️POR FAVOR FIJE ESTE MSG EN EL CHAT❗️\nLos comandos son:\n\n/start para ver este mensaje\n/status Para ver los stats de tu player\n/suscrip para ver las funciones contratadas por esta cuenta\n/config para ver la configuración actual del script\n'
    #if stat.atk is not None:
        #welcomeMsg+= '/atk_on para coger las ordenes\n/atk_off para defender SIR\n/no_atk para no coger ordenes de attaque'\n\n
    if stat.quest:
        welcomeMsg+= '/quest para configurar las quest\n'
    if stat.hunt:
        welcomeMsg+= "/hunt para configurar la caza de mobs\n"
    if stat.arena:
        welcomeMsg+= "/arena_time [hh:mm] para cambiar la hora que se hace las arenas(valido a partir del proximo dia)\n"
    if stat.go:
        welcomeMsg+= "/go para cambiar las opciones del intervine\n"
    if stat.auction:
        welcomeMsg+= '/auction para ver los ajustes del auction\n'
    if stat.pogs:
        welcomeMsg+= '/pogs para ver los ajustes del autocraft de pogs'
    welcomeMsg+= '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹'
    await event.respond(welcomeMsg)

@events.register(events.NewMessage(pattern='/status'))
async def handle_status_bot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    await event.respond(stat.jugador())

@events.register(events.NewMessage(pattern='/suscrip'))
async def handle_suscrip_bot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    await event.respond(stat.suscripcion())

@events.register(events.NewMessage(pattern='/config'))
async def handle_config_bot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    await event.respond(stat.config())
#commando quest
buttonList = [Button.inline('🌲Forest', data='Forest'),Button.inline('🍄Swamp', data='Swamp'),Button.inline('🏔Valley', data='Valley')]
buttonList1 = [Button.inline('🏇Foray', data='Foray'),Button.inline('🎲Random', data='Random'),Button.inline('❌', data='Cerrar')]

buttonList2 = [Button.inline('🛵Quest✅', data='/quest_on'),Button.inline('🛵Quest❌', data='/quest_off')]#,Button.inline('🛵Target', data='/change_quest_target')]

@events.register(events.NewMessage(pattern='/quest'))
async def handle_quest_bot(event):
    id = event.peer_id.user_id
    await event.respond( msg_quest(id), buttons=[buttonList2,buttonList,buttonList1])

@events.register(events.CallbackQuery())
async def handleButtomBot1(event):
    id = event.original_update.user_id
    stat = stats[id]
    listEvents = stats[id].favQuest
    #stat.sort()
    if event.data == b'/quest_on':
        try:
            stat.fullquest = True
            await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass
    elif event.data == b'/quest_off':
        try:
            stat.fullquest = False
            await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass    
    elif event.data == b'Forest':
        try:
            if 0 in listEvents:
                stat.foray = False
                stat.forest = True
                stat.swamp = False
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(0)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
            else:
                stat.foray = False
                stat.forest = True
                stat.swamp = False
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(0)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass
    elif event.data == b'Swamp':
        #listEvents = stats[id].favQuest
        try:
            if 1 in listEvents:
                stat.foray = False
                stat.forest = False
                stat.swamp = True
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(1)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
            else:
                stat.foray = False
                stat.forest = False
                stat.swamp = True
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(1)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass
    elif event.data == b'Valley':
        #listEvents = stats[id].favQuest
        try:
            if 2 in listEvents:
                stat.foray = False
                stat.forest = False
                stat.swamp = False
                stat.valley = True
                stat.random = False
                listEvents.clear() 
                listEvents.append(2)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
            else:
                stat.foray = False
                stat.forest = False
                stat.swamp = False
                stat.valley = True
                stat.random = False
                listEvents.clear() 
                listEvents.append(2)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass
    elif event.data == b'Foray':
        #listEvents = stats[id].favQuest
        try:
            if 3 in listEvents:
                stat.foray = True
                stat.forest = False
                stat.swamp = False
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(3)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
            else:
                stat.foray = True
                stat.forest = False
                stat.swamp = False
                stat.valley = False
                stat.random = False
                listEvents.clear() 
                listEvents.append(3)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
        except:
            pass
    elif event.data == b'Random':
        #listEvents = stats[id].favQuest
        try:
            if 4 in listEvents:
                stat.foray = False
                stat.forest = False
                stat.swamp = False
                stat.valley = False
                stat.random = True
                listEvents.clear() 
                listEvents.append(0)
                listEvents.append(1)
                listEvents.append(2)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
            else:
                stat.foray = False
                stat.forest = False
                stat.swamp = False
                stat.valley = False
                stat.random = True
                listEvents.clear() 
                listEvents.append(0)
                listEvents.append(1)
                listEvents.append(2)
                await event.edit(msg_quest(id),buttons=[buttonList2,buttonList,buttonList1])
                #await event.answer('Quest Favorito Cambiado!', alert=True)
        except:
            pass
    elif event.data == b'Cerrar':
        try:
            welcomeMsg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nLos comandos son:\n\n/start para ver este mensaje\n/status Para ver los stats de tu player\n/suscrip para ver las funciones contratadas por esta cuenta\n/config para ver la configuración actual del script\n'
            #if stat.atk is not None:
                #welcomeMsg+= '/atk_on para coger las ordenes\n/atk_off para defender SIR\n/no_atk para no coger ordenes de attaque'\n\n
            if stat.quest:
                welcomeMsg+= '/quest para configurar las quest\n'
            if stat.hunt:
                welcomeMsg+= "/hunt para configurar la caza de mobs\n"
            if stat.arena:
                welcomeMsg+= "/arena_time [hh:mm] para cambiar la hora que se hace las arenas(valido a partir del proximo dia)\n"
            if stat.go:
                welcomeMsg+= "/go para cambiar las opciones del intervine\n"
            if stat.auction:
                welcomeMsg+= '/auction para ver los ajustes del auction\n'
            if stat.pogs:
                welcomeMsg+= '/pogs para ver los ajustes del autocraft de pogs'
            welcomeMsg+= '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹'
            await event.edit(welcomeMsg)
            
        except:
            pass
#comando quest end

#comando hunt
buttonhunt = [Button.inline('👾ON✅', data='huntOn'),Button.inline('👾OFF❌',data='huntOff')]
buttonhunt1 = [Button.inline('Add👂', data='addgrp'),Button.inline('Del👂',data='delgrp')]
buttonhunt2 = [Button.inline('HELP👍', data='addhlp'),Button.inline('HELP👎',data='delhlp'),Button.inline('❌', data='Cerrar')]

@events.register(events.NewMessage(pattern='/hunt'))
async def handle_mobs_bot(event):
    id = event.peer_id.user_id
    await event.respond(msg_hunt(id), buttons=[buttonhunt,buttonhunt1,buttonhunt2])

@events.register(events.CallbackQuery())
async def handleButtomBot(event):
    id = event.original_update.user_id
    stat = stats[id]
    if event.data == b'huntOn':
        try:
            if stat.mobs:
                await event.edit(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
            else:
                stat.mobs = True
                await event.edit(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
        except:
            pass
    elif event.data == b'huntOff':
        try:
            if stat.mobs == False:
              await event.edit(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
            else:
                stat.mobs = False
                await event.edit(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
        except:
            pass
    elif event.data == b'addgrp':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el id del grupo\nEj: -100243794685\n')
                grp = await conv.get_response()
                list = grp.text
                stat.agregar_hunter(list)
                await conv.send_message(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
                await event.answer('Agregado con éxito')
        except:
            pass
    elif event.data == b'delgrp':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el id del grupo a borrar\nEj: -100243794685\n')
                grp = await conv.get_response()
                list = grp.text
                stat.borrar_hunter(list)
                await conv.send_message(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
                await event.answer('Eliminnación exitosa')
        except:
            pass
    elif event.data == b'addhlp':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el id del grupo\nEj: -100243794685\n')
                grp = await conv.get_response()
                list = grp.text
                stat.agregar_envio(list)
                await conv.send_message(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
                await event.answer('Agregado con éxito')
        except:
            pass
    elif event.data == b'delhlp':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el id del grupo a borrar\nEj: -100243794685\n')
                grp = await conv.get_response()
                list = grp.text
                stat.borrar_envio(list)
                await conv.send_message(msg_hunt(id),buttons=[buttonhunt,buttonhunt1,buttonhunt2])
                await event.answer('Eliminnación exitosa')
        except:
            pass
    elif event.data == b'Cerrar':
        try:
            welcomeMsg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nLos comandos son:\n\n/start para ver este mensaje\n/status Para ver los stats de tu player\n/suscrip para ver las funciones contratadas por esta cuenta\n/config para ver la configuración actual del script\n'
            #if stat.atk is not None:
                #welcomeMsg+= '/atk_on para coger las ordenes\n/atk_off para defender SIR\n/no_atk para no coger ordenes de attaque'\n\n
            if stat.quest:
                welcomeMsg+= '/quest para configurar las quest\n'
            if stat.hunt:
                welcomeMsg+= "/hunt para configurar la caza de mobs\n"
            if stat.arena:
                welcomeMsg+= "/arena_time [hh:mm] para cambiar la hora que se hace las arenas(valido a partir del proximo dia)\n"
            if stat.go:
                welcomeMsg+= "/go para cambiar las opciones del intervine\n"
            if stat.auction:
                welcomeMsg+= '/auction para ver los ajustes del auction\n'
            if stat.pogs:
                welcomeMsg+= '/pogs para ver los ajustes del autocraft de pogs'
            welcomeMsg+= '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹'
            await event.edit(welcomeMsg)
            
        except:
            pass
#hunt end

#arena time
@events.register(events.NewMessage(pattern='/arena_time'))
async def handle_set_arena_time_bot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    stat.arenaTime = event.message.text.split(' ')[1]
    schedule1.cancel_job(stat.arenaDeamon)
    stat.arenaDeamon = schedule1.every().day.at(stat.arenaTime).do(startArenas, cliente=stat.cuenta)    
    await event.respond(stat.config())
#arena time end

#intervine
buttongo=[Button.inline('⛔️ON✅', data='goOn'),Button.inline('⛔️OFF❌',data='goOff')]
buttongo1=[Button.inline('Trader✅', data='traderOn'),Button.inline('Trader❌',data='traderOff'),Button.inline('🍖RSS🍖',data='rssId')]
buttongo2=[Button.inline('🎁Pledge✅', data='pledgeOn'),Button.inline('🎁Pledge❌',data='pledgeOff'),Button.inline('❌',data='Cerrar')]


@events.register(events.NewMessage(pattern='/go'))
async def handle_go_bot(event):
    id = event.peer_id.user_id
    await event.respond( msg_go(id), buttons=[buttongo,buttongo1,buttongo2])

@events.register(events.CallbackQuery())
async def handleButtomBot2(event):
    id = event.original_update.user_id
    stat = stats[id]
    if event.data == b'goOn':
        try:
            if stat.gointervine:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.gointervine = True
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    if event.data == b'goOff':
        try:
            if stat.gointervine == False:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.gointervine = False
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    if event.data == b'traderOn':
        try:
            if stat.trader:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.trader = True
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    if event.data == b'traderOff':
        try:
            if stat.trader == False:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.trader = False
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    if event.data == b'pledgeOn':
        try:
            if stat.pledge:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.pledge = True
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    if event.data == b'pledgeOff':
        try:
            if stat.pledge == False:
              await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
            else:
                stat.pledge = False
                await event.edit(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
        except:
            pass
    elif event.data == b'rssId':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el id del recurso\nEj: 02\n')
                grp = await conv.get_response()
                list = grp.text
                stat.traderId = list
                await conv.send_message(msg_go(id),buttons=[buttongo,buttongo1,buttongo2])
                await event.answer('Recurso gardado')
        except:
            pass
    elif event.data == b'Cerrar':
        try:
            welcomeMsg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nLos comandos son:\n\n/start para ver este mensaje\n/status Para ver los stats de tu player\n/suscrip para ver las funciones contratadas por esta cuenta\n/config para ver la configuración actual del script\n'
            #if stat.atk is not None:
                #welcomeMsg+= '/atk_on para coger las ordenes\n/atk_off para defender SIR\n/no_atk para no coger ordenes de attaque'\n\n
            if stat.quest:
                welcomeMsg+= '/quest para configurar las quest\n'
            if stat.hunt:
                welcomeMsg+= "/hunt para configurar la caza de mobs\n"
            if stat.arena:
                welcomeMsg+= "/arena_time [hh:mm] para cambiar la hora que se hace las arenas(valido a partir del proximo dia)\n"
            if stat.go:
                welcomeMsg+= "/go para cambiar las opciones del intervine\n"
            if stat.auction:
                welcomeMsg+= '/auction para ver los ajustes del auction\n'
            if stat.pogs:
                welcomeMsg+= '/pogs para ver los ajustes del autocraft de pogs'
            welcomeMsg+= '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹'
            await event.edit(welcomeMsg)
            
        except:
            pass
#intervine end

#solo admin 
'''@events.register(events.NewMessage(pattern='/save'))
async def handle_savePlayer_bot(event):
    id = event.peer_id.user_id
    stat = stats[id]
    if stat.admin:
        open_bbdd()
        await asyncio.sleep(2)
        await event.respond('Datos guardados')'''

#auction
buttonauct=[Button.inline('🏦ADD🏦', data='auctAdd'),Button.inline('🏦DEL🏦',data='delauct'),Button.inline('🏦Clear🏦', data='clearAuct')]
buttonauct1=[Button.inline('➕Lot➕', data='addlot'),Button.inline('➖Lot➖',data='dellot'),Button.inline('✖️Clear✖️',data='clearLot')]
buttonauct2=[Button.inline('❌',data='Cerrar')]


@events.register(events.NewMessage(pattern='/auction'))
async def handle_auction_bot(event):
    id = event.peer_id.user_id
    stat=stats[id]
    if stat.auction:
        await event.respond( msg_auction(id), buttons=[buttonauct,buttonauct1,buttonauct2])

@events.register(events.CallbackQuery())
async def handleButtomBot3(event):
    id = event.original_update.user_id
    stat = stats[id]
    if event.data == b'auctAdd':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el nombre del item respetando emojis, espacios y mayusculas.\nEj: Manticore Gloves +\nImperial Axe +\n🧩Force stone shard\n🖋Scroll of Engraving\nChaos stone\n📃Blessed Cloak recipe\nTenga en cuenta que suscribirse a joyas y totems puede ser confuso para el script')
                itm = await conv.get_response()
                item = itm.text
                await conv.send_message('Introduzca el valor maximo a pagar')
                pre = await conv.get_response()
                precio=pre.text
                stat.compras[item]=precio
                await conv.send_message(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
                await event.answer('Suscripcion gardada')
        except:
            pass
    if event.data == b'delauct':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el nombre del item a borrar respetando emojis, espacios y mayusculas. En caso de armaduras y armas agregar al nombre el simbolo +\nEj: Manticore Gloves +\nImperial Axe +\n🧩Force stone shard\n🖋Scroll of Engraving\nChaos stone\n📃Blessed Cloak recipe\n')
                itm = await conv.get_response()
                item = itm.text
                del stat.compras[item]
                await conv.send_message(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
                await event.answer('Suscripcion gardada')
        except:
            pass
    if event.data == b'clearAuct':
        try:
            stat.compras.clear()
            await event.edit(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
            await event.answer('Suscripcion gardada')
        except:
            pass
    if event.data == b'addlot':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el lote para hacerle seguimiento')
                itm = await conv.get_response()
                item = itm.text
                await conv.send_message('Introduzca el valor maximo a pagar')
                pre = await conv.get_response()
                precio=pre.text
                stat.lots[item]=precio
                await conv.send_message(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
                await event.answer('Suscripcion gardada')
        except:
            pass
    if event.data == b'dellot':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el lote que quiere dejar de seguir')
                itm = await conv.get_response()
                item = itm.text
                del stat.lots[item]
                await conv.send_message(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
                await event.answer('Suscripcion gardada')
        except:
            pass
    if event.data == b'clearLot':
        try:
            stat.lots.clear()
            await event.edit(msg_auction(id),buttons=[buttonauct,buttonauct1,buttonauct2])
            await event.answer('Suscripcion gardada')
        except:
            pass

#pogs
buttonpog=[Button.inline('ON✅', data='pogOn'),Button.inline('OFF❌',data='pogOff')]
buttonpog1=[Button.inline('👝Min pogs👝', data='minPog'),Button.inline('❌',data='Cerrar')]
buttonpog2=[Button.inline('❗️Predeterminado❗️',data='restart')]

@events.register(events.NewMessage(pattern='/pogs'))
async def handle_pogs_bot(event):
    id = event.peer_id.user_id
    stat=stats[id]
    if stat.pogs:
        await event.respond(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])

@events.register(events.CallbackQuery())
async def handleButtomBot4(event):
    id = event.original_update.user_id
    stat = stats[id]

    if event.data == b'pogOn':
        if stat.autopogs:
            await event.edit(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])
        else:
            stat.autopogs=True
            await event.edit(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])

    if event.data == b'pogOff':
        try:
            if stat.autopogs == False:
                await event.edit(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])
            else:
                stat.autopogs=False
                await event.edit(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])
        except:
            pass

    if event.data == b'minPog':
        try:
            async with event.client.conversation(event.original_update.user_id, timeout=300) as conv:
                await conv.send_message('🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nIntroduce el minimo de pogs a craftear en cada vuelta')
                itm = await conv.get_response()
                stat.maxpog = int(itm.text)
                await conv.send_message(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])
                await event.answer('gardado')
        except:
            pass
    
    if event.data == b'restart':
        try:
            stat.maxpog = 5
            await event.edit(msg_pogs(id), buttons=[buttonpog,buttonpog1,buttonpog2])
        except:
            pass

    elif event.data == b'Cerrar':
        try:
            welcomeMsg = '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\nLos comandos son:\n\n/start para ver este mensaje\n/status Para ver los stats de tu player\n/suscrip para ver las funciones contratadas por esta cuenta\n/config para ver la configuración actual del script\n'
            #if stat.atk is not None:
                #welcomeMsg+= '/atk_on para coger las ordenes\n/atk_off para defender SIR\n/no_atk para no coger ordenes de attaque'\n\n
            if stat.quest:
                welcomeMsg+= '/quest para configurar las quest\n'
            if stat.hunt:
                welcomeMsg+= "/hunt para configurar la caza de mobs\n"
            if stat.arena:
                welcomeMsg+= "/arena_time [hh:mm] para cambiar la hora que se hace las arenas(valido a partir del proximo dia)\n"
            if stat.go:
                welcomeMsg+= "/go para cambiar las opciones del intervine\n"
            if stat.auction:
                welcomeMsg+= '/auction para ver los ajustes del auction\n'
            if stat.pogs:
                welcomeMsg+= '/pogs para ver los ajustes del autocraft de pogs'
            welcomeMsg+= '🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹'
            await event.edit(welcomeMsg)
            
        except:
            pass


