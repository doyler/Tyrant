import httplib
import hashlib
import time
import gzip
import StringIO
import json
#import base64
import math

class tyrant_test(object):
    def __init__(self):
        self.version = "2.9.17"
        self.flashcode = "c2a91a26a92020dfaa83b69814280527"
        self.faction_id = "1534002"
        self.user_id = "982276"
        with open('authtoken.txt', 'r') as f:
	    self.game_auth_token = f.readline()
        self.client_code = "null"

        self.headers = {
            "Connection": "keep-alive",
            "Origin": "http://kg.tyrantonline.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Referer": "http://kg.tyrantonline.com/Main.swf?"+self.version,
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8"
        }

        self.time_hash = "fgjk380vf34078oi37890ioj43"
        self.myTime = str(int(time.time())/900)

        #ccache = hashlib.md5()
        #ccache.update(self.myTime)
        #ccache.update(self.user_id)
        #ccache = ccache.hexdigest()

        self.cards = {}

    def getHash(self, time, message):
        reqHash = hashlib.md5()
        reqHash.update(message)
        reqHash.update(self.myTime)
        reqHash.update(self.time_hash)
        reqHash = reqHash.hexdigest()

        return reqHash

    def sendRequestDecompressResponse(self, message, additional):
        path = "/api.php?user_id="+self.user_id+"&message="+message
        if message == "init":
            data = "?&flashcode="+self.flashcode+"&time=0&version=&hash="+self.getHash("0", message)+"&ccache=&client_code="+self.client_code+"&game_auth_token="+self.game_auth_token+"&rc=2"
        else:
            data = "&flashcode="+self.flashcode+"&time="+self.myTime+"&version="+self.version+"&hash="+self.getHash(self.myTime, message)+"&ccache=&client_code="+str(self.client_code)+"&game_auth_token="+self.game_auth_token+"&rc=2"+additional

        conn = httplib.HTTPConnection('kg.tyrantonline.com')
        conn.set_debuglevel(0)
        conn.request("POST", path, data, self.headers)
        decompressed_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(conn.getresponse().read())).read()
        conn.close()

        return decompressed_data

    def loadCardList(self):
        for line in open('cardlist.txt'):
            (key, val) = line.rstrip('\n').split(':')
            self.cards[int(key)] = val

    def hash_encode(self, cards):
        deck = []
        com = False
        for cid in cards:
            if cid >= 1000 and cid < 2000:
                if com:
                    continue
                com = True
                deck.insert(0, cid)
                continue
            deck.append(cid)
        hash = ''
        i = 0
        while i < len(deck):
            cid = deck[i]
            if cid > 4999:
                #???
                print '7'
                continue
            else:
                #print '9: ' + str(cid)
                hash += self.base64encode(cid)
                #print '10: ' + hash
            cnt = 0
            while i < len(deck) and deck[i] == cid:
                # finding multiplier?
                cnt += 1
                i += 1
            if cnt > 1:
                # adding multiplier
                hash += self.base64encode(4000 + cnt)
        return hash

    def base64encode(self, card):
        offset = 0
        extra_char = ''
        if card > 4000:
            offset = 4000
            #print 'marco: ' + str(card)
            card = card - 4000
            #print 'polo: ' + str(card)
            extra_char = '-'
        base64string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        #print 'f of card: ' + str(card) + ' is: ' + str(int(math.floor(card/64)))
        first_char = base64string[int(math.floor(card/64))]
        #print 's of card: ' + str(card) + ' is: ' + str(card%64)
        second_char = base64string[card%64]
        return extra_char + '' + first_char + '' + second_char

    def init(self):
        message = "init"

        response = self.sendRequestDecompressResponse(message, "")
        json_data = json.loads(response)
        self.client_code = json_data["client_code"]

    def setUserFlag(self, flag, value):
        message = "setUserFlag"

        response = self.sendRequestDecompressResponse(message, "&flag="+flag+"&value="+value)
        json_data = json.loads(response)
        
        return json_data

    def setActiveDeck(self, deck):
        message = "setActiveDeck"

        response = self.sendRequestDecompressResponse(message, "&deck_id="+deck)
        json_data = json.loads(response)
        
        return json_data

    def getFactionNews(self):
        message = "getFactionNews"

        response = self.sendRequestDecompressResponse(message, "")
        json_data = json.loads(response)
        
        return json_data

    def getFactionMembers(self):
        message = "getFactionMembers"

        response = self.sendRequestDecompressResponse(message, "")
        json_data = json.loads(response)
        
        return json_data

    def getFactionMessages(self):
        message = "getFactionMessages"

        response = self.sendRequestDecompressResponse(message, "")
        json_data = json.loads(response)
        
        return json_data

    def getMap(self):
        message = "getConquestMap"

        response = self.sendRequestDecompressResponse(message, "")
        json_data = json.loads(response)
        
        return json_data

    def doArenaFight(self, enemy):
        message = "doArenaFight"

        response = self.sendRequestDecompressResponse(message, "&enemy_id="+enemy)
        json_data = json.loads(response)
        
        return json_data

myTyrant = tyrant_test()
myTyrant.init()

myTyrant.loadCardList()
members = myTyrant.getFactionMembers()

myTyrant.setUserFlag("autopilot", "1")
myTyrant.setActiveDeck("3")

values = []
valueToAdd = ''

for member in members["members"]:
    valueToAdd = members["members"][member]["name"] + " : " + members["members"][member]["user_id"] + " : "

    print valueToAdd

    fight = myTyrant.doArenaFight(members["members"][member]["user_id"])

    print json.dumps(fight)

    deck = myTyrant.cards[int(fight["defend_commander"])]
    cards = []
    cards.append(int(fight["defend_commander"]))

    for key in fight["card_map"]:
        if int(key) > 10:
            deck += ", " + myTyrant.cards[int(fight["card_map"][key])]
            cards.append(int(fight["card_map"][key]))

    valueToAdd += myTyrant.hash_encode(cards)
    values += valueToAdd

myTyrant.setActiveDeck("2")
myTyrant.setUserFlag("autopilot", "0")

with open('members_output.txt', 'wb') as f:
    for value in values:
        f.write(value + '\n')

'''
messages = myTyrant.getFactionMessages()

for line in messages["messages"]:
    print line["message"]
    '''
