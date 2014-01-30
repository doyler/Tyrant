import httplib
import hashlib
import time
import gzip
import StringIO
import json

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

myTyrant.setUserFlag("autopilot", "1")
myTyrant.setActiveDeck("3")
fight = myTyrant.doArenaFight("5871864") #nether

for key, value in fight.iteritems():
    print key
    #if type(value) == type(['']):
            #for sub_value in value:
                #strg = str(json.dumps(sub_value))
                #for key2, value2 in strg.iteritems():
                    #print key2
    #else:
        #print value

myTyrant.setActiveDeck("2")
myTyrant.setUserFlag("autopilot", "0")

'''
messages = myTyrant.getFactionMessages()

for line in messages["messages"]:
    print line["message"]
    '''
