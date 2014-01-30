# -*- coding: cp1252 -*-
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

    def getHash(self, message):
        reqHash = hashlib.md5()
        reqHash.update(message)
        reqHash.update(self.myTime)
        reqHash.update(self.time_hash)
        reqHash = reqHash.hexdigest()
        

    def init(self):
        message = "init"
        self.myTime = "0"
        
    
        path = "/api.php?user_id="+self.user_id+"&message="+message
        data = "?&flashcode="+self.flashcode+"&time="+self.myTime+"&version=&hash="+reqHash+"&ccache=&client_code="+self.client_code+"&game_auth_token="+self.game_auth_token+"&rc=2"
    
        conn = httplib.HTTPConnection('kg.tyrantonline.com')
        conn.set_debuglevel(1)
        conn.request("POST", path, data, self.headers)

        decompressed_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(conn.getresponse().read())).read()
        json_data = json.loads(decompressed_data)
        conn.close()
        
        self.client_code = json_data["client_code"]

    def getFactionNews(self):
        message = "getFactionNews"
        self.myTime = str(int(time.time())/900)
        reqHash = hashlib.md5()
        reqHash.update(message)
        reqHash.update(self.myTime)
        reqHash.update(self.time_hash)
        reqHash = reqHash.hexdigest()
    
        path = "/api.php?user_id="+self.user_id+"&message="+message
        data = "&flashcode="+self.flashcode+"&time="+self.myTime+"&version="+self.version+"&hash="+reqHash+"&ccache=&client_code="+str(self.client_code)+"&game_auth_token="+self.game_auth_token+"&rc=2"

        conn = httplib.HTTPConnection('kg.tyrantonline.com')
        conn.set_debuglevel(1)
        conn.request("POST", path, data, self.headers)

        decompressed_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(conn.getresponse().read())).read()
        json_data = json.loads(decompressed_data)
        
        conn.close()
        return json_data

    def getFactionMembers(self):
        message = "getFactionMembers"
        self.myTime = str(int(time.time())/900)
        reqHash = hashlib.md5()
        reqHash.update(message)
        reqHash.update(self.myTime)
        reqHash.update(self.time_hash)
        reqHash = reqHash.hexdigest()
    
        path = "/api.php?user_id="+self.user_id+"&message="+message
        data = "&flashcode="+self.flashcode+"&time="+self.myTime+"&version="+self.version+"&hash="+reqHash+"&ccache=&client_code="+str(self.client_code)+"&game_auth_token="+self.game_auth_token+"&rc=2"

        conn = httplib.HTTPConnection('kg.tyrantonline.com')
        conn.set_debuglevel(1)
        conn.request("POST", path, data, self.headers)

        decompressed_data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(conn.getresponse().read())).read()
        
        conn.close()
        return decompressed_data    

myTyrant = tyrant_test()
myTyrant.init()
print myTyrant.getFactionMembers()
