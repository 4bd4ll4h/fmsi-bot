import sqlite3

class dbQuery():
    def __init__(self, db):
        self.db = db


    #check and insert new account into the dataBase
    def setAccount(self, userId,userChat):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        isRegistered = cur.execute(f'SELECT * FROM users WHERE UserID={userId}').fetchone()
        con.commit()

        isRegistered = True if isRegistered else False

        if not isRegistered:
            cur.execute(f'Insert into users (UserID,userChat) values ({userId},"{userChat}")')
            con.commit()
        
        return isRegistered
    #set the Student grade Level
    def setLev(self, lev,userId):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'Update users set Lev= "{lev}" WHERE UserID={userId}')
        con.commit()
        con.close()
    def getSubUser(self,patch:str):
        con =sqlite3.connect(self.db)
        cur=con.cursor()
        res=cur.execute(f'SELECT userChat from users WHERE PatchNews = true and Lev like "{patch}"').fetchall()
        con.commit()
        con.close()
        return res
    def setUserInfo(self,userId,column,data):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(f'Update users set {column}= {data} WHERE UserID={userId}')
        con.commit()
        con.close()
    def setIndex(self,userID,index):
        con=sqlite3.connect(self.db)
        cur=con.cursor()
        cur.execute(f'''UPDATE users set SIndex="{index}" WHERE UserID={userID}
        ''')
        con.commit()
        con.close()
    def checkInfo(self, userId,info):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        isRegistered = cur.execute(f'SELECT {info} FROM users WHERE UserID={userId}').fetchone()
        con.commit()

        isRegistered = True if isRegistered[0] else False

        
        return isRegistered
        
    def getLanguage(self,userId):
        con=sqlite3.connect(self.db)
        cur=con.cursor()
        lang= cur.execute(f"SELECT Lang from users WHERE UserID={userId}").fetchone()
        con.commit()
        con.close()
        return lang[0] if lang else 'ar'
    def getMessgesIDs(self,dirs):
        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        ids=cur.execute(f'SELECT chatId,messageId,content_type FROM messages WHERE dir = "{dirs}"').fetchall()
        return ids
    def checkDirCode(self,d):
        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        codes=cur.execute(f'SELECT ar , en FROM codeNames WHERE dir = "{d}"').fetchone()
        conn.commit()
        conn.close()
        if codes:
            if not codes[0]:
                return ['ar']
            elif not codes[1]:
                return ['en']
        else:
            return ['ar','en']
        return True
    def insertMessageId(self,dirs,chatId,messageId,content_type):
        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        cur.execute(f''' INSERT INTO messages (dir, messageId,chatId,content_type)
         VALUES
          ("{dirs}","{messageId}","{chatId}","{content_type}")
        ''')
        conn.commit()
        conn.close()
    def setDir(self, lang,dirs ,name):
        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        print(lang)
        print(dirs)
        print(name)
        try:
            cur.execute(f''' INSERT INTO codeNames (dir, {lang})
            VALUES
             ("{dirs}","{name}")
             ON CONFLICT(dir)
             DO UPDATE SET {lang}="{name}";
            ''')
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def getMessagesDir(self,dirs):

        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        res=cur.execute(f'SELECT dir FROM messages WHERE dir like "{dirs}%"').fetchall()[0]
        conn.close
        return res
    def getDirName(self , dr,lang):
        conn=sqlite3.connect(self.db)
        cur=conn.cursor()
        res=cur.execute(f'SELECT {lang} FROM codeNames WHERE dir like "{dr}%"').fetchone()[0]
        return res



        
    

