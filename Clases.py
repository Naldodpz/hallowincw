class clasePlayer:
    def  __init__(self,cuenta=None,quest=None,craft=None,arena=None,go=None,auction=None,hunt=None,pogs=None,scroll=None,orden=None,ranger=False,admin=False):
        #parametros del suscripcion
        self.cuenta=cuenta
        self.quest=quest
        self.craft=craft
        self.arena=arena
        self.go=go
        self.auction=auction
        self.hunt=hunt
        self.pogs=pogs
        self.scroll=scroll
        self.orden=orden
        self.ranger=ranger
        self.admin=admin

        #info player
        self.player=None
        self.lvl=None
        self.Maxhp=None
        self.hp=None
        self.Maxstamina=None
        self.stamina=None
        self.oro=None
        self.mana=None
        self.Maxmana=None
        self.accion=None

        #funciones editables
        #quest
        self.fullquest=True
        self.foray=False
        self.forest=False
        self.swamp=False
        self.valley=False
        self.random=True
        self.favQuest=[0,1,2]

        #mobs
        self.mobs=True
        self.grouphunter=[]
        self.mobrenvio=[]
        
        #arena
        self.goarena=True
        self.arenaTime='09:30'
        self.arenaDeamon = None
        
        #intervine
        self.gointervine=True
        self.trader=True
        self.traderId='02'
        self.pledge=True
        
        #auction
        self.clarity=False
        self.order=False
        self.armas=False
        self.force=False
        self.forceshard=False
        self.chaos=False
        self.chaosshard=False
        self.lots={}
        self.compras={}

        #craft
        self.gocraft=None
        self.crafrecipe=None
        self.horacraft=None
        self.cantcraft=0

        #pogs
        self.autopogs=True
        self.maxpog=5

        #reenvios msg
        self.forward=False
        self.msg={}

#metodos de la clase
    #lotes auction
    def agregar_lot(self,elem=0):
        self.lots.append(elem)
    
    def borrar_lot(self,elem=0):
        self.lots.remove(elem)
    
    #grupos caza
    def agregar_hunter(self,elem=0):
        self.grouphunter.append(elem)
    
    def borrar_hunter(self,elem=0):
        self.grouphunter.remove(elem)
    
    def agregar_envio(self,elem=0):
        self.mobrenvio.append(elem)
    
    def borrar_envio(self,elem=0):
        self.mobrenvio.remove(elem)
    
    #g=m.split()
    #f=re.findall(r'\d+',m)
    def jugador(self):
      mes="""
        Info actual del player:
        ---------------------
        Player: %s
        Level: %s🏅
        HP max: %s❤️
        HP: %s💔
        Stamina max: %s🔋
        Stamina: %s🧪
        Mana max: %s💧
        Mana: %s💦
        Oro: %s💰""" % (self.player,self.lvl,self.Maxhp,self.hp,self.Maxstamina,self.stamina,self.Maxmana,self.mana,self.oro)
      return mes
    
    def suscripcion(self):
        mes="""
        Funciones contratadas:
        ---------------------
        🎫Player: %s
        🛵Auto quest: %s
        🔬Craft diarios: %s
        🤺Arenas: %s
        🚫Intervine: %s
        📊Auction: %s
        🏇MobsHunt: %s
        💸Auto pogs: %s
        🗞Scrolles: %s
        📝Orden Batalla: %s""" % (self.player,self.quest,self.craft,self.arena,self.go,self.auction,self.hunt,self.pogs,self.scroll,self.orden)
        return mes

    def config(self):
        mes="""
        Configuracion actual script:
        ---------------------
        Player: %s
        Quest: %s
          Full Staminas: %s
          Forest: %s
          Swamp: %s
          Valley: %s
          Random: %s
          Forays: %s
        Arena: %s
          Arenas horario: %s
        Crafts: %s
          cantidad de craft: %s
          Craft recipe: %s
          craft horario: %s
        Caza: %s
          MobsHunt: %s
          Grupos de escucha: %s
          Grupos de envio: %s
        Intervine: %s
          Trader rss: %s
        Scrolles: %s
        Orden: %s
          Ranger aiming: %s
        Auction: %s
          Clarity: %s
          Order: %s
          Armas: %s
          Chaos stone: %s
          Chaos shard: %s
          Force stone: %s
          Force shard: %s
          Lotes vigilados: %s
        
        ...................""" % (self.player,self.quest,self.fullquest,self.forest,self.swamp,self.valley,self.random,self.foray,self.arena,self.arenaTime,self.craft,self.gocraft,self.crafrecipe,self.horacraft,self.hunt,self.mobs,self.grouphunter,self.mobrenvio,self.go,self.traderId,self.scroll,self.orden,self.ranger,self.auction,self.clarity,self.order,self.armas,self.chaos,self.chaosshard,self.force,self.forceshard,self.lots)
        return mes
